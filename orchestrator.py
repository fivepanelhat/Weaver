from typing import Any, Dict, Optional

from agents import IntakeAgent
from coastal_alpine_core.security import SecurityGuard
from coastal_alpine_core.telemetry import TelemetryTracker


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
    def query(self, query: str, tenant_id: str):
        return []


class AgentOrchestrator:
    """
    Demo orchestrator that wraps the intake agent with security and telemetry checks.
    """

    def __init__(
        self,
        tenant_id: str,
        tenant_config: Optional[Dict[str, Any]] = None,
        knowledge_base_client=None,
        memory_store=None,
    ):
        self.tenant_id = tenant_id
        self.tenant_config = tenant_config or {}
        self.knowledge_base_client = knowledge_base_client or _KnowledgeBaseClient()
        self.memory_store = memory_store or _MemoryStore()
        self.security_guard = SecurityGuard()
        self.intake_agent = IntakeAgent(
            self.knowledge_base_client,
            self.memory_store,
            tenant_id=self.tenant_id,
            tenant_config=self.tenant_config,
        )

    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        # Security + Telemetry as before...
        sec_result = self.security_guard.check_prompt(str(message))
        if not sec_result.is_safe:
            return {"status": "blocked"}

        measurement = TelemetryTracker.measure_latency("orchestrator_process_message")
        result = self.intake_agent.process_interaction(message)

        TelemetryTracker.complete_measurement(
            measurement, include_system_metrics=True
        )

        return result
