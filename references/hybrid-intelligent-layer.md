# Hybrid Intelligent Layer Pattern

Extracted from ScaffyLads architecture session (2026-07-20).

## Preferred Shape for CAT Domain Products

```
Client Layer
  Next.js (Web + PWA) + Tauri 2 (Windows / Linux Desktop)
  Tailwind + consistent glassmorphism design system
        ↓
Intelligent Layer (Python / FastAPI)
  - Domain CRUD
  - Voice → structured entry
  - Natural language query engine (“Ask X”)
  - Reports, compliance helpers, structured extraction
  - Optional local LLM / RAG
        ↓
Data Layer
  Local-first: SQLite (desktop) / IndexedDB (web)
  Progressive: optional Supabase (Auth + Postgres + Storage + RLS)
  Future: CAT edge nodes (RPi 5 + Hailo)
```

## Rules

- Keep the UI shell and the intelligent layer clearly separated.
- Default to local-first. Cloud is opt-in and requires explicit consent design.
- Prefer FastAPI for any new intelligent / agentic / NL layer so it stays congruent with Weaver, Aether Python tooling, and edge deployment paths.
- Natural language query interfaces should operate over structured domain logs (journals, telemetry, inspections) with source citation.

## When to Apply

Any new CAT vertical (scaffolding, microgreens, soil, water, biosecurity, etc.) should start from this shape unless there is a strong, documented reason to deviate.
