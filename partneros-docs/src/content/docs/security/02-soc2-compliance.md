---
title: SOC 2 Compliance Guide for Partners
section: Security
category: compliance
template_number: S.2
version: 1.0.0
last_updated: 2026-02-20
author: PartnerOS Team

tier:
  - Gold
  - Strategic
skill_level: intermediate
purpose: operational
phase: enablement
time_required: 2-4 hours
difficulty: medium
prerequisites:
  - Security Questionnaire (S.1)

description: >
  Guide for partners to understand and demonstrate SOC 2 compliance requirements.

purpose_detailed: >
  Use this guide to communicate your SOC 2 posture to partners, set compliance
  expectations for accessing customer data or production systems, and establish
  a shared security baseline.

outcomes:
  - Defined SOC 2 requirements for partner access
  - Clear evidence collection process
  - Shared security controls baseline

skills_gained:
  - Security compliance management
  - Third-party risk assessment
  - Partner security governance
---


## Outcomes

- Defined SOC 2 requirements for partner access
- Clear evidence collection process
- Shared security controls baseline

## Skills Gained

- Security compliance management
- Third-party risk assessment
- Partner security governance

---

## How to Use This Template

**Purpose:**
Customers increasingly require their vendors — and those vendors' partners — to
demonstrate SOC 2 compliance. Use this guide to communicate requirements to
partners who handle, transmit, or have access to customer data.

**Steps:**
1. Customize sections with your specific data environment
2. Share with Gold/Strategic partners during onboarding
3. Request partner's current SOC 2 report or equivalents
4. Review annually or upon significant partner change

---

# SOC 2 Compliance Guide for Partners

**Issued by:** [Company Name] Security Team
**Version:** 1.0
**Review Date:** [Date + 12 months]
**Applies to:** Partners with access to [Company] systems, customer data, or production environments

---

## WHY THIS MATTERS

[Company] holds SOC 2 Type II certification. Partners who access our systems
or customer data are required to demonstrate equivalent controls — or operate
under our security framework.

Failure to meet these requirements may result in:
- Restricted access to production environments
- Delay or suspension of integration approvals
- Exclusion from Gold/Strategic tier programs

---

## SCOPE OF THIS GUIDE

This guide applies when a partner:

- Accesses [Company] production APIs with customer data in scope
- Handles, stores, or processes [Company] customer PII or confidential data
- Integrates with [Company] systems via shared credentials or service accounts
- Provides professional services inside a customer's environment alongside [Company] software

> **Not in scope:** Partners who only resell or refer — with no data access.

---

## SOC 2 TRUST SERVICE CRITERIA (OVERVIEW)

| Criteria | Description | Required for Partners? |
|----------|-------------|----------------------|
| Security (CC) | System protected against unauthorized access | **Yes — All partners** |
| Availability (A) | System available per SLA commitments | Yes — for SaaS integrations |
| Processing Integrity (PI) | Processing complete, valid, and accurate | Where applicable |
| Confidentiality (C) | Confidential info protected as committed | **Yes — data-handling partners** |
| Privacy (P) | PII collected, used, retained, disposed per policy | Yes — PII in scope |

---

## PARTNER REQUIREMENTS BY ACCESS LEVEL

### Level 1 — API / Integration Access (No Customer PII)

| Control | Requirement |
|---------|------------|
| Authentication | OAuth 2.0 or API key rotation every [90] days |
| Transport security | TLS 1.2+ for all API calls |
| Credential storage | No hardcoded credentials; use secrets manager |
| Logging | API access logged and retained [90] days |
| Incident response | Notify [Company Security] within [24 hours] of suspected breach |

**Evidence required:** Self-attestation form (annual)

---

### Level 2 — Customer Data Access (PII or Confidential)

All Level 1 controls plus:

| Control | Requirement |
|---------|------------|
| SOC 2 report | SOC 2 Type II report (< 12 months old) or equivalent |
| Access control | Role-based access; least privilege enforced |
| Encryption at rest | AES-256 or equivalent for stored customer data |
| MFA | Required for all staff with data access |
| Background checks | Required for all staff with production access |
| Subprocessor disclosure | List all subprocessors handling [Company] data |
| DPA signed | Data Processing Addendum required |

**Evidence required:** Current SOC 2 Type II report + DPA

---

### Level 3 — Managed Service / Full Production Access

All Level 1 + Level 2 controls plus:

| Control | Requirement |
|---------|------------|
| Annual pen test | By qualified third party; results shared |
| Vulnerability management | Critical vulns patched within [7] days |
| Security training | Annual security awareness training, documented |
| Incident response plan | Written IRP, tested annually |
| Business continuity | BCP tested within prior 12 months |
| Insurance | Cyber liability coverage ≥ $[amount] |

**Evidence required:** SOC 2 Type II + pen test summary + security controls attestation

---

## EVIDENCE COLLECTION PROCESS

### Step 1 — Initial Submission (Onboarding)

Partners submit the following to [security@company.com]:

| Document | Level 1 | Level 2 | Level 3 |
|----------|---------|---------|---------|
| Self-attestation form | ✅ | ✅ | ✅ |
| SOC 2 Type II report | — | ✅ | ✅ |
| Signed DPA | — | ✅ | ✅ |
| Pen test executive summary | — | — | ✅ |
| Subprocessor list | — | ✅ | ✅ |

### Step 2 — Review

[Company] Security reviews within [15 business days]. Outcome:

- **Approved** — Partner access granted / maintained
- **Conditional** — Access granted with remediation plan (90-day window)
- **Denied** — Material gaps; access suspended until resolved

### Step 3 — Annual Renewal

Partners must re-submit evidence annually. Automated reminders sent [60] days
before expiration.

---

## ACCEPTABLE ALTERNATIVES TO SOC 2

If a partner does not have SOC 2 Type II, [Company] may accept:

| Alternative | Notes |
|-------------|-------|
| ISO 27001 certification | Current certificate required |
| FedRAMP authorization | If applicable to partner's product |
| PCI DSS Level 1 | For payment-data-specific controls |
| [Company] security questionnaire | Level 1 partners only; scored ≥ [80%] |

---

## INCIDENT NOTIFICATION REQUIREMENTS

Partners must notify [Company] at [security@company.com] **within [24 hours]**
of becoming aware of:

- Unauthorized access to systems handling [Company] data
- Confirmed or suspected breach of [Company] customer data
- Ransomware or destructive malware affecting in-scope systems
- Loss or theft of devices containing [Company] data

Include in notification:
- Date/time discovered
- Systems and data potentially affected
- Actions taken so far
- Point of contact for incident response coordination

---

## CHECKLIST — PARTNER ONBOARDING

- [ ] Determine access level (1, 2, or 3)
- [ ] Collect required evidence per level
- [ ] Review and approve / conditionally approve
- [ ] Execute DPA (Level 2/3)
- [ ] Document approval and expiration in partner record
- [ ] Set renewal reminder
- [ ] Add partner to security incident notification list

---

## Related Templates

- [Security Questionnaire](01-security-questionnaire.md/)
- [Data Processing Addendum](../legal/03-dpa.md/)
- [Partnership Agreement](../recruitment/08-agreement.md/)
- [Technical Integration Guide](../enablement/05-technical-integration.md/)
---

## Template Metadata

| Attribute | Value |
|-----------|-------|
| **Template Number** | S.2 |
| **Version** | 1.0.0 |
| **Last Updated** | 2026-02-20 |
| **Time Required** | 2-4 hours |
| **Difficulty** | medium |
| **Skill Level** | intermediate |
| **Phase** | enablement |
| **Purpose** | operational |

## Outcomes

- Defined SOC 2 requirements for partner access
- Clear evidence collection process
- Shared security controls baseline

## Skills Gained

- Security compliance management
- Third-party risk assessment
- Partner security governance

## Prerequisites

- Security Questionnaire (S.1)
