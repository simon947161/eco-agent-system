param(
  [int]$Port = 8787,
  [string]$Python = "python"
)
$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
& $Python (Join-Path $ProjectRoot "adapter\loopback_adapter.py") --port $Port
