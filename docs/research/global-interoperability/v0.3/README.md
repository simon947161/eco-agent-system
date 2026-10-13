# GGG Global Interoperability v0.3

This is a bounded, dependency-free localhost adapter prototype for the v0.2 canonical cross-OS transport contract.

It exposes the same validator through:

- OpenAPI-style HTTP: `POST /v0.3/handoffs`
- MCP JSON-RPC: `POST /mcp` with `tools/list` and `tools/call`

The server binds only to `127.0.0.1`. It accepts synthetic fixtures only, performs no external action, performs no domain-system or mainline write, and contains no private person or biometric asset.

## Windows location

Recommended local path:

`D:\Codex\ClimateOS\eco-agent-system\docs\research\global-interoperability\v0.3\`

Start in PowerShell:

```powershell
cd D:\Codex\ClimateOS\eco-agent-system\docs\research\global-interoperability\v0.3
.\windows\Start-GGGLoopbackAdapter.ps1
```

In a second PowerShell window:

```powershell
.\windows\Test-GGGLoopbackAdapter.ps1
```

## Dependency-free validation

```powershell
python .\tests\test_loopback_adapter.py
```

Expected result: `11/11 PASS`.

## Non-production boundary

This prototype has no authentication, signature verification, durable queue, TLS, production registry, or reliable retry store. Those omissions are intentional under the Founder-approved v0.3 boundary.
