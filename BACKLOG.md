# PartnerOS Backlog - Prioritized Roadmap
*Generated: February 19, 2026*
*Updated: February 20, 2026*
*Based on: ARCHITECTURE.md*

---

## Vision
**"Give them the playbook + the coach"**
- Templates = The playbook (what to do)
- Agent = The coach (guides them through it)
- You = The advisor (help customize and implement)

**Target:** Companies that can drop in PartnerOS and immediately have a world-class partner program.

---

## Phase 1: Foundation (Drop-Ready) ⚡

*Goal: A company can download and get started in 30 minutes*

| # | Item | Purpose | Effort | Status |
|---|------|---------|--------|--------|
| 1.1 | **Company Config Script** | `python scripts/onboard.py` - prompts for company info, generates config | 2 hrs | ✅ DONE |
| 1.2 | **Template Variable System** | Replace `{{company_name}}` etc with their company | 2 hrs | ✅ DONE |
| 1.3 | **Quick Start Guide** | "From zero to first partner in 30 minutes" | 3 hrs | ✅ DONE |
| 1.4 | **Example Fills** | 3-5 completed templates showing format | 4 hrs | ✅ DONE |

---

## Phase 2: Sales Ready 📦

*Goal: Something to show prospects, easy to demo*

| # | Item | Purpose | Effort | Status |
|---|------|---------|--------|--------|
| 2.1 | **Demo Mode** | Pre-filled fake company data for demos | 2 hrs | ✅ DONE |
| 2.2 | **One-Pager** | Product sheet to give prospects | 1 hr | ✅ DONE |
| 2.3 | **Pricing Sheet** | How to license/subscribe | 1 hr | ✅ DONE |
| 2.4 | **Testimonials/Case Study Template** | Social proof | 2 hrs | PENDING |

---

## Phase 3: Onboarding Flow 🎯

*Goal: Clear "first partner" path that actually works*

| # | Item | Purpose | Effort | Status |
|---|------|---------|--------|--------|
| 3.1 | **First Partner Onboarding Path** | Documented sequence: which templates in what order | 3 hrs | PENDING |
| 3.2 | **Test Partner Design** | "TechStart Inc" - realistic test case for validation | 2 hrs | PENDING |
| 3.3 | **Onboarding Test Cases** | Automated tests simulating partner lifecycle | 4 hrs | PENDING |
| 3.4 | **End-to-End Validation** | Run full onboarding flow, fix gaps | 3 hrs | PENDING |

---

## Phase 4: Agent Superpowers 🤖

*Goal: The agent becomes a real "coach"*

| # | Item | Purpose | Effort | Status |
|---|------|---------|--------|--------|
| 4.1 | **Partner Memory** | tier, health_score, notes, milestones persisted per partner | 4 hrs | ✅ DONE |
| 4.2 | **Template Recommendations** | `recommend_templates()` suggests next playbooks by stage + tier | 3 hrs | ✅ DONE |
| 4.3 | **Tier Guidance** | Tier config (Gold/Silver/Registered) wired into every LLM system prompt | 2 hrs | ✅ DONE |
| 4.4 | **Email Generation** | `generate_email()` + interactive menu option 6 | 2 hrs | ✅ DONE |
| 4.5 | **Report Generation** | `scripts/generate_report.py` — markdown report for all or one partner | 3 hrs | ✅ DONE |

---

## Phase 4: Template Completion 📋

*Goal: Complete the template library*

| # | Item | Category | Purpose | Effort | Status |
|---|------|----------|---------|--------|--------|
| 4.1 | Revenue Sharing Model | Finance | Joint venture partnerships | 2 hrs | PENDING |
| 4.2 | Partner Rebate Program | Finance | Volume-based incentives | 2 hrs | PENDING |
| 4.3 | SOC2 Compliance Guide | Security | Compliance requirements | 2 hrs | PENDING |
| 4.4 | Deal Registration Policy | Operations | Rules and eligibility | 2 hrs | PENDING |
| 4.5 | Weekly Partner Standup | Operations | Weekly team sync | 1 hr | PENDING |
| 4.6 | Monthly Partner Report | Operations | Roll-up metrics | 2 hrs | PENDING |
| 4.7 | Partner Portal Guide | Operations | PRM system guide | 2 hrs | PENDING |
| 4.8 | Board Deck - Partner Program | Executive | Quarterly board update | 3 hrs | PENDING |
| 4.9 | Partner Health Scorecard | Analysis | Quarterly assessment | 2 hrs | PENDING |

---

## Phase 5: Polish & Package 🎁

*Goal: Professional product ready for distribution*

| # | Item | Purpose | Effort | Status |
|---|------|---------|--------|--------|
| 5.1 | **PDF Export Script** | Convert markdown to PDF | 3 hrs | PENDING |
| 5.2 | **Package as .zip** | No git required to use | 1 hr | PENDING |
| 5.3 | **Video Walkthroughs** | For key templates | 8 hrs | PENDING |

---

## Completed Items ✅

| Item | Date |
|------|------|
| Partner Memory (tier, health, notes, milestones) | Feb 20, 2026 |
| Tier Guidance in LLM prompts | Feb 20, 2026 |
| Template Recommendations engine | Feb 20, 2026 |
| Email Generation (generate_email + menu) | Feb 20, 2026 |
| Report Generation (scripts/generate_report.py) | Feb 20, 2026 |
| Agent tests expanded to 40 (9 new superpower tests) | Feb 20, 2026 |
| Tests (31 tests) | Feb 20, 2026 |
| Legal Templates (NDA, MSA, DPA, SLA) | Feb 20, 2026 |
| Commission Structure | Feb 20, 2026 |
| Security Questionnaire | Feb 20, 2026 |
| Template Generator Script | Feb 20, 2026 |
| Standardize Script | Feb 20, 2026 |
| MkDocs Navigation | Feb 20, 2026 |
| Pre-commit Hooks | Feb 20, 2026 |

---

## Quick Reference

### Running Tests
```bash
pytest tests/ -v
```

### Generating Template
```bash
python scripts/generate_template.py --category legal --name my-template
```

### Onboarding (Future)
```bash
python scripts/onboard.py
```

---

*Backlog managed per ARCHITECTURE.md vision - "Give them the playbook + the coach"*
