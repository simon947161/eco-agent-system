# ClimateOS Task2020 — Windows SQLite Lifecycle Revision Founder Gate

Date: 2026-07-20

Status: `WINDOWS_REVISION_VALIDATED / READY_FOR_FOUNDER_DECISION / PR92_DRAFT / DO_NOT_AUTO_MERGE`

PR: `#92`

Revision authority:

`REQUEST_PR92_REVISION`

Authoritative pre-revision head:

`b9032b32743cefe823b25956658c874bfbecbc81`

## Decision requested

The Founder is asked to review the narrow Windows SQLite handle-lifecycle revision.
No merge is implied or authorized by this record.

## Root cause

SQLite connections were used as transaction context managers. Python's SQLite
connection context commits or rolls back on exit but does not close the connection.
On Windows, those handles could survive until garbage collection and prevent
`TemporaryDirectory` from deleting synthetic SQLite files, producing `WinError 32`.

## Narrow revision

- every operation-scoped SQLite connection is explicitly closed after transaction exit;
- runtime, program, continuity and store objects expose idempotent `close()` methods;
- localhost threaded servers own their runtime resources and implement idempotent
  shutdown, server close and resource close paths;
- server test teardown performs shutdown, server close, worker-thread join and
  resource close before temporary-directory cleanup;
- direct-runtime tests close runtime resources and direct SQLite test connections;
- no sleep, expected-failure marker, Windows skip or weakened assertion was added.

## Windows validation

- continuity tests: `8 tests / OK / 1 symlink-permission skip`;
- affected runtime, program and server tests: `40 tests / OK`;
- complete suite: `343 tests / OK / 1 symlink-permission skip`;
- synthetic SQLite immediate deletion: passed;
- restore-preview SQLite SHA-256 before and after:
  `386c27a59e16f538f46584c3de738faaa54d46ae418d505cc19baac97736d9c5`;
- restore preview reported the synthetic cycle difference, `sqlite_changed: false`,
  and `automatic_import_available: false`;
- `git diff --check`: passed locally.

GitHub Actions must be successful on the published revision head before Founder
approval. The authoritative remote check state remains the PR check result itself.

## Preserved boundaries

- no Founder SQLite or real observation was accessed;
- no continuity safety contract, path boundary, overwrite rule or restore mode changed;
- no automatic restore, import, database migration or external transfer was added;
- no official-source refresh, real data acquisition or environmental conclusion occurred;
- `prototype/` remains unrelated, untracked and untouched;
- PR #92 remains Draft and must not be merged automatically.

## Founder options

1. `APPROVE_PR92_CONTROLLED_MERGE`
2. `REQUEST_PR92_REVISION: <reason>`
3. `HOLD_PR92`
