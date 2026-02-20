# CLAUDE.md — PartnerOS Codebase Guide

This file provides guidance for AI assistants working in this repository.

## Project Overview

**PartnerOS** is a complete playbook system for building and scaling strategic partnerships, combining:

- 38+ Markdown documentation templates (rendered via MkDocs Material)
- An AI-powered Partner Agent (`scripts/partner_agent/agent.py`) supporting local Ollama, Anthropic, and OpenAI
- 7 automation playbooks covering the full partner lifecycle
- GitHub Actions for doc deployment and markdown linting

**Live site:** https://danieloleary.github.io/PartnerOS

---

## Repository Structure

```
PartnerOS/
├── docs/                          # MkDocs documentation source (rendered site)
│   ├── strategy/                  # 9 strategy templates
│   ├── recruitment/               # 10 recruitment templates
│   ├── enablement/                # 8 enablement templates
│   ├── agent/                     # Partner Agent docs
│   ├── getting-started/           # Quick start, lifecycle, how-to-use
│   ├── resources/                 # Glossary, maturity model
│   └── stylesheets/extra.css      # Custom CSS overrides
├── scripts/
│   ├── partner_agent/             # AI Partner Agent
│   │   ├── agent.py               # Main agent (1 file, ~775 lines)
│   │   ├── config.yaml            # Agent configuration
│   │   ├── .env.example           # Environment variable template
│   │   ├── requirements.txt       # Python dependencies
│   │   ├── playbooks/             # 7 YAML playbook definitions
│   │   │   ├── recruit.yaml
│   │   │   ├── onboard.yaml
│   │   │   ├── qbr.yaml
│   │   │   ├── expand.yaml
│   │   │   ├── exit.yaml
│   │   │   ├── co-marketing.yaml
│   │   │   └── support-escalation.yaml
│   │   ├── partner_agent/         # Python package wrapper
│   │   │   └── __init__.py        # Re-exports PartnerAgent from agent.py
│   │   └── state/                 # Partner session state (gitignored)
│   ├── lint_markdown.py           # Custom markdown linter
│   ├── generate_file_list.py      # Template inventory generator
│   ├── manage_templates.py        # Template management utilities
│   └── update_keywords.py         # YAML frontmatter keyword updater
├── tests/
│   ├── test_templates.py          # Template structure/frontmatter tests
│   ├── test_agent.py              # Agent unit tests (sanitization, path validation)
│   └── requirements.txt           # Test dependencies (pytest, pyyaml)
├── site/                          # Built MkDocs output (gitignored in practice)
├── .github/workflows/
│   ├── deploy-docs.yml            # Deploys docs to GitHub Pages on push to main
│   ├── markdown_lint.yml          # Runs markdown linter on all *.md changes
│   └── run_partner_agent.yml      # Manual workflow to run a playbook via Actions
├── mkdocs.yml                     # MkDocs site configuration
├── requirements.txt               # Python deps for MkDocs (mkdocs-material, etc.)
├── package.json                   # Node.js: npm run lint:md → python lint script
├── CHANGELOG.md                   # Version history
├── README.md                      # Project overview
├── Example_Partner_Plan.md        # Sample partner plan document
└── PartnerOS_Assistant_Agent_Design.md  # Agent architecture design doc
```

---

## Development Commands

### Documentation (MkDocs)

```bash
# Install docs dependencies
pip install mkdocs-material mkdocs-minify-plugin pillow cairosvg

# Preview locally (hot reload at http://localhost:8000)
mkdocs serve

# Build static site to site/
mkdocs build
```

### Partner Agent

```bash
cd scripts/partner_agent

# Install agent dependencies
pip install -r requirements.txt

# Run interactively (default: interactive mode)
python agent.py

# Run specific playbook for a partner
python agent.py --playbook recruit --partner "Acme Corp"

# Resume saved session
python agent.py --resume acme-corp

# Show all partner statuses
python agent.py --status

# Reload config without restart
python agent.py --reload

# Enable debug logging
python agent.py --verbose
```

### Environment Setup (Agent)

```bash
# Local Ollama (free, offline, recommended)
export OLLAMA_ENDPOINT=http://localhost:11434
export OLLAMA_MODEL=llama3.2:3b
export PROVIDER=ollama

# Anthropic (cloud)
export ANTHROPIC_API_KEY=sk-ant-...
export PROVIDER=anthropic

# OpenAI (cloud)
export OPENAI_API_KEY=sk-...
export PROVIDER=openai
```

### Testing

```bash
# Run template tests
python3 tests/test_templates.py

# Run agent tests
python3 tests/test_agent.py

# Or with pytest (from repo root)
pytest tests/
```

### Markdown Linting

```bash
# Via npm (calls Python linter)
npm run lint:md

# Or directly
python3 scripts/lint_markdown.py
```

---

## Key Conventions

### Markdown Templates (docs/)

Every `.md` file in `docs/` **must** start with YAML frontmatter:

```yaml
---
title: Template Title
section: Strategy          # or Recruitment, Enablement, etc.
template_number: I.1       # Roman numeral section + number
last_updated: 2024-06-10
description: >
  Brief description of this template's purpose.
tags: [strategy, business-case]
---
```

The `test_templates_have_frontmatter` test enforces this — any file missing `---` at the start will fail CI.

### Playbook YAML Format

Playbooks in `scripts/partner_agent/playbooks/` follow this schema:

```yaml
name: Human-readable playbook name
description: What this playbook accomplishes
tags: [tag1, tag2]

steps:
  - name: Step Name
    template: docs/recruitment/01-foo.md  # relative to repo root
    prompt: |
      Instruction to the AI for this step.
    # KPIs, checklist, and automation hints as comments

success_criteria:
  - Measurable outcome 1
  - Measurable outcome 2

next_playbook: onboard   # optional — which playbook to run next
```

Template paths in playbooks are relative to the repo root (e.g., `docs/recruitment/01-foo.md`).

### Partner State Storage

Partner state is saved to `scripts/partner_agent/state/<slug>/metadata.json` (gitignored). The slug is derived from `_sanitize_partner_name()` → `slugify()`:

- Alphanumeric, dashes, underscores only
- Max 100 characters
- No path traversal characters (`.`, `/`, `\`)

### Agent Configuration (`config.yaml`)

```yaml
provider: anthropic        # anthropic | openai | ollama | auto
model: sonnet-4-20250514   # model identifier

templates_dir: ../../docs   # relative to agent.py - points to docs/
state_dir: ./state

company:
  name: "[Your Company]"
  product: "[Your Product]"
  value_prop: "[Your Value Proposition]"
  website: "[Your Website]"
```

The `config.yaml` is committed; `.env` is gitignored (use `.env.example` as a starting point).

---

## Architecture: Partner Agent

### Class Structure (`agent.py`)

| Class/Component | Responsibility |
|---|---|
| `PartnerAgent` | Main orchestrator; loads config, LLM, playbooks, templates |
| `OllamaClient` | Local Ollama HTTP client with exponential backoff retry |
| `RetryConfig` | Configures retry behavior (max attempts, delays) |

### LLM Provider Priority

1. If `provider=ollama` or `provider=auto` and Ollama health check passes → use Ollama
2. If `provider=anthropic` → use `anthropic.Anthropic` SDK
3. If `provider=openai` → use `openai.OpenAI` SDK (v1.x syntax)

### Security Considerations

The agent enforces two key security controls:

1. **Path traversal prevention** (`_validate_path`): template and playbook paths are resolved and checked to remain within their base directories
2. **Input sanitization** (`_sanitize_partner_name`): partner names are validated for length, character set, and path traversal sequences

Do not remove or weaken these controls.

### Output Formatting

All agent output goes through `_print()`, `_print_error()`, `_print_success()`, `_print_warning()`. These gracefully degrade when `rich` is not installed.

---

## CI/CD Workflows

| Workflow | Trigger | What it does |
|---|---|---|
| `deploy-docs.yml` | Push to `main` (docs/** or mkdocs.yml) | Builds MkDocs site, deploys to GitHub Pages |
| `markdown_lint.yml` | Push/PR touching `*.md` | Runs `scripts/lint_markdown.py` via `npm run lint:md` |
| `run_partner_agent.yml` | Manual (`workflow_dispatch`) | Runs a specific playbook + partner via GitHub Actions |

### Deploy Docs Requirements

- Python 3.11
- `mkdocs-material`, `mkdocs-minify-plugin`, `pillow`, `cairosvg`
- Pushes to `main` only; requires `contents: read`, `pages: write`, `id-token: write` permissions

### Manual Agent Workflow Inputs

- `playbook`: one of recruit / onboard / qbr / expand / exit / co-marketing / support-escalation
- `partner`: partner name string
- `provider`: anthropic / openai / ollama
- Requires `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` secrets in the repository

---

## Markdown Linting Rules

`scripts/lint_markdown.py` enforces:

- No trailing whitespace on any line
- Space after `##` heading hashes (e.g., `## Title` not `##Title`)
- Newline at end of file
- No extraneous shell prompt lines (lines starting with `root@`)

Linting runs on every `*.md` push via `markdown_lint.yml`.

---

## Template Categories

### Strategy Templates (`docs/strategy/`)

| # | Template | Purpose |
|---|---|---|
| 1 | Partner Business Case | Business justification for a partnership |
| 2 | Ideal Partner Profile | Define target partner characteristics |
| 3 | 3C/4C Evaluation Framework | Structured partner scoring |
| 4 | Competitive Differentiation | Position vs. competitors |
| 5 | Partner Strategy Plan | Full GTM strategy |
| 6 | Program Architecture | Bronze/Silver/Gold tier design |
| 7 | Internal Alignment Playbook | Stakeholder buy-in |
| 8 | Partner Exit Checklist | Graceful partner offboarding |

### Recruitment Templates (`docs/recruitment/`)

| # | Template | Purpose |
|---|---|---|
| 1 | Email Sequence | Cold outreach cadence |
| 2 | Outreach/Engagement Sequence | Multi-touch engagement |
| 3 | Qualification Framework | Scoring potential partners |
| 4 | Discovery Call Script | First-call structure |
| 5 | Partner Pitch Deck | Slide deck outline |
| 6 | Partnership One-Pager | Executive summary leave-behind |
| 7 | Proposal Template | Formal partnership proposal |
| 8 | Agreement Template | Contract structure |
| 9 | Onboarding Checklist | New partner activation steps |
| 10 | ICP Alignment Tracker | Ideal customer profile tracking |

### Enablement Templates (`docs/enablement/`)

| # | Template | Purpose |
|---|---|---|
| 1 | Enablement Roadmap | Training timeline |
| 2 | Training Deck | Partner training materials |
| 3 | Certification Program | Partner certification structure |
| 4 | Co-Marketing Playbook | Joint marketing campaigns |
| 5 | Technical Integration Guide | Integration documentation |
| 6 | Partner Success Metrics | KPI tracking framework |
| III.7 | QBR Template | Quarterly business review |

---

## Partner Tier Model

The enterprise framework uses three tiers:

| Tier | Revenue Target | Key Benefits |
|---|---|---|
| Bronze (Registered) | < $100K/year | Self-service portal, deal registration, basic materials |
| Silver (Certified) | $100K–$500K/year | Co-marketing, priority leads, dedicated partner manager |
| Gold (Strategic) | $500K+/year | Executive sponsor, joint GTM, custom enablement, QBRs |

QBR frequency by tier: Gold → quarterly, Silver → semi-annually, Bronze → annually.

---

## Adding New Content

### Adding a New Documentation Template

1. Create a `.md` file in the appropriate `docs/` subdirectory
2. Add YAML frontmatter at the top (required — CI will fail without it)
3. Add the file to `mkdocs.yml` under the appropriate `nav` section
4. Run `mkdocs serve` locally to verify rendering

### Adding a New Playbook

1. Create `scripts/partner_agent/playbooks/<name>.yaml`
2. Follow the playbook YAML schema above
3. Add the playbook name to `run_partner_agent.yml` options list
4. Add it to `test_playbooks_exist` in `tests/test_templates.py`
5. Test with: `python agent.py --playbook <name> --partner "Test Partner"`

### Adding a New Source Template

1. Add the `.md` file to the relevant `docs/` subdirectory (strategy, recruitment, enablement)
2. Reference it in a playbook step's `template` field if applicable
3. Ensure the file has YAML frontmatter

---

## What Not to Do

- Do not commit `.env` files — use `.env.example` as the template
- Do not commit `scripts/partner_agent/state/` — it contains partner data and is gitignored
- Do not commit to `main` directly — use pull requests
- Do not skip YAML frontmatter in `docs/` Markdown files — CI enforces it
- Do not weaken `_validate_path` or `_sanitize_partner_name` — these prevent path traversal attacks
- Do not use the `site/` directory as a source — it is build output only
