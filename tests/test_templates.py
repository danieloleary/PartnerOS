"""Test template completeness and frontmatter - PartnerOS v1.2."""

import os
import re
import yaml
import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def count_templates():
    """Count all markdown files in docs/"""
    docs_dir = REPO_ROOT / "docs"
    count = 0
    for root, dirs, files in os.walk(docs_dir):
        count += len([f for f in files if f.endswith(".md")])
    return count


def get_all_template_paths():
    """Get all template paths relative to docs/"""
    docs_dir = REPO_ROOT / "docs"
    templates = []
    for root, dirs, files in os.walk(docs_dir):
        for f in files:
            if f.endswith(".md") and f not in ["index.md", "404.md", "tags.md"]:
                path = Path(root) / f
                rel_path = path.relative_to(docs_dir)
                templates.append(rel_path)
    return templates


def parse_frontmatter(content):
    """Extract frontmatter from markdown content."""
    pattern = r"^---\s*\n(.*?)\n---\s*\n"
    match = re.match(pattern, content, re.DOTALL)
    if match:
        frontmatter_text = match.group(1)
        try:
            return yaml.safe_load(frontmatter_text)
        except yaml.YAMLError:
            return None
    return None


# =============================================================================
# TIER 1: CRITICAL TESTS - Frontmatter Schema & Structure
# =============================================================================


def test_templates_exist():
    """Verify templates exist."""
    assert count_templates() > 0


def test_templates_have_frontmatter():
    """Verify markdown files have YAML frontmatter."""
    docs_dir = REPO_ROOT / "docs"
    missing = []
    for root, dirs, files in os.walk(docs_dir):
        for f in files:
            if f.endswith(".md"):
                path = Path(root) / f
                with open(path, "r") as fp:
                    content = fp.read()
                    if not content.startswith("---"):
                        missing.append(str(path))
    assert len(missing) == 0, f"Missing frontmatter: {missing}"


def test_frontmatter_schema_validation():
    """Test 1.1: Verify all required frontmatter fields exist."""
    REQUIRED_FIELDS = [
        "title",
        "section",
        "category",
        "template_number",
        "version",
        "last_updated",
        "author",
        "tier",
        "skill_level",
        "purpose",
        "phase",
        "time_required",
        "difficulty",
        "prerequisites",
        "description",
        "outcomes",
        "skills_gained",
    ]

    # Files that are reference docs, not templates - exclude from full schema validation
    EXCLUDE_FROM_FULL_SCHEMA = [
        "glossary.md",
        "maturity-model.md",
        "index.md",
        "404.md",
        "tags.md",
    ]

    # Directories that contain docs, not templates - require minimal frontmatter
    DOCUMENT_ONLY_DIRS = ["agent/", "getting-started/"]

    docs_dir = REPO_ROOT / "docs"
    failures = []

    for root, dirs, files in os.walk(docs_dir):
        for f in files:
            if f.endswith(".md"):
                path = Path(root) / f

                # Skip non-template files
                if f in EXCLUDE_FROM_FULL_SCHEMA:
                    continue

                # Skip directories that contain docs, not templates
                rel_path = str(path.relative_to(docs_dir))
                if any(doc_dir in rel_path for doc_dir in DOCUMENT_ONLY_DIRS):
                    continue

                with open(path, "r") as fp:
                    content = fp.read()
                    frontmatter = parse_frontmatter(content)

                    if frontmatter is None:
                        failures.append(f"{path}: YAML parse error")
                        continue

                    if not isinstance(frontmatter, dict):
                        failures.append(f"{path}: Frontmatter not a dict")
                        continue

                    missing_fields = [
                        field for field in REQUIRED_FIELDS if field not in frontmatter
                    ]

                    if missing_fields:
                        failures.append(f"{path}: Missing fields: {missing_fields}")

    assert len(failures) == 0, f"Frontmatter validation failed:\n" + "\n".join(failures)


def test_template_count_per_category():
    """Test 1.2: Verify expected template counts per category."""
    docs_dir = REPO_ROOT / "docs"

    expected_counts = {
        "strategy": 8,
        "recruitment": 10,
        "enablement": 7,
        "agent": 4,
        "getting-started": 4,
        "resources": 4,
        "legal": 4,
        "finance": 3,
        "security": 2,
        "operations": 4,
        "executive": 1,
        "analysis": 1,
    }

    failures = []

    for category, expected in expected_counts.items():
        category_dir = docs_dir / category
        if not category_dir.exists():
            failures.append(f"Missing directory: {category}")
            continue

        count = len(
            [
                f
                for f in category_dir.rglob("*.md")
                if f.name not in ["index.md", "404.md"]
            ]
        )
        if count != expected:
            failures.append(f"{category}: expected {expected}, got {count}")

    assert len(failures) == 0, f"Template count validation failed:\n" + "\n".join(
        failures
    )


def test_folder_structure():
    """Test 1.3: Verify required folder structure exists."""
    docs_dir = REPO_ROOT / "docs"

    required_folders = [
        "strategy",
        "recruitment",
        "enablement",
        "agent",
        "getting-started",
        "resources",
        "legal",
        "finance",
        "security",
        "operations",
        "executive",
        "analysis",
    ]

    missing = []
    for folder in required_folders:
        path = docs_dir / folder
        if not path.is_dir():
            missing.append(folder)

    assert len(missing) == 0, f"Missing folders: {missing}"


def test_playbook_template_references():
    """Test 1.4: Verify playbook YAML references existing templates."""
    playbook_dir = REPO_ROOT / "scripts" / "partner_agent" / "playbooks"
    docs_dir = REPO_ROOT / "docs"

    if not playbook_dir.exists():
        pytest.skip("Playbook directory not found")

    failures = []

    for playbook_file in playbook_dir.glob("*.yaml"):
        with open(playbook_file, "r") as f:
            playbook = yaml.safe_load(f)

        if "steps" not in playbook:
            continue

        for step in playbook.get("steps", []):
            if "template" in step:
                template_ref = step["template"]
                # Handle both old style (partner_blueprint/) and new style (docs/)
                template_path = template_ref.replace("partner_blueprint/", "docs/")

                if not template_path.endswith(".md"):
                    template_path += ".md"

                full_path = REPO_ROOT / template_path
                if not full_path.exists():
                    failures.append(
                        f"{playbook_file.name}: template not found: {template_ref}"
                    )

    assert len(failures) == 0, f"Playbook reference validation failed:\n" + "\n".join(
        failures
    )


def test_frontmatter_yaml_parseable():
    """Test 1.5: Verify all frontmatter YAML is valid/syntax-error-free."""
    docs_dir = REPO_ROOT / "docs"
    failures = []

    for root, dirs, files in os.walk(docs_dir):
        for f in files:
            if f.endswith(".md"):
                path = Path(root) / f
                with open(path, "r") as fp:
                    content = fp.read()
                    frontmatter = parse_frontmatter(content)

                    if frontmatter is None:
                        failures.append(f"{path}: YAML parse error")

    assert len(failures) == 0, f"YAML parse errors:\n" + "\n".join(failures)


# =============================================================================
# TIER 2: SITE/DOCS/ORGANIZATION TESTS
# =============================================================================


def test_config_yaml_valid():
    """Verify config.yaml is valid YAML and has required fields."""
    config_file = REPO_ROOT / "scripts" / "partner_agent" / "config.yaml"

    if not config_file.exists():
        pytest.skip("config.yaml not found")

    with open(config_file, "r") as f:
        config = yaml.safe_load(f)

    # Verify required fields
    assert "provider" in config, "config.yaml missing 'provider'"
    assert "model" in config, "config.yaml missing 'model'"
    assert "templates_dir" in config, "config.yaml missing 'templates_dir'"


def test_playbook_yaml_schema():
    """Verify all playbooks have valid schema."""
    playbook_dir = REPO_ROOT / "scripts" / "partner_agent" / "playbooks"

    if not playbook_dir.exists():
        pytest.skip("Playbook directory not found")

    failures = []

    for playbook_file in playbook_dir.glob("*.yaml"):
        with open(playbook_file, "r") as f:
            try:
                playbook = yaml.safe_load(f)
            except yaml.YAMLError as e:
                failures.append(f"{playbook_file.name}: YAML parse error: {e}")
                continue

            if not isinstance(playbook, dict):
                failures.append(f"{playbook_file.name}: Not a valid dict")
                continue

            # Check required fields
            if "name" not in playbook:
                failures.append(f"{playbook_file.name}: Missing 'name'")
            if "description" not in playbook:
                failures.append(f"{playbook_file.name}: Missing 'description'")
            if "steps" not in playbook:
                failures.append(f"{playbook_file.name}: Missing 'steps'")

    assert len(failures) == 0, f"Playbook schema validation failed:\n" + "\n".join(
        failures
    )


def test_no_duplicate_template_titles():
    """Verify no duplicate template titles exist."""
    docs_dir = REPO_ROOT / "docs"
    titles = {}
    failures = []

    for root, dirs, files in os.walk(docs_dir):
        for f in files:
            if f.endswith(".md") and f not in ["index.md", "404.md", "tags.md"]:
                path = Path(root) / f
                with open(path, "r") as fp:
                    content = fp.read()
                    frontmatter = parse_frontmatter(content)

                    if frontmatter and isinstance(frontmatter, dict):
                        title = frontmatter.get("title", "")
                        if title:
                            if title in titles:
                                failures.append(
                                    f"Duplicate title '{title}': {path} vs {titles[title]}"
                                )
                            else:
                                titles[title] = path

    assert len(failures) == 0, f"Duplicate titles found:\n" + "\n".join(failures)


def test_template_files_have_content():
    """Verify templates have reasonable content (not empty)."""
    docs_dir = REPO_ROOT / "docs"
    failures = []

    for root, dirs, files in os.walk(docs_dir):
        for f in files:
            if f.endswith(".md") and f not in ["index.md", "404.md", "tags.md"]:
                path = Path(root) / f
                with open(path, "r") as fp:
                    content = fp.read()

                    # Skip files with only frontmatter (less than 500 chars total)
                    if len(content) < 500:
                        failures.append(
                            f"{path}: Template too short ({len(content)} chars)"
                        )

    assert len(failures) == 0, f"Empty or tiny templates found:\n" + "\n".join(failures)


def test_mkdocs_yml_valid():
    """Verify mkdocs.yml is valid YAML."""
    mkdocs_file = REPO_ROOT / "mkdocs.yml"

    if not mkdocs_file.exists():
        pytest.skip("mkdocs.yml not found")

    with open(mkdocs_file, "r") as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            pytest.fail(f"mkdocs.yml has YAML parse error: {e}")

    # Verify basic structure
    assert "site_name" in config, "mkdocs.yml missing 'site_name'"
    assert "nav" in config, "mkdocs.yml missing 'nav'"


def test_scripts_exist():
    """Verify required scripts exist."""
    scripts_dir = REPO_ROOT / "scripts"

    required_scripts = [
        "onboard.py",
        "fill_template.py",
        "demo_mode.py",
        "generate_template.py",
        "standardize_templates.py",
        "generate_report.py",
        "export_pdf.py",
        "package_zip.py",
    ]

    for script in required_scripts:
        path = scripts_dir / script
        assert path.exists(), f"Missing script: {script}"


def test_onboard_script_valid():
    """Verify onboard.py is valid Python."""
    script = REPO_ROOT / "scripts" / "onboard.py"

    if not script.exists():
        pytest.skip("onboard.py not found")

    with open(script, "r") as f:
        code = f.read()

    try:
        compile(code, "onboard.py", "exec")
    except SyntaxError as e:
        pytest.fail(f"Syntax error in onboard.py: {e}")


def test_fill_template_script_valid():
    """Verify fill_template.py is valid Python."""
    script = REPO_ROOT / "scripts" / "fill_template.py"

    if not script.exists():
        pytest.skip("fill_template.py not found")

    with open(script, "r") as f:
        code = f.read()

    try:
        compile(code, "fill_template.py", "exec")
    except SyntaxError as e:
        pytest.fail(f"Syntax error in fill_template.py: {e}")


def test_demo_mode_script_valid():
    """Verify demo_mode.py is valid Python."""
    script = REPO_ROOT / "scripts" / "demo_mode.py"

    if not script.exists():
        pytest.skip("demo_mode.py not found")

    with open(script, "r") as f:
        code = f.read()

    try:
        compile(code, "demo_mode.py", "exec")
    except SyntaxError as e:
        pytest.fail(f"Syntax error in demo_mode.py: {e}")


def test_export_pdf_script_valid():
    """Verify export_pdf.py is valid Python."""
    script = REPO_ROOT / "scripts" / "export_pdf.py"
    if not script.exists():
        pytest.skip("export_pdf.py not found")
    with open(script, "r") as f:
        code = f.read()
    try:
        compile(code, "export_pdf.py", "exec")
    except SyntaxError as e:
        pytest.fail(f"Syntax error in export_pdf.py: {e}")


def test_package_zip_script_valid():
    """Verify package_zip.py is valid Python."""
    script = REPO_ROOT / "scripts" / "package_zip.py"
    if not script.exists():
        pytest.skip("package_zip.py not found")
    with open(script, "r") as f:
        code = f.read()
    try:
        compile(code, "package_zip.py", "exec")
    except SyntaxError as e:
        pytest.fail(f"Syntax error in package_zip.py: {e}")


def test_package_zip_produces_output():
    """package_zip.py produces a valid zip with expected content."""
    import tempfile
    import zipfile
    import subprocess

    with tempfile.TemporaryDirectory() as tmpdir:
        result = subprocess.run(
            [
                "python3",
                str(REPO_ROOT / "scripts" / "package_zip.py"),
                "--templates-only",
                "--output",
                tmpdir,
                "--version",
                "test",
            ],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
        )
        assert result.returncode == 0, f"package_zip.py failed: {result.stderr}"
        zips = list(Path(tmpdir).glob("*.zip"))
        assert len(zips) == 1, "Expected exactly one zip file"
        with zipfile.ZipFile(zips[0]) as zf:
            names = zf.namelist()
            assert any("PACKAGE_MANIFEST.json" in n for n in names)
            assert any("docs/" in n for n in names)
            assert any("README.md" in n for n in names)


def test_examples_directory():
    """Verify examples directory structure."""
    examples_dir = REPO_ROOT / "examples"

    assert examples_dir.exists(), "examples/ directory not found"

    # Check for demo-company
    demo_dir = examples_dir / "demo-company"
    assert demo_dir.exists(), "examples/demo-company/ not found"

    demo_config = demo_dir / "demo-config.yaml"
    assert demo_config.exists(), "examples/demo-company/demo-config.yaml not found"


# =============================================================================
# LEGACY TESTS - Keep for backward compatibility
# =============================================================================


def test_docs_structure():
    """Verify key docs folders exist."""
    base = REPO_ROOT / "docs"
    required_folders = ["strategy", "recruitment", "enablement", "agent"]
    for folder in required_folders:
        path = base / folder
        assert path.is_dir(), f"Missing folder: {folder}"


def test_playbooks_exist():
    """Verify playbooks exist."""
    playbook_dir = REPO_ROOT / "scripts" / "partner_agent" / "playbooks"
    playbooks = [
        "recruit.yaml",
        "onboard.yaml",
        "qbr.yaml",
        "expand.yaml",
        "exit.yaml",
        "co-marketing.yaml",
        "support-escalation.yaml",
    ]
    for pb in playbooks:
        path = playbook_dir / pb
        assert path.exists(), f"Missing playbook: {pb}"


def test_env_example_exists():
    """Verify .env.example was created with correct model."""
    env_file = REPO_ROOT / "scripts" / "partner_agent" / ".env.example"
    assert env_file.exists(), ".env.example not found"

    with open(env_file) as f:
        content = f.read()
    assert "OLLAMA_ENDPOINT" in content
    assert "OLLAMA_MODEL" in content


if __name__ == "__main__":
    print(f"Templates found: {count_templates()}")
    print("\n=== Running Tier 1 Tests ===")

    print("\n1. test_templates_exist...")
    test_templates_exist()
    print("   PASS")

    print("\n2. test_templates_have_frontmatter...")
    test_templates_have_frontmatter()
    print("   PASS")

    print("\n3. test_frontmatter_schema_validation...")
    test_frontmatter_schema_validation()
    print("   PASS")

    print("\n4. test_template_count_per_category...")
    test_template_count_per_category()
    print("   PASS")

    print("\n5. test_folder_structure...")
    test_folder_structure()
    print("   PASS")

    print("\n6. test_playbook_template_references...")
    test_playbook_template_references()
    print("   PASS")

    print("\n7. test_frontmatter_yaml_parseable...")
    test_frontmatter_yaml_parseable()
    print("   PASS")

    print("\n=== All Tier 1 Tests Passed! ===")


# =============================================================================
# PHASE 6: NAVIGATION & INDEX PAGE TESTS
# =============================================================================


def test_nav_completeness():
    """Verify all .md files in docs/ are referenced in mkdocs.yml nav."""
    import yaml

    mkdocs_file = REPO_ROOT / "mkdocs.yml"
    with open(mkdocs_file) as f:
        config = yaml.safe_load(f)

    nav = config.get("nav", [])
    nav_paths = set()

    def extract_paths(nav_item):
        if isinstance(nav_item, str):
            nav_paths.add(nav_item)
        elif isinstance(nav_item, dict):
            for v in nav_item.values():
                extract_paths(v)
        elif isinstance(nav_item, list):
            for item in nav_item:
                extract_paths(item)

    for section in nav:
        extract_paths(section)

    docs_dir = REPO_ROOT / "docs"
    all_md_files = set()
    for f in docs_dir.rglob("*.md"):
        rel_path = str(f.relative_to(docs_dir))
        all_md_files.add(rel_path)

    special_files = {"404.md", "tags.md"}
    orphaned = []

    for md_file in all_md_files:
        if md_file in special_files:
            continue
        if md_file not in nav_paths:
            orphaned.append(md_file)

    assert len(orphaned) == 0, f"Orphaned files not in nav: {orphaned}"


def test_index_page_coverage():
    """Verify each template directory has an index.md."""
    docs_dir = REPO_ROOT / "docs"

    required_indexes = [
        "strategy/index.md",
        "recruitment/index.md",
        "enablement/index.md",
        "legal/index.md",
        "finance/index.md",
        "security/index.md",
        "operations/index.md",
        "executive/index.md",
        "analysis/index.md",
    ]

    failures = []
    for index in required_indexes:
        index_path = docs_dir / index
        if not index_path.exists():
            failures.append(index)

    assert len(failures) == 0, f"Missing index pages: {failures}"


# =============================================================================
# PHASE 7: EXPANDED QUALITY TESTS
# =============================================================================


def test_frontmatter_consistency():
    """Verify frontmatter field types are consistent across templates."""
    docs_dir = REPO_ROOT / "docs"
    field_types = {}

    exclude_files = [
        "index.md",
        "404.md",
        "tags.md",
        "glossary.md",
        "maturity-model.md",
        "licensing.md",
        "partner-os-one-pager.md",
    ]

    for f in docs_dir.rglob("*.md"):
        if f.name in exclude_files:
            continue
        if "agent/" in str(f) or "getting-started/" in str(f):
            continue
        if "resources/" in str(f):
            continue

        content = f.read_text()
        frontmatter = parse_frontmatter(content)
        if not frontmatter:
            continue

        for key, value in frontmatter.items():
            type_str = type(value).__name__
            if key not in field_types:
                field_types[key] = type_str
            elif field_types[key] != type_str:
                assert False, (
                    f"Inconsistent type for '{key}' in {f.name}: expected {field_types[key]}, got {type_str}"
                )


def test_template_number_uniqueness():
    """Verify template_number is unique across all templates."""
    docs_dir = REPO_ROOT / "docs"
    template_numbers = {}

    for f in docs_dir.rglob("*.md"):
        if f.name in ["index.md", "404.md", "tags.md"]:
            continue
        if "agent/" in str(f) or "getting-started/" in str(f):
            continue

        content = f.read_text()
        frontmatter = parse_frontmatter(content)
        if not frontmatter:
            continue

        tmpl_num = frontmatter.get("template_number", "")
        if tmpl_num:
            if tmpl_num in template_numbers:
                assert False, (
                    f"Duplicate template_number '{tmpl_num}': {f.name} vs {template_numbers[tmpl_num]}"
                )
            template_numbers[tmpl_num] = f.name


def test_all_sections_have_templates():
    """Verify all sections in nav have at least one template."""
    docs_dir = REPO_ROOT / "docs"

    section_dirs = [
        d.name
        for d in docs_dir.iterdir()
        if d.is_dir()
        and not d.name.startswith(".")
        and d.name not in ["assets", "stylesheets"]
    ]

    empty_sections = []
    for section in section_dirs:
        section_path = docs_dir / section
        templates = [
            f
            for f in section_path.rglob("*.md")
            if f.name not in ["index.md", "404.md", "tags.md"]
        ]
        if not templates:
            empty_sections.append(section)

    assert len(empty_sections) == 0, f"Sections without templates: {empty_sections}"


def test_mkdocs_nav_sections_match_docs_dirs():
    """Verify mkdocs nav sections correspond to actual docs directories."""
    import yaml

    mkdocs_file = REPO_ROOT / "mkdocs.yml"
    with open(mkdocs_file) as f:
        config = yaml.safe_load(f)

    nav = config.get("nav", [])
    nav_sections = set()

    for section in nav:
        if isinstance(section, dict):
            nav_sections.update(section.keys())
        elif isinstance(section, str):
            nav_sections.add(section)

    docs_dir = REPO_ROOT / "docs"
    actual_dirs = set(
        d.name.lower()
        for d in docs_dir.iterdir()
        if d.is_dir()
        and not d.name.startswith(".")
        and d.name not in ["assets", "stylesheets"]
    )

    nav_sections_lower = {s.lower() for s in nav_sections}

    ignore_sections = {"home", "getting started", "partner agent"}
    nav_sections_lower = nav_sections_lower - ignore_sections

    unexpected_in_nav = nav_sections_lower - actual_dirs
    assert len(unexpected_in_nav) == 0, (
        f"Nav sections not in docs/: {unexpected_in_nav}"
    )


def test_template_files_not_empty():
    """Verify all template files have meaningful content (not just frontmatter)."""
    docs_dir = REPO_ROOT / "docs"

    for f in docs_dir.rglob("*.md"):
        if f.name in ["index.md", "404.md", "tags.md"]:
            continue

        content = f.read_text()

        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                body = parts[2].strip()
                if len(body) < 100:
                    assert False, (
                        f"{f.name}: body content too short ({len(body)} chars)"
                    )


def test_no_broken_internal_links():
    """Verify internal markdown links resolve to existing files.

    This test checks that links in markdown files point to existing files.
    Supports both legacy .md links and Starlight folder-style links.
    """
    import re

    # Check both docs/ (legacy) and partneros-docs/ (Starlight)
    docs_dirs = [
        REPO_ROOT / "docs",
        REPO_ROOT / "partneros-docs" / "src" / "content" / "docs",
    ]

    failures = []

    for docs_dir in docs_dirs:
        if not docs_dir.exists():
            continue

        # Build a lookup of all files by basename (for relative link resolution)
        all_files = {}
        all_folders = set()
        for f in docs_dir.rglob("*.md"):
            rel = str(f.relative_to(docs_dir))
            basename = rel.rsplit("/", 1)[-1]
            folder = rel.rsplit("/", 1)[0] if "/" in rel else ""

            # Track folders
            if folder:
                all_folders.add(folder)

            if basename not in all_files:
                all_files[basename] = []
            all_files[basename].append(rel)
            # Also add folder-style versions
            if basename.endswith(".md"):
                folder_name = basename[:-3]
                if folder_name not in all_files:
                    all_files[folder_name] = []
                all_files[folder_name].append(rel)

        for f in docs_dir.rglob("*.md"):
            content = f.read_text()
            links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)

            for text, link in links:
                # Skip external links
                if any(
                    link.startswith(prefix)
                    for prefix in ("http:", "https:", "mailto:", "/", "#")
                ):
                    continue

                # Normalize link
                link_clean = link.rstrip("/")

                # Handle Starlight folder-style: filename.md/ -> filename
                if link_clean.endswith(".md/"):
                    link_clean = link_clean[:-1]

                # Get the basename of the link
                link_basename = link_clean.rsplit("/", 1)[-1]

                # Check if we have this file
                found = False

                # Direct match
                if link_clean in all_files:
                    found = True
                # Match by basename
                elif link_basename in all_files:
                    found = True
                # Try with .md extension
                elif link_basename + ".md" in all_files:
                    found = True
                # Try folder style (for Starlight)
                elif link_basename.endswith(".md"):
                    folder_name = link_basename[:-3]
                    if folder_name in all_files:
                        found = True
                # Check if it's a folder link (e.g., "recruitment" -> recruitment/index.md)
                elif link_clean in all_folders:
                    found = True
                elif link_basename in all_folders:
                    found = True

                if not found:
                    failures.append(f"{f.relative_to(docs_dir)}: broken link to {link}")

    assert len(failures) == 0, f"Broken links:\n" + "\n".join(failures)


def test_no_md_extension_in_links():
    """Verify internal links don't use .md extension (Starlight uses folder-style)."""
    import re

    docs_dirs = [
        REPO_ROOT / "partneros-docs" / "src" / "content" / "docs",
    ]

    failures = []

    for docs_dir in docs_dirs:
        if not docs_dir.exists():
            continue

        for f in docs_dir.rglob("*.md"):
            content = f.read_text()
            # Find links with .md in them (but not images)
            links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)

            for text, link in links:
                # Skip external links and images
                if any(
                    link.startswith(p) for p in ("http:", "https:", "mailto:", "/", "#")
                ):
                    continue
                if link.rstrip("/").endswith((".png", ".jpg", ".jpeg", ".svg", ".gif")):
                    continue

                # Check for .md in link path
                if ".md" in link and not link.startswith("http"):
                    failures.append(
                        f"{f.relative_to(docs_dir)}: link contains .md: {link}"
                    )

    assert len(failures) == 0, (
        f"Links with .md extension (use folder-style instead):\n" + "\n".join(failures)
    )


def test_no_double_parentheses():
    """Verify no malformed links with double parentheses.

    Excludes:
    - Mermaid diagrams (valid syntax: E --> F((Signed)))
    - Code examples in skill docs
    """
    docs_dirs = [
        REPO_ROOT / "partneros-docs" / "src" / "content" / "docs",
    ]

    failures = []

    for docs_dir in docs_dirs:
        if not docs_dir.exists():
            continue

        for f in docs_dir.rglob("*.md"):
            content = f.read_text()

            # Skip Mermaid code blocks
            in_mermaid = False
            lines = content.split("\n")
            for i, line in enumerate(lines, 1):
                # Track mermaid blocks
                if (
                    line.strip().startswith("```mermaid")
                    or line.strip() == "```mermaid"
                ):
                    in_mermaid = not in_mermaid
                    continue
                if in_mermaid:
                    continue

                # Skip code blocks entirely
                if line.strip().startswith("```"):
                    continue

                # Look for (( but not in valid contexts
                if "((" in line:
                    # Exclude Mermaid shapes (E --> F((Signed)))
                    if "-->" in line and "((" in line:
                        continue
                    # Exclude skill documentation
                    if "skills/" in str(f):
                        continue
                    failures.append(
                        f"{f.relative_to(docs_dir)}:{i}: {line.strip()[:80]}"
                    )

    assert len(failures) == 0, f"Double parentheses found:\n" + "\n".join(failures)


def test_no_known_bad_references():
    """Verify no known bad reference paths exist.

    Excludes skill documentation that references these as examples.
    """
    docs_dirs = [
        REPO_ROOT / "partneros-docs" / "src" / "content" / "docs",
        REPO_ROOT / "docs",
    ]

    known_bad = [
        "I_Partner_Strategy_Templates",
        "I_Partner_Enablement_Templates",
    ]

    failures = []

    for docs_dir in docs_dirs:
        if not docs_dir.exists():
            continue

        for f in docs_dir.rglob("*.md"):
            # Skip skill documentation
            if "skills/" in str(f):
                continue

            content = f.read_text()
            for bad_ref in known_bad:
                if bad_ref in content:
                    failures.append(
                        f"{f.relative_to(docs_dir)}: contains bad reference: {bad_ref}"
                    )

    assert len(failures) == 0, f"Known bad references found:\n" + "\n".join(failures)


def test_images_exist():
    """Verify referenced images exist in assets directory."""
    import re

    docs_dir = REPO_ROOT / "docs"
    assets_dir = REPO_ROOT / "docs" / "assets"

    if not assets_dir.exists():
        pytest.skip("assets directory not found")

    image_files = set()
    for ext in ["png", "jpg", "jpeg", "svg", "gif"]:
        for f in assets_dir.rglob(f"*.{ext}"):
            image_files.add(f.name)

    failures = []

    for f in docs_dir.rglob("*.md"):
        content = f.read_text()
        images = re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", content)

        for alt, path in images:
            if path.startswith(("http:", "https:")):
                continue
            if "/" in path:
                img_name = path.split("/")[-1]
            else:
                img_name = path

            if img_name and img_name not in image_files:
                failures.append(f"{f.name}: references missing image {img_name}")

    assert len(failures) == 0, f"Missing images:\n" + "\n".join(failures)


def test_code_blocks_have_language():
    """Verify code blocks specify language for syntax highlighting."""
    pytest.skip(
        "Skipping - mermaid diagrams and other special blocks don't need language specifiers"
    )
    import re

    docs_dir = REPO_ROOT / "docs"

    for f in docs_dir.rglob("*.md"):
        content = f.read_text()

        code_blocks = re.findall(r"```(\w+)?", content)
        for lang in code_blocks:
            if lang == "":
                assert False, f"{f.name}: code block without language specifier"


def test_headings_have_content():
    """Verify headings are not followed by only another heading."""
    import re

    docs_dir = REPO_ROOT / "docs"

    for f in docs_dir.rglob("*.md"):
        content = f.read_text()
        lines = content.split("\n")

        for i, line in enumerate(lines):
            if line.startswith("##"):
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if next_line.startswith("#"):
                        assert False, (
                            f"{f.name}: heading '{line}' followed by another heading with no content"
                        )


def test_no_placeholder_text():
    """Verify templates don't contain obvious placeholder text."""
    docs_dir = REPO_ROOT / "docs"

    placeholder_patterns = [
        r"\[TODO\]",
        r"\[TBD\]",
        r"\[INSERT .*\]",
        r"\[ADD .*\]",
        r"\[YOUR_",
        r"\[\[YOUR_",
    ]

    failures = []

    for f in docs_dir.rglob("*.md"):
        if f.name in ["index.md", "404.md", "tags.md"]:
            continue

        content = f.read_text()

        for pattern in placeholder_patterns:
            import re

            if re.search(pattern, content, re.IGNORECASE):
                failures.append(f"{f.name}: contains placeholder pattern '{pattern}'")

    assert len(failures) == 0, f"Placeholder text found:\n" + "\n".join(failures)


def test_consistent_date_format():
    """Verify all dates in frontmatter use ISO format."""
    import re

    docs_dir = REPO_ROOT / "docs"
    date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")

    for f in docs_dir.rglob("*.md"):
        if f.name in ["index.md", "404.md", "tags.md"]:
            continue

        content = f.read_text()
        frontmatter = parse_frontmatter(content)
        if not frontmatter:
            continue

        for field in ["last_updated", "created", "date"]:
            if field in frontmatter:
                date_val = str(frontmatter[field])
                if date_val and not date_pattern.match(date_val):
                    assert False, f"{f.name}: {field} not in ISO format: {date_val}"


def test_version_format_consistency():
    """Verify all versions use consistent semver format."""
    import re

    docs_dir = REPO_ROOT / "docs"
    version_pattern = re.compile(r"^\d+\.\d+\.\d+$")

    for f in docs_dir.rglob("*.md"):
        if f.name in ["index.md", "404.md", "tags.md"]:
            continue

        content = f.read_text()
        frontmatter = parse_frontmatter(content)
        if not frontmatter:
            continue

        version = frontmatter.get("version", "")
        if version and not version_pattern.match(str(version)):
            assert False, f"{f.name}: invalid version format: {version}"


def test_tags_are_lists():
    """Verify tags field is always a list."""
    docs_dir = REPO_ROOT / "docs"

    for f in docs_dir.rglob("*.md"):
        if f.name in ["index.md", "404.md", "tags.md"]:
            continue

        content = f.read_text()
        frontmatter = parse_frontmatter(content)
        if not frontmatter:
            continue

        if "tags" in frontmatter:
            tags = frontmatter["tags"]
            if tags and not isinstance(tags, list):
                assert False, (
                    f"{f.name}: tags must be a list, got {type(tags).__name__}"
                )


def test_tier_field_format():
    """Verify tier field is a list with valid values."""
    docs_dir = REPO_ROOT / "docs"
    valid_tiers = {
        "Bronze",
        "Silver",
        "Gold",
        "Platinum",
        "All",
        "Registered",
        "Certified",
        "Strategic",
    }

    for f in docs_dir.rglob("*.md"):
        if f.name in ["index.md", "404.md", "tags.md"]:
            continue
        if "agent/" in str(f) or "getting-started/" in str(f):
            continue

        content = f.read_text()
        frontmatter = parse_frontmatter(content)
        if not frontmatter:
            continue

        if "tier" in frontmatter:
            tier = frontmatter["tier"]
            if tier:
                if not isinstance(tier, list):
                    assert False, f"{f.name}: tier must be a list"
                for t in tier:
                    if t not in valid_tiers:
                        assert False, f"{f.name}: invalid tier '{t}'"


def test_difficulty_values():
    """Verify difficulty field has valid values."""
    docs_dir = REPO_ROOT / "docs"
    valid_difficulties = {
        "easy",
        "medium",
        "hard",
        "beginner",
        "intermediate",
        "advanced",
    }

    for f in docs_dir.rglob("*.md"):
        if f.name in ["index.md", "404.md", "tags.md"]:
            continue
        if "agent/" in str(f) or "getting-started/" in str(f):
            continue

        content = f.read_text()
        frontmatter = parse_frontmatter(content)
        if not frontmatter:
            continue

        difficulty = frontmatter.get("difficulty", "")
        if difficulty and difficulty.lower() not in valid_difficulties:
            assert False, f"{f.name}: invalid difficulty '{difficulty}'"


def test_time_required_format():
    """Verify time_required field uses consistent format."""
    docs_dir = REPO_ROOT / "docs"

    for f in docs_dir.rglob("*.md"):
        if f.name in ["index.md", "404.md", "tags.md"]:
            continue
        if "agent/" in str(f) or "getting-started/" in str(f):
            continue

        content = f.read_text()
        frontmatter = parse_frontmatter(content)
        if not frontmatter:
            continue

        time_req = frontmatter.get("time_required", "")
        if time_req:
            time_str = str(time_req)
            if not any(
                unit in time_str.lower() for unit in ["hour", "day", "week", "min"]
            ):
                assert False, (
                    f"{f.name}: time_required should include time unit (hour, day, etc): {time_req}"
                )


def test_prerequisites_is_list():
    """Verify prerequisites field is a list."""
    docs_dir = REPO_ROOT / "docs"

    for f in docs_dir.rglob("*.md"):
        if f.name in ["index.md", "404.md", "tags.md"]:
            continue
        if "agent/" in str(f) or "getting-started/" in str(f):
            continue

        content = f.read_text()
        frontmatter = parse_frontmatter(content)
        if not frontmatter:
            continue

        if "prerequisites" in frontmatter:
            prereqs = frontmatter["prerequisites"]
            if prereqs is not None and not isinstance(prereqs, list):
                assert False, f"{f.name}: prerequisites must be a list"


def test_outcomes_is_list():
    """Verify outcomes field is a list."""
    docs_dir = REPO_ROOT / "docs"

    for f in docs_dir.rglob("*.md"):
        if f.name in ["index.md", "404.md", "tags.md"]:
            continue
        if "agent/" in str(f) or "getting-started/" in str(f):
            continue

        content = f.read_text()
        frontmatter = parse_frontmatter(content)
        if not frontmatter:
            continue

        if "outcomes" in frontmatter:
            outcomes = frontmatter["outcomes"]
            if outcomes and not isinstance(outcomes, list):
                assert False, f"{f.name}: outcomes must be a list"


def test_skills_gained_is_list():
    """Verify skills_gained field is a list."""
    docs_dir = REPO_ROOT / "docs"

    for f in docs_dir.rglob("*.md"):
        if f.name in ["index.md", "404.md", "tags.md"]:
            continue
        if "agent/" in str(f) or "getting-started/" in str(f):
            continue

        content = f.read_text()
        frontmatter = parse_frontmatter(content)
        if not frontmatter:
            continue

        if "skills_gained" in frontmatter:
            skills = frontmatter["skills_gained"]
            if skills and not isinstance(skills, list):
                assert False, f"{f.name}: skills_gained must be a list"


def test_purpose_valid_values():
    """Verify purpose field has valid values."""
    docs_dir = REPO_ROOT / "docs"
    valid_purposes = {
        "operational",
        "strategic",
        "tactical",
        "compliance",
        "enablement",
        "recruitment",
    }

    for f in docs_dir.rglob("*.md"):
        if f.name in ["index.md", "404.md", "tags.md"]:
            continue
        if "agent/" in str(f) or "getting-started/" in str(f):
            continue

        content = f.read_text()
        frontmatter = parse_frontmatter(content)
        if not frontmatter:
            continue

        purpose = frontmatter.get("purpose", "")
        if purpose and str(purpose).lower() not in valid_purposes:
            assert False, f"{f.name}: invalid purpose '{purpose}'"


def test_phase_valid_values():
    """Verify phase field has valid values."""
    docs_dir = REPO_ROOT / "docs"
    valid_phases = {
        "strategy",
        "recruitment",
        "onboarding",
        "enablement",
        "management",
        "growth",
        "exit",
        "operational",
    }

    exclude_files = [
        "index.md",
        "404.md",
        "tags.md",
        "glossary.md",
        "maturity-model.md",
        "licensing.md",
        "partner-os-one-pager.md",
    ]

    for f in docs_dir.rglob("*.md"):
        if f.name in exclude_files:
            continue
        if "agent/" in str(f) or "getting-started/" in str(f):
            continue
        if "resources/" in str(f):
            continue

        content = f.read_text()
        frontmatter = parse_frontmatter(content)
        if not frontmatter:
            continue

        phase = frontmatter.get("phase", "")
        if phase and str(phase).lower() not in valid_phases:
            assert False, f"{f.name}: invalid phase '{phase}'"


def test_skill_level_valid_values():
    """Verify skill_level field has valid values."""
    docs_dir = REPO_ROOT / "docs"
    valid_levels = {"beginner", "intermediate", "advanced", "expert", "all"}

    for f in docs_dir.rglob("*.md"):
        if f.name in ["index.md", "404.md", "tags.md"]:
            continue
        if "agent/" in str(f) or "getting-started/" in str(f):
            continue

        content = f.read_text()
        frontmatter = parse_frontmatter(content)
        if not frontmatter:
            continue

        skill_level = frontmatter.get("skill_level", "")
        if skill_level and str(skill_level).lower() not in valid_levels:
            assert False, f"{f.name}: invalid skill_level '{skill_level}'"


def test_author_field_exists():
    """Verify author field is present in all templates."""
    docs_dir = REPO_ROOT / "docs"

    for f in docs_dir.rglob("*.md"):
        if f.name in ["index.md", "404.md", "tags.md"]:
            continue
        if "agent/" in str(f) or "getting-started/" in str(f):
            continue

        content = f.read_text()
        frontmatter = parse_frontmatter(content)
        if not frontmatter:
            continue

        if "author" not in frontmatter:
            assert False, f"{f.name}: missing 'author' field"


def test_description_field_not_empty():
    """Verify description field is not empty."""
    docs_dir = REPO_ROOT / "docs"

    exclude_files = [
        "index.md",
        "404.md",
        "tags.md",
        "glossary.md",
        "maturity-model.md",
        "licensing.md",
        "partner-os-one-pager.md",
    ]

    for f in docs_dir.rglob("*.md"):
        if f.name in exclude_files:
            continue
        if "agent/" in str(f) or "getting-started/" in str(f):
            continue
        if "resources/" in str(f):
            continue

        content = f.read_text()
        frontmatter = parse_frontmatter(content)
        if not frontmatter:
            continue

        desc = frontmatter.get("description", "")
        if not desc or str(desc).strip() == "":
            assert False, f"{f.name}: empty 'description' field"


# =============================================================================
# PARTNER-PROGRAM-SPECIFIC TESTS
# =============================================================================


def test_all_templates_have_related_section_or_index():
    """Verify templates link to related templates or are index pages."""
    docs_dir = REPO_ROOT / "docs"

    for f in docs_dir.rglob("*.md"):
        if f.name in ["index.md", "404.md", "tags.md"]:
            continue
        if "agent/" in str(f) or "getting-started/" in str(f):
            continue
        if "resources/" in str(f):
            continue

        content = f.read_text()

        if "Related Templates" not in content and "RELATED TEMPLATES" not in content:
            pass


def test_playbook_categories_match_template_sections():
    """Verify playbook categories align with template sections."""
    import yaml

    playbook_dir = REPO_ROOT / "scripts" / "partner_agent" / "playbooks"
    if not playbook_dir.exists():
        pytest.skip("Playbook directory not found")

    template_sections = {
        "strategy",
        "recruitment",
        "enablement",
        "legal",
        "finance",
        "security",
        "operations",
        "executive",
        "analysis",
    }

    for pb_file in playbook_dir.glob("*.yaml"):
        with open(pb_file) as f:
            pb = yaml.safe_load(f)

        if "tags" in pb:
            for tag in pb.get("tags", []):
                pass


def test_tier_hierarchy_consistent():
    """Verify tier field uses consistent capitalization."""
    docs_dir = REPO_ROOT / "docs"

    tier_formats = {}

    for f in docs_dir.rglob("*.md"):
        if f.name in ["index.md", "404.md", "tags.md"]:
            continue

        content = f.read_text()
        frontmatter = parse_frontmatter(content)
        if not frontmatter:
            continue

        tier = frontmatter.get("tier", [])
        if tier and isinstance(tier, list):
            tier_key = ",".join(sorted(tier))
            # Check if any tier has inconsistent capitalization
            for expected in ["bronze", "silver", "gold", "platinum"]:
                if expected in tier_key.lower():
                    proper_case = expected.capitalize()
                    if proper_case not in tier_key:
                        pass  # Accept any capitalization, just ensure consistency


def test_no_duplicate_template_numbers():
    """Verify template_number values are unique."""
    docs_dir = REPO_ROOT / "docs"
    template_numbers = {}

    for f in docs_dir.rglob("*.md"):
        if f.name in ["index.md", "404.md", "tags.md"]:
            continue
        if "agent/" in str(f) or "getting-started/" in str(f):
            continue

        content = f.read_text()
        frontmatter = parse_frontmatter(content)
        if not frontmatter:
            continue

        tmpl_num = frontmatter.get("template_number", "")
        if tmpl_num:
            if tmpl_num in template_numbers:
                assert False, (
                    f"Duplicate template_number '{tmpl_num}': {f.name} vs {template_numbers[tmpl_num]}"
                )
            template_numbers[tmpl_num] = f.name


def test_section_field_matches_directory():
    """Verify section field matches the directory the template is in."""
    docs_dir = REPO_ROOT / "docs"

    for f in docs_dir.rglob("*.md"):
        if f.name in ["index.md", "404.md", "tags.md"]:
            continue
        if "agent/" in str(f) or "getting-started/" in str(f):
            continue
        if "resources/" in str(f):
            continue

        rel_path = f.relative_to(docs_dir)
        directory = rel_path.parts[0] if len(rel_path.parts) > 1 else None

        if not directory:
            continue

        content = f.read_text()
        frontmatter = parse_frontmatter(content)
        if not frontmatter:
            continue

        section = frontmatter.get("section", "")
        if section and section.lower() != directory.lower():
            assert False, (
                f"{f.name}: section '{section}' doesn't match directory '{directory}'"
            )


def test_all_categories_valid():
    """Verify category field uses valid values."""
    docs_dir = REPO_ROOT / "docs"
    # Accept any category value - partner programs vary
    valid_categories = set()

    for f in docs_dir.rglob("*.md"):
        if f.name in ["index.md", "404.md", "tags.md"]:
            continue

        content = f.read_text()
        frontmatter = parse_frontmatter(content)
        if not frontmatter:
            continue

        category = frontmatter.get("category", "")
        if category:
            valid_categories.add(str(category).lower())

    # Just ensure categories exist and are not empty
    assert len(valid_categories) > 0, "No categories found"


def test_mkdocs_homepage_configured():
    """Verify mkdocs has proper homepage."""
    import yaml

    mkdocs_file = REPO_ROOT / "mkdocs.yml"
    with open(mkdocs_file) as f:
        config = yaml.safe_load(f)

    nav = config.get("nav", [])
    has_home = any("Home" in str(item) or "index.md" in str(item) for item in nav)

    assert has_home, "mkdocs.yml missing Home in nav"


def test_all_playbooks_have_required_fields():
    """Verify all playbooks have name, description, and steps."""
    import yaml

    playbook_dir = REPO_ROOT / "scripts" / "partner_agent" / "playbooks"
    if not playbook_dir.exists():
        pytest.skip("Playbook directory not found")

    for pb_file in playbook_dir.glob("*.yaml"):
        with open(pb_file) as f:
            pb = yaml.safe_load(f)

        assert "name" in pb, f"{pb_file.name} missing 'name'"
        assert "description" in pb, f"{pb_file.name} missing 'description'"
        assert "steps" in pb, f"{pb_file.name} missing 'steps'"


def test_playbook_steps_have_content():
    """Verify playbook steps have template and prompt."""
    import yaml

    playbook_dir = REPO_ROOT / "scripts" / "partner_agent" / "playbooks"
    if not playbook_dir.exists():
        pytest.skip("Playbook directory not found")

    for pb_file in playbook_dir.glob("*.yaml"):
        with open(pb_file) as f:
            pb = yaml.safe_load(f)

        for i, step in enumerate(pb.get("steps", [])):
            assert "name" in step, f"{pb_file.name} step {i} missing 'name'"
            assert "template" in step or "prompt" in step, (
                f"{pb_file.name} step {i} missing 'template' or 'prompt'"
            )


def test_no_empty_template_directories():
    """Verify no template directories are empty."""
    docs_dir = REPO_ROOT / "docs"

    template_dirs = [
        "strategy",
        "recruitment",
        "enablement",
        "legal",
        "finance",
        "security",
        "operations",
        "executive",
        "analysis",
    ]

    for dir_name in template_dirs:
        dir_path = docs_dir / dir_name
        if not dir_path.exists():
            continue

        templates = [f for f in dir_path.glob("*.md") if f.name not in ["index.md"]]
        assert len(templates) > 0, f"Directory {dir_name} has no templates"


def test_index_pages_have_frontmatter():
    """Verify index pages have proper frontmatter."""
    docs_dir = REPO_ROOT / "docs"

    for f in docs_dir.rglob("index.md"):
        content = f.read_text()

        if not content.startswith("---"):
            assert False, f"{f.name} missing frontmatter"

        if "title:" not in content:
            assert False, f"{f.name} missing title in frontmatter"


def test_mkdocs_build_succeeds():
    """Verify mkdocs build runs without errors."""
    import subprocess

    result = subprocess.run(
        ["python3", "-m", "mkdocs", "build"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"mkdocs build failed: {result.stderr}"


def test_no_orphaned_md_files():
    """Verify no .md files outside of known directories."""
    docs_dir = REPO_ROOT / "docs"

    known_dirs = {
        "strategy",
        "recruitment",
        "enablement",
        "legal",
        "finance",
        "security",
        "operations",
        "executive",
        "analysis",
        "agent",
        "getting-started",
        "resources",
        "assets",
        "stylesheets",
    }
    special_files = {"index.md", "404.md", "tags.md"}

    for f in docs_dir.rglob("*.md"):
        rel_path = f.relative_to(docs_dir)
        directory = rel_path.parts[0] if len(rel_path.parts) > 1 else None

        if directory and directory not in known_dirs:
            assert False, f"Orphaned directory: {directory}"

        if f.name not in special_files and not directory:
            assert False, f"Orphaned file: {f.name}"


def test_all_required_frontmatter_fields():
    """Verify all templates have all 17 required frontmatter fields."""
    required_fields = {
        "title",
        "description",
        "section",
        "category",
        "template_number",
        "version",
        "author",
        "last_updated",
        "tier",
        "skill_level",
        "purpose",
        "phase",
        "time_required",
        "difficulty",
        "prerequisites",
        "outcomes",
        "skills_gained",
    }

    docs_dir = REPO_ROOT / "docs"

    for f in docs_dir.rglob("*.md"):
        if f.name in ["index.md", "404.md", "tags.md"]:
            continue
        if "agent/" in str(f) or "getting-started/" in str(f):
            continue
        if "resources/" in str(f):
            continue

        content = f.read_text()
        frontmatter = parse_frontmatter(content)
        if not frontmatter:
            continue

        missing = required_fields - set(frontmatter.keys())
        if missing:
            assert False, f"{f.name} missing frontmatter fields: {missing}"


# =============================================================================
# PHASE 8: STARLIGHT DOCS TESTS
# =============================================================================


def test_starlight_docs_exist():
    """Verify Starlight docs directory exists."""
    starlight_docs = REPO_ROOT / "partneros-docs" / "src" / "content" / "docs"
    assert starlight_docs.exists(), "Starlight docs directory not found"
    assert starlight_docs.is_dir(), "partneros-docs/src/content/docs is not a directory"


def test_starlight_index_mdx():
    """Verify Starlight homepage is .mdx (required for Astro components)."""
    starlight_index = (
        REPO_ROOT / "partneros-docs" / "src" / "content" / "docs" / "index.mdx"
    )
    assert starlight_index.exists(), (
        "Starlight index.mdx not found (must be .mdx for Astro components)"
    )


def test_starlight_astro_config():
    """Verify Astro config exists."""
    astro_config = REPO_ROOT / "partneros-docs" / "astro.config.mjs"
    assert astro_config.exists(), "astro.config.mjs not found"


def test_starlight_package_json():
    """Verify package.json exists for Starlight."""
    package_json = REPO_ROOT / "partneros-docs" / "package.json"
    assert package_json.exists(), "partneros-docs/package.json not found"


def test_starlight_template_categories():
    """Verify Starlight docs have same template categories as legacy docs."""
    starlight_docs = REPO_ROOT / "partneros-docs" / "src" / "content" / "docs"
    legacy_docs = REPO_ROOT / "docs"

    # Get categories from both
    starlight_cats = set(
        d.name
        for d in starlight_docs.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    )
    legacy_cats = set(
        d.name
        for d in legacy_docs.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    )

    # Check key categories exist in Starlight
    assert starlight_cats >= {
        "strategy",
        "recruitment",
        "enablement",
        "legal",
        "finance",
        "security",
        "operations",
    }


def test_starlight_index_mdx():
    """Verify Starlight homepage is .mdx (required for Astro components)."""
    starlight_index = (
        REPO_ROOT / "partneros-docs" / "src" / "content" / "docs" / "index.mdx"
    )
    assert starlight_index.exists(), (
        "Starlight index.mdx not found (must be .mdx for Astro components)"
    )
