"""Unified Weaver orchestrator: security + telemetry + agents + optional graph path."""

from __future__ import annotations

import logging
import time
import uuid
from typing import Any, Callable, Dict, Mapping, Optional

from agents import IntakeAgent
from coastal_alpine_core.security import SecurityGuard
from coastal_alpine_core.session_events import SessionEventStore
from coastal_alpine_core.telemetry import TelemetryTracker

try:
    from coastal_alpine_core import record_session_trajectory  # Core ≥0.5.9
except ImportError:  # pragma: no cover
    record_session_trajectory = None  # type: ignore

try:
    from coastal_alpine_core import ConfigOverlay  # Core ≥0.5.10
except ImportError:  # pragma: no cover
    ConfigOverlay = None  # type: ignore

try:
    from coastal_alpine_core import EffectJournal, CodeModeRunner  # Core ≥0.5.10
except ImportError:  # pragma: no cover
    EffectJournal = None  # type: ignore
    CodeModeRunner = None  # type: ignore

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

    Soft Core seams:
    - SessionEvents (0.5.7+) / Trajectories (0.5.9+)
    - ConfigOverlay, EffectJournal, CodeModeRunner (0.5.10+)
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
        flywheel_path: Optional[str] = None,
        config_overlay: Any = None,
        llm_profile: str = "edge-default",
        effect_journal: Any = None,
        code_mode_tools: Optional[Mapping[str, Callable[..., Any]]] = None,
        code_mode_hitl: Optional[Callable[[str], bool]] = None,
    ):
        self.tenant_id = tenant_id
        self.tenant_config = tenant_config or {}
        self.knowledge_base_client = knowledge_base_client or _KnowledgeBaseClient()
        self.memory_store = memory_store or _MemoryStore()
        self.llm = llm
        self.use_graph = use_graph
        self.llm_profile = llm_profile
        self.security_guard = SecurityGuard()
        self.event_store = event_store or SessionEventStore(
            storage_path=f"session_events_{tenant_id}.jsonl"
        )
        self.flywheel_path = flywheel_path or f"flywheel_{tenant_id}.jsonl"

        self.config_overlay = config_overlay
        if self.config_overlay is None and ConfigOverlay is not None:
            try:
                self.config_overlay = ConfigOverlay(
                    defaults={
                        "llm": {"profile": llm_profile},
                        "tenant_id": tenant_id,
                        "use_graph": use_graph,
                    }
                )
                self.config_overlay.register_profile(
                    "edge-default", {"llm": {"profile": "edge-default"}}
                )
                self.config_overlay.register_profile(
                    "edge-fast", {"llm": {"profile": "edge-fast"}}
                )
                self.config_overlay.use_profile(
                    llm_profile
                    if llm_profile in ("edge-default", "edge-fast")
                    else "edge-default"
                )
                safe_tenant = {
                    k: v
                    for k, v in self.tenant_config.items()
                    if k
                    in (
                        "brand_voice",
                        "escalation_rules",
                        "locale",
                        "timezone",
                        "llm_profile",
                    )
                }
                if safe_tenant:
                    self.config_overlay.set_tenant(safe_tenant)
            except Exception as exc:
                logger.debug("ConfigOverlay init failed: %s", exc)
                self.config_overlay = None

        self.effect_journal = effect_journal
        if self.effect_journal is None and EffectJournal is not None:
            try:
                self.effect_journal = EffectJournal(
                    audit_path=f"effects_{tenant_id}.jsonl"
                )
            except Exception as exc:
                logger.debug("EffectJournal init failed: %s", exc)
                self.effect_journal = None

        self.code_mode = None
        self._code_mode_tools: Dict[str, Callable[..., Any]] = dict(
            code_mode_tools or {}
        )
        self._code_mode_hitl = code_mode_hitl
        self._rebuild_code_mode()

        self.intake_agent = IntakeAgent(
            self.knowledge_base_client,
            self.memory_store,
            tenant_id=self.tenant_id,
            tenant_config=self.tenant_config,
        )
        self._graph = None

    def _rebuild_code_mode(self) -> None:
        if CodeModeRunner is None:
            self.code_mode = None
            return
        try:
            self.code_mode = CodeModeRunner(
                self._code_mode_tools,
                hitl=self._code_mode_hitl,
            )
        except Exception as exc:
            logger.debug("CodeModeRunner init failed: %s", exp)
            self.code_mode = None

    def register_code_tool(self, name: str, fn: Callable[..., Any]) -> None:
        if not name or not callable(fn):
            raise ValueError("name and callable fn required")
        self._code_mode_tools[name] = fn
        self._rebuild_code_mode()

    def run_code_mode(self, source: str) -> Dict[str, Any]:
        if self.code_mode is None:
            return {"success": False, "error": "code_mode_unavailable"}
        try:
            result = self.code_mode.run(source)
            out = {
                "success": bool(result.success),
                "output": result.output,
                "error": result.error,
                "tool_calls": list(result.tool_calls or []),
            }
            if self.effect_journal is not None and result.success:
                try:
                    self.effect_journal.record(
                        "code_mode.run",
                        payload={"tool_calls": out["tool_calls"]},
                        reversible=False,
                        metadata={"tenant_id": self.tenant_id},
                    )
                except Exception as exp:
                    logger.debug("effect record failed: %s", exp)
            return out
        except Exception as exp:
            logger.debug("run_code_mode failed: %s", exp)
            return {"success": False, "error": str(exp)[:200]}

    def record_effect(
        self,
        action: str,
        *,
        payload: Optional[Dict[str, Any]] = None,
        reverse_action: Optional[str] = None,
        reverse_payload: Optional[Dict[str, Any]] = None,
        reversible: Optional[bool] = None,
    ) -> Optional[Any]:
        if self.effect_journal is None:
            return None
        try:
            return self.effect_journal.record(
                action,
                payload=payload,
                reverse_action=reverse_action,
                reverse_payload=reverse_payload,
                reversible=reversible,
                metadata={"tenant_id": self.tenant_id},
            )
        except Exception as exp:
            logger.debug("record_effect failed: %s", exp)
            return None

    def undo_last_effect(self) -> Optional[Any]:
        if self.effect_journal is None:
            return None
        try:
            return self.effect_journal.undo_last()
        except Exception as exp:
            logger.debug("undo_last_effect failed: %s", exp)
            return None

    def resolved_config(self) -> Dict[str, Any]:
        if self.config_overlay is None:
            return {
                "tenant_id": self.tenant_id,
                "use_graph": self.use_graph,
                "llm": {"profile": self.llm_profile},
            }
        try:
            return self.config_overlay.resolve()
        except Exception:
            return {"tenant_id": self.tenant_id}

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

    def _bind_session_overlay(self, session_id: str) -> None:
        if self.config_overlay is None:
            return
        try:
            self.config_overlay.set_session(
                {"session_id": session_id, "use_graph": self.use_graph}
            )
        except Exception as exp:
            logger.debug("session overlay failed: %s", exp)

    def _bind_llm_session(self, session_id: str) -> None:
        llm = self.llm
        if llm is None:
            return
        binder = getattr(llm, "bind_session", None)
        if callable(binder):
            try:
                binder(
                    session_id=session_id,
                    event_store=self.event_store,
                    tenant_id=self.tenant_id,
                )
            except Exception as exp:
                logger.debug("LLM bind_session failed: %s", exp)

    def _record_trajectory(
        self,
        *,
        session_id: str,
        outcome: str,
        input_summary: str,
        output_summary: str,
        latency_seconds: float,
    ) -> None:
        if record_session_trajectory is None:
            return
        try:
            record_session_trajectory(
                session_id=session_id,
                action="weaver.process_message",
                outcome=outcome,
                input_summary=input_summary,
                output_summary=output_summary,
                latency_seconds=latency_seconds,
                tenant_id=self.tenant_id,
                storage_path=self.flywheel_path,
            )
        except Exception as exp:
            logger.debug("Trajectory record failed: %s", exp)

    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        session_id = self._session_id_from_message(message)
        user_text = message.get("content") or message.get("user_message") or ""
        if not isinstance(user_text, str):
            user_text = str(user_text)

        self._bind_session_overlay(session_id)
        self._bind_llm_session(session_id)

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
            self._record_trajectory(
                session_id=session_id,
                outcome="blocked",
                input_summary=f"chars={len(user_text)}",
                output_summary="status=blocked",
                latency_seconds=0.0,
            )
            return {
                "status": "blocked",
                "tenant_id": self.tenant_id,
                "session_id": session_id,
            }

        measurement = TelemetryTracker.measure_latency("orchestrator_process_message")
        t0 = time.perf_counter()
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
            status = result.get("status") if isinstance(result, dict) else "ok"
            self.event_store.emit(
                session_id=session_id,
                event_type="session_end",
                actor="orchestrator",
                tenant_id=self.tenant_id,
                payload={"status": status},
                outcome="success",
            )
            self._record_trajectory(
                session_id=session_id,
                outcome="success",
                input_summary=f"chars={len(user_text)}",
                output_summary=f"status={status}",
                latency_seconds=time.perf_counter() - t0,
            )
            return result
        except Exception:
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
            self._record_trajectory(
                session_id=session_id,
                outcome="error",
                input_summary=f"chars={len(user_text)}",
                output_summary="status=error",
                latency_seconds=time.perf_counter() - t0,
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
