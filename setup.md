# Environment & Prerequisites Setup Guide - Weaver

This guide lists system prerequisites **before** installing Weaver on **Windows** or **Linux**. Production edge target remains **Raspberry Pi 5 (16GB) + Hailo-10H**.

Hybrid dependencies: **Coastal-Alpine-Core** (required SDK), optional **Aether** (companion), optional **coastal-alpine-stack** (monorepo).

---

## Shared requirements (all platforms)

| Component | Version / notes |
| :--- | :--- |
| **Python** | 3.10+ (3.11+ recommended) |
| **Git** | Any recent release |
| **pip / venv** | Bundled with Python |
| **Ollama** | Local LLM runtime - [ollama.com](https://ollama.com) |
| **Model** | e.g. `ollama pull gemma4:e4b` |
| **Core SDK** | Coastal-Alpine-Core `@v0.5.4` (or newer tagged release) |

Optional:

- **PostgreSQL** for multi-tenant production stores (in-memory / SQLite OK for demos)
- **Docker** for stack compose (Mosquitto, etc.) when working inside coastal-alpine-stack

---

## Linux setup (Ubuntu / Debian / Raspberry Pi OS)

### 1. System packages

```bash
sudo apt-get update
sudo apt-get install -y \
 python3 python3-dev python3-venv python3-pip \
 git build-essential
```

### 2. Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull gemma4:e4b
```

### 3. Install Weaver

```bash
# One-liner
curl -fsSL https://raw.githubusercontent.com/fivepanelhat/Weaver/main/install.sh | bash

# Or from clone
git clone https://github.com/fivepanelhat/Weaver.git
cd Weaver
./install.sh
# or: python3 bootstrap.py
```

See [installation.md](installation.md) for manual steps.

---

## Windows setup (Windows 10 / 11)

### 1. Prerequisites

1. **Python 3.10+** from [python.org](https://www.python.org/downloads/) - enable **Add Python to PATH** and **py launcher**.
2. **Git for Windows** from [git-scm.com](https://git-scm.com/).
3. **PowerShell 5.1+** or **PowerShell 7+** (recommended).

If `Activate.ps1` is blocked:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### 2. Ollama

Install from [ollama.com](https://ollama.com/download/windows), then:

```powershell
ollama pull gemma4:e4b
```

### 3. Install Weaver

```powershell
# One-liner
irm https://raw.githubusercontent.com/fivepanelhat/Weaver/main/install.ps1 | iex

# Or from clone
git clone https://github.com/fivepanelhat/Weaver.git
cd Weaver
powershell -ExecutionPolicy Bypass -File .\install.ps1
# or: python bootstrap.py
```

---

## Hybrid companion (optional)

| Tool | Linux | Windows |
| :--- | :--- | :--- |
| **Aether** | `curl -fsSL https://raw.githubusercontent.com/fivepanelhat/Aether/main/install.sh \| bash` | `irm https://raw.githubusercontent.com/fivepanelhat/Aether/main/install.ps1 \| iex` |
| **Core only** | `curl -fsSL https://raw.githubusercontent.com/fivepanelhat/Coastal-Alpine-Core/main/install.sh \| bash` | `irm https://raw.githubusercontent.com/fivepanelhat/Coastal-Alpine-Core/main/install.ps1 \| iex` |
| **Full stack** | `curl -fsSL https://raw.githubusercontent.com/fivepanelhat/coastal-alpine-stack/main/install.sh \| bash` | `irm https://raw.githubusercontent.com/fivepanelhat/coastal-alpine-stack/main/install.ps1 \| iex` |

---

## Verify

```bash
# After venv activate
python -c "import coastal_alpine_core; print('core ok')"
python demo.py
pytest
```

On Windows, use the same commands inside an activated PowerShell venv (`.\venv\Scripts\Activate.ps1`).
