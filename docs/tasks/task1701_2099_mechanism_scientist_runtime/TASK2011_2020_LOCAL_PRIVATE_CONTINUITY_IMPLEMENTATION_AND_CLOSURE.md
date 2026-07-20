# ClimateOS Task2011–2020 — Local Private Continuity Implementation and Closure

Date: 2026-07-20

Status: `IMPLEMENTED / AUTOMATED_VALIDATION_PASSED / DRAFT_PR92 / FOUNDER_GATE_REQUIRED`

Authoritative base:

`f00f77ffe344264b1999ce2ec336576fd6783603`

Branch:

`agent/task2011-2020-local-private-continuity`

Draft PR: `#92`

## 1. Outcome

Task2011–2020 implements a bounded local continuity layer for the persistent research
Runtime. It can preview a canonical backup, write one new JSON backup file under a
dedicated ignored local root, validate that file, and preview restore differences.

It does not copy SQLite and does not import, merge or mutate any database record.

## 2. Task map closure

| Task | Implemented result |
|---|---|
| 2011 | backup envelope, privacy label and non-scientific status |
| 2012 | canonical UTF-8 JSON and deterministic SHA-256 content digest |
| 2013 | preview-only backup response with no directory or file creation |
| 2014 | explicit new-file export using temporary write, verification and atomic rename; overwrite refused |
| 2015 | closed schema, size, identity, record-count and digest validation |
| 2016 | program/cycle restore-difference preview with no database mutation |
| 2017 | observation records remain inside exact selected cycle content; no automatic interchange/import admitted |
| 2018 | malformed, oversized, traversal, absolute/nested path, overwrite and symlink-root denial tests |
| 2019 | synthetic temporary SQLite and ignored `runtime_data/` output only; no Founder/private fixture or log content |
| 2020 | automated closure complete; Founder merge gate remains open |

## 3. Runtime contract

Local root:

`<database parent>/runtime_data/local_private_continuity/`

The repository already ignores `runtime_data/` and `*.sqlite3`.

Localhost endpoints:

- `GET /api/continuity/status`
- `POST /api/continuity/preview`
- `POST /api/continuity/export`
- `POST /api/continuity/restore-preview`

Preview/export fields are closed. A browser or client may select a program and exact
cycle identities, but export accepts only a simple `.json` filename, never an absolute
or nested path.

## 4. Backup manifest

Each backup includes:

- schema ID `climateos.local_private_continuity.v0.1`;
- privacy label `LOCAL_PRIVATE_CONTINUITY_NOT_SCIENTIFIC_EVIDENCE`;
- exact program identity;
- export time;
- record counts;
- canonical content digest;
- restore mode `PREVIEW_ONLY_NO_DATABASE_MUTATION`;
- scientific status `NOT_AN_ENVIRONMENTAL_CONCLUSION`.

The digest covers exact program and selected cycle content. The outer envelope and
manifest fields are closed during validation.

## 5. Write safety

- default maximum payload is 256 KiB;
- output root must not be a symlink;
- destination must be one simple JSON filename;
- absolute, nested and traversal paths are rejected before access;
- an existing destination or symlink is rejected;
- the payload is written to a temporary file, flushed, fsynced and length-checked;
- the final name is exclusively reserved and the verified temporary file is atomically moved;
- final bytes are read back and verified;
- SQLite bytes are not copied or rewritten.

Windows reparse-point defence is implemented through the same fail-closed root and
resolved-destination confinement. A later Windows Founder review may confirm local
behaviour, but no real Founder database is required for this gate.

## 6. Restore boundary

Restore is validation and difference preview only. It reports:

- program missing/unchanged/different;
- cycles only in backup;
- cycles only locally;
- cycles changed;
- cycles unchanged.

It exposes no import operation and performs no SQL write.

## 7. Validation

GitHub Actions `CCZPS-Lite Tests` completed its compile and complete unit-test steps
successfully on the implementation branch. Added tests use temporary synthetic
program/cycle records only and cover:

- deterministic preview and no-write behaviour;
- new-file export and overwrite refusal;
- restore difference preview without SQLite mutation;
- digest and record-count tampering;
- malformed and oversized files;
- traversal, absolute/nested path and extension rejection;
- unknown cycle identity rejection;
- symlink-root rejection where the platform permits symlink creation;
- closed envelope and manifest fields.

## 8. Explicit exclusions

Not implemented or authorized:

- automatic restore or SQLite mutation;
- copying a live SQLite file;
- selecting arbitrary filesystem paths;
- cloud/object storage, email or external transfer;
- scheduler, notification or unattended backup;
- ChatGPT/MCP-to-localhost bridge;
- real official-source refresh or scientific-data acquisition;
- Cooma environmental trend, forecast, causal, operational or engineering conclusion;
- GraphCast, WRF, WRF-Chem, GIS or external package execution.

## 9. Founder Gate

PR #92 remains Draft and must not be merged automatically. Founder may authorize merge
based on this bounded implementation and automated evidence, request a narrow Windows
localhost review, or request revision.
