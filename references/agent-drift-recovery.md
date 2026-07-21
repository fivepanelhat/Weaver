# Agent Drift Recovery Protocol

When Grok Build or any agent produces output that diverges from the product’s ARCHITECTURE.md or AGENTS.md:

1. Stop further generation on the drifted artefacts.
2. Load `cat-architecture-congruence` skill + the product’s triad documents.
3. Explicitly name the drift (what was produced vs what the architecture requires).
4. Propose a concrete re-alignment plan.
5. Obtain explicit human approval before accepting or rewriting the drifted work.
6. After re-alignment, update the triad if new durable decisions were made.

Never silently accept architectural drift.

This protocol is mandatory for all CAT products.
