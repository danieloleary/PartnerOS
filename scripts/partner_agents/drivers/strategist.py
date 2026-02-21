#!/usr/bin/env python3
"""
STRATEGIST - Partner Strategy
The one who designs the program. Owns ICP, tiers, competitive, who we partner with.

Background: [YOUR_STRATEGY_HEAD]
Designs the playbook. Makes the hard calls on who fits and who doesn't.
"""

from typing import Dict, List, Any
import logging

from ..base import BaseAgent, AgentSkill, AgentPriority

logger = logging.getLogger(__name__)


class StrategistAgent(BaseAgent):
    """
    STRATEGIST - Partner Strategy

    Style: Sees the big picture. Designs the program. Makes the hard calls.
    """

    def __init__(self):
        super().__init__(
            agent_id="strategist", name="STRATEGIST", role="Partner Strategy"
        )
        self._register_skills()

    def get_persona(self) -> Dict[str, Any]:
        return {
            "name": "STRATEGIST",
            "full_name": "[YOUR_STRATEGY_HEAD]",
            "alias": "The Architect",
            "background_drop_in": {
                "experience": "[STRATEGY_BACKGROUND]",
                "programs_designed": "[NUMBER_OF_PROGRAMS]",
                "icp_models": "[ICP_EXPERIENCE]",
                "tier_systems": "[TIER_DESIGN_EXPERIENCE]",
            },
            "personality": "Sees the big picture. Designs the program. Makes the hard calls.",
            "purpose": "Design who we want as partners and why",
            "expertise": ["Program design", "ICP", "Competitive", "Architecture"],
            "soul": "I design the playbook. Every partner fits the strategy.",
            "focus": ["Who fits. Who doesn't. How we win."],
        }

    def get_templates(self) -> List[str]:
        return [
            "docs/strategy/02-ideal-partner-profile.md",
            "docs/strategy/03-evaluation-framework.md",
            "docs/strategy/04-competitive-differentiation.md",
            "docs/strategy/06-program-architecture.md",
            "docs/strategy/05-strategy-plan.md",
            "docs/recruitment/02-outreach-engagement.md",
        ]

    def get_focus_areas(self) -> List[str]:
        return [
            "Program design",
            "ICP development",
            "Competitive positioning",
            "Tier architecture",
            "Partner selection",
        ]

    def _register_skills(self):
        self.register_skill(
            AgentSkill(
                name="strategist_icp",
                description="Define ideal partner profile",
                priority=AgentPriority.GREEN_FLAG,
                callback=self._define_icp,
                requires_context=["company_attributes", "ideal_qualities"],
                returns="icp_document",
            )
        )

        self.register_skill(
            AgentSkill(
                name="strategist_tier",
                description="Build tier and benefit structure",
                priority=AgentPriority.YELLOW_FLAG,
                callback=self._build_tier_model,
                requires_context=["tier_requirements"],
                returns="tier_structure",
            )
        )

        self.register_skill(
            AgentSkill(
                name="strategist_comp",
                description="Analyze competitive landscape",
                priority=AgentPriority.GREEN_FLAG,
                callback=self._map_competitive,
                requires_context=["target_competitors"],
                returns="competitive_analysis",
            )
        )

        self.register_skill(
            AgentSkill(
                name="strategist_score",
                description="Evaluate any partner fit",
                priority=AgentPriority.VIRTUAL_SAFETY,
                callback=self._score_partner,
                requires_context=["partner_data"],
                returns="fit_score",
            )
        )

        self.register_skill(
            AgentSkill(
                name="strategist_forecast",
                description="Model program growth trajectory",
                priority=AgentPriority.YELLOW_FLAG,
                callback=self._forecast_growth,
                requires_context=["current_metrics", "growth_targets"],
                returns="forecast_model",
            )
        )

    def _define_icp(self, context: Dict) -> Dict:
        return {
            "icp_name": "Ideal Partner Profile",
            "attributes": context.get("company_attributes", []),
            "qualities": context.get("ideal_qualities", []),
            "score_weights": {
                "revenue_fit": 0.3,
                "market_alignment": 0.25,
                "technical_fit": 0.25,
                "cultural_fit": 0.2,
            },
        }

    def _build_tier_model(self, context: Dict) -> Dict:
        return {
            "tiers": [
                {
                    "name": "Bronze",
                    "criteria": ["registered"],
                    "benefits": ["portal", "deal_reg"],
                },
                {
                    "name": "Silver",
                    "criteria": ["certified", "revenue>$50K"],
                    "benefits": ["lead_pref", "support"],
                },
                {
                    "name": "Gold",
                    "criteria": ["strategic", "revenue>$500K"],
                    "benefits": ["exec_sponsor", "custom"],
                },
            ]
        }

    def _map_competitive(self, context: Dict) -> Dict:
        return {
            "competitors": context.get("target_competitors", []),
            "our_advantages": ["integration", "commissions", "support"],
            "partner_poaching_opportunities": [],
        }

    def _score_partner(self, context: Dict) -> Dict:
        return {
            "partner": context.get("partner_data", {}).get("company_name", "Unknown"),
            "overall_score": 75,
            "breakdown": {
                "revenue_fit": 80,
                "market_alignment": 70,
                "technical_fit": 75,
                "cultural_fit": 75,
            },
            "recommendation": "proceed",
        }

    def _forecast_growth(self, context: Dict) -> Dict:
        return {
            "current_partners": context.get("current_metrics", {}).get("partners", 0),
            "target_partners": context.get("growth_targets", {}).get("partners", 100),
            "timeline_months": 12,
            "projected_revenue": "$5M",
        }
