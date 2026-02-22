#!/usr/bin/env python3
"""
Create all PartnerOS GitHub issues.

Usage:
    export GITHUB_TOKEN=ghp_your_token_here
    python3 scripts/create_github_issues.py

    # Dry run (print issues without creating):
    python3 scripts/create_github_issues.py --dry-run
"""

import os
import sys
import json
import time
import argparse
import urllib.request
import urllib.error

REPO = "danieloleary/PartnerOS"
API_BASE = "https://api.github.com"

ISSUES = [
    # ─── SECURITY (P0) ────────────────────────────────────────────────────────
    {
        "title": "🔐 [Security] Rotate hardcoded OpenRouter API key in web.py",
        "body": """## Problem
An OpenRouter API key (`sk-or-v1-c81bce5c...`) is hardcoded in `scripts/partner_agents/web.py` on lines 34–35 and 221, and is now baked into git history.

## Risk
Anyone with read access to the repo can use this key and rack up charges.

## Fix
1. Rotate the key immediately at https://openrouter.ai
2. Remove hardcoded value — use `os.environ.get("OPENROUTER_API_KEY", "")` only
3. Add the key to `.env.example` with a placeholder
4. Add a pre-commit hook (or GitHub Actions secret scan) that blocks commits containing `sk-or-v1-` or `sk-ant-` patterns
5. Optionally purge from git history with `git filter-repo`

## Files
- `scripts/partner_agents/web.py` lines 34–35, 221
""",
        "labels": ["security", "bug", "P0"],
    },
    {
        "title": "🔐 [Security] Add input sanitization to partner_agents/ system",
        "body": """## Problem
The new `scripts/partner_agents/` system has **zero** input sanitization or path validation, unlike the original `scripts/partner_agent/agent.py` which has battle-tested `_validate_path()` and `_sanitize_partner_name()`.

In `state.py`, `partner_id` is used directly in file paths — a classic path traversal vector.

## Risk
Path traversal attacks: a malicious `partner_id` like `../../etc/passwd` could read or overwrite arbitrary files.

## Fix
1. Extract `_validate_path()` and `_sanitize_partner_name()` from `agent.py` into a shared `scripts/partner_agents/security.py` module
2. Import and apply them in `state.py`, `partner_state.py`, and all driver agents before any file I/O
3. Add tests to `test_agents.py` covering sanitization edge cases (path traversal, long strings, special chars)

## Files
- `scripts/partner_agents/state.py`
- `scripts/partner_agents/partner_state.py`
- `scripts/partner_agent/agent.py` (reference implementation)
""",
        "labels": ["security", "bug", "P0"],
    },
    {
        "title": "🔐 [Security] Remove partners.json and site/ from git tracking",
        "body": """## Problem
Two things that should be gitignored are committed to `main`:

1. `scripts/partner_agents/partners.json` — contains partner data (Acme Corp, john@acme.com)
2. `site/` — 116 MkDocs build output HTML files (~279K lines)

## Fix
1. Add to `.gitignore`:
   ```
   site/
   scripts/partner_agents/partners.json
   scripts/partner_agents/state/
   ```
2. Remove from tracking: `git rm -r --cached site/ scripts/partner_agents/partners.json`
3. Commit the removal
4. Optionally purge from history with `git filter-repo` or BFG Repo Cleaner

## Files
- `.gitignore`
- `scripts/partner_agents/partners.json`
- `site/` (entire directory)
""",
        "labels": ["security", "cleanup", "P0"],
    },

    # ─── QUALITY / BUGS (P1) ──────────────────────────────────────────────────
    {
        "title": "🐛 [Bug] Fix 100 trailing whitespace lint errors blocking CI",
        "body": """## Problem
The markdown linter (`markdown_lint.yml` workflow) will fail on 100 trailing whitespace errors across 15 files. This blocks any PR from merging.

## Worst offenders
| File | Errors |
|------|--------|
| `docs/legal/02-msa.md` | 11 |
| `docs/legal/03-dpa.md` | 10 |
| `docs/legal/04-sla.md` | 9 |
| `docs/strategy/03-evaluation-framework.md` | 8 |
| `docs/legal/01-nda.md` | 7 |
| `docs/agent/playbooks.md` | 6 |

## Fix
Single automated pass:
```bash
find docs/ -name "*.md" -exec sed -i 's/[[:space:]]*$//' {} +
```
Then verify with `npm run lint:md`.
""",
        "labels": ["bug", "quality", "P1"],
    },
    {
        "title": "🐛 [Bug] Fix 18 broken cross-reference links in templates",
        "body": """## Problem
18 `[Related Templates](path.md)` links in the docs point to nonexistent paths. All are path prefix errors.

## Categories
- **14 missing `../` prefix** — links from `finance/`, `legal/`, `security/` to sibling directories
- **3 missing index files** — `quick-start.md` links to `../legal/index.md` and `../finance/index.md` which don't exist
- **1 typo** — `first-partner-path.md` links to `../recnership/07-proposal.md` (should be `../recruitment/`)

## Examples
| File | Broken | Should be |
|------|--------|-----------|
| `finance/01-commission.md` | `operations/04-deal-registration.md` | `../operations/01-deal-registration.md` |
| `legal/01-nda.md` | `recruitment/08-agreement.md` | `../recruitment/08-agreement.md` |
| `first-partner-path.md` | `../recnership/07-proposal.md` | `../recruitment/07-proposal.md` |

## Fix
Update relative paths in the 10 affected source files. Also create `docs/legal/index.md` and `docs/finance/index.md` to resolve the missing index links.
""",
        "labels": ["bug", "docs", "P1"],
    },
    {
        "title": "🐛 [Bug] Fix agent.py reload_config() not using stored config path",
        "body": """## Problem
`reload_config()` in `scripts/partner_agent/agent.py` (line 216) doesn't store the original `config_path` passed at init time. When called, it silently reverts to the default `config.yaml` location, ignoring any custom path the user specified.

## Impact
`python agent.py --config /path/to/custom.yaml --reload` will reload the wrong file without any warning.

## Fix
1. Store `config_path` as an instance attribute in `__init__`
2. Use it in `reload_config()` instead of hardcoding the default

## Files
- `scripts/partner_agent/agent.py` around line 216
""",
        "labels": ["bug", "P1"],
    },
    {
        "title": "🐛 [Bug] Update manage_templates.py from OpenAI v0.x to v1.x API",
        "body": """## Problem
`scripts/manage_templates.py` lines 133–143 use the deprecated OpenAI v0.x API (`openai.ChatCompletion.create`). This crashes with modern `openai` package (v1.x+).

## Impact
The `enhance` subcommand is completely broken for anyone with a current OpenAI install.

## Fix
Update to v1.x syntax:
```python
# Old (broken)
response = openai.ChatCompletion.create(model=..., messages=...)

# New
from openai import OpenAI
client = OpenAI()
response = client.chat.completions.create(model=..., messages=...)
```

## Files
- `scripts/manage_templates.py` lines 133–143
""",
        "labels": ["bug", "P1"],
    },
    {
        "title": "🏗️ [Infrastructure] Wire multi-agent tests into GitHub Actions CI",
        "body": """## Problem
Four new test files exist (`test_agents.py`, `test_agents_comprehensive.py`, `test_web.py`, `test_web_comprehensive.py` — ~936 lines total) but none are included in any GitHub Actions workflow. The CI only runs the original 3 test files.

## Fix
Add a new workflow `.github/workflows/test-agents.yml` (or extend the existing test workflow) to:
1. Install `scripts/partner_agents/` dependencies
2. Run `pytest tests/test_agents.py tests/test_agents_comprehensive.py tests/test_web.py tests/test_web_comprehensive.py -v`
3. Trigger on PRs touching `scripts/partner_agents/**` or `tests/test_agents*.py` or `tests/test_web*.py`

## Files
- `.github/workflows/` (new workflow)
- `tests/test_agents.py`
- `tests/test_agents_comprehensive.py`
- `tests/test_web.py`
- `tests/test_web_comprehensive.py`
""",
        "labels": ["infrastructure", "quality", "P1"],
    },
    {
        "title": "🏗️ [Infrastructure] Merge two competing state systems in partner_agents/",
        "body": """## Problem
`scripts/partner_agents/` has two incompatible systems doing the same job:
- `state.py` — `Telemetry` class, per-partner JSON files in `state/<partner_id>/`
- `partner_state.py` — CRUD management using a single `partners.json`

This causes data inconsistency (a partner created in one system doesn't exist in the other) and doubles the maintenance burden.

## Fix
1. Pick one canonical approach — per-partner JSON files (`state.py` pattern) scales better for large partner counts
2. Migrate `partner_state.py` functionality into `state.py` or a thin wrapper
3. Delete the redundant module
4. Update all driver agents and the orchestrator to use the unified system
5. Add a migration script for any existing `partners.json` data

## Files
- `scripts/partner_agents/state.py`
- `scripts/partner_agents/partner_state.py`
- `scripts/partner_agents/drivers/*.py` (all use one or both)
""",
        "labels": ["architecture", "quality", "P1"],
    },
    {
        "title": "📝 [Docs] Add missing docs/legal/index.md and docs/finance/index.md",
        "body": """## Problem
`getting-started/quick-start.md` links to `../legal/index.md` and `../finance/index.md`, but neither file exists. These are broken links visible to all users on the quick start page.

Additionally, `legal/` and `finance/` are the only two template sections still missing index landing pages (security, operations, executive, and analysis got theirs in v1.4).

## Fix
Create both files following the same pattern as the other index pages (template-grid layout with Material icons and template cards):
- `docs/legal/index.md`
- `docs/finance/index.md`

Add both to `mkdocs.yml` nav under their respective sections.

## Files
- `docs/legal/index.md` (new)
- `docs/finance/index.md` (new)
- `mkdocs.yml`
""",
        "labels": ["docs", "P1"],
    },
    {
        "title": "🧹 [Cleanup] Remove dead code in generate_file_list.py",
        "body": """## Problem
`scripts/generate_file_list.py` references directories that don't exist in the repo: `Source Materials/` and `webapp/`. The script will silently produce incorrect output or fail.

## Fix
1. Audit what the script is supposed to do
2. Either update the directory references to match the actual repo structure, or remove the script if it's fully superseded by other tooling
3. If kept, add it to the test suite (`test_scripts_exist`) and verify it works end-to-end

## Files
- `scripts/generate_file_list.py`
""",
        "labels": ["cleanup", "P2"],
    },
    {
        "title": "🧹 [Cleanup] Fix redundant double file-read in lint_markdown.py",
        "body": """## Problem
`scripts/lint_markdown.py` lines 20–24 read each file twice — once for the main content checks and once specifically for the EOF newline check. This is a minor inefficiency but also a code smell.

## Fix
Read the file once, store the lines, and pass them to both checks. Should be a 5-line change.

## Files
- `scripts/lint_markdown.py` lines 20–24
""",
        "labels": ["cleanup", "P2"],
    },
    {
        "title": "🧹 [Cleanup] Fix typo 'recnership' in first-partner-path.md",
        "body": """## Problem
`docs/getting-started/first-partner-path.md` contains a broken link: `../recnership/07-proposal.md` — 'recnership' is a typo for 'recruitment'.

This causes a 404 when clicked in the rendered docs.

## Fix
Change `recnership` to `recruitment` in the link.

## Files
- `docs/getting-started/first-partner-path.md`
""",
        "labels": ["bug", "docs", "P1"],
    },

    # ─── UI / UX ──────────────────────────────────────────────────────────────
    {
        "title": "✨ [UI] Web UI: Add agent handoff visualization",
        "body": """## Problem / Opportunity
The orchestrator supports full agent handoffs, but the web UI shows only a flat chat stream. Users have no visibility into which agent is responding, what skills were called, or how work is flowing between agents.

## Proposed Solution
Add a live sidebar to the web UI showing:
- **Active agent** — name, avatar/icon, role description
- **Handoff timeline** — visual flow: Architect → Engine → Spark (with timestamps)
- **Skill execution log** — which skill was called and its result summary
- **Agent status** — idle / thinking / responding

## Implementation Notes
- The `TeamRadio` messaging bus in `messages.py` already emits events — tap into these for the sidebar
- Consider using Server-Sent Events (SSE) for real-time updates without websockets
- FastAPI already used in `web.py` — SSE endpoint is straightforward to add

## Files
- `scripts/partner_agents/web.py`
- `scripts/partner_agents/messages.py`
""",
        "labels": ["enhancement", "UI", "UX"],
    },
    {
        "title": "✨ [UI] Interactive template wizard in the web UI",
        "body": """## Problem / Opportunity
Templates are static Markdown with `{{placeholder}}` variables. Users currently fill them manually with no guidance. This is the biggest friction point for new users.

## Proposed Solution
Build a step-by-step template wizard in the web UI:
1. User picks a template from a dropdown (grouped by category)
2. Wizard extracts all `{{placeholder}}` fields from the template
3. For each field, show: field name, description hint, and an **AI-suggest button** that calls the active agent for a recommendation based on company/partner context
4. On completion: render a live preview, then export as filled Markdown or PDF

## Implementation Notes
- Use `fill_template.py` (already exists) as the backend fill engine
- AI suggestions can go through the existing `chat()` endpoint in `web.py`
- PDF export via `export_pdf.py` (already exists)

## Files
- `scripts/partner_agents/web.py`
- `scripts/fill_template.py`
- `scripts/export_pdf.py`
""",
        "labels": ["enhancement", "UI", "UX", "customer-experience"],
    },

    # ─── CUSTOMER EXPERIENCE ──────────────────────────────────────────────────
    {
        "title": "✨ [CX] 'First 30 Minutes' guided onboarding flow",
        "body": """## Problem / Opportunity
New users land on 40 templates, 7 agents, and 7 playbooks — completely overwhelming. There's no guided path from "I just installed this" to "I got my first useful output."

## Proposed Solution
Build a guided onboarding that runs on first launch (or at `/onboard`):
1. Ask 3 questions: company size, partner program maturity (use the maturity model), immediate goal
2. Based on answers, recommend: top 3 templates to fill first, which agent to talk to, which playbook to run
3. Walk through filling template #1 using the wizard UI (see template wizard issue)
4. Output: one completed, download-ready partner document

## Implementation Notes
- Maturity model data already exists at `docs/resources/maturity-model.md`
- The demo in `demos/onboarding.py` can serve as the logic backbone
- Store onboarding completion state so it doesn't re-run on second launch

## Files
- `scripts/partner_agents/web.py`
- `scripts/partner_agents/demos/onboarding.py`
- `docs/resources/maturity-model.md`
""",
        "labels": ["enhancement", "customer-experience", "UX"],
    },
    {
        "title": "✨ [CX] Partner health dashboard with alerts",
        "body": """## Problem / Opportunity
The Partner Health Scorecard (`docs/analysis/01-health-scorecard.md`) exists as a static Markdown template. There's no live visibility into portfolio health across all managed partners.

## Proposed Solution
Add a `/dashboard` route to the web UI showing:
- **Portfolio summary**: partner count by tier (Bronze/Silver/Gold), total pipeline value
- **Health indicators**: partners by health score band (green/yellow/red)
- **Staleness alerts**: partners with no activity in 30+ days
- **Upcoming QBRs**: next 30-day calendar of scheduled reviews (Gold: quarterly, Silver: semi-annually)
- **At-risk partners**: health score below threshold with recommended actions

## Implementation Notes
- Pull data from partner state files in `state/<slug>/metadata.json`
- Alert thresholds can be configured in `config.yaml`
- Slack/email alert hooks can be added as a follow-up

## Files
- `scripts/partner_agents/web.py`
- `scripts/partner_agents/state.py`
- `scripts/partner_agent/config.yaml`
""",
        "labels": ["enhancement", "customer-experience", "UI"],
    },

    # ─── EASE OF USE ──────────────────────────────────────────────────────────
    {
        "title": "✨ [DX] One-command bootstrap: make setup",
        "body": """## Problem / Opportunity
Getting started requires: reading docs, installing Python deps, setting env vars, configuring YAML, and knowing which script to run. Time from clone to first useful output is 15+ minutes for a new user.

## Proposed Solution
Add a `Makefile` with a `setup` target (and optionally an `npx partneros init` wrapper) that:
1. Detects OS and Python version
2. Installs all pip dependencies (`requirements.txt` + `scripts/partner_agent/requirements.txt`)
3. Copies `.env.example` → `.env` if not present
4. Prompts for: company name, product name, preferred LLM provider + API key
5. Writes `config.yaml` with the provided values
6. Runs `pytest tests/ -q` to verify installation
7. Prints next steps: "Run `python scripts/partner_agents/web.py` to open the web UI"

## Implementation Notes
- Python script is more portable than Makefile for cross-platform support
- Interactive prompts via `rich.prompt` or plain `input()`
- Extend `scripts/onboard.py` (already exists) rather than creating from scratch

## Files
- `Makefile` (new) or `scripts/onboard.py` (extend)
- `scripts/partner_agent/.env.example`
""",
        "labels": ["enhancement", "developer-experience", "ease-of-use"],
    },
    {
        "title": "✨ [DX] Unified input sanitization in shared security.py module",
        "body": """## Problem / Opportunity
Security controls are duplicated (or missing). `partner_agent/agent.py` has `_validate_path()` and `_sanitize_partner_name()`. `partner_agents/` has nothing. As the codebase grows, this divergence will worsen.

## Proposed Solution
Extract into a shared module:
```
scripts/
├── partner_agent/agent.py       (imports from shared security)
├── partner_agents/security.py   (new - canonical implementation)
└── partner_agents/state.py      (imports and uses security)
```

`security.py` should export:
- `validate_path(path, base_dir) -> bool`
- `sanitize_partner_name(name) -> str`
- `sanitize_partner_id(partner_id) -> str`

## Files
- `scripts/partner_agents/security.py` (new)
- `scripts/partner_agent/agent.py` (import from shared module)
- `scripts/partner_agents/state.py` (add sanitization)
- `scripts/partner_agents/partner_state.py` (add sanitization)
""",
        "labels": ["security", "architecture", "enhancement"],
    },

    # ─── CONTENT / BUSINESS ───────────────────────────────────────────────────
    {
        "title": "📄 [Content] Add Registered-tier self-serve templates",
        "body": """## Problem / Opportunity
The Registered tier (< $100K/year) has only **2 templates**: Deal Registration Policy and Partner Portal Guide. These are your highest-volume, lowest-touch partners — they need to self-serve effectively without a partner manager.

## Proposed Solution
Add 2–3 Registered-tier templates:
1. **Partner Welcome Kit** — what to expect, how to get started, key contacts, portal login
2. **Self-Service FAQ** — common partner questions, deal registration how-to, commission basics
3. **Partner Quick Reference Card** — one-pager: tier benefits, key links, escalation path

## Notes
- Tier: Registered / Bronze
- Skill level: beginner
- Should require zero partner manager involvement to use

## Files
- `docs/resources/` or `docs/enablement/` (new templates)
- `mkdocs.yml` (add to nav)
""",
        "labels": ["enhancement", "content", "customer-experience"],
    },
    {
        "title": "📄 [Content] Add partner co-marketing asset templates",
        "body": """## Problem / Opportunity
The co-marketing **playbook** exists (`scripts/partner_agent/playbooks/co-marketing.yaml` and `docs/enablement/04-co-marketing.md`) but there are no actual **asset templates** to fill in during a campaign.

## Proposed Solution
Add 3 co-marketing asset templates:
1. **Joint Press Release Template** — announcement of partnership with dual-company quotes
2. **Co-Branded Email Template** — campaign email with both company logos, co-authored CTA
3. **Joint Webinar Brief** — agenda, speaker bios, promotion plan, follow-up sequence

## Notes
- Category: Enablement
- Phase: enablement / growth
- Should be referenced from the co-marketing playbook steps

## Files
- `docs/enablement/` (new templates)
- `scripts/partner_agent/playbooks/co-marketing.yaml` (add template references)
- `mkdocs.yml`
""",
        "labels": ["enhancement", "content"],
    },
    {
        "title": "📄 [Content] Add renewal and retention playbook",
        "body": """## Problem / Opportunity
There's an **exit playbook** for ending partnerships but nothing focused on proactive renewal and retention. Partners at risk of churning need a structured intervention process.

## Proposed Solution
Add a `retain.yaml` playbook covering:
1. **Health check trigger** — run when health score drops below threshold (e.g., < 60)
2. **Root cause analysis** — structured discovery call to identify friction
3. **Recovery plan** — customized re-engagement based on tier and issue type
4. **Executive escalation** — template for looping in exec sponsors (Gold/Strategic only)
5. **Renewal confirmation** — formal renewal agreement and updated commitments

Also add a companion template `docs/strategy/09-retention-playbook.md`.

## Files
- `scripts/partner_agent/playbooks/retain.yaml` (new)
- `docs/strategy/09-retention-playbook.md` (new)
- `mkdocs.yml`
- `.github/workflows/run_partner_agent.yml` (add `retain` to options)
""",
        "labels": ["enhancement", "content", "customer-experience"],
    },
    {
        "title": "📄 [Content] Add ISV/technology partner track templates",
        "body": """## Problem / Opportunity
All current templates assume a **reseller or referral partner** model. Technology partners (ISVs, integration partners, marketplace partners) have fundamentally different needs: integration documentation, API partner agreements, marketplace listing requirements, and joint solution briefs.

## Proposed Solution
Add an ISV/Tech Partner sub-track:
1. **Technology Partner Agreement** — API usage rights, integration certification, data sharing terms
2. **Integration Certification Checklist** — technical requirements to achieve "Certified Integration" status
3. **Marketplace Listing Brief** — how to list on partner's app marketplace, required assets
4. **Joint Solution Brief** — customer-facing one-pager describing the combined solution

## Notes
- New section: `docs/integrations/` or add to `docs/enablement/`
- New playbook: `scripts/partner_agent/playbooks/integrate.yaml`
- Skill level: advanced (technical audience)

## Files
- `docs/enablement/` or `docs/integrations/` (new templates)
- `scripts/partner_agent/playbooks/integrate.yaml` (new)
- `mkdocs.yml`
""",
        "labels": ["enhancement", "content"],
    },
]


def create_label(token: str, name: str, color: str, description: str = ""):
    """Create a label if it doesn't exist."""
    url = f"{API_BASE}/repos/{REPO}/labels"
    data = json.dumps({"name": name, "color": color, "description": description}).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Authorization", f"token {token}")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/vnd.github.v3+json")
    try:
        urllib.request.urlopen(req)
        print(f"  Created label: {name}")
    except urllib.error.HTTPError as e:
        if e.code == 422:
            pass  # Already exists
        else:
            print(f"  Warning: could not create label '{name}': {e}")


def ensure_labels(token: str):
    """Ensure all needed labels exist."""
    labels = [
        ("security", "d73a4a", "Security vulnerability or hardening"),
        ("bug", "ee0701", "Something isn't working"),
        ("P0", "b60205", "Critical — fix immediately"),
        ("P1", "e4e669", "High priority"),
        ("P2", "0075ca", "Medium priority"),
        ("enhancement", "84b6eb", "New feature or improvement"),
        ("docs", "0075ca", "Documentation"),
        ("cleanup", "e4e669", "Code cleanup / tech debt"),
        ("architecture", "5319e7", "Architectural change"),
        ("infrastructure", "1d76db", "CI/CD or infrastructure"),
        ("quality", "0e8a16", "Code quality"),
        ("UI", "fbca04", "User interface"),
        ("UX", "f9d0c4", "User experience"),
        ("customer-experience", "c2e0c6", "Customer/partner experience"),
        ("developer-experience", "bfd4f2", "Developer experience"),
        ("ease-of-use", "d4c5f9", "Ease of use improvement"),
        ("content", "c5def5", "Documentation content / templates"),
    ]
    print("Ensuring labels exist...")
    for name, color, description in labels:
        create_label(token, name, color, description)


def create_issue(token: str, issue: dict, dry_run: bool = False) -> int | None:
    """Create a single GitHub issue. Returns the issue number."""
    if dry_run:
        print(f"\n[DRY RUN] Would create: {issue['title']}")
        print(f"  Labels: {', '.join(issue.get('labels', []))}")
        return None

    url = f"{API_BASE}/repos/{REPO}/issues"
    data = json.dumps({
        "title": issue["title"],
        "body": issue["body"],
        "labels": issue.get("labels", []),
    }).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Authorization", f"token {token}")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/vnd.github.v3+json")

    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
            number = result["number"]
            print(f"  ✓ Created #{number}: {issue['title']}")
            return number
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"  ✗ Failed to create '{issue['title']}': {e.code} {body[:200]}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Create PartnerOS GitHub issues")
    parser.add_argument("--dry-run", action="store_true", help="Print issues without creating them")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN", "")

    if not args.dry_run and not token:
        print("Error: GITHUB_TOKEN environment variable not set.")
        print("Usage: export GITHUB_TOKEN=ghp_... && python3 scripts/create_github_issues.py")
        sys.exit(1)

    if args.dry_run:
        print(f"\n{'='*60}")
        print(f"DRY RUN — {len(ISSUES)} issues would be created in {REPO}")
        print(f"{'='*60}")
        for issue in ISSUES:
            create_issue(token, issue, dry_run=True)
        print(f"\nTotal: {len(ISSUES)} issues")
        return

    print(f"\nCreating {len(ISSUES)} issues in {REPO}...\n")
    ensure_labels(token)

    created = []
    failed = []

    for i, issue in enumerate(ISSUES):
        print(f"[{i+1}/{len(ISSUES)}]", end=" ")
        number = create_issue(token, issue)
        if number:
            created.append(number)
        else:
            failed.append(issue["title"])

        if i < len(ISSUES) - 1:
            time.sleep(0.5)  # Respect rate limits

    print(f"\n{'='*60}")
    print(f"Done! Created {len(created)} issues, {len(failed)} failed.")
    if created:
        print(f"Issues: {', '.join(f'#{n}' for n in created)}")
    if failed:
        print(f"Failed:\n" + "\n".join(f"  - {t}" for t in failed))
    print(f"\nView at: https://github.com/{REPO}/issues")


if __name__ == "__main__":
    main()
