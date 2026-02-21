#!/usr/bin/env python3
"""Fix malformed markdown links in Starlight docs.

The earlier sed command created malformed links like:
- ((filename.md/)) -> should be (filename.md/)
- ((../path/file.md/)) -> should be (../path/file.md/)

This script fixes those.
"""

import re
from pathlib import Path

DOCS_DIR = Path(__file__).parent.parent / "partneros-docs" / "src" / "content" / "docs"


def fix_double_parens(filepath: Path) -> int:
    """Fix double parentheses in links."""
    content = filepath.read_text()
    original = content

    # Fix ((something)) -> (something)
    # But be careful to only fix links that have .md in them
    content = re.sub(r"\(\(([^)]+\.md/?)\)\)", r"(\1)", content)

    if content != original:
        filepath.write_text(content)
        return 1
    return 0


def main():
    total = 0
    for md_file in DOCS_DIR.rglob("*.md"):
        fixed = fix_double_parens(md_file)
        if fixed:
            print(f"Fixed: {md_file.relative_to(DOCS_DIR)}")
            total += fixed

    print(f"\nTotal files modified: {total}")


if __name__ == "__main__":
    main()
