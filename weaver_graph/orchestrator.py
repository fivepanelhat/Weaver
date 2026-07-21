"""Agnostic multi-tenant helpdesk graph with real RAG + LLM hooks."""

from __future__ import annotations

import json
import logging
from typing import TypedDict, List, Annotated, Any, Optional
import operator

from pydantic import BaseModel, Field

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


class RouteDecision(BaseModel):
    """Structured output schema for LLM routing decisions."""
    route: str = Field(
        description="Either 'fulfilment' or 'escalation'",
        pattern="^(fulfilment|escalation)$"
    )
    reply: str = Field(
        description="Short customer-facing response (max 280 chars)",
        max_length=280
    )
    confidence: float = Field(
        default=0.8,
        ge=0.0,
        le=1.0,
        description="Model confidence in the routing decision"
    )


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
    Uses structured output when available, falls back to text parsing.
    Keyword escalation is authoritative (fail-safe).
    """
    message = state.get("user_message") or ""
    rules = state.get("escalation_rules") or {}
    brand = state.get("brand_voice") or "Professional and helpful."

    # Keyword fast-path (cheap + deterministic)
    keyword = _keyword_route(message, rules if isinstance(rules, dict) else {})

    if llm is None:
        if keyword == "escalation":
            return "escalation", "I understand this needs careful attention. Connecting you with a human advisor."
        return "fulfilment", "Let me check that against our policies and records."

    # Try structured output first (Ollama JSON schema)
    try:
        if hasattr(llm, "invoke_structured"):
            decision: RouteDecision = llm.invoke_structured(
                prompt=_build_route_prompt(message, context, brand, rules),
                schema=RouteDecision,
            )
            route = decision.route
            reply = decision.reply.strip()

            # Safety: keyword escalation is authoritative
            if keyword == "escalation" and route != "escalation":
                route = "escalation"
                reply = "I'll escalate this to a human specialist."

            return route, reply
    except Exception as e:
        logger.warning("Structured routing failed, falling back to text: %s", e)

    # Fallback: original text parsing path
    prompt = _build_route_prompt(message, context, brand, rules)
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

    # Safety: keyword escalation is authoritative
    if keyword == "escalation" and route != "escalation":
        route = "escalation"
        if not reply:
            reply = "I'll escalate this to a human specialist."

    if not reply:
        reply = (
            "I'll connect you with a human advisor."
            if route == "escalation"
            else "I'll help with that using our local policies."
        )

    return route, reply


def _build_route_prompt(message: str, context: str, brand: str, rules: dict) -> str:
    return (
        "You are a tenant-scoped helpdesk router. Respond with a clear routing decision.\n"
        f"Brand voice: {brand}\n"
        f"Escalation rules: {rules}\n"
        f"Retrieved policy context:\n{context or '(none)'}\n\n"
        f"Customer message: {message}\n"
    )


def agnostic_intake_node(state: HelpdeskState, *args, **kwargs):
    vector_db_client = kwargs.get("vector_db_client")
    kb_client = kwargs.get("kb_client")
    llm = kwargs.get("llm")

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
    logger.info("Fulfilment for tenant=%s", state.get("tenant_id"))
    ctx = (state.get("retrieved_context") or "").strip()
    if ctx:
        summary = ctx.splitlines()[0][:240]
        msg = f"AI: Fulfilment task complete. Based on our records: {summary}"
    else:
        msg = "AI: Fulfilment task complete."
    return {"conversation_history": [msg]}


def escalation_node(state: HelpdeskState, *args, **kwargs):
    logger.info("Escalation for tenant=%s", state.get("tenant_id"))
    return {
        "conversation_history": ["System: Ticket escalated to human support."]
    }


def build_agnostic_helpdesk():
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
