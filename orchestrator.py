import uuid
from typing import Any, Dict, Optional, Protocol

from coastal_alpine_core.security import SecurityGuard, SecurityResult
from coastal_alpine_core.telemetry import TelemetryTracker

from agents import FulfilmentAgent, IntakeAgent, ResolutionAgent
from knowledge_base import (
    HashEmbeddingService,
    InMemoryKnowledgeBaseClient,
    KnowledgeBaseClient,
)

# ... (Protocols and helper classes remain the same) ...

class AgentOrchestrator:
    """
    Tenant-aware agent orchestrator with deep SecurityGuard + TelemetryTracker integration.
    Enterprise-ready with structured security events and performance measurement.
    """

    def __init__(self, tenant_id: str, tenant_config: Optional[Dict[str, Any]] = None, ...):
        # ... existing init ...
        self.security_guard = SecurityGuard()

    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        # Security check on incoming message
        prompt_text = str(message.get("content", ""))
        sec_result: SecurityResult = self.security_guard.check_prompt(prompt_text)

        if not sec_result.is_safe:
            logger.warning(f"Blocked unsafe message: {sec_result.reason}")
            return {"status": "blocked", "reason": sec_result.reason}

        measurement = TelemetryTracker.measure_latency("orchestrator_process_message")

        # ... existing intake logic ...

        TelemetryTracker.complete_measurement(
            measurement,
            token_count=len(str(message).split()),
            include_system_metrics=True
        )

        # ... rest of the method ...
