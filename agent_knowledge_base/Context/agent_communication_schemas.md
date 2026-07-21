# Agent Communication Schemas Report

## Mana Kai & Byte Size Kai Agentic Architecture

**Date:** 23 May 2026

This document defines the communication schemas for the agentic architecture. It builds directly upon the previously defined agent roles and ensures reliable, secure, and efficient interaction within the sovereign, on-premise environment on the Raspberry Pi 16GB with Hailo-10H NPU.

### 1. Communication Architecture Overview

The system employs a hybrid communication model optimized for edge computing:

- **Primary Protocol**: MQTT (Message Queuing Telemetry Transport) for lightweight, real-time pub/sub messaging, ideal for IoT and agent coordination.
- **Secondary Mechanisms**:
  - Local REST/gRPC for synchronous agent-to-agent requests where needed.
  - Shared memory / vector database for persistent state.
- **Message Format**: JSON (with optional binary payloads for images or time-series data).
- **Security**: All communications encrypted via TLS 1.3 (local CA). Role-based access control enforced at the broker level.
- **Resilience**: QoS levels (0, 1, 2) applied based on message criticality. Persistent sessions and last-will messages for agent health monitoring.

### 2. Core Message Types

| Message Type              | Directionality                  | Purpose                              | QoS Level |
|---------------------------|---------------------------------|--------------------------------------|-----------|
| Command                   | Orchestrator → Agent            | Task assignment                      | 1         |
| Status Update             | Agent → Orchestrator / Peers    | Health and progress reporting        | 1         |
| Data Event                | Data Ingestion → Multiple       | New sensor or analysis data          | 2         |
| Alert                     | Any Agent → Alerting Agent      | Anomaly or critical notification     | 2         |
| Query / Response          | Agent ↔ Agent                   | Synchronous information exchange     | 1         |
| Synchronization           | Digital Twin Agent ↔ Others     | State alignment                      | 1         |

### 3. Standardized Message Schema

All messages follow this base structure:

```json
{
  "message_id": "uuid-string",
  "timestamp": "ISO 8601 UTC",
  "sender": "agent_name",
  "recipient": "agent_name or 'broadcast'",
  "message_type": "Command | StatusUpdate | DataEvent | Alert | Query | Response | Sync",
  "correlation_id": "uuid (for request-response pairing)",
  "payload": { ... },
  "metadata": {
    "priority": "high | medium | low",
    "ttl": "seconds",
    "version": "1.0"
  }
}
```

### 4. Detailed Payload Schemas

#### 4.1 Command Message (Orchestrator → Agent)

```json
"payload": {
  "command": "start_monitoring | analyze_growth | optimize_resources | run_prediction",
  "parameters": {
    "target": "microgreens_batch_47",
    "duration": 3600,
    "config": { ... }
  },
  "deadline": "ISO 8601"
}
```

#### 4.2 Data Event Message

```json
"payload": {
  "data_type": "sensor_reading | growth_analysis | prediction",
  "batch_id": "string",
  "readings": {
    "temperature": 22.5,
    "humidity": 68.0,
    "light_intensity": 4500,
    "image_hash": "sha256-hash",
    "growth_stage": "cotyledon"
  },
  "confidence": 0.95
}
```

#### 4.3 Alert Message

```json
"payload": {
  "severity": "critical | warning | info",
  "alert_type": "temperature_spike | nutrient_deficiency | pest_detected",
  "description": "Temperature exceeded 28°C for 12 minutes",
  "recommended_action": "increase_ventilation",
  "affected_batch": "batch_47"
}
```

#### 4.4 Status Update Message

```json
"payload": {
  "status": "healthy | degraded | offline",
  "uptime": 86400,
  "metrics": {
    "cpu_usage": 45.2,
    "memory_usage": 62.8,
    "last_processed": "ISO 8601"
  },
  "queue_length": 12
}
```

#### 4.5 Query / Response

```json
"payload": {
  "query": "get_current_conditions",
  "filters": { "batch_id": "47" }
}
```

Response uses identical structure with `message_type: "Response"` and mirrored `correlation_id`.

### 5. MQTT Topic Structure

A hierarchical topic namespace ensures clear routing:

- `mankai/command/{agent_name}`
- `mankai/data/{data_type}/{batch_id}`
- `mankai/alert/{severity}`
- `mankai/status/{agent_name}`
- `mankai/sync/digital_twin`
- `mankai/query/{target_agent}`

### 6. Implementation Considerations

- **Broker**: Eclipse Mosquitto or EMQX (lightweight, suitable for Raspberry Pi).
- **Libraries**:
  - Python: `paho-mqtt` or `asyncio-mqtt`
  - Node.js: `mqtt.js`
- **Error Handling**: Every agent must implement retry logic (exponential backoff) and dead-letter queues for failed messages.
- **Monitoring**: Orchestrator Agent subscribes to all status topics and maintains an agent registry.
- **Scalability**: Schema supports easy addition of new agents without breaking existing communication.

This communication schema provides a robust, standardized foundation for agent interaction while remaining lightweight enough for on-premise Raspberry Pi deployment. It enables the autonomous yet coordinated behavior required for effective digital twin operation of Mana Kai’s microgreens production.
