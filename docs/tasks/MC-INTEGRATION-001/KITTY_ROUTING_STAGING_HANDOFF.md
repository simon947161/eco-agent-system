# KITTY production-route staging handoff

- Task: GitHub Issue #126, comment `6262793437`
- Founder decision: Option A — staging preparation only
- Status: `STAGING_PATCH_GO`; `LIVE_E2E_NO_GO` pending separate authorization
- Isolated branch: `codex/mc-integration-001`

## Outcome

The isolated candidate fixes the pre-DSH routing failure without changing the production KITTY tree. A shorthand such as `GitHub Issue #126` can resolve only through an explicit repository binding supplied as request field `githubRepository` or configuration `KITTY_GITHUB_REPO_BINDING`. The selected `owner/repo` must pass the existing `github-issues.mjs` allowlist. Missing, malformed, or off-list bindings fail explicitly and never fall back to public search.

The route produces only three evidence outcomes: `ACCESS_CONFIRMED`, `ACCESS_BLOCKED`, or `TOOL_UNAVAILABLE`. Public search remains available for ordinary current-information questions, including general GitHub product news, but never serves as an access probe or substitute for canonical repository bytes. Audit telemetry records only the decision, reason, binding source, target counts, and bounded read statuses; it excludes prompts, content, paths, and credentials.

## Intended production diff

The reviewable patch is `docs/tasks/MC-INTEGRATION-001/KITTY_ROUTING_STAGING.patch`. It is limited to:

1. Add `docs/taskboard/server/github-evidence-routing.mjs`.
2. Modify `docs/taskboard/server/taskboard-server.mjs` to resolve and validate the explicit binding, pass it to the existing shorthand parsers, gate public research, append an explicit failure result to the model prompt, and write safe route telemetry.

No change is proposed for `github-issues.mjs`; its existing `extractIssueRefs(text, fallbackRepo)`, `extractEvidenceRefs(text, fallbackRepo)`, and allowlist are reused. No change is proposed for the launcher, DSH, credentials, ports, or Council systems.

## Verification

| Check | Result |
| --- | --- |
| Focused route tests | PASS — 13/13 |
| Full MC-INTEGRATION regression | PASS — 34/34 |
| Candidate/test syntax | PASS |
| Patch `git apply --check` against a read-only copy of the canonical server | PASS |
| Patched temporary server/helper syntax | PASS |
| Canonical production dirty set after preparation | PASS — exact match to the 2,381-entry captured set |
| Production source modification/restart | NOT PERFORMED |
| Live KITTY end-to-end | NOT PERFORMED; requires next-stage authorization |

Commands used in the isolated worktree:

```powershell
node --test tests/test_kitty_evidence_routing.mjs
node --test tests/test_mc_integration_runner.mjs tests/test_production_adapter.mjs tests/test_kitty_evidence_routing.mjs
git apply --check --unsafe-paths --directory=.tmp-kitty-staging docs/tasks/MC-INTEGRATION-001/KITTY_ROUTING_STAGING.patch
node --check .tmp-kitty-staging/docs/taskboard/server/taskboard-server.mjs
node --check .tmp-kitty-staging/docs/taskboard/server/github-evidence-routing.mjs
```

## Canonical production preservation evidence

- Repository: `D:\Codex\ClimbOS-Mission-Control`
- Branch/HEAD: `deepseek/gpt-taskboard-integration` / `23fd40122a8166946688f81194eba9735d613eba`
- Exact status snapshot: `C:\Users\doras\OneDrive\Documents\Claimos-mission-control\worktrees\eco-agent-system-mc-integration-001\docs\tasks\MC-INTEGRATION-001\CANONICAL_DIRTY_TREE_SNAPSHOT.txt`
- Snapshot SHA-256: `7A2940A40E3B1BAF8048C6AB256D7272A875D9FD5658394B2FEEB09AB19CFD51`
- `taskboard-server.mjs`: `F364FA91B62870CD0817FF249A78C3E3DBBF9CA836046631E76AF04E11AA1E20`
- `github-issues.mjs`: `BFDF97170DA855110209D8A327B05458DC9BCE10903AE09330F20AB368691959`
- `katie-brain.mjs`: `ED73990A7A770D2510522D16DAC85B36B5CBAE806943F7867A4B1DB6DDBF13D0`
- `start-mission-control.ps1`: `6818B0F9EA6E7565A2F1B2A02CBEB01880FDEC348DCFA3059AA726F767EBCB30`
- Observation at final read-only inspection: ports 3543, 3597, and 3080 had listeners. They were not started, stopped, or restarted by this work.

## Next-stage startup gate

Only after separate Founder authorization:

1. Review the immutable commit and apply the patch to a clean staging mirror based on the approved production commit.
2. Set an explicit allowlisted repository binding for the controlled test; do not introduce a guessed default.
3. Re-run syntax and regression tests, then verify only one controlled KITTY instance owns the expected endpoint.
4. Exercise shorthand-with-binding, no-binding, denied-access, pinned-file, fresh-session, and ordinary-news cases.
5. Confirm the `github:route` audit entry contains no prompt, content, path, or credential.

Production rollout remains `NO_GO` until the live test is separately authorized and these checks pass.

## Rollback preparation

Before any authorized live change, record fresh hashes and make exact recoverable copies of the two intended target files. If rollback is required, stop only the controlled test instance, restore `taskboard-server.mjs`, remove the newly added `github-evidence-routing.mjs`, clear only `KITTY_GITHUB_REPO_BINDING`, and restart through the canonical launcher. Verify health and source hashes afterward. Do not use `git reset --hard`, `git clean`, or broad replacement against the existing dirty production tree.

## Remaining validation boundary

- VERIFIED: parsing, binding precedence and allowlist enforcement, no-search failure behavior, route telemetry shape, regressions, patch applicability, syntax, and production-tree preservation.
- UNVERIFIED: live KITTY request/response behavior, live audit persistence, controlled restart, and rollback execution.
- DECISION: stop after publishing this immutable staging evidence; wait for the next-stage authorization.
