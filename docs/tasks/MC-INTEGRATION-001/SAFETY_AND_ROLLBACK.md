# MC-INTEGRATION-001 safety and rollback

## Safety controls

The isolated candidate is default-off, Issue-126-only, creates no listener, reads no credential values, and exposes no Council or public-system path. Runtime state must live outside Git. Logs and receipts contain IDs, status, hashes, sanitized results and byte-bounded redacted failures, not prompts or environment dumps.

Current production source fingerprints (read-only capture, 2026-10-19):

| File | SHA-256 |
|---|---|
| `docs/taskboard/server/taskboard-server.mjs` | `F364FA91B62870CD0817FF249A78C3E3DBBF9CA836046631E76AF04E11AA1E20` |
| `docs/taskboard/server/deepseek-executor.mjs` | `EDA61F718066B98AA4844DF98E722E9E4A4FDCDC669057AF8B9CEDFB1D75E811` |
| `docs/taskboard/server/github-issues.mjs` | `BFDF97170DA855110209D8A327B05458DC9BCE10903AE09330F20AB368691959` |
| `docs/taskboard/server/katie-brain.mjs` | `ED73990A7A770D2510522D16DAC85B36B5CBAE806943F7867A4B1DB6DDBF13D0` |

These hashes are evidence, not a claim that the dirty tree is safe to overwrite.

## Rollback design

Rollback is fail-closed and does not require deleting receipts:

1. Set `KITTY_CODEX_ADAPTER_ENABLED=0` in the reviewed service configuration.
2. Stop accepting new Codex jobs; abort active jobs cooperatively and require confirmed executor termination. If termination is not confirmed within the grace period, fail closed and do not retry.
3. Preserve the state directory and Issue comments as audit evidence.
4. Revert only the reviewed adapter import/route/config patch in a clean worktree or deploy the prior reviewed artifact.
5. Restart only after Founder approval and confirm `/api/status`, `/api/kitty/diagnostics`, and the existing DeepSeek path.
6. Compare the restored source hashes/commit with the pre-deployment manifest. Do not use `reset --hard`, `clean`, or broad file replacement on the current dirty production tree.

## Exact executor actions after approval

The deployer must work from a clean worktree created at the approved production commit, review the patch, run the two focused Node test files, and use the existing canonical launcher for a controlled restart only after separate approval:

`D:\Codex\ClimbOS-Mission-Control\start-mission-control.ps1`

That script is the single Founder entry point, holds mutex `Local\KITTYCanonicalStartup3543`, reuses a healthy bridge, launches the exact Node server when required, retries startup once, and checks health. No automated rollback command was identified. The absence of automated rollback remains a deployment blocker and is not permission to kill the live PID manually.

## Rollback acceptance

- adapter reports `ADAPTER_DISABLED`;
- no Codex child process starts;
- existing KITTY and DeepSeek diagnostics remain healthy;
- prior receipts remain readable;
- Issue #126 receives the rollback outcome or explicit writeback failure;
- sorted pre/post `git status --porcelain=v1` entry sets have no unexplained delta; no fixed dirty-entry count is an acceptance criterion.
