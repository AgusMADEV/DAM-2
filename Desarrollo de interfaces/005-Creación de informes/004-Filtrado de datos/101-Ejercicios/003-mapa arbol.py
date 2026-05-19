#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OpenCV filesystem tree viewer (irregular "tree-like" layout with collision avoidance)

What changed vs concentric rings:
- No fixed, equidistant circles.
- Initial layout is hierarchical and local: each node places its children around itself (each branch gets its own 360°).
- Then a lightweight physics relaxation runs to:
  - keep parent-child relations (springs)
  - repel nodes so node circles do not collide (repulsion)
  - keep everything inside the 1280x720 viewport (soft bounds)

Usage:
  python3 tree_opencv_tree_layout.py /var/www/html/dam/Primero

Deps:
  pip install opencv-python numpy
"""

import os
import sys
import math
import cv2
import numpy as np
from collections import deque, defaultdict


# ----------------------------
# Data model
# ----------------------------
class Node:
    __slots__ = ("name", "path", "is_dir", "children", "parent", "depth", "pos", "subtree_size")

    def __init__(self, name, path, is_dir):
        self.name = name
        self.path = path
        self.is_dir = is_dir
        self.children = []
        self.parent = None
        self.depth = 0
        self.pos = np.zeros(2, dtype=np.float32)
        self.subtree_size = 1


def build_tree(root_path: str, max_nodes: int = 800, max_depth: int | None = None) -> Node:
    """
    Builds a tree, with safe limits to keep rendering/relaxation interactive.
    """
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


def assign_depths_and_subtree_sizes(root: Node):
    # depth BFS
    q = deque([(root, 0)])
    while q:
        n, d = q.popleft()
        n.depth = d
        for c in n.children:
            q.append((c, d + 1))

    # subtree sizes postorder
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


def collect_nodes(root: Node):
    nodes = []
    stack = [root]
    while stack:
        n = stack.pop()
        nodes.append(n)
        for c in n.children:
            stack.append(c)
    return nodes


# ----------------------------
# Initial "branch gets 360°" layout
# ----------------------------
def initial_local_radial_layout(root: Node, center_xy, base_edge_len: float):
    """
    Each node places its children around itself using the full 2π range.
    Distances vary by subtree size, producing a more tree-like irregular structure.
    """
    root.pos[:] = center_xy

    # Deterministic angle seed from name/path
    def hash01(s: str) -> float:
        # stable-ish, simple
        h = 2166136261
        for ch in s:
            h ^= ord(ch)
            h = (h * 16777619) & 0xFFFFFFFF
        return (h / 0xFFFFFFFF)

    stack = [root]
    while stack:
        parent = stack.pop()
        kids = parent.children
        if not kids:
            continue

        # Sort to stabilize
        kids.sort(key=lambda x: x.path)

        k = len(kids)

        # Radius of this "child ring" around the parent:
        # depends on how "big" the branch is.
        # sqrt() prevents huge jumps but allows larger branches more breathing room.
        branch_weight = math.sqrt(max(1, parent.subtree_size))
        ring_r = base_edge_len * (1.0 + 0.18 * branch_weight)

        # Small random-ish rotation so identical branching doesn't look too symmetric.
        rot = (hash01(parent.path) * 2.0 - 1.0) * 0.6  # ~[-0.6, 0.6] rad

        for i, child in enumerate(kids):
            # Spread evenly across 360° for this parent
            ang = rot + (2.0 * math.pi) * (i / k)

            # Give larger subtrees slightly more distance from parent
            child_weight = math.sqrt(max(1, child.subtree_size))
            r = ring_r * (1.0 + 0.08 * child_weight)

            child.pos[0] = parent.pos[0] + r * math.cos(ang)
            child.pos[1] = parent.pos[1] + r * math.sin(ang)

            stack.append(child)


# ----------------------------
# Collision-avoidance relaxation (springs + repulsion)
# ----------------------------
def relax_layout(nodes, edges, root_index, W, H,
                 node_radius=10.0,
                 target_edge=90.0,
                 iters=220,
                 dt=0.25):
    """
    Physics:
      - Edge springs: keep parent-child at target_edge (scaled per subtree size by precomputed edge target)
      - Repulsion: prevent node disks from colliding
      - Soft bounds: push nodes back into screen
    Uses spatial hashing so repulsion is near-linear for typical trees.
    """

    n = len(nodes)
    pos = np.stack([nd.pos for nd in nodes], axis=0).astype(np.float32)
    vel = np.zeros_like(pos)

    # Precompute per-edge targets (use child subtree size to allow big subtrees more room)
    e_u = np.array([u for (u, v) in edges], dtype=np.int32)
    e_v = np.array([v for (u, v) in edges], dtype=np.int32)

    subtree = np.array([nd.subtree_size for nd in nodes], dtype=np.float32)
    # edge target grows a bit with subtree size of child
    edge_target = target_edge * (1.0 + 0.05 * np.sqrt(np.maximum(1.0, subtree[e_v])))

    # Spatial hashing parameters
    min_sep = node_radius * 2.2
    cell = float(min_sep)

    def build_grid(p):
        grid = defaultdict(list)
        gx = np.floor(p[:, 0] / cell).astype(np.int32)
        gy = np.floor(p[:, 1] / cell).astype(np.int32)
        for i in range(n):
            grid[(gx[i], gy[i])].append(i)
        return grid

    # Forces coefficients
    k_spring = 0.04
    k_repulse = 0.85
    k_damp = 0.88
    k_bounds = 0.12

    # Bounds padding
    pad = 40.0

    for _ in range(iters):
        # Root fixed (anchor)
        pos[root_index] = pos[root_index]  # explicit
        vel[root_index] *= 0.0

        force = np.zeros_like(pos)

        # ---- Springs (edges) ----
        pu = pos[e_u]
        pv = pos[e_v]
        d = pv - pu
        dist = np.linalg.norm(d, axis=1) + 1e-6
        dir_ = d / dist[:, None]
        # Spring tries to match edge_target
        stretch = (dist - edge_target)
        f = (-k_spring * stretch)[:, None] * dir_
        # Apply: u gets -f, v gets +f
        np.add.at(force, e_u, -f)
        np.add.at(force, e_v, +f)

        # ---- Repulsion (collision avoidance) using grid ----
        grid = build_grid(pos)
        for (cx, cy), idxs in grid.items():
            # Check this cell + neighbors
            neigh_cells = [
                (cx-1, cy-1), (cx, cy-1), (cx+1, cy-1),
                (cx-1, cy),   (cx, cy),   (cx+1, cy),
                (cx-1, cy+1), (cx, cy+1), (cx+1, cy+1),
            ]
            candidates = []
            for nc in neigh_cells:
                candidates.extend(grid.get(nc, []))
            if not candidates:
                continue

            # For each i in cell, compare to candidates (j>i to avoid double work)
            for i in idxs:
                pi = pos[i]
                for j in candidates:
                    if j <= i:
                        continue
                    pj = pos[j]
                    dv = pi - pj
                    dist2 = float(dv[0]*dv[0] + dv[1]*dv[1])
                    if dist2 < 1e-6:
                        # almost same spot: nudge deterministically
                        dv = np.array([0.123, 0.456], dtype=np.float32)
                        dist2 = float(dv[0]*dv[0] + dv[1]*dv[1])

                    dist = math.sqrt(dist2)
                    if dist >= min_sep:
                        continue

                    # Push apart proportional to overlap
                    overlap = (min_sep - dist)
                    dirv = dv / dist
                    rep = (k_repulse * overlap)
                    fi = dirv * rep
                    force[i] += fi
                    force[j] -= fi

        # ---- Soft bounds ----
        # left
        over = (pad - pos[:, 0])
        mask = over > 0
        force[mask, 0] += k_bounds * over[mask]
        # right
        over = (pos[:, 0] - (W - pad))
        mask = over > 0
        force[mask, 0] -= k_bounds * over[mask]
        # top
        over = (pad - pos[:, 1])
        mask = over > 0
        force[mask, 1] += k_bounds * over[mask]
        # bottom
        over = (pos[:, 1] - (H - pad))
        mask = over > 0
        force[mask, 1] -= k_bounds * over[mask]

        # Integrate
        vel += force * dt
        vel *= k_damp
        pos += vel * dt

        # Keep root fixed exactly at its starting pos (center)
        pos[root_index] = pos[root_index]

    # Write back
    for i, nd in enumerate(nodes):
        nd.pos[:] = pos[i]


# ----------------------------
# Rendering
# ----------------------------
def shorten(text: str, max_len: int = 22) -> str:
    return text if len(text) <= max_len else (text[: max_len - 1] + "…")


def draw_scene(nodes, edges, W, H):
    frame = np.full((H, W, 3), 255, dtype=np.uint8)

    # Colors (BGR)
    COL_LINE = (190, 190, 190)
    COL_DIR = (60, 120, 60)
    COL_FILE = (120, 60, 60)
    COL_ROOT = (70, 70, 160)
    COL_TEXT = (20, 20, 20)

    # Draw edges first
    for u, v in edges:
        x1, y1 = nodes[u].pos
        x2, y2 = nodes[v].pos
        cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), COL_LINE, 1, cv2.LINE_AA)

    # Draw nodes + labels
    for i, n in enumerate(nodes):
        x, y = int(n.pos[0]), int(n.pos[1])

        if n.parent is None:
            color = COL_ROOT
            radius = 14
            thickness = 2
        else:
            color = COL_DIR if n.is_dir else COL_FILE
            radius = 9 if n.is_dir else 7
            thickness = 2 if n.is_dir else 1

        cv2.circle(frame, (x, y), radius, color, thickness, cv2.LINE_AA)

        label = shorten(n.name, 26)
        cv2.putText(frame, label, (x + radius + 4, y + 4),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.42, COL_TEXT, 1, cv2.LINE_AA)

    # Legend / hint
    cv2.putText(frame, "DIR", (12, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.6, COL_TEXT, 1, cv2.LINE_AA)
    cv2.circle(frame, (52, 22), 8, COL_DIR, 2, cv2.LINE_AA)
    cv2.putText(frame, "FILE", (92, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.6, COL_TEXT, 1, cv2.LINE_AA)
    cv2.circle(frame, (150, 22), 7, COL_FILE, 1, cv2.LINE_AA)
    cv2.putText(frame, "q / ESC to quit", (12, H - 18), cv2.FONT_HERSHEY_SIMPLEX, 0.6, COL_TEXT, 1, cv2.LINE_AA)

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

    # Safety limits: adjust if you want
    MAX_NODES = 900
    MAX_DEPTH = None  # e.g. 8

    root = build_tree(root_path, max_nodes=MAX_NODES, max_depth=MAX_DEPTH)
    assign_depths_and_subtree_sizes(root)

    nodes = collect_nodes(root)

    # Map nodes to indices and edges list
    index = {id(n): i for i, n in enumerate(nodes)}
    edges = []
    for n in nodes:
        if n.parent is not None:
            edges.append((index[id(n.parent)], index[id(n)]))

    root_index = index[id(root)]
    center = np.array([W * 0.5, H * 0.5], dtype=np.float32)

    # Initial irregular hierarchical layout
    initial_local_radial_layout(root, center_xy=center, base_edge_len=65.0)

    # Relax to avoid collisions while keeping a tree-ish structure
    relax_layout(
        nodes=nodes,
        edges=edges,
        root_index=root_index,
        W=W,
        H=H,
        node_radius=10.0,     # collision uses node circles, not labels
        target_edge=85.0,     # average parent-child distance
        iters=240,
        dt=0.28
    )

    win = "Tree Viewer"
    cv2.namedWindow(win, cv2.WINDOW_AUTOSIZE)

    while True:
        frame = draw_scene(nodes, edges, W, H)
        cv2.imshow(win, frame)
        key = cv2.waitKey(16) & 0xFF
        if key in (27, ord("q")):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

