---
title: Home
description: The complete playbook for building and scaling strategic partnerships
hide:
  - navigation
  - toc
---

<div class="hero" markdown>

# PartnerOS

**The complete playbook for building and scaling strategic partnerships.**

Build world-class partner programs with battle-tested templates, proven playbooks, and AI-powered automation.

<div class="cta-buttons">
  <a href="getting-started/quick-start/" class="cta-button primary">
    :material-rocket-launch: Get Started
  </a>
  <a href="strategy/index.md" class="cta-button secondary">
    :material-file-document-multiple: Browse Templates
  </a>
</div>

</div>

<div class="stats">
  <div class="stat">
    <div class="stat-number">25</div>
    <div class="stat-label">Templates</div>
  </div>
  <div class="stat">
    <div class="stat-number">5</div>
    <div class="stat-label">Playbooks</div>
  </div>
  <div class="stat">
    <div class="stat-number">3</div>
    <div class="stat-label">Lifecycle Phases</div>
  </div>
</div>

---

## :material-compass: Partner Lifecycle

<div class="grid">

<div class="card" markdown>

### :material-lightbulb: Strategy

Define your partnership vision, ideal partner profile, and program architecture.

[8 Templates →](strategy/index.md){ .md-button }

</div>

<div class="card" markdown>

### :material-account-plus: Recruitment

Find, qualify, pitch, and sign the right partners for your ecosystem.

[10 Templates →](recruitment/){ .md-button }

</div>

<div class="card" markdown>

### :material-school: Enablement

Onboard, train, and empower partners to sell and deliver successfully.

[7 Templates →](enablement/){ .md-button }

</div>

</div>

---

## :material-robot: Partner Agent

AI-powered assistant that runs playbooks end-to-end.

<div class="playbook-flow">
  <span class="playbook-step">Recruit</span>
  <span class="playbook-arrow">→</span>
  <span class="playbook-step">Onboard</span>
  <span class="playbook-arrow">→</span>
  <span class="playbook-step">QBR</span>
  <span class="playbook-arrow">→</span>
  <span class="playbook-step">Expand</span>
</div>

```bash
# Run a playbook with AI assistance
python agent.py --playbook recruit --partner "Acme Corp"
```

[Learn More →](agent/index.md){ .md-button }

---

## :material-star: Featured Templates

<div class="template-grid">

<a href="strategy/02-ideal-partner-profile/" class="template-card" markdown>
#### Ideal Partner Profile
Define exactly who you're looking for in a partner.
</a>

<a href="recruitment/04-discovery-call/" class="template-card" markdown>
#### Discovery Call Script
Structured questions for qualifying partners.
</a>

<a href="enablement/07-qbr-template/" class="template-card" markdown>
#### QBR Template
Run effective quarterly business reviews.
</a>

<a href="strategy/08-exit-checklist/" class="template-card" markdown>
#### Exit Checklist
End partnerships professionally.
</a>

</div>

---

## :material-clock-fast: Quick Start

=== "Browse Templates"

    1. Pick a lifecycle phase: [Strategy](strategy/index.md), [Recruitment](recruitment/index.md), or [Enablement](enablement/index.md)
    2. Find the template you need
    3. Copy, customize, and use

=== "Run Playbooks"

    ```bash
    cd scripts/partner_agent
    pip install -r requirements.txt
    export ANTHROPIC_API_KEY=sk-ant-...
    python agent.py
    ```

=== "Deploy Site"

    ```bash
    pip install mkdocs-material
    mkdocs serve        # Local preview
    mkdocs gh-deploy    # Deploy to GitHub Pages
    ```

---

<div style="text-align: center; opacity: 0.7; margin-top: 3rem;">

Built with :material-heart: for partnership teams everywhere.

[:material-github: GitHub](https://github.com/danieloleary/PartnerOS){ .md-button }

</div>
