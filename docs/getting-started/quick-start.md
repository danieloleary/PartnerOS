---
title: Quick Start
category: operational
version: 1.0.0
last_updated: 2026-02-20
author: PartnerOS Team
tier:
  - Bronze
  - Silver
  - Gold
skill_level: beginner
purpose: operational
phase: onboarding
time_required: 30 minutes
difficulty: easy
prerequisites: []
description: Get up and running with PartnerOS in 30 minutes
outcomes:
  - PartnerOS configured for your company
  - Understanding of available templates
  - First partner recruitment started
skills_gained:
  - Partner program setup
  - Template selection
  - Customization basics
---
---
# PartnerOS Quick Start Guide

*From zero to your first partner in 30 minutes*

---

## Step 1: Set Up (5 minutes)

### Interactive Setup (Recommended)

```bash
python scripts/onboard.py
```

This prompts for your company name, website, contact info, and brand color.

### Manual Setup

Create `.company-config/customize.yaml`:

```yaml
company:
  name: "Your Company"
  website: "https://yourcompany.com"
contact:
  name: "Partner Manager"
  email: "partners@yourcompany.com"
branding:
  brand_color: "#3B82F6"
```

---

## Step 2: Find Templates (5 minutes)

| Your Stage | Start Here |
|-----------|-----------|
| No partners yet | [Recruitment templates](../recruitment/index.md) |
| Need process | [Enablement templates](../enablement/index.md) |
| Design program | [Strategy templates](../strategy/index.md) |
| Legal needed | [Legal templates](../legal/index.md) |

---

## Step 3: Customize (10 minutes)

### Use Variables

```bash
# See all variables
python scripts/fill_template.py --list-vars

# Fill a template
python scripts/fill_template.py --template docs/recruitment/01-email-sequence.md
```

Variables: `{{company_name}}`, `{{contact_name}}`, `{{contact_email}}`, `{{today_date}}`

---

## Step 4: Your First Partner (10 minutes)

### Recommended Path

1. [Ideal Partner Profile](../strategy/02-ideal-partner-profile.md)
2. [Email Sequence](../recruitment/01-email-sequence.md)
3. [Qualification Framework](../recruitment/03-qualification-framework.md)
4. [Pitch Deck](../recruitment/05-pitch-deck.md)
5. [Agreement Template](../recruitment/08-agreement.md)

---

## Choose Your Path

=== ":material-account-cog: Full Setup (30 min)"

    **Best for:** Companies who want PartnerOS customized for their use.

    1. **Run the setup script:**
        ```bash
        python scripts/onboard.py
        ```
    
    2. **Follow the prompts:**
        - Your company name
        - Website
        - Primary partner contact
        - Brand color
    
    3. **Start using templates:**
        ```bash
        # See available variables
        python scripts/fill_template.py --list-vars
        
        # Fill a template
        python scripts/fill_template.py --template docs/recruitment/01-email-sequence.md
        ```

    4. **Browse templates by category:**
        - [Strategy](../strategy/index.md) - Program design
        - [Recruitment](../recruitment/index.md) - Find partners
        - [Enablement](../enablement/index.md) - Train partners
        - [Legal](../legal/index.md) - Contracts
        - [Finance](../finance/index.md) - Commissions

    **Best for:** Teams who want to browse and use templates directly.

    1. Browse the template sections:
        - [Strategy](../strategy/index.md) - Define your partnership vision
        - [Recruitment](../recruitment/index.md) - Find and sign partners
        - [Enablement](../enablement/index.md) - Train and support partners

    2. Find a template that fits your need

    3. Copy the content and customize for your company

=== ":material-robot: Partner Agent (AI)"

    **Best for:** Teams who want AI-assisted playbook execution.

    ```bash
    # Clone the repo
    git clone https://github.com/danieloleary/PartnerOS.git
    cd PartnerOS/scripts/partner_agent

    # Install dependencies
    pip install -r requirements.txt

    # Set your API key
    export ANTHROPIC_API_KEY=sk-ant-...
    # or
    export OPENAI_API_KEY=sk-...

    # Run interactively
    python agent.py
    ```

=== ":material-web: Self-Host Docs"

    **Best for:** Teams who want their own internal documentation site.

    ```bash
    # Clone the repo
    git clone https://github.com/danieloleary/PartnerOS.git
    cd PartnerOS

    # Install MkDocs
    pip install mkdocs-material

    # Preview locally
    mkdocs serve

    # Deploy to GitHub Pages
    mkdocs gh-deploy
    ```

---

## Template Structure

Every template follows a consistent structure:

```markdown
---
title: Template Name
description: What this template is for
keywords: [searchable, tags]
---

## How to Use This Template

Step-by-step instructions...

---

# Template Name

## Section 1
[Content with placeholders like [Your Company]]

## Section 2
[More content...]
```

!!! tip "Placeholders"
    Look for text in `[brackets]` - these are placeholders for you to fill in with your specific information.

---

## Recommended Workflow

### For New Partner Programs

```mermaid
graph LR
    A[Business Case] --> B[Ideal Partner Profile]
    B --> C[Program Architecture]
    C --> D[Start Recruiting]
```

1. Start with [Partner Business Case](../strategy/01-partner-business-case.md)
2. Define your [Ideal Partner Profile](../strategy/02-ideal-partner-profile.md)
3. Design your [Program Architecture](../strategy/06-program-architecture.md)
4. Begin [Recruitment](../recruitment/index.md)

### For Signing a Specific Partner

```mermaid
graph LR
    A[Qualify] --> B[Discovery Call]
    B --> C[Pitch]
    C --> D[Proposal]
    D --> E[Agreement]
```

1. Use the [Qualification Framework](../recruitment/03-qualification-framework.md)
2. Run a [Discovery Call](../recruitment/04-discovery-call.md)
3. Present the [Pitch Deck](../recruitment/05-pitch-deck.md)
4. Send a [Proposal](../recruitment/07-proposal.md)

### For Ongoing Management

- Run quarterly [QBRs](../enablement/07-qbr-template.md)
- Track [Success Metrics](../enablement/06-success-metrics.md)
- Update [ICP Alignment](../recruitment/10-icp-tracker.md)

---

## Next Steps

<div class="grid">

<div class="card" markdown>

### :material-book-open-variant: Learn the Lifecycle
Understand the partner journey from strategy to enablement.

[Partner Lifecycle →](lifecycle.md)

</div>

<div class="card" markdown>

### :material-pencil: Customize Templates
Tips for making templates your own.

[How to Use Templates →](how-to-use.md)

</div>

</div>
