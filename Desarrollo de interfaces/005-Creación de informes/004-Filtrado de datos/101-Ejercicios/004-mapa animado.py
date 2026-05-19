#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OpenCV filesystem tree viewer with incremental animated growth + "physical" collision avoidance.

Now enforces:
- Node-node: NO overlap (hard projection)
- Node-edge: nodes keep away from branches (forces)
- Edge-edge: branches avoid crossing (forces + hard "uncross" projection)

Animation:
- 1280x720 viewer
- each second adds ONE node in hierarchical preorder (folder-by-folder feel)
- smooth relocation using persistent velocities + physics

Usage:
  python3 tree_anim_physical.py /var/www/html/dam/Primero

Deps:
  pip install opencv-python numpy
"""

import os
import sys
import math
import time
import cv2
import numpy as np


# ----------------------------
# Tree model
# ----------------------------
class Node:
    __slots__ = ("name", "path", "is_dir", "children", "parent", "subtree_size")

    def __init__(self, name, path, is_dir):
        self.name = name
        self.path = path
        self.is_dir = is_dir
        self.children = []
        self.parent = None
        self.subtree_size = 1


def build_tree(root_path: str, max_nodes: int = 1200, max_depth: int | None = None) -> Node:
    root_path = os.path.abspath(root_path)
    root = Node(os.path.basename(root_path) or root_path, root_path, True)

    node_count = 1

    def _build(parent: Node, depth: int):
        nonlocal node_count
        if max_depth is not None and depth >= max_depth:
            return
        try:
            entries = sorted(os.listdir(parent.path))
        except (PermissionError, FileNotFoundError):
            return

        for e in entries:
            if node_count >= max_nodes:
                return
            full = os.path.join(parent.path, e)
            is_dir = os.path.isdir(full)
            child = Node(e, full, is_dir)
            child.parent = parent
            parent.children.append(child)
            node_count += 1
            if is_dir:
                _build(child, depth + 1)

    _build(root, 0)
    return root


def compute_subtree_sizes(root: Node):
    order = []
    stack = [root]
    while stack:
        n = stack.pop()
        order.append(n)
        for c in n.children:
            stack.append(c)
    for n in reversed(order):
        s = 1
        for c in n.children:
            s += c.subtree_size
        n.subtree_size = s


def preorder_list(root: Node):
    out = []
    stack = [root]
    while stack:
        n = stack.pop()
        out.append(n)
        if n.children:
            kids = sorted(n.children, key=lambda x: x.path)
            for c in reversed(kids):
                stack.append(c)
    return out


# ----------------------------
# Geometry helpers
# ----------------------------
def point_segment_distance_and_dir(p: np.ndarray, a: np.ndarray, b: np.ndarray):
    """
    p, a, b are (2,) float32
    Returns (distance, unit_dir_from_segment_to_point)
    """
    ab = b - a
    ap = p - a
    denom = float(ab[0] * ab[0] + ab[1] * ab[1])
    if denom < 1e-8:
        d = p - a
        dist = float(np.linalg.norm(d)) + 1e-6
        return dist, d / dist

    t = float((ap[0] * ab[0] + ap[1] * ab[1]) / denom)
    if t < 0.0:
        t = 0.0
    elif t > 1.0:
        t = 1.0

    proj = a + ab * t
    d = p - proj
    dist = float(np.linalg.norm(d)) + 1e-6
    return dist, d / dist


def seg_intersect(a, b, c, d):
    """
    Proper segment intersection test (including touching as intersect).
    a,b,c,d: (2,) float vectors
    """
    def orient(p, q, r):
        return float((q[0]-p[0])*(r[1]-p[1]) - (q[1]-p[1])*(r[0]-p[0]))

    def on_segment(p, q, r):
        # q on pr bounding box
        return (min(p[0], r[0]) - 1e-6 <= q[0] <= max(p[0], r[0]) + 1e-6 and
                min(p[1], r[1]) - 1e-6 <= q[1] <= max(p[1], r[1]) + 1e-6)

    o1 = orient(a, b, c)
    o2 = orient(a, b, d)
    o3 = orient(c, d, a)
    o4 = orient(c, d, b)

    # general
    if (o1 * o2 < 0.0) and (o3 * o4 < 0.0):
        return True

    # collinear/touching
    if abs(o1) < 1e-6 and on_segment(a, c, b):
        return True
    if abs(o2) < 1e-6 and on_segment(a, d, b):
        return True
    if abs(o3) < 1e-6 and on_segment(c, a, d):
        return True
    if abs(o4) < 1e-6 and on_segment(c, b, d):
        return True

    return False


def seg_intersection_point(a, b, c, d):
    """
    Intersection point for non-parallel lines (not strictly segments),
    used only when seg_intersect() is true to compute a reasonable "push" point.
    """
    r = b - a
    s = d - c
    denom = float(r[0]*s[1] - r[1]*s[0])
    if abs(denom) < 1e-8:
        # fallback: midpoint of midpoints
        return 0.5*(0.5*(a+b) + 0.5*(c+d))
    t = float(((c[0]-a[0])*s[1] - (c[1]-a[1])*s[0]) / denom)
    return a + r * t


def perp(v):
    return np.array([-v[1], v[0]], dtype=np.float32)


# ----------------------------
# Animated physical layout
# ----------------------------
class AnimatedLayout:
    def __init__(self, nodes_ordered, W, H):
        self.W = W
        self.H = H
        self.nodes = nodes_ordered
        self.idx = {id(n): i for i, n in enumerate(self.nodes)}

        self.parent_of = np.full(len(self.nodes), -1, dtype=np.int32)
        for i, n in enumerate(self.nodes):
            if n.parent is not None:
                self.parent_of[i] = self.idx[id(n.parent)]

        self.pos = np.zeros((len(self.nodes), 2), dtype=np.float32)
        self.vel = np.zeros_like(self.pos)
        self.active = np.zeros(len(self.nodes), dtype=bool)

        # root at center
        self.pos[0] = (W * 0.5, H * 0.5)

        # ---- collision geometry (conservative) ----
        self.node_r = 11.0
        self.line_margin = 9.0
        self.min_node_sep = self.node_r * 3.0
        self.edge_clearance = self.node_r * 2.2  # keep edges away from each other

        # ---- forces ----
        self.target_edge = 90.0
        self.k_spring = 0.055

        self.k_repulse = 2.9
        self.k_node_edge = 3.2
        self.k_edge_edge = 2.4

        self.k_damp = 0.82
        self.k_bounds = 0.18

        self.pad = 35.0

        self._hash_cache = {}

    def _hash01(self, s: str) -> float:
        if s in self._hash_cache:
            return self._hash_cache[s]
        h = 2166136261
        for ch in s:
            h ^= ord(ch)
            h = (h * 16777619) & 0xFFFFFFFF
        v = h / 0xFFFFFFFF
        self._hash_cache[s] = v
        return v

    def _active_indices(self):
        return np.where(self.active)[0]

    def _active_edges(self):
        act = self.active
        edges = []
        for v in np.where(act)[0]:
            u = self.parent_of[v]
            if u >= 0 and act[u]:
                edges.append((u, v))
        return edges

    def activate_next(self) -> bool:
        for i in range(len(self.nodes)):
            if not self.active[i]:
                self.active[i] = True
                if i == 0:
                    self.vel[i] *= 0.0
                    return True

                p = self.parent_of[i]
                parent_pos = self.pos[p].copy()
                ang = (self._hash01(self.nodes[i].path) * 2.0 - 1.0) * math.pi
                r0 = 32.0 + (10.0 if self.nodes[i].is_dir else 0.0)
                self.pos[i] = parent_pos + np.array([math.cos(ang), math.sin(ang)], dtype=np.float32) * r0
                self.vel[i] *= 0.0
                return True
        return False

    def step(self, dt: float):
        act_idx = self._active_indices()
        if act_idx.size <= 1:
            return

        root = 0
        self.vel[root] *= 0.0

        force = np.zeros_like(self.pos)
        edges = self._active_edges()

        # ---- Springs ----
        if edges:
            u = np.array([e[0] for e in edges], dtype=np.int32)
            v = np.array([e[1] for e in edges], dtype=np.int32)

            pu = self.pos[u]
            pv = self.pos[v]
            d = pv - pu
            dist = np.linalg.norm(d, axis=1) + 1e-6
            dir_ = d / dist[:, None]

            subtree = np.array([self.nodes[i].subtree_size for i in v], dtype=np.float32)
            target = self.target_edge * (1.0 + 0.05 * np.sqrt(np.maximum(1.0, subtree)))

            stretch = dist - target
            f = (-self.k_spring * stretch)[:, None] * dir_

            np.add.at(force, u, -f)
            np.add.at(force, v, +f)

        # ---- Node-node repulsion ----
        min_sep = self.min_node_sep
        for ii in range(len(act_idx)):
            i = act_idx[ii]
            pi = self.pos[i]
            for jj in range(ii + 1, len(act_idx)):
                j = act_idx[jj]
                pj = self.pos[j]
                dv = pi - pj
                dist2 = float(dv[0]*dv[0] + dv[1]*dv[1])
                if dist2 < 1e-10:
                    dv = np.array([0.123, 0.456], dtype=np.float32)
                    dist2 = float(dv[0]*dv[0] + dv[1]*dv[1])
                dist = math.sqrt(dist2)
                if dist >= min_sep:
                    continue
                overlap = (min_sep - dist)
                dirv = dv / (dist + 1e-6)
                fi = dirv * (self.k_repulse * overlap)
                force[i] += fi
                force[j] -= fi

        # ---- Node-edge repulsion (nodes away from non-incident branches) ----
        if edges:
            eu = np.array([e[0] for e in edges], dtype=np.int32)
            ev = np.array([e[1] for e in edges], dtype=np.int32)
            A = self.pos[eu]
            B = self.pos[ev]
            safe = self.node_r + self.line_margin

            for i in act_idx:
                pi = self.pos[i]
                for k in range(len(edges)):
                    u = eu[k]
                    v = ev[k]
                    if i == u or i == v:
                        continue
                    dist, dirv = point_segment_distance_and_dir(pi, A[k], B[k])
                    if dist >= safe:
                        continue
                    overlap = (safe - dist)
                    force[i] += dirv * (self.k_node_edge * overlap)

        # ---- Edge-edge avoidance (forces) ----
        # 1) If edges cross -> push their endpoints away to uncross
        # 2) If edges are too close (even without crossing) -> mild separation (midpoint repulsion)
        if edges and len(edges) >= 2:
            eu = [e[0] for e in edges]
            ev = [e[1] for e in edges]
            P = self.pos

            clearance = self.edge_clearance

            m = len(edges)
            for i in range(m):
                a_i = eu[i]; b_i = ev[i]
                A1 = P[a_i]; B1 = P[b_i]
                mid1 = 0.5 * (A1 + B1)
                v1 = B1 - A1
                n1 = perp(v1)
                n1n = float(np.linalg.norm(n1)) + 1e-6
                n1 = n1 / n1n

                for j in range(i + 1, m):
                    a_j = eu[j]; b_j = ev[j]
                    # skip if share a node (incident edges)
                    if a_i == a_j or a_i == b_j or b_i == a_j or b_i == b_j:
                        continue

                    A2 = P[a_j]; B2 = P[b_j]
                    mid2 = 0.5 * (A2 + B2)

                    # crossing?
                    if seg_intersect(A1, B1, A2, B2):
                        ip = seg_intersection_point(A1, B1, A2, B2)

                        # push endpoints away from intersection along their edge normals
                        v2 = B2 - A2
                        n2 = perp(v2)
                        n2n = float(np.linalg.norm(n2)) + 1e-6
                        n2 = n2 / n2n

                        # choose normal direction consistently: point away from other edge midpoint
                        if float(np.dot(n1, (mid2 - ip))) > 0:
                            n1 = -n1
                        if float(np.dot(n2, (mid1 - ip))) > 0:
                            n2 = -n2

                        # apply forces to endpoints
                        push = self.k_edge_edge * 1.8
                        force[a_i] += n1 * push
                        force[b_i] += n1 * push
                        force[a_j] += n2 * push
                        force[b_j] += n2 * push
                        continue

                    # not crossing: keep some distance between segments (cheap approximation)
                    # measure midpoint-to-segment distances
                    d12, dir12 = point_segment_distance_and_dir(mid1, A2, B2)
                    d21, dir21 = point_segment_distance_and_dir(mid2, A1, B1)

                    if d12 < clearance:
                        force[a_i] += dir12 * (self.k_edge_edge * (clearance - d12) * 0.35)
                        force[b_i] += dir12 * (self.k_edge_edge * (clearance - d12) * 0.35)
                    if d21 < clearance:
                        force[a_j] += dir21 * (self.k_edge_edge * (clearance - d21) * 0.35)
                        force[b_j] += dir21 * (self.k_edge_edge * (clearance - d21) * 0.35)

        # ---- Soft bounds ----
        x = self.pos[:, 0]
        y = self.pos[:, 1]

        over = (self.pad - x)
        mask = over > 0
        force[mask, 0] += self.k_bounds * over[mask]

        over = (x - (self.W - self.pad))
        mask = over > 0
        force[mask, 0] -= self.k_bounds * over[mask]

        over = (self.pad - y)
        mask = over > 0
        force[mask, 1] += self.k_bounds * over[mask]

        over = (y - (self.H - self.pad))
        mask = over > 0
        force[mask, 1] -= self.k_bounds * over[mask]

        # ---- Integrate ----
        self.vel[act_idx] += force[act_idx] * dt
        self.vel[act_idx] *= self.k_damp
        self.pos[act_idx] += self.vel[act_idx] * dt

        # root anchored
        self.vel[root] *= 0.0
        self.pos[root] = self.pos[root]

    def project_no_overlap(self, iterations: int = 10):
        """
        HARD node-node constraint: separate overlapping nodes.
        """
        act_idx = self._active_indices()
        if act_idx.size <= 1:
            return

        root = 0
        min_sep = self.min_node_sep

        for _ in range(iterations):
            moved = False
            for ii in range(len(act_idx)):
                i = act_idx[ii]
                if i == root:
                    continue
                pi = self.pos[i]
                for jj in range(ii + 1, len(act_idx)):
                    j = act_idx[jj]
                    if j == root:
                        continue
                    pj = self.pos[j]

                    dv = pi - pj
                    dist2 = float(dv[0]*dv[0] + dv[1]*dv[1])
                    if dist2 < 1e-10:
                        dv = np.array([0.123, 0.456], dtype=np.float32)
                        dist2 = float(dv[0]*dv[0] + dv[1]*dv[1])

                    dist = math.sqrt(dist2)
                    if dist >= min_sep:
                        continue

                    overlap = (min_sep - dist)
                    dirv = dv / (dist + 1e-6)
                    push = 0.5 * overlap * dirv

                    self.pos[i] += push
                    self.pos[j] -= push
                    moved = True

            self.pos[root] = self.pos[root]
            if not moved:
                break

    def project_uncross_edges(self, iterations: int = 6):
        """
        HARD edge-edge constraint: if edges intersect, directly move endpoints to uncross.
        """
        edges = self._active_edges()
        if len(edges) < 2:
            return

        root = 0
        P = self.pos

        for _ in range(iterations):
            changed = False
            m = len(edges)
            for i in range(m):
                u1, v1 = edges[i]
                A1 = P[u1]; B1 = P[v1]
                mid1 = 0.5*(A1 + B1)
                dir1 = B1 - A1
                n1 = perp(dir1)
                n1n = float(np.linalg.norm(n1)) + 1e-6
                n1 = n1 / n1n

                for j in range(i + 1, m):
                    u2, v2 = edges[j]
                    if u1 == u2 or u1 == v2 or v1 == u2 or v1 == v2:
                        continue

                    A2 = P[u2]; B2 = P[v2]
                    mid2 = 0.5*(A2 + B2)

                    if not seg_intersect(A1, B1, A2, B2):
                        continue

                    ip = seg_intersection_point(A1, B1, A2, B2)

                    dir2 = B2 - A2
                    n2 = perp(dir2)
                    n2n = float(np.linalg.norm(n2)) + 1e-6
                    n2 = n2 / n2n

                    # choose normals away from the other edge midpoint
                    if float(np.dot(n1, (mid2 - ip))) > 0:
                        n1 = -n1
                    if float(np.dot(n2, (mid1 - ip))) > 0:
                        n2 = -n2

                    step = self.edge_clearance * 0.35

                    # move endpoints (skip moving root)
                    if u1 != root:
                        P[u1] += n1 * step
                    if v1 != root:
                        P[v1] += n1 * step
                    if u2 != root:
                        P[u2] += n2 * step
                    if v2 != root:
                        P[v2] += n2 * step

                    changed = True

            P[root] = P[root]
            if not changed:
                break

    def render(self):
        frame = np.full((self.H, self.W, 3), 255, dtype=np.uint8)

        COL_LINE = (185, 185, 185)
        COL_DIR = (60, 120, 60)
        COL_FILE = (120, 60, 60)
        COL_ROOT = (70, 70, 160)

        edges = self._active_edges()

        for u, v in edges:
            x1, y1 = self.pos[u]
            x2, y2 = self.pos[v]
            cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), COL_LINE, 1, cv2.LINE_AA)

        act_idx = self._active_indices()
        for i in act_idx:
            n = self.nodes[i]
            x, y = int(self.pos[i, 0]), int(self.pos[i, 1])

            if i == 0:
                color = COL_ROOT
                radius = 12
                thickness = 2
            else:
                color = COL_DIR if n.is_dir else COL_FILE
                radius = 9 if n.is_dir else 7
                thickness = 2 if n.is_dir else 1

            cv2.circle(frame, (x, y), radius, color, thickness, cv2.LINE_AA)

        cv2.putText(
            frame,
            f"nodes: {int(self.active.sum())}/{len(self.nodes)}  (q/ESC to quit)",
            (12, self.H - 18),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (20, 20, 20),
            1,
            cv2.LINE_AA
        )

        return frame


# ----------------------------
# Main
# ----------------------------
def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <folder>")
        sys.exit(1)

    root_path = sys.argv[1]
    if not os.path.isdir(root_path):
        print("Error: path is not a directory")
        sys.exit(1)

    W, H = 1280, 720

    # Performance guardrails (edge-edge is O(m^2), node-node is O(n^2))
    MAX_NODES = 650
    MAX_DEPTH = None  # e.g. 10

    root = build_tree(root_path, max_nodes=MAX_NODES, max_depth=MAX_DEPTH)
    compute_subtree_sizes(root)
    ordered = preorder_list(root)

    layout = AnimatedLayout(ordered, W, H)
    layout.activate_next()  # root

    add_interval = 0.1
    last_add = time.time()

    win = "Tree Viewer (physical collisions)"
    cv2.namedWindow(win, cv2.WINDOW_AUTOSIZE)

    prev = time.time()
    while True:
        now = time.time()
        dt = now - prev
        prev = now
        if dt > 0.05:
            dt = 0.05

        if (now - last_add) >= add_interval:
            layout.activate_next()
            last_add = now

        # More substeps => smoother, better collision handling
        substeps = 7
        subdt = dt / substeps
        for _ in range(substeps):
            layout.step(subdt)

        # Hard constraints:
        layout.project_no_overlap(iterations=10)
        layout.project_uncross_edges(iterations=6)

        frame = layout.render()
        cv2.imshow(win, frame)

        key = cv2.waitKey(16) & 0xFF
        if key in (27, ord("q")):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

