# NZ AI Compliance + SOC 2 Type II Skill — Implementation Guide

**Skill Version:** 1.0.0  
**Repositories:** Weaver, Core, Stack, Aether  
**CAT Classification:** Diamond (primary) | Platinum (secondary) | Gold (tertiary)  
**HITL Gate:** Required for all implementation decisions

---

## What This Skill Does

This skill operationalizes compliance + security for Coastal Alpine Tech across all four production repositories. It enforces:

1. **NZ Privacy Act 2020** — Information Privacy Principles (IPPs 1-11) + sensitive data protection
2. **Te Mana Raraunga** — Māori data sovereignty (OCAP® principles: Ownership, Control, Access, Possession)
3. **MBIE Responsible AI** — Safety-by-design, explainability, HITL gates, fairness
4. **SOC 2 Type II Controls** — Enterprise-grade security, availability, confidentiality (audit logging, access control, encryption)
5. **Algorithm Charter for Aotearoa** — Transparent automated decision-making with human appeal pathways

---

## Implementation Across Four Repos

### Phase 1: Establish Governance (Week 1)

**In each repo (Weaver, Core, Stack, Aether):**

```bash
# 1. Create COMPLIANCE.md (repo root)
# 2. Create .github/compliance/ directory
# 3. Copy skill to repo for offline reference
# 4. Update GOVERNANCE.md to reference this skill
```

**Action Items:**

- [ ] Create `COMPLIANCE.md` in each repo (see template below)
- [ ] Establish Compliance Officer role (or designate)
- [ ] Schedule monthly compliance reviews (calendar sync)
- [ ] Create `#compliance` Slack channel for alerts + discussions

---

### Phase 2: Harden Technical Controls (Week 2-4)

**Access Control & Authentication:**
- [ ] Enable MFA for all GitHub accounts (required)
- [ ] Configure RBAC in production (viewer/editor/admin/auditor roles)
- [ ] Implement short-lived service account credentials (max 1 hour)
- [ ] Rotate API keys every 90 days (automate)
- [ ] Review SSH keys; rotate annual

**Encryption & Secrets:**
- [ ] Deploy HashiCorp Vault or AWS Secrets Manager
- [ ] Migrate all hardcoded secrets to vault
- [ ] Enable database encryption at rest (AES-256)
- [ ] Enforce TLS 1.3+ for all APIs
- [ ] Automated secret rotation pipeline

**Audit Logging & Monitoring:**
- [ ] Centralize logs (ELK / Splunk / CloudWatch)
- [ ] Enable immutable audit logs (18-month retention)
- [ ] Configure automated alerts (failed login, unauthorized access, DDoS)
- [ ] Deploy SIEM for security monitoring
- [ ] Create compliance dashboard (uptime, security events, access patterns)

**Backup & Disaster Recovery:**
- [ ] Verify daily backups (hourly for critical systems)
- [ ] Test monthly restore (from production backup)
- [ ] Document RTO/RPO targets (≤4 hours RTO, ≤1 hour RPO)
- [ ] Implement immutable backups (prevent ransomware deletion)
- [ ] Multi-region backup replication (optional but recommended)

---

### Phase 3: Privacy Act Compliance (Week 2-4)

**Data Inventory & Classification:**
- [ ] Catalog all personal data systems (ROPA — Record of Processing Activity)
- [ ] Classify by sensitivity (Level 1: public, Level 2: personal, Level 3: health/sensitive)
- [ ] Document retention periods (health data: 7 years max)
- [ ] Map data flows (collection → storage → use → disclosure → deletion)

**User Rights Workflows:**
- [ ] Implement Data Subject Access Request (DSAR) portal
- [ ] SLA: Respond within 20 working days (automated)
- [ ] Export data in CSV/JSON (human-readable format)
- [ ] Implement data deletion workflow (verifiable, not just soft-delete)
- [ ] Implement data correction workflow

**Third-Party Management:**
- [ ] Audit all vendors/processors (who accesses data?)
- [ ] Sign Data Processing Agreements (DPAs) with all third parties
- [ ] Document subprocessors (published list, updated quarterly)
- [ ] Log all third-party data access
- [ ] Establish vendor compliance review process (annual audit)

---

### Phase 4: Te Mana Raraunga (Māori Data Sovereignty) (Week 3-6)

**Community Engagement (HITL Gate Required):**
- [ ] Identify all iwi/hapū/whānau whose data is held
- [ ] Establish Cultural Advisory Board (monthly meetings minimum)
- [ ] Develop data use agreements (signed by iwi + organization leadership)
- [ ] Document community benefit-sharing (what does iwi gain?)

**Technical Implementation:**
- [ ] Implement data localization (all Māori data in Aotearoa, encrypted)
- [ ] Dual-key encryption: iwi + organization hold keys (threshold cryptography option)
- [ ] Cultural data classification system (Level 1: public, Level 2: community, Level 3: sacred)
- [ ] Annual community hui (gathering) to review data uses + outcomes

---

### Phase 5: Incident Response & Testing (Week 5-8)

**Documentation:**
- [ ] Create incident response plan (stored in repo)
- [ ] Define P0/P1/P2/P3 severity + SLAs
- [ ] Draft Privacy Commissioner notification template (legal review required)
- [ ] Draft individual notification template (72-hour SLA)
- [ ] Establish breach register (log all incidents, 7+ year retention)

**Testing & Drills:**
- [ ] Tabletop exercise (quarterly): simulate data breach response
- [ ] Backup restoration test (monthly): verify RTO/RPO
- [ ] Penetration testing (annual, external auditor)
- [ ] Incident response drill (quarterly, rotate roles)

---

### Phase 6: Audit Preparation (Week 9-12)

**External Audit:**
- [ ] Engage external SOC 2 auditor (AICPA-qualified)
- [ ] Provide all documentation + evidence
- [ ] Walk through all controls (interviews + walkthroughs)
- [ ] Auditor issues report + opinion (standard SLA: ~3 months)
- [ ] Address any audit findings (remediation plan)

**Continuous Monitoring:**
- [ ] Monthly compliance reviews (checklist in `COMPLIANCE_AUDIT_CHECKLIST.md`)
- [ ] Quarterly access reviews + recertification
- [ ] Annual security training (all staff)
- [ ] Bi-annual penetration testing (optional but recommended)

---

## COMPLIANCE.md Template (for each repo)

Create this file in each repo root (`Weaver/COMPLIANCE.md`, `Core/COMPLIANCE.md`, etc.):

```markdown
# Compliance — NZ AI + SOC 2 Type II

This repository is governed by the **NZ AI Compliance + SOC 2 Type II** framework.

## Compliance Contacts

| Role | Name | Email | On-Call |
|------|------|-------|---------|
| Compliance Officer | [Name] | [Email] | [Schedule] |
| Privacy Officer | [Name] | [Email] | Emergency only |
| CISO / Security Lead | [Name] | [Email] | [Schedule] |
| Cultural Advisor | [Name] | [Email] | [Schedule] |

## Relevant Policies & Documents

- [NZ Privacy Act 2020 Mapping](../../skills/nz-ai-compliance-soc2/references/NZ_PRIVACY_ACT_2020_MAPPING.md)
- [SOC 2 Control Matrix](../../skills/nz-ai-compliance-soc2/references/SOC2_CONTROL_MATRIX.md)
- [Te Mana Raraunga Principles](../../skills/nz-ai-compliance-soc2/references/TE_MANA_RARAUNGA_PRINCIPLES.md)
- [Incident Response Playbook](../../skills/nz-ai-compliance-soc2/references/INCIDENT_RESPONSE_PLAYBOOK.md)
- [Compliance Audit Checklist](../../skills/nz-ai-compliance-soc2/references/COMPLIANCE_AUDIT_CHECKLIST.md)

## Data Classification

This system processes data classified as:

| Level | Examples | Protection |
|-------|----------|-----------|
| **Level 1 (Public)** | General health tips, announcements | Standard security |
| **Level 2 (Restricted)** | Personal health info, appointment dates | Encryption at rest/transit + RBAC |
| **Level 3 (Sensitive)** | Genetic data, mental health, cultural knowledge | Dual-key encryption + iwi oversight |

## Compliance Milestones

- [ ] Phase 1: Governance established (Week 1)
- [ ] Phase 2: Technical controls hardened (Week 4)
- [ ] Phase 3: Privacy Act compliance (Week 4)
- [ ] Phase 4: Te Mana Raraunga implementation (Week 6)
- [ ] Phase 5: Incident response tested (Week 8)
- [ ] Phase 6: Audit-ready (Week 12)

## Monthly Compliance Checklist

Every month, Compliance Officer reviews:

- [ ] All access logs reviewed (no suspicious patterns)
- [ ] Incident register updated
- [ ] Backup restoration test passed
- [ ] No unresolved security alerts
- [ ] Third-party DPA status current
- [ ] Māori data access appropriate (if applicable)
- [ ] Cultural Advisory Board meeting held (if applicable)

## Incident Reporting

**Report to:** privacy@[organization].nz (email) or #compliance Slack

**SLA:**
- P0 (Critical): Response within 15 min
- P1 (High): Response within 1 hour
- P2 (Medium): Response within 4 hours
- P3 (Low): Response within 1 business day

## Related Documentation

- [Governance Standards](./GOVERNANCE.md)
- [Security Policy](.github/SECURITY.md)
- [Privacy Notice](./PRIVACY.md)
```

---

## Integration with CAT Standards

This compliance skill is aligned with CAT Architectural Standards:

**DIAMOND (Primary):**
- Implements enterprise-grade security (encryption, audit logging, access controls)
- Enforces production-readiness + compliance from day one
- Integrates IaC for compliance infrastructure

**PLATINUM (Secondary):**
- Compliance posture as data flywheel (learn from incidents → improve guardrails)
- Bias detection + algorithmic drift monitoring
- Continuous improvement of risk thresholds

**GOLD (Tertiary):**
- Linear compliance audit workflow (Discovery → Design → Development → Testing → Deployment)
- Transparent approval gates + HITL decision-making
- Clear documentation of compliance decisions

---

## Common Questions

### Q: How do I report a security incident?

**A:** Contact Privacy Officer immediately:
- Phone: [on-call number]
- Email: privacy@[org].nz
- Slack: #compliance (ping @privacy-officer)

SLA: Response within 15 min (P0), 1 hour (P1)

### Q: How do I get approval to process Māori health data?

**A:** 
1. Submit data use case to Compliance Officer
2. Compliance Officer escalates to Cultural Advisory Board
3. CAB reviews (requires iwi + kaumātua approval)
4. If approved: sign data use agreement + implement controls
5. Ongoing: monthly oversight + annual community hui

### Q: What if I find a hardcoded credential in code?

**A:**
1. Do NOT commit it to main branch
2. Notify Security Lead immediately
3. Move to Vault (HashiCorp Vault / AWS Secrets Manager)
4. Rotate the credential (assume compromise)
5. Document incident + remediation

### Q: When is the next external audit?

**A:** Contact Compliance Officer. Standard frequency: annual for SOC 2 Type II.

### Q: How long do we keep logs?

**A:** Audit logs: 18 months minimum (SOC 2 requirement)  
Health data: 7 years maximum (NZ Health Privacy Code)  
Incident register: 7+ years (Privacy Commissioner guidance)

---

## Escalation Contacts

| Scenario | Contact | Priority |
|----------|---------|----------|
| Data breach (confirmed) | Privacy Officer + CEO | IMMEDIATE |
| Unauthorized access attempt | Security Lead + Compliance Officer | WITHIN 1 HOUR |
| Potential policy violation | Compliance Officer | WITHIN 1 DAY |
| Audit finding (pre-audit) | Compliance Officer + CISO | WITHIN 1 WEEK |
| New data use request | Compliance Officer + CAB | WITHIN 1 MONTH |

---

## References

- **NZ Privacy Commissioner:** https://www.privacy.org.nz/
- **MBIE Responsible AI:** https://www.mbie.govt.nz/dmsdocument/19433
- **Te Mana Raraunga:** https://www.temanararaunga.maori.nz/
- **AICPA SOC 2:** https://www.aicpa.org/interestareas/informationsystems/audit-attest/aicpa-soc-2-report
- **NZ Health Information Privacy Code:** https://www.privacy.org.nz/your-rights/codes-of-practice/health-information-privacy-code/
```

---

## Deployment to Repos

**For each of Weaver, Core, Stack, Aether:**

1. Create `.github/compliance/` directory
2. Add `COMPLIANCE.md` to repo root
3. Update `GOVERNANCE.md` to reference this skill
4. Create `.github/workflows/compliance-audit.yml` (monthly automated audit)
5. Add compliance labels to all PRs (mark as "compliance-related" if touching sensitive data)

---

## Monthly Cadence (Recurring Task)

```
EVERY MONTH:
  - Review audit logs (no suspicious patterns)
  - Run compliance checklist (mark items ✓)
  - Update compliance status dashboard
  - Brief leadership on compliance status
  - Identify any needed remediation
```

---

## Success Criteria (6 Months)

- ✓ External SOC 2 Type II audit passed (auditor opinion issued)
- ✓ Privacy Commissioner has confidence in controls (zero breaches)
- ✓ Cultural Advisory Board gives approval (Māori data sovereignty respected)
- ✓ Zero critical compliance findings
- ✓ Incident response tested + SLAs consistently met
- ✓ All staff trained on compliance (100% completion)

