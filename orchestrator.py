import uuid
from typing import Any, Dict, Optional, Protocol

from agents import FulfilmentAgent, IntakeAgent, ResolutionAgent
from knowledge_base import (
    HashEmbeddingService,
    InMemoryKnowledgeBaseClient,
    KnowledgeBaseClient,
)


class MemoryStore(Protocol):
    def update_context(self, interaction_id: str, customer_profile: Dict[str, Any], classification: str) -> None: ...


class CRMClient(Protocol):
    def update_customer(self, *args: Any, **kwargs: Any) -> Dict[str, Any]: ...


class LLMPool(Protocol):
    def generate(self, prompt: str) -> str: ...


class TelemetryLogger(Protocol):
    def log_event(self, event_name: str, data: Dict[str, Any]) -> None: ...


class EscalationQueue(Protocol):
    def push(self, context: Dict[str, Any]) -> None: ...


class InMemoryMemoryStore:
    """Simple in-memory store for demos and tests. Replace with persistent store in production."""

    def __init__(self) -> None:
        self.store: Dict[str, Dict[str, Any]] = {}

    def update_context(
        self, interaction_id: str, customer_profile: Dict[str, Any], classification: str
    ) -> None:
        self.store[interaction_id] = {
            "customer_profile": customer_profile,
            "classification": classification,
        }


class NoOpCRM:
    def update_customer(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        return {}


class NoOpLLMPool:
    def generate(self, prompt: str) -> str:
        return f"[LLM response generated from prompt: {prompt[:120]}...]"


class NoOpTelemetryLogger:
    def log_event(self, event_name: str, data: Dict[str, Any]) -> None:
        print(f"Telemetry: {event_name}", data)


class NoOpEscalationQueue:
    def push(self, context: Dict[str, Any]) -> None:
        print(f"Escalation queue received context: {context}")


class AgentOrchestrator:
    """
    Tenant-aware agent orchestrator with clean dependency injection.
    Integrates TelemetryTracker on process_message for optimisation loop.
    """

    def __init__(
        self,
        tenant_id: str,
        tenant_config: Optional[Dict[str, Any]] = None,
        knowledge_base_client: Optional[KnowledgeBaseClient] = None,
        memory_store: Optional[MemoryStore] = None,
        crm_client: Optional[CRMClient] = None,
        llm_pool: Optional[LLMPool] = None,
        telemetry_logger: Optional[TelemetryLogger] = None,
        escalation_queue: Optional[EscalationQueue] = None,
    ) -> None:
        self.tenant_id = tenant_id
        self.tenant_config = tenant_config or {}
        self.memory_store = memory_store or InMemoryMemoryStore()
        self.kb_client = knowledge_base_client or InMemoryKnowledgeBaseClient(HashEmbeddingService())
        self.crm_client = crm_client or NoOpCRM()
        self.llm_pool = llm_pool or NoOpLLMPool()
        self.telemetry_logger = telemetry_logger or NoOpTelemetryLogger()
        self.escalation_queue = escalation_queue or NoOpEscalationQueue()

    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        from coastal_alpine_core.telemetry import TelemetryTracker

        measurement = TelemetryTracker.measure_latency("orchestrator_process_message")

        intake_agent = IntakeAgent(
            knowledge_base_client=self.kb_client,
            memory_store=self.memory_store,
            tenant_id=self.tenant_id,
            tenant_config=self.tenant_config,
        )

        result = intake_agent.process_interaction(message)

        TelemetryTracker.complete_measurement(measurement, token_count=len(str(message).split()))

        if result.get("status") == "handoff_required":
            return self._route_handoff(result)

        return result

    def _route_handoff(self, handoff: Dict[str, Any]) -> Dict[str, Any]:
        target = handoff.get("target_agent")
        context = handoff.get("context", {})

        if target == "FulfillmentAgent":
            agent = FulfilmentAgent(
                crm_client=self.crm_client,
                order_db=None,
                llm_pool=self.llm_pool,
                tenant_id=self.tenant_id,
                escalation_rules=self.tenant_config.get("escalation_rules", {}),
            )
            return agent.execute_task({"intent": "process_order", **context})

        if target == "ResolutionAgent":
            agent = ResolutionAgent(
                telemetry_logger=self.telemetry_logger,
                escalation_queue=self.escalation_queue,
                tenant_id=self.tenant_id,
            )
            return agent.handle_issue({"issue_id": str(uuid.uuid4()), **context})

        return {"status": "unknown_target", "target_agent": target}


def build_sample_orchestrator() -> AgentOrchestrator:
    kb_client = InMemoryKnowledgeBaseClient(HashEmbeddingService())
    return AgentOrchestrator(
        tenant_id="tenant-demo",
        tenant_config={
            "brand_voice": "Friendly, concise and professional.",
            "escalation_rules": {"require_human_for": "high_risk"},
            "custom_instructions": "Always cite the tenant knowledge base and avoid speculation.",
        },
        knowledge_base_client=kb_client,
    )
