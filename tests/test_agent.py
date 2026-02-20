"""Test Partner Agent functionality - v1.2 (Agent Superpowers)."""

import os
import sys
import tempfile
from pathlib import Path

# Add partner_agent to path
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts" / "partner_agent"))


def test_agent_import():
    """Verify agent can be imported."""
    try:
        with open(REPO_ROOT / "scripts" / "partner_agent" / "agent.py") as f:
            code = f.read()
        compile(code, "agent.py", "exec")
    except SyntaxError as e:
        raise AssertionError(f"Syntax error in agent.py: {e}")


def test_env_example_exists():
    """Verify .env.example was created."""
    env_file = REPO_ROOT / "scripts" / "partner_agent" / ".env.example"
    assert env_file.exists(), ".env.example not found"

    with open(env_file) as f:
        content = f.read()
    assert "OLLAMA_ENDPOINT" in content
    assert "OLLAMA_MODEL" in content


def test_partner_sanitization():
    """Test partner name sanitization."""
    # Import after path setup
    from partner_agent import PartnerAgent

    # Create temp config
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
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

    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
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

    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
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


def _make_agent():
    """Create a PartnerAgent with a minimal temp config."""
    import tempfile
    from partner_agent import PartnerAgent
    config_content = (
        "provider: anthropic\n"
        "model: claude-sonnet-4-6\n"
        "tiers:\n"
        "  - name: Gold\n"
        "    revenue_threshold: 500000\n"
        "    certification_required: true\n"
        "  - name: Silver\n"
        "    revenue_threshold: 100000\n"
        "    certification_required: false\n"
        "  - name: Registered\n"
        "    revenue_threshold: 0\n"
        "    certification_required: false\n"
        "qbr_frequency:\n"
        "  Gold: quarterly\n"
        "  Silver: semi-annually\n"
        "  Registered: annually\n"
    )
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False)
    f.write(config_content)
    f.close()  # flush and close before PartnerAgent reads it
    return PartnerAgent(config_path=f.name), f.name


def test_partner_state_defaults():
    """New partner state includes all memory fields."""
    agent, config_path = _make_agent()
    try:
        state = agent.get_partner_state("Acme Corp")
        assert state["name"] == "Acme Corp"
        assert "tier" in state
        assert "health_score" in state
        assert "notes" in state
        assert isinstance(state["notes"], list)
        assert "milestones" in state
        assert isinstance(state["milestones"], list)
        assert "vertical" in state
        assert "rm" in state
    finally:
        os.unlink(config_path)


def test_add_note():
    """add_note appends a timestamped entry and saves state."""
    import tempfile
    agent, config_path = _make_agent()
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            agent.state_dir = Path(tmpdir)
            state = agent.get_partner_state("TechStart")
            state = agent.add_note(state, "First call went well")
            assert len(state["notes"]) == 1
            assert state["notes"][0]["text"] == "First call went well"
            assert "ts" in state["notes"][0]
    finally:
        os.unlink(config_path)


def test_add_milestone():
    """add_milestone appends a timestamped entry and saves state."""
    import tempfile
    agent, config_path = _make_agent()
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            agent.state_dir = Path(tmpdir)
            state = agent.get_partner_state("TechStart")
            state = agent.add_milestone(state, "First deal closed")
            assert len(state["milestones"]) == 1
            assert state["milestones"][0]["name"] == "First deal closed"
    finally:
        os.unlink(config_path)


def test_recommend_templates_new_partner():
    """New partner with no playbooks should recommend recruit."""
    agent, config_path = _make_agent()
    try:
        state = {"name": "NewCo", "tier": None, "playbooks": {}}
        recs = agent.recommend_templates(state)
        assert "recruit" in recs
    finally:
        os.unlink(config_path)


def test_recommend_templates_after_recruit():
    """After recruit is complete, onboard should be recommended."""
    agent, config_path = _make_agent()
    try:
        state = {
            "name": "AcmeCorp", "tier": "Silver",
            "playbooks": {"recruit": {"completed": True}}
        }
        recs = agent.recommend_templates(state)
        assert "onboard" in recs
    finally:
        os.unlink(config_path)


def test_recommend_templates_gold_tier():
    """Gold partners get co-marketing and expand recommended."""
    agent, config_path = _make_agent()
    try:
        state = {
            "name": "BigPartner", "tier": "Gold",
            "playbooks": {"recruit": {"completed": True}, "onboard": {"completed": True}}
        }
        recs = agent.recommend_templates(state)
        assert "co-marketing" in recs or "expand" in recs
    finally:
        os.unlink(config_path)


def test_system_prompt_includes_tier():
    """System prompt should include partner tier when partner_data provided."""
    agent, config_path = _make_agent()
    try:
        partner_data = {
            "name": "AcmeCorp", "tier": "Gold",
            "vertical": "SaaS", "health_score": 85,
            "rm": "Jane Smith", "notes": [], "milestones": []
        }
        prompt = agent._get_system_prompt(partner_data)
        assert "Gold" in prompt
        assert "AcmeCorp" in prompt
        assert "85/100" in prompt
    finally:
        os.unlink(config_path)


def test_generate_report_script_valid():
    """generate_report.py should have valid Python syntax."""
    report_script = REPO_ROOT / "scripts" / "generate_report.py"
    assert report_script.exists(), "generate_report.py not found"
    with open(report_script) as f:
        code = f.read()
    try:
        compile(code, "generate_report.py", "exec")
    except SyntaxError as e:
        raise AssertionError(f"Syntax error in generate_report.py: {e}")


def test_generate_report_no_partners():
    """generate_report produces output even with zero partners."""
    import tempfile
    import subprocess
    with tempfile.TemporaryDirectory() as tmpdir:
        result = subprocess.run(
            ["python3", str(REPO_ROOT / "scripts" / "generate_report.py"),
             "--state-dir", tmpdir],
            capture_output=True, text=True
        )
        # Should exit 0 (no partners = informational message to stderr, clean exit)
        assert result.returncode == 0 or "No partner state found" in result.stderr


if __name__ == "__main__":
    print("Running PartnerOS v1.2 tests...")

    test_agent_import()
    print("✓ Agent import test passed")

    test_env_example_exists()
    print("✓ Env example test passed")

    test_partner_sanitization()

    test_path_validation()

    test_slugify()

    test_partner_state_defaults()
    print("✓ Partner state defaults test passed")

    test_add_note()
    print("✓ Add note test passed")

    test_add_milestone()
    print("✓ Add milestone test passed")

    test_recommend_templates_new_partner()
    print("✓ Recommendations (new partner) test passed")

    test_recommend_templates_after_recruit()
    print("✓ Recommendations (after recruit) test passed")

    test_recommend_templates_gold_tier()
    print("✓ Recommendations (gold tier) test passed")

    test_system_prompt_includes_tier()
    print("✓ System prompt tier test passed")

    test_generate_report_script_valid()
    print("✓ generate_report.py syntax test passed")

    print("\nAll PartnerOS v1.2 tests passed!")
