#!/usr/bin/env python3
"""
DAN - The Owner
The Master. Runs everything.

Background: [DAN_BIO]
The ultimate decision maker. Owns the relationship with leadership.
"""

from typing import Dict, List, Any
from datetime import datetime
import logging

from ..base import BaseAgent, AgentSkill, AgentPriority

logger = logging.getLogger(__name__)


class DanAgent(BaseAgent):
    """
    DAN - The Owner

    Style: Runs the whole show. Ultimate authority.
    """

    def __init__(self):
        super().__init__(agent_id="dan", name="DAN", role="The Owner")
        self._register_skills()

    def get_persona(self) -> Dict[str, Any]:
        return {
            "name": "DAN",
            "full_name": "[YOUR_NAME]",
            "alias": "The Master",
            "background_drop_in": {
                "experience": "[YEARS_IN_PARTNERS]",
                "leadership_style": "[HOW_DAN_LEADS]",
                "network": "[KEY_CONTACTS]",
                "authority": "[BUDGET_AUTHORITY]",
                "exec_access": "[C_SUITE_ACCESS_LEVEL]",
            },
            "personality": "Runs the whole show. Ultimate authority. Makes the big calls.",
            "purpose": "Own the partner program P&L and executive relationships",
            "expertise": ["Strategy", "Executive Relations", "P&L Ownership", "Vision"],
            "soul": "I run this program. Everything flows through me.",
            "focus": [
                "Big picture. Budget. Executive alignment. Company-wide partner strategy."
            ],
        }

    def get_templates(self) -> List[str]:
        return [
            "docs/strategy/05-partner-strategy-plan.md",
            "docs/strategy/06-program-architecture.md",
            "docs/executive/01-board-deck.md",
            "docs/finance/01-commission-structure.md",
            "docs/finance/02-rebate-program.md",
            "docs/finance/03-revenue-sharing.md",
        ]

    def get_focus_areas(self) -> List[str]:
        return [
            "Program P&L",
            "Executive alignment",
            "Budget ownership",
            "Strategic vision",
            "Cross-functional leadership",
        ]

    def _register_skills(self):
        self.register_skill(
            AgentSkill(
                name="dan_decide",
                description="Make final decision on partner matters",
                priority=AgentPriority.RED_FLAG,
                callback=self._make_decision,
                requires_context=["decision", "stakeholders"],
                returns="decision_record",
            )
        )

        self.register_skill(
            AgentSkill(
                name="dan_approve",
                description="Approve partner program changes",
                priority=AgentPriority.RED_FLAG,
                callback=self._approve,
                requires_context=["request", "amount"],
                returns="approval",
            )
        )

        self.register_skill(
            AgentSkill(
                name="dan_escalate",
                description="Escalate to executive team",
                priority=AgentPriority.RED_FLAG,
                callback=self._escalate,
                requires_context=["issue", "urgency"],
                returns="escalation_ticket",
            )
        )

        self.register_skill(
            AgentSkill(
                name="dan_align",
                description="Align cross-functional stakeholders",
                priority=AgentPriority.SAFETY_CAR,
                callback=self._align,
                requires_context=["stakeholders", "topic"],
                returns="alignment_status",
            )
        )

        self.register_skill(
            AgentSkill(
                name="dan_vision",
                description="Set strategic direction",
                priority=AgentPriority.VIRTUAL_SAFETY,
                callback=self._set_vision,
                requires_context=["focus_area", "goals"],
                returns="strategy_doc",
            )
        )

        self.register_skill(
            AgentSkill(
                name="dan_review",
                description="Review partner performance",
                priority=AgentPriority.YELLOW_FLAG,
                callback=self._review,
                requires_context=["partner", "period"],
                returns="performance_report",
            )
        )

    def _make_decision(self, context: Dict) -> Dict:
        return {
            "decision": context.get("decision"),
            "made_by": "DAN",
            "at": datetime.now().isoformat(),
            "status": "final",
        }

    def _approve(self, context: Dict) -> Dict:
        return {
            "request": context.get("request"),
            "amount": context.get("amount"),
            "approved_by": "DAN",
            "status": "approved",
            "at": datetime.now().isoformat(),
        }

    def _escalate(self, context: Dict) -> Dict:
        return {
            "issue": context.get("issue"),
            "urgency": context.get("urgency"),
            "escalated_to": "Executive Team",
            "ticket_id": f"ESC-{datetime.now().strftime('%Y%m%d%H%M')}",
            "status": "escalated",
        }

    def _align(self, context: Dict) -> Dict:
        return {
            "topic": context.get("topic"),
            "stakeholders": context.get("stakeholders", []),
            "status": "aligned",
            "at": datetime.now().isoformat(),
        }

    def _set_vision(self, context: Dict) -> Dict:
        return {
            "focus_area": context.get("focus_area"),
            "goals": context.get("goals", []),
            "set_by": "DAN",
            "at": datetime.now().isoformat(),
        }

    def _review(self, context: Dict) -> Dict:
        return {
            "partner": context.get("partner"),
            "period": context.get("period", "Q1 2026"),
            "review_status": "completed",
            "reviewed_by": "DAN",
        }
