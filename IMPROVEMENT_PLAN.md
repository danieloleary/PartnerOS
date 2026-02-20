# PartnerOS Improvement Plan
*Generated: January 29, 2026*
*Updated: February 19, 2026*

> **See [BACKLOG.md](BACKLOG.md) for comprehensive feature list and long-term roadmap**

## Current State Assessment

**Strengths:**
- ✅ 38 battle-tested templates across Strategy/Recruitment/Enablement/Resources/Agent
- ✅ Standardized frontmatter schema (tier, skill_level, purpose, phase, time_required, difficulty, outcomes, skills_gained)
- ✅ MkDocs site with professional styling
- ✅ AI Partner Agent with 7 playbooks (recruit, onboard, qbr, expand, exit, co-marketing, support-escalation)
- ✅ GitHub Actions CI/CD for docs deployment
- ✅ GitHub Pages live at danieloleary.github.io/PartnerOS
- ✅ Automated template schema standardization script

**Gaps:**
- ⚠️ Missing Legal templates (NDA, MSA, DPA, SLA)
- ⚠️ Missing Finance templates (commission, revenue share, rebates)
- ⚠️ Missing Security templates (security questionnaire, compliance)
- ⚠️ No local AI integration (Whisper, Sherpa TTS, Ollama) for offline work

---

## Prioritized Improvements

### HIGH PRIORITY (This Week)

#### 1. Add Missing Template Categories
**Goal:** Complete template coverage for enterprise partner programs

**Actions:**
- [ ] Create `docs/legal/` directory
- [ ] Add NDA Template (`01-nda.md`)
- [ ] Add Master Service Agreement (`02-msa.md`)
- [ ] Add Data Processing Agreement (`03-dpa.md`)
- [ ] Add Service Level Agreement (`04-sla.md`)
- [ ] Create `docs/finance/` directory
- [ ] Add Commission Structure Template (`01-commission.md`)
- [ ] Add Revenue Sharing Model (`02-revenue-share.md`)
- [ ] Add Partner Rebate Program (`03-rebate.md`)
- [ ] Create `docs/security/` directory
- [ ] Add Security Questionnaire (`01-security-questionnaire.md`)
- [ ] Add SOC2 Compliance Guide (`02-soc2-compliance.md`)
- [ ] Apply standard frontmatter to all new templates

**Estimated Effort:** 4-6 hours

**Impact:** Complete template coverage for enterprise needs

#### 2. Integrate Local AI Stack into Partner Agent
**Goal:** Remove Anthropic API dependency, run partner agent locally

**Actions:**
- [ ] Modify `scripts/partner_agent/agent.py` to use Ollama instead of Anthropic API
- [ ] Update requirements.txt to include ollama-python or use subprocess
- [ ] Create `.env.example` with OLLAMA_ENDPOINT configuration
- [ ] Document local AI setup in `docs/agent/local-setup.md`
- [ ] Test agent with llama3.2:3b model

**Estimated Effort:** 2-4 hours

**Impact:** Free, private, offline partner agent

#### 2. Update Template Inventory
**Goal:** Ensure markdown_inventory.csv reflects current templates

**Actions:**
- [ ] Run `find docs/ -name "*.md" | wc -l` to count actual templates
- [ ] Compare with inventory.csv
- [ ] Update inventory.csv or clean up orphaned templates
- [ ] Add inventory generation script to `scripts/`

**Estimated Effort:** 1-2 hours

**Impact:** Accurate template tracking, easier maintenance

#### 3. Add Automated Tests
**Goal:** Prevent regressions in templates and agent

**Actions:**
- [ ] Create `tests/` directory
- [ ] Add template validation (frontmatter completeness)
- [ ] Add agent playbook tests (mock execution)
- [ ] Add GitHub Actions workflow for tests
- [ ] Badge in README showing test status

**Estimated Effort:** 3-5 hours

**Impact:** Confidence when making changes

---

### MEDIUM PRIORITY (This Month)

#### 4. Improve Documentation
- [ ] Add screenshots to key templates
- [ ] Create "Getting Started" video walkthrough
- [ ] Add troubleshooting section to agent docs
- [ ] Document common partnership scenarios

#### 5. Expand Partner Agent Playbooks
- [ ] Add "co-marketing" playbook
- [ ] Add "technical integration" playbook
- [ ] Add "partner success" playbook
- [ ] Create playbook template for custom playbooks

#### 6. Local TTS/STT for Partner Agent
- [ ] Add voice commands to agent
- [ ] Add voice summaries for playbook outputs
- [ ] Integrate Whisper for voice input
- [ ] Integrate Sherpa TTS for voice output

---

### LOW PRIORITY (This Quarter)

#### 7. Community & Distribution
- [ ] Create template marketplace
- [ ] Add contribution guidelines with templates
- [ ] Create GitHub template for new partners
- [ ] Add Docker container for agent

#### 8. Integration Improvements
- [ ] Add Slack bot integration
- [ ] Add CRM webhook support (Salesforce, HubSpot)
- [ ] Add calendar integration (Google Calendar)
- [ ] Add video conferencing integration (Zoom)

---

## Implementation Roadmap

### Week 1 (This Week)
```
Day 1:   Add missing template categories (Legal, Finance, Security)
Day 2-3: Create 11 new templates with standardized frontmatter
Day 4:   Template inventory cleanup
Day 5:   Update IMPROVEMENT_PLAN.md
```

### Week 2-3
```
Week 2: Local AI integration improvements + 2 new playbooks
Week 3: Voice integration (Whisper + Sherpa TTS)
```

### Week 4+
```
Community features + CRM integrations
```

---

## Success Metrics

| Metric | Current | Target (30 days) | Target (90 days) |
|--------|---------|------------------|------------------|
| Templates documented | 38 | 48 | 55 |
| Template schema standardized | ✅ | N/A | N/A |
| Legal templates | 0 | 4 | 4 |
| Finance templates | 0 | 3 | 3 |
| Security templates | 0 | 2 | 2 |
| Agent runs locally | ✅ | N/A | N/A |
| Automated tests | 2 | 10 | 25 |
| Local AI integration | ✅ | N/A | N/A |
| Partner agent playbooks | 7 | 7 | 10 |

---

## Files to Modify/Create

```
Modified:
- IMPROVEMENT_PLAN.md (updated with new tasks)
- docs/*/*.md (standardized frontmatter schema applied)
- scripts/standardize_templates.py (new - schema standardizer)

Created:
- docs/legal/01-nda.md
- docs/legal/02-msa.md
- docs/legal/03-dpa.md
- docs/legal/04-sla.md
- docs/finance/01-commission.md
- docs/finance/02-revenue-share.md
- docs/finance/03-rebate.md
- docs/security/01-security-questionnaire.md
- docs/security/02-soc2-compliance.md
```

---

## Next Steps

1. ✅ **DONE** - Clone repo and assess state
2. ⬜ **NOW** - Review this plan with Dan
3. ⬜ - Prioritize and start HIGH items
4. ⬜ - Weekly check-ins on progress

---

*Questions? Contact: daniel.oleary@gmail.com*
