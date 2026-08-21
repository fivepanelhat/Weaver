# Weaver — dual-platform installer (Windows / PowerShell)
$ErrorActionPreference = "Stop"

$RepoUrl    = if ($env:WEAVER_REPO_URL) { $env:WEAVER_REPO_URL } else { "https://github.com/fivepanelhat/Weaver.git" }
$InstallDir = if ($env:WEAVER_HOME)     { $env:WEAVER_HOME }     else { Join-Path $env:USERPROFILE ".weaver-app" }
$VenvDir    = Join-Path $InstallDir "venv"
$CoreGit    = if ($env:CORE_GIT_URL)    { $env:CORE_GIT_URL }    else { "git+https://github.com/fivepanelhat/Coastal-Alpine-Core.git@v0.5.10" }

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
if (-not $PythonBin) { Fail "Python 3.10+ is required." }
$PyVer = & $PythonBin -c "import sys; print('%d.%d' % sys.version_info[:2])"
& $PythonBin -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)"
if ($LASTEXITCODE -ne 0) { Fail "Python 3.10+ is required (found $PyVer)" }
Info "Using Python $PyVer ($PythonBin)"

if ((Test-Path "bootstrap.py") -and ((Test-Path "requirements.txt") -or (Test-Path "pyproject.toml"))) {
    $SrcDir = (Get-Location).Path
} else {
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) { Fail "git is required." }
    New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
    $SrcDir = Join-Path $InstallDir "src"
    if (Test-Path (Join-Path $SrcDir ".git")) {
        git -C $SrcDir pull --ff-only 2>$null
    } else {
        git clone --depth 1 $RepoUrl $SrcDir
        Require-Ok "git clone"
    }
}

Set-Location $SrcDir
if (Test-Path "bootstrap.py") {
    & $PythonBin bootstrap.py
    Require-Ok "bootstrap"
    exit 0
}

& $PythonBin -m venv $VenvDir
Require-Ok "venv create"
$VenvPython = Join-Path $VenvDir "Scripts\python.exe"
& $VenvPython -m pip install --upgrade pip
& $VenvPython -m pip install $CoreGit
Require-Ok "pip install Core"
if (Test-Path "requirements.txt") { & $VenvPython -m pip install -r requirements.txt }
if (Test-Path "requirements-dev.txt") { & $VenvPython -m pip install -r requirements-dev.txt }
if ((Test-Path ".env.example") -and -not (Test-Path ".env")) { Copy-Item ".env.example" ".env" }
Info "Done. Activate: $VenvDir\Scripts\Activate.ps1"
