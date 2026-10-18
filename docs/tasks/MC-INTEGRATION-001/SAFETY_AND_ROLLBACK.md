# MC-INTEGRATION-001 safety and rollback

## Safety controls

The isolated candidate is default-off, Issue-126-only, creates no listener, reads no credential values, and exposes no Council or public-system path. Runtime state must live outside Git. Logs and receipts contain IDs, status, hashes and redacted failures, not prompts or environment dumps.

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
2. Stop accepting new Codex jobs; allow any active child process to terminate at its bounded timeout.
3. Preserve the state directory and Issue comments as audit evidence.
4. Revert only the reviewed adapter import/route/config patch in a clean worktree or deploy the prior reviewed artifact.
5. Restart only after Founder approval and confirm `/api/status`, `/api/kitty/diagnostics`, and the existing DeepSeek path.
6. Compare the restored source hashes/commit with the pre-deployment manifest. Do not use `reset --hard`, `clean`, or broad file replacement on the current dirty production tree.

## Exact executor actions after approval

The deployer must work from a clean worktree created at the approved production commit, review the patch, run the two focused Node test files, and use the existing service supervisor/launcher to perform a controlled restart. The current process was started directly as:

`node D:\Codex\ClimbOS-Mission-Control\docs\taskboard\server\taskboard-server.mjs`

No verified supervisor or automatic rollback command was discovered in this audit. Therefore a production command sequence is intentionally not asserted until the service owner identifies the canonical launcher. This is a deployment blocker, not permission to kill PID `18172` manually.

## Rollback acceptance

- adapter reports `ADAPTER_DISABLED`;
- no Codex child process starts;
- existing KITTY and DeepSeek diagnostics remain healthy;
- prior receipts remain readable;
- Issue #126 receives the rollback outcome or explicit writeback failure;
- no unrelated dirty-tree entry changes.
