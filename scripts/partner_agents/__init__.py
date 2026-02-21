"""
PartnerOS Multi-Agent Partner Team
The collaborative partner program automation team.

Team:
- DAN: The Owner - runs everything
- ARCHITECT: Partner Program Manager - owns relationships
- STRATEGIST: Partner Strategy - ICP, tiers, selection
- ENGINE: Partner Operations - deals, commissions, portal
- SPARK: Partner Marketing - campaigns, leads, content
- CHAMPION: Partner Leader - board decks, ROI, exec comms
- BUILDER: Partner Technical - integrations, APIs, docs
"""

__version__ = "1.0.0"

from .base import BaseAgent, AgentPriority, AgentStatus, AgentSkill, HandoffRequest
from .orchestrator import Orchestrator, RaceStrategy
from .messages import TeamRadio, TeamMessage, MessageType
from .state import Telemetry, PartnerState, ProgramMetrics
from .config import TeamConfig

__all__ = [
    "BaseAgent",
    "AgentPriority",
    "AgentStatus",
    "AgentSkill",
    "HandoffRequest",
    "Orchestrator",
    "RaceStrategy",
    "TeamRadio",
    "TeamMessage",
    "MessageType",
    "Telemetry",
    "PartnerState",
    "ProgramMetrics",
    "TeamConfig",
]
