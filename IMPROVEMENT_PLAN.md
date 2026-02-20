# PartnerOS Improvement Plan
*Generated: January 29, 2026*
*Updated: February 20, 2026*

> **See [ARCHITECTURE.md](ARCHITECTURE.md) for architecture decisions**
> **See [BACKLOG.md](BACKLOG.md) for prioritized roadmap**

---

## Current State (February 20, 2026)

**What's Done:**
- ✅ 44 templates across 9 categories
- ✅ 20 automated tests
- ✅ Template generator script
- ✅ Standardize script
- ✅ MkDocs documentation site
- ✅ 7 Agent playbooks
- ✅ Legal/Finance/Security templates
- ✅ Pre-commit hooks

---

## Phase 1: Foundation (Drop-Ready) ⚡

*Goal: A company can download and get started in 30 minutes*

### 1.1 Company Config Script
**File:** `scripts/onboard.py`

**Features:**
- Interactive prompts for company name, website, logo URL, colors
- Generates `.company-config/customize.yaml`
- Optional: walks through key templates

**Prompt Questions:**
```
Welcome to PartnerOS Setup!
What's your company name? [Acme Corp]
What's your website? [acmecorp.com]
Who should partners contact? [name, email]
What's your primary brand color? [#000000]
Logo URL (optional)? [https://...]
```

### 1.2 Template Variable System
**Files:** `scripts/fill_template.py` (new)

**Variables Supported:**
```
{{company_name}}
{{company_website}}
{{contact_name}}
{{contact_email}}
{{logo_url}}
{{brand_color}}
{{today_date}}
```

### 1.3 Quick Start Guide
**File:** `docs/getting-started/quick-start.md`

**Sections:**
1. What is PartnerOS?
2. How to customize for your company (5 min)
3. Finding the right template (template selection guide)
4. First week checklist
5. Resources & help

### 1.4 Example Fills
**Directory:** `examples/complete-examples/`

**Create 3-5 filled examples:**
- `example-partner-onboarding.md` - Full onboarding example
- `example-partner-business-case.md` - Completed business case
- `example-qbr-template.md` - Filled QBR

---

## Phase 2: Sales Ready 📦

*Goal: Something to show prospects, easy to demo*

### 2.1 Demo Mode
**Features:**
- Pre-configured `.company-config` with fake company
- Example partners (Acme Partners, Beta Resellers)
- Sample pipeline and deals

### 2.2 One-Pager
**File:** `docs/resources/partner-os-one-pager.md`

**Content:**
- What is PartnerOS
- Key features (3-4 bullet points)
- Who is it for
- Pricing/licensing
- Contact info

### 2.3 Pricing Sheet
**File:** `docs/resources/licensing.md`

**Options:**
- Self-service (free)
- Implementation + Training (TBD)
- Enterprise (custom)

---

## Execution Log

### Completed This Session (Feb 20, 2026)
- Created ARCHITECTURE.md
- Updated BACKLOG.md with 5-phase plan
- Created/improved tests (20 total)

---

*See BACKLOG.md for full prioritized list*
