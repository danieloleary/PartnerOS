#!/usr/bin/env python3
"""
Generate a file list of all markdown templates in docs/.

This script scans the docs/ directory and outputs a JSON list of all .md files.
Useful for inventory and documentation purposes.
"""

import os
import json
from pathlib import Path

# Use the docs directory (symlinked to partneros-docs/src/content/docs)
DOCS_DIR = Path("docs")

# Fallback to partneros-docs path if docs doesn't exist
if not DOCS_DIR.exists():
    DOCS_DIR = Path("partneros-docs/src/content/docs")

files = []

if DOCS_DIR.exists():
    for root, dirs, filenames in os.walk(DOCS_DIR):
        for fn in filenames:
            if fn.lower().endswith(".md") or fn.lower().endswith(".mdx"):
                relpath = os.path.join(root, fn)
                relpath = relpath.replace("\\", "/")
                files.append(relpath)

files.sort()

output_path = Path("docs/file_list.json")
with open(output_path, "w") as f:
    json.dump(files, f, indent=2)

print(f"Found {len(files)} markdown files in {DOCS_DIR}")
print(f"Output: {output_path}")
