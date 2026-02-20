# PartnerOS

**The complete playbook for building and scaling strategic partnerships with AI-powered automation.**

[![Deploy Docs](https://github.com/danieloleary/PartnerOS/actions/workflows/deploy-docs.yml/badge.svg)](https://github.com/danieloleary/PartnerOS/actions/workflows/deploy-docs.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## The Problem

Building a world-class partner program is hard. Most companies:

- **Start from scratch** — Reinventing the wheel with every new partnership
- **Lack consistency** — No standardized processes for recruitment, onboarding, or enablement
- ** Struggle to scale** — Manual workflows that break as partner count grows
- **Miss revenue** — No systematic approach to partner-driven growth

**PartnerOS solves this.**

---

## Why PartnerOS?

| Benefit | Description |
|---------|-------------|
| **Complete Playbooks** | 7 end-to-end automation playbooks covering the entire partner lifecycle |
| **34 Ready-to-Use Templates** | Strategy (8), recruitment (10), and enablement (7) templates plus getting started guides and resources |
| **AI-Powered Agent** | Local AI partner assistant runs offline with Ollama — no API keys required |
| **Enterprise-Ready** | Three-tier partner framework (Bronze/Silver/Gold) with clear progression paths |
| **Tested & Validated** | Automated template validation and agent tests ensure reliability |

---

## Who Is This For?

- **Startup founders** building their first partner program
- **Partner managers** at mid-market companies scaling partnerships
- **Channel directors** at enterprises managing 100+ partners
- **Revenue leaders** looking to unlock partner-driven growth
- **Anyone** building strategic partnerships from scratch

---

## Live Demo

**👉 [danieloleary.github.io/PartnerOS](https://danieloleary.github.io/PartnerOS)**

Browse the full documentation, explore templates, and see the AI Agent in action.

---

## Quick Start

### Option 1: Run the AI Partner Agent (Recommended)

```bash
# Clone the repo
git clone https://github.com/danieloleary/PartnerOS.git
cd PartnerOS/scripts/partner_agent

# Install dependencies
pip install -r requirements.txt

# Set up local AI (free, private, offline)
brew install ollama
ollama pull llama3.2:3b

# Run the agent
export OLLAMA_ENDPOINT=http://localhost:11434
export OLLAMA_MODEL=llama3.2:3b
python agent.py
```

Or use Anthropic API (cloud):
```bash
export ANTHROPIC_API_KEY=sk-ant-...
export PROVIDER=anthropic
python agent.py
```

### Option 2: Browse Online

**[danieloleary.github.io/PartnerOS](https://danieloleary.github.io/PartnerOS)** — Full documentation with all templates.

### Option 3: Run Locally

```bash
pip install mkdocs-material
mkdocs serve
# Open http://localhost:8000
```

---

## Playbooks

| Playbook | Steps | Description |
|----------|-------|-------------|
| **recruit** | 5 | Find, qualify, and sign new partners |
| **onboard** | 5 | Activate and enable signed partners |
| **qbr** | 4 | Quarterly business reviews |
| **expand** | 5 | Grow existing partnerships |
| **exit** | 5 | End partnerships gracefully |
| **co-marketing** | 5 | Joint marketing campaigns |
| **support-escalation** | 5 | Handle partner issues |

---

## Enterprise Partner Framework

PartnerOS implements a three-tier partner model:

### Bronze (Registered)
- Self-service enablement portal
- Basic sales materials
- Deal registration
- **Annual Revenue Target:** <$100K

### Silver (Certified)
- Technical certification
- Co-marketing access
- Priority lead distribution
- Dedicated partner manager
- **Annual Revenue Target:** $100K-$500K

### Gold (Strategic)
- Executive sponsorship
- Custom enablement
- Joint GTM planning
- Quarterly business reviews
- **Annual Revenue Target:** $500K+

---

## Project Structure

```
PartnerOS/
├── docs/                      # Templates & documentation (single source of truth)
│   ├── strategy/              # Strategy templates (8)
│   ├── recruitment/           # Recruitment templates (10)
│   ├── enablement/            # Enablement templates (7)
│   ├── getting-started/       # Quick start guides
│   ├── resources/             # Glossary, maturity model
│   └── agent/                 # Partner Agent docs
├── scripts/
│   └── partner_agent/         # AI Partner Agent
│       ├── agent.py           # Main agent (Ollama + Anthropic)
│       ├── config.yaml        # Agent & company configuration
│       ├── playbooks/         # Playbook definitions (7 total)
│       └── .env.example       # Environment config
├── .partner_data/             # YOUR private partner data (gitignored)
├── tests/                     # Automated tests
├── mkdocs.yml                 # Site configuration
├── ROADMAP.md                 # Product roadmap
├── BACKLOG.md                 # Missing templates backlog
└── README.md                  # This file
```

---

## Testing

```bash
# Run all tests
python3 tests/test_templates.py
python3 tests/test_agent.py

# Expected output: "All tests passed!"
```

---

## Recent Updates

### v1.1 (February 2026)
- ✅ Fixed incomplete `_continue_playbook_interactive` method
- ✅ Added partner name sanitization & path traversal protection
- ✅ Added API retry with exponential backoff
- ✅ Added structured logging (--verbose flag)
- ✅ Added config reload support (--reload flag)
- ✅ Comprehensive test suite

### v1.0 (January 2026)
- ✅ 7 automation playbooks
- ✅ Local Ollama support (no API keys required)
- ✅ Enterprise partner framework (three-tier model)
- ✅ Automated testing framework

---

## Contributing

We welcome contributions! Here's how to help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Add** templates to `docs/` with YAML frontmatter
4. **Update** playbooks in `scripts/partner_agent/playbooks/`
5. **Test** your changes (`python3 tests/test_templates.py`)
6. **Commit** your changes (`git commit -m 'Add amazing feature'`)
7. **Push** to the branch (`git push origin feature/amazing-feature`)
8. **Open** a Pull Request

### Adding New Templates

- Add Markdown files to appropriate `docs/` subdirectories
- Include YAML frontmatter with `title`, `description`, and `tags`
- Follow existing template patterns

### Adding New Playbooks

- Define in `scripts/partner_agent/playbooks/`
- Include step definitions, criteria, KPIs, and checklists
- Test with `python3 tests/test_agent.py`

---

## License

MIT License — See [LICENSE](LICENSE) for details.

---

## Resources

- **Documentation:** [danieloleary.github.io/PartnerOS](https://danieloleary.github.io/PartnerOS)
- **GitHub:** [github.com/danieloleary/PartnerOS](https://github.com/danieloleary/PartnerOS)
- **Issues:** Report bugs and feature requests on GitHub
