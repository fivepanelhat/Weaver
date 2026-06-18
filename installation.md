# Installation Guide - Weaver

Follow the instructions below to install Weaver on your operating system.

## Linux Installation

### Option 1: Automated Setup (Recommended)
Run the bootstrap script, which creates the virtual environment, configures environment files, upgrades pip, and installs all dependencies:
```bash
python3 bootstrap.py
```

### Option 2: Manual Setup
If you prefer to perform the setup steps manually:
1. Clone the repository:
   ```bash
   git clone https://github.com/fivepanelhat/Weaver.git
   cd Weaver
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Upgrade pip and install dependencies:
   ```bash
   pip install --upgrade pip
   pip install git+https://github.com/fivepanelhat/coastal-alpine-core.git
   pip install -r requirements-dev.txt
   ```

---

## Windows Installation

### Option 1: Automated Setup (Recommended)
Run the bootstrap script in PowerShell or Command Prompt:
```powershell
python bootstrap.py
```

### Option 2: Manual Setup
If you prefer to perform the setup steps manually:
1. Clone the repository:
   ```powershell
   git clone https://github.com/fivepanelhat/Weaver.git
   cd Weaver
   ```
2. Create and activate a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Upgrade pip and install dependencies:
   ```powershell
   python -m pip install --upgrade pip
   pip install git+https://github.com/fivepanelhat/coastal-alpine-core.git
   pip install -r requirements-dev.txt
   ```
