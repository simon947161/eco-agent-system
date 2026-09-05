param([int]$Port = 8787)
$ErrorActionPreference = "Stop"
$BaseUri = "http://127.0.0.1:$Port"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Fixture = Get-Content (Join-Path $ProjectRoot "fixtures\synthetic_climateos_to_buildingos.json") -Raw
$Health = Invoke-RestMethod -Uri "$BaseUri/health" -Method Get
$Receipt = Invoke-RestMethod -Uri "$BaseUri/v0.3/handoffs" -Method Post -ContentType "application/json" -Body $Fixture
if ($Health.network_scope -ne "LOOPBACK_ONLY" -or $Receipt.status -ne "ACCEPTED") {
  throw "Loopback validation failed"
}
[pscustomobject]@{ Health = $Health.status; Network = $Health.network_scope; Handoff = $Receipt.status; Hash = $Receipt.envelope_sha256 }
