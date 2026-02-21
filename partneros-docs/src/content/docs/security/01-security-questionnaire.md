---
title: Partner Security Questionnaire
section: Security
category: compliance
template_number: S.1
version: 1.0.0
last_updated: 2026-02-20
author: PartnerOS Team

tier:
  - Silver
  - Gold
skill_level: intermediate
purpose: operational
phase: recruitment
time_required: 1-2 hours
difficulty: medium
prerequisites:
  - Mutual NDA (L.1)

description: >
  Security questionnaire for assessing partner security posture.

purpose_detailed: >
  Use this questionnaire to evaluate the security practices of potential
  and existing partners before sharing sensitive data.

outcomes:
  - Security assessment completed
  - Risk areas identified
  - Compliance verification

skills_gained:
  - Security assessment
  - Compliance verification
  - Risk evaluation
---

> **Security questionnaire for assessing partner security posture.**



## How to Use This Template

**Purpose:**
Use this questionnaire to assess the security posture of partners before granting access to sensitive systems or data.

**Steps:**
1. Send questionnaire to partner
2. Collect responses
3. Evaluate answers
4. Identify gaps/risks
5. Determine approval status

---

# Partner Security Questionnaire

## PARTNER INFORMATION

**Company Name:** _________________________________

**Contact Name:** _________________________________

**Contact Email:** _________________________________

**Date Completed:** _________________________________

## SECTION 1: ORGANIZATIONAL SECURITY

### 1.1 Security Governance
| Question | Response |
|----------|----------|
| Do you have a dedicated information security function? | [ ] Yes [ ] No |
| Do you have a Chief Information Security Officer (CISO)? | [ ] Yes [ ] No |
| Is security budget allocated annually? | [ ] Yes [ ] No |
| Do you have written information security policies? | [ ] Yes [ ] No |

**If yes, please provide:** [Attach policies]

### 1.2 Compliance Certifications
| Certification | Status | Expiration |
|--------------|--------|------------|
| SOC 2 Type II | [ ] Yes - Date: ____ | ____ |
| ISO 27001 | [ ] Yes - Date: ____ | ____ |
| PCI DSS | [ ] Yes - Date: ____ | ____ |
| HIPAA | [ ] Yes - Date: ____ | ____ |
| FedRAMP | [ ] Yes - Date: ____ | ____ |
| GDPR | [ ] Compliant [ ] In Progress [ ] N/A |

**Other certifications:** _________________________________

### 1.3 Security Training
| Question | Response |
|----------|----------|
| Is security training mandatory for all employees? | [ ] Yes [ ] No |
| How often is security training conducted? | [ ] |
| Do you track completion rates? | [ ] Yes [ ] No |

## SECTION 2: DATA PROTECTION

### 2.1 Data Encryption
| Question | Response |
|----------|----------|
| Is data encrypted at rest? | [ ] Yes [ ] No |
| Encryption standard used: | [ ] |
| Is data encrypted in transit? | [ ] Yes [ ] No |
| TLS version used: | [ ] |
| Do you use customer-managed encryption keys? | [ ] Yes [ ] No [ ] N/A |

### 2.2 Access Control
| Question | Response |
|----------|----------|
| Do you use role-based access control (RBAC)? | [ ] Yes [ ] No |
| Is multi-factor authentication (MFA) required? | [ ] Yes [ ] No |
| For which systems? | [ ] |
| How often are access rights reviewed? | [ ] |

### 2.3 Data Classification
| Question | Response |
|----------|----------|
| Do you have a data classification scheme? | [ ] Yes [ ] No |
| How is sensitive data identified? | [ ] |
| Do you have data loss prevention (DLP) tools? | [ ] Yes [ ] No |

## SECTION 3: INFRASTRUCTURE SECURITY

### 3.1 Network Security
| Question | Response |
|----------|----------|
| Do you use firewalls? | [ ] Yes [ ] No |
| Is network segmentation implemented? | [ ] Yes [ ] No |
| Do you conduct vulnerability scanning? | [ ] Yes [ ] No |
| Frequency: | [ ] |
| Do you conduct penetration testing? | [ ] Yes [ ] No |
| Frequency: | [ ] |
| Last penetration test date: | ____ |

### 3.2 Cloud Security
| Provider | Services Used | Compliance |
|----------|--------------|------------|
| AWS | [ ] | [ ] |
| Azure | [ ] | [ ] |
| GCP | [ ] | [ ] |
| Other | [ ] | [ ] |

### 3.3 Endpoint Security
| Question | Response |
|----------|----------|
| Is antivirus/anti-malware deployed? | [ ] Yes [ ] No |
| Is endpoint detection and response (EDR) used? | [ ] Yes [ ] No |
| Are endpoints automatically patched? | [ ] Yes [ ] No |

## SECTION 4: INCIDENT RESPONSE

### 4.1 Incident Response Capabilities
| Question | Response |
|----------|----------|
| Do you have an incident response plan? | [ ] Yes [ ] No |
| When was it last tested? | ____ |
| Do you have a dedicated security operations center (SOC)? | [ ] Yes [ ] No |
| Do you have cyber insurance? | [ ] Yes [ ] No |

### 4.2 Breach Notification
| Question | Response |
|----------|----------|
| What is your breach notification timeline? | [ ] |
| How do you notify customers? | [ ] |
| Have you had a breach in the past 24 months? | [ ] Yes [ ] No |

**If yes, describe:** _________________________________

## SECTION 5: THIRD-PARTY SECURITY

### 5.1 Vendor Management
| Question | Response |
|----------|----------|
| Do you assess third-party vendor security? | [ ] Yes [ ] No |
| How often? | [ ] |
| Do you have a vendor risk management program? | [ ] Yes [ ] No |

### 5.2 Sub-processors
| Question | Response |
|----------|----------|
| Do you use sub-processors? | [ ] Yes [ ] No |
| Can you provide a list? | [ ] Yes [ ] No |

## SECTION 6: HUMAN RESOURCES

### 6.1 Employee Security
| Question | Response |
|----------|----------|
| Do you conduct background checks? | [ ] Yes [ ] No |
| Are employees required to sign NDAs? | [ ] Yes [ ] No |
| Is there a termination process for access removal? | [ ] Yes [ ] No |

## SECTION 7: BUSINESS CONTINUITY

### 7.1 Resilience
| Question | Response |
|----------|----------|
| Do you have a disaster recovery plan? | [ ] Yes [ ] No |
| Is data backed up regularly? | [ ] Yes [ ] No |
| What is your RTO (Recovery Time Objective)? | [ ] |
| What is your RPO (Recovery Point Objective)? | [ ] |

---

## SCORING

| Section | Weight | Score | Max |
|---------|--------|-------|-----|
| Organizational Security | 15% | __/10 | 10 |
| Data Protection | 20% | __/10 | 10 |
| Infrastructure Security | 20% | __/10 | 10 |
| Incident Response | 15% | __/10 | 10 |
| Third-Party Security | 10% | __/10 | 10 |
| Human Resources | 10% | __/10 | 10 |
| Business Continuity | 10% | __/10 | 10 |
| **TOTAL** | 100% | **__/70** | 70 |

### Risk Rating
| Score | Risk Level | Action |
|-------|------------|--------|
| 56-70 | Low | Approve |
| 42-55 | Medium | Conditional approval |
| 28-41 | High | Additional review required |
| 0-27 | Critical | Do not proceed |

---

## ASSESSMENT CONCLUSION

| Item | Decision |
|------|----------|
| Overall Risk Score | __/70 |
| Risk Rating | [ ] Low [ ] Medium [ ] High [ ] Critical |
| Recommended Action | [ ] Approve [ ] Conditional [ ] Reject |
| Reviewer Name | _______________________ |
| Review Date | _______________________ |

**Notes:** _________________________________

---

## Checklist

- [ ] Send questionnaire to partner
- [ ] Collect completed responses
- [ ] Verify certifications (request evidence)
- [ ] Score responses
- [ ] Determine risk rating
- [ ] Document decision
- [ ] Communicate outcome to partner
- [ ] Store in partner file

---

## Related Templates

- [Mutual NDA](../legal/01-nda/)
- [Data Processing Agreement](../legal/03-dpa/)
- [SOC2 Compliance Guide](02-soc2-compliance/)
---
