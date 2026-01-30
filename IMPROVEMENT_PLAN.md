# PartnerOS Improvement Plan
*Generated: January 29, 2026*

## Current State Assessment

**Strengths:**
- ✅ 25 battle-tested templates across Strategy/Recruitment/Enablement
- ✅ MkDocs site with professional styling
- ✅ AI Partner Agent with 5 playbooks (recruit, onboard, qbr, expand, exit)
- ✅ GitHub Actions CI/CD for docs deployment
- ✅ GitHub Pages live at danieloleary.github.io/PartnerOS

**Gaps:**
- ⚠️ Agent requires ANTHROPIC_API_KEY - not integrated with local AI
- ⚠️ Template inventory (markdown_inventory.csv) exists but may be outdated
- ⚠️ No automated testing for templates or agent
- ⚠️ Partner Agent design doc exists but may not match current implementation
- ⚠️ Scripts directory has 7 items - unclear what each does
- ⚠️ No local AI integration (Whisper, Sherpa TTS, Ollama) for offline work

---

## Prioritized Improvements

### HIGH PRIORITY (This Week)

#### 1. Integrate Local AI Stack into Partner Agent
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
Day 1-2: Local AI integration for partner agent
Day 3: Template inventory cleanup
Day 4-5: Automated tests setup
```

### Week 2-3
```
Week 2: Documentation improvements + 2 new playbooks
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
| Templates documented | 25 | 25 | 30 |
| Agent runs locally | ❌ | ✅ | ✅ |
| Automated tests | 0 | 10 | 25 |
| Local AI integration | ❌ | ✅ | ✅ |
| Voice commands | ❌ | ❌ | ✅ |
| Partner agent playbooks | 5 | 5 | 8 |

---

## Files to Modify/Create

```
Modified:
- scripts/partner_agent/agent.py (local AI)
- requirements.txt (ollama-python)
- markdown_inventory.csv (sync)

Created:
- docs/agent/local-setup.md
- tests/test_templates.py
- tests/test_agent.py
- .github/workflows/tests.yml
- IMPROVEMENT_PLAN.md (this file)
```

---

## Next Steps

1. ✅ **DONE** - Clone repo and assess state
2. ⬜ **NOW** - Review this plan with Dan
3. ⬜ - Prioritize and start HIGH items
4. ⬜ - Weekly check-ins on progress

---

*Questions? Contact: daniel.oleary@gmail.com*
