"""Test template completeness and frontmatter."""
import os
import sys

# Add partnerOS to path
sys.path.insert(0, '/Users/danieloleary/partnerOS')

def count_templates():
    """Count all markdown files in docs/"""
    count = 0
    for root, dirs, files in os.walk('/Users/danieloleary/partnerOS/docs'):
        count += len([f for f in files if f.endswith('.md')])
    return count

def test_templates_exist():
    """Verify templates exist."""
    assert count_templates() > 0

def test_templates_have_frontmatter():
    """Verify markdown files have YAML frontmatter."""
    missing = []
    for root, dirs, files in os.walk('/Users/danieloleary/partnerOS/docs'):
        for f in files:
            if f.endswith('.md'):
                path = os.path.join(root, f)
                with open(path, 'r') as fp:
                    content = fp.read()
                    if not content.startswith('---'):
                        missing.append(f)
    assert len(missing) == 0, f"Missing frontmatter: {missing}"

def test_docs_structure():
    """Verify key docs folders exist."""
    base = '/Users/danieloleary/partnerOS/docs'
    required_folders = ['strategy', 'recruitment', 'enablement', 'agent']
    for folder in required_folders:
        path = os.path.join(base, folder)
        assert os.path.isdir(path), f"Missing folder: {folder}"

def test_playbooks_exist():
    """Verify playbooks exist."""
    playbook_dir = '/Users/danieloleary/partnerOS/scripts/partner_agent/playbooks'
    playbooks = ['recruit.yaml', 'onboard.yaml', 'qbr.yaml', 'expand.yaml', 
                 'exit.yaml', 'co-marketing.yaml', 'support-escalation.yaml']
    for pb in playbooks:
        path = os.path.join(playbook_dir, pb)
        assert os.path.exists(path), f"Missing playbook: {pb}"

if __name__ == "__main__":
    print(f"Templates found: {count_templates()}")
    test_templates_exist()
    test_templates_have_frontmatter()
    test_docs_structure()
    test_playbooks_exist()
    print("All tests passed!")
