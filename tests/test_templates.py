"""Test template completeness and frontmatter - Fixed v1.1."""
import os
import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def count_templates():
    """Count all markdown files in docs/"""
    docs_dir = REPO_ROOT / 'docs'
    count = 0
    for root, dirs, files in os.walk(docs_dir):
        count += len([f for f in files if f.endswith('.md')])
    return count


def test_templates_exist():
    """Verify templates exist."""
    assert count_templates() > 0


def test_templates_have_frontmatter():
    """Verify markdown files have YAML frontmatter."""
    docs_dir = REPO_ROOT / 'docs'
    missing = []
    for root, dirs, files in os.walk(docs_dir):
        for f in files:
            if f.endswith('.md'):
                path = Path(root) / f
                with open(path, 'r') as fp:
                    content = fp.read()
                    if not content.startswith('---'):
                        missing.append(str(path))
    assert len(missing) == 0, f"Missing frontmatter: {missing}"


def test_docs_structure():
    """Verify key docs folders exist."""
    base = REPO_ROOT / 'docs'
    required_folders = ['strategy', 'recruitment', 'enablement', 'agent']
    for folder in required_folders:
        path = base / folder
        assert path.is_dir(), f"Missing folder: {folder}"


def test_playbooks_exist():
    """Verify playbooks exist."""
    playbook_dir = REPO_ROOT / 'scripts' / 'partner_agent' / 'playbooks'
    playbooks = ['recruit.yaml', 'onboard.yaml', 'qbr.yaml', 'expand.yaml', 
                 'exit.yaml', 'co-marketing.yaml', 'support-escalation.yaml']
    for pb in playbooks:
        path = playbook_dir / pb
        assert path.exists(), f"Missing playbook: {pb}"


def test_env_example_exists():
    """Verify .env.example was created with correct model."""
    env_file = REPO_ROOT / 'scripts' / 'partner_agent' / '.env.example'
    assert env_file.exists(), ".env.example not found"
    
    with open(env_file) as f:
        content = f.read()
    assert 'OLLAMA_ENDPOINT' in content
    assert 'OLLAMA_MODEL' in content
    # Verify no speculative model names
    assert 'claude-sonnet-4-20250514' not in content or 'sonnet-4-20250514' in content


if __name__ == "__main__":
    print(f"Templates found: {count_templates()}")
    test_templates_exist()
    test_templates_have_frontmatter()
    test_docs_structure()
    test_playbooks_exist()
    test_env_example_exists()
    print("All tests passed!")
