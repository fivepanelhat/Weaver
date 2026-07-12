# NZ Privacy Act 2020 - Implementation Mapping

**Effective Date:** 14 September 2020  
**Jurisdiction:** Aotearoa New Zealand  
**Applies to:** All organizations handling personal information (domestic or cross-border)

---

## Information Privacy Principles (IPPs) 1-11

### IPP 1: Collection Purpose

**Principle:** Personal information must be collected for a lawful purpose that is necessary for functions of the entity.

**Implementation Checklist:**
- [ ] Document all collection purposes in a Privacy Notice (plaintext, accessible)
- [ ] Disclose purposes to data subjects at collection time
- [ ] Limit collection to necessary information only (purpose limitation)
- [ ] Example: "We collect your email to send appointment reminders. We will not use it for marketing."

**Breach Scenario:**
- Collecting phone numbers "for emergency contact" but using them for marketing calls → **IPP1 breach**

**Remediation:**
```yaml
Collection Purpose Statement:
  - Purpose: Health appointment reminders (SMS/email)
  - Necessity: Required to schedule + confirm appointments
  - Retention: Delete after appointment completion + 90-day grace period
  - Disclosure: Not shared with third parties (except SMS provider for delivery)
```

---

### IPP 2: Source of Personal Information

**Principle:** Reasonable steps must be taken to ensure individual is aware of the information being collected and the purpose.

**Implementation Checklist:**
- [ ] Privacy Notice provided at point of collection
- [ ] For indirect collection (web forms, APIs), embed privacy disclosure
- [ ] For health data, inform patient of Health Information Privacy Code compliance
- [ ] Document source attestation (direct vs. indirect collection)

**Breach Scenario:**
- Purchasing patient list from third party without disclosure → **IPP2 breach**

**Remediation:**
```yaml
Indirect Collection Protocol:
  - Trigger: Data received from referral partner
  - Action: Send data subject a Privacy Notice within 5 working days
  - Content: Purpose, retention period, access rights, complaint pathway
  - Documentation: Log notification timestamp + delivery proof
```

---

### IPP 3: Collection Manner

**Principle:** Information must be collected by fair and lawful means; no deception/coercion.

**Implementation Checklist:**
- [ ] Obtain explicit consent for sensitive data (health, ethnicity, cultural info)
- [ ] No pre-ticked consent boxes (positive action required)
- [ ] Consent withdrawal mechanism available
- [ ] Document consent audit trail (timestamp, version of terms, user action)

**Breach Scenario:**
- Scraping patient data from public health portal without consent → **IPP3 breach**

**Remediation:**
```yaml
Consent Capture:
  - Mechanism: Explicit checkbox (not pre-ticked)
  - Text: "I consent to Weaver storing my health information for appointment management"
  - Audit Trail: Timestamp + IP + session ID stored (immutable log)
  - Withdrawal: One-click unsubscribe; processed within 5 working days
```

---

### IPP 4: Storage & Security

**Principle:** Personal information must be protected by reasonable security safeguards against misuse, loss, unauthorized access.

**Implementation Checklist:**
- [ ] Encryption at rest: AES-256 (all databases)
- [ ] Encryption in transit: TLS 1.3+ (all API calls)
- [ ] Access controls: RBAC + MFA for admin access
- [ ] Secret management: Vault / Secrets Manager (no hardcoded credentials)
- [ ] Audit logging: 18-month retention (immutable, centralized)
- [ ] Regular security testing: quarterly penetration testing + weekly vulnerability scans

**Breach Scenario:**
- Sending PHI via unencrypted email → **IPP4 critical breach** (likely Privacy Commissioner notification)
- Storing passwords in plaintext → **IPP4 critical breach**

**Remediation:**
```yaml
Storage Security Hardening:
  Encryption at Rest:
    - Database: Postgres with pgcrypto + encrypted tablespaces
    - Backups: S3 with encryption key in KMS
    - Key Rotation: Every 90 days (automated)
  
  Encryption in Transit:
    - All APIs: TLS 1.3 minimum
    - Database connections: SSL/TLS enforced
    - Key pinning: HPKP headers on all web responses
  
  Access Control:
    - Admin panel: MFA + RBAC (roles: read-only, editor, admin)
    - Service accounts: Short-lived creds (max 1 hour), rotated daily
    - SSH keys: ED25519 only, audited monthly
  
  Audit Logging:
    - Events: API calls, login attempts, data access, modifications
    - Retention: 18 months (immutable, stored in separate secure bucket)
    - Alerts: Unauthorized access attempts trigger email + Slack notification
```

---

### IPP 5: Access by Individual

**Principle:** Individuals must be able to access their personal information held by the entity.

**Implementation Checklist:**
- [ ] Data Subject Access Request (DSAR) portal implemented
- [ ] SLA: Respond within 20 working days
- [ ] Export format: Human-readable (CSV, PDF, JSON)
- [ ] Verification: Confirm identity before disclosure
- [ ] Cost: Free for first request per year (subsequent: reasonable cost)

**Breach Scenario:**
- Refusing to provide patient their own health records → **IPP5 breach**

**Remediation:**
```yaml
DSAR Workflow:
  1. User submits request via portal
  2. System verifies identity (email verification + security questions)
  3. Generate data export: all stored PII linked to user
  4. Include: Audit trail of accesses, usage purposes, retention schedule
  5. Deliver via secure download link (expires after 7 days)
  6. Log completion: timestamp + response method in compliance audit trail
  7. Deadline: 20 working days from receipt
```

---

### IPP 6: Correction of Personal Information

**Principle:** Individuals must be able to request correction of inaccurate information.

**Implementation Checklist:**
- [ ] Correction request form available (web + email)
- [ ] SLA: Acknowledge request within 10 working days
- [ ] Investigation: Verify accuracy of information
- [ ] Decision: Approve, partially approve, or decline (with reasons)
- [ ] Documentation: Maintain record of corrections + disputes

**Breach Scenario:**
- Patient's gender recorded incorrectly; patient requests correction; system refuses → **IPP6 breach**

**Remediation:**
```yaml
Correction Request Workflow:
  1. User identifies inaccurate information
  2. Submit correction form (include: field, current value, correct value, reason)
  3. System generates ticket + notifies compliance team
  4. Investigation: Verify against source (e.g., medical record, patient declaration)
  5. Decision (within 10 working days):
     - Approve: Update record, notify requester, log change
     - Decline: Provide written reason + appeal pathway
  6. If disputed: Add notation to record ("Correction disputed by individual on [date]")
```

---

### IPP 8: Accuracy, Completeness & Currency

**Principle:** Information must be accurate, complete, up-to-date, not misleading.

**Implementation Checklist:**
- [ ] Data quality audits: quarterly
- [ ] Stale data detection: flag records inactive >12 months
- [ ] Verification workflows: ask users to confirm accuracy annually
- [ ] Source matching: reconcile against authoritative source (e.g., NZ Inland Revenue)
- [ ] Correction history: audit trail of all modifications

**Breach Scenario:**
- Patient's age auto-populated as 2025 (current year) instead of birth year → **IPP8 breach** (misleading)

**Remediation:**
```yaml
Data Quality Assurance:
  Quarterly Audits:
    - Identify records >18 months old without update
    - Detect invalid formats (e.g., email without @, phone < 7 digits)
    - Reconcile against NZ Birth Register (if applicable)
    - Generate compliance report with remediation actions
  
  User Verification:
    - Annual email: "Please confirm your information is correct"
    - Opt-in update links (one-click verify)
    - Non-response after 60 days: flag for manual review
  
  Correction Audit Trail:
    - Store all versions (soft deletes, not hard deletes)
    - Timestamp + user who made change
    - Reason for modification (mandatory field)
```

---

### IPP 10: Limits on Use of Personal Information

**Principle:** Information collected for one purpose cannot be used for a different, unrelated purpose without consent.

**Implementation Checklist:**
- [ ] Map all data uses: list every system/report that accesses user data
- [ ] Document secondary uses: flag any uses outside original collection purpose
- [ ] Consent audit: verify explicit consent for all secondary uses
- [ ] Access logging: track who accesses data, when, for what purpose

**Breach Scenario:**
- Collected patient email for appointment reminders; sold list to pharmaceutical company for marketing → **IPP10 critical breach**

**Remediation:**
```yaml
Use Limitation Enforcement:
  Primary Use:
    - Purpose: "Appointment scheduling + reminder notifications"
    - Authorized: Weaver (appointment system), SMS provider (delivery only)
    - Unauthorized: Marketing, analytics, third-party sharing
  
  Secondary Use (if required):
    - Example: "Anonymized appointment patterns for Hub capacity planning"
    - Requirement: Explicit user consent OR anonymization proof (k-anonymity ≥10)
    - Log: Store secondary use purposes in compliance metadata
  
  Access Control:
    - Admin API: filter by purpose (e.g., read appointment data = yes, read email = no)
    - Audit log: every data access includes purpose code
    - Alert: flag unauthorized purpose accesses
```

---

### IPP 11: Disclosure of Personal Information

**Principle:** Information must not be disclosed to third parties without consent (with exceptions for law enforcement, public interest).

**Implementation Checklist:**
- [ ] Third-party audit: document all vendors/processors who access data
- [ ] Data Processing Agreements (DPAs): signed with all third parties
- [ ] Consent audit: verify user consent before sharing
- [ ] Disclosure logging: immutable audit trail of all third-party accesses
- [ ] Legal exceptions: maintain list of law enforcement / regulatory requests

**Breach Scenario:**
- Sharing patient data with insurance company to "reduce fraud" without consent → **IPP11 breach**

**Remediation:**
```yaml
Disclosure Control:
  Third-Party Inventory:
    - SMS provider: accesses phone + appointment date (send reminders)
    - Email provider: accesses email + appointment date (send reminders)
    - Backup provider: accesses all data (unencrypted, in transit) → STOP: encrypt before transfer
  
  Data Processing Agreements:
    - Requirement: Signed DPA with all third parties before any data sharing
    - Content: Purpose, duration, security measures, deletion schedule, liability
    - Review: Annually, or when vendor changes practices
  
  Disclosure Audit Trail:
    - Event: "Data shared with [vendor]"
    - Context: Date, purpose, data elements, user consent record
    - Result: Success/failure, any errors
    - Retention: 7 years (per Privacy Act recommended practice)
  
  Law Enforcement Requests:
    - Policy: Require legal warrant before disclosure (Police, IRD, etc.)
    - Log: All requests logged with decision + legal authority cited
    - Notification: Inform user of disclosure (unless legally prohibited)
```

---

## Sensitive Personal Information (Privacy Commissioner Guidance)

### Health Information
- **Definition:** Any information about a person's physical/mental health, disability, medical history
- **Special Protection:** IPP4 security requirements enhanced; encryption at rest/transit mandatory
- **Retention:** Delete after 7 years (NZ Health Information Privacy Code)
- **Health Professional Privilege:** Doctors/nurses may withhold info if disclosure would harm patient

### Biometric Data
- **Definition:** Fingerprints, iris scans, DNA, voice recognition patterns
- **Special Protection:** Explicit consent required; cannot be repurposed without consent
- **Risk:** High re-identification risk; anonymization difficult
- **Implementation:** Store encrypted, access logged, deletion on-demand

### Financial Information
- **Definition:** Bank account numbers, credit card numbers, tax records, income
- **Special Protection:** IPP4 enhanced; PCI-DSS compliance (if credit cards)
- **Retention:** Delete after 7 years

### Ethnic / Cultural Information
- **Definition:** Māori/Pasifika ancestry, cultural affiliation, iwi membership
- **Special Protection:** Subject to Te Mana Raraunga principles; iwi consent may be required
- **Risk:** Can be used for discrimination; must be anonymized for analytics

---

## Privacy Commissioner Enforcement

### Complaint Process
1. Individual files complaint with Privacy Commissioner (free, no time limit generally)
2. Privacy Commissioner investigates (may take 12+ months)
3. If breach found:
   - **Investigation** findings published (can damage reputation)
   - **Remediation order** issued
   - **Financial penalty** possible (up to $300,000 for significant breaches)
   - **Injunction** to cease unlawful conduct

### Notification Requirements
- **Serious Data Breach:** Notify affected individuals + Privacy Commissioner within reasonable time (typically 72 hours)
- **Notification Content:** Nature of breach, likely consequences, mitigation steps, contact info
- **Documentation:** Maintain breach register (2+ years retention)

---

## Compliance Verification Checklist

- [ ] All 11 IPPs mapped to system architecture
- [ ] Sensitive data encryption at rest (AES-256) + in transit (TLS 1.3+)
- [ ] DSAR workflow implemented + SLA met (20 working days)
- [ ] Audit logs immutable + 18-month retention
- [ ] Third-party DPAs signed + data access logged
- [ ] Privacy Notices available at point of collection
- [ ] Consent capture audit trail enabled
- [ ] Data quality audits scheduled (quarterly)
- [ ] Incident response plan includes Privacy Commissioner notification SLA
- [ ] Privacy impact assessment (PIA) completed for new systems
