# ClimateOS Task2020 — Founder Gate

Date: 2026-07-20

Status: `READY_FOR_FOUNDER_DECISION / PR92_DRAFT / DO_NOT_AUTO_MERGE`

Draft PR: `#92`

Base:

`f00f77ffe344264b1999ce2ec336576fd6783603`

## Decision requested

Task2011–2020 Local Private Continuity has completed its bounded implementation and
automated test pass. The Founder is asked to choose one of:

1. `APPROVE_PR92_CONTROLLED_MERGE`
2. `REQUEST_TASK2020_WINDOWS_REVIEW`
3. `REQUEST_PR92_REVISION: <reason>`
4. `HOLD_PR92`

No merge is implied by this gate.

## What approval would accept

- canonical local backup envelope and deterministic digest;
- preview-only backup response;
- explicit new-file-only JSON export inside the dedicated ignored runtime-data root;
- overwrite, malformed, oversized, path escape and symlink-root denial;
- schema, identity, counts and digest validation;
- restore-difference preview only, without import or SQLite mutation;
- localhost-only continuity endpoints;
- synthetic tests only.

## What approval would not authorize

- accessing or exporting the Founder's real SQLite records during repository work;
- arbitrary-path export, automatic backup or automatic restore;
- cloud, email, scheduler, notification or external bridge;
- official-source refresh, scientific-data collection or model execution;
- a Cooma environmental conclusion;
- any later Task2021+ scope.

## Optional Windows review

A Windows review is optional rather than mandatory because the implementation has no
visual UI change and the test suite uses temporary synthetic records. If requested,
the narrow review should use a temporary/synthetic database and verify:

1. continuity status reports new-file-only and preview-only modes;
2. preview creates no file;
3. one synthetic JSON export is created below `runtime_data/local_private_continuity`;
4. repeating the same filename is refused;
5. restore preview reports differences without changing SQLite.

Do not use the Founder's real research records for that optional test.
