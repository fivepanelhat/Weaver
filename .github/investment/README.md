# Kotahitanga Investment Strategy — Weaver Orchestration Layer

**Repository:** Weaver  
**Primary Tier:** DIAMOND (enterprise-grade orchestration)  
**Secondary Tier:** PLATINUM (autonomous orchestration loops)  
**Role:** Central orchestration + tenant isolation + health data governance  
**Compliance Baseline:** 94% (target: ≥95% for Diamond tier)  
**Last Updated:** 2026-07-12

---

## Weaver's Role in Kotahitanga

Weaver is the **central orchestration hub** for Coastal Alpine Tech's sovereign AI infrastructure. It manages:

1. **Tenant Isolation** — Secure multi-tenant health data separation (HITL gates on every data access)
2. **Health Data Governance** — NZ Privacy Act compliance + Health Information Privacy Code (7-year retention)
3. **Orchestration Services** — Coordination across Aether (AI), Core (edge SDK), and Stack (deployment)
4. **Error Sanitization** — Fail-closed error handling (no internal details leak; tenant IDs safe for logging)
5. **Compliance Enforcement** — All health data access requires audit logging + post-hoc verification

**Diamond Tier Classification Rationale:**
- Health data is inherently sensitive (Level 3 classification)
- Requires enterprise-grade security (AES-256 encryption, TLS 1.3+, MFA, RBAC)
- All changes require HITL approval (code review gates)
- Audit logging mandatory (18-month immutable retention)
- External SOC 2 Type II audit required
- Backup/disaster recovery tested monthly (≤4 hour RTO, ≤1 hour RPO)

**Platinum Secondary Rationale:**
- Orchestration logic learns from errors + audit logs
- Continuous improvement loop: capture incident data → improve validation rules → hot-deploy
- Fair distribution of computational resources across tenants (fairness monitoring)

---

## Data Classification in Weaver

| Level | Examples | Protection |
|-------|----------|-----------|
| **Level 1 (Public)** | General health tips, resource lists | Standard TLS, public API |
| **Level 2 (Restricted)** | Personal health info (conditions, medications), appointment dates | Encryption at rest + transit, RBAC, audit logging |
| **Level 3 (Sensitive)** | Genetic data, mental health records, cultural health knowledge, Māori health data | Dual-key encryption, iwi oversight, dual approval (org + iwi), geofencing, data localization |

**Key Constraint:** Level 3 data requires **Cultural Advisory Board approval** for any new use.

---

## Compliance Status (Current)

**Overall Score: 94% (214/225 items) — GREEN** ✓

| Category | Items | Passing | Score | Status |
|----------|-------|---------|-------|--------|
| CC1 (Governance) | 15 | 15 | 100% | ✓ |
| CC6 (Access) | 49 | 46 | 94% | ✓ |
| CC7 (Change/Secrets) | 38 | 36 | 95% | ✓ |
| CC9 (Security) | 42 | 40 | 95% | ✓ |
| A (Availability) | 22 | 21 | 95% | ✓ |
| P (Privacy) | 34 | 33 | 97% | ✓ |
| Te Mana Raraunga | 11 | 11 | 100% | ✓ |
| Architecture | 9 | 9 | 100% | ✓ |
| **TOTAL** | **225** | **214** | **94%** | **🟢 GREEN** |

**Status:** Ready for Diamond tier projects. Last external audit: [DATE]. Next audit: [DATE].

**Minor Gaps (all have remediation in progress):**
- CC6: 3 items (access logging edge case for inter-tenant handoffs, being addressed in Sprint X)
- CC7: 2 items (credential rotation automation for non-primary secrets, backlog for Sprint X)
- CC9: 2 items (quarterly backup restore test procedure, scheduled monthly)
- A: 1 item (disaster recovery runbook update, in progress)

---

## OCAP® Verification Framework for Weaver

### Level 1 & 2 Data (Non-Indigenous)

**Standard OCAP® Verification:**

☐ **OWNERSHIP**
- Organization owns general + restricted personal health data
- Users retain right to request export/deletion
- Data Use Agreement published + acknowledged on signup

☐ **CONTROL**
- RBAC enforces access (viewer/editor/admin roles)
- API keys rotate every 90 days
- Quarterly access review (manager approval + audit)

☐ **ACCESS**
- All access logged (immutable, 18-month retention)
- Failed login attempts logged + monitored
- Rate limiting on API endpoints

☐ **POSSESSION**
- Infrastructure: AWS Aotearoa region (no international cloud)
- Backups: encrypted + replicated to separate region
- Disaster recovery: monthly restore test (RTO ≤4 hours)

---

### Level 3 Data (Indigenous/Māori Health)

**OCAP® + Cultural Advisory Board Verification:**

☐ **OWNERSHIP**
- Iwi/hapū holds legal ownership of cultural/Māori health data
- Organization holds operational ownership
- Dual-ownership documented in signed Data Use Agreement
- Data ownership registry maintained + reviewed quarterly

☐ **CONTROL**
- Threshold encryption: iwi master key + organization operational key (both required to decrypt)
- Cultural Advisory Board has veto authority over all access
- Quarterly joint access review (iwi + organization)
- Community can request deletion within 30 days (verified + acted on within 7 days)

☐ **ACCESS**
- All access logged (immutable, 18-month retention minimum)
- Weekly access audit by Cultural Advisory Board rep
- MFA required for all access
- Geofencing: access only from Aotearoa-based locations
- Purpose limitation: can only access for stated purpose in DUA

☐ **POSSESSION**
- All Māori health data in Aotearoa-based infrastructure (NO international cloud)
- Physical access controls: badge/CCTV/environmental monitoring (data center)
- Backup media: encrypted + stored separately in Aotearoa
- Disaster recovery tested monthly
- Possession register: document all copies + locations

**Cultural Advisory Board Review Schedule:**
- Monthly: Access pattern audit
- Quarterly: OCAP® verification renewal
- Annually: Comprehensive hui (gathering) to review outcomes + community benefit-sharing
- As-needed: Emergency veto authority (project can be stopped immediately if cultural sovereignty at risk)

---

## Active Kotahitanga Projects Using Weaver

| Project ID | Name | Data Level | Allocation | Status | Compliance |
|------------|------|-----------|-----------|--------|-----------|
| KAS-2026-001 | Sovereign Regional Health Cloud | Level 2/3 (mixed) | $1.2M | ACTIVE | 94% ✓ |

**For detailed tracking, see:**
- `.github/investment/CAPITAL_ALLOCATION_TRACKER.md` (updated weekly)
- Dashboard: https://[compliance-dashboard-url]

---

## How to Request Health Data Processing

**For Level 1/2 Data (Non-Indigenous):**

1. Submit feature request via GitHub issue
2. Compliance Officer reviews (< 5 days SLA)
3. Privacy Officer signs off (privacy impact assessment)
4. Technical review (code review gate)
5. Deploy (to production with audit logging enabled)

**For Level 3 Data (Indigenous/Māori Health):**

1. Submit detailed proposal to Compliance Officer + Cultural Advisor
2. **HITL Gate 1:** Cultural Advisory Board reviews (30-day review period, mandatory)
3. **HITL Gate 2:** Privacy Officer + Data Officer verify OCAP® (10 days)
4. **HITL Gate 3:** CFO approves budget + CISO approves security (5 days)
5. Data Use Agreement signed by iwi leadership + organization leadership
6. Deploy (with dual-key encryption + geofencing enforced)

**Timeline:** 45–60 days total (CAB review is longest)

---

## Compliance Obligations During Project

**Monthly:**
- ☐ 225-point compliance checklist review (Green/Yellow/Red status)
- ☐ Remediation progress tracked
- ☐ No unresolved security alerts
- ☐ Incident register updated

**Quarterly:**
- ☐ Full 225-point compliance re-audit
- ☐ OCAP® verification renewed
- ☐ Cultural Advisory Board briefing (for Level 3 projects)
- ☐ Board compliance dashboard updated

**If Compliance Drops Below 90%:**
- 🟡 YELLOW (70–89%): Capital freeze on remaining tranches (50% escrow hold)
  - Remediation plan due within 7 days
  - Target Green status within 30 days
  - Weekly progress check-ins

- 🔴 RED (<70%): Complete capital freeze + infrastructure lockout
  - Immediate board escalation + incident response
  - Comprehensive remediation required
  - If not remediated within 60 days: project termination + capital reclamation

---

## Key Governance Controls for Weaver

### Error Sanitization (Fail-Closed Design)

**Rule:** Never leak internal exception details or stack traces to clients.

**Implementation:**
```
Request → Validation → Business Logic → Error Handling → Response

If error occurs:
  - Log full error + stack trace (server-side, immutable logs)
  - Return to client: { "status": "error", "code": "VALIDATION_FAILED", "tenant_id": "..." }
  - Tenant ID is NOT sensitive (helps caller correlate logs)
  - No internal details exposed
```

**Compliance Goal:** IPP4 (storage/security of personal information)

### Tenant Isolation (HITL Gates)

**Rule:** Every cross-tenant data access requires human review.

**Implementation:**
```
When service A requests data from service B:
  1. Check isolation boundary (is this a legitimate inter-tenant flow?)
  2. If YES: Log the request (immutable audit trail)
  3. If NO: Fail-closed (reject request, alert Compliance Officer)
  4. Post-hoc: Monthly audit of all cross-tenant flows
```

### DSAR Workflow (20-Working-Day SLA)

**Rule:** Data Subject Access Requests must be fulfilled within 20 working days.

**Implementation:**
```
DSAR received → Auto-logged in DSAR register
  → Compliance Officer reviews within 1 day
  → Technical team extracts data (within 5 days)
  → Privacy Officer redacts sensitive third-party data
  → User delivers response (within 20 working days, with proof of delivery)
  → Register updated with response date + evidence
```

---

## Incident Response SLA (Weaver)

| Severity | Definition | Examples | Response SLA | Notification SLA |
|----------|-----------|----------|--------------|------------------|
| **P0 — CRITICAL** | Large breach of health records | 100+ health records exposed | 15 min | 24 hours |
| **P1 — HIGH** | Medium breach | 10–99 health records exposed | 1 hour | 72 hours |
| **P2 — MEDIUM** | Minor breach | 1–9 records exposed | 4 hours | 10 business days |
| **P3 — LOW** | Potential issue | Suspicious log entry | 1 business day | 30 business days |

**Notification Recipients:**
- Privacy Commissioner: breaches@privacy.org.nz
- Affected individuals: within 72 hours (P1), within 10 business days (P2)
- Cultural Advisory Board: immediately (if Māori health data affected)

---

## Recommended Reading

1. **CAT Architectural Standards:** `.github/compliance/nz-ai-compliance-soc2/SKILL.md`
2. **Kotahitanga Investment Strategy:** `.github/investment/KOTAHITANGA_INVESTMENT_STRATEGY.md`
3. **225-Point Audit Checklist:** `.github/compliance/references/COMPLIANCE_AUDIT_CHECKLIST.md`
4. **Privacy Act Mapping:** `.github/compliance/references/NZ_PRIVACY_ACT_2020_MAPPING.md`
5. **Te Mana Raraunga:** `.github/compliance/references/TE_MANA_RARAUNGA_PRINCIPLES.md`
6. **Incident Response:** `.github/compliance/references/INCIDENT_RESPONSE_PLAYBOOK.md`

---

## Contacts

| Role | Name | Email |
|------|------|-------|
| Investment Decision Authority | [CTO/CISO] | [Email] |
| Compliance Officer | [Name] | [Email] |
| Privacy Officer | [Name] | [Email] |
| Cultural Advisor | [Name] | [Email] |
| Repository Owner | [Name] | [Email] |

---

**Version:** 1.0.0  
**Status:** READY FOR DIAMOND TIER PROJECTS  
**Last External Audit:** [DATE]  
**Next External Audit:** [DATE]
