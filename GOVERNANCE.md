# Governance — CAT Architectural Standards

This repository is governed by the **Coastal Alpine Tech (CAT) Architectural
Standards** maturity model (Gold / Diamond / Platinum). The canonical decision
skill lives in the [Aether](https://github.com/fivepanelhat/Aether) repo at
`skills/cat-architectural-standards/SKILL.md`.

## Tier classification

| Tier | Role | Applies to Weaver as |
| :--- | :--- | :--- |
| **Platinum** *(primary)* | Intelligent self-improving system | Multi-tenant agentic mesh — local LangGraph orchestration and per-tenant RAG that improve with use while data stays partitioned at the edge. |
| **Diamond** *(secondary)* | Enterprise-grade foundation | Strict tenant isolation (SQLAlchemy + partitioned vector stores), security scanning, least-privilege CI, offline-first reliability. |
| **Gold** *(secondary)* | Workflow-native design | Intake → Fulfilment → Resolution agents mirror a real helpdesk lifecycle as an unbroken data chain. |

## Operating rules

- **Classify before building.** Declare the primary (and any secondary) tier in
  each PR/ADR.
- **HITL gates are non-negotiable:** changes to tenant-isolation guarantees,
  classification, security posture, data sovereignty, or any tier-compliance
  release claim require human approval.
- **Sovereignty overlay applies to all tiers.** Te Tiriti o Waitangi and Te Mana
  Raraunga principles are architectural requirements — tenant data stays local
  and strictly partitioned; no silent cloud exfiltration.

## References

- Aether: `skills/cat-architectural-standards/SKILL.md` — decision protocol
- `SECURITY.md`, `COMPLIANCE.md`, `ARCHITECTURE.md` — Diamond/sovereignty detail
