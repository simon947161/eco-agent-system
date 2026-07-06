# Task132 Git Permission and Transport Risk Diagnosis

## Purpose

Task132 diagnoses prior `.git` permission failures and Windows Git / Schannel risks using the evidence available after Task131.

This document is diagnosis-only. It records findings and safe fix options, but does not apply fixes, change Git configuration, change Windows permissions or ownership, resume QCloud, or implement Task133-140.

## Governing Scope

The frozen Task131-140 Formal Execution Brief defines Task132 as:

```text
Diagnose prior `.git` permission failures and Windows Git / Schannel risks
```

Task132 is part of the repository-stability and operating-mode recovery sprint. It is not runtime, API, MCP, website, calculator, database, compliance, assurance, scoring, automation, QCloud, or CarbonOS implementation work.

## Evidence Reviewed

| Evidence | Observed Result |
| --- | --- |
| Current branch | `task46-repository-control-codex-batch-queue` |
| Local HEAD at Task132 start | `055d4dd9433691a08583e3f32ac76c921a26198a` |
| Remote official branch at Task132 start | `055d4dd9433691a08583e3f32ac76c921a26198a` |
| Working tree | Clean |
| `.git/*.lock` files | None found |
| `.git/index.lock` | Not present |
| `.git/FETCH_HEAD` | Present |
| Normal `git status --short` | Clean |
| `git ls-remote origin HEAD` | Succeeded |
| Current Windows user | `dell-dora\codexsandboxoffline` |
| Repository folder owner | `DELL-Dora\CodexSandboxOffline` |
| `.git` folder owner | `DELL-Dora\CodexSandboxOffline` |

## Git Configuration Evidence

Relevant Git configuration observed during Task132:

```text
file:D:/AI_Tools/Git/etc/gitconfig  http.sslbackend schannel
file:D:/AI_Tools/Git/etc/gitconfig  credential.helper manager
file:.git/config                    http.sslbackend openssl
file:.git/config                    http.version HTTP/1.1
file:.git/config                    user.name simon947161
file:.git/config                    user.email 151257334+simon947161@users.noreply.github.com
command line:                       safe.directory D:\Codex\ClimateOS\eco-agent-system-codex-working
```

Global user `safe.directory` entries were present for other workspaces, but not as a persistent user-level entry for this exact repository path.

## Diagnosis Summary

| Issue | Current Classification | Diagnosis |
| --- | --- | --- |
| Prior `.git` permission / lock failures | Historical resolved issue, with residual risk | No active lock file was found, normal status is clean, and Task131 commit/push already completed. The exact prior failures are not currently reproducing in the normal Codex shell. |
| Dubious-ownership guard | Manageable operational risk | The guard appears in escalated Git operations where Git sees a different Windows user than the repository owner. One-command repo-specific `safe.directory` override has worked without changing global config. |
| Schannel / remote transport risk | Manageable operational risk | System Git defaults to Schannel, but this repo overrides `http.sslbackend` to `openssl` and `http.version` to `HTTP/1.1`. Read-only remote query succeeded. |
| GitHub credential / transport availability | Manageable operational risk | `git ls-remote origin HEAD` succeeded. Future write operations may still depend on credential availability and escalation context. |
| Persistent safe.directory policy | Needs human confirmation before change | A persistent exact-path safe.directory entry could reduce repeated escalated-operation friction, but it is a policy choice and was not applied. |

## Interpretation

The repository is usable in the normal Codex shell. The prior `.git` permission failures do not appear to be an active blocker at the time of Task132.

The main remaining risk is operational-context mismatch: normal Codex commands run as `dell-dora\codexsandboxoffline`, while prior escalated Git failures reported a different user. That mismatch can trigger Git's dubious-ownership guard even when the repository and `.git` directory are otherwise healthy.

The Schannel risk appears mitigated for this repository by repo-local OpenSSL and HTTP/1.1 settings. Because read-only remote access succeeded, there is no current evidence that Schannel is blocking this repository in normal operation.

## Safe Fix Options Not Applied

| Option | What It Would Do | Risk / Note |
| --- | --- | --- |
| Keep using one-command repo-specific override only when needed | Continue `git -c safe.directory=D:/Codex/ClimateOS/eco-agent-system-codex-working ...` for escalated Git operations. | Lowest persistence risk; slightly repetitive. |
| Add persistent safe.directory for exact repo path only | Add this exact repo path to user Git config. | Reduces repeated guard prompts, but changes global user Git config and needs explicit human approval. |
| Keep repo-local OpenSSL / HTTP/1.1 settings | Preserve existing repo-local transport configuration. | Already in place; no action required. |
| Create a fresh clone owned by the interactive push user | Avoid ownership mismatch by aligning repo owner and escalated Git user. | More disruptive; requires careful migration and explicit approval. |
| Change folder ownership or ACLs | Align ownership in-place. | Not recommended without explicit approval; permission changes can destabilize Codex access. |

The whole D drive must not be added as a safe directory.

## What Was Not Done

- No Git global config was changed.
- No system Git config was changed.
- No repository ownership or permissions were changed.
- No permission-modifying commands were run.
- No runtime, API, MCP, website, calculator, database, compliance, assurance, scoring, or automation work was created.
- No QCloud work was resumed or dispatched.
- No closure records were created.
- Task133-140 were not implemented.

## Task132 Result

```text
Task132 Result: DIAGNOSIS COMPLETE
.git permission / lock failures: HISTORICAL RESOLVED ISSUE WITH RESIDUAL RISK
Dubious-ownership guard: MANAGEABLE OPERATIONAL RISK
Schannel / transport risk: MANAGEABLE OPERATIONAL RISK
QCloud Builder Work: SUSPENDED
Task133-140: NOT STARTED
Fixes Applied: NONE
```
