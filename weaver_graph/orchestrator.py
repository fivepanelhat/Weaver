"""Agnostic multi-tenant helpdesk graph with real RAG + LLM hooks."""

from __future__ import annotations

import logging
from typing import TypedDict, List, Annotated, Any, Optional
import operator

from weaver_graph.graph import StateGraph, END

logger = logging.getLogger("weaver.graph.orchestrator")


class HelpdeskState(TypedDict):
 tenant_id: str
 brand_voice: str
 escalation_rules: dict
 user_message: str
 retrieved_context: str
 classification: str
 conversation_history: Annotated[List[str], operator.add]


def _extract_docs_text(docs: Any) -> str:
 if not docs:
 return ""
 parts: List[str] = []
 for d in docs:
 if hasattr(d, "page_content"):
 parts.append(str(d.page_content))
 elif isinstance(d, dict):
 parts.append(str(d.get("content") or d.get("page_content") or d.get("content_payload") or ""))
 else:
 parts.append(str(d))
 return "\n".join(p for p in parts if p).strip()


def _retrieve_context(
 state: HelpdeskState,
 vector_db_client: Any = None,
 kb_client: Any = None,
 top_k: int = 3,
) -> str:
 """Tenant-aware retrieval via vector DB or knowledge base client."""
 query = state.get("user_message") or ""
 tenant_id = state.get("tenant_id") or ""

 # Prefer explicit vector DB (tests / production adapters)
 if vector_db_client is not None:
 try:
 if hasattr(vector_db_client, "similarity_search"):
 docs = vector_db_client.similarity_search(
 query, filter={"tenant_id": tenant_id}, k=top_k
 )
 text = _extract_docs_text(docs)
 if text:
 return text
 if hasattr(vector_db_client, "query"):
 results = vector_db_client.query(query, tenant_id=tenant_id, top_k=top_k)
 text = _extract_docs_text(results)
 if text:
 return text
 except Exception as e:
 logger.warning("Vector retrieval failed: %s", e)

 # Knowledge base client (InMemory / SQLAlchemy)
 if kb_client is not None:
 try:
 results = kb_client.query(query, tenant_id=tenant_id, top_k=top_k)
 text = _extract_docs_text(results)
 if text:
 return text
 except Exception as e:
 logger.warning("KB retrieval failed: %s", e)

 return state.get("retrieved_context") or ""


def _keyword_route(message: str, rules: Optional[dict] = None) -> str:
 lower = message.lower()
 rules = rules or {}
 require_human = str(rules.get("require_human_for", "")).lower()
 escalate_keywords = (
 "angry",
 "anger",
 "refund",
 "lawyer",
 "sue",
 "safety",
 "urgent emergency",
 "manager",
 )
 if require_human and require_human.replace("_", " ") in lower:
 return "escalation"
 if any(k in lower for k in escalate_keywords):
 return "escalation"
 return "fulfilment"


def _llm_route(
 state: HelpdeskState,
 context: str,
 llm: Any = None,
) -> tuple[str, str]:
 """
 Returns (classification, response_text).
 classification is 'fulfilment' | 'escalation'.
 """
 message = state.get("user_message") or ""
 rules = state.get("escalation_rules") or {}
 brand = state.get("brand_voice") or "Professional and helpful."

 # Keyword fast-path first (cheap, deterministic)
 keyword = _keyword_route(message, rules if isinstance(rules, dict) else {})

 if llm is None:
 if keyword == "escalation":
 return "escalation", (
 "I understand this needs careful attention. "
 "Connecting you with a human advisor."
 )
 return "fulfilment", (
 "Let me check that against our policies and records."
 )

 prompt = (
 "You are a tenant-scoped helpdesk router. Respond with EXACTLY two lines:\n"
 "ROUTE: fulfilment|escalation\n"
 "REPLY: <one short customer-facing sentence>\n\n"
 f"Brand voice: {brand}\n"
 f"Escalation rules: {rules}\n"
 f"Retrieved policy context:\n{context or '(none)'}\n\n"
 f"Customer message: {message}\n"
 )
 try:
 raw = str(llm.invoke(prompt)).strip()
 except Exception as e:
 logger.warning("LLM route failed, using keywords: %s", e)
 if keyword == "escalation":
 return "escalation", "I'll escalate this to a human specialist."
 return "fulfilment", "I'll look that up in our local knowledge base."

 route = keyword
 reply = ""
 upper = raw.upper()
 if "ROUTE:" in upper:
 for line in raw.splitlines():
 if line.upper().startswith("ROUTE:"):
 val = line.split(":", 1)[-1].strip().lower()
 if "escalat" in val:
 route = "escalation"
 elif "fulfil" in val or "fulfill" in val:
 route = "fulfilment"
 if line.upper().startswith("REPLY:"):
 reply = line.split(":", 1)[-1].strip()
 elif "ESCALATE" in upper:
 route = "escalation"

 # Safety: never downgrade keyword escalation without explicit fulfilment
 if keyword == "escalation" and route != "fulfilment":
 route = "escalation"

 if not reply:
 reply = (
 "I'll connect you with a human advisor."
 if route == "escalation"
 else "I'll help with that using our local policies."
 )
 return route, reply


def agnostic_intake_node(state: HelpdeskState, *args, **kwargs):
 """
 Frontline agent: retrieves tenant-specific context and categorizes intent.

 Optional injected deps (positional or keyword):
 vector_db_client / vdb
 llm
 kb_client
 """
 vector_db_client = kwargs.get("vector_db_client")
 kb_client = kwargs.get("kb_client")
 llm = kwargs.get("llm")

 # Positional convenience: graph.run(state, vdb, llm) as used by tests
 if len(args) >= 1 and vector_db_client is None:
 vector_db_client = args[0]
 if len(args) >= 2 and llm is None:
 llm = args[1]
 if len(args) >= 3 and kb_client is None:
 kb_client = args[2]

 logger.info("Intake for tenant=%s", state.get("tenant_id"))

 context_str = _retrieve_context(state, vector_db_client=vector_db_client, kb_client=kb_client)
 next_step, response_text = _llm_route(state, context_str, llm=llm)

 return {
 "retrieved_context": context_str,
 "classification": next_step,
 "conversation_history": [f"AI: {response_text}"],
 }


def fulfilment_node(state: HelpdeskState, *args, **kwargs):
 """Handles standard operational tasks (e.g., checking order DBs)."""
 logger.info("Fulfilment for tenant=%s", state.get("tenant_id"))
 ctx = (state.get("retrieved_context") or "").strip()
 if ctx:
 summary = ctx.splitlines()[0][:240]
 msg = f"AI: Fulfilment task complete. Based on our records: {summary}"
 else:
 msg = "AI: Fulfilment task complete."
 return {"conversation_history": [msg]}


def escalation_node(state: HelpdeskState, *args, **kwargs):
 """Pushes complex or rule-breaking queries to a human queue."""
 logger.info("Escalation for tenant=%s", state.get("tenant_id"))
 return {
 "conversation_history": ["System: Ticket escalated to human support."]
 }


def build_agnostic_helpdesk():
 """Compiles the helpdesk state machine."""
 workflow = StateGraph(HelpdeskState)

 workflow.add_node("intake", agnostic_intake_node)
 workflow.add_node("fulfilment", fulfilment_node)
 workflow.add_node("escalation", escalation_node)

 workflow.set_entry_point("intake")
 workflow.add_conditional_edges(
 "intake",
 lambda state: state["classification"],
 {
 "fulfilment": "fulfilment",
 "escalation": "escalation",
 },
 )

 workflow.add_edge("fulfilment", END)
 workflow.add_edge("escalation", END)

 return workflow.compile()
