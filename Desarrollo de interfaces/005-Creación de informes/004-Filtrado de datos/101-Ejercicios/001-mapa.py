#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

def print_tree(root_path, prefix=""):
    try:
        entries = sorted(os.listdir(root_path))
    except PermissionError:
        print(prefix + "[Permission denied]")
        return

    for index, entry in enumerate(entries):
        full_path = os.path.join(root_path, entry)
        is_last = index == len(entries) - 1

        connector = "└── " if is_last else "├── "
        print(prefix + connector + entry)

        if os.path.isdir(full_path):
            extension = "    " if is_last else "│   "
            print_tree(full_path, prefix + extension)

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <folder>")
        sys.exit(1)

    root = sys.argv[1]

    if not os.path.isdir(root):
        print("Error: path is not a directory")
        sys.exit(1)

    print(root)
    print_tree(root)

if __name__ == "__main__":
    main()

