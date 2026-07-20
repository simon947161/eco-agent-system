# ClimateOS Task2011–2020 — Local Private Continuity Readiness Plan

Date: 2026-07-20

Status: PLANNING_READY / IMPLEMENTATION_NOT_STARTED / NO_LOCAL_DATA_ACCESSED

## Purpose

The next product objective is to keep the Founder's long-running research record
safe and portable without turning public GitHub, ChatGPT or an external cloud
service into the storage location.

The intended local-only path is:

`select scope → preview manifest → choose local destination → write new backup → verify digest → keep SQLite unchanged`

Restore remains a separate validation path:

`select backup → validate schema/digest/limits → preview differences → human decision → no automatic import`

## Proposed task map

| Task | Candidate capability |
|---|---|
| 2011 | define program/cycle backup envelope and privacy labels |
| 2012 | define canonical JSON manifest and content digest |
| 2013 | build preview-only local backup response |
| 2014 | add explicit new-file write with overwrite refusal |
| 2015 | validate backup schema, size, identity and digest |
| 2016 | build restore-difference preview without database mutation |
| 2017 | define human-confirmed observation-draft interchange |
| 2018 | test malformed, oversized, path and overwrite denials |
| 2019 | test that private records never enter repository fixtures or logs |
| 2020 | Founder review, closure and next gate |

## Admission conditions before implementation

- PR #91 remains unmerged until the deferred Founder computer review;
- the backup destination must be chosen locally by the human;
- default paths must remain under a dedicated ignored runtime-data directory;
- every write must create a new file and refuse overwrite;
- payloads must have a small explicit size ceiling;
- backup JSON must carry schema version, program identity, export time, record
  counts and a canonical content digest;
- restore must be preview-only in the first implementation;
- no browser upload to GitHub, cloud synchronization, email or external API;
- no SQLite file copying while an uncontrolled write may be active;
- no personal, Council-internal or customer record may be introduced into tests.

## Threat and failure register

| Risk | Required response |
|---|---|
| path traversal or absolute-path escape | reject before file access |
| symlink/reparse-point escape | refuse or constrain to the admitted local root |
| accidental overwrite | fail closed; generate no replacement |
| partial write or interruption | write temporary local file, verify, then atomic rename |
| malformed or incompatible schema | report validation errors; no import |
| digest mismatch | quarantine backup as invalid |
| oversized payload | reject before parse/write |
| observation leaked into Git history | ignored output root plus repository-status test |
| backup mistaken for environmental evidence | explicit non-scientific continuity label |
| automatic restore corrupts SQLite | restore remains preview-only until a later gate |

## Work allowed while Founder is mobile

This plan and repository-authored synthetic tests may be refined. No real local
SQLite file, Founder observation, external storage, scheduler, notification,
network bridge or restore mutation is authorized by this planning record.

## Next implementation decision

After PR #91 visual review, choose whether Task2011–2020 should implement:

- backup preview and new-file export only (recommended first slice); or
- hold continuity work and focus on another Runtime usability burden.

