# Incident Response Playbook — Data Breach & Security Events

**Authority:** Privacy Act 2020 § 109-112, Privacy Commissioner Guidance  
**Effective Date:** Immediately upon detection  
**Scope:** All Coastal Alpine Tech systems (Weaver, Core, Stack, Aether)

---

## Incident Classification & SLAs

| Severity | Definition | Examples | Response SLA | Notification SLA |
|----------|-----------|----------|--------------|------------------|
| **P0 — CRITICAL** | Large-scale data breach, active exploitation | 100+ health records exposed; ransomware | 15 min | 24 hours |
| **P1 — HIGH** | Medium breach, contained threat | 10-99 health records exposed; unauthorized admin access | 1 hour | 72 hours |
| **P2 — MEDIUM** | Minor breach, user impact | 1-9 records exposed; failed login attempts | 4 hours | 10 business days |
| **P3 — LOW** | Potential issue, no confirmed impact | Suspicious log entry; configuration drift | 1 business day | 30 business days |

---

## Incident Response Workflow

### Phase 1: Detection & Initial Response (15 min - P0, 1 hour - P1)

**Automated Detection:**

```yaml
Monitoring Alerts (Always On):
  - Unauthorized login attempts: 5+ failures in 5 min → P1
  - Data exfiltration: >1GB data transfer in 10 min → P0
  - Encryption key accessed: Outside normal business hours → P1
  - Database query: Direct SELECT on sensitive tables (not via app) → P1
  - API rate limiting: 1000+ requests/sec (possible DDoS) → P1
  - Failed backup: Restore test fails or backup corrupted → P2

On-Call Rotation:
  - Weekdays: 9am-5pm (in-office)
  - Evenings/weekends: On-call engineer (rotate weekly)
  - Alert channels: Phone call (primary), SMS (backup), email (tertiary)
  - Response time: Acknowledge within 5 min, brief within 15 min
```

**Initial Triage:**

```yaml
Step 1: Confirm Incident (5 min)
  - Q: Is there confirmed unauthorized access?
  - Q: Is health/sensitive data affected?
  - Q: Is active exploitation ongoing?
  - Result: Assign P0/P1/P2/P3

Step 2: Isolate (if needed) (5-10 min)
  - Decision: Do we need to shut down affected service?
    - YES if: Active exploitation, data exfiltration, ransomware
    - NO if: Potential issue but contained
  - Action: Isolate service from network (manual kill-switch)
  - Notify: Alert compliance team immediately (P0/P1 only)

Step 3: Activate Incident Commander (5 min)
  - Role: Lead investigation + decision-making
  - Authority: Can override normal processes (e.g., skip code review for emergency patch)
  - Communication hub: All updates flow through IC
```

---

### Phase 2: Investigation & Containment (1-4 hours)

**Incident Commander Leads:**

```yaml
Investigation Steps:
  1. Determine Scope:
     - When did the incident start? (timestamp)
     - How many records affected? (count + data elements)
     - Which systems were accessed? (app, database, API, etc.)
     
  2. Preserve Evidence:
     - Pull full audit logs (immutable copy to separate storage)
     - Capture network traffic (pcap files)
     - Take filesystem snapshots (AWS AMI, filesystem backup)
     - Lock down affected systems (no further changes until forensics)
  
  3. Identify Root Cause:
     - Unauthorized access: How did attacker get credentials? (phishing, brute force, leaked key?)
     - Data exfiltration: Which API/endpoint? Via what mechanism? (download, API, etc.)
     - Malware: Scan for persistence; check for C2 communications
     - Insider threat: Review user access patterns vs. normal behavior
  
  4. Contain the Threat:
     - Revoke credentials: Reset passwords for affected accounts (immediate)
     - Patch vulnerability: If known CVE, deploy patch now
     - Kill sessions: Terminate all active sessions for affected users
     - Block IP/domains: If external attacker, block at firewall
     - Rotate encryption keys: If key was compromised (immediate)
  
  5. Forensics:
     - Timeline: Reconstruct exact sequence of events
     - Attribution: Who was the attacker? (IP, user agent, behavioral patterns)
     - Impact: Exactly which records were accessed/modified/deleted?
     - Evasion: Did attacker try to hide tracks? (log tampering, cleanup)

Containment Checklist:
  - [ ] Service isolated from network (if active exploitation)
  - [ ] Affected credentials revoked + reset
  - [ ] Vulnerability patched in production
  - [ ] User sessions terminated
  - [ ] Firewall rules updated (block attacker IP)
  - [ ] Encryption keys rotated
  - [ ] Evidence collected + preserved
```

---

### Phase 3: Notification & Escalation (24-72 hours)

**Privacy Commissioner Notification (Mandatory for Data Breach):**

```yaml
Trigger: Any unauthorized access to personal information likely to cause harm

Notification Timeline:
  - Without unreasonable delay (ideally <72 hours)
  - Send to: breaches@privacy.org.nz
  - Method: Email (sign with digital certificate or GPG key)

Notification Content:
  1. Summary:
     - Description of breach (what, when, how discovered)
     - Date range of unauthorized access
     - Number of individuals affected
  
  2. Data Elements:
     - What information was exposed? (names, health data, contact info, etc.)
     - Sensitivity level (Level 1: public, Level 2: personal, Level 3: health/sensitive)
  
  3. Likely Consequences:
     - For individuals: Risk of identity theft, discrimination, etc.
     - Severity: Low, medium, high, or critical
  
  4. Mitigation:
     - What steps have we taken? (credential reset, encryption, etc.)
     - What steps do individuals need to take? (monitor credit, change passwords, etc.)
     - Ongoing monitoring: How will we prevent recurrence?
  
  5. Contact Information:
     - Organization contact: [Name, email, phone]
     - Description of breach can be reviewed by affected individuals? Yes/No
  
  6. Proof of Notification:
     - Attach evidence that individuals were notified (email template, letter, etc.)

Example Notification Email:
  Subject: Data Breach Notification - Privacy Commissioner

  To: breaches@privacy.org.nz

  On [DATE], Coastal Alpine Tech detected unauthorized access to health records
  in the Weaver system affecting approximately [COUNT] individuals.

  Unauthorized access: [DATE] to [DATE] (estimated)
  Data exposed: Names, health conditions, appointment dates
  Cause: Compromised API key used to download patient records

  Mitigation taken:
    - API key revoked (immediate)
    - All affected users notified via email + SMS
    - Password resets required on next login
    - Encryption keys rotated
    - Firewall rules updated to block attacker IP

  Ongoing:
    - Continuous monitoring for similar access patterns
    - Monthly vulnerability scans
    - Security training for all staff
    - API key rotation policy (90-day max)

  Individuals can view breach details: [secure link expires in 30 days]

  Contact: [Name], Privacy Officer, privacy@coastalalp.tech, +64 9 XXX XXXX
```

**Individual Notification (Within 72 hours of Privacy Commissioner):**

```yaml
Delivery Method:
  - Primary: Email to registered address
  - Backup: SMS to phone number
  - Fallback: Registered mail (if email delivery fails)

Notification Content:
  Subject: "Important: Your Health Records Were Affected by a Security Incident"

  Body:
    On [DATE], we discovered that [NUMBER] of your health records were accessed
    without authorization as part of a data breach affecting Weaver.

    What happened:
      - An unauthorized person gained access to patient health records
      - Your [SPECIFIC INFO] may have been viewed
      - No modifications or deletions were made

    What we've done:
      - Immediately revoked the unauthorized access
      - Notified the Privacy Commissioner
      - Implemented stronger security (new encryption, access controls)

    What you should do:
      - Change your password immediately
      - Monitor bank/credit accounts for unauthorized activity
      - Watch for phishing emails or suspicious calls
      - If you suspect fraud, contact [Bank], [Police], [Organization]

    Questions:
      - Call our privacy hotline: 0800 PRIVACY
      - Email: privacy@coastalalp.tech
      - Free credit monitoring: [provider] for 12 months

    More information: [Breach details page with timeline + FAQ]
```

**Affected Individual Monitoring:**

```yaml
12-Month Monitoring Program:
  - Credit monitoring: Free service for all affected individuals
  - Identity theft insurance: Coverage up to $100,000 (12 months)
  - Regular updates: Quarterly newsletter on breach remediation status
  - Remediation hotline: Free support line for affected individuals
  - Legal support: Access to lawyer if identity theft occurs

Cost: Organization pays all monitoring costs (no cost to individuals)
```

---

### Phase 4: Post-Incident (2-4 weeks)

**Root Cause Analysis & Lessons Learned:**

```yaml
Blameless Postmortem (Mandatory):
  - When: Within 1 week of incident resolution
  - Attendees: Incident Commander, engineers, security team, compliance
  - Facilitator: Senior leader (not directly involved in incident)
  - Tone: Non-punitive; focus on system failures, not individual blame

Postmortem Template:
  1. Timeline:
     - Exact sequence of events
     - What was detected and when?
     - How long from detection to containment?
  
  2. Root Cause:
     - Why did the incident happen?
     - Was it a known vulnerability, misconfiguration, or new attack?
     - Did existing controls fail? Why?
  
  3. Contributing Factors:
     - Technical: System design, tool gaps
     - Operational: Process gaps, training needs
     - Organizational: Unclear responsibilities, communication delays
  
  4. Impact:
     - How many records were affected?
     - How long was data exposed?
     - What's the financial/reputational cost?
  
  5. What Worked Well:
     - Automated alerts detected incident quickly
     - Incident Commander coordinated response effectively
     - Communication was timely + transparent
  
  6. What Didn't Work:
     - Forensic tools unavailable; manual investigation took 6 hours
     - Database backups weren't tested; couldn't restore clean version
     - Notification template wasn't prepared; delayed Privacy Commissioner notification
  
  7. Action Items (Preventive):
     - Action: [Specific change]
     - Owner: [Person responsible]
     - Deadline: [Date]
     - Status: [Open/In Progress/Closed]
  
  Example Actions:
    - Deploy new SIEM tool + train team (by [date])
    - Quarterly backup restoration test (schedule recurring)
    - Pre-draft notification template + legal review (by [date])
    - API key rotation every 60 days (vs. 90) (implement by [date])

  8. Document:
     - Store postmortem in shared wiki (accessible to all staff)
     - Summarize lessons learned for next team
     - Track action item completion
```

---

## Incident Response Plan Testing

**Quarterly Tabletop Exercise:**

```yaml
Scenario: "Health data breach affecting 100 patients. Discovered by automated alert.
            What's your response?"

Participants:
  - Incident Commander (rotate role)
  - Security team
  - Compliance officer
  - Customer support (for handling individual inquiries)
  - Legal counsel
  - Executive (CEO or CISO)

Timeline:
  - T+0: Incident declared; IC briefed on situation
  - T+15 min: Initial response plan decided
  - T+1 hour: Investigation underway; scope estimated
  - T+4 hours: Root cause identified; containment completed
  - T+24 hours: Privacy Commissioner notification drafted
  - T+72 hours: Individual notifications sent
  - T+1 week: Postmortem completed; action items assigned

Evaluation:
  - Did response meet SLAs? (detection → notification timing)
  - Were all stakeholders notified appropriately?
  - Was communication clear + timely?
  - Were there gaps or confusion?
  - What training do we need?

Document Results:
  - Attach test results to incident response plan
  - Track any issues identified + track to resolution
  - Share lessons learned with whole organization
```

**Annual Penetration Test:**

```yaml
Scope: Attempt to breach systems + extract health data
Frequency: Annual (external auditor)
Focus Areas:
  - API authentication + authorization (can we access other users' data?)
  - Encryption key access (can we extract keys?)
  - Database security (can we SQL inject or directly access DB?)
  - Backup security (can we access backups?)
  - Supply chain: Can we access via third-party integrations?

Output: Formal report with findings + remediation recommendations
Follow-up: Address all critical + high findings within 30 days
```

---

## Incident Severity Matrix

| Indicator | P0 | P1 | P2 | P3 |
|-----------|----|----|----|----|
| Records exposed | 100+ | 10-99 | 1-9 | 0 (suspected) |
| Health data? | Yes | Maybe | Unlikely | No |
| Active exploitation? | Yes | Possibly | No | No |
| Data exfiltration? | Yes | Possibly | No | No |
| System down? | Yes | Partial | No | No |
| Response time | 15 min | 1 hour | 4 hours | 1 day |
| Notification time | 24 hours | 72 hours | 10 days | 30 days |

---

## Emergency Contacts

```yaml
On-Call Rotation:
  - Monday-Friday 9am-5pm: [Name], [Email], [Phone]
  - Monday-Friday 5pm-9am: [On-call engineer], [Phone]
  - Weekends/holidays: [On-call rotation], [Phone], [Escalation contact]

Escalation Chain:
  Level 1: On-call engineer (respond within 5 min)
  Level 2: Security team lead (respond within 15 min for P0/P1)
  Level 3: CISO / Chief Compliance Officer (respond within 30 min for P0)
  Level 4: CEO (notify for P0 + Privacy Commissioner escalation)

External Contacts:
  Privacy Commissioner: breaches@privacy.org.nz, 0800 803 202
  Police (if criminal): 111 or local non-emergency
  Lawyers: [Firm name], [Contact]
  PR/Communications: [Internal contact]
  AWS Support (if infrastructure): [Premium support account number]
```

---

## Breach Register (Compliance Tracking)

Maintain spreadsheet (encrypted, access restricted):

| Date | Type | Severity | Records | Root Cause | Resolution | Status |
|------|------|----------|---------|-----------|------------|--------|
| 2026-03-15 | Unauthorized access | P2 | 5 | Weak password | Password reset + MFA enforced | Closed |
| 2026-05-22 | Data exfiltration attempt | P1 | 50 (attempted, 0 actual) | Compromised API key | Key rotated, firewall updated | Closed |

**Retention:** 7+ years (required by Privacy Commissioner)

