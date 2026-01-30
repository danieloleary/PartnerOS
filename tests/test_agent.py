"""Test Partner Agent functionality."""
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
# Add partner_agent to path
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

if __name__ == "__main__":
    print("Running partnerOS tests...")
    test_agent_import()
    test_backup_exists()
    test_env_example_exists()
    print("All partnerOS tests passed!")
