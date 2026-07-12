# Compliance Audit Checklist — Pre-Audit Readiness Verification

**Purpose:** Verify system readiness for external SOC 2 Type II audit (minimum 6 months of operating controls)  
**Frequency:** Monthly review (leading up to audit), quarterly post-audit  
**Responsibility:** Compliance Officer + Security Team

---

## Quick Readiness Score

Calculate compliance percentage:

```
Total checks: ____ items marked ✓
Total audit checklist: 92 items
Readiness: (checked / 92) × 100 = ____%

Target: ≥95% before external audit engagement
```

**Traffic Light Status:**
- 🟢 **Green (≥90%):** Ready for external audit within 4 weeks
- 🟡 **Yellow (70-89%):** On track; address gaps within 8 weeks
- 🔴 **Red (<70%):** Significant gaps; delay audit 12+ weeks

---

## CC: Common Criteria

### CC1: Governance & Oversight

**CC1.1 Control Environment**
- [ ] Governance charter signed by board/leadership
- [ ] Board minutes document security discussions (4+ meetings/year)
- [ ] Compliance committee established (meets quarterly min)
- [ ] RACI matrix documented (clear roles & responsibilities)
- [ ] Audit plan shared with board + stakeholders
- [ ] Risk register maintained (reviewed quarterly)

**CC1.2 Ethical Conduct**
- [ ] Code of Conduct documented + signed by all employees (100%)
- [ ] Confidentiality agreements in place (all staff)
- [ ] Anti-bribery/corruption policy documented
- [ ] Conflict of interest disclosure policy + disclosures tracked
- [ ] Whistleblower hotline (anonymous) established + promoted
- [ ] Investigations process documented + sample incident reviewed
- [ ] No unresolved ethics violations (or documented remediation)

**CC1.3 Policies & Procedures**
- [ ] Security policy: documented, dated, reviewed ≥annual
- [ ] Privacy policy: published + accessible to users
- [ ] Incident response plan: documented + tested annually
- [ ] Change management process: documented + followed
- [ ] Access control policy: documented + enforced
- [ ] Data retention policy: documented + enforced
- [ ] Backup/disaster recovery policy: documented + tested

**Score: ___ / 15**

---

### CC6: Logical & Physical Access

**CC6.1 Logical Access**

Authentication & Authorization:
- [ ] MFA enforced for all admin/privileged access (100%)
- [ ] Password policy: min 12 chars, complexity, history, expiry
- [ ] Session timeout: 15 min (admin), 60 min (general)
- [ ] Account lockout: 5 attempts → 30 min lockout (configured)
- [ ] RBAC implemented (roles: viewer, editor, admin, auditor, etc.)
- [ ] Segregation of duties enforced (matrix documented)
- [ ] Default deny (whitelist, not blacklist)
- [ ] Service accounts: short-lived creds (max 1 hour) ← KEY
- [ ] API authentication: OAuth 2.0 / JWT (not basic auth)
- [ ] API tokens: max 1 hour expiry
- [ ] Refresh tokens: max 30 days
- [ ] API key rotation: enforced every 90 days
- [ ] API key retirement: old keys disabled (not deleted immediately)
- [ ] VPN/remote access: MFA + logging
- [ ] SSH keys: ED25519 only, documented, rotated annually

Access Review & Recertification:
- [ ] Quarterly access review completed (4 consecutive quarters)
- [ ] Access review sign-offs: manager approved (documented)
- [ ] Orphaned accounts removed (no active employee)
- [ ] Termination process: access revoked within 1 hour

Audit Logging:
- [ ] Login attempts logged (success + failure)
- [ ] Failed login alerts (configured + monitored)
- [ ] Admin action audit trail: who did what, when
- [ ] API access audit trail: all requests logged
- [ ] Logs immutable (write-once, cannot be modified)
- [ ] Logs centralized (not local to each server)
- [ ] Log retention: 18 months minimum
- [ ] Log review: automated alerts + manual review

**CC6.2 Physical Access**

Data Center Security:
- [ ] Physical access controls: badge/keycard
- [ ] Tailgating prevention: turnstile/mantrap
- [ ] Visitor log maintained (manual or automated)
- [ ] Visitors accompanied by employee at all times
- [ ] CCTV surveillance: 24/7, 90-day retention minimum
- [ ] After-hours access: requires approval + notification
- [ ] Environmental monitoring: temp, humidity, power (alerts)
- [ ] UPS + backup generator (tested quarterly)
- [ ] Fire suppression system (tested annually)
- [ ] Facility security guards / access control personnel

Server Room / Cabinet Security:
- [ ] Locked cabinet or cage (key access restricted)
- [ ] Access limited to authorized personnel
- [ ] Physical access audit trail (log + CCTV)
- [ ] Cable management: labeled + documented
- [ ] Backup media security: encrypted + locked storage

**Score: ___ / 49**

---

### CC7: Restricted Access to System Assets

**CC7.1 Change Management**

Requirements & Approval:
- [ ] Change requests documented (form + approval)
- [ ] Change control board: review + approval (documented)
- [ ] Impact assessment: documented for each change
- [ ] Rollback plan: documented before deployment
- [ ] Authorized approvers: CFO, CTO, or delegates (list)

Testing & Staging:
- [ ] Test environment: isolated from production
- [ ] Changes tested in staging before production
- [ ] Test results documented (pass/fail)
- [ ] User acceptance testing (UAT): documented approval
- [ ] Performance testing: no degradation confirmed

Deployment & Tracking:
- [ ] Deployment checklist: signed off before go-live
- [ ] Deployment window: scheduled, communicated
- [ ] Deployment log: timestamp + who deployed + change ID
- [ ] Monitoring: enhanced during/after deployment
- [ ] Rollback: executed if issues detected
- [ ] Post-deployment verification: system working as intended

**CC7.2 Change Frequency & Limits**

- [ ] Change frequency policy: documented (e.g., max 2x/week)
- [ ] Emergency change process: expedited but still documented
- [ ] Change audit: 100% of changes in last 12 months tracked
- [ ] No unauthorized/undocumented changes (detected by code review or infrastructure audit)

**CC7.3 Version Control**

- [ ] All code in Git (not scattered across local machines)
- [ ] Branch protection: require code review + approval
- [ ] Commit signatures: GPG / SSH (verify authenticity)
- [ ] Deploy keys: separate from development keys (least privilege)
- [ ] Key audit: all SSH/deploy keys documented + rotated annually
- [ ] GitHub/GitLab audit: all actions logged + monitored

**CC7.4 Secret Management**

- [ ] Centralized secret vault: HashiCorp Vault / AWS Secrets Manager
- [ ] No hardcoded credentials in code (enforced by static analysis)
- [ ] Static analysis (e.g., truffleHog, git-secrets) running in CI
- [ ] Secret rotation: automated, every 90 days
- [ ] Secret access audit: who accessed what, when (logged)
- [ ] Secret access alerts: notify on unusual access patterns
- [ ] Service accounts: unique per service (no shared creds)
- [ ] Database credentials: separate per environment (prod/staging/dev)

**CC7.5 Patch Management**

- [ ] Vulnerability scanning: weekly (all container images)
- [ ] Patch policy: critical (0-24h), high (1-7d), medium (30d)
- [ ] Patch testing: applied to staging first
- [ ] Patch deployment: tracked in change log
- [ ] Patch audit: 100% of patches applied in last 12 months
- [ ] End-of-life OS/software: documented + upgrade plan

**Score: ___ / 38**

---

### CC9: Logical & Information Security

**CC9.1 Encryption at Rest**

- [ ] Database encryption: AES-256 (Postgres pgcrypto / native)
- [ ] Backup encryption: AES-256 (S3 / Vault)
- [ ] Encryption key management: documented
- [ ] Key rotation: every 90 days (automated)
- [ ] Key escrow: master key in separate secure location
- [ ] Encryption validation: test decryption quarterly
- [ ] Unencrypted data: none on production servers (verified)

**CC9.2 Encryption in Transit**

- [ ] API endpoints: TLS 1.3+ only (no downgrade to 1.2)
- [ ] HSTS headers: enforced on all domains
- [ ] Certificate pinning: HPKP headers (optional but recommended)
- [ ] Database connections: SSL/TLS enforced (no plaintext)
- [ ] Message queues: encrypted (e.g., RabbitMQ with TLS)
- [ ] VPN traffic: encrypted, no split tunneling
- [ ] Email: TLS for SMTP (no plaintext)
- [ ] Cert audit: valid, not expired, proper domain

**CC9.3 Malware Prevention**

- [ ] Antivirus: installed on admin machines (Windows/Mac)
- [ ] Container scanning: Trivy (weekly) + Clair (on deployment)
- [ ] Image registry scanning: DockerHub / ECR scanning enabled
- [ ] SAST (static analysis): SonarQube running in CI
- [ ] DAST (dynamic analysis): quarterly penetration test
- [ ] Log monitoring: detect malware signatures in logs
- [ ] EDR (Endpoint Detection): deployed on admin machines (optional)

**CC9.4 Backup & Disaster Recovery**

- [ ] Backup frequency: daily (hourly for critical)
- [ ] Backup retention: 30 days (hot), 1 year (cold archive)
- [ ] Backup encryption: encrypted at rest + in transit
- [ ] Backup testing: restore from backup monthly
- [ ] Backup audit: verify data integrity + completeness
- [ ] RTO (Recovery Time Objective): documented + achievable
- [ ] RPO (Recovery Point Objective): documented + achievable
- [ ] Immutable backup: prevent accidental/ransomware deletion
- [ ] Geographic diversity: backups in separate region (recommended)
- [ ] DR drill: annual restore-from-backup test

**CC9.5 Incident Response & Monitoring**

- [ ] SIEM (Security Information Event Management): Splunk / ELK
- [ ] Alerting: automated for suspicious events
- [ ] Detection: IDS/IPS (Snort / Suricata)
- [ ] DDoS protection: AWS Shield / Cloudflare WAF
- [ ] WAF rules: OWASP Top 10 coverage
- [ ] Rate limiting: configured on all APIs
- [ ] Monitoring dashboard: real-time visibility
- [ ] Incident response plan: documented + tested annually

**Score: ___ / 42**

---

## A: Availability

**Availability Monitoring & SLA**

- [ ] Uptime monitoring: external service (StatusPage, Pingdom)
- [ ] Uptime SLO: 99.5% monthly (documented)
- [ ] Uptime reporting: monthly dashboard published
- [ ] Response time SLA: documented for APIs
- [ ] Response time monitoring: p99 latency tracked
- [ ] Outage communication: status page updated every 30 min

**High Availability Architecture**

- [ ] No single point of failure: all services replicated
- [ ] Load balancing: active-active (not active-passive)
- [ ] Database replication: primary + hot standby
- [ ] Automatic failover: tested quarterly
- [ ] Failover time: <5 min (documented)
- [ ] Database replica lag: <1 sec (monitored)
- [ ] Blue-green deployments: zero-downtime updates
- [ ] DNS failover: multi-region routing (if applicable)

**Capacity Planning**

- [ ] Baseline metrics: CPU, memory, disk under normal load
- [ ] Capacity growth model: predict when limits will be hit
- [ ] Scaling triggers: auto-scale before hitting limits (documented)
- [ ] Load testing: quarterly (simulate peak traffic)
- [ ] Forecasting: resource needs 6-12 months ahead

**On-Call & Incident Response**

- [ ] On-call rotation: 24/7 coverage
- [ ] On-call SLA: acknowledge alert within 5 min
- [ ] Escalation path: documented + followed
- [ ] Runbooks: step-by-step recovery procedures
- [ ] Communication plan: stakeholder notifications during incident

**Score: ___ / 22**

---

## S: Security

(Covered in CC6, CC7, CC9 above)

**Score: ___ / 0 (already counted)**

---

## P: Privacy (SOC 2:2024)

**Privacy by Design**

- [ ] Privacy impact assessment (PIA): completed for new systems
- [ ] Data minimization: collect only necessary data
- [ ] Purpose limitation: use only for stated purpose
- [ ] Retention limits: auto-delete after configured period
- [ ] Privacy policy: published + clear (non-technical language)

**Consent & User Rights**

- [ ] Consent capture: explicit (not pre-ticked)
- [ ] Consent audit trail: timestamp + version of terms
- [ ] Consent withdrawal: one-click unsubscribe
- [ ] DSAR workflow: automated portal + SLA (20 working days)
- [ ] DSAR response: data export in human-readable format
- [ ] Deletion workflow: implemented + verified
- [ ] Portability: export in machine-readable format (JSON/CSV)

**Third-Party Management**

- [ ] DPA (Data Processing Agreements): signed with all vendors
- [ ] Vendor audit: verify security + compliance
- [ ] Vendor access logging: track who accessed data, when
- [ ] Subprocessor list: published + updated quarterly
- [ ] Breach liability: contractually assigned (vendor responsible)

**Breach Response**

- [ ] Incident response plan: includes Privacy Commissioner notification
- [ ] Notification SLA: 72 hours to Privacy Commissioner
- [ ] Breach register: maintained + reviewed
- [ ] Forensics: 18+ month log retention

**Score: ___ / 20**

---

## NZ Privacy Act 2020 (IPPs 1-11)

**Information Privacy Principles**

- [ ] IPP1: Collection purpose documented + disclosed
- [ ] IPP2: Source communicated (if indirect collection)
- [ ] IPP3: Fair collection (no deception/coercion)
- [ ] IPP4: Storage security (encryption at rest/transit)
- [ ] IPP5: Data subject access (DSAR portal implemented)
- [ ] IPP6: Correction (user can request corrections)
- [ ] IPP8: Data accuracy (quarterly audit)
- [ ] IPP10: Use limitation (secondary uses logged)
- [ ] IPP11: Disclosure limits (third-party DPAs signed)
- [ ] Health data retention: 7 years (Health Privacy Code)

**Privacy Commissioner Compliance**

- [ ] Privacy notice: published on website
- [ ] Privacy contact: published + monitored
- [ ] Complaint handling: process documented + SLA met
- [ ] Complaint register: maintained (2+ year retention)

**Score: ___ / 14**

---

## Te Mana Raraunga (Māori Data Sovereignty)

- [ ] Data ownership registry: maintained + reviewed quarterly
- [ ] Cultural Advisory Board: established + meets monthly
- [ ] Data use agreements: signed for all Māori datasets
- [ ] Encryption key: iwi holds master key (or threshold system)
- [ ] Data localization: all Māori data in Aotearoa
- [ ] Cultural classification: all data classified Level 1/2/3
- [ ] Staff training: annual cultural competency (100% completion)
- [ ] Community hui: annual meeting to review data uses
- [ ] Access audit: all Māori data access logged (weekly review)
- [ ] Benefit-sharing: tracked + reported quarterly
- [ ] Deletion workflow: tested annually

**Score: ___ / 11**

---

## System Architecture & Infrastructure

- [ ] Architecture diagram: documented + reviewed
- [ ] Data flow diagram: shows all systems + connections
- [ ] Technology stack: documented (OS, database, middleware)
- [ ] Dependencies: documented + EOL tracked
- [ ] Infrastructure as Code (IaC): Terraform / CloudFormation
- [ ] Environment parity: dev/staging/prod configurations match
- [ ] Secrets management: centralized (no environment variables in code)
- [ ] Monitoring & logging: comprehensive coverage
- [ ] Disaster recovery architecture: documented + tested

**Score: ___ / 9**

---

## TOTAL READINESS SCORE

**Common Criteria (CC1/6/7/9): ___ / 149**  
**Availability (A): ___ / 22**  
**Privacy Act 2020 (P + IPPs): ___ / 34**  
**Te Mana Raraunga: ___ / 11**  
**Architecture & Infrastructure: ___ / 9**

**TOTAL: ___ / 225**

**Readiness Percentage: (Total / 225) × 100 = ____%**

---

## Remediation Tracking

| Gap | Priority | Owner | Deadline | Status | Evidence |
|-----|----------|-------|----------|--------|----------|
| API tokens lack expiry | High | [Name] | [Date] | In Progress | PR#123 |
| SIEM not deployed | Critical | [Name] | [Date] | Open | — |
| Cultural Advisory Board not yet established | High | [Name] | [Date] | Planned | — |

---

## Auditor Sign-Off

**External Auditor Readiness Assessment:**

- [ ] Auditor has reviewed this checklist
- [ ] Auditor confirms all items validated
- [ ] Auditor identified no material gaps
- [ ] Auditor ready to proceed with SOC 2 Type II engagement

**Auditor Name:** ________________  
**Date:** ________________  
**Firm:** ________________  

**Organization Attestation:**

I certify that the above checklist reflects the accurate state of Coastal Alpine Tech systems and controls as of this date. All items marked ✓ are confirmed, implemented, and operating effectively.

**Compliance Officer:** ________________  
**Date:** ________________  
**Title:** ________________  

