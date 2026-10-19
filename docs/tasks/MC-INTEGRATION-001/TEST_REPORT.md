# MC-INTEGRATION-001 test report

Date: 2026-10-19 (Australia/Sydney)

Review status: `REVIEW_PENDING`

Deployment status: `PRODUCTION_NO-GO`

## F-1–F-6 remediation

| Finding | Result | Regression evidence |
|---|---|---|
| F-1 corrupt recovery | FIXED / PASS | A corrupt receipt is renamed and preserved, a failed placeholder is written, and a separate stale `RUNNING` job still recovers. |
| F-2 empty receipt race | FIXED / PASS | Claim and receipt use separate files; 12 concurrent duplicates return one readable receipt while the executor starts once. |
| F-3 cooperative cancellation | FIXED / PASS | Executor receives `AbortSignal`; timeout retry reaches maximum concurrency 1; unconfirmed termination suppresses retry; post-start cancel returns `CANCELLED`. |
| F-4 mutable allowlist | FIXED / PASS | Exported defaults, copied effective array and returned config reject mutation; caller-array mutation cannot widen policy. |
| F-5 unbounded failure | FIXED / PASS | UTF-8 failure text is redacted and remains at or below configured byte limit, including multibyte input. |
| F-6 success-result leakage | FIXED / PASS | Nested secret-named keys and token-shaped strings are sanitized before both persistence and Issue-writer invocation. |

## Required coverage

PASS: repository and Issue policy denial, invalid job ID, empty and oversized prompt, unsupported model, unavailable CLI, missing result, non-PASS result, oversized result, writeback permission failure, sequential/concurrent duplicate job, pre-start and post-start cancellation, confirmed timeout retry, unconfirmed termination fail-closed, corrupt recovery, rollback switch, redaction and byte bounding.

The existing runner suite remains included and passed. The pinned review packet must include both:

- `tests/test_mc_integration_runner.mjs`
- `tests/test_production_adapter.mjs`

## Commands and results

- `node --check tools/mc_integration/production-adapter.mjs` — PASS
- `node --test tests/test_mc_integration_runner.mjs tests/test_production_adapter.mjs` — PASS, 21/21
- `git diff --check` — PASS

The first regression run was 19/20 because the policy-denial test matched message text even though the implementation correctly exposed `error.code = POLICY_DENIED`. The assertion was corrected to inspect the structured code; no production behavior was weakened.

## Evidence boundary

- Tests use injected executor and Issue-writer functions to verify adapter state, concurrency, cancellation and safety behavior. They do not claim live KITTY route integration.
- Prior live no-tool Codex/writeback evidence remains job `MC126-1792354654093-3dd81a`, Issue comment `6254653915`.
- Actual Codex tool/shell execution in the Windows read-only sandbox remains unverified after the prior `CreateProcessWithLogonW failed: 2` result.
- `start-mission-control.ps1` is verified as the canonical Founder entry point; no automated rollback command is verified.
- The formal service was not deployed, restarted or modified by this remediation.
