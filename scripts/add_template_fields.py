#!/usr/bin/env python3
"""Add missing skills_gained and prerequisites to templates."""

import yaml
import re
from pathlib import Path

DOCS_DIR = Path(__file__).parent.parent / "partneros-docs" / "src" / "content" / "docs"

# Default skills by category
CATEGORY_SKILLS = {
    "strategy": [
        "Strategic planning",
        "Partner program design",
        "Competitive analysis",
    ],
    "recruitment": ["Sales outreach", "Negotiation", "Partner qualification"],
    "enablement": ["Training development", "Certification design", "Content creation"],
    "legal": ["Contract drafting", "Compliance", "Risk management"],
    "finance": ["Financial modeling", "Commission structures", "Revenue forecasting"],
    "security": ["Security assessment", "Compliance auditing", "Risk assessment"],
    "operations": ["Process optimization", "Partner management", "Reporting"],
    "executive": [
        "Executive presentation",
        "Strategic storytelling",
        "Board communication",
    ],
    "analysis": ["Data analysis", "Metrics design", "Performance tracking"],
    "getting-started": ["Onboarding", "Process implementation", "Best practices"],
    "agent": ["AI prompting", "Automation", "Workflow design"],
}

# Default prerequisites by category
CATEGORY_PREREQS = {
    "strategy": ["Clear partner program vision"],
    "recruitment": ["Target partner list"],
    "enablement": ["Partner-signed agreement"],
    "legal": ["Legal team review"],
    "finance": ["Budget approval"],
    "security": ["Security questionnaire completed"],
    "operations": ["Partner CRM or tracking system"],
    "executive": ["Board meeting scheduled"],
    "analysis": ["Partner data available"],
    "getting-started": ["None - good starting point"],
    "agent": ["Python 3.10+", "API keys configured"],
}


def get_category(filepath):
    """Extract category from file path."""
    parts = filepath.parts
    if "partneros-docs" in parts:
        idx = parts.index("content") + 2
        if idx < len(parts):
            return parts[idx]
    return None


def add_missing_fields(filepath):
    """Add missing skills_gained and prerequisites to frontmatter."""
    content = filepath.read_text()

    if not content.startswith("---"):
        return False

    # Split frontmatter and body
    parts = content.split("---", 2)
    if len(parts) < 3:
        return False

    fm_text = parts[1]
    body = parts[2]

    try:
        fm = yaml.safe_load(fm_text)
    except:
        return False

    if not fm:
        return False

    modified = False

    # Add skills_gained if missing
    if not fm.get("skills_gained") or len(fm.get("skills_gained", [])) == 0:
        category = get_category(filepath)
        skills = CATEGORY_SKILLS.get(category, ["Template usage", "Best practices"])
        fm["skills_gained"] = skills
        modified = True

    # Add prerequisites if missing
    if not fm.get("prerequisites") or len(fm.get("prerequisites", [])) == 0:
        category = get_category(filepath)
        prereqs = CATEGORY_PREREQS.get(
            category, ["Completed prior templates in this section"]
        )
        fm["prerequisites"] = prereqs
        modified = True

    if modified:
        # Reconstruct file with updated frontmatter
        new_fm_text = yaml.dump(fm, default_flow_style=False, sort_keys=False)
        new_content = f"---\n{new_fm_text}---{body}"
        filepath.write_text(new_content)
        return True

    return False


def main():
    count = 0
    for md_file in DOCS_DIR.rglob("*.md"):
        # Skip index files
        if md_file.name == "index.md":
            continue
        if add_missing_fields(md_file):
            print(f"Updated: {md_file.relative_to(DOCS_DIR)}")
            count += 1

    print(f"\nTotal files updated: {count}")


if __name__ == "__main__":
    main()
