#!/usr/bin/env python3
"""
Coastal Alpine Tech Limited — Cross-Platform Bootstrap Script
==============================================================
Universal installer for Windows, Linux, and macOS.
Creates a virtual environment, installs Coastal-Alpine-Core + deps, validates.

Usage:
    python bootstrap.py                   # Auto-detect monorepo vs portal
    python bootstrap.py --portal-only     # Force portal mode
    python bootstrap.py --help

Requires: Python 3.10+
"""

from __future__ import annotations

import os
import platform
import shlex
import shutil
import subprocess
import sys
import venv

VENV_DIR = "venv"
ROOT_VENV_DIR = ".venv"

PORTALS = [
    "AquaGuard-Portal",
    "Blue-Moon-Portal",
    "SoilGuard-Portal",
    "Sting-Operation-AI",
    "Weaver",
]

CORE_PACKAGE = "coastal_alpine_core"
# Canonical GitHub repo + pin (case-sensitive path on Linux clones)
CORE_GIT_URL = "https://github.com/fivepanelhat/Coastal-Alpine-Core.git@v0.5.4"


def is_windows() -> bool:
    return sys.platform == "win32"


def require_python_310() -> None:
    if sys.version_info < (3, 10):
        print(
            f"✗ Python 3.10+ required (found {sys.version.split()[0]}). "
            "Install from https://www.python.org or your OS package manager."
        )
        sys.exit(1)


def get_venv_dir() -> str:
    if os.path.exists(".gitmodules") or os.path.exists(CORE_PACKAGE):
        return ROOT_VENV_DIR
    return VENV_DIR


def get_pip_exe(venv_path: str) -> str:
    if is_windows():
        return os.path.join(venv_path, "Scripts", "pip.exe")
    return os.path.join(venv_path, "bin", "pip")


def get_python_exe(venv_path: str) -> str:
    if is_windows():
        return os.path.join(venv_path, "Scripts", "python.exe")
    return os.path.join(venv_path, "bin", "python")


def get_activate_cmd(venv_path: str) -> str:
    if is_windows():
        return f".\\{venv_path}\\Scripts\\Activate.ps1"
    return f"source {venv_path}/bin/activate"


def run_cmd(cmd, description=None, critical: bool = True) -> bool:
    if description:
        print(f"  → {description}")
    try:
        args = cmd if isinstance(cmd, list) else shlex.split(cmd)
        subprocess.run(args, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Command failed: {args if isinstance(cmd, list) else cmd}")
        if e.stderr:
            for line in e.stderr.strip().split("\n")[-12:]:
                print(f"    {line}")
        if critical:
            print("  ✗ Install cannot continue (critical step failed).")
            sys.exit(1)
        return False


def print_header(text: str) -> None:
    print(f"\n{'─' * 60}")
    print(f"  {text}")
    print(f"{'─' * 60}")


def print_step(step: int, total: int, text: str) -> None:
    print(f"\n[{step}/{total}] {text}")


def create_venv(venv_path: str) -> bool:
    if os.path.exists(venv_path):
        print(f"  ✓ Virtual environment '{venv_path}' already exists")
        return True
    print(f"  Creating virtual environment '{venv_path}'...")
    try:
        # upgrade_deps can fail on locked/offline hosts — create without it first
        try:
            venv.create(venv_path, with_pip=True, upgrade_deps=True)
        except TypeError:
            venv.create(venv_path, with_pip=True)
        except Exception:
            # retry without upgrade_deps
            if os.path.exists(venv_path):
                shutil.rmtree(venv_path, ignore_errors=True)
            venv.create(venv_path, with_pip=True)
        print("  ✓ Virtual environment created")
        return True
    except Exception as e:
        print(f"  ✗ Failed to create venv: {e}")
        return False


def install_requirements(pip_exe: str, req_file: str, critical: bool = True) -> bool:
    if not os.path.exists(req_file):
        print(f"  ⊘ {req_file} not found, skipping")
        return True
    return run_cmd(
        [pip_exe, "install", "-r", req_file],
        f"Installing {req_file}",
        critical=critical,
    )


def install_core(pip_exe: str, editable: bool = False) -> bool:
    if editable and os.path.exists(CORE_PACKAGE):
        return run_cmd(
            [pip_exe, "install", "-e", f"./{CORE_PACKAGE}"],
            "Installing coastal_alpine_core (editable mode)",
            critical=True,
        )
    # Prefer git+ URL with pin; fall back to main if tag missing
    ok = run_cmd(
        [pip_exe, "install", f"git+{CORE_GIT_URL}"],
        f"Installing coastal_alpine_core from GitHub ({CORE_GIT_URL})",
        critical=False,
    )
    if ok:
        return True
    print("  → Retrying Core install from main branch…")
    return run_cmd(
        [
            pip_exe,
            "install",
            "git+https://github.com/fivepanelhat/Coastal-Alpine-Core.git",
        ],
        "Installing coastal_alpine_core from GitHub (main)",
        critical=True,
    )


def copy_env_example() -> None:
    if os.path.exists(".env.example") and not os.path.exists(".env"):
        shutil.copy2(".env.example", ".env")
        print("  ✓ Copied .env.example → .env")
    elif os.path.exists(".env"):
        print("  ✓ .env already exists")
    else:
        print("  ⊘ No .env.example found")


def detect_context() -> str:
    if os.path.exists(".gitmodules") or os.path.exists(CORE_PACKAGE):
        return "monorepo"
    basename = os.path.basename(os.getcwd())
    for portal in PORTALS:
        if basename == portal or basename.lower() == portal.lower():
            return "portal"
    if os.path.exists("portal_core") or os.path.exists("portal_schemas") or os.path.exists("requirements.txt"):
        return "portal"
    return "standalone"


def verify_import(python_exe: str) -> None:
    run_cmd(
        [
            python_exe,
            "-c",
            "import coastal_alpine_core; print('coastal_alpine_core OK', getattr(coastal_alpine_core, '__version__', ''))",
        ],
        "Verifying coastal_alpine_core import",
        critical=True,
    )


def setup_monorepo() -> None:
    venv_path = ROOT_VENV_DIR
    total = 5
    print_header("Coastal Alpine Stack — Monorepo Setup")
    print(f"  Platform: {platform.system()} ({platform.machine()})")
    print(f"  Python:   {sys.version.split()[0]}")

    print_step(1, total, "Virtual Environment")
    if not create_venv(venv_path):
        sys.exit(1)
    pip_exe = get_pip_exe(venv_path)
    py_exe = get_python_exe(venv_path)

    print_step(2, total, "Upgrading pip")
    run_cmd([pip_exe, "install", "--upgrade", "pip"], "Upgrading pip", critical=True)

    print_step(3, total, "Installing coastal_alpine_core")
    install_core(pip_exe, editable=True)

    print_step(4, total, "Installing dev dependencies")
    install_requirements(pip_exe, "requirements-dev.txt", critical=False)
    install_requirements(pip_exe, "requirements-optional.txt", critical=False)
    install_requirements(pip_exe, "requirements.txt", critical=False)

    print_step(5, total, "Verify")
    verify_import(py_exe)

    print_header("Setup Complete")
    print(f"  Activate:\n    {get_activate_cmd(venv_path)}\n")


def setup_portal() -> None:
    venv_path = VENV_DIR
    portal_name = os.path.basename(os.getcwd())
    total = 6
    print_header(f"{portal_name} — Portal Setup")
    print(f"  Platform: {platform.system()} ({platform.machine()})")
    print(f"  Python:   {sys.version.split()[0]}")

    print_step(1, total, "Virtual Environment")
    if not create_venv(venv_path):
        sys.exit(1)
    pip_exe = get_pip_exe(venv_path)
    py_exe = get_python_exe(venv_path)

    print_step(2, total, "Upgrading pip")
    run_cmd([pip_exe, "install", "--upgrade", "pip"], "Upgrading pip", critical=True)

    print_step(3, total, "Installing coastal_alpine_core")
    install_core(pip_exe, editable=False)

    print_step(4, total, "Installing dependencies")
    if not install_requirements(pip_exe, "requirements.txt", critical=True):
        sys.exit(1)
    install_requirements(pip_exe, "requirements-dev.txt", critical=False)
    install_requirements(pip_exe, "requirements-optional.txt", critical=False)

    print_step(5, total, "Environment configuration")
    copy_env_example()

    print_step(6, total, "Verify")
    verify_import(py_exe)

    print_header("Setup Complete")
    print(f"  Activate:\n    {get_activate_cmd(venv_path)}\n")
    print("  Next: pull a local model if needed —  ollama pull gemma4:e4b\n")


def main() -> None:
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        sys.exit(0)

    require_python_310()
    portal_only = "--portal-only" in sys.argv
    context = detect_context()

    if portal_only or context == "portal":
        setup_portal()
    elif context == "monorepo":
        setup_monorepo()
    else:
        setup_portal()


if __name__ == "__main__":
    main()
