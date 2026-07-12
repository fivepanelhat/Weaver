"""Unified Weaver orchestrator: security + telemetry + agents + optional graph path."""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from agents import IntakeAgent
from coastal_alpine_core.security import SecurityGuard
from coastal_alpine_core.telemetry import TelemetryTracker

logger = logging.getLogger("weaver.orchestrator")


class _MemoryStore:
    def __init__(self):
        self._contexts: Dict[Optional[str], Dict[str, Any]] = {}

    def update_context(
        self,
        message_id: Optional[str],
        customer_profile: Dict[str, Any],
        request_classification: str,
    ) -> None:
        self._contexts[message_id] = {
            "customer_profile": customer_profile,
            "request_classification": request_classification,
        }


class _KnowledgeBaseClient:
    def query(self, query: str, tenant_id: str, top_k: int = 5):
        return []


class AgentOrchestrator:
    """
    Production entrypoint for multi-tenant helpdesk messages.

    Wraps IntakeAgent with security + telemetry. Optionally exposes the
    weaver_graph helpdesk state machine for graph-based routing.
    """

    def __init__(
        self,
        tenant_id: str,
        tenant_config: Optional[Dict[str, Any]] = None,
        knowledge_base_client=None,
        memory_store=None,
        llm=None,
        use_graph: bool = False,
    ):
        self.tenant_id = tenant_id
        self.tenant_config = tenant_config or {}
        self.knowledge_base_client = knowledge_base_client or _KnowledgeBaseClient()
        self.memory_store = memory_store or _MemoryStore()
        self.llm = llm
        self.use_graph = use_graph
        self.security_guard = SecurityGuard()
        self.intake_agent = IntakeAgent(
            self.knowledge_base_client,
            self.memory_store,
            tenant_id=self.tenant_id,
            tenant_config=self.tenant_config,
        )
        self._graph = None

    def _get_graph(self):
        if self._graph is None:
            from weaver_graph.orchestrator import build_agnostic_helpdesk

            self._graph = build_agnostic_helpdesk()
        return self._graph

    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        # Security gate first — never run agents on unsafe prompts.
        # Guard the actual user-supplied text, not str(message): the dict
        # repr escapes unicode, so a zero-width char used to obfuscate an
        # injection becomes a literal backslash-u200b and slips past the
        # guard's normalization. Check the raw content field instead.
        user_text = message.get("content") or message.get("user_message") or ""
        if not isinstance(user_text, str):
            user_text = str(user_text)
        sec_result = self.security_guard.check_prompt(user_text)
        if not sec_result.is_safe:
            return {"status": "blocked", "tenant_id": self.tenant_id}

        measurement = TelemetryTracker.measure_latency("orchestrator_process_message")
        try:
            if self.use_graph:
                result = self._process_via_graph(message)
            else:
                result = self.intake_agent.process_interaction(message)
            return result
        except Exception:
            # Diamond: log the full error server-side, return a sanitized status.
            # Never leak internal exception details (or tenant data) to callers.
            logger.exception(
                "orchestrator_process_message failed for tenant %s", self.tenant_id
            )
            return {"status": "error", "tenant_id": self.tenant_id}
        finally:
            TelemetryTracker.complete_measurement(
                measurement, include_system_metrics=True
            )

    def _process_via_graph(self, message: Dict[str, Any]) -> Dict[str, Any]:
        graph = self._get_graph()
        state = {
            "tenant_id": self.tenant_id,
            "brand_voice": self.tenant_config.get(
                "brand_voice", "Professional and helpful."
            ),
            "escalation_rules": self.tenant_config.get("escalation_rules") or {},
            "user_message": message.get("content") or message.get("user_message") or "",
            "retrieved_context": "",
            "classification": "",
            "conversation_history": [],
        }
        out = graph.run(
            state,
            kb_client=self.knowledge_base_client,
            llm=self.llm,
        )
        return {
            "status": "graph_complete",
            "tenant_id": self.tenant_id,
            "classification": out.get("classification"),
            "retrieved_context": out.get("retrieved_context"),
            "conversation_history": out.get("conversation_history", []),
        }
