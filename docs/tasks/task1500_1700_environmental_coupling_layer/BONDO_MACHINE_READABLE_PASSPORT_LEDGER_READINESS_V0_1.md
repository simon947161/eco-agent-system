# Bondo Machine-Readable Passport and Manual Ledger Readiness v0.1

Date: 2026-07-16

Status: LOCAL_STATIC_PROTOTYPE_PASS / REAL_SOURCE_OPERATION_BLOCKED / CONCLUSIONS_BLOCKED

## 1. Prototype result

The prototype provides a strict JSON Schema artifact, a small static example,
a dependency-free validator and a local JSONL ledger. The static example is a
machine representation of already-authored repository content; it is not a
new Bondo observation and does not claim completeness.

The representation retains:

- readable claim wording and readable state;
- one or more controlled states rather than a truth score;
- supporting, contradicting and missing-evidence references;
- raw-data, GIS, model/weight, account/cost and scientific-approval guards;
- prohibited uses through validation and alert preview.

## 2. Ledger contract

Every event must be manually supplied and classified as either
`FICTIONAL_MANUAL` or `REPOSITORY_STATIC_MANUAL`. It records no source access.
The ledger assigns a monotonically increasing sequence, links the prior record
hash and computes a deterministic SHA-256 receipt over canonical JSON.

Before appending, the complete existing chain is revalidated. Editing an older
event, sequence or link causes validation failure. This is tamper-evidence for
a local prototype, not a claim of adversarial security, notarization or legal
record status.

## 3. Alert boundary

`preview_internal_alert` returns deterministic `RECORD_ONLY` or
`REVIEW_REQUIRED` content. It contains no transport, webhook, email, message,
account or recipient function and always reports `dispatch_performed: false`.

## 4. Verification

Local isolated command:

`python -m unittest discover -s tests -p 'test_bondo_passport_ledger.py' -v`

Result on 2026-07-16: `8 passed`.

Verified cases:

1. readable and controlled claim states coexist;
2. raw-data admission and scientific approval are rejected;
3. unknown states and unresolved references are rejected;
4. two fictional manual events form a valid hash chain;
5. changed ledger content fails receipt validation;
6. source access, real data, external contact, notification and scientific-conclusion flags are rejected;
7. material-event alerts remain preview-only;
8. fixture loading is confined to the repository input directory.

The JSON artifacts also parse successfully with the Python standard library.
No third-party package, external service or network access is required.

## 5. Readiness decision

`MACHINE_STRUCTURE_PASS / LOCAL_FICTIONAL_LEDGER_PASS / REAL_SOURCE_EVENT_INTAKE_BLOCKED / AUTOMATION_BLOCKED / SCIENTIFIC_USE_PROHIBITED`

This prototype is ready for Founder review and repository-level CI. It is not
ready for real source observations, automated monitoring, external alerts,
scientific review admission or project decisions.

## 6. Cost, data and contact state

| Boundary | Result |
|---|---|
| incremental cost | AUD 0 |
| account/cloud/paid source | none |
| external inquiry or reviewer contact | none |
| source refresh or network check | none |
| raw PDF/GIS/meteorological/reanalysis data | none |
| model or weight | none |
| real ledger event committed | none |
| external alert sent | none |
| scientific/project conclusion | none |
| GraphCast | `LATER` |
