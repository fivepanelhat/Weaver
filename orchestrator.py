import logging
import time
import uuid
from typing import Any, Dict, Optional

from agents import IntakeAgent
from coastal_alpine_core.flywheel import (
    BayesianOptimisationHook,
    DataFlywheel,
    Trajectory,
)
from coastal_alpine_core.security import SecurityGuard
from coastal_alpine_core.telemetry import TelemetryTracker

logger = logging.getLogger(__name__)


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
    def query(self, _query: str, _tenant_id: str):
        return []


class AgentOrchestrator:
    """
    Enterprise orchestrator with full Data Flywheel + Bayesian Optimisation scaffolding.
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
        self.flywheel = DataFlywheel(storage_path=f"flywheel_{tenant_id}.jsonl")
        self.bo_hook = BayesianOptimisationHook()
        self.security_guard = SecurityGuard()

    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        # Security + Telemetry as before...
        sec_result = self.security_guard.check_prompt(str(message))
        if not sec_result.is_safe:
            return {"status": "blocked"}

        measurement = TelemetryTracker.measure_latency("orchestrator_process_message")

        intake_agent = IntakeAgent(
            self.knowledge_base_client,
            self.memory_store,
            tenant_id=self.tenant_id,
            tenant_config=self.tenant_config,
        )
        result = intake_agent.process_interaction(message)

        # === Data Flywheel Recording ===
        try:
            traj = Trajectory(
                trajectory_id=str(uuid.uuid4()),
                timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                action="process_message",
                input_summary=str(message)[:300],
                output_summary=str(result)[:300],
                outcome="success" if result.get("status") != "error" else "failure",
                latency_seconds=0.0,  # populated after complete_measurement
                estimated_energy_joules=0.0,
                system_metrics={},
                metadata={"tenant_id": self.tenant_id},
            )
            self.flywheel.record_trajectory(traj)
        except Exception as exc:
            logger.warning("Flywheel recording failed: %s", exc)

        TelemetryTracker.complete_measurement(measurement, include_system_metrics=True)

        # Optional: Ask BO hook for suggestions periodically
        if len(self.flywheel.get_recent_trajectories(10)) % 20 == 0:
            suggestion = self.bo_hook.suggest_next_configuration({"current_latency": 2.3})
            logger.info("BO Suggestion: %s", suggestion)

        return result
