#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tree viewer (concentric radial layout) using OpenCV.

- Opens a 1280x720 window
- Root node centered
- Each depth level is a concentric ring
- Files/folders are nodes, with lines parent->child

Usage:
  python3 tree_opencv.py /var/www/html/dam/Primero

Deps:
  pip install opencv-python
"""

import os
import sys
import math
import cv2


# ----------------------------
# Data model
# ----------------------------
class Node:
    __slots__ = ("name", "path", "is_dir", "children", "parent", "depth", "pos")

    def __init__(self, name, path, is_dir):
        self.name = name
        self.path = path
        self.is_dir = is_dir
        self.children = []
        self.parent = None
        self.depth = 0
        self.pos = (0, 0)


def build_tree(root_path: str, max_entries_per_dir: int | None = None) -> Node:
    root_path = os.path.abspath(root_path)
    root = Node(os.path.basename(root_path) or root_path, root_path, True)

    def _build(parent: Node):
        try:
            entries = sorted(os.listdir(parent.path))
        except (PermissionError, FileNotFoundError):
            return

        if max_entries_per_dir is not None:
            entries = entries[:max_entries_per_dir]

        for e in entries:
            full = os.path.join(parent.path, e)
            is_dir = os.path.isdir(full)
            child = Node(e, full, is_dir)
            child.parent = parent
            parent.children.append(child)
            if is_dir:
                _build(child)

    _build(root)
    return root


def assign_depths(root: Node) -> int:
    max_depth = 0
    stack = [(root, 0)]
    while stack:
        n, d = stack.pop()
        n.depth = d
        max_depth = max(max_depth, d)
        for c in n.children:
            stack.append((c, d + 1))
    return max_depth


def collect_by_depth(root: Node):
    levels = {}
    stack = [root]
    while stack:
        n = stack.pop()
        levels.setdefault(n.depth, []).append(n)
        for c in n.children:
            stack.append(c)
    # deterministic ordering within each depth
    for d in levels:
        levels[d].sort(key=lambda x: x.path)
    return levels


# ----------------------------
# Layout (concentric rings)
# ----------------------------
def layout_concentric(root: Node, w: int, h: int, margin: int = 70):
    cx, cy = w // 2, h // 2
    max_depth = assign_depths(root)
    levels = collect_by_depth(root)

    # Radii per depth (fit within screen)
    if max_depth == 0:
        root.pos = (cx, cy)
        return

    max_radius = min(w, h) // 2 - margin
    ring_step = max(40, int(max_radius / max_depth))

    # Place root in center
    root.pos = (cx, cy)

    # For each depth ring, place nodes evenly around the circle
    for d in range(1, max_depth + 1):
        nodes = levels.get(d, [])
        if not nodes:
            continue

        r = d * ring_step
        n = len(nodes)
        # If there are many nodes, slightly shrink radius to reduce clipping
        r = min(r, max_radius)

        # Start angle shifted so the first node isn't exactly at 0 radians
        start_angle = -math.pi / 2
        for i, node in enumerate(nodes):
            angle = start_angle + (2 * math.pi * i / n)
            x = int(cx + r * math.cos(angle))
            y = int(cy + r * math.sin(angle))
            node.pos = (x, y)


# ----------------------------
# Rendering
# ----------------------------
def shorten(text: str, max_len: int = 18) -> str:
    if len(text) <= max_len:
        return text
    return text[: max_len - 1] + "…"


def draw_scene(root: Node, w: int, h: int):
    img = (255 * (1.0)).__class__  # dummy to satisfy linters (unused)
    canvas = (255 * (0)).__class__  # dummy

    # White background
    canvas = (255 * 0)  # placeholder

    canvas = (255 * 0)  # not used
    frame = (255 * 0)   # not used

    frame = (255 * 0)   # not used
    frame = None

    frame = (255 * 0)   # not used
    frame = None

    frame = (255 * 0)   # not used
    frame = None

    # Real frame init
    frame = 255 * (0)   # will be overwritten
    frame = None
    frame = 255 * 0
    frame = None

    frame = 255 * 0
    frame = None

    frame = 255 * 0
    frame = None

    frame = 255 * 0
    frame = None

    # OK, actual frame:
    frame = 255 * 0  # will be replaced below
    import numpy as np
    frame = np.full((h, w, 3), 255, dtype=np.uint8)

    # Colors (BGR)
    COL_LINE = (180, 180, 180)
    COL_DIR = (60, 120, 60)
    COL_FILE = (120, 60, 60)
    COL_TEXT = (20, 20, 20)
    COL_ROOT = (70, 70, 160)

    # Gather nodes for drawing
    nodes = []
    stack = [root]
    while stack:
        n = stack.pop()
        nodes.append(n)
        for c in n.children:
            stack.append(c)

    # Draw edges first (so nodes are on top)
    for n in nodes:
        for c in n.children:
            x1, y1 = n.pos
            x2, y2 = c.pos
            cv2.line(frame, (x1, y1), (x2, y2), COL_LINE, 1, cv2.LINE_AA)

    # Draw nodes + labels
    for n in nodes:
        x, y = n.pos
        if n is root:
            color = COL_ROOT
            radius = 14
            thickness = 2
        else:
            color = COL_DIR if n.is_dir else COL_FILE
            radius = 9 if n.is_dir else 7
            thickness = 2 if n.is_dir else 1

        cv2.circle(frame, (x, y), radius, color, thickness, cv2.LINE_AA)

        label = shorten(n.name, 22)
        # offset text slightly
        tx, ty = x + radius + 4, y + 4
        cv2.putText(
            frame,
            label,
            (tx, ty),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.42,
            COL_TEXT,
            1,
            cv2.LINE_AA,
        )

    # Legend
    cv2.putText(frame, "DIR", (12, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.6, COL_TEXT, 1, cv2.LINE_AA)
    cv2.circle(frame, (52, 22), 8, COL_DIR, 2, cv2.LINE_AA)
    cv2.putText(frame, "FILE", (92, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.6, COL_TEXT, 1, cv2.LINE_AA)
    cv2.circle(frame, (150, 22), 7, COL_FILE, 1, cv2.LINE_AA)
    cv2.putText(frame, "Press q / ESC to quit", (12, h - 18), cv2.FONT_HERSHEY_SIMPLEX, 0.6, COL_TEXT, 1, cv2.LINE_AA)

    return frame


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <folder>")
        sys.exit(1)

    root_path = sys.argv[1]
    if not os.path.isdir(root_path):
        print("Error: path is not a directory")
        sys.exit(1)

    W, H = 1280, 720
    root = build_tree(root_path, max_entries_per_dir=None)
    layout_concentric(root, W, H, margin=80)

    win = "Tree Viewer"
    cv2.namedWindow(win, cv2.WINDOW_AUTOSIZE)

    while True:
        frame = draw_scene(root, W, H)
        cv2.imshow(win, frame)

        key = cv2.waitKey(16) & 0xFF
        if key in (27, ord("q")):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

