# SOC 2 Type II Control Matrix

**Framework:** AICPA Trust Services Criteria (2024 Edition)  
**Attestation Type:** Type II (operating effectiveness over time, min 6-month observation period)  
**Audit Cycle:** Annual external audit (recommended)

---

## Trust Services Criteria Overview

| Criterion | Scope | SOC 2 Type I | SOC 2 Type II |
|-----------|-------|-------------|--------------|
| **CC (Common Criteria)** | Organization-wide controls | ✓ | ✓ |
| **A (Availability)** | System uptime + performance | Optional | ✓ |
| **S (Security)** | Data confidentiality + integrity | ✓ | ✓ |
| **C (Confidentiality)** | Non-public data access restrictions | Optional | Optional |
| **P (Privacy)** | Personal data handling (new 2024) | Optional | ✓ |

---

## CC: Common Criteria (Organization-Wide)

### CC1: General Controls Environment

**Control Objective:** Establish accountability + responsibility for controls.

**Implementation:**

```yaml
CC1.1 Governance Structure:
  - Documented organizational chart with defined roles
  - Board/leadership oversight of security + compliance
  - Compliance committee meets quarterly
  - Policies published + acknowledged by all staff

CC1.2 Ethical Conduct:
  - Code of Conduct signed by all employees
  - Confidentiality agreements in place
  - Whistleblower hotline available (anonymous)
  - Investigation process documented
```

**Evidence for Auditor:**
- Board minutes showing security discussions
- Signed code of conduct (employee acknowledgment)
- Training records (annual security awareness)

---

### CC6: Logical & Physical Access Controls

**Control Objective:** Restrict access to systems + data by role + need.

#### CC6.1 Logical Access

```yaml
Authentication:
  - MFA enforced for all administrative access
  - Password policy: min 12 characters, complexity rules
  - Session timeout: 15 min inactivity (admin), 60 min (users)
  - Account lockout: 5 failed attempts → 30 min lockout

Authorization:
  - RBAC: roles = {viewer, editor, admin, compliance-auditor}
  - Principle of least privilege: default deny, whitelist
  - Access review: quarterly verification of role assignments
  - Segregation of duties: same user cannot create + approve payment

API Authentication:
  - OAuth 2.0 / JWT tokens (not basic auth)
  - Token expiry: max 1 hour
  - Refresh tokens: max 30 days
  - API key rotation: 90 days
  - Revoked keys logged + monitored
```

#### CC6.2 Physical Access

```yaml
Data Center Security:
  - Badge access + turnstile (prevent tailgating)
  - Video surveillance (90-day retention)
  - Visitor log (manual or automated)
  - After-hours access: requires approval + logging

Server Room Access:
  - Locked cabinet / cage
  - Authorized personnel only
  - Environmental monitoring (temp, humidity, power)
  - UPS + backup generator (zero downtime)
```

**Evidence for Auditor:**
- MFA configuration screenshots
- RBAC role matrix (template + actual assignments)
- Quarterly access review sign-offs
- Physical access logs (90-day samples)
- Badge swipe reports

---

### CC7: Restricted Access to System Assets

**Control Objective:** Prevent unauthorized modification of systems + data.

```yaml
Change Management:
  - Change request process: documented, approved, tested
  - Test environment isolation: separate from production
  - Peer review: code changes reviewed by second person
  - Rollback procedure: documented, tested quarterly
  - Deployment frequency: max 2x per week (reduces risk)

Segregation of Duties:
  - Developer: cannot deploy to production
  - DevOps: cannot change access policies
  - Auditor: read-only access (cannot modify logs)
  - Conflict matrix: document incompatible roles

Secret Management:
  - Centralized vault: HashiCorp Vault / AWS Secrets Manager
  - No hardcoded credentials in code (enforced by static analysis)
  - Secret rotation: every 90 days (automated)
  - Secret access audit: log who accessed what, when
  - Principle: service account ≠ human account

Version Control:
  - All changes in Git (commits logged)
  - Branch protection: require code review + approval
  - Commit signatures: GPG / SSH (verify authenticity)
  - Deploy keys: separate from development keys

Patch Management:
  - Vulnerability scanning: weekly (all container images)
  - Patch policy: critical (0-24 hours), high (1-7 days), medium (30 days)
  - Test patches in staging before production
  - Maintain patch history (2+ year retention)
```

**Evidence for Auditor:**
- Change request log (sample: 3 months)
- Code review records (GitHub pull requests)
- Segregation of duties matrix
- Patch history (vulnerabilities remediated)
- Secret rotation audit trail

---

### CC9: Logical & Information Security

**Control Objective:** Protect against data loss, corruption, malware.

```yaml
Encryption:
  Data at Rest:
    - Database: AES-256 (Postgres native encryption)
    - Backup: S3 encryption with KMS key
    - Key rotation: 90 days (automated)
    - Key escrow: master key in separate vault
  
  Data in Transit:
    - TLS 1.3+ (minimum)
    - HSTS headers: enforce HTTPS (1 year)
    - Certificate pinning: prevent MITM attacks
    - API endpoints: all HTTPS (no fallback to HTTP)

Malware Prevention:
  - Antivirus: scans on CI/CD build step
  - Container scanning: Trivy (weekly) + clair (on deployment)
  - Static analysis: SAST (SonarQube) on all code
  - Dynamic analysis: DAST (Burp / OWASP ZAP) quarterly
  - EDR (Endpoint Detection): deployed on all admin devices

Backup & Disaster Recovery:
  - Backup frequency: daily (hourly for critical systems)
  - Retention: 30 days (hot), 1 year (cold archive)
  - RTO: ≤ 4 hours
  - RPO: ≤ 1 hour
  - DR test: quarterly (restore from backup, verify data integrity)
  - Immutable backup: prevent accidental/ransomware deletion

Incident Response:
  - IR plan documented + drilled (annual)
  - Detection: automated alerting (failed logins, DDoS, data access anomalies)
  - Response time: P1 (0-1 hour), P2 (1-4 hours), P3 (1 day)
  - Forensics: log retention 18+ months (immutable, centralized)
  - Post-incident: blameless postmortem, document lessons learned
```

**Evidence for Auditor:**
- Encryption algorithm documentation + key rotation logs
- TLS certificate chain + renewal history
- Antivirus/container scan reports (samples)
- SAST/DAST results + remediation tracking
- Backup restore test records (quarterly)
- Incident log (last 12 months) + response times
- IR plan + drill schedule

---

## A: Availability

**Control Objective:** System must be available when needed; uptime SLO ≥ 99.5%.

```yaml
Monitoring & Alerting:
  - Uptime monitoring: external (e.g., StatusPage, Pingdom)
  - Response time: alert if >1 sec (user-facing), >5 sec (backend)
  - CPU/Memory: alert at 80% usage (prevent outage)
  - Disk space: alert at 80% (prevent disk full crash)
  - Database connections: alert if >90% of max pool
  - Alert severity: P0 (page on-call immediately), P1 (email + Slack), P2 (log)

High Availability:
  - No single point of failure: all services replicated (min 3 nodes)
  - Load balancing: round-robin + health checks (remove failed nodes)
  - Database replication: primary + hot standby (automatic failover)
  - DNS failover: multi-region routing (active-active preferred)
  - Blue-green deployments: zero-downtime updates

Capacity Planning:
  - Baseline: measure CPU, memory, disk under normal load
  - Growth plan: scale infrastructure before hitting limits
  - Load testing: quarterly (simulate peak traffic)
  - Forecasting: predict resource needs 6 months ahead

Incident Response (Availability):
  - On-call rotation: 24/7 coverage (weekends + holidays)
  - Escalation path: documented + tested
  - Runbooks: step-by-step recovery procedures
  - Communication: status page updates every 30 min during incident
```

**SLO Targets:**
- Production services: 99.5% uptime monthly
- API response time: p99 < 1 sec
- Dashboard load time: p99 < 2 sec
- Data freshness: <5 min lag (reporting systems)

**Evidence for Auditor:**
- Uptime reports (monthly, with outage summaries)
- Monitoring dashboard screenshots
- Incident response times (vs. SLO target)
- Load test results
- Capacity plan (current + 12-month forecast)

---

## S: Security

**Control Objective:** Protect data confidentiality + integrity; prevent unauthorized modification.

### S1: Logical & Information System Security

(Covered in CC9 above: encryption, patch management, malware prevention)

### S2: Physical Security of Assets

(Covered in CC6 above: data center access, server room security)

---

## P: Privacy (New for SOC 2:2024)

**Control Objective:** Personal information must be protected per privacy laws + regulations.

(Covered in separate `NZ_PRIVACY_ACT_2020_MAPPING.md`; here we focus on operational mechanisms)

```yaml
Privacy Controls Integration:
  - Privacy by Design: assess new systems for privacy risks
  - Data Minimization: collect only what's necessary
  - Retention Limits: auto-delete data after configured period
  - Consent Management: capture + verify user consent for processing
  - Privacy Incident Response: breach notification within 72 hours
  - Privacy Impact Assessment (PIA): quarterly review
  - Third-party DPA: enforce data processor agreements
  - User Rights: DSAR/deletion/portability workflows automated
```

---

## Control Assessment Template

For each control, evaluate:

| Dimension | Question | Status | Evidence |
|-----------|----------|--------|----------|
| **Design** | Is the control properly designed to address the objective? | ✓ / ✗ | [Attach documentation] |
| **Implementation** | Has the control been implemented? | ✓ / ✗ | [Screenshots / logs] |
| **Effectiveness** | Is the control operating as designed? | ✓ / ✗ | [Audit results / test records] |
| **Monitoring** | Is the control continuously monitored? | ✓ / ✗ | [Alert logs, reports] |

---

## Audit Readiness Checklist

- [ ] CC1: Governance structure + board oversight documented
- [ ] CC6.1: MFA enforced for all admin accounts; RBAC configured
- [ ] CC6.2: Physical access logged; data center badges + surveillance
- [ ] CC7: Change management enforced; segregation of duties matrix
- [ ] CC9: Encryption at rest (AES-256) + in transit (TLS 1.3+)
- [ ] CC9: Patch management policy; vulnerability scans weekly
- [ ] CC9: Backup tested quarterly; RTO/RPO met
- [ ] A1: Uptime monitoring; SLO 99.5% documented
- [ ] A1: High availability architecture (no single point of failure)
- [ ] A1: On-call rotation + runbooks documented
- [ ] S1/S2: Incident response plan + annual drill
- [ ] P: DSAR workflow automated + SLA met (20 working days)
- [ ] P: Privacy notices at point of collection
- [ ] P: Third-party DPAs signed + access logged

---

## External Audit Preparation (12+ Months)

### Month 1-3: Design & Documentation
- Finalize control documentation
- Diagram system architecture
- Document all processes + policies

### Month 4-6: Implementation & Testing
- Deploy all controls to production
- Test controls (e.g., MFA, change management, incident response)
- Collect baseline evidence

### Month 7-9: Monitoring & Improvement
- Establish continuous monitoring
- Run through full audit procedures
- Fix any gaps discovered

### Month 10-12: Audit Engagement
- Engage external auditor (AICPA-qualified)
- Provide all evidence + documentation
- Conduct interviews + walkthroughs
- Auditor issues report + opinion (issued ~3 months post-engagement)

---

## Expected Audit Findings (Common)

| Finding | Mitigation |
|---------|-----------|
| "MFA not enforced for all accounts" | Implement universal MFA; phase in over 60 days |
| "Change management documentation incomplete" | Create PR template; require change ticket link in every commit |
| "Encryption key rotation not automated" | Deploy HashiCorp Vault + configure auto-rotation pipeline |
| "Incident response plan not tested" | Schedule annual IR drill; document results |
| "Access reviews not quarterly" | Automate RBAC review; send quarterly for manual approval |

