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
        "finance": 1,
        "security": 1,
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
