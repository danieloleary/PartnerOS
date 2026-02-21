#!/usr/bin/env python3
"""Move template metadata from top to bottom of pages."""

import re
import yaml
from pathlib import Path

DOCS_DIR = Path(__file__).parent.parent / "partneros-docs" / "src" / "content" / "docs"

METADATA_TEMPLATE = """---

## Template Metadata

| Attribute | Value |
|-----------|-------|
| **Template Number** | {template_number} |
| **Version** | {version} |
| **Last Updated** | {last_updated} |
| **Time Required** | {time_required} |
| **Difficulty** | {difficulty} |
| **Skill Level** | {skill_level} |
| **Phase** | {phase} |
| **Purpose** | {purpose} |

## Outcomes

{outcomes}

## Skills Gained

{skills_gained}

## Prerequisites

{prerequisites}
"""


def get_category(filepath):
    """Extract category from file path."""
    parts = filepath.parts
    if "partneros-docs" in parts:
        idx = parts.index("content") + 2
        if idx < len(parts):
            return parts[idx]
    return None


def move_metadata_to_bottom(filepath):
    """Move metadata section from top to bottom of template."""
    content = filepath.read_text()

    if not content.startswith("---"):
        return False

    # Check if there's a "## Template Metadata" section near the top
    # Split into lines
    lines = content.split("\n")

    # Find the Template Metadata section (should be early in file)
    metadata_start = None
    metadata_end = None
    in_metadata = False
    metadata_lines = []

    for i, line in enumerate(lines):
        if line.strip() == "## Template Metadata":
            metadata_start = i
            in_metadata = True
        elif in_metadata and line.startswith("## "):
            # Found next section
            metadata_end = i
            break
        elif in_metadata:
            metadata_lines.append(line)

    if metadata_start is None:
        return False

    # Extract frontmatter
    parts = content.split("---", 2)
    if len(parts) < 3:
        return False

    fm_text = parts[1]
    try:
        fm = yaml.safe_load(fm_text)
    except:
        return False

    if not fm or not fm.get("template_number"):
        return False

    # Build new metadata at bottom
    outcomes = fm.get("outcomes", [])
    outcomes_text = (
        "\n".join(f"- {o}" for o in outcomes) if outcomes else "- (No outcomes defined)"
    )

    skills = fm.get("skills_gained", [])
    skills_text = (
        "\n".join(f"- {s}" for s in skills) if skills else "- (No skills defined)"
    )

    prereqs = fm.get("prerequisites", [])
    prereqs_text = (
        "\n".join(f"- {p}" for p in prereqs) if prereqs else "- (No prerequisites)"
    )

    new_metadata = METADATA_TEMPLATE.format(
        template_number=fm.get("template_number", "N/A"),
        version=fm.get("version", "N/A"),
        last_updated=fm.get("last_updated", "N/A"),
        time_required=fm.get("time_required", "N/A"),
        difficulty=fm.get("difficulty", "N/A"),
        skill_level=fm.get("skill_level", "N/A"),
        phase=fm.get("phase", "N/A"),
        purpose=fm.get("purpose", "N/A"),
        outcomes=outcomes_text,
        skills_gained=skills_text,
        prerequisites=prereqs_text,
    )

    # Remove the metadata section from top
    if metadata_end:
        new_lines = lines[:metadata_start] + lines[metadata_end:]
    else:
        new_lines = lines[:metadata_start]

    # Find where to add the metadata (at the end, before any last ---)
    new_content = "\n".join(new_lines)

    # Add metadata at the end
    new_content = new_content.rstrip() + "\n" + new_metadata

    filepath.write_text(new_content)
    return True


def main():
    count = 0
    for md_file in DOCS_DIR.rglob("*.md"):
        if md_file.name == "index.md":
            continue
        if move_metadata_to_bottom(md_file):
            print(f"Updated: {md_file.relative_to(DOCS_DIR)}")
            count += 1

    print(f"\nTotal files updated: {count}")


if __name__ == "__main__":
    main()
