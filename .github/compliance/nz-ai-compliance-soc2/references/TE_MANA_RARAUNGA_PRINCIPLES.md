# Te Mana Raraunga — Māori Data Sovereignty Framework

**Authority:** Te Mana Raraunga — The Māori Data Sovereignty Network  
**Alignment:** UN Declaration on Rights of Indigenous Peoples (UNDRIP)  
**Context:** Aotearoa New Zealand + diaspora Māori communities  
**Applies to:** Any system handling Māori/Iwi/Hapū/whānau data

---

## Core Principles (OCAP® Framework)

### Ownership — Tino Rangatiratanga

**Principle:** Māori collectives (iwi, hapū, whānau) own their data.

Organizations are **stewards, not owners**. Māori data is not an asset to be exploited.

**Implementation:**

```yaml
Ownership Registry:
  - Maintain master list of all Māori data collected
  - Link each dataset to responsible iwi/hapū/whānau
  - Document ownership transfer (if delegated to organization)
  - Quarterly: verify ownership status with communities

Example Ownership Statement:
  Dataset: "Whakapapa + health outcomes (Te Waihou Iwi Members)"
  Owner: Te Waihou Iwi Trust
  Steward: Weaver (Coastal Alpine Tech)
  Purpose: Health service improvement for whānau
  Authority: Signed data use agreement + Cultural Advisory Board approval
```

---

### Control — Manaakitanga (Guardianship)

**Principle:** Māori must have authority over who can access, use, modify their data.

**Implementation:**

```yaml
Access Control Layers:
  Layer 1: Community Gatekeeper
    - Iwi Cultural Advisor reviews data access requests
    - Veto power: can refuse access for cultural reasons
    - Timeline: 5 working days for decision
  
  Layer 2: Technical Access Control
    - RBAC: roles include "cultural-reviewer" + "data-custodian"
    - Encryption key: iwi holds master key (separate from organization)
    - Audit log: all access logged + reported to iwi quarterly
  
  Layer 3: Purpose Limitation
    - Data use strictly limited to stated purpose
    - No secondary use without iwi consent
    - No data mining / machine learning without explicit permission
    - No third-party sharing without consent

Data Use Agreement Template:
  Title: "Relationship Agreement for [Dataset Name]"
  Parties: [Iwi Name], Weaver/Aether/Coastal Alpine Tech
  Purpose: [Specific use case, e.g., "health improvement research"]
  Duration: [End date, e.g., "2028-12-31"]
  Governance: [Cultural Advisory Board oversight]
  Modification: [How to request changes or terminate]
  Cancellation: [Either party can cancel with 30 days notice]
  Signature: [Iwi leader, Coastal Alpine Tech CEO, Cultural Advisor]
```

---

### Access — Whānaungatanga (Reciprocal Relationships)

**Principle:** Data access must be based on reciprocal relationships + benefit-sharing.

**Implementation:**

```yaml
Benefit-Sharing Model:
  Direct Benefit:
    - Health outcomes: whānau gets improved health service
    - Data literacy: community trained to interpret their own data
    - Employment: iwi members hired for data roles
  
  Community Benefit:
    - Revenue sharing: if insights generate commercial value, iwi receives share
    - Capacity building: provide data analysis tools to community
    - Knowledge transfer: teach iwi to manage data independently
  
  Transparency & Relationships:
    - Annual community forum: review data use, outcomes, benefits
    - Whānau hui: cultural gathering to discuss new uses
    - Relationships: regular (monthly) check-ins with iwi leadership
    - Feedback loop: act on community concerns promptly

Example Benefit-Sharing:
  Product: "Health app for Māori wellness tracking"
  Commercial value: $2M Series A funding
  Benefit-sharing arrangement:
    - Iwi receives: 2% of future revenue (if profitable)
    - Community receives: Free access to app
    - Employment: 5 Māori analysts hired for data team
    - Training: Annual "data for social good" workshop
```

---

### Possession — Kaitiakitanga (Guardianship of Resources)

**Principle:** Physical + logical control of data must remain with Māori (or trusted steward).

**Implementation:**

```yaml
Data Localization:
  Requirement: Māori/Iwi data must be stored on servers in Aotearoa New Zealand
  Prohibition: No storage in US cloud (AWS, Azure, Google Cloud without encryption + local key)
  Storage Location: Specify jurisdiction in data use agreement
  Example:
    - Approved: AWS (Auckland region) with NZ-held encryption key
    - Prohibited: AWS (us-east-1) with AWS-managed encryption key
    - Approved: On-premise (iwi data center or Coastal Alpine Tech NZ office)

Encryption Key Management:
  Primary key: Held by iwi (hardware security module, offline storage)
  Operational key: Held by organization (HSM, Vault)
  Key rotation: Annual (iwi must approve)
  Access log: Every key operation (creation, rotation, deletion) logged + reported

Data Deletion:
  Timeline: On request, delete within 30 days
  Proof: Provide certificate of deletion (cryptographic hash of deleted data)
  Backups: Purge from backup systems within 90 days
  Verification: Iwi can verify deletion (restore from random backup, confirm missing)

Physical Security:
  Data center: Only Coastal Alpine Tech staff + iwi designates may access
  Video surveillance: 24/7, footage retained 90 days, reviewed upon request
  After-hours access: Requires iwi approval + notification
```

---

### Possession + Ownership (Dual)

**Principle:** In sensitive cases, both organization + iwi hold encryption keys (threshold cryptography).

**Implementation:**

```yaml
Threshold Encryption (3-of-5 keys):
  Keys held by:
    1. Iwi Cultural Advisor (hardware security module)
    2. Iwi CEO (separate HSM)
    3. Coastal Alpine Tech Chief Technology Officer (Vault)
    4. External auditor / notary (custody)
    5. Backup key (sealed, held by legal counsel)
  
  To decrypt data:
    - Minimum 3 keys required
    - Iwi must participate (holds 2 keys)
    - Organization cannot unilaterally decrypt
    - Audit trail: when keys are used, who used them, for what purpose

High-Sensitivity Data:
  Examples: Genealogy (whakapapa), sacred knowledge, health + mental health data
  Storage: Threshold encryption mandatory
  Access: Requires iwi + organization authorization (dual sign-off)
```

---

## Mātauranga Māori (Māori Knowledge) Protection

**Principle:** Cultural knowledge, traditional practices, traditional ecological knowledge (TEK) requires special protection.

**Implementation:**

```yaml
Cultural Knowledge Classification:
  Level 1: Public
    - General health promotion tips
    - Community event announcements
    - Published research with consent
  
  Level 2: Restricted (Community Only)
    - Specific health practices (rongoā Māori)
    - Whakapapa (genealogy) information
    - Spiritual/cultural significance of practices
    - Access: Māori whānau + authorized researchers only
  
  Level 3: Sacred (Iwi Leadership Only)
    - Waiata (songs), karakia (prayers) with spiritual power
    - Tohunga Whakairo (carving knowledge)
    - Secrets of rongoā Māori
    - Access: Iwi leaders + cultural experts only

Cultural Advisor Role:
  Responsibility: Determine classification level for all data
  Authority: Can request data deletion if classified improperly
  Engagement: Quarterly meetings with data team
  Training: All staff receive cultural competency training (annual)

Intellectual Property Protection:
  - Copyright: Māori authors/creators retain copyright
  - Attribution: Must credit iwi/whānau for knowledge contributions
  - Derivative works: Cannot modify cultural knowledge without consent
  - Perpetual rights: Community retains rights in perpetuity (not "until contract ends")
```

---

## Whakahaere Raraunga (Data Governance) Structure

```
┌─────────────────────────────────────────────┐
│ Iwi Leadership (Rangatira)                  │
│ - Final authority on data use               │
│ - Approves new uses/secondary purposes      │
└─────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────┐
│ Cultural Advisory Board (Monthly)           │
│ - Iwi Cultural Advisor                      │
│ - Kaumātua (elders)                         │
│ - Community health representative           │
│ - Data scientist (māori preferably)         │
│ - Organization liaison                      │
│ Decision: Approve/reject new data uses      │
└─────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────┐
│ Data Stewardship Team (Weekly)              │
│ - Data Custodian (organization)             │
│ - Iwi Data Officer                          │
│ - Compliance Officer                        │
│ - Security Officer                          │
│ Responsibility: Day-to-day data management  │
└─────────────────────────────────────────────┘
```

---

## Data Use Agreement (Template)

**This is a BINDING LEGAL DOCUMENT. Engage iwi lawyers + community.**

```
RELATIONSHIP AGREEMENT FOR MĀORI DATA STEWARDSHIP

Between:
  [Iwi Name] (Owner) and 
  Coastal Alpine Tech / Weaver / Aether / Core (Steward)

Purpose:
  To enable [specific purpose] for the benefit of [community name] whānau,
  in accordance with Te Mana Raraunga principles.

Data Description:
  Dataset: [e.g., "Health outcomes for whānau members, 2020–2026"]
  Elements: [e.g., age, health conditions, medications, appointments]
  Volume: [e.g., "500 whānau members"]
  Sensitivity: Level [1/2/3 per classification above]

Ownership & Control:
  Owner: [Iwi Name] retains all ownership rights
  Steward: [Organization] holds data on trust
  Encryption Key: [Specify who holds master key]
  Duration: [Start date] to [End date], renewable annually

Governance:
  Cultural Advisory Board: [Names + roles]
  Review frequency: [Monthly/quarterly]
  Veto authority: CAB can refuse new uses or terminate
  Community hui: [Frequency] to inform community

Benefit-Sharing:
  Direct: [E.g., free app access for whānau]
  Revenue: [E.g., 2% if commercial success]
  Employment: [E.g., 3 Māori data roles]
  Training: [E.g., annual data literacy workshop]

Data Use Restrictions:
  Approved uses:
    - Health service improvement for whānau
    - Anonymous research (k-anonymity ≥10)
  Prohibited uses:
    - Marketing / commercial targeting
    - Third-party sale or sharing
    - Machine learning without consent
    - Genealogy research without cultural approval

Data Security:
  Encryption: [Specify algorithm + key management]
  Access control: [Specify roles + audit logging]
  Monitoring: [Specify continuous monitoring]
  Incident response: [Specify SLA for breach notification]

Data Deletion:
  On request: [E.g., 30 days]
  End of agreement: [E.g., 90 days after termination]
  Proof: [Certificate of deletion provided]

Termination:
  Either party may terminate with [30 days] notice
  No reason required
  Upon termination: all data deleted within [90 days]

Dispute Resolution:
  Process: [Escalation path, arbitration process]
  Governing law: Aotearoa New Zealand
  Cultural protocols: Māori alternative dispute resolution (whakatupuranga)

Signatures:
  [Iwi Rangatira], [Date], [Title]
  [Organization CEO], [Date]
  [Cultural Advisor], [Date] (as witness)
```

---

## Compliance Verification Checklist (Te Mana Raraunga)

- [ ] Data ownership registry: maintained + reviewed quarterly
- [ ] Cultural Advisory Board: established + meeting monthly
- [ ] Data use agreements: signed for all Māori datasets
- [ ] Encryption key: iwi holds master key (or threshold system in place)
- [ ] Data localization: all Māori data stored in Aotearoa (verified)
- [ ] Cultural classification: all data classified Level 1/2/3
- [ ] Staff training: annual cultural competency (100% completion)
- [ ] Community hui: annual meeting to review data uses + outcomes
- [ ] Access audit: log all Māori data access (weekly review)
- [ ] Benefit-sharing: tracking + reporting to iwi (quarterly)
- [ ] Deletion: processes documented + tested annually
- [ ] Incident response: breach notification SLA ≤72 hours (to iwi + Privacy Commissioner)

---

## Common Pitfalls (Anti-Patterns)

❌ **"We're anonymized, so we don't need consent"**  
→ Re-identification risk for small Māori communities (k-anonymity <10). Consent required.

❌ **"We'll ask permission after we've already used the data"**  
→ Violates OCAP principles. Get consent BEFORE collection.

❌ **"We'll store data in US cloud with encryption; iwi has no jurisdiction"**  
→ Violates Possession principle + data localization requirement. Store in Aotearoa.

❌ **"Machine learning on Māori health data = innovation"**  
→ Without explicit consent, violates Control principle. Cannot build models without permission.

❌ **"We asked one iwi member; that's enough consent for the whole iwi"**  
→ Māori data is collective. Need iwi leadership + Cultural Advisory Board approval.

---

## Resources & References

- **Te Mana Raraunga Website:** https://www.temanararaunga.maori.nz/
- **OCAP® Principles:** https://fnigc.ca/ocap-principles/ (Canadian Indigenous context; principles apply globally)
- **Aotearoa New Zealand AI Framework:** https://www.mbie.govt.nz/dmsdocument/19433-responsible-artificial-intelligence-framework
- **Health Information Privacy Code 2020:** Commissioner guidance on Māori health data
- **Te Ara Tika — Guiding Principles for Research Involving Māori:** https://www.nhmrc.gov.au/about-us/publications/ara-tika

