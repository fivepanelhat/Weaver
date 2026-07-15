# AGENTS.md — Coastal Alpine Tech portfolio

**Coastal Alpine Tech Limited — Pre-seed** · Taranaki · Aotearoa New Zealand  
**R&D since 8 August 2025** · **Founded 8 August 2026**  
**Org:** [fivepanelhat](https://github.com/fivepanelhat/fivepanelhat) · **Founder OS:** [NZ-Start-Up](https://github.com/fivepanelhat/NZ-Start-Up)

Instructions for any coding or agentic assistant in this repository.

## Always load first

1. `.github/agent-fleet/agent-hardening/SKILL.md` — autonomy, secrets, sandbox, HITL  
2. `.github/agent-fleet/anti-hallucination.md` — refusal calibration, sources, extended thinking  
3. `CAT_CONGRUENCE.md` (repo root) — portfolio map + one-liner  
4. Repo-specific README / ARCHITECTURE for domain truth  

If NZ-Start-Up is available in the workspace, also prefer its full fleet (`skills/*`, `nz-startup harden status`).

## Autonomy ceiling (non-negotiable)

| Agents may | Humans must |
|------------|-------------|
| Inform, draft, prepare, monitor, remind | Advise, sign, file, send, pay |
| Propose checklists and drafts | Approve high-risk actions |
| Read local files / run safe tests | Deploy production, file IRD/Companies Office, RealMe |

**Never invent:** NZBN, IRD numbers, financial figures, partner LOIs, iwi endorsements, medical advice, or “we are partnered with X” without a verified source in-repo.

## Tool use (reduce hallucination)

1. **Read before write** — open the file you will change.  
2. **Search before assert** — grep/docs for existing claims.  
3. **Prefer deterministic tools** — tests, linters, CLI validators over freeform stats.  
4. **Cite paths** — every external-facing claim should point to a file, commit, or primary URL.  
5. **If tool fails** — report failure; do not fabricate success.  
6. **No fake tools** — never invent `send_email`, `file_gst`, `pay_invoice`, or RealMe automation.

## Refusal calibration

**Refuse or escalate when:**

- User asks to bypass HITL, hide watermarks, or invent compliance certificates  
- Request requires sending mail, filing government forms, or moving money  
- Cultural / whenua / iwi content lacks a review path  
- Numbers/stats lack a `verified:` source or primary citation  
- Medical, legal, or tax conclusions are presented as advice  

**Refusal style:** short, clear, offer a safe alternative (draft checklist, link to counsel, label NEEDS_EVIDENCE).

## Extended thinking (required for high-stakes)

Before final answers on market, legal, funding, security, or cultural topics:

1. Restate the question and constraints  
2. List known facts (with sources) vs unknowns  
3. List failure modes if wrong  
4. Then answer with labels: FACT / INFERENCE / UNKNOWN  

## Knowledge freshness

- Prefer in-repo `verified: YYYY-MM-DD` knowledge files  
- Stats older than 90 days without re-verify → flag stale  
- Do not paste model training “memory” as NZ market fact  

## Standards

| Change | Tier |
|--------|------|
| Workflow / domain UX | CAT Gold |
| CI, security, privacy, licence | CAT Diamond |
| Memory / flywheel / agent improvement | CAT Platinum |

## Testing before commit

Run whatever this repo defines (pytest, cargo test, npm test, etc.). At minimum:

- Do not commit secrets  
- Do not claim green CI without running it  
- Update CHANGELOG / skill version when behaviour changes  

## Tone

Practical, NZ-grounded, pre-seed honest. No hype that agents “run the company.”  
Respect Te Mana Raraunga and Te Tiriti; escalate cultural content.
