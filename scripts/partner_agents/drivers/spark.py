#!/usr/bin/env python3
"""
SPARK - Partner Marketing
The one who ignites campaigns. Gets partners out there and generating leads.

Background: [YOUR_GTM_LEAD]
Creates the buzz. Runs campaigns. Gets partners in front of customers.
"""

from typing import Dict, List, Any
from datetime import datetime
import logging

from ..base import BaseAgent, AgentSkill, AgentPriority

logger = logging.getLogger(__name__)


class SparkAgent(BaseAgent):
    """
    SPARK - Partner Marketing

    Style: Ignites campaigns. Gets the crowd hyped.
    """

    def __init__(self):
        super().__init__(agent_id="spark", name="SPARK", role="Partner Marketing")
        self._register_skills()

    def get_persona(self) -> Dict[str, Any]:
        return {
            "name": "SPARK",
            "full_name": "[YOUR_GTM_LEAD]",
            "alias": "The Igniter",
            "background_drop_in": {
                "experience": "[MARKETING_EXPERIENCE]",
                "campaigns_run": "[CAMPAIGNS_LAUNCHED]",
                "leads_generated": "[LEAD_VOLUME]",
                "content_style": "[CONTENT_APPROACH]",
            },
            "personality": "Ignites campaigns. Gets the crowd hyped. Fun but delivers.",
            "purpose": "Generate leads and revenue through partner channels",
            "expertise": ["Demand gen", "Content", "Events", "Social"],
            "soul": "I make partners visible. I turn interest into pipeline.",
            "focus": ["Crowd energy. Engagement. Converting interest to customers."],
        }

    def get_templates(self) -> List[str]:
        return [
            "docs/recruitment/01-email-sequence.md",
            "docs/recruitment/05-pitch-deck.md",
            "docs/recruitment/06-one-pager.md",
            "docs/enablement/04-co-marketing.md",
            "docs/enablement/02-training-deck.md",
            "docs/enablement/01-roadmap.md",
            "docs/enablement/03-certification.md",
        ]

    def get_focus_areas(self) -> List[str]:
        return [
            "Demand generation",
            "Campaign creation",
            "Content marketing",
            "Partner enablement",
            "Event marketing",
        ]

    def _register_skills(self):
        self.register_skill(
            AgentSkill(
                name="spark_ignite",
                description="Launch a co-marketing campaign",
                priority=AgentPriority.YELLOW_FLAG,
                callback=self._launch_campaign,
                requires_context=["campaign_name", "partner", "type"],
                returns="campaign_details",
            )
        )

        self.register_skill(
            AgentSkill(
                name="spark_sequence",
                description="Write email outreach sequence",
                priority=AgentPriority.GREEN_FLAG,
                callback=self._write_sequence,
                requires_context=["template", "partner_name", "goal"],
                returns="email_sequence",
            )
        )

        self.register_skill(
            AgentSkill(
                name="spark_deck",
                description="Build sales pitch deck",
                priority=AgentPriority.VIRTUAL_SAFETY,
                callback=self._build_deck,
                requires_context=["partner", "key_messages"],
                returns="deck_outline",
            )
        )

        self.register_skill(
            AgentSkill(
                name="spark_leads",
                description="Track leads from campaign",
                priority=AgentPriority.GREEN_FLAG,
                callback=self._track_leads,
                requires_context=["campaign_id"],
                returns="lead_report",
            )
        )

        self.register_skill(
            AgentSkill(
                name="spark_content",
                description="Request partner content assets",
                priority=AgentPriority.GREEN_FLAG,
                callback=self._request_content,
                requires_context=["content_type", "partner"],
                returns="content_plan",
            )
        )

    def _launch_campaign(self, context: Dict) -> Dict:
        return {
            "campaign_id": f"CAMP-{datetime.now().strftime('%Y%m%d')}",
            "name": context.get("campaign_name", "New Campaign"),
            "partner": context.get("partner"),
            "type": context.get("type", "webinar"),
            "status": "launched",
            "launched_at": datetime.now().isoformat(),
        }

    def _write_sequence(self, context: Dict) -> Dict:
        return {
            "template": context.get("template", "outreach"),
            "partner": context.get("partner_name"),
            "emails": [
                {"subject": "Partnership Opportunity", "body": "..."},
                {"subject": "Following up", "body": "..."},
                {"subject": "Let's connect", "body": "..."},
            ],
            "created_at": datetime.now().isoformat(),
        }

    def _build_deck(self, context: Dict) -> Dict:
        return {
            "partner": context.get("partner"),
            "slides": [
                "Title",
                "Why Partner",
                "Mutual Benefits",
                "Success Stories",
                "Next Steps",
            ],
            "created_at": datetime.now().isoformat(),
        }

    def _track_leads(self, context: Dict) -> Dict:
        return {
            "campaign_id": context.get("campaign_id"),
            "total_leads": 150,
            "qualified": 45,
            "converted": 12,
            "pipeline_value": "$250000",
        }

    def _request_content(self, context: Dict) -> Dict:
        return {
            "content_type": context.get("content_type", "case_study"),
            "partner": context.get("partner"),
            "status": "requested",
            "due_date": "2026-03-01",
        }
