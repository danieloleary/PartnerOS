#!/usr/bin/env python3
"""
Template Variable Filler
Replaces {{variables}} in templates with company-specific values.

Usage:
    python scripts/fill_template.py --template docs/recruitment/01-email-sequence.md
    python scripts/fill_template.py --template docs/recruitment/01-email-sequence.md --output filled.md
    python scripts/fill_template.py --template docs/recruitment/01-email-sequence.md --preview
"""

import os
import re
import argparse
import yaml
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).parent.parent
CONFIG_FILE = REPO_ROOT / ".company-config" / "customize.yaml"

DEFAULT_VARIABLES = {
    "company_name": "Your Company",
    "company_website": "https://yourcompany.com",
    "contact_name": "Partner Manager",
    "contact_email": "partners@yourcompany.com",
    "logo_url": "",
    "brand_color": "#3B82F6",
    "primary_contact_role": "Partner Manager",
    "today_date": datetime.now().strftime("%B %d, %Y"),
    "current_year": str(datetime.now().year),
}


def load_config():
    """Load company configuration."""
    if not CONFIG_FILE.exists():
        return {}

    with open(CONFIG_FILE, "r") as f:
        config = yaml.safe_load(f)

    if config and "variables" in config:
        return config["variables"]

    if config and "company" in config:
        variables = {}
        if "company" in config:
            variables["company_name"] = config["company"].get(
                "name", DEFAULT_VARIABLES["company_name"]
            )
            variables["company_website"] = config["company"].get(
                "website", DEFAULT_VARIABLES["company_website"]
            )
        if "contact" in config:
            variables["contact_name"] = config["contact"].get(
                "name", DEFAULT_VARIABLES["contact_name"]
            )
            variables["contact_email"] = config["contact"].get(
                "email", DEFAULT_VARIABLES["contact_email"]
            )
            variables["primary_contact_role"] = config["contact"].get(
                "role", DEFAULT_VARIABLES["primary_contact_role"]
            )
        if "branding" in config:
            variables["logo_url"] = config["branding"].get(
                "logo_url", DEFAULT_VARIABLES["logo_url"]
            )
            variables["brand_color"] = config["branding"].get(
                "brand_color", DEFAULT_VARIABLES["brand_color"]
            )
        return variables

    return {}


def get_variables():
    """Get variables from config or defaults."""
    config_vars = load_config()

    variables = DEFAULT_VARIABLES.copy()
    variables.update(config_vars)

    return variables


def replace_variables(content, variables):
    """Replace {{variable}} with values."""

    def replacer(match):
        var_name = match.group(1).strip()
        return variables.get(var_name, match.group(0))

    return re.sub(r"\{\{(\w+)\}\}", replacer, content)


def process_template(template_path, output_path=None, preview=False):
    """Process a template file."""
    if not template_path.exists():
        print(f"Error: Template not found: {template_path}")
        return False

    with open(template_path, "r") as f:
        content = f.read()

    variables = get_variables()

    # Show available variables
    if preview:
        print("\nAvailable variables:")
        for key, value in variables.items():
            print(f"  {{{{{key}}}}} = {value}")
        print()

    # Replace variables
    filled_content = replace_variables(content, variables)

    if output_path:
        with open(output_path, "w") as f:
            f.write(filled_content)
        print(f"✓ Created: {output_path}")
    else:
        print(filled_content)

    return True


def main():
    parser = argparse.ArgumentParser(description="Fill template with company variables")
    parser.add_argument(
        "--template", "-t", required=True, help="Template file to process"
    )
    parser.add_argument("--output", "-o", help="Output file (default: print to stdout)")
    parser.add_argument(
        "--preview", "-p", action="store_true", help="Show available variables"
    )
    parser.add_argument(
        "--list-vars", "-l", action="store_true", help="List available variables"
    )

    args = parser.parse_args()

    template_path = Path(args.template)

    # Handle absolute paths
    if not template_path.is_absolute():
        template_path = REPO_ROOT / template_path

    if args.list_vars:
        variables = get_variables()
        print("\nAvailable variables:")
        for key, value in variables.items():
            print(f"  {{{{{key}}}}} = {value}")
        return

    process_template(template_path, args.output, args.preview)


if __name__ == "__main__":
    main()
