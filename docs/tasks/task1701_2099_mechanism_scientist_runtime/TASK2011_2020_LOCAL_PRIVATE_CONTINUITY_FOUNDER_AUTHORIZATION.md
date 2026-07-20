# ClimateOS Task2011–2020 — Local Private Continuity Founder Authorization

Date: 2026-07-20

Status: FOUNDER_AUTHORIZED / IMPLEMENTATION_STARTED / LOCAL_PRIVATE_ONLY

Authoritative base main:

`f00f77ffe344264b1999ce2ec336576fd6783603`

Implementation branch:

`agent/task2011-2020-local-private-continuity`

## Founder decision

The Founder accepted the Task2010 computer UI review and authorized:

1. merge of PR #91;
2. verification of the resulting authoritative main;
3. implementation of Task2011–2020 Local Private Continuity.

PR #91 merged as:

`f00f77ffe344264b1999ce2ec336576fd6783603`

## Authorized objective

Keep the supervised research record locally safe and portable without using public GitHub, ChatGPT, email, an external API or cloud storage as the record store.

The authorized flow is:

`select scope → preview manifest → choose local destination → write new backup → verify digest → keep SQLite unchanged`

Restore remains validation-only:

`select backup → validate schema/digest/limits → preview differences → human decision → no automatic import`

## Authorized task map

- Task2011: program/cycle backup envelope and privacy labels;
- Task2012: canonical JSON manifest and deterministic content digest;
- Task2013: preview-only local backup response;
- Task2014: explicit new-file export with overwrite refusal and atomic completion;
- Task2015: schema, size, identity and digest validation;
- Task2016: restore-difference preview without database mutation;
- Task2017: human-confirmed observation-draft interchange;
- Task2018: malformed, oversized, path, symlink/reparse and overwrite denial tests;
- Task2019: tests preventing private records entering Git fixtures, status output or logs;
- Task2020: Founder review, closure and next gate.

## First implementation slice

Begin with the recommended bounded slice:

1. synthetic backup envelope and canonical manifest;
2. preview-only response;
3. local destination constrained to a dedicated ignored runtime-data root;
4. new-file-only export with overwrite refusal;
5. explicit small payload ceiling;
6. digest verification;
7. synthetic tests only.

The first slice must not copy or migrate the Founder SQLite database and must not access a real Founder observation.

## Mandatory security behaviour

- reject absolute paths and traversal before file access;
- reject destination escape through symlinks or Windows reparse points;
- refuse overwrite and fail closed;
- write to a temporary local file, verify it, then atomically rename;
- reject oversized input before parsing or writing;
- reject malformed/incompatible schema and digest mismatch;
- keep restore preview-only and database-mutating import absent;
- keep generated backups under an ignored local runtime-data directory;
- do not print private payloads in application, test or CI logs.

## Scientific and operational boundary

This work is continuity infrastructure, not environmental evidence.

It does not authorize:

- official-source refresh or real scientific data acquisition;
- Cooma trend, forecast, causal, water-security, fire-risk, wastewater-capacity or adaptation conclusions;
- model, GIS or external package download;
- GraphCast, WRF or WRF-Chem execution;
- scheduler, alerts, publication or unattended operation;
- ChatGPT/MCP-to-localhost bridge;
- cloud/object storage, account, secret or payment;
- expert, Council, agency or developer contact;
- automatic restore or SQLite mutation.

GraphCast remains `LATER`.

## Required delivery pattern

Implementation must remain reviewable in a Draft PR. Return a separate Founder Gate before merge, including:

- exact files changed;
- threat controls implemented;
- tests and results;
- proof that generated private output is ignored and absent from Git history/logs;
- confirmation that no real local database or observation was accessed;
- remaining limitations and proposed Task2020 human review.
