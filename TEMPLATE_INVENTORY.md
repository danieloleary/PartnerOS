# PartnerOS Template Inventory

**Updated:** February 20, 2026
**Single Source of Truth:** `docs/`

---

## Summary

| Category | Count |
|----------|-------|
| **Strategy** | 8 templates |
| **Recruitment** | 10 templates |
| **Enablement** | 7 templates |
| **Getting Started** | 3 guides |
| **Resources** | 2 references |
| **Agent Docs** | 4 pages |
| **Total** | **34 templates** |

---

## Templates by Category

### Strategy (8)

| # | File | Title |
|---|------|-------|
| 1 | `docs/strategy/01-partner-business-case.md` | Partner Business Case |
| 2 | `docs/strategy/02-ideal-partner-profile.md` | Ideal Partner Profile |
| 3 | `docs/strategy/03-evaluation-framework.md` | 3C/4C Evaluation Framework |
| 4 | `docs/strategy/04-competitive-differentiation.md` | Competitive Differentiation |
| 5 | `docs/strategy/05-strategy-plan.md` | Partner Strategy Plan |
| 6 | `docs/strategy/06-program-architecture.md` | Program Architecture |
| 7 | `docs/strategy/07-internal-alignment.md` | Internal Alignment Playbook |
| 8 | `docs/strategy/08-exit-checklist.md` | Partner Exit Checklist |

### Recruitment (10)

| # | File | Title |
|---|------|-------|
| 1 | `docs/recruitment/01-email-sequence.md` | Recruitment Email Sequence |
| 2 | `docs/recruitment/02-outreach-engagement.md` | Outreach Engagement Sequence |
| 3 | `docs/recruitment/03-qualification-framework.md` | Partner Qualification Framework |
| 4 | `docs/recruitment/04-discovery-call.md` | Discovery Call Script |
| 5 | `docs/recruitment/05-pitch-deck.md` | Partner Pitch Deck |
| 6 | `docs/recruitment/06-one-pager.md` | Partnership One-Pager |
| 7 | `docs/recruitment/07-proposal.md` | Partnership Proposal |
| 8 | `docs/recruitment/08-agreement.md` | Partnership Agreement |
| 9 | `docs/recruitment/09-onboarding.md` | Onboarding Checklist |
| 10 | `docs/recruitment/10-icp-tracker.md` | ICP Alignment Tracker |

### Enablement (7)

| # | File | Title |
|---|------|-------|
| 1 | `docs/enablement/01-roadmap.md` | Enablement Roadmap |
| 2 | `docs/enablement/02-training-deck.md` | Training Deck |
| 3 | `docs/enablement/03-certification.md` | Partner Certification Program |
| 4 | `docs/enablement/04-co-marketing.md` | Co-Marketing Playbook |
| 5 | `docs/enablement/05-technical-integration.md` | Technical Integration Guide |
| 6 | `docs/enablement/06-success-metrics.md` | Partner Success Metrics |
| 7 | `docs/enablement/07-qbr-template.md` | QBR Template |

---

## Playbooks (7)

| # | Playbook | File | Templates Used |
|---|----------|------|----------------|
| 1 | recruit | `playbooks/recruit.yaml` | 5 (strategy + recruitment) |
| 2 | onboard | `playbooks/onboard.yaml` | 5 (recruitment + enablement) |
| 3 | qbr | `playbooks/qbr.yaml` | 4 (enablement + strategy) |
| 4 | expand | `playbooks/expand.yaml` | 5 (strategy + enablement) |
| 5 | exit | `playbooks/exit.yaml` | 4 (strategy + recruitment + enablement) |
| 6 | co-marketing | `playbooks/co-marketing.yaml` | 5 (enablement + recruitment) |
| 7 | support-escalation | `playbooks/support-escalation.yaml` | 5 (enablement + strategy) |

---

## Architecture Notes

- **Single source of truth:** All templates live in `docs/` and are served by MkDocs
- **Legacy `partner_blueprint/` directory removed** - it was a near-identical copy with only link path differences
- **Agent and playbooks** now reference `docs/` directly via `templates_dir: ../../docs` in config
- **Private data** goes in `.partner_data/` (gitignored)

---

*See BACKLOG.md for planned templates.*
