import uuid
from typing import Any, Dict, Optional, Protocol

from coastal_alpine_core.security import SecurityGuard, SecurityResult
from coastal_alpine_core.telemetry import TelemetryTracker
from coastal_alpine_core.flywheel import DataFlywheel, Trajectory, BayesianOptimisationHook

# ... existing imports and classes ...

class AgentOrchestrator:
    """
    Enterprise orchestrator with full Data Flywheel + Bayesian Optimisation scaffolding.
    """

    def __init__(self, tenant_id: str, tenant_config: Optional[Dict[str, Any]] = None, ...):
        # ... existing init code ...
        self.flywheel = DataFlywheel(storage_path=f"flywheel_{tenant_id}.jsonl")
        self.bo_hook = BayesianOptimisationHook()
        self.security_guard = SecurityGuard()

    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        # Security + Telemetry as before...
        sec_result = self.security_guard.check_prompt(str(message))
        if not sec_result.is_safe:
            return {"status": "blocked"}

        measurement = TelemetryTracker.measure_latency("orchestrator_process_message")

        # ... existing intake and routing logic ...

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
                metadata={"tenant_id": self.tenant_id}
            )
            self.flywheel.record_trajectory(traj)
        except Exception as e:
            logger.warning(f"Flywheel recording failed: {e}")

        TelemetryTracker.complete_measurement(measurement, include_system_metrics=True)

        # Optional: Ask BO hook for suggestions periodically
        if len(self.flywheel.get_recent_trajectories(10)) % 20 == 0:
            suggestion = self.bo_hook.suggest_next_configuration({"current_latency": 2.3})
            logger.info(f"BO Suggestion: {suggestion}")

        return result

    # ... rest of the class ...
