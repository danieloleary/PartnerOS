#!/usr/bin/env python3
"""Add metadata display to template files.

This script adds a metadata table to templates that don't have one,
showing template info like number, version, time, difficulty, etc.
"""

import re
import yaml
from pathlib import Path

DOCS_DIR = Path(__file__).parent.parent / "partneros-docs" / "src" / "content" / "docs"

METADATA_TEMPLATE = """
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

---

"""


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


def has_metadata_section(content):
    """Check if the file already has a metadata section."""
    return "## Template Metadata" in content or "## Outcomes" in content


def add_metadata_to_template(filepath):
    """Add metadata section to a template file."""
    content = filepath.read_text()

    # Skip if already has metadata
    if has_metadata_section(content):
        return False

    # Extract frontmatter
    fm = extract_frontmatter(content)
    if not fm:
        return False

    # Skip if not a template (no template_number)
    if "template_number" not in fm:
        return False

    # Build metadata from frontmatter
    outcomes = fm.get("outcomes", [])
    outcomes_text = (
        "\n".join(f"- {o}" for o in outcomes) if outcomes else "- (No outcomes defined)"
    )

    skills = fm.get("skills_gained", [])
    skills_text = (
        "\n".join(f"- {s}" for s in skills) if skills else "- (No skills defined)"
    )

    metadata = METADATA_TEMPLATE.format(
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
    )

    # Find where to insert - after frontmatter, before the first # heading
    pattern = r"^---\s*\n.*?\n---\s*\n"
    match = re.match(pattern, content, re.DOTALL)
    if match:
        end_of_fm = match.end()
        # Find first heading
        remaining = content[end_of_fm:]
        heading_match = re.search(r"^#+\s+", remaining)
        if heading_match:
            insert_pos = end_of_fm + heading_match.start()
            new_content = content[:insert_pos] + metadata + content[insert_pos:]
            filepath.write_text(new_content)
            return True

    return False


def main():
    count = 0
    for md_file in DOCS_DIR.rglob("*.md"):
        # Skip index files
        if md_file.name == "index.md":
            continue
        if add_metadata_to_template(md_file):
            print(f"Updated: {md_file.relative_to(DOCS_DIR)}")
            count += 1

    print(f"\nTotal files updated: {count}")


if __name__ == "__main__":
    main()
