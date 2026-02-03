# PartnerOS v1.1 - CHANGELOG

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
