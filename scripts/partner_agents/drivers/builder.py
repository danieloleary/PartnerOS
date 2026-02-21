#!/usr/bin/env python3
"""
BUILDER - Partner Technical
The one who builds integrations. API docs, SDKs, technical partner success.

Background: [YOUR_TECHNICAL_LEAD]
Makes partners work. Integrations, APIs, developer experience.
"""

from typing import Dict, List, Any
from datetime import datetime
import logging

from ..base import BaseAgent, AgentSkill, AgentPriority

logger = logging.getLogger(__name__)


class BuilderAgent(BaseAgent):
    """
    BUILDER - Partner Technical

    Style: Builds things. Makes integrations work. Developer experience.
    """

    def __init__(self):
        super().__init__(agent_id="builder", name="BUILDER", role="Partner Technical")
        self._register_skills()

    def get_persona(self) -> Dict[str, Any]:
        return {
            "name": "BUILDER",
            "full_name": "[YOUR_TECHNICAL_LEAD]",
            "alias": "The Architect",
            "background_drop_in": {
                "experience": "[TECHNICAL_BACKGROUND]",
                "integrations_built": "[INTEGRATION_COUNT]",
                "api_experience": "[API_DESIGN]",
                "devrel_style": "[HOW_YOU_SUPPORT_DEVS]",
            },
            "personality": "Builds things. Makes integrations work. Developer experience.",
            "purpose": "Enable technical integration and partner developer success",
            "expertise": ["APIs", "Integrations", "Documentation", "SDKs"],
            "soul": "I make partners work. Every integration is on me.",
            "focus": ["API quality. Integration speed. Developer experience."],
        }

    def get_templates(self) -> List[str]:
        return [
            "docs/enablement/05-technical-integration.md",
            "docs/security/01-security-questionnaire.md",
            "docs/security/02-soc2-compliance.md",
            "docs/operations/04-partner-portal.md",
        ]

    def get_focus_areas(self) -> List[str]:
        return [
            "API documentation",
            "Integration support",
            "Technical onboarding",
            "Developer experience",
            "Security compliance",
        ]

    def _register_skills(self):
        self.register_skill(
            AgentSkill(
                name="builder_integrate",
                description="Build or accelerate technical integration",
                priority=AgentPriority.RED_FLAG,
                callback=self._build_integration,
                requires_context=["partner", "integration_type"],
                returns="integration_plan",
            )
        )

        self.register_skill(
            AgentSkill(
                name="builder_stabilize",
                description="Stabilize integration",
                priority=AgentPriority.YELLOW_FLAG,
                callback=self._stabilize_integration,
                requires_context=["partner", "focus_area"],
                returns="stability_report",
            )
        )

        self.register_skill(
            AgentSkill(
                name="builder_docs",
                description="Generate API documentation",
                priority=AgentPriority.GREEN_FLAG,
                callback=self._generate_docs,
                requires_context=["api_spec", "format"],
                returns="documentation",
            )
        )

        self.register_skill(
            AgentSkill(
                name="builder_support",
                description="Technical support escalation",
                priority=AgentPriority.RED_FLAG,
                callback=self._tech_support,
                requires_context=["issue", "priority"],
                returns="support_ticket",
            )
        )

    def _build_integration(self, context: Dict) -> Dict:
        return {
            "partner": context.get("partner"),
            "integration_type": context.get("integration_type", "api"),
            "status": "in_progress",
            "started_at": datetime.now().isoformat(),
            "expected_completion": "2026-03-15",
        }

    def _stabilize_integration(self, context: Dict) -> Dict:
        return {
            "partner": context.get("partner"),
            "focus_area": context.get("focus_area", "performance"),
            "status": "stabilized",
            "completed_at": datetime.now().isoformat(),
        }

    def _generate_docs(self, context: Dict) -> Dict:
        return {
            "api_spec": context.get("api_spec"),
            "format": context.get("format", "openapi"),
            "sections": ["Authentication", "Endpoints", "Webhooks", "Errors"],
            "generated_at": datetime.now().isoformat(),
        }

    def _tech_support(self, context: Dict) -> Dict:
        return {
            "issue": context.get("issue"),
            "priority": context.get("priority", "medium"),
            "ticket_id": f"TICKET-{datetime.now().strftime('%Y%m%d%H%M')}",
            "status": "created",
        }
