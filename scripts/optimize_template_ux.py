#!/usr/bin/env python3
"""Optimize template UX for humans.

This script:
1. Standardizes all internal links to Starlight folder format (adds trailing /)
2. Adds "When to use" one-liner at top if missing
3. Removes duplicate metadata sections (keeps frontmatter)
4. Ensures proper content structure
"""

import re
import yaml
from pathlib import Path

DOCS_DIR = Path(__file__).parent.parent / "partneros-docs" / "src" / "content" / "docs"


def extract_frontmatter(content):
    """Extract and parse frontmatter from markdown content."""
    pattern = r"^---\s*\n(.*?)\n---\s*\n"
    match = re.match(pattern, content, re.DOTALL)
    if match:
        try:
            return yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            return None
    return None


def standardize_links(content):
    """Standardize all internal links to Starlight folder format."""

    # Match markdown links: [text](path)
    def replace_link(match):
        text = match.group(1)
        link = match.group(2)

        # Skip external links
        if link.startswith(("http:", "https:", "mailto:", "#", "/")):
            return match.group(0)

        # Skip anchor links
        if link.startswith("#"):
            return match.group(0)

        # Skip fragment-only
        if not link.strip():
            return match.group(0)

        # Skip image links
        if link.endswith((".png", ".jpg", ".jpeg", ".svg", ".gif")):
            return match.group(0)

        # For .md links, convert to folder style
        link_clean = link.rstrip("/")
        if link_clean.endswith(".md"):
            # Convert to folder-style: file.md -> file.md/
            # But preserve ../ relative paths
            if not link_clean.startswith("../"):
                link = link_clean + "/"
            else:
                link = link_clean + "/"

        return f"]({link})"

    # Replace .md links with folder-style
    content = re.sub(r"(\[([^\]]*)\]\(([^)]+\.md)\))", replace_link, content)

    return content


def add_when_to_use(content, fm):
    """Add 'When to use' section at top if missing."""
    # Check if we already have a When to use section
    if "## When to Use" in content or "**When to use**" in content:
        return content

    # Get description from frontmatter
    description = fm.get("description", "")
    if isinstance(description, str):
        description = description.strip()

    if not description:
        # Generate a simple one
        purpose = fm.get("purpose", "")
        phase = fm.get("phase", "")
        description = (
            f"Use this template during the {phase} phase for {purpose} activities."
        )

    # Find where to insert - after frontmatter, before first heading
    lines = content.split("\n")

    # Find first heading
    first_heading_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith("#"):
            first_heading_idx = i
            break

    if first_heading_idx is None:
        return content

    # Build the When to use section
    when_to_use = f"\n> **{description}**\n"

    # Insert after frontmatter (first --- line) but before first content
    # Find the end of frontmatter
    frontmatter_end = None
    in_frontmatter = False
    for i, line in enumerate(lines):
        if line.strip() == "---":
            if not in_frontmatter:
                in_frontmatter = True
            else:
                frontmatter_end = i
                break

    if frontmatter_end is not None:
        # Insert right after frontmatter
        new_lines = (
            lines[: frontmatter_end + 1] + [when_to_use] + lines[frontmatter_end + 1 :]
        )
        return "\n".join(new_lines)

    return content


def clean_duplicate_metadata(content):
    """Remove duplicate metadata sections that were added by our earlier script.

    Keep only frontmatter, remove ## Template Metadata, ## Outcomes, ## Skills Gained, ## Prerequisites
    from the body since they're in frontmatter.
    """
    lines = content.split("\n")
    new_lines = []
    skip_until_next_heading = False
    metadata_sections = [
        "## Template Metadata",
        "## Outcomes",
        "## Skills Gained",
        "## Prerequisites",
    ]

    i = 0
    while i < len(lines):
        line = lines[i]

        # Check if we're at a metadata section to skip
        if any(section in line for section in metadata_sections):
            skip_until_next_heading = True
            i += 1
            continue

        # If we're skipping, look for next non-empty line or heading
        if skip_until_next_heading:
            # Skip empty lines in metadata section
            if not line.strip():
                i += 1
                continue
            # If we hit a heading (that isn't another metadata section), stop skipping
            if line.startswith("#"):
                skip_until_next_heading = False
            else:
                i += 1
                continue

        new_lines.append(line)
        i += 1

    return "\n".join(new_lines)


def has_tldr(content):
    """Check if content starts with a blockquote (TLDR)."""
    lines = content.split("\n")
    for line in lines:
        if line.strip():
            return line.strip().startswith(">")
    return False


def process_template(filepath):
    """Process a single template file."""
    content = filepath.read_text()
    original = content

    # Extract frontmatter
    fm = extract_frontmatter(content)
    if not fm or not fm.get("template_number"):
        return False

    # 1. Standardize links
    content = standardize_links(content)

    # 2. Add When to use section if missing
    if not has_tldr(content):
        content = add_when_to_use(content, fm)

    # 3. Clean duplicate metadata from body (keep in frontmatter)
    content = clean_duplicate_metadata(content)

    if content != original:
        filepath.write_text(content)
        return True
    return False


def main():
    count = 0
    for md_file in DOCS_DIR.rglob("*.md"):
        # Skip index files
        if md_file.name == "index.md":
            continue
        if process_template(md_file):
            print(f"Updated: {md_file.relative_to(DOCS_DIR)}")
            count += 1

    print(f"\nTotal files updated: {count}")


if __name__ == "__main__":
    main()
