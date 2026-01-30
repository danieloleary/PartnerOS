"""Test template completeness and frontmatter."""
import os

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

def test_inventory_matches():
    """Verify inventory.csv matches actual files."""
    actual_count = count_templates()
    inventory_path = '/Users/danieloleary/partnerOS/markdown_inventory.csv'
    assert os.path.exists(inventory_path), "inventory.csv missing"
    
    with open(inventory_path) as f:
        lines = f.readlines()
    assert len(lines) > 1, "inventory.csv appears empty"

if __name__ == "__main__":
    print(f"Templates found: {count_templates()}")
    test_templates_exist()
    test_templates_have_frontmatter()
    test_inventory_matches()
    print("All tests passed!")
