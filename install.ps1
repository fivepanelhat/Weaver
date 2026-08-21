# Weaver — dual-platform installer (Windows / PowerShell)
#
# One-line:
#   irm https://raw.githubusercontent.com/fivepanelhat/Weaver/main/install.ps1 | iex
#
# From a clone:
#   powershell -ExecutionPolicy Bypass -File .\install.ps1
#
# Creates a virtualenv, installs Coastal-Alpine-Core + Weaver deps for Windows.

$ErrorActionPreference = "Stop"

$RepoUrl    = if ($env:WEAVER_REPO_URL) { $env:WEAVER_REPO_URL } else { "https://github.com/fivepanelhat/Weaver.git" }
$InstallDir = if ($env:WEAVER_HOME)     { $env:WEAVER_HOME }     else { Join-Path $env:USERPROFILE ".weaver-app" }
$VenvDir    = Join-Path $InstallDir "venv"
$CoreGit    = if ($env:CORE_GIT_URL)    { $env:CORE_GIT_URL }    else { "git+https://github.com/fivepanelhat/Coastal-Alpine-Core.git@v0.5.9" }

function Info($m) { Write-Host "[weaver] $m" -ForegroundColor Cyan }
function Warn($m) { Write-Host "[weaver] $m" -ForegroundColor Yellow }
function Fail($m) { Write-Host "[weaver] $m" -ForegroundColor Red; exit 1 }
function Require-Ok([string]$Step) {
    if ($null -ne $LASTEXITCODE -and $LASTEXITCODE -ne 0) {
        Fail "$Step failed (exit code $LASTEXITCODE)"
    }
}

$PythonBin = $null
foreach ($cand in @("python", "python3", "py")) {
    if (Get-Command $cand -ErrorAction SilentlyContinue) { $PythonBin = $cand; break }
}
if (-not $PythonBin) {
    Fail "Python 3.10+ is required. Install from https://www.python.org (Add to PATH) and re-run."
}
$PyVer = & $PythonBin -c "import sys; print('%d.%d' % sys.version_info[:2])"
& $PythonBin -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)"
if ($LASTEXITCODE -ne 0) { Fail "Python 3.10+ is required (found $PyVer)" }
Info "Using Python $PyVer ($PythonBin)"

if ((Test-Path "bootstrap.py") -and ((Test-Path "requirements.txt") -or (Test-Path "pyproject.toml"))) {
    $SrcDir = (Get-Location).Path
    Info "Installing from current checkout: $SrcDir"
} else {
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        Fail "git is required. Install Git for Windows from https://git-scm.com or run from a clone."
    }
    New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
    $SrcDir = Join-Path $InstallDir "src"
    if (Test-Path (Join-Path $SrcDir ".git")) {
        Info "Updating existing checkout in $SrcDir"
        git -C $SrcDir pull --ff-only 2>$null
    } else {
        Info "Cloning $RepoUrl"
        git clone --depth 1 $RepoUrl $SrcDir
        Require-Ok "git clone"
    }
}

Set-Location $SrcDir

if (Test-Path "bootstrap.py") {
    Info "Running bootstrap.py (venv + Core + dependencies)"
    & $PythonBin bootstrap.py
    Require-Ok "bootstrap"
    Write-Host ""
    Info "Done. Activate with:  .\venv\Scripts\Activate.ps1"
    Info "Validate:  python demo.py   |   pytest"
    exit 0
}

Info "Creating virtualenv at $VenvDir"
& $PythonBin -m venv $VenvDir
Require-Ok "venv create"
$VenvPython = Join-Path $VenvDir "Scripts\python.exe"
& $VenvPython -m pip install --upgrade pip
Require-Ok "pip upgrade"

Info "Installing Coastal-Alpine-Core (hybrid SDK)"
& $VenvPython -m pip install $CoreGit
Require-Ok "pip install Core"

if (Test-Path "requirements.txt") {
    Info "Installing requirements.txt"
    & $VenvPython -m pip install -r requirements.txt
    Require-Ok "pip install requirements"
}
if (Test-Path "requirements-dev.txt") {
    Info "Installing requirements-dev.txt"
    & $VenvPython -m pip install -r requirements-dev.txt
    if ($LASTEXITCODE -ne 0) { Warn "Some dev deps failed; continuing." }
}
if ((Test-Path ".env.example") -and -not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Info "Copied .env.example → .env"
}

Write-Host ""
Info "Done. Activate:  $VenvDir\Scripts\Activate.ps1"
Info "Pull a model:    ollama pull gemma4:e4b"
Info "Validate:        python demo.py"
