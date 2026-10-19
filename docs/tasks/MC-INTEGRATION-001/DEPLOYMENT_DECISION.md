# MC-INTEGRATION-001 deployment decision

Code-review status: **REVIEW_PENDING** at the new remediation commit

Deployment decision: **PRODUCTION_NO-GO**

## Basis

The adapter candidate and failure controls are reviewable and locally tested. Production deployment is not yet safe because:

1. the canonical KITTY worktree is dirty and live runtime files change; a staging procedure must compare sorted pre/post porcelain entry sets and explain every delta;
2. the candidate has not been wired to a real KITTY route;
3. actual Codex tool/shell execution in the Windows read-only sandbox remains failed/unverified;
4. `start-mission-control.ps1` is the verified canonical Founder launcher, but no automated rollback command was verified;
5. production restart/recovery and state-directory rename semantics have not been tested;
6. deployment/restart requires a separate Founder gate under the current KITTY policy.

## What is ready

- default-off isolated adapter candidate;
- repository/Issue/model allowlists;
- bounded prompt/result/failure resources and termination-aware timeout policy;
- durable race-free idempotency and explicit failure receipts;
- cooperative cancellation, corrupt-evidence isolation, recovery, writeback and recursive redaction behavior;
- documented clean-worktree integration and rollback sequence.

## Required next approval

KITTY must independently re-read and review the new immutable remediation commit. A separate Founder decision is still required before creating a staging integration or invoking the verified canonical launcher. Approval to open a PR, merge or deploy has not been inferred.

## Conversation Radar

- Knowledge: production KITTY is healthy and localhost-only; its GitHub routes are currently read-only.
- Decision: keep the Codex adapter separate and default-off; do not touch the dirty production tree.
- Risk: filesystem semantics and Codex child-shell behavior differ between sandbox and normal host execution.
- Open question: what reviewed command or artifact provides automated rollback before staging can be considered?
- Next action: KITTY re-reviews the isolated remediation commit; `REVIEW_PENDING` must not be conflated with `PRODUCTION_NO-GO`.
- Keywords: `ClimateOS`, `KITTY`, `Mission Control`, `Codex CLI`, `GitHub Issue`, `idempotency`, `rollback`, `human-in-the-loop`.
