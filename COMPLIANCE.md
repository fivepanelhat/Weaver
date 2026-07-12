# Compliance — NZ AI + SOC 2 Type II

This repository is governed by the **NZ AI Compliance + SOC 2 Type II** framework.  
**Classification:** Diamond (primary) | Platinum (secondary) | Gold (tertiary)  
**HITL Gate:** Required for all compliance decisions + data sovereignty matters

---

## Purpose

Weaver is the **orchestration layer** for Coastal Alpine Tech's autonomous GitOps + multi-tenant LLM workflows. It handles:
- Tenant configuration + isolation
- LLM agentic processes + security guardrails
- Error sanitization + sensitive output masking
- Orchestration of Coastal Alpine Core SDK

**Compliance Impact:** HIGH
- Processes health data (requires Health Privacy Code compliance)
- Implements HITL gates (requires audit trail + approval logging)
- Multi-tenant isolation (requires access control + data segregation)

---

## Compliance Contacts

| Role | Contact |
|------|---------|
| Compliance Officer | [ASSIGN] |
| Privacy Officer | [ASSIGN] |
| CISO / Security Lead | [ASSIGN] |
| Cultural Advisor | [ASSIGN] |

---

## Data Inventory

| Data Type | Sensitivity | Retention | Protection |
|-----------|-------------|-----------|------------|
| Tenant configuration | Level 2 | Until deletion | Encryption + RBAC |
| Health-related LLM inputs | Level 3 | Per policy | Encryption + audit log |
| Appointment/care data | Level 3 | 7 years max | Encryption + access control |
| API logs + error messages | Level 2 | 18 months | Immutable, centralized |

---

## Compliance Status (Track Progress)

- [ ] Phase 1: Governance established (Week 1)
- [ ] Phase 2: Technical controls hardened (Week 4)
- [ ] Phase 3: Privacy Act compliance (Week 4)
- [ ] Phase 4: Te Mana Raraunga implementation (Week 6)
- [ ] Phase 5: Incident response tested (Week 8)
- [ ] Phase 6: SOC 2 audit ready (Week 12)

---

## Incident Reporting

**Email:** privacy@coastalalp.tech  
**Slack:** #compliance  
**Phone:** [On-call number]

**SLA:** P0 (15 min), P1 (1 hour), P2 (4 hours), P3 (1 day)

---

## Monthly Compliance Checklist

- [ ] Audit logs reviewed (no suspicious patterns)
- [ ] Incident register updated
- [ ] Backup restore test passed
- [ ] No unresolved P0/P1 alerts
- [ ] Third-party DPAs current
- [ ] Tenant isolation verified
- [ ] HITL audit trail complete
- [ ] Error messages sanitized
- [ ] Health data encrypted

**Sign-Off:** Compliance Officer: _________________ Date: _________

---

**Related:** [NZ AI Compliance Skill](./.github/compliance/nz-ai-compliance-soc2/)  
**Last Updated:** 2026-07-12
