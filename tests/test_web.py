"""Test PartnerOS web interface."""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))


def test_web_import():
    """Test that web module can be imported."""
    from scripts.partner_agents import web

    assert web is not None


def test_fallback_responses():
    """Test fallback response function."""
    from scripts.partner_agents.web import get_fallback_response

    # Test onboard
    result = get_fallback_response("Onboard Acme Corp as Gold partner")
    assert "partner" in result["response"].lower()
    assert result["agent"] == "Partner Manager"

    # Test deal
    result = get_fallback_response("Register a deal for TechCorp")
    assert "deal" in result["response"].lower()
    assert result["agent"] == "Operations"

    # Test marketing
    result = get_fallback_response("Launch a campaign")
    assert "campaign" in result["response"].lower()
    assert result["agent"] == "Marketing"

    # Test default
    result = get_fallback_response("Hello")
    assert "help" in result["response"].lower()


def test_chat_endpoint_structure():
    """Test that chat endpoint returns correct structure."""
    from scripts.partner_agents.web import get_fallback_response

    result = get_fallback_response("test")
    assert "response" in result
    assert "agent" in result
    assert isinstance(result["response"], str)
    assert isinstance(result["agent"], str)
