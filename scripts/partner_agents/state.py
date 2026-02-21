#!/usr/bin/env python3
"""
Telemetry System - Live state tracking
The data layer for all agent activity.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
from pathlib import Path


@dataclass
class PartnerState:
    """State for a single partner"""

    partner_id: str
    company_name: str
    tier: str
    health_score: int = 50
    owner: str = "max"
    last_contact: Optional[str] = None
    next_action: Optional[str] = None
    renewal_date: Optional[str] = None
    expansion_opportunity: Optional[str] = None
    blockers: List[str] = field(default_factory=list)
    champion: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class ProgramMetrics:
    """Program-level telemetry"""

    total_partners: int = 0
    active_partners: int = 0
    partners_by_tier: Dict[str, int] = field(default_factory=dict)
    total_pipeline: float = 0.0
    closed_revenue: float = 0.0
    mtd_new_partners: int = 0
    ytd_new_partners: int = 0


class Telemetry:
    """
    The telemetry system.
    Persists partner state, program metrics, activity logs.
    """

    def __init__(self, state_dir: str = "scripts/partner_agents/state"):
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True)

        self.partners: Dict[str, PartnerState] = {}
        self.metrics = ProgramMetrics()
        self.activity_log: List[Dict] = []

    def save_partner(self, state: PartnerState):
        """Persist partner state"""
        self.partners[state.partner_id] = state

        file_path = self.state_dir / f"{state.partner_id}.json"
        with open(file_path, "w") as f:
            json.dump(
                {
                    "partner_id": state.partner_id,
                    "company_name": state.company_name,
                    "tier": state.tier,
                    "health_score": state.health_score,
                    "owner": state.owner,
                    "last_contact": state.last_contact,
                    "next_action": state.next_action,
                    "renewal_date": state.renewal_date,
                    "blockers": state.blockers,
                    "champion": state.champion,
                    "metadata": state.metadata,
                    "updated_at": state.updated_at,
                },
                f,
                indent=2,
            )

    def load_partner(self, partner_id: str) -> Optional[PartnerState]:
        """Load partner from disk"""
        if partner_id in self.partners:
            return self.partners[partner_id]

        file_path = self.state_dir / f"{partner_id}.json"
        if file_path.exists():
            with open(file_path) as f:
                data = json.load(f)
                state = PartnerState(**data)
                self.partners[partner_id] = state
                return state
        return None

    def get_partners_by_driver(self, driver_id: str) -> List[PartnerState]:
        """Get all partners owned by a specific driver"""
        return [p for p in self.partners.values() if p.owner == driver_id]

    def log_activity(self, driver_id: str, action: str, details: Dict):
        """Log an activity"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "driver": driver_id,
            "action": action,
            "details": details,
        }
        self.activity_log.append(entry)

    def get_driver_telemetry(self, driver_id: str) -> Dict:
        """Get full telemetry for a driver"""
        partners = self.get_partners_by_driver(driver_id)

        return {
            "driver": driver_id,
            "partner_count": len(partners),
            "avg_health": sum(p.health_score for p in partners) / max(len(partners), 1),
            "partners": [
                {
                    "id": p.partner_id,
                    "company": p.company_name,
                    "tier": p.tier,
                    "health": p.health_score,
                    "next_action": p.next_action,
                }
                for p in partners
            ],
        }


telemetry = Telemetry()
