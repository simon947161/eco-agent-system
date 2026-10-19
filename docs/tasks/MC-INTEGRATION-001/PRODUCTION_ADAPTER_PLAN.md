# MC-INTEGRATION-001 production adapter plan

Date: 2026-10-19 (Australia/Sydney)
Review status: `REVIEW_PENDING` after bounded F-1–F-6 remediation

Deployment status: `PRODUCTION_NO-GO`; no production wiring

## Observed production state

- Canonical KITTY source: `D:\Codex\ClimbOS-Mission-Control` (`simon947161/Simon.git`).
- Branch/HEAD: `deepseek/gpt-taskboard-integration` / `23fd40122a8166946688f81194eba9735d613eba`.
- Runtime: `node.exe ...\docs\taskboard\server\taskboard-server.mjs`, PID `18172`, listener `127.0.0.1:3543`.
- Health at inspection: `/api/status` returned `ok:true`; `/api/kitty/diagnostics` returned `identity:KITTY`, `health:ONLINE`, `activeRunCount:0`.
- Existing execution path: single-flight DeepSeek manager with bounded attempts. Existing GitHub routes are allowlisted **GET-only** readers. No Codex execution route exists.
- Safety gate: the production worktree is dirty and live runtime records may change. Preserve and compare sorted `git status --porcelain=v1` entry sets before and after any staging action; investigate every unexpected delta instead of relying on a fixed count. It was not edited, cleaned, reset, committed, or restarted by this remediation.

## Candidate boundary

The candidate is an additive module in the isolated `eco-agent-system` branch:

- `tools/mc_integration/production-adapter.mjs`
- `tests/test_production_adapter.mjs`

It does not open a port. A later reviewed KITTY integration would call the module in-process from an explicit `POST` route or manager task type and inject:

1. a Codex CLI executor;
2. an Issue #126 comment writer;
3. a dedicated state directory outside source control.

## Least-privilege contract

- disabled by default (`enabled:false`);
- fixed repository `simon947161/eco-agent-system` and Issue `126`;
- explicit model allowlist;
- localhost-only transport remains the responsibility of the existing server (`127.0.0.1`); the module creates no listener;
- one durable job ID is the idempotency key; a separate immutable claim file removes the empty-receipt race, and concurrent duplicates wait only for a readable receipt and never execute again;
- one attempt by default, 180-second timeout, 1-second termination-confirmation grace, 32 KiB prompt, 64 KiB result and 4 KiB failure-text caps;
- the executor receives an `AbortSignal`; cancellation and timeout must confirm attempt termination before any retry, otherwise the job fails closed with retries suppressed;
- stale `RUNNING` receipts become explicit `RECOVERY_REQUIRED` failures on restart; corrupt receipts are preserved individually and do not block recovery of other jobs;
- model allowlists are copied and frozen, including exported defaults and returned effective configuration;
- credential-shaped strings are recursively removed from successful results before persistence/writeback and redacted from byte-bounded failures;
- a successful execution is not terminally successful until GitHub writeback succeeds.

## Proposed production changes (not applied)

The smallest reviewed integration would modify only:

1. `docs/taskboard/server/taskboard-server.mjs`: import a vendored adapter, construct it once, call `recover()` on startup, expose a localhost-only authenticated task route, and audit request/result IDs without prompts or secrets.
2. `docs/taskboard/server/codex-adapter.mjs`: reviewed copy of the isolated module plus concrete Codex/GitHub dependency functions.
3. one configuration record: `KITTY_CODEX_ADAPTER_ENABLED=0` by default, state path, model allowlist, timeout and resource limits.
4. focused tests for the route and dependency wiring.

No change is proposed to `deepseek-executor.mjs` or the existing GitHub GET routes.

## Required staging sequence

1. Snapshot the four production source hashes listed in `SAFETY_AND_ROLLBACK.md` and the sorted porcelain entry set; after staging, compare sets and investigate every unexpected delta.
2. Create a clean worktree from the exact reviewed production HEAD.
3. Apply only the reviewed adapter/route patch in that clean worktree.
4. Run unit/failure tests with the adapter disabled, then enabled against mock dependencies.
5. Run one live Codex no-tool read-only task and one Issue #126 writeback in staging.
6. Verify concurrent duplicate, cooperative cancel, termination-confirmed retry, fail-closed unconfirmed termination, restart/corrupt recovery, timeout, invalid/oversize result, redaction and denied writeback.
7. Obtain Founder approval for any production deployment/restart.

## Evidence status

- VERIFIED: production health/listener/process and dirty-tree boundary.
- VERIFIED: prior live Codex no-tool E2E and GitHub comment, job `MC126-1792354654093-3dd81a`.
- VERIFIED: isolated candidate F-1–F-6 behavior and validation gaps through focused injected-dependency regression tests.
- UNVERIFIED: real KITTY route to the candidate, Codex tool execution on Windows read-only sandbox, production restart/recovery, and production rollback.
