# PartnerOS Backlog - Prioritized Roadmap

*Generated: February 19, 2026*
*Updated: February 21, 2026*
*Based on: ARCHITECTURE.md + Full Audit (Feb 21)*

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
| 1.1 | **Company Config Script** | `python scripts/onboard.py` - prompts for company info, generates config | 2 hrs | DONE |
| 1.2 | **Template Variable System** | Replace `{{company_name}}` etc with their company | 2 hrs | DONE |
| 1.3 | **Quick Start Guide** | "From zero to first partner in 30 minutes" | 3 hrs | DONE |
| 1.4 | **Example Fills** | 3-5 completed templates showing format | 4 hrs | DONE |

---

## Phase 2: Sales Ready 📦

*Goal: Something to show prospects, easy to demo*

| # | Item | Purpose | Effort | Status |
|---|------|---------|--------|--------|
| 2.1 | **Demo Mode** | Pre-filled fake company data for demos | 2 hrs | DONE |
| 2.2 | **One-Pager** | Product sheet to give prospects | 1 hr | DONE |
| 2.3 | **Pricing Sheet** | How to license/subscribe | 1 hr | DONE |
| 2.4 | **Testimonials/Case Study Template** | Social proof | 2 hrs | PENDING |

---

## Phase 3: Onboarding Flow 🎯

*Goal: Clear "first partner" path that actually works*

| # | Item | Purpose | Effort | Status |
|---|------|---------|--------|--------|
| 3.1 | **First Partner Onboarding Path** | Documented sequence: which templates in what order | 3 hrs | DONE |
| 3.2 | **Test Partner Design** | "TechStart Inc" - realistic test case for validation | 2 hrs | DONE |
| 3.3 | **Onboarding Test Cases** | Automated tests simulating partner lifecycle | 4 hrs | DONE |
| 3.4 | **End-to-End Validation** | Run full onboarding flow, fix gaps | 3 hrs | DONE |

---

## Phase 4: Agent Superpowers 🤖

*Goal: The agent becomes a real "coach"*

| # | Item | Purpose | Effort | Status |
|---|------|---------|--------|--------|
| 4.1 | **Partner Memory** | tier, health_score, notes, milestones persisted per partner | 4 hrs | DONE |
| 4.2 | **Template Recommendations** | `recommend_templates()` suggests next playbooks by stage + tier | 3 hrs | DONE |
| 4.3 | **Tier Guidance** | Tier config (Gold/Silver/Registered) wired into every LLM system prompt | 2 hrs | DONE |
| 4.4 | **Email Generation** | `generate_email()` + interactive menu option 6 | 2 hrs | DONE |
| 4.5 | **Report Generation** | `scripts/generate_report.py` — markdown report for all or one partner | 3 hrs | DONE |

---

## Phase 4b: Template Completion 📋

*Goal: Complete the template library*

| # | Item | Category | Purpose | Effort | Status |
|---|------|----------|---------|--------|--------|
| 4b.1 | Revenue Sharing Model | Finance | Joint venture partnerships | 2 hrs | DONE |
| 4b.2 | Partner Rebate Program | Finance | Volume-based incentives | 2 hrs | DONE |
| 4b.3 | SOC2 Compliance Guide | Security | Compliance requirements | 2 hrs | DONE |
| 4b.4 | Deal Registration Policy | Operations | Rules and eligibility | 2 hrs | DONE |
| 4b.5 | Weekly Partner Standup | Operations | Weekly team sync | 1 hr | DONE |
| 4b.6 | Monthly Partner Report | Operations | Roll-up metrics | 2 hrs | DONE |
| 4b.7 | Partner Portal Guide | Operations | PRM system guide | 2 hrs | DONE |
| 4b.8 | Board Deck - Partner Program | Executive | Quarterly board update | 3 hrs | DONE |
| 4b.9 | Partner Health Scorecard | Analysis | Quarterly assessment | 2 hrs | DONE |

---

## Phase 5: Documentation Refresh 📝

*Goal: All meta-documentation accurately reflects the codebase*

| # | Item | Purpose | Effort | Status |
|---|------|---------|--------|--------|
| 5.1 | **Full Audit** | Test suite + UI/UX site audit | 2 hrs | DONE |
| 5.2 | **Update IMPROVEMENT_PLAN.md** | Comprehensive findings and roadmap | 1 hr | DONE |
| 5.3 | **Update BACKLOG.md** | Mark completed items, add new findings | 30 min | DONE |
| 5.4 | **Update CLAUDE.md** | Accurate file tree, counts, test list | 1 hr | DONE |
| 5.5 | **Update README.md** | Fix counts, structure, typo | 30 min | DONE |
| 5.6 | **Update CHANGELOG.md** | Add v1.3 entry | 15 min | DONE |
| 5.7 | **Update ARCHITECTURE.md** | Current state, completed features | 30 min | DONE |

---

## Phase 6: Navigation & Index Pages 🧭

*Goal: Every section has a landing page, no orphaned files*

| # | Item | Purpose | Effort | Status |
|---|------|---------|--------|--------|
| 6.1 | **Create `docs/security/index.md`** | Security section landing page with template grid | 30 min | PENDING |
| 6.2 | **Create `docs/operations/index.md`** | Operations section landing page with template grid | 30 min | PENDING |
| 6.3 | **Create `docs/executive/index.md`** | Executive section landing page | 20 min | PENDING |
| 6.4 | **Create `docs/analysis/index.md`** | Analysis section landing page | 20 min | PENDING |
| 6.5 | **Add orphaned files to nav** | Add `first-partner-path.md`, `licensing.md`, `partner-os-one-pager.md` to `mkdocs.yml` | 15 min | PENDING |
| 6.6 | **Add nav completeness test** | Verify all docs/ files appear in mkdocs.yml nav | 30 min | PENDING |
| 6.7 | **Add index coverage test** | Verify each template dir has index.md | 20 min | PENDING |

---

## Phase 7: Test Expansion 🧪

*Goal: Comprehensive test coverage for site integrity*

| # | Item | Purpose | Effort | Status |
|---|------|---------|--------|--------|
| 7.1 | **Nav completeness test** | Verify all .md files in docs/ are referenced in mkdocs.yml | 30 min | PENDING |
| 7.2 | **Cross-reference test** | Verify internal markdown links between templates resolve | 1 hr | PENDING |
| 7.3 | **MkDocs build test** | Run `mkdocs build --strict` in CI to catch broken pages | 30 min | PENDING |
| 7.4 | **Playbook dry-run test** | Validate playbook step execution without LLM calls | 1 hr | PENDING |

---

## Phase 8: Polish & Package 🎁

*Goal: Professional product ready for distribution*

| # | Item | Purpose | Effort | Status |
|---|------|---------|--------|--------|
| 8.1 | **Testimonial/Case Study template** | Social proof for prospects | 2 hrs | PENDING |
| 8.2 | **Mermaid diagrams in key templates** | Visual richness in strategy, recruitment, enablement | 2 hrs | PENDING |
| 8.3 | **PDF Export Script polish** | Clean PDF output for offline use | 2 hrs | PENDING |
| 8.4 | **Package as .zip polish** | Clean distribution package | 1 hr | PENDING |
| 8.5 | **Video Walkthroughs** | For key templates | 8 hrs | PENDING |

---

## Completed Items

| Item | Date |
|------|------|
| Documentation refresh (CLAUDE.md, README, BACKLOG, CHANGELOG, ARCHITECTURE, IMPROVEMENT_PLAN) | Feb 21, 2026 |
| Full test suite + UI/UX audit | Feb 21, 2026 |
| Partner Memory (tier, health, notes, milestones) | Feb 20, 2026 |
| Tier Guidance in LLM prompts | Feb 20, 2026 |
| Template Recommendations engine | Feb 20, 2026 |
| Email Generation (generate_email + menu) | Feb 20, 2026 |
| Report Generation (scripts/generate_report.py) | Feb 20, 2026 |
| Agent tests expanded (43 total) | Feb 20, 2026 |
| Legal Templates (NDA, MSA, DPA, SLA) | Feb 20, 2026 |
| Finance Templates (Commission, Rebate, Revenue Share) | Feb 20, 2026 |
| Security Templates (Questionnaire, SOC2) | Feb 20, 2026 |
| Operations Templates (Deal Reg, Standup, Report, Portal) | Feb 20, 2026 |
| Executive Template (Board Deck) | Feb 20, 2026 |
| Analysis Template (Health Scorecard) | Feb 20, 2026 |
| Template Generator Script | Feb 20, 2026 |
| Standardize Script | Feb 20, 2026 |
| MkDocs Navigation (9 sections) | Feb 20, 2026 |
| Template Schema Standardization (17-field frontmatter) | Feb 19, 2026 |
| Demo Mode | Feb 19, 2026 |
| One-Pager & Licensing | Feb 19, 2026 |
| Company Onboarding (onboard.py) | Feb 19, 2026 |
| Template Variables (fill_template.py) | Feb 19, 2026 |
| Quick Start Guide | Feb 19, 2026 |
| Example Fills | Feb 19, 2026 |
| Agent v1.1 fixes (security, retry, logging) | Feb 2, 2026 |
| Initial release (7 playbooks, 25 templates, agent) | Jan 2026 |

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

### Onboarding

```bash
python scripts/onboard.py
```

---

*Backlog managed per ARCHITECTURE.md vision - "Give them the playbook + the coach"*
