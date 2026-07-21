# COMPLIANCE_REGIONS.md

**Coastal Alpine Tech Limited**  
Last updated: 22 July 2026

> Multi-region compliance **mapping** under a **New Zealand AI safety-first** baseline.  
> **Not legal advice.** **Not** a claim of ISO, SOC 2, GDPR, EU AI Act, or APP certification unless a formal independent report is published for a named product.

## 0. Non-negotiable commercial & privacy stance

| Rule | Statement |
| --- | --- |
| **No data sales** | Coastal Alpine Tech **does not sell** personal information or customer operational datasets to third parties for advertising, brokerage, model-marketplaces, or unrelated commercial exploitation. |
| **No silent exfil** | Product defaults avoid sending personal/operational content to third parties without explicit operator configuration and disclosure (e.g. optional AI keys labelled in-product). |
| **NZ home baseline** | All products are designed first for **Aotearoa New Zealand** law, culture, and AI safety posture; overseas maps are **interoperability alignments**, not a dilution of NZ commitments. |

---

## 1. New Zealand (home jurisdiction) — AI safety baseline

CAT products are designed to operate **in accordance with**:

| Instrument | How we align |
| --- | --- |
| **Privacy Act 2020** | IPP-based collection/use/disclosure/security/access; purpose limitation; reasonable safeguards |
| **Privacy Amendment Act 2025 / IPP 3A** | Awareness of notification duties when personal information is collected from third parties (effective 1 May 2026) |
| **Te Mana Raraunga** | Operate **in accordance with** Māori data sovereignty principles (Rangatiratanga, Whakapapa, Whanaungatanga, Kotahitanga, Manaakitanga, Kaitiakitanga) as stewardship obligations for Māori data and community data interests |
| **Algorithm Charter for Aotearoa NZ** (spirit) | Fairness, transparency, partnership, human oversight where algorithms affect people |
| **Responsible AI / digital.govt.nz & CDEI guidance** | Human accountability, risk-aware deployment, cultural safety considerations for AI |
| **Sector law (product-specific)** | e.g. WorkSafe-related records, biosecurity, RMA/water — documented per product README |

### NZ AI safety operating principles (fleet)

1. **Human-in-the-loop** for high-stakes outcomes (legal, clinical, financial, safety-critical, cultural).  
2. **Transparency** when AI processes personal or sensitive operational content.  
3. **Local-first** preference to reduce unnecessary cross-border transfer.  
4. **No silent training** on private customer journals/tenants without explicit consent and contract.  
5. **Kaitiakitanga** — protect data quality, access, and purpose over extractive reuse.

---

## 2. Australia

Designed for **interoperability** with Australian expectations when deploying for AU customers or dual NZ–AU operations:

| Instrument | Alignment approach |
| --- | --- |
| **Privacy Act 1988 (Cth) & Australian Privacy Principles (APPs)** | Purpose limitation, security (APP 11), cross-border disclosure controls (APP 8), access/correction |
| **Notifiable Data Breaches scheme** | Incident readiness and notification workflows for eligible breaches |
| **Australia’s AI Ethics Principles** (DISR) | Human-centred values, fairness, privacy protection, reliability, transparency, accountability |
| **OAIC guidance** on AI & privacy | Privacy-by-design for AI features; minimise training on personal information |

**NZ AI safety bridge:** AU deployments inherit NZ HITL / no-data-sale / no-silent-exfil defaults; AU APP obligations are treated as additional floors, not replacements for NZ Privacy Act + Te Mana Raraunga.

---

## 3. Asia-Pacific (selected frameworks)

Regional deployments map to commonly adopted APAC frameworks (product contracts specify the exact market):

| Framework | Alignment approach |
| --- | --- |
| **Singapore PDPA** + **Model AI Governance Framework** | Consent/notification, purpose limitation, accountability, AI governance documentation |
| **Japan APPI** | Proper acquisition, purpose specification, security control measures |
| **Korea PIPA** | Consent and overseas transfer controls where applicable |
| **ASEAN Guide on AI Governance and Ethics** | Transparency, fairness, human-centricity, robustness |
| **Aotearoa–Asia trade & data** | Prefer contractual data residency options (NZ/Oceania first) over unrestricted transfer |

**NZ AI safety bridge:** Asia deployments keep Te Mana Raraunga / NZ Privacy Act design defaults for CAT-operated systems; local PDPA/APPI terms are layered via DPA / customer agreements.

---

## 4. Europe

| Instrument | Alignment approach |
| --- | --- |
| **GDPR / UK GDPR** | Lawful basis, purpose limitation, data minimisation, security of processing, DPIA mindset for higher-risk AI, international transfer tools (SCCs) when needed |
| **EU AI Act** | Transparency & human oversight for AI systems; risk-tier awareness; documentation and logging for higher-risk uses if ever claimed |
| **ePrivacy (as applicable)** | Care with communications content and metadata |
| **NIS2 (where applicable)** | Cyber risk management for essential/important entities if a product is deployed in scope |

**NZ AI safety bridge:** EU features do not weaken NZ “no data sale / HITL / local-first” defaults. Cross-border processing requires explicit configuration and contractual transfer mechanisms.

---

## 5. Assurance frameworks (SOC 2, ISO, etc.)

| Framework | CAT posture |
| --- | --- |
| **SOC 2 (Trust Services Criteria)** | **Alignment path** for multi-tenant SaaS (Security, Availability, Confidentiality, Processing Integrity, Privacy). Not claimed as certified until an independent Type I/II report is issued for a named system. |
| **ISO/IEC 27001** | Information security management **direction** for mature hosted offerings |
| **ISO/IEC 42001** | AI management system **direction** (policy, risk, human oversight, monitoring) |
| **ISO/IEC 27701** | Privacy information management **direction** where PII is systematically processed |

Engineering controls that support future assurance: access control, audit logging, change management via PRs, secret hygiene, vulnerability scanning (SecOps/RedTeam/CI where present), encryption in transit for hosted paths, least privilege.

---

## 6. What “in accordance with” means here

- Product **architecture and defaults** are designed against these instruments.  
- **Not** a warranty that every deployment automatically meets every overseas statute without configuration, contracts, and legal review.  
- Customer-specific regulated use (health, children’s data, critical infrastructure) requires a **written assessment** and may require additional controls.  
- Contact NZ counsel / local counsel for commercial claims, tenders, and cross-border DPAs.

---

## 7. Document control

| Field | Value |
| --- | --- |
| Owner | Coastal Alpine Tech Limited |
| Applies to | All fivepanelhat / CAT fleet products unless a product COMPLIANCE.md narrows scope |
| Companion | `COMPLIANCE.md`, `SECURITY.md`, `CAT_CONGRUENCE.md` |
| Review cadence | On material product or legal change; fleet reaffirmation after Super Grok / compliance drops |

