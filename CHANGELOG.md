# Weaver Agents Changelog

All notable changes to the `weaver` repository will be documented in this file.

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
