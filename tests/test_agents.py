"""Test Multi-Agent Partner Team functionality."""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))


def test_agents_import():
    """Verify all agents can be imported."""
    from scripts.partner_agents.drivers import (
        DanAgent,
        ArchitectAgent,
        StrategistAgent,
        EngineAgent,
        SparkAgent,
        ChampionAgent,
        BuilderAgent,
    )

    assert DanAgent is not None
    assert ArchitectAgent is not None
    assert StrategistAgent is not None
    assert EngineAgent is not None
    assert SparkAgent is not None
    assert ChampionAgent is not None
    assert BuilderAgent is not None


def test_framework_imports():
    """Verify framework modules can be imported."""
    from scripts.partner_agents import BaseAgent, Orchestrator
    from scripts.partner_agents.base import AgentPriority, AgentStatus, AgentSkill
    from scripts.partner_agents.messages import TeamRadio
    from scripts.partner_agents.state import Telemetry

    assert BaseAgent is not None
    assert Orchestrator is not None
    assert AgentPriority is not None
    assert AgentStatus is not None


def test_dan_agent():
    """Test DAN agent creation and skills."""
    from scripts.partner_agents.drivers import DanAgent

    agent = DanAgent()
    assert agent.agent_id == "dan"
    assert agent.name == "DAN"
    assert len(agent.skills) == 6

    persona = agent.get_persona()
    assert persona["name"] == "DAN"
    assert persona["purpose"] is not None

    templates = agent.get_templates()
    assert len(templates) == 6


def test_architect_agent():
    """Test ARCHITECT agent creation and skills."""
    from scripts.partner_agents.drivers import ArchitectAgent

    agent = ArchitectAgent()
    assert agent.agent_id == "architect"
    assert len(agent.skills) == 6

    result = agent.call_skill(
        "architect_onboard", {"partner_id": "Test", "tier": "Gold"}
    )
    assert result["tier"] == "Gold"
    assert len(result["checklist"]) == 4


def test_strategist_agent():
    """Test STRATEGIST agent creation and skills."""
    from scripts.partner_agents.drivers import StrategistAgent

    agent = StrategistAgent()
    assert agent.agent_id == "strategist"
    assert len(agent.skills) == 5

    result = agent.call_skill(
        "strategist_icp",
        {"company_attributes": ["SaaS"], "ideal_qualities": ["Enterprise"]},
    )
    assert "icp_name" in result


def test_engine_agent():
    """Test ENGINE agent creation and skills."""
    from scripts.partner_agents.drivers import EngineAgent

    agent = EngineAgent()
    assert agent.agent_id == "engine"
    assert len(agent.skills) == 5

    result = agent.call_skill(
        "engine_register",
        {"partner_id": "TestCorp", "deal_value": 50000, "account_name": "Acme"},
    )
    assert "deal_id" in result
    assert result["status"] == "registered"


def test_spark_agent():
    """Test SPARK agent creation and skills."""
    from scripts.partner_agents.drivers import SparkAgent

    agent = SparkAgent()
    assert agent.agent_id == "spark"
    assert len(agent.skills) == 5

    result = agent.call_skill(
        "spark_ignite",
        {"campaign_name": "Launch", "partner": "Acme", "type": "webinar"},
    )
    assert result["status"] == "launched"


def test_champion_agent():
    """Test CHAMPION agent creation and skills."""
    from scripts.partner_agents.drivers import ChampionAgent

    agent = ChampionAgent()
    assert agent.agent_id == "champion"
    assert len(agent.skills) == 5

    result = agent.call_skill("champion_board", {"time_period": "Q1", "metrics": {}})
    assert "deck_id" in result


def test_builder_agent():
    """Test BUILDER agent creation and skills."""
    from scripts.partner_agents.drivers import BuilderAgent

    agent = BuilderAgent()
    assert agent.agent_id == "builder"
    assert len(agent.skills) == 4

    result = agent.call_skill(
        "builder_integrate", {"partner": "Acme", "integration_type": "api"}
    )
    assert result["status"] == "in_progress"


def test_skill_registration():
    """Test that skills are registered correctly."""
    from scripts.partner_agents.drivers import ArchitectAgent

    agent = ArchitectAgent()
    assert "architect_onboard" in agent.skills
    assert "architect_status" in agent.skills
    assert "architect_qbr" in agent.skills


def test_skill_execution():
    """Test that skill execution returns expected data."""
    from scripts.partner_agents.drivers import EngineAgent

    agent = EngineAgent()

    result = agent.call_skill(
        "engine_calculate", {"deal_id": "D1", "partner_tier": "Gold"}
    )
    assert result["tier"] == "Gold"
    assert "commission" in result


def test_orchestrator():
    """Test orchestrator can coordinate agents."""
    from scripts.partner_agents.drivers import ArchitectAgent, EngineAgent
    from scripts.partner_agents import Orchestrator
    from scripts.partner_agents.base import AgentPriority

    orchestrator = Orchestrator()

    architect = ArchitectAgent()
    engine = EngineAgent()

    orchestrator.register_driver(architect)
    orchestrator.register_driver(engine)

    result = orchestrator.call_driver(
        "architect",
        "architect_onboard",
        {"partner_id": "TestCorp", "tier": "Gold"},
        from_driver="system",
    )

    assert result["agent"] == "architect"
    assert result["skill_used"] == "architect_onboard"


def test_team_stats():
    """Test total team stats."""
    from scripts.partner_agents.drivers import (
        DanAgent,
        ArchitectAgent,
        StrategistAgent,
        EngineAgent,
        SparkAgent,
        ChampionAgent,
        BuilderAgent,
    )

    agents = [
        DanAgent(),
        ArchitectAgent(),
        StrategistAgent(),
        EngineAgent(),
        SparkAgent(),
        ChampionAgent(),
        BuilderAgent(),
    ]

    total_skills = sum(len(a.skills) for a in agents)
    total_templates = sum(len(a.get_templates()) for a in agents)

    assert total_skills == 36
    assert total_templates == 47
