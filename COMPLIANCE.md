# COMPLIANCE.md

**Coastal Alpine Tech Limited** | **Product:** Weaver
Last updated: 19 July 2026

## Privacy · Security · Governance (fleet mandatory)

| Pillar | Standard |
| --- | --- |
| **Privacy** | Local-first default; purpose-limited collection; Privacy Act 2020; Te Mana Raraunga spirit; third-party processing only when opt-in and disclosed |
| **Security** | No silent exfil; owner-controlled credentials; least privilege; SecOps / red-team cadence where CI is present |
| **Governance** | HITL for high-stakes; agents draft only; humans sign / send / pay |

Last reviewed (fleet block): 2026-07-21

> Super Grok compliance briefing (19 July 2026). This is **alignment evidence**, not a compliance certificate or legal advice.

## Regulatory Mapping

### New Zealand
- Privacy Act 2020 + **IPP 3A** (Privacy Amendment Act 2025) - effective **1 May 2026**  
  Notification required when personal information is collected indirectly.
- Biometric Processing Privacy Code 2025  
  New biometric processing: 3 November 2025  
  Existing biometric processing: 3 August 2026
- Health Information Privacy Code (applies where health / wellbeing data is processed)
- Te Mana Raraunga principles - primary data sovereignty framework

### European Union
- **EU AI Act** - Annex III high-risk obligations enforceable **2 August 2026**
- Relevant high-risk categories:
  - Health decision support
  - Biometrics (remote identification, categorisation, emotion recognition)
  - Critical infrastructure / essential services
- Required: risk management, data governance, technical documentation, human oversight, logging, transparency, post-market monitoring

### International Standards
- **ISO/IEC 42001** - AI Management System (AIMS)  
  Covers AI policy, risk assessment, data governance, human oversight, monitoring, continual improvement
- **SOC 2** - Security, Availability, Confidentiality, Processing Integrity, Privacy  
  Priority for multi-tenant / customer-facing components

### Core Technical Controls (Mandatory)
- Local-first / offline-native processing by default
- Owner-controlled encryption keys
- No silent data exfiltration
- Explicit Human-in-the-Loop (HITL) gates for high-impact and culturally sensitive decisions
- Data residency under New Zealand control

### Scope Notes
- Current systems prioritise offline-native operation and data minimisation.
- Any future multi-tenant or customer-facing features will be assessed against SOC 2 and EU AI Act high-risk requirements before release.

### Limitations
- Not legal advice; not a certification claim.
- Confirm statute application with NZ counsel before commercial shipping claims.
- Agents inform / draft / prepare only; humans advise / sign / file / send / pay.

---

## Product-specific mapping

This guide outlines how the **Weaver** multi-tenant agentic helpdesk engine complies with New Zealand legislation and customary data rights in on-premise and edge configurations.

---

## 1. Privacy Act 2020 & Information Privacy Principles (IPPs)

Weaver processes user tickets, support chats, and enterprise files. It enforces the Privacy Act 2020 requirements directly at the database and application layer:

* **IPP 1 (Purpose of collection) & IPP 2 (Source of personal information):** Scopes customer intake parameters. Ticket context is processed locally via LangGraph to determine appropriate routing without publishing records to cloud engines.
* **IPP 5 (Storage & Security):** Ensures strict tenant partitioning. Multi-tenant database entries use SQLAlchemy tenant scope checks (`coastal_alpine_core.security.tenant_isolated_query`), keeping customer records isolated.
* **IPP 6 (Access) & IPP 7 (Correction):** Database models support programmatic extraction of all customer interaction logs and vector embeddings linked to a tenant ID for audit exports.
* **IPP 11 (Limits on disclosure):** Because Weaver runs 100% offline on local hardware, customer communications are immune to inadvertent cloud security disclosures or unauthorized web scraping.

---

## 2. Public Records Act 2005

For New Zealand public sector organisations, local councils, and public services utilising Weaver:
* **Record Integrity:** Weaver automatically maintains an immutable, chronological audit trail of all customer interactions in the `interaction_logs` relational table.
* **Metadata Standardisation:** Interaction records are timestamped and annotated with tenant identifiers, allowing easy integration with council records management archives.
* **Retain & Dispose:** Storage capacity managers can be scheduled to prune temporary vector stores while safeguarding long-term compliance metadata in standard SQL outputs.

---

## 3. Māori Data Sovereignty (Te Mana Raraunga)

* **Te Mana o te Raraunga:** Personal information, oral history files, and customary land registry data vectorized for RAG systems represent digital expressions of *whakapapa* and *taonga*.
* **Local Guardianship:** Weaver is compiled and deployed locally in New Plymouth, Taranaki. By avoiding offshore clouds (such as AWS, GCP, or Azure), iwi trust entities retain custody of their digital records on their own physical *whenua* (land).
* **Consent Controls:** Tenant configurations allow administrators to restrict RAG vector indexing to certified internal models, ensuring information remains protected under customary authority boundaries.
