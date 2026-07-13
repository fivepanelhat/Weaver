# Weaver Agents Changelog


## Hybrid platform update (July 2026)

- Dual-platform installers: `install.sh` (Linux/macOS) and `install.ps1` (Windows)
- Mermaid system maps updated for hybridisation (Core · Weaver · Aether · stack) and Windows + Linux hosts
- Architecture overview images refreshed for hybrid stack + dual OS targets
- Developer setup / installation docs cover Windows and Linux prerequisites and packages

All notable changes to the `weaver` repository will be documented in this file.

## [0.1.0] - 2026-07-13 — First public release

First tagged, public release of Weaver. This `0.1.0` marks the start of
public [semantic versioning](https://semver.org/); the `1.x` entries below
were **internal pre-release iterations** and are retained for history.

### Included
- `AgentOrchestrator` unified entrypoint with two routing modes: direct
  agent intake (`agents.py`) and the `weaver_graph` LangGraph state machine
  (`use_graph=True`).
- Tenant-isolated knowledge base (in-memory + SQLAlchemy clients) with
  cosine-similarity RAG retrieval; cross-tenant leakage covered by tests.
- Security gate on every message via Coastal-Alpine-Core `SecurityGuard`;
  telemetry via `TelemetryTracker`.
- Offline-capable local inference through Ollama (`gemma4:e4b`) with a
  deterministic fallback when disconnected.
- pytest suite (routing, escalation, tenant isolation, LLM fallback, demo
  smoke) plus an adversarial `tests_security_stress/` red-team suite.

### Changed for release
- Removed orphaned industrial edge-fleet modules (`src/`: MQTT black-box
  logger, fleet policy, OPC-UA bridge, TPM attestation) that did not belong
  to the helpdesk product; they remain in git history.
- Dockerfile entrypoint now runs the helpdesk demo instead of the removed
  black-box logger.
- Packaging: static `version = "0.1.0"` (previously an unresolved
  `dynamic` version that broke `pip install .` / `python -m build`).
- README: corrected directory structure; relabelled aspirational
  "real-world examples" as target scenarios and benchmarks as preliminary
  targets.

### Known limitations
- Fulfilment / Resolution agents are scaffolds; the graph path is the
  primary tested route.
- Requires a locally running Ollama for live inference (falls back offline).
- Proprietary licence — see [LICENSE](./LICENSE); no open-source grant.

## [1.3.0] - 2026-07-10

### Changed
- Renamed local `langgraph/` package to `weaver_graph/` (no longer shadows PyPI `langgraph`).
- Helpdesk intake performs real tenant-aware RAG retrieval and optional LLM routing (keyword fallback).
- Database engine is lazy-initialised; schema auto-create only when `WEAVER_AUTO_INIT_DB=1`.
- Batch vector embedding inserts via `TenantAwareDB.add_vector_embeddings_batch`.
- Default local model is `gemma4:e4b` via thin Ollama HTTP / Coastal-Alpine-Core client.
- `AgentOrchestrator` supports optional graph path (`use_graph=True`).

### Tests
- Expanded suite: routing, keyword escalation, tenant isolation, KB kwargs, LLM fallback.

## [1.2.0] - 2026-06-08

### Added
- Unified version bump alignment.
- Structured pre-commit hooks.

## [1.0.0] - 2026-06-07

### Added
- Integrated local `langgraph` state engine package.
- Scaffolding for multi-tenant database using SQLAlchemy models (`models.py`, `database.py`).
- Tenant-scoped retrieval interface in `knowledge_base.py`.
- Demonstration agent flow `demo.py`.
- Governance docs in `agent_knowledge_base/`.
- Standardized README, `.env.example`, `CHANGELOG.md`, `CONTRIBUTING.md`, and `requirements-dev.txt`.
- Added test suite validation under `tests/test_orchestrator.py`.
