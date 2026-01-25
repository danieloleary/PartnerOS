# PartnerOS

The complete playbook for building and scaling strategic partnerships.

[![Deploy Docs](https://github.com/danieloleary/PartnerOS/actions/workflows/deploy-docs.yml/badge.svg)](https://github.com/danieloleary/PartnerOS/actions/workflows/deploy-docs.yml)

## Overview

PartnerOS provides **25 battle-tested templates** and an **AI-powered Partner Agent** to help you build world-class partner programs.

| Phase | Templates | Description |
|-------|-----------|-------------|
| **Strategy** | 8 | Define your partnership vision and program architecture |
| **Recruitment** | 10 | Find, qualify, pitch, and sign the right partners |
| **Enablement** | 7 | Train, support, and grow successful partners |

## Quick Start

### Browse Templates Online

**[danieloleary.github.io/PartnerOS](https://danieloleary.github.io/PartnerOS)**

### Run Locally

```bash
git clone https://github.com/danieloleary/PartnerOS.git
cd PartnerOS
pip install mkdocs-material
mkdocs serve
```

Open http://localhost:8000

### Deploy Your Own

```bash
mkdocs gh-deploy
```

## Partner Agent

AI-powered assistant that runs playbooks end-to-end.

```bash
cd scripts/partner_agent
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
python agent.py
```

### Playbooks

| Playbook | Description |
|----------|-------------|
| `recruit` | Sign a new partner (IPP → Qualification → Discovery → Pitch → Proposal) |
| `onboard` | Activate a signed partner (Agreement → Checklist → Enablement → Training) |
| `qbr` | Quarterly business review (Metrics → ICP Review → QBR Doc → Strategy) |
| `expand` | Grow an existing partnership (Business Case → Strategy → Co-Marketing) |
| `exit` | End a partnership gracefully (Exit Checklist → Customer Transition) |

### Run from GitHub

1. Add `ANTHROPIC_API_KEY` to repository secrets
2. Go to **Actions** → **Run Partner Agent**
3. Click **Run workflow** and select a playbook

## Project Structure

```
PartnerOS/
├── docs/                    # MkDocs documentation site
│   ├── strategy/           # Strategy templates (8)
│   ├── recruitment/        # Recruitment templates (10)
│   ├── enablement/         # Enablement templates (7)
│   └── agent/              # Partner Agent docs
├── scripts/
│   └── partner_agent/      # AI agent for playbooks
├── partner_blueprint/       # Original template source
├── mkdocs.yml              # Site configuration
└── .github/workflows/      # CI/CD
```

## Templates

### Strategy (8)

- Partner Business Case
- Ideal Partner Profile
- 3C/4C Evaluation Framework
- Competitive Differentiation
- Partner Strategy Plan
- Program Architecture
- Internal Alignment Playbook
- Partner Exit Checklist

### Recruitment (10)

- Email Sequences
- Outreach Engagement
- Qualification Framework
- Discovery Call Script
- Partner Pitch Deck
- Partnership One-Pager
- Proposal Template
- Agreement Template
- Onboarding Checklist
- ICP Alignment Tracker

### Enablement (7)

- Enablement Roadmap
- Training Deck
- Certification Program
- Co-Marketing Playbook
- Technical Integration Guide
- Success Metrics
- QBR Template

## Contributing

1. Fork the repository
2. Add templates to `docs/` with YAML frontmatter
3. Submit a pull request

## License

MIT License
