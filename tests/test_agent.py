"""Test Partner Agent functionality."""
import os
import sys

# Add partner_agent to path
sys.path.insert(0, '/Users/danieloleary/partnerOS/scripts/partner_agent')

def test_agent_import():
    """Verify agent can be imported."""
    try:
        with open('/Users/danieloleary/partnerOS/scripts/partner_agent/agent.py') as f:
            code = f.read()
        compile(code, 'agent.py', 'exec')
    except SyntaxError as e:
        raise AssertionError(f"Syntax error in agent.py: {e}")

def test_backup_exists():
    """Verify backup was created."""
    backup = '/Users/danieloleary/partnerOS/scripts/partner_agent/agent.py.backup'
    assert os.path.exists(backup), "agent.py.backup not found"

def test_env_example_exists():
    """Verify .env.example was created."""
    env_file = '/Users/danieloleary/partnerOS/scripts/partner_agent/.env.example'
    assert os.path.exists(env_file), ".env.example not found"
    
    with open(env_file) as f:
        content = f.read()
    assert 'OLLAMA_ENDPOINT' in content
    assert 'OLLAMA_MODEL' in content

if __name__ == "__main__":
    print("Running partnerOS tests...")
    test_agent_import()
    test_backup_exists()
    test_env_example_exists()
    print("All partnerOS tests passed!")
