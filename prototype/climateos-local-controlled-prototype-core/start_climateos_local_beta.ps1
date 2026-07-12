$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

Write-Host "ClimateOS Limited Local Beta" -ForegroundColor Green
Write-Host "Localhost only; synthetic review; no external data or automatic conclusions."

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "Creating the local Python environment..."
    python -m venv .venv
}

& ".venv\Scripts\python.exe" -m pip install -r requirements.txt
& ".venv\Scripts\python.exe" scripts\init_db.py --seed

Write-Host "Open http://127.0.0.1:8765 after the service starts."
Write-Host "Press Ctrl+C in this window to stop ClimateOS."
& ".venv\Scripts\python.exe" scripts\run_local_service.py --host 127.0.0.1 --port 8765
