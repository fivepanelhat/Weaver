# Weaver: AI-Native Multi-Tenant Agentic Mesh

<p align="center">
  <img src="assets/social_preview.png" alt="Weaver — Coastal Alpine Tech liquid glass banner" width="100%" />
</p>

**Coastal Alpine Tech Limited**  
*Edge AI | Sovereign Systems | Practical Intelligence*

**License: Proprietary — Coastal Alpine Tech Limited** · See [LICENSE](./LICENSE) (same Coastal Alpine proprietary terms as AquaGuard, SoilGuard, Blue-Moon, Sting-Operation, Core, and the rest of the edge stack).

White-label multi-tenant AI helpdesk scaffold with isolated knowledge retrieval and local LangGraph orchestration.

---

## The 5 Ws: Project Context

- **Who:** Built by Coastal Alpine Tech Limited, designed for high-stakes Kiwi industries (civil construction, agritech, etc.).
- **What:** A decentralized LangGraph orchestration layer that safely directs multi-agent tasks and handles local document vectorization.
- **Where:** Engineered at HQ in New Plymouth, Taranaki. Deployable strictly at the edge.
- **When:** Active development as of June 2026.
- **Why:** To guarantee data sovereignty by keeping tenant operational data local and strictly partitioned.

---

## The Problem We Are Solving

The problem we are solving is ensuring secure, tenant-isolated AI operations in multi-client environments without reliance on external cloud services that risk data leakage or compliance violations.

Additional challenges addressed:
1. **Data Leakage & Compliance** — Sending sensitive industrial data to external LLM providers is unacceptable.
2. **Tenant Cross-Contamination** — Risk of mixing client data in shared systems.
3. **Rigid Routing** — Inability of static helpdesks to adapt intelligently to varied requests.

---

## Key Features

- Tenant-aware multi-agent orchestration (Intake, Fulfilment, Resolution)
- Strict data isolation via SQLAlchemy and tenant-partitioned vector stores
- Local LangGraph-based state machine for adaptive routing
- Modular knowledge base with RAG support
- White-label ready for industry-specific deployments
- Full offline edge capability

---

## Quick Start

### Prerequisites

- Python 3.10+
- Ollama with a local LLM Gemma 4 E4B
- PostgreSQL (optional) or in-memory mode

### Installation & Setup

We provide separate guides for system environment setup and installation for Windows and Linux users:

* **Prerequisites & System Setup Guide**: Read [setup.md](setup.md)
* **Installation Guide**: Read [installation.md](installation.md)

### Quick Start (Automated Setup)
The fastest way to install is running the cross-platform bootstrap script:

```bash
python bootstrap.py
```

Weaver
python bootstrap.py
```

### Manual Installation

<details open>
<summary><strong>🐧 Linux / macOS (Bash)</strong></summary>

```bash
git clone https://github.com/fivepanelhat/weaver.git
cd weaver

python3 -m venv venv
source venv/bin/activate

pip install git+https://github.com/fivepanelhat/coastal-alpine-core.git@v0.2.0
pip install -r requirements.txt
pip install -r requirements-dev.txt
cp .env.example .env
```

</details>

<details>
<summary><strong>🪟 Windows (PowerShell)</strong></summary>

```powershell
git clone https://github.com/fivepanelhat/weaver.git
cd weaver

python -m venv venv
.\venv\Scripts\Activate.ps1

pip install git+https://github.com/fivepanelhat/coastal-alpine-core.git@v0.2.0
pip install -r requirements.txt
pip install -r requirements-dev.txt
Copy-Item .env.example .env
```

> **Note:** If you receive an execution policy error, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` first.

</details>

### Model Setup & Validation

Ensure Ollama is running locally and pull the target model:
```bash
ollama pull gemma4:e4b
python demo.py
```

To run smoke tests validating state graph transitions:
```bash
pytest
```

---

## Architecture Overview

Weaver routes multi-tenant requests entirely on the edge node: **RPi 5 16GB + Hailo-10H**, local Ollama, and tenant-isolated stores. No tenant data leaves the deployment site.

![Weaver architecture — liquid glass overview](assets/architecture_overview.png)

### System map

```mermaid
%%{init: {
  "theme": "dark",
  "themeVariables": {
    "fontSize": "16px",
    "fontFamily": "Inter, ui-sans-serif, system-ui, sans-serif",
    "primaryColor": "#0ea5e9",
    "primaryTextColor": "#f8fafc",
    "primaryBorderColor": "#38bdf8",
    "lineColor": "#67e8f9",
    "secondaryColor": "#1e293b",
    "tertiaryColor": "#0f172a",
    "clusterBkg": "#0b1220cc",
    "clusterBorder": "#38bdf880",
    "titleColor": "#e2e8f0"
  },
  "flowchart": {
    "nodeSpacing": 40,
    "rankSpacing": 48,
    "padding": 20,
    "htmlLabels": true,
    "curve": "basis"
  }
}}%%
flowchart TB

    classDef sense fill:#052e16,stroke:#4ade80,stroke-width:2px,color:#f0fdf4
    classDef edge fill:#0c4a6e,stroke:#38bdf8,stroke-width:2px,color:#f0f9ff
    classDef core fill:#134e4a,stroke:#2dd4bf,stroke-width:2px,color:#f0fdfa
    classDef act fill:#422006,stroke:#fbbf24,stroke-width:2px,color:#fffbeb
    classDef store fill:#1e1b4b,stroke:#a5b4fc,stroke-width:2px,color:#eef2ff
    classDef ai fill:#3b0764,stroke:#e879f9,stroke-width:2px,color:#fdf4ff
    classDef app fill:#1e1b4b,stroke:#c4b5fd,stroke-width:2px,color:#eef2ff

    U["User / operator query"] --> ORCH["LangGraph orchestrator"]
    ORCH --> IN["Intake agent<br/>auth · tenant scope"]
    ORCH --> FU["Fulfilment agent<br/>RAG · tools"]
    ORCH --> RE["Resolution agent<br/>response · actions"]
    IN & FU & RE --> KB["Tenant-aware knowledge base"]
    KB --> STORE["Isolated vector + SQL store"]
    STORE --> LLM["Local LLM via Ollama<br/>Gemma 4 e4b"]
    LLM --> ORCH
    ORCH --> OUT["Actions & responses"]

    subgraph EDGE["Sovereign edge — RPi 5 16GB + Hailo-10H"]
        ORCH
        KB
        STORE
        LLM
    end

    class U,OUT act
    class ORCH,IN,FU,RE core
    class KB,STORE store
    class LLM ai
```

| Layer | Components | Role |
| :--- | :--- | :--- |
| **Orchestrator** | LangGraph state machine | Deterministic multi-agent routing |
| **Agents** | Intake · Fulfilment · Resolution | Tenant-scoped task handling |
| **Knowledge** | Isolated vector + SQL | No cross-tenant leakage |
| **Inference** | Ollama on-device | Offline-capable responses |
| **Hardware** | RPi 5 16GB + Hailo-10H | Canonical Coastal Alpine target |

*Full detail: [ARCHITECTURE.md](./ARCHITECTURE.md)*

## Directory Structure

```bash
Weaver/
├── agent_knowledge_base/      # Policy, ethics, and platform runbooks
├── langgraph/                 # Core Graph structures
│   ├── graph.py               # StateGraph compiler
│   ├── llm.py                 # Local Ollama client bridge
│   └── orchestrator.py        # Graph processing nodes
├── tests/                     # Automated testing suite
│   └── test_orchestrator.py   # StateGraph smoke tests
├── .env.example
├── requirements.txt
├── requirements-dev.txt
├── demo.py                    # Local simulation runner
├── database.py                # Database connection utilities
├── models.py                  # SQLAlchemy relational & vector schemas
├── ARCHITECTURE.md            # System design details
└── README.md                  # This file
```

---

## Technology Stack

**Hardware**  
- **Raspberry Pi 5 (16GB)** with **Hailo-10H NPU** (40 TOPS AI Accelerator / AI HAT+ 2)

**Software**  
- Orchestration: LangGraph  
- Inference: Ollama + Local LLMs  
- Data: SQLAlchemy + pgvector / local vector stores  
- Deployment: Docker-ready, systemd compatible

---

## Real-World Examples and Implementation

- **Civil Construction Helpdesk**: Deployed on-premise at a New Zealand construction firm to route project compliance queries across multiple subcontractors while   maintaining strict data isolation per client.
- **Agritech Support Platform**: Used by cooperatives in Horowhenua to provide localized advisory services without exposing farm data to third-party clouds.
- **White-Label Service Providers**: Integrated into existing SaaS platforms where clients demand sovereign data handling.

**Implementation Notes:**
- Install on a dedicated edge server or Raspberry Pi cluster.
- Configure tenant IDs at database and vector store level for isolation.
- Use systemd services for persistent operation and monitor via local dashboards.
- Start with the `demo.py` to validate routing and isolation before production scaling.

---

## Performance & Benchmarks

* **Local Inference Latency:** ~1.10 seconds per routing decision executing Gemma 4 E4B via Ollama.
* **Energy Consumption:** Average active power draw is ~6.2W running on a headless Raspberry Pi 5 16GB node.
* **Storage Footprint:** SQL and vectorized SQLite databases consume <200MB, leaving ample space on edge SD cards.

---

## Documentation

- [ARCHITECTURE.md](./ARCHITECTURE.md)
- [agent_knowledge_base/platform_runbook.md](./agent_knowledge_base/platform_runbook.md)
- [agent_knowledge_base/ethics_review_playbook.md](./agent_knowledge_base/ethics_review_playbook.md)
- [CHANGELOG.md](./CHANGELOG.md)

---

## License

This project is licensed under the **Coastal Alpine Tech Limited License** (proprietary / commercial) — the same license used across the Kiwi Edge AI Stack (Weaver, AquaGuard, SoilGuard, Blue-Moon, Sting-Operation, Coastal-Alpine-Core, coastal-alpine-stack, Sovereign-Edge-Firmware, fivepanelhat).

- Full terms: [LICENSE](./LICENSE)
- No open-source grant is implied by access to this repository
- Commercial use requires a written agreement with Coastal Alpine Tech Limited

---

**Built with focus on data sovereignty and edge intelligence.**  
Questions or collaboration? Contact Coastal Alpine Tech Limited.

---

*Last updated: June 2026*

---

## Project badges

Status badges for this repository (CI, security, license, and stack metadata):

[![License](https://img.shields.io/badge/License-Proprietary--Commercial-blue?style=flat-square)](LICENSE)  
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square)](https://www.python.org/)  
[![Hardware Target](https://img.shields.io/badge/Hardware-Raspberry%20Pi%205%2016GB-C11A5B?style=flat-square&logo=raspberry-pi&logoColor=white)]()  
[![NPU Acceleration](https://img.shields.io/badge/NPU-Hailo--10H%20Accelerated-005A9C?style=flat-square)]()  
[![Sovereignty](https://img.shields.io/badge/Sovereignty-NZ%20Data%20Bound-00247D?style=flat-square)]()  
[![CI](https://github.com/fivepanelhat/Weaver/actions/workflows/ci-scan.yml/badge.svg?branch=main)](https://github.com/fivepanelhat/Weaver/actions/workflows/ci-scan.yml)  
[![SecOps](https://img.shields.io/github/actions/workflow/status/fivepanelhat/Weaver/secops.yml?branch=main&label=SecOps&style=flat-square&color=success)](https://github.com/fivepanelhat/Weaver/actions/workflows/secops.yml)  
[![RedTeam](https://img.shields.io/github/actions/workflow/status/fivepanelhat/Weaver/redteam.yml?branch=main&label=RedTeam&style=flat-square&color=critical)](https://github.com/fivepanelhat/Weaver/actions/workflows/redteam.yml)  
[![Dependabot](https://img.shields.io/badge/Dependencies-Monitored-brightgreen?style=flat-square&logo=dependabot)]()  
[![Sustainability](https://img.shields.io/badge/EECA%20NZ-Carbon%20Tracked-green?style=flat-square)]()
