# MC-INTEGRATION-001 deployment decision

Decision: **NO-GO FOR PRODUCTION DEPLOYMENT**
Secondary status: **GO FOR FOUNDER/KITTY/CHATGPT REVIEW OF ISOLATED CANDIDATE**

## Basis

The adapter candidate and failure controls are reviewable and locally tested. Production deployment is not yet safe because:

1. the canonical KITTY worktree contains 1,015 dirty entries;
2. the candidate has not been wired to a real KITTY route;
3. actual Codex tool/shell execution in the Windows read-only sandbox remains failed/unverified;
4. the canonical service launcher/supervisor and automated rollback command were not verified;
5. production restart/recovery and state-directory rename semantics have not been tested;
6. deployment/restart requires a separate Founder gate under the current KITTY policy.

## What is ready

- default-off isolated adapter candidate;
- repository/Issue/model allowlists;
- bounded resource and timeout policy;
- durable idempotency and explicit failure receipts;
- cancel/recovery/writeback/redaction behavior;
- documented clean-worktree integration and rollback sequence.

## Required next approval

Founder approval is required only after review to create a clean staging integration against the exact KITTY production commit, identify the canonical launcher, and run a staging restart. Approval to push, open a PR, merge, or deploy has not been inferred.

## Conversation Radar

- Knowledge: production KITTY is healthy and localhost-only; its GitHub routes are currently read-only.
- Decision: keep the Codex adapter separate and default-off; do not touch the dirty production tree.
- Risk: filesystem semantics and Codex child-shell behavior differ between sandbox and normal host execution.
- Open question: which launcher/supervisor is authoritative for controlled KITTY restart and rollback?
- Next action: review the isolated commit and evidence, then explicitly authorize staging integration if accepted.
- Keywords: `ClimateOS`, `KITTY`, `Mission Control`, `Codex CLI`, `GitHub Issue`, `idempotency`, `rollback`, `human-in-the-loop`.
