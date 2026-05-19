#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Filesystem Tree Timeline Viewer (OpenCV) — radial botanical tree + chronological reveal.
"""

import os
import sys
import math
import time
import heapq
import cv2
import numpy as np
from datetime import datetime

# ----------------------------
# Tree model
# ----------------------------
class Node:
    __slots__ = ("name", "path", "is_dir", "children", "parent", "depth",
                 "t", "leaf_count", "angle", "x", "y")

    def __init__(self, name, path, is_dir, t):
        self.name = name
        self.path = path
        self.is_dir = is_dir
        self.children = []
        self.parent = None
        self.depth = 0
        self.t = float(t)
        self.leaf_count = 1
        self.angle = 0.0
        self.x = 0.0
        self.y = 0.0

def get_best_time(path: str) -> float:
    st = os.stat(path, follow_symlinks=False)
    bt = getattr(st, "st_birthtime", None)
    if bt is not None:
        return float(bt)
    return float(st.st_mtime)

def build_tree(root_path: str, max_nodes: int = 1500, max_depth: int | None = None) -> Node:
    root_path = os.path.abspath(root_path)
    root = Node(os.path.basename(root_path) or root_path, root_path, True, get_best_time(root_path))
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
            try:
                is_dir = os.path.isdir(full)
                t = get_best_time(full)
            except (PermissionError, FileNotFoundError):
                continue

            child = Node(e, full, is_dir, t)
            child.parent = parent
            parent.children.append(child)
            node_count += 1
            if is_dir:
                _build(child, depth + 1)

    _build(root, 0)
    return root

def assign_depths(root: Node):
    stack = [(root, 0)]
    while stack:
        n, d = stack.pop()
        n.depth = d
        for c in n.children:
            stack.append((c, d + 1))

def compute_leaf_counts(root: Node):
    order = []
    stack = [root]
    while stack:
        n = stack.pop()
        order.append(n)
        for c in n.children:
            stack.append(c)

    for n in reversed(order):
        if not n.children:
            n.leaf_count = 1
        else:
            n.leaf_count = sum(max(1, c.leaf_count) for c in n.children)

def collect_nodes(root: Node):
    out = []
    stack = [root]
    while stack:
        n = stack.pop()
        out.append(n)
        for c in n.children:
            stack.append(c)
    return out

# ----------------------------
# Radial botanical tree layout
# ----------------------------
def compute_radial_tree_layout(root: Node, center_x: float, center_y: float):
    """Layout nodes as a radial tree growing outward in 360 degrees from center."""
    
    def compute_positions(node: Node, x: float, y: float, base_angle: float, spread: float):
        node.x = x
        node.y = y
        
        if not node.children:
            return
        
        # Sort children by timestamp
        kids = sorted(node.children, key=lambda k: (k.t, k.path))
        n_kids = len(kids)
        
        # Branch length decreases with depth
        branch_len = 80 - (node.depth * 8)
        branch_len = max(30, branch_len)
        
        # Calculate angular spread for branches
        total_spread = spread * 0.8  # Each level narrows the spread
        
        if n_kids == 1:
            # Single child continues in same direction
            child_angle = base_angle
            child_x = x + branch_len * math.cos(child_angle)
            child_y = y + branch_len * math.sin(child_angle)
            compute_positions(kids[0], child_x, child_y, child_angle, total_spread)
        else:
            # Multiple children spread out
            start_angle = base_angle - total_spread / 2
            angle_step = total_spread / (n_kids - 1) if n_kids > 1 else 0
            
            for i, kid in enumerate(kids):
                child_angle = start_angle + i * angle_step
                child_x = x + branch_len * math.cos(child_angle)
                child_y = y + branch_len * math.sin(child_angle)
                compute_positions(kid, child_x, child_y, child_angle, total_spread)
    
    # Root is at center
    root.x = center_x
    root.y = center_y
    
    if not root.children:
        return
    
    # Distribute root's children evenly around 360 degrees
    kids = sorted(root.children, key=lambda k: (k.t, k.path))
    n_kids = len(kids)
    
    for i, kid in enumerate(kids):
        # Each main branch gets an equal slice of 360 degrees
        base_angle = (2 * math.pi * i / n_kids) - math.pi / 2  # Start from top
        
        # Initial branch length from root
        branch_len = 80
        child_x = center_x + branch_len * math.cos(base_angle)
        child_y = center_y + branch_len * math.sin(base_angle)
        
        # Each main branch gets a wedge to spread into
        angular_spread = (2 * math.pi / n_kids) * 0.7  # 70% of available space
        
        compute_positions(kid, child_x, child_y, base_angle, angular_spread)

# ----------------------------
# Chronological reveal
# ----------------------------
class ChronoRevealer:
    def __init__(self, root: Node, idx_of):
        self.idx_of = idx_of
        self.heap = []
        self._push_children(root)

    def _push_children(self, node: Node):
        kids = sorted(node.children, key=lambda k: (k.t, k.path))
        for k in kids:
            heapq.heappush(self.heap, (k.t, k.path, self.idx_of[id(k)]))

    def next_index(self, active_mask):
        while self.heap:
            _, _, i = heapq.heappop(self.heap)
            if not active_mask[i]:
                return i
        return None

    def on_activated(self, node: Node):
        self._push_children(node)

# ----------------------------
# Viewer
# ----------------------------
class Viewer:
    def __init__(self, nodes, root_index, idx_map, W, H):
        self.nodes = nodes
        self.root = root_index
        self.idx_map = idx_map
        self.W, self.H = W, H
        self.active = np.zeros(len(nodes), dtype=bool)

        self.parent = np.full(len(nodes), -1, dtype=np.int32)
        for i, n in enumerate(nodes):
            if n.parent is not None:
                self.parent[i] = idx_map[id(n.parent)]

        self.recent = []
        self.recent_ttl = 1.5

    def activate(self, i: int, now: float):
        if self.active[i]:
            return
        self.active[i] = True
        self.recent.append((now, i))

    def _prune_recent(self, now):
        self.recent = [(t, i) for (t, i) in self.recent if (now - t) <= self.recent_ttl]

    def draw_branch(self, frame, x1, y1, x2, y2, thickness):
        """Draw a curved branch using bezier-like curve."""
        # Control point for curve (perpendicular offset for natural curve)
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        
        # Direction vector
        dx = x2 - x1
        dy = y2 - y1
        length = math.sqrt(dx*dx + dy*dy)
        
        if length < 1:
            cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), 
                    (101, 67, 33), thickness, cv2.LINE_AA)
            return
        
        # Perpendicular offset for curve
        perp_x = -dy / length
        perp_y = dx / length
        
        # Control point offset (creates gentle curve)
        offset = length * 0.15
        ctrl_x = mid_x + perp_x * offset
        ctrl_y = mid_y + perp_y * offset
        
        # Draw quadratic bezier curve as multiple line segments
        points = []
        steps = 20
        for i in range(steps + 1):
            t = i / steps
            # Quadratic bezier
            bx = (1-t)**2 * x1 + 2*(1-t)*t * ctrl_x + t**2 * x2
            by = (1-t)**2 * y1 + 2*(1-t)*t * ctrl_y + t**2 * y2
            points.append((int(bx), int(by)))
        
        # Draw the curve
        for i in range(len(points) - 1):
            cv2.line(frame, points[i], points[i+1], (101, 67, 33), thickness, cv2.LINE_AA)

    def render(self, now: float, global_min_t: float, global_max_t: float, current_t: float | None):
        # Soft gradient background
        frame = np.full((self.H, self.W, 3), (250, 235, 215), dtype=np.uint8)

        # Get active nodes
        act_idx = np.where(self.active)[0]
        
        # Draw branches first (parent to child)
        for i in act_idx:
            if i == self.root:
                continue
            parent_idx = self.parent[i]
            if parent_idx >= 0 and self.active[parent_idx]:
                parent = self.nodes[parent_idx]
                child = self.nodes[i]
                
                # Branch thickness decreases with depth
                thickness = max(1, 7 - child.depth)
                self.draw_branch(frame, parent.x, parent.y, child.x, child.y, thickness)

        # Draw nodes as leaves or branch points
        for i in act_idx:
            node = self.nodes[i]
            x, y = int(node.x), int(node.y)
            
            if i == self.root:
                # Root - draw as trunk center
                cv2.circle(frame, (x, y), 12, (101, 67, 33), -1, cv2.LINE_AA)
                cv2.circle(frame, (x, y), 12, (80, 50, 20), 2, cv2.LINE_AA)
            elif not node.children or not any(self.active[self.idx_map[id(c)]] for c in node.children):
                # Leaf node - draw as a leaf
                if node.is_dir:
                    color = (34, 139, 34)  # Forest green for directories
                else:
                    color = (50, 205, 50)  # Lime green for files
                cv2.circle(frame, (x, y), 8, color, -1, cv2.LINE_AA)
                cv2.circle(frame, (x, y), 8, (255, 255, 255), 1, cv2.LINE_AA)
            else:
                # Branch point - smaller brown circle
                cv2.circle(frame, (x, y), 4, (101, 67, 33), -1, cv2.LINE_AA)

        # Labels for recent nodes
        self._prune_recent(now)
        for _, i in self.recent[-15:]:  # Only last 15 labels
            if i == self.root:
                continue
            node = self.nodes[i]
            x, y = int(node.x), int(node.y)
            name = node.name[:20]  # Truncate long names
            
            # Calculate text position to avoid center overlap
            angle = math.atan2(y - self.H/2, x - self.W/2)
            offset_x = 12 if x > self.W/2 else -12 - len(name) * 5
            offset_y = -8
            
            # Draw text with background
            text_size = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 1)[0]
            bg_x1 = x + offset_x - 2
            bg_y1 = y + offset_y - text_size[1] - 2
            bg_x2 = x + offset_x + text_size[0] + 2
            bg_y2 = y + offset_y + 4
            
            cv2.rectangle(frame, (int(bg_x1), int(bg_y1)), (int(bg_x2), int(bg_y2)), 
                         (255, 255, 255), -1)
            cv2.putText(frame, name, (x + offset_x, y + offset_y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (40, 40, 40), 1, cv2.LINE_AA)

        # Info overlay
        def fmt(ts):
            return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

        range_txt = f"Range: {fmt(global_min_t)}  →  {fmt(global_max_t)}"
        cur_txt = "Current: -" if current_t is None else f"Current: {fmt(current_t)}"

        # Semi-transparent background for text
        overlay = frame.copy()
        cv2.rectangle(overlay, (5, 5), (650, 80), (255, 255, 255), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)

        cv2.putText(frame, cur_txt, (12, 26),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (20, 20, 20), 1, cv2.LINE_AA)
        cv2.putText(frame, range_txt, (12, 52),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (80, 80, 80), 1, cv2.LINE_AA)
        cv2.putText(frame, f"nodes: {int(self.active.sum())}/{len(self.nodes)}   (q/ESC to quit)",
                    (12, self.H - 18), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (20, 20, 20), 1, cv2.LINE_AA)

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

    MAX_NODES = 1400
    MAX_DEPTH = None

    root = build_tree(root_path, max_nodes=MAX_NODES, max_depth=MAX_DEPTH)
    assign_depths(root)
    compute_leaf_counts(root)
    nodes = collect_nodes(root)

    if not nodes:
        print("No nodes found.")
        sys.exit(0)

    # Global time range
    all_t = [n.t for n in nodes]
    global_min_t = min(all_t)
    global_max_t = max(all_t)

    # Index mapping
    idx_map = {id(n): i for i, n in enumerate(nodes)}
    root_index = idx_map[id(root)]

    # Compute radial tree layout from center
    center_x = W * 0.5
    center_y = H * 0.5
    compute_radial_tree_layout(root, center_x, center_y)

    # Viewer
    viewer = Viewer(nodes, root_index, idx_map, W, H)

    # Activate root
    now = time.time()
    viewer.activate(root_index, now)

    # Chronological revealer
    revealer = ChronoRevealer(root, idx_map)

    # Add one node every 0.1 seconds
    add_interval = 0.1
    last_add = time.time()
    last_added_time = None

    win = "Radial Tree Timeline Viewer"
    cv2.namedWindow(win, cv2.WINDOW_AUTOSIZE)

    prev = time.time()
    while True:
        now = time.time()
        dt = now - prev
        prev = now

        if (now - last_add) >= add_interval:
            nxt = revealer.next_index(viewer.active)
            if nxt is not None:
                viewer.activate(nxt, now)
                revealer.on_activated(nodes[nxt])
                last_added_time = nodes[nxt].t
            last_add = now

        frame = viewer.render(now, global_min_t, global_max_t, last_added_time)
        cv2.imshow(win, frame)

        key = cv2.waitKey(16) & 0xFF
        if key in (27, ord("q")):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
