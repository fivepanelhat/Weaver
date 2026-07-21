# Security Policy — Weaver

Sovereign multi-tenant AI routing and RAG orchestration at the edge.

## Supported Versions

| Branch / track | Supported |
| -------------- | --------- |
| `main` | Yes |

## Vulnerability Disclosure

Do **not** open public issues for security flaws.

Report via private GitHub Security Advisory or the Chief Architect. Include tenant-isolation impact if relevant.

## Security Notifications

| Channel | Response |
| ------- | -------- |
| Dependabot (pip + Actions) | Merge security PRs promptly; pin floors for `langsmith`, `pydantic-settings`, Core |
| Code scanning / Bandit / Gitleaks | Fix on `main`; no secrets in tree |
| Red team / stress suites | Expand guardrails; never weaken tenant ACLs for convenience |
| Core SDK advisories | Bump `coastal-alpine-core` and re-run pytest |

## Active patches (2026-07)

| ID | Mitigation |
| -- | ---------- |
| GHSA-f4xh-w4cj-qxq8 | `langsmith>=0.8.18` |
| GHSA-4xgf-cpjx-pc3j | `pydantic-settings>=2.14.2` |
| Prompt injection | Core `SecurityGuard` on all inbound LLM messages |
| GITHUB_TOKEN sprawl | CI `permissions: contents: read` |

## Local / edge hygiene

- `.env*`, `*.pem`, `*.key`, `secrets/` gitignored.
- Prefer mTLS MQTT (`ssl://…:8883`) in production.
- Pre-commit secret detection where enabled.

## Quality gates

- CI: install Core + requirements, flake8, pytest.
- SecOps + red-team scheduled workflows.

## Fleet security principles

- **No silent exfiltration** of personal or tenant operational data
- Prefer **local-first** processing; third-party AI only with explicit operator configuration and UI/docs disclosure
- Report vulnerabilities via GitHub Security Advisories or the maintainer contact on the org profile
- High-stakes production changes require human approval (HITL)

## Data sales and third parties

- **We do not sell personal information or customer operational data to third parties.**
- Optional AI or cloud services run only when configured by the operator; processing must be disclosed (in-product and/or docs).
- Prefer local-first paths so third-party transfer is unnecessary by default.

## NZ Privacy Act and Te Mana Raraunga

- Design in accordance with the **Privacy Act 2020**.
- Operate in accordance with **Te Mana Raraunga** principles for Māori data sovereignty interests.
- Align AI features with **NZ AI safety** / responsible AI expectations (HITL, transparency, no silent training on private content).

