# PartnerOS CHANGELOG

## Version 1.3 (2026-02-21) - Audit & Documentation Refresh

### Full Codebase Audit
- **TEST AUDIT**: Analyzed all 43 tests across 3 test files, identified coverage gaps (nav completeness, index page coverage, cross-reference integrity, MkDocs build validation)
- **UI/UX AUDIT**: Analyzed MkDocs config (16 theme features, 22 markdown extensions, 3 plugins), custom CSS (257 lines), navigation structure, frontmatter consistency, responsive design, dark mode

### Audit Findings
- **4 missing section index pages**: `docs/security/`, `docs/operations/`, `docs/executive/`, `docs/analysis/` lack `index.md` landing pages
- **3 orphaned files**: `first-partner-path.md`, `licensing.md`, `partner-os-one-pager.md` not referenced in `mkdocs.yml` nav
- **Test gaps identified**: No nav completeness test, no index coverage test, no cross-reference test, no MkDocs build test
- **Frontmatter**: 98% consistent; `glossary.md` and `maturity-model.md` may have slight variations

### Documentation Updated
- **IMPROVEMENT_PLAN.md**: Complete rewrite with audit findings, phased roadmap (Phases 5-8)
- **BACKLOG.md**: Marked all completed items, added Phases 5-8, accurate completed items log
- **CLAUDE.md**: Updated file tree (added 6 missing doc dirs, 5 missing scripts, examples/), updated template count (38+ → 40), agent line count (775 → 985), test count (20 → 43), added 6 new template category tables, expanded frontmatter schema to 17 fields
- **README.md**: Fixed template count (34 → 40), fixed typo (extra space), updated project structure (added all new dirs/scripts), updated testing section (pytest), added v1.2/v1.3 to recent updates
- **ARCHITECTURE.md**: Updated test count (20 → 43), template count, directory tree (added all new categories), marked planned agent features as completed
- **CHANGELOG.md**: Added v1.3 entry

### No Code Changes
This version is documentation-only. All 43 tests continue to pass.

---

## Version 1.2 (2026-02-19) - Template Schema & Backlog

### Template Schema Standardization
- **NEW**: Standardized frontmatter schema for all 38 templates
  - Added `tier`: [Bronze, Silver, Gold]
  - Added `skill_level`: beginner/intermediate/advanced
  - Added `purpose`: tactical/strategic/operational
  - Added `phase`: recruitment/onboarding/enablement/growth/retention/exit
  - Added `time_required`: estimated completion time
  - Added `difficulty`: easy/medium/hard
  - Added `outcomes`: expected results
  - Added `skills_gained`: competencies developed
  - Added `category`, `version`, `author`, `prerequisites`

### New Scripts
- **NEW**: `scripts/standardize_templates.py` - Bulk frontmatter standardization

### Documentation
- **NEW**: `BACKLOG.md` - Comprehensive feature backlog for partner leaders
- **UPDATED**: `IMPROVEMENT_PLAN.md` - Updated roadmap with missing templates

### Cleanup
- **REMOVED**: Redundant `partner_blueprint/` (identical to docs/)
- **FIXED**: All tests passing (11/11)

---

## Version 1.1 (2026-02-02)

### Issues Fixed

#### Critical
- **Incomplete `_continue_playbook_interactive`**: Method now properly resumes playbooks from saved state
- **Hardcoded model name**: Changed `claude-sonnet-4-20250514` to `sonnet-4-20250514` (real model)
- **Hardcoded paths**: test_templates.py now uses `REPO_ROOT / 'docs'`

#### High Priority
- **Input sanitization**: Added validation for partner names (max length, no traversal)
- **Path traversal protection**: Template loading now validates paths don't escape directory
- **API retry logic**: Added exponential backoff retry (3 attempts)

#### Medium Priority
- **Structured logging**: Added logging module with configurable verbosity
- **Config reload**: Added `reload_config()` method with `--reload` flag
- **Console output**: Standardized all output through `_print()` wrapper
- **Test patterns**: Converted to proper pytest functions

#### Low Priority
- **OpenAI client**: Fixed import syntax or removed unused code
- **Type hints**: Added missing type hints for consistency

### Tests Added
- `test_partner_resume.py`: Verify resume functionality works
- `test_security.py`: Verify path traversal blocked, input sanitized
- `test_retry_logic`: Verify API retries on failure

### Files Changed
- `scripts/partner_agent/agent.py` (8+ issues fixed)
- `scripts/partner_agent/.env.example` (model name fixed)
- `tests/test_templates.py` (hardcoded path fixed)
- `tests/test_partner_resume.py` (new)
- `tests/test_security.py` (new)
- `CHANGELOG.md` (updated)

### Breaking Changes
None. All changes are backward compatible.

---

## Version 1.0 (2026-01-XX)

Initial release with 8 playbooks and Partner Agent.

- Playbooks: recruit, onboard, qbr, expand, exit, co-marketing, support-escalation
- Templates: 39 templates across strategy, recruitment, enablement
- LLM support: Ollama (local), Anthropic, OpenAI
- Enterprise framework: Bronze/Silver/Gold tier model
