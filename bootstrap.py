#!/usr/bin/env python3
"""
Coastal Alpine Tech Limited — Cross-Platform Bootstrap Script
==============================================================
Universal installer that works on Windows, Linux, and macOS.
Creates a virtual environment, installs dependencies, and validates the setup.

Usage:
    python bootstrap.py                   # Full install (root monorepo)
    python bootstrap.py --portal-only     # Install portal deps only (run from portal dir)
    python bootstrap.py --help            # Show help

Works with:
    - Windows (PowerShell, CMD)
    - Linux / macOS (Bash, Zsh)
    - Python 3.10+
"""

import os
import platform
import shutil
import subprocess
import sys
import venv


# ── Configuration ──────────────────────────────────────────────────────────

VENV_DIR = "venv"          # Portal-level venv name
ROOT_VENV_DIR = ".venv"    # Root monorepo venv name

PORTALS = [
    "AquaGuard-Portal",
    "Blue-Moon-Portal",
    "SoilGuard-Portal",
    "Sting-Operation-AI",
    "Weaver",
]

CORE_PACKAGE = "coastal_alpine_core"
CORE_GIT_URL = "https://github.com/fivepanelhat/coastal-alpine-core.git"


# ── Helpers ────────────────────────────────────────────────────────────────

def is_windows():
    return sys.platform == "win32"


def get_venv_dir():
    """Determine which venv directory name to use based on context."""
    # If we're in the root monorepo (has .gitmodules), use .venv
    if os.path.exists(".gitmodules") or os.path.exists(CORE_PACKAGE):
        return ROOT_VENV_DIR
    return VENV_DIR


def get_pip_exe(venv_path):
    """Return the path to pip inside the venv."""
    if is_windows():
        return os.path.join(venv_path, "Scripts", "pip.exe")
    return os.path.join(venv_path, "bin", "pip")


def get_python_exe(venv_path):
    """Return the path to python inside the venv."""
    if is_windows():
        return os.path.join(venv_path, "Scripts", "python.exe")
    return os.path.join(venv_path, "bin", "python")


def get_activate_cmd(venv_path):
    """Return the activation command for user display."""
    if is_windows():
        return f".\\{venv_path}\\Scripts\\Activate.ps1"
    return f"source {venv_path}/bin/activate"


def run_cmd(cmd, description=None):
    """Run a shell command with error handling."""
    if description:
        print(f"  → {description}")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Command failed: {cmd}")
        if e.stderr:
            # Show only last 5 lines of stderr to avoid wall of text
            lines = e.stderr.strip().split("\n")
            for line in lines[-5:]:
                print(f"    {line}")
        return None


def print_header(text):
    print(f"\n{'─' * 60}")
    print(f"  {text}")
    print(f"{'─' * 60}")


def print_step(step, total, text):
    print(f"\n[{step}/{total}] {text}")


# ── Core Logic ─────────────────────────────────────────────────────────────

def create_venv(venv_path):
    """Create a virtual environment if it doesn't exist."""
    if os.path.exists(venv_path):
        print(f"  ✓ Virtual environment '{venv_path}' already exists")
        return True

    print(f"  Creating virtual environment '{venv_path}'...")
    try:
        venv.create(venv_path, with_pip=True, upgrade_deps=True)
        print(f"  ✓ Virtual environment created")
        return True
    except Exception as e:
        print(f"  ✗ Failed to create venv: {e}")
        return False


def install_requirements(pip_exe, req_file):
    """Install a requirements file."""
    if not os.path.exists(req_file):
        print(f"  ⊘ {req_file} not found, skipping")
        return True

    result = run_cmd(
        f'"{pip_exe}" install -r {req_file}',
        f"Installing {req_file}",
    )
    return result is not None


def install_core(pip_exe, editable=False):
    """Install coastal_alpine_core package."""
    if editable and os.path.exists(CORE_PACKAGE):
        result = run_cmd(
            f'"{pip_exe}" install -e ./{CORE_PACKAGE}',
            "Installing coastal_alpine_core (editable mode)",
        )
    else:
        result = run_cmd(
            f'"{pip_exe}" install git+{CORE_GIT_URL}',
            "Installing coastal_alpine_core from GitHub",
        )
    return result is not None


def copy_env_example():
    """Copy .env.example to .env if it exists and .env doesn't."""
    if os.path.exists(".env.example") and not os.path.exists(".env"):
        shutil.copy2(".env.example", ".env")
        print("  ✓ Copied .env.example → .env")
    elif os.path.exists(".env"):
        print("  ✓ .env already exists")
    else:
        print("  ⊘ No .env.example found")


def detect_context():
    """Detect if we're in the root monorepo or a portal subdirectory."""
    if os.path.exists(".gitmodules") or os.path.exists(CORE_PACKAGE):
        return "monorepo"
    for portal in PORTALS:
        basename = os.path.basename(os.getcwd())
        if basename == portal or basename == portal.lower():
            return "portal"
    # Check for portal indicators
    if os.path.exists("portal_core") or os.path.exists("portal_schemas"):
        return "portal"
    return "standalone"


# ── Entry Points ───────────────────────────────────────────────────────────

def setup_monorepo():
    """Full monorepo setup: venv, core, dev deps."""
    venv_path = ROOT_VENV_DIR
    total_steps = 4

    print_header("Coastal Alpine Stack — Monorepo Setup")
    print(f"  Platform: {platform.system()} ({platform.machine()})")
    print(f"  Python:   {sys.version.split()[0]}")

    # Step 1: Create venv
    print_step(1, total_steps, "Virtual Environment")
    if not create_venv(venv_path):
        sys.exit(1)

    pip_exe = get_pip_exe(venv_path)

    # Step 2: Upgrade pip
    print_step(2, total_steps, "Upgrading pip")
    run_cmd(f'"{pip_exe}" install --upgrade pip', "Upgrading pip")

    # Step 3: Install core
    print_step(3, total_steps, "Installing coastal_alpine_core")
    install_core(pip_exe, editable=True)

    # Step 4: Install dev requirements
    print_step(4, total_steps, "Installing dev dependencies")
    install_requirements(pip_exe, "requirements-dev.txt")

    # Done
    print_header("Setup Complete")
    activate = get_activate_cmd(venv_path)
    print(f"  To activate your environment:\n    {activate}\n")
    print(f"  To set up a specific portal:")
    print(f"    cd <portal-name>")
    print(f"    python bootstrap.py\n")


def setup_portal():
    """Portal-level setup: venv, core from GitHub, requirements."""
    venv_path = VENV_DIR
    portal_name = os.path.basename(os.getcwd())
    total_steps = 5

    print_header(f"{portal_name} — Portal Setup")
    print(f"  Platform: {platform.system()} ({platform.machine()})")
    print(f"  Python:   {sys.version.split()[0]}")

    # Step 1: Create venv
    print_step(1, total_steps, "Virtual Environment")
    if not create_venv(venv_path):
        sys.exit(1)

    pip_exe = get_pip_exe(venv_path)

    # Step 2: Upgrade pip
    print_step(2, total_steps, "Upgrading pip")
    run_cmd(f'"{pip_exe}" install --upgrade pip', "Upgrading pip")

    # Step 3: Install core
    print_step(3, total_steps, "Installing coastal_alpine_core")
    install_core(pip_exe, editable=False)

    # Step 4: Install requirements
    print_step(4, total_steps, "Installing dependencies")
    install_requirements(pip_exe, "requirements.txt")
    install_requirements(pip_exe, "requirements-dev.txt")

    # Step 5: Environment config
    print_step(5, total_steps, "Environment Configuration")
    copy_env_example()

    # Done
    print_header("Setup Complete")
    activate = get_activate_cmd(venv_path)
    print(f"  To activate your environment:\n    {activate}\n")


def main():
    # Parse args
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        sys.exit(0)

    portal_only = "--portal-only" in sys.argv

    # Detect context
    context = detect_context()

    if portal_only or context == "portal":
        setup_portal()
    elif context == "monorepo":
        setup_monorepo()
    else:
        # Default: treat as portal
        setup_portal()


if __name__ == "__main__":
    main()
