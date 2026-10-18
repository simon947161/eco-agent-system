# MC-INTEGRATION-001 test report

Date: 2026-10-19 (Australia/Sydney)

## Results

| Test | Result | Evidence boundary |
|---|---|---|
| KITTY -> Codex -> receipt -> GitHub | PASS | Prior live no-tool job `MC126-1792354654093-3dd81a`; Issue comment `6254653915`. This is real CLI/writeback evidence, not a mock, but it uses host-prechecked evidence. |
| Success receipt/writeback state | PASS | Injected isolation test. |
| Unsupported model | PASS | Rejected before executor invocation. |
| Codex CLI unavailable | PASS | Explicit `CODEX_UNAVAILABLE` receipt. |
| Missing/invalid result | PASS | Explicit `INVALID_RESULT` receipt. |
| GitHub permission/write failure | PASS | Explicit failed writeback with redaction. |
| Duplicate job | PASS | Same receipt returned; executor invoked once. |
| Cancellation | PASS | Pre-start marker prevents execution. |
| Restart/recovery | PASS | Stale `RUNNING` receipt becomes `RECOVERY_REQUIRED`. |
| Rollback switch | PASS | Default configuration rejects work as `ADAPTER_DISABLED`. |
| Credential redaction | PASS | Credential-shaped values removed from failure text. |
| Production service unchanged | PASS | PID `18172`, HEAD `23fd401...`, and source hashes captured read-only; no restart or file write. |

Commands:

- `node --check tools/mc_integration/production-adapter.mjs` — PASS
- `node --test tests/test_mc_integration_runner.mjs tests/test_production_adapter.mjs` — PASS, 14/14 on normal Windows host filesystem semantics
- `git diff --check` — PASS

## Important environment finding

The same Node tests initially failed inside Codex's virtualized sandbox temporary directory because Windows `rename` returned `EPERM`. The unchanged suite passed outside that filesystem virtualization. This is evidence that the adapter's atomic replacement must be rechecked in the exact future service state directory; it is not evidence of production readiness.

## Validation boundaries

- The new adapter tests use injected executor and Issue-writer functions. They validate state transitions and safety controls, not live KITTY wiring.
- The prior live job proves real Codex CLI invocation and GitHub writeback, but Codex was instructed not to invoke tools; KITTY's host collected the repository evidence.
- A prior attempt at actual Codex shell use in Windows read-only sandbox failed with `CreateProcessWithLogonW failed: 2`.
- The DeepSeek diagnostics endpoint was read and healthy; no paid DeepSeek job was launched.
- Timeout logic is bounded in code but a production child-process termination strategy remains unverified.
