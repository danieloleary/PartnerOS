"""Test Partner Agent functionality - Fixed v1.1."""
import os
import sys
import tempfile
from pathlib import Path

# Add partner_agent to path
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / 'scripts' / 'partner_agent'))


def test_agent_import():
    """Verify agent can be imported."""
    try:
        with open(REPO_ROOT / 'scripts' / 'partner_agent' / 'agent.py') as f:
            code = f.read()
        compile(code, 'agent.py', 'exec')
    except SyntaxError as e:
        raise AssertionError(f"Syntax error in agent.py: {e}")


def test_backup_exists():
    """Verify backup was created."""
    backup = REPO_ROOT / 'scripts' / 'partner_agent' / 'agent.py.backup'
    assert backup.exists(), "agent.py.backup not found"


def test_env_example_exists():
    """Verify .env.example was created."""
    env_file = REPO_ROOT / 'scripts' / 'partner_agent' / '.env.example'
    assert env_file.exists(), ".env.example not found"
    
    with open(env_file) as f:
        content = f.read()
    assert 'OLLAMA_ENDPOINT' in content
    assert 'OLLAMA_MODEL' in content


def test_partner_sanitization():
    """Test partner name sanitization."""
    # Import after path setup
    from partner_agent import PartnerAgent
    
    # Create temp config
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("provider: anthropic\n")
        f.write("model: sonnet-4-20250514\n")
        config_path = f.name
    
    try:
        agent = PartnerAgent(config_path=config_path)
        
        # Test valid names
        assert agent._sanitize_partner_name("Acme Corp") == "Acme Corp"
        assert agent._sanitize_partner_name("test-partner_123") == "test-partner_123"
        
        # Test invalid names
        try:
            agent._sanitize_partner_name("")
            assert False, "Should reject empty string"
        except ValueError:
            pass
        
        try:
            agent._sanitize_partner_name("../etc/passwd")
            assert False, "Should reject path traversal"
        except ValueError:
            pass
        
        try:
            agent._sanitize_partner_name("x" * 101)
            assert False, "Should reject >100 chars"
        except ValueError:
            pass
        
        print("✓ Partner sanitization tests passed")
    finally:
        os.unlink(config_path)


def test_path_validation():
    """Test path validation prevents traversal."""
    from partner_agent import PartnerAgent
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("provider: anthropic\n")
        f.write("model: sonnet-4-20250514\n")
        config_path = f.name
    
    try:
        agent = PartnerAgent(config_path=config_path)
        
        # Test valid path
        valid_path = Path("recruit.yaml")
        assert agent._validate_path(valid_path, agent.playbooks_dir)
        
        # Test invalid path (traversal)
        invalid_path = Path("../etc/passwd")
        assert not agent._validate_path(invalid_path, agent.playbooks_dir)
        
        # Test non-existent file
        invalid_path = Path("nonexistent.yaml")
        assert not agent._validate_path(invalid_path, agent.playbooks_dir)
        
        print("✓ Path validation tests passed")
    finally:
        os.unlink(config_path)


def test_slugify():
    """Test slugify with sanitization."""
    from partner_agent import PartnerAgent
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("provider: anthropic\n")
        f.write("model: sonnet-4-20250514\n")
        config_path = f.name
    
    try:
        agent = PartnerAgent(config_path=config_path)
        
        # Test valid slugify
        assert agent.slugify("Acme Corp") == "acme-corp"
        assert agent.slugify("Test Partner 123") == "test-partner-123"
        
        # Test that sanitization is applied first
        try:
            agent.slugify("../evil")
            assert False, "Should reject path traversal"
        except ValueError:
            pass
        
        print("✓ Slugify tests passed")
    finally:
        os.unlink(config_path)


if __name__ == "__main__":
    print("Running PartnerOS v1.1 tests...")
    
    test_agent_import()
    print("✓ Agent import test passed")
    
    test_backup_exists()
    print("✓ Backup exists test passed")
    
    test_env_example_exists()
    print("✓ Env example test passed")
    
    test_partner_sanitization()
    
    test_path_validation()
    
    test_slugify()
    
    print("\nAll PartnerOS tests passed!")
