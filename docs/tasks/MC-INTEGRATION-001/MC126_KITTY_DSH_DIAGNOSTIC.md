# MC126 KITTY / DeepSeek Harness 双轨诊断

- Task: GitHub Issue #126, comment `6262630193`
- Date: 2026-10-19 (Australia/Sydney)
- Scope: read-only production diagnosis; isolated reference fix and tests only
- Production status: `PRODUCTION_NO-GO`

## Executive result

**VERIFIED root cause:** KITTY's repeated public-search failure was caused by Mission Control's pre-DSH router, not by an absent GitHub reader and not by a DeepSeek model defect. The shorthand request `GitHub Issue #126` did not include a repository name or full issue URL, so `extractIssueRefs()` returned no issue target. The request also named a commit but no repository file paths, so `extractEvidenceRefs()` returned no file target. Because the message contained `最新`, `needsResearch()` returned true; with an empty `githubReads` array, `taskboard-server.mjs` enabled DSH `web_search`. Six irrelevant public searches then produced zero hits, and the answer incorrectly treated that as repository inaccessibility.

**Isolated fix completed:** this branch now contains a deterministic evidence-routing guard. GitHub evidence intent suppresses public-search fallback and yields exactly one of `ACCESS_CONFIRMED`, `ACCESS_BLOCKED`, or `TOOL_UNAVAILABLE`. Public-search results cannot alter that classification. Seven new regression tests pass, and the combined MC126 suite passes 28/28 when its temporary directory is kept inside the isolated worktree.

**DSH disposition:** `UPGRADE_LATER`, not now. The local CLI is `@deepseek-ai/dsh 0.1.0-rc.7`; the official npm `latest` dist-tag is `0.2.1-rc.2`. The upgrade crosses multiple prerelease generations and changes plugin/configuration/model-catalog behavior. It should be rehearsed in a separate clone with configuration diffs and rollback evidence before any approval to touch the current installation.

## Track A — KITTY evidence routing

### Observations

1. The canonical GitHub reader is registered in production code and supports allowlisted, read-only issue and pinned-file retrieval. It runs in `taskboard-server.mjs` before DSH is invoked. It is not a DSH headless-session tool.
2. A successful review session, `BR-mvexvnsm-vztgg`, states that it read the pinned files and returned concrete `file:line` findings.
3. The failed re-review session, `BR-mveyr5v0-4lgpq`, states that it ran six public searches, received zero relevant hits, and concluded that the repository evidence was unavailable.
4. The follow-up session, `BR-mveyvv7u-dvgdi`, correctly observed that `/api/github/evidence` was not exposed as a direct tool inside its DSH headless session. That observation does not mean the server-side reader was absent.
5. `extractIssueRefs()` accepts a full issue URL, or a bare `#N` only when a repository is also named. `GitHub Issue #126` therefore supplies no canonical issue target.
6. `extractEvidenceRefs()` requires an explicit blob URL or an allowlisted repository plus a path-shaped token. A commit SHA and the phrase “seven files” do not supply file targets.
7. `needsResearch()` matches `最新`. The server's current condition enables public research when no successful GitHub read exists, including when no GitHub target was parsed at all.
8. Job records persist the message, model and basic metrics, but not the parsed GitHub targets, access classification, reader availability, or reason that public research was enabled. This is an observability gap.

### Root-cause classification

| Candidate | Result | Evidence-based judgment |
|---|---|---|
| Reader registered/callable | YES | The server contains issue and file readers; an earlier pinned review succeeded. |
| Reader callable as a DSH headless tool | NO | It is a Mission Control pre-processing route, not a DSH plugin exposed to the model. |
| Router misclassification | **PRIMARY CAUSE** | Shorthand issue + commit wording parsed to zero canonical targets, then `最新` enabled web research. |
| Missing session/context state | CONTRIBUTOR | Recent dialogue was present, but capability/routing state was not durable or injected as an explicit contract. |
| Bad fallback/failure classification | **PRIMARY CAUSE** | Search zero-hits were allowed to stand in for authenticated repository access. |
| DSH/model malfunction | NOT SUPPORTED | The failed turn completed normally on `deepseek-v4-pro`; it followed the wrongly selected search route. |

### Minimal isolated repair

Files:

- `tools/mc_integration/kitty-evidence-routing.mjs`
- `tests/test_kitty_evidence_routing.mjs`

Rule:

1. Detect GitHub evidence intent before generic current-information research.
2. If canonical content was returned, report `ACCESS_CONFIRMED`.
3. If the canonical reader returned an explicit failure, report `ACCESS_BLOCKED` and retain the exact reason.
4. If no canonical target was parsed or the reader is absent in the current route, report `TOOL_UNAVAILABLE`.
5. Never start or interpret public search as a repository-access probe.

This is a reference implementation in the isolated feature branch. It has **not** been copied into, deployed to, or hot-loaded by the production KITTY repository.

### Regression results

| Case | Expected | Result |
|---|---|---|
| Exact failed shorthand request containing `最新` | `TOOL_UNAVAILABLE`, no public research | PASS |
| Fresh pinned GitHub blob read | `ACCESS_CONFIRMED` | PASS |
| Existing-session issue result | `ACCESS_CONFIRMED` | PASS |
| Canonical `NOT_ALLOWLISTED` result | `ACCESS_BLOCKED` | PASS |
| Reader absent in current route | `TOOL_UNAVAILABLE` | PASS |
| Public search has zero/irrelevant results | Classification unchanged | PASS |
| Ordinary current-version question | Public research permitted | PASS |

Test command: `node --test tests/test_mc_integration_runner.mjs tests/test_production_adapter.mjs tests/test_kitty_evidence_routing.mjs`

- First run: 15 passed / 13 failed. Every failure was `EPERM` while renaming under the Windows sandbox's default temporary directory.
- Controlled rerun with `TEMP` and `TMP` set to `.tmp-mc126-tests` inside the worktree: **28 passed / 0 failed**. The temporary directory was removed after the run.
- Syntax checks for both new files: PASS.

## Track B — local DeepSeek Harness audit

### Installed runtime and routing

| Item | Verified state |
|---|---|
| Local root | `D:\EcoEngine\eco-engine-lab\deepseek-harness` |
| Declared dependency | `@deepseek-ai/dsh: ^0.1.0-rc.7` |
| Installed CLI | `0.1.0-rc.7` (`dsh --version`) |
| Installed Codex adapter | `@deepseek-ai/dsh-subagent-codex@0.1.0-rc.7` (extraneous local package) |
| Profiles | `headless`, `kitty-worker`, `nightshift-deepseek-codex`, `web` |
| `headless` | Base + headless bundles; no custom tools in its patch |
| `kitty-worker` | Base + headless plus explicit `subagent_codex`; execution-only boundary |
| `web` | Base + web app plus local Windows directory-picker compatibility patch |
| Mission Control reasoning route | `headless` |
| Mission Control execution route | `kitty-worker` |
| GitHub evidence route | Mission Control server-side reader; not shared with DSH headless |

The production bridge selects `deepseek-v4-flash` for normal reasoning and `deepseek-v4-pro` for deep turns. Existing isolated Stage-0 evidence recorded successful `deepseek-v4-pro` execution and an API error that listed `deepseek-v4-pro`, `deepseek-v4-flash`, and `deepseek-v4-flash-vision-exp` as supported at that test date. This is evidence of the local adapter/API behavior at the time of the recorded test, not a fresh live provider probe.

### Non-destructive runtime checks

- CLI version query: PASS (`0.1.0-rc.7`).
- Package/dependency inventory: PASS.
- Profile and patch inspection: PASS; no credential values were read or copied.
- Historical successful model result: PASS (`PONG-STAGE0-OK`).
- Historical invalid-model classification: PASS; explicit provider error retained.
- Historical provider-disconnect classification: PASS; explicit network error retained.
- Current process/port check: **NOT RUNNING**. At final inspection there was no Node process and neither port `3080` nor `3597` was listening. No service was started or restarted.
- Fresh live model call: NOT RUN, because the authorized task forbids altering/restarting production and a live call was unnecessary to diagnose the router defect.

### Actual issues and risks

1. **Version drift:** installed `0.1.0-rc.7` is materially behind official npm `latest` `0.2.1-rc.2`.
2. **Upgrade compatibility:** upstream `0.2.0-rc.2` updated the third-party model catalog and warns that some older model IDs were removed. The current local profiles and the separately installed Codex adapter require compatibility testing.
3. **Current availability:** DSH and KITTY were not listening at final inspection. This is an operational state, not a reason to restart them without approval.
4. **Timeout termination:** the current Mission Control bridge calls `child.kill()` and immediately settles timeout failure without waiting for confirmed child termination. That can leave uncertain process state; it is outside this isolated routing patch.
5. **Telemetry gap:** the failed KITTY job did not retain evidence-target parsing and access-status fields, which made the wrong search route harder to audit.

### Official update evidence

- Official npm registry metadata: `@deepseek-ai/dsh` currently tags `0.2.1-rc.2` as `latest` and `next` (published 2026-10-17): <https://registry.npmjs.org/%40deepseek-ai%2Fdsh>
- Official release `v0.2.1-rc.2` adds DeepSeek-V4.1-Flash-1017 and DeepSeek Search/Fetch API support: <https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.2.1-rc.2>
- Official release `v0.2.0-rc.2` documents Windows fixes and model-catalog compatibility changes, including removed old model IDs: <https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.2.0-rc.2>
- Official CLI documentation defines profiles as ordered plugin-bundle stacks and supports configuration inspection with `--dump-config`: <https://github.com/deepseek-ai/deepseek-harness/blob/master/apps/cli/README.md>

### Recommendation: UPGRADE_LATER

Do not in-place upgrade the current harness. After Founder approval:

1. Create a separate DSH clone/install pinned to `0.2.1-rc.2`.
2. Copy no credentials; point the test instance at a separate test home and loopback port.
3. Compare `--dump-config` for `headless`, `kitty-worker`, and `web` against sanitized current configuration.
4. Verify the Codex adapter version/API, the three required model routes, tool allowlists, Windows PowerShell completion, cancellation, and a GitHub-evidence request that must not invoke public search.
5. Record rollback as restoring the current `package-lock.json`, `node_modules` version set, profile files, and prior start command; only then request production change approval.

## Evidence paths

- Failed public-search output: `D:\Codex\ClimbOS-Mission-Control\docs\taskboard\evidence\_katie-brain\stdout-BR-mveyr5v0-4lgpq.log`
- Successful pinned review output: `D:\Codex\ClimbOS-Mission-Control\docs\taskboard\evidence\_katie-brain\stdout-BR-mvexvnsm-vztgg.log`
- Follow-up tool-availability result: `D:\Codex\ClimbOS-Mission-Control\docs\taskboard\evidence\_katie-brain\result-BR-mveyvv7u-dvgdi.json`
- Production router: `D:\Codex\ClimbOS-Mission-Control\docs\taskboard\server\taskboard-server.mjs`
- GitHub reader/parser: `D:\Codex\ClimbOS-Mission-Control\docs\taskboard\server\github-issues.mjs`
- Brain research classifier: `D:\Codex\ClimbOS-Mission-Control\docs\taskboard\server\katie-brain.mjs`
- DSH bridge: `D:\Codex\ClimbOS-Mission-Control\docs\taskboard\server\deepseek-executor.mjs`
- DSH profiles: `D:\EcoEngine\eco-engine-lab\deepseek-harness\config\dsh-home\profiles`
- Historical Stage-0 results: `D:\EcoEngine\eco-engine-lab\deepseek-harness\workspace\stage0-results`

## Change and approval boundary

### Fixed now

- Root cause identified from source and session logs.
- Minimal deterministic routing guard implemented in isolation.
- Fresh/existing/blocked/unavailable/search-fallback cases covered by tests.
- DSH installed version, profiles, model evidence, routing and current availability audited.
- No production repository, service, port, key, model default or DSH installation changed.

### Requires Founder approval

- Port the reviewed routing guard into production `taskboard-server.mjs` and persist route-decision telemetry.
- Start or restart production KITTY/DSH to perform a live end-to-end re-review.
- Patch timeout termination semantics in the production DSH bridge.
- Rehearse and later approve any DSH upgrade to `0.2.1-rc.2`.
- Merge this feature branch. `PRODUCTION_NO-GO` remains until those steps are separately approved and verified.

## Conversation Radar

- Knowledge: GitHub evidence is a server-side canonical read path; DSH web search is a separate, non-authoritative research path.
- Idea: make evidence access a typed state machine and persist its decision fields with every job.
- Decision: isolate the fix; suppress public search for GitHub evidence intent; recommend `UPGRADE_LATER`.
- Risks: production router still contains the defect; services were not running at final inspection; DSH upgrade compatibility is untested.
- Open questions: whether the production reader should resolve bare issue references from a thread-level repository binding; whether DSH timeout cancellation needs a process-tree kill contract on Windows.
- Next actions: Founder review, approve production port and controlled restart test, then separately approve an isolated DSH upgrade rehearsal.
- Related projects: ClimateOS, EcoEngine, Mission Control, KITTY, evidence governance, human-in-the-loop validation.

