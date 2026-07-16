# Installation Guide - Weaver

Follow the instructions for your OS. Weaver runs on **Windows**, **Linux**, and **macOS** for development; production edge remains **RPi 5 16GB + Hailo-10H**.

Hybrid stack: installs **Coastal-Alpine-Core** automatically (SecurityGuard, Telemetry, SovereignOllamaClient). Optional companion: [Aether](https://github.com/fivepanelhat/Aether).

Prerequisites: [setup.md](setup.md).

---

## Linux / macOS

### Option 1: One-line installer (recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/fivepanelhat/Weaver/main/install.sh | bash
```

### Option 2: Bootstrap from clone

```bash
git clone https://github.com/fivepanelhat/Weaver.git
cd Weaver
python3 bootstrap.py
source venv/bin/activate
```

### Option 3: Manual setup

```bash
git clone https://github.com/fivepanelhat/Weaver.git
cd Weaver
python3 -m venv venv
source venv/bin/activate
pip install -U pip
pip install "git+https://github.com/fivepanelhat/Coastal-Alpine-Core.git@v0.5.4"
pip install -r requirements.txt
pip install -r requirements-dev.txt
cp .env.example .env
ollama pull gemma4:e4b
python demo.py
```

---

## Windows

### Option 1: One-line installer (recommended)

```powershell
irm https://raw.githubusercontent.com/fivepanelhat/Weaver/main/install.ps1 | iex
```

### Option 2: Bootstrap from clone

```powershell
git clone https://github.com/fivepanelhat/Weaver.git
cd Weaver
python bootstrap.py
.\venv\Scripts\Activate.ps1
```

### Option 3: Manual setup

```powershell
git clone https://github.com/fivepanelhat/Weaver.git
cd Weaver
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install "git+https://github.com/fivepanelhat/Coastal-Alpine-Core.git@v0.5.4"
pip install -r requirements.txt
pip install -r requirements-dev.txt
Copy-Item .env.example .env
ollama pull gemma4:e4b
python demo.py
```

> If activation fails: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

---

## Validate

```bash
pytest
python demo.py
```

---

## Next: hybrid stack

| Component | Purpose |
| :--- | :--- |
| [Coastal-Alpine-Core](https://github.com/fivepanelhat/Coastal-Alpine-Core) | Shared SDK already installed as a dependency |
| [Aether](https://github.com/fivepanelhat/Aether) | Agentic companion, skills, computer use |
| [coastal-alpine-stack](https://github.com/fivepanelhat/coastal-alpine-stack) | Full monorepo (portals, MQTT, K3s) |
