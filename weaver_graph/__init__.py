"""Weaver lightweight state-graph package (edge-friendly, no LangGraph dep required at runtime).

Named ``weaver_graph`` so it does not shadow the optional PyPI ``langgraph`` package.
"""

from .graph import StateGraph, END
from .orchestrator import build_agnostic_helpdesk, HelpdeskState
from .llm import LocalSovereignLLM

__all__ = [
 "StateGraph",
 "END",
 "build_agnostic_helpdesk",
 "HelpdeskState",
 "LocalSovereignLLM",
 "ingestion",
 "embeddings",
 "graph",
 "orchestrator",
 "llm",
]
