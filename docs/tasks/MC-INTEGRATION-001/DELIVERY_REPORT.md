# MC-INTEGRATION-001 delivery report

Date: 2026-10-19 (Australia/Sydney)

Issue: [simon947161/eco-agent-system#126](https://github.com/simon947161/eco-agent-system/issues/126)

Branch: `codex/mc-integration-001`

Baseline: `9eb7577e145e76161f9f1cd8509348b19c2904cc` (`origin/main`)

Status: `MINIMUM_E2E_VERIFIED / LOCAL_BRANCH_ONLY / NOT_DEPLOYED`

## Outcome

A bounded adapter now implements the smallest reusable path:

```text
GitHub Issue #126
  -> KITTY invocation identity and host-side read-only precheck
  -> ephemeral Codex CLI structured verification
  -> durable local receipt
  -> automatic GitHub Issue comment
```

The successful run did not require Simon to copy a prompt or result between
systems. It did not use a new framework, a public listener, a new credential,
or a Council system. It did not push, merge, deploy, or alter application data.

## Existing capabilities audited

| Capability | Observed state | Decision |
|---|---|---|
| Canonical KITTY / Mission Control | `127.0.0.1:3543`, runtime healthy, canonical repository at `D:\Codex\ClimbOS-Mission-Control` | Reuse identity, governance, job/receipt conventions; do not modify its dirty production worktree. |
| Mission Control task manager | Durable task evidence and DeepSeek manager loop exist | No second queue or scheduler added. |
| DeepSeek Harness | Existing local harness online through Mission Control | Audited but not needed for the minimal Codex probe; no paid DeepSeek task launched. |
| Codex CLI | `0.142.5`, authenticated | Reused with ephemeral structured output and no tool invocation. |
| GitHub connection | Existing `gh` credential can read Issue #126 and post comments | Reused; no token value read or persisted. |
| Existing GitHub module | Read-only issue/file evidence reader | Preserved; the new adapter contains a separate, Issue-126-only writeback seam. |

## Successful end-to-end evidence

- Job ID: `MC126-1792354654093-3dd81a`
- Actor: `KITTY`
- Executor: `Codex CLI 0.142.5`
- Model: `codex-auto-review` (the installed CLI model directory's advertised API-capable model)
- Input mode: `KITTY_HOST_READ_ONLY_PRECHECK`
- Result: `SUCCESS / PASS`
- Baseline and observed HEAD: `9eb7577e145e76161f9f1cd8509348b19c2904cc`
- README SHA-256: `4907723cd15250e2bf783d6a9acef9c521a08e45894277ec7b601937b615a3ce`
- Prompt SHA-256: `2a6d7f2744270a7e086351c46668698aeabef4044ae66aba1d8c96fe53834c14`
- Result SHA-256: `6524eef68b393185fb0f8df90d6beba8e255c09901507e4624d9bcb7391ccf61`
- Automatic writeback: [Issue comment 6254653915](https://github.com/simon947161/eco-agent-system/issues/126#issuecomment-6254653915)
- Local receipt: `C:\Users\doras\OneDrive\Documents\Claimos-mission-control\handoffs\MC-INTEGRATION-001\evidence\MC126-1792354654093-3dd81a\receipt.json`

The adapter reads the repository HEAD and `README.md` on KITTY's authorized
host side, hashes the file, and sends only those bounded facts to Codex. Codex
is told not to invoke tools or a shell and returns a schema-validated result.
This preserves the safety objective after the Windows read-only Codex sandbox
proved unable to start a child shell.

## Failure evidence retained and written back

The failed attempts were not hidden:

| Job | Failure | GitHub evidence |
|---|---|---|
| `MC126-1792354549578-a07953` | Initial result file absent after unsupported default model; early error reporting was too generic. | [comment 6254634925](https://github.com/simon947161/eco-agent-system/issues/126#issuecomment-6254634925) |
| `MC126-1792354572502-b1c213` | `gpt-6-sol` rejected by the CLI ChatGPT account channel; adapter then preserved `MODEL_UNSUPPORTED`. | [comment 6254639792](https://github.com/simon947161/eco-agent-system/issues/126#issuecomment-6254639792) |
| `MC126-1792354606265-939b8e` | API-capable model ran, but Windows read-only shell launch failed with `CreateProcessWithLogonW failed: 2`; Codex returned structured FAIL. | [comment 6254647095](https://github.com/simon947161/eco-agent-system/issues/126#issuecomment-6254647095) |

The first comment is a historical receipt produced before failure
classification was improved; later receipts preserve the precise model and
sandbox causes.

## Validation

- `node --check tools/mc_integration/mc-integration-runner.mjs`: PASS
- `node --test tests/test_mc_integration_runner.mjs`: PASS (`4/4`)
- allowlist rejects other repositories and issue numbers: PASS
- prompt fixes no-push/no-merge/no-deploy/no-secret/no-Council boundaries: PASS
- successful Codex structured output matches repository, HEAD and file: PASS
- automatic GitHub success writeback read back through the GitHub connection: PASS
- failure comments read back through the GitHub connection: PASS
- `git diff --check`: PASS
- production Mission Control worktree modified by this task: NO
- remote branch, push, PR, merge or deployment: NONE

## Boundaries and remaining work

- The adapter is committed only on a local feature branch. The canonical
  `127.0.0.1:3543` service was not modified or restarted because its production
  worktree contains unrelated user/runtime changes.
- This proves the requested minimum invocation and writeback path; it does not
  claim unattended production scheduling.
- Installing the adapter into the canonical KITTY manager, pushing the branch,
  opening a PR, merging, or deploying remains a separate review/authorization
  step.
- DeepSeek remains available for tasks that need its existing manager path, but
  inserting it into this small verification would add cost and another failure
  surface without improving the acceptance result.

## Conversation Radar

- Knowledge points: canonical KITTY and DeepSeek are healthy; Codex CLI model
  availability differs from desktop model labels; Windows read-only child-shell
  creation is unavailable on this host.
- Idea point: keep deterministic host evidence collection separate from model
  interpretation when a stronger sandbox cannot execute.
- Decision: one Issue-specific adapter, no new platform.
- Risks: production wiring is not yet installed; CLI model availability may drift.
- Open question: whether canonical Mission Control should expose this adapter as
  a reviewed task type after the local branch is reviewed.
- Next action: review the local commit, then separately authorize push/PR and
  production wiring if desired.
- Keywords: `ClimateOS`, `Mission Control`, `KITTY`, `Codex CLI`, `DeepSeek Harness`,
  `GitHub Issue`, `receipt`, `human-in-the-loop`.
