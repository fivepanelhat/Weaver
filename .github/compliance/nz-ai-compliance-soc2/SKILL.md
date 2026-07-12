---
name: nz-ai-compliance-soc2
version: "1.0.0"
type: compliance-governance
requires_hitl: true
description: New Zealand AI Compliance + SOC 2 Type II framework for Coastal Alpine Tech stack. Enforces Privacy Act 2020 (IPPs), Te Mana Raraunga data sovereignty, MBIE Responsible AI, Algorithm Charter for Aotearoa, and SOC 2 Type II controls (audit logging, access controls, data retention, breach detection). Mandatory for all Weaver, Core, Stack, and Aether production deployments.
status: active
owner: Coastal Alpine Tech Compliance
last_updated: "2026-07-12"
---

# NZ AI Compliance + SOC 2 Type II Framework

Lead Sovereign AI Compliance Auditor for New Zealand (Aotearoa). This skill evaluates AI architectures, data flows, and autonomous agent deployments against formal NZ regulatory and SOC 2 frameworks.

## Core Compliance Pillars

### 1. Privacy Act 2020 (Information Privacy Principles)

**IPP 1: Collection Purpose** — Data collected only for stated, lawful purpose  
**IPP 2: Source** — Information about source must be provided where practicable  
**IPP 3: Collection Manner** — Collection must be fair and lawful  
**IPP 4: Storage & Security** — Must be held securely; accessible only to authorized personnel  
**IPP 5/6: Access & Correction** — Individuals can access and correct personal information  
**IPP 8: Accuracy** — Information must be accurate, up-to-date, complete  
**IPP 10/11: Use/Disclosure Limits** — Information may only be used/disclosed for collection purpose or related purpose  

**Guardrails:**
- No personal data transmitted to public LLM endpoints (critical IPP4 breach)
- All health data (PHI) encrypted at rest + in transit (mandatory)
- Data subject access requests processed within 20 working days (mandatory)
- Retention: Delete health data after 7 years (NZ Health Information Privacy Code)

### 2. Te Mana Raraunga (Māori Data Sovereignty)

**Ownership Principle:** Māori data belongs to Māori collective; organizations are stewards, not owners.  
**Control Principle:** Māori community exercises authority over data collection, use, access.  
**Possession Principle:** Physical + logical control remains localized.

**Guardrails:**
- No Māori cultural data silently exported to cloud vendors
- Iwi + hapū must be notified of any health/welfare data uses
- Explicit consent (tika data governance) required before processing
- Local-first processing; no foreign data residency for sensitive collections

### 3. MBIE Responsible AI Guidance

**Safety-by-Design:** AI systems must be designed with security + transparency from the start.  
**Explainability:** Agent decisions must be auditable and explainable (no black-box deployments).  
**Human-in-the-Loop:** High-risk decisions require human approval before execution.  
**Fairness:** Bias detection + mitigation required; algorithmic discrimination prohibited.

**Guardrails:**
- All agent actions logged + auditable (immutable audit trail)
- High-risk operations (refunds, access grants, health recommendations) require HITL approval
- Bias scoring on classifier outputs monthly (detect model drift)
- Explainability threshold: agents must cite data sources for recommendations

### 4. Public Service Algorithm Charter for Aotearoa

**Transparency:** All public-facing algorithmic decisions must be explainable to affected parties.  
**Accountability:** Clear responsibility chain; no "algorithm decided it" excuses.  
**Fairness & Non-Discrimination:** Protected characteristics (race, ethnicity, disability, gender) must not drive decisions.  
**Consent & Appeal:** Automated decisions can be appealed; human review always available.

**Guardrails:**
- Algorithm impact assessments (AIA) for any government/public sector work
- Public sector deployments: explainability score ≥ 0.85 (LIME/SHAP analysis)
- Appeal pathway: users can request human review within 30 days
- Decision provenance: store input features, model version, inference timestamp

### 5. Consumer Protection & Competition

**Fair Trading Act 1986:** Prohibits misleading conduct; AI hallucinations = liability.  
**Commerce Act:** Algorithmic collusion is illegal; competitors cannot coordinate pricing via AI.

**Guardrails:**
- LLM output validation: flag hallucinations (fact-check against authoritative sources)
- Price recommendations logged + auditable (detect collusion signals)
- Disclosure: inform consumers when AI-assisted recommendations are provided

---

## SOC 2 Type II Controls

### CC6: Logical & Physical Access Controls

**Implementation:**
- RBAC (role-based access control) for all APIs + dashboards
- MFA (multi-factor authentication) for all admin actions
- API key rotation: every 90 days (max)
- SSH key audit: monthly verification of authorized keys
- VPC isolation: all production services run in private subnets

**Audit Trail:**
- Log all access attempts (success + failure)
- Retain audit logs for 18 months (SOC 2 requirement)
- Alert on suspicious patterns (e.g., 5+ failed logins in 5 min)

### CC7: Restricted Access to Assets

**Implementation:**
- Principle of least privilege: no default admin access
- Service accounts: short-lived credentials (max 1 hour expiry)
- Secrets management: HashiCorp Vault or AWS Secrets Manager (encrypted)
- No hardcoded credentials in code (static analysis enforced)

**Audit Trail:**
- Log all secrets access (who, when, what, success/failure)
- Alert on unauthorized secrets reads

### A1: Availability

**Implementation:**
- No single point of failure: all services replicated
- RTO (Recovery Time Objective): ≤ 4 hours
- RPO (Recovery Point Objective): ≤ 1 hour
- Blue-green deployments: zero-downtime updates

**Monitoring:**
- Uptime SLO: 99.5% (monthly target)
- Automated failover: trigger within 5 minutes
- Status page: public transparency on incidents

### S1/S2: Security

**Implementation:**
- Encryption at rest: AES-256 for all databases
- Encryption in transit: TLS 1.3+ for all connections
- DDoS protection: AWS Shield / Cloudflare WAF
- Vulnerability scanning: weekly on all container images
- Penetration testing: quarterly (external auditor)

**Audit Trail:**
- Log all encryption key operations (creation, rotation, deletion)
- Alert on weak cipher suite use

---

## Compliance Audit Protocol

**Execution Workflow (Linear/Gold):**

1. **Discovery Phase** → Collect system architecture, data flows, API endpoints
2. **Risk Assessment Phase** → Map against Privacy Act IPPs + SOC 2 controls
3. **Gap Analysis Phase** → Identify non-compliance, list remediation actions
4. **Remediation Phase** → Implement fixes with HITL approval gates
5. **Verification Phase** → Audit checks confirm compliance
6. **Sign-Off Phase** → Governance review + legal sign-off

**Decision Tree:**

```
Does the system handle PHI (health data)?
├─ YES → IPP4 (storage/security) + NZ Health Code mandatory
│         Require: encryption at rest/transit + local processing
├─ NO → Continue to next question
│
Does the system use Māori/Iwi data?
├─ YES → Te Mana Raraunga + explicit consent mandatory
│         Require: iwi notification + local-first processing
├─ NO → Continue to next question
│
Does the system make automated decisions affecting users?
├─ YES → MBIE Responsible AI + HITL approval mandatory
│         Require: explainability score ≥ 0.85 + audit trail
├─ NO → Continue to next question
│
Does the system interface with public sector / government?
├─ YES → Algorithm Charter mandatory
│         Require: algorithmic impact assessment + appeal pathway
├─ NO → Standard SOC 2 Type II controls apply
```

---

## Hardening Checklist (SOC 2 Type II Readiness)

### Authentication & Access (CC6/CC7)

- [ ] RBAC implemented for all APIs
- [ ] MFA enforced for admin console access
- [ ] Service accounts use short-lived credentials (≤1 hour)
- [ ] Secrets rotation: every 90 days
- [ ] SSH keys audited: monthly
- [ ] Unauthorized access alerts configured
- [ ] Access logs: 18-month retention

### Data Protection (S1/S2)

- [ ] AES-256 encryption at rest (all databases)
- [ ] TLS 1.3+ for all connections
- [ ] No hardcoded credentials in code (static scan passing)
- [ ] Secrets stored in Vault / Secrets Manager
- [ ] Regular vulnerability scans (weekly, all images)
- [ ] Quarterly penetration testing scheduled

### Privacy Act Compliance

- [ ] IPP1: Collection purpose documented (ROPA - Record of Processing Activity)
- [ ] IPP3: Fair collection practices verified
- [ ] IPP4: Storage security audit completed
- [ ] IPP5: Data subject access workflow implemented
- [ ] IPP8: Data accuracy checks scheduled (quarterly)
- [ ] IPP10/11: Use/disclosure logging enabled

### Te Mana Raraunga Compliance

- [ ] Iwi/Hapū notification protocol documented
- [ ] Consent capture mechanism in place
- [ ] Local-first processing verified (no silent cloud export)
- [ ] Cultural data masking rules enforced
- [ ] Whakapapa/genealogy data encryption verified

### Incident Response

- [ ] Incident response plan documented + drilled
- [ ] Breach notification SLA: ≤72 hours (Privacy Commissioner)
- [ ] Audit logs immutable + centralized
- [ ] Automated alerts configured for suspicious events
- [ ] Forensic analysis capability (log retention ≥18 months)

---

## Integration with CAT Standards

**DIAMOND Alignment:**
- Enforces production-ready security + observability
- Implements IaC (compliance infrastructure as code)
- Blue-green deployments with zero-downtime updates
- Multi-layered security (VPC, WAF, encryption, RBAC)

**PLATINUM Alignment:**
- Compliance posture monitoring as a data flywheel
- Learn from compliance events → improve guardrails
- Bias scoring + model drift detection loops
- Continuous fine-tuning of risk thresholds

**GOLD Alignment:**
- Linear compliance audit workflow with phase gates
- Transparent decision documentation
- Human-in-the-loop approval for all remediation

---

## Anti-Patterns to Avoid

- Treating compliance as "tick-box exercise" without real security investment
- Storing sensitive data in unencrypted cloud buckets (IPP4 critical breach)
- Deploying government systems without explainability testing
- Silently exporting Māori data without iwi consent (sovereignty violation)
- Logging compliance events but never analyzing them (data flywheel blocked)
- Skipping HITL gates for high-risk automated decisions

---

## Reference Documents

- `references/NZ_PRIVACY_ACT_2020_MAPPING.md` — Full IPP mapping + remediation
- `references/SOC2_CONTROL_MATRIX.md` — SOC 2 Type II control families + implementation
- `references/TE_MANA_RARAUNGA_PRINCIPLES.md` — Māori data sovereignty framework
- `references/INCIDENT_RESPONSE_PLAYBOOK.md` — Breach detection + notification SLAs
- `references/COMPLIANCE_AUDIT_CHECKLIST.md` — Pre-audit readiness verification
