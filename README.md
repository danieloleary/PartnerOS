# PartnerOS

The complete playbook for building and scaling strategic partnerships with an AI-powered Partner Agent.

[![Deploy Docs](https://github.com/danieloleary/PartnerOS/actions/workflows/deploy-docs.yml/badge.svg)](https://github.com/danieloleary/PartnerOS/actions/workflows/deploy-docs.yml)

---

## Overview

PartnerOS provides enterprise-grade templates and an AI-powered Partner Agent to build world-class partner programs.

### Key Features

| Feature | Description |
|---------|-------------|
| **7 Playbooks** | End-to-end partner lifecycle automation |
| **67 Templates** | Strategy, recruitment, and enablement (34 in docs, 33 in partner_blueprint) |
| **Local AI** | Runs offline with Ollama (no API keys needed) |
| **Enterprise Framework** | Three-tier partner model (Bronze/Silver/Gold) |
| **Automated Testing** | Template validation and agent tests |

---

## Quick Start

### Option 1: Use the Partner Agent (Recommended)

```bash
# Clone and set up
git clone https://github.com/danieloleary/PartnerOS.git
cd PartnerOS/scripts/partner_agent

# Install dependencies
pip install -r requirements.txt

# Run with local AI (Ollama)
export OLLAMA_ENDPOINT=http://localhost:11434
export OLLAMA_MODEL=llama3.2:3b
python agent.py

# Or run with Anthropic API (cloud)
export ANTHROPIC_API_KEY=sk-ant-...
export PROVIDER=anthropic
export MODEL=sonnet-4-20250514
python agent.py
```

### Option 2: Browse Templates Online

**[danieloleary.github.io/PartnerOS](https://danieloleary.github.io/PartnerOS)**

### Option 3: Run Locally (Docs Site)

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

**Total: 7 Playbooks**

---

## Enterprise Partner Framework

PartnerOS implements a three-tier partner model:

### Bronze (Registered)
- Self-service enablement portal
- Basic sales materials
- Deal registration
- Annual Revenue Target: <$100K

### Silver (Certified)
- Technical certification
- Co-marketing access
- Priority lead distribution
- Dedicated partner manager
- Annual Revenue Target: $100K-$500K

### Gold (Strategic)
- Executive sponsorship
- Custom enablement
- Joint GTM planning
- Quarterly business reviews
- Annual Revenue Target: $500K+

---

## Project Structure

```
PartnerOS/
├── docs/                      # MkDocs documentation
│   ├── strategy/              # Strategy templates (8)
│   ├── recruitment/           # Recruitment templates (10)
│   ├── enablement/            # Enablement templates (7)
│   └── agent/                 # Partner Agent docs
├── scripts/
│   └── partner_agent/         # AI Partner Agent
│       ├── agent.py           # Main agent (Ollama + Anthropic)
│       ├── playbooks/         # Playbook definitions (7 total)
│       ├── .env.example       # Environment config
│       └── agent.py.backup    # Original backup
├── tests/                     # Automated tests
│   ├── test_templates.py      # Template validation
│   └── test_agent.py          # Agent validation
├── partner_blueprint/         # Original template source
├── mkdocs.yml                 # Site configuration
├── CHANGELOG.md               # Version history
├── FIXES.md                   # Fix documentation
└── IMPROVEMENT_PLAN.md        # Enhancement roadmap
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

## Local AI Setup

PartnerOS works with local Ollama models (free, private, offline):

```bash
# Install Ollama
brew install ollama

# Pull recommended model
ollama pull llama3.2:3b

# Verify
ollama list
# NAME           ID              SIZE      MODIFIED
# llama3.2:3b    abc123def456    4.7 GB    Just now
```

### Supported Models
- **Llama 3.2:3b** (recommended - local, private)
- **Qwen2.5:7b** (alternative - larger context)
- **Mistral 7B** (fast option)

---

## Configuration

Copy `.env.example` to `.env` and configure:

```bash
# Local Ollama (recommended)
OLLAMA_ENDPOINT=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b
PROVIDER=ollama

# Or Anthropic Cloud
# ANTHROPIC_API_KEY=sk-ant-...
# PROVIDER=anthropic
# MODEL=sonnet-4-20250514  # Verified Feb 2026
```

---

## Recent Updates (February 2026)

### v1.1 - Security & Stability
- ✅ Fixed incomplete `_continue_playbook_interactive` method
- ✅ Fixed speculative model names (use verified models)
- ✅ Fixed hardcoded paths (use REPO_ROOT)
- ✅ Added partner name sanitization
- ✅ Added path traversal protection
- ✅ Added API retry with exponential backoff
- ✅ Added structured logging (--verbose flag)
- ✅ Added config reload support (--reload flag)
- ✅ Standardized console output
- ✅ Added comprehensive tests

### v1.0 (January 2026)
- ✅ Added 2 new playbooks (co-marketing, support-escalation)
- ✅ Integrated local Ollama support (no API keys required)
- ✅ Created enterprise partner framework (three-tier model)
- ✅ Added automated testing framework
- ✅ Enhanced all playbooks with tier criteria, KPIs, and checklists
- ✅ Improved documentation and README

---

## Contributing

1. Fork the repository
2. Add templates to `docs/` with YAML frontmatter
3. Update playbooks in `scripts/partner_agent/playbooks/`
4. Run tests before submitting
5. Submit a pull request

---

## License

MIT License - See LICENSE file for details.

---

## Resources

- **Documentation:** [danieloleary.github.io/PartnerOS](https://danieloleary.github.io/PartnerOS)
- **GitHub:** [github.com/danieloleary/PartnerOS](https://github.com/danieloleary/PartnerOS)
- **Issues:** Report bugs and feature requests on GitHub
