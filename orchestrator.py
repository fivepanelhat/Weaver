"""Unified Weaver orchestrator: security + telemetry + agents + optional graph path."""

from __future__ import annotations

import logging
import uuid
from typing import Any, Dict, Optional

from agents import IntakeAgent
from coastal_alpine_core.security import SecurityGuard
from coastal_alpine_core.session_events import SessionEventStore
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
    Emits SessionEvents (Core 0.5.7+) for HITL / Trajectory audit.
    """

    def __init__(
        self,
        tenant_id: str,
        tenant_config: Optional[Dict[str, Any]] = None,
        knowledge_base_client=None,
        memory_store=None,
        llm=None,
        use_graph: bool = False,
        event_store: Optional[SessionEventStore] = None,
    ):
        self.tenant_id = tenant_id
        self.tenant_config = tenant_config or {}
        self.knowledge_base_client = knowledge_base_client or _KnowledgeBaseClient()
        self.memory_store = memory_store or _MemoryStore()
        self.llm = llm
        self.use_graph = use_graph
        self.security_guard = SecurityGuard()
        self.event_store = event_store or SessionEventStore(
            storage_path=f"session_events_{tenant_id}.jsonl"
        )
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

    def _session_id_from_message(self, message: Dict[str, Any]) -> str:
        return str(
            message.get("session_id")
            or message.get("conversation_id")
            or message.get("id")
            or uuid.uuid4()
        )

    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        # Security gate first — never run agents on unsafe prompts.
        # Guard the actual user-supplied text, not str(message): the dict
        # repr escapes unicode, so a zero-width char used to obfuscate an
        # injection becomes a literal backslash-u200b and slips past the
        # guard's normalization. Check the raw content field instead.
        session_id = self._session_id_from_message(message)
        user_text = message.get("content") or message.get("user_message") or ""
        if not isinstance(user_text, str):
            user_text = str(user_text)

        self.event_store.emit(
            session_id=session_id,
            event_type="prompt_received",
            actor="orchestrator",
            tenant_id=self.tenant_id,
            payload={"chars": len(user_text), "use_graph": self.use_graph},
        )

        sec_result = self.security_guard.check_prompt(user_text)
        self.event_store.emit(
            session_id=session_id,
            event_type="security_check",
            actor="security_guard",
            tenant_id=self.tenant_id,
            payload={"is_safe": bool(sec_result.is_safe)},
            outcome="pass" if sec_result.is_safe else "blocked",
        )
        if not sec_result.is_safe:
            self.event_store.emit(
                session_id=session_id,
                event_type="blocked",
                actor="orchestrator",
                tenant_id=self.tenant_id,
                payload={"reason": "security_guard"},
                outcome="blocked",
            )
            return {
                "status": "blocked",
                "tenant_id": self.tenant_id,
                "session_id": session_id,
            }

        measurement = TelemetryTracker.measure_latency("orchestrator_process_message")
        try:
            if self.use_graph:
                result = self._process_via_graph(message, session_id=session_id)
            else:
                self.event_store.emit(
                    session_id=session_id,
                    event_type="agent_step",
                    actor="intake",
                    tenant_id=self.tenant_id,
                    payload={"path": "intake_agent"},
                )
                result = self.intake_agent.process_interaction(message)
            if isinstance(result, dict):
                result = {**result, "session_id": session_id}
            self.event_store.emit(
                session_id=session_id,
                event_type="session_end",
                actor="orchestrator",
                tenant_id=self.tenant_id,
                payload={
                    "status": result.get("status")
                    if isinstance(result, dict)
                    else "ok"
                },
                outcome="success",
            )
            return result
        except Exception:
            # Diamond: log the full error server-side, return a sanitized status.
            # Tenant ID is not sensitive data and helps callers correlate errors;
            # exception details and stack traces never leak.
            logger.exception(
                "orchestrator_process_message failed for tenant %s", self.tenant_id
            )
            self.event_store.emit(
                session_id=session_id,
                event_type="error",
                actor="orchestrator",
                tenant_id=self.tenant_id,
                payload={"where": "process_message"},
                outcome="error",
            )
            return {
                "status": "error",
                "tenant_id": self.tenant_id,
                "session_id": session_id,
            }
        finally:
            TelemetryTracker.complete_measurement(
                measurement, include_system_metrics=True
            )

    def _process_via_graph(
        self, message: Dict[str, Any], session_id: str
    ) -> Dict[str, Any]:
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
        self.event_store.emit(
            session_id=session_id,
            event_type="agent_step",
            actor="graph",
            tenant_id=self.tenant_id,
            payload={"path": "weaver_graph"},
        )
        out = graph.run(
            state,
            kb_client=self.knowledge_base_client,
            llm=self.llm,
        )
        classification = out.get("classification")
        if classification == "escalation":
            self.event_store.emit(
                session_id=session_id,
                event_type="escalation",
                actor="graph",
                tenant_id=self.tenant_id,
                payload={"classification": classification},
                outcome="escalation",
            )
        return {
            "status": "graph_complete",
            "tenant_id": self.tenant_id,
            "session_id": session_id,
            "classification": classification,
            "retrieved_context": out.get("retrieved_context"),
            "conversation_history": out.get("conversation_history", []),
        }
