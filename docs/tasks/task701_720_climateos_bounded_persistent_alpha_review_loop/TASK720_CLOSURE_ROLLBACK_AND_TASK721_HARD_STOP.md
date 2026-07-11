# Task720 Closure Rollback And Task721 Hard Stop

## Closure

Task701-720 closes only after the full regression and new test suites,
migration, integrity, diagnostics, backup/restore, restart, rollback,
concurrency, static syntax, Git and boundary checks pass.

## Rollback

1. stop the localhost service;
2. validate the recorded pre-migration v2 or final v3 backup;
3. restore only through the manual restore command to a reviewed target;
4. run migration preflight and integrity diagnostics;
5. retain the preserved pre-restore database and all audit evidence;
6. revert code only through a reviewed, non-destructive Git operation.

The v3 migration is additive. Existing v2 tables remain intact. Alpha rollback
creates a new revision and never deletes prior revisions or audit events.

## Prohibited Work Not Performed

No private EcoEngine or D: drive access, production runtime, public API, MCP,
authentication, encryption platform, external model, live data, sensor,
gateway, autonomous agent, automation, EcoChain, scoring, certification,
compliance conclusion, deployment, PR, merge, release or tag.

## Hard Stop

Stop at Task720. Task721 is not started and requires a separate Founder Gate.
