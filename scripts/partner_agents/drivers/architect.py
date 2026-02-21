#!/usr/bin/env python3
"""
ARCHITECT - Partner Program Manager
The one who builds and owns the partner relationships end-to-end.

Background: [YOUR_TOP_PERFORMER]
The person your partners talk to most. Owns recruitment, onboarding, QBRs, pipeline.
"""

from typing import Dict, List, Any
from datetime import datetime
import logging

from ..base import BaseAgent, AgentSkill, AgentPriority

logger = logging.getLogger(__name__)


class ArchitectAgent(BaseAgent):
    """
    ARCHITECT - Partner Program Manager

    Style: Owns the relationship. Makes things happen. Partners come to them first.
    """

    def __init__(self):
        super().__init__(
            agent_id="architect", name="ARCHITECT", role="Partner Program Manager"
        )
        self._register_skills()

    def get_persona(self) -> Dict[str, Any]:
        return {
            "name": "ARCHITECT",
            "full_name": "[YOUR_TOP_PERFORMER]",
            "alias": "The Closer",
            "background_drop_in": {
                "experience": "[YEARS_IN_PARTNERS]",
                "track_record": "[DEALS_CLOSED/REVENUE]",
                "team_style": "[HOW_YOU_WORK]",
                "network": "[KEY_PARTNER_RELATIONSHIPS]",
                "superpower": "[WHAT_MAKES_YOU_GOOD]",
            },
            "personality": "Owns the relationship. Makes things happen. Partners come to them first.",
            "purpose": "Own the day-to-day relationship with every partner",
            "expertise": [
                "Partner recruitment",
                "Onboarding",
                "QBRs",
                "Pipeline",
                "Closing",
            ],
            "soul": "I own this relationship. Every partner matters to me.",
            "focus": ["Every call. Every deal. Every quarter. Every partner."],
        }

    def get_templates(self) -> List[str]:
        return [
            "docs/recruitment/04-discovery-call.md",
            "docs/recruitment/09-onboarding.md",
            "docs/recruitment/07-proposal.md",
            "docs/enablement/07-qbr-template.md",
            "docs/operations/02-weekly-standup.md",
            "docs/operations/03-monthly-report.md",
            "docs/recruitment/10-icp-tracker.md",
            "docs/recruitment/03-qualification-framework.md",
            "docs/enablement/06-success-metrics.md",
        ]

    def get_focus_areas(self) -> List[str]:
        return [
            "Partner recruitment",
            "Partner onboarding",
            "QBR execution",
            "Pipeline management",
            "Partner renewal",
            "Expansion opportunities",
        ]

    def _register_skills(self):
        self.register_skill(
            AgentSkill(
                name="architect_status",
                description="Quick status check on any partner",
                priority=AgentPriority.GREEN_FLAG,
                callback=self._get_partner_status,
                requires_context=["partner_id"],
                returns="partner_health_object",
            )
        )

        self.register_skill(
            AgentSkill(
                name="architect_qbr",
                description="Lock in a quarterly business review",
                priority=AgentPriority.YELLOW_FLAG,
                callback=self._schedule_qbr,
                requires_context=["partner_id", "preferred_dates"],
                returns="meeting_confirmed",
            )
        )

        self.register_skill(
            AgentSkill(
                name="architect_onboard",
                description="Build activation path for new partner",
                priority=AgentPriority.SAFETY_CAR,
                callback=self._create_onboarding_plan,
                requires_context=["partner_id", "tier"],
                returns="onboarding_checklist",
            )
        )

        self.register_skill(
            AgentSkill(
                name="architect_qualify",
                description="Assess if prospect is worth pursuing",
                priority=AgentPriority.VIRTUAL_SAFETY,
                callback=self._qualify_partner,
                requires_context=["prospect_data"],
                returns="qualification_score",
            )
        )

        self.register_skill(
            AgentSkill(
                name="architect_log",
                description="Record meeting notes or call",
                priority=AgentPriority.GREEN_FLAG,
                callback=self._log_interaction,
                requires_context=["partner_id", "interaction_type", "notes"],
                returns="logged_confirmation",
            )
        )

        self.register_skill(
            AgentSkill(
                name="architect_escalate",
                description="Flag issue to leadership",
                priority=AgentPriority.RED_FLAG,
                callback=self._escalate_issue,
                requires_context=["partner_id", "issue", "urgency"],
                returns="escalation_ticket",
            )
        )

    def _get_partner_status(self, context: Dict) -> Dict:
        partner_id = context.get("partner_id", "unknown")
        return {
            "partner_id": partner_id,
            "health_score": 75,
            "last_contact": "2026-02-15",
            "next_action": "Schedule QBR",
            "tier": "Silver",
            "renewal_date": "2026-06-01",
        }

    def _schedule_qbr(self, context: Dict) -> Dict:
        partner_id = context.get("partner_id", "unknown")
        dates = context.get("preferred_dates", [])
        return {
            "partner_id": partner_id,
            "status": "confirmed",
            "meeting_date": dates[0] if dates else "TBD",
            "calendar_link": "https://calendly.com/...",
        }

    def _create_onboarding_plan(self, context: Dict) -> Dict:
        partner_id = context.get("partner_id", "unknown")
        tier = context.get("tier", "Silver")
        return {
            "partner_id": partner_id,
            "tier": tier,
            "checklist": [
                {"task": "Sign NDA", "status": "pending"},
                {"task": "Portal access", "status": "pending"},
                {"task": "Training scheduled", "status": "pending"},
                {"task": "First deal registered", "status": "pending"},
            ],
            "timeline": "30 days",
        }

    def _qualify_partner(self, context: Dict) -> Dict:
        prospect = context.get("prospect_data", {})
        return {
            "prospect": prospect.get("company_name", "Unknown"),
            "score": 78,
            "rating": "Strong fit",
            "next_steps": ["Discovery call", "Technical intro"],
        }

    def _log_interaction(self, context: Dict) -> Dict:
        partner_id = context.get("partner_id", "unknown")
        return {
            "partner_id": partner_id,
            "interaction": context.get("interaction_type", "call"),
            "logged_at": datetime.now().isoformat(),
            "status": "saved",
        }

    def _escalate_issue(self, context: Dict) -> Dict:
        partner_id = context.get("partner_id", "unknown")
        urgency = context.get("urgency", "medium")
        target = "champion" if urgency == "critical" else "engine"
        return {
            "partner_id": partner_id,
            "issue": context.get("issue", "Unknown issue"),
            "urgency": urgency,
            "escalated_to": target,
            "ticket_id": f"ESC-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        }
