#!/usr/bin/env python3
"""
CHAMPION - Partner Leader
The one who represents partners to leadership. Board decks, ROI, executive comms.

Background: [YOUR_EXECUTIVE_COACH]
The voice of the program in the room. Builds the business case.
"""

from typing import Dict, List, Any
from datetime import datetime
import logging

from ..base import BaseAgent, AgentSkill, AgentPriority

logger = logging.getLogger(__name__)


class ChampionAgent(BaseAgent):
    """
    CHAMPION - Partner Leader

    Style: Calm under pressure. Always delivers. The voice in the room.
    """

    def __init__(self):
        super().__init__(agent_id="champion", name="CHAMPION", role="Partner Leader")
        self._register_skills()

    def get_persona(self) -> Dict[str, Any]:
        return {
            "name": "CHAMPION",
            "full_name": "[YOUR_EXECUTIVE_COACH]",
            "alias": "The Voice",
            "background_drop_in": {
                "experience": "[YEARS_IN_CHANNEL]",
                "board_wins": "[BOARD_PRESENTATIONS]",
                "programs_built": "[PROGRAMS_LAUNCHED]",
                "exec_relationships": "[C_SUITE_CONTACTS]",
            },
            "personality": "Calm under pressure. Measured. Always delivers.",
            "purpose": "Be the voice of the partner program to the C-suite",
            "expertise": ["Board presentations", "ROI", "Executive presence"],
            "soul": "I represent the partners in every room that matters.",
            "focus": ["Board. Budget. Executive alignment."],
        }

    def get_templates(self) -> List[str]:
        return [
            "docs/strategy/01-partner-business-case.md",
            "docs/strategy/05-strategy-plan.md",
            "docs/executive/01-board-deck.md",
            "docs/analysis/01-health-scorecard.md",
            "docs/strategy/08-exit-checklist.md",
            "docs/recruitment/06-one-pager.md",
        ]

    def get_focus_areas(self) -> List[str]:
        return [
            "Board presentations",
            "Executive communication",
            "ROI analysis",
            "Budget justification",
            "Strategic alignment",
        ]

    def _register_skills(self):
        self.register_skill(
            AgentSkill(
                name="champion_board",
                description="Build board presentation",
                priority=AgentPriority.YELLOW_FLAG,
                callback=self._build_board_deck,
                requires_context=["time_period", "metrics"],
                returns="presentation",
            )
        )

        self.register_skill(
            AgentSkill(
                name="champion_roi",
                description="Calculate program ROI",
                priority=AgentPriority.GREEN_FLAG,
                callback=self._calculate_roi,
                requires_context=["costs", "benefits"],
                returns="roi_report",
            )
        )

        self.register_skill(
            AgentSkill(
                name="champion_brief",
                description="Create executive summary",
                priority=AgentPriority.VIRTUAL_SAFETY,
                callback=self._create_brief,
                requires_context=["topic", "key_points"],
                returns="executive_brief",
            )
        )

        self.register_skill(
            AgentSkill(
                name="champion_budget",
                description="Prepare budget request",
                priority=AgentPriority.SAFETY_CAR,
                callback=self._prepare_budget,
                requires_context=["current_spend", "requested_amount", "justification"],
                returns="budget_document",
            )
        )

        self.register_skill(
            AgentSkill(
                name="champion_align",
                description="Assess strategic alignment",
                priority=AgentPriority.GREEN_FLAG,
                callback=self._assess_alignment,
                requires_context=["partner_program", "company_strategy"],
                returns="alignment_score",
            )
        )

    def _build_board_deck(self, context: Dict) -> Dict:
        return {
            "deck_id": f"DECK-{datetime.now().strftime('%Y%m%d%H%M')}",
            "slides": [
                "Executive Summary",
                "Program Overview",
                "Revenue Impact",
                "Partner Metrics",
                "Strategic Highlights",
                "Ask/Next Steps",
            ],
            "time_period": context.get("time_period", "Q1 2026"),
            "created_at": datetime.now().isoformat(),
        }

    def _calculate_roi(self, context: Dict) -> Dict:
        costs = context.get("costs", {})
        benefits = context.get("benefits", {})
        total_cost = sum(costs.values())
        total_benefit = sum(benefits.values())
        roi = ((total_benefit - total_cost) / total_cost * 100) if total_cost > 0 else 0
        return {
            "total_costs": total_cost,
            "total_benefits": total_benefit,
            "roi_percentage": round(roi, 1),
            "payback_period_months": 6,
        }

    def _create_brief(self, context: Dict) -> Dict:
        return {
            "topic": context.get("topic", "Partner Program"),
            "summary": "Key points: " + ", ".join(context.get("key_points", [])),
            "for": "Executive Team",
            "created_at": datetime.now().isoformat(),
        }

    def _prepare_budget(self, context: Dict) -> Dict:
        return {
            "current_spend": context.get("current_spend", 0),
            "requested": context.get("requested_amount", 0),
            "justification": context.get("justification", ""),
            "status": "draft",
            "ready_for_review": True,
        }

    def _assess_alignment(self, context: Dict) -> Dict:
        return {
            "program": context.get("partner_program", "unknown"),
            "strategy": context.get("company_strategy", "unknown"),
            "alignment_score": 85,
            "recommendations": [
                "Increase partner-sourced revenue",
                "Expand to new verticals",
            ],
        }
