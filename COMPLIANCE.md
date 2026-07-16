# Weaver Compliance & Regulatory Framework Guide

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
