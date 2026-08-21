#!/usr/bin/env bash
# Weaver — dual-platform installer (Linux / macOS)
#
# One-line:
#   curl -fsSL https://raw.githubusercontent.com/fivepanelhat/Weaver/main/install.sh | bash
#
# From a clone:
#   ./install.sh
#
# Creates a virtualenv, installs Coastal-Alpine-Core + Weaver deps, copies .env.
set -euo pipefail

REPO_URL="${WEAVER_REPO_URL:-https://github.com/fivepanelhat/Weaver.git}"
INSTALL_DIR="${WEAVER_HOME:-$HOME/.weaver-app}"
VENV_DIR="$INSTALL_DIR/venv"
CORE_GIT="${CORE_GIT_URL:-git+https://github.com/fivepanelhat/Coastal-Alpine-Core.git@v0.5.9}"

info() { printf '\033[36m[weaver]\033[0m %s\n' "$1"; }
warn() { printf '\033[33m[weaver]\033[0m %s\n' "$1"; }
err()  { printf '\033[31m[weaver]\033[0m %s\n' "$1" >&2; }

PYTHON_BIN="$(command -v python3 || command -v python || true)"
if [[ -z "$PYTHON_BIN" ]]; then
  err "Python 3.10+ is required. On Debian/Ubuntu/RPi OS:"
  err "  sudo apt-get install -y python3 python3-venv python3-pip git build-essential"
  exit 1
fi
PY_VER="$("$PYTHON_BIN" -c 'import sys; print("%d.%d" % sys.version_info[:2])')"

# Python version gate
PY_MAJOR="$("$PYTHON_BIN" -c 'import sys; print(sys.version_info[0])')"
PY_MINOR="$("$PYTHON_BIN" -c 'import sys; print(sys.version_info[1])')"
if [[ "$PY_MAJOR" -lt 3 ]] || { [[ "$PY_MAJOR" -eq 3 ]] && [[ "$PY_MINOR" -lt 10 ]]; }; then
  err "Python 3.10+ is required (found ${PY_MAJOR}.${PY_MINOR})."
  exit 1
fi
info "Using Python $PY_VER ($PYTHON_BIN)"

if [[ -f "bootstrap.py" ]] && [[ -f "requirements.txt" || -f "pyproject.toml" ]]; then
  SRC_DIR="$(pwd)"
  info "Installing from current checkout: $SRC_DIR"
else
  if ! command -v git >/dev/null 2>&1; then
    err "git is required to fetch Weaver. Install git or run from a clone."
    exit 1
  fi
  mkdir -p "$INSTALL_DIR"
  SRC_DIR="$INSTALL_DIR/src"
  if [[ -d "$SRC_DIR/.git" ]]; then
    info "Updating existing checkout in $SRC_DIR"
    git -C "$SRC_DIR" pull --ff-only || warn "Could not fast-forward; using existing checkout."
  else
    info "Cloning $REPO_URL"
    git clone --depth 1 "$REPO_URL" "$SRC_DIR"
  fi
fi

cd "$SRC_DIR"

# Prefer cross-platform bootstrap when present
if [[ -f "bootstrap.py" ]]; then
  info "Running bootstrap.py (venv + Core + dependencies)"
  "$PYTHON_BIN" bootstrap.py
  echo
  info "Done. Activate with:  source $SRC_DIR/venv/bin/activate"
  info "Validate:  python demo.py   |   pytest"
  exit 0
fi

info "Creating virtualenv at $VENV_DIR"
"$PYTHON_BIN" -m venv "$VENV_DIR"
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"
python -m pip install --upgrade pip >/dev/null

info "Installing Coastal-Alpine-Core (hybrid SDK)"
pip install "$CORE_GIT"

if [[ -f requirements.txt ]]; then
  info "Installing requirements.txt"
  pip install -r requirements.txt
fi
if [[ -f requirements-dev.txt ]]; then
  info "Installing requirements-dev.txt"
  pip install -r requirements-dev.txt
fi
if [[ -f .env.example && ! -f .env ]]; then
  cp .env.example .env
  info "Copied .env.example → .env"
fi

echo
info "Done. Activate:  source $VENV_DIR/bin/activate"
info "Pull a model:    ollama pull gemma4:e4b"
info "Validate:        python demo.py"
