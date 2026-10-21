# Council Bridge v0.1 — local synthetic rehearsal

Standard implementation unit: **Council**, including its jurisdiction and organisational responsibilities. The farm remains a child site. First candidate context: Snowy Monaro Regional Council. There is no Council endorsement or real deployment.

## Start

Python 3.10+; standard library only. From the repository root:

```bash
python run_council_bridge.py
```

Open the complete URL printed by the process. Its fragment contains a temporary session capability. The page removes the fragment from browser history and keeps it in page memory; refreshing requires reopening the original full link. Do not share it. Stop with Ctrl+C.

The server binds only `127.0.0.1` on port 8767 (override with `--port`). No background installation, dependency download, network egress or external computation. Data lives in ignored `runtime_data/council_bridge/<council_id>/bridge.sqlite3`.

The supplied fixtures have an explicit 2026-10-01 to 2026-11-01 validity window. They expire normally; the application must not silently redraft their dates. Tests inject a controlled clock. For future rehearsals, author a new reviewed fixture revision and use a separate runtime root rather than overwrite old records.

## Walkthrough

1. Inspect Council overview and spatial objects. Two named settlement contexts, a farm, fictional shared water system and other resources have distinct scopes. The diagram is not geographic evidence.
2. Prepare a request. Inspect its variables, units, periods, spatial identities and exact approval digest.
3. Approve the zero-cost synthetic run. Receive the mock result, or rehearse timeout, retry and cancellation.
4. Generate the existing Time-Bounded Environmental Answer shape. The result remains L0/S0, with explicit missing real evidence and no scientific conclusion.
5. Accept or reject the workflow rehearsal. Accepted demo review is not professional sign-off. Record a fixed synthetic follow-up outcome.
6. Preview metadata sharing, approve that exact preview, then download its JSON. Without approval no export is possible.
7. Copy the approved digest, switch to the second fictional Council and import from the source Council. This copies approved metadata only, never a database or private notes.
8. Withdraw source evidence, return to the receiving Council and explicitly reconcile imports. The old answer text and exchange payload remain preserved, but their usability changes. Offline recipients do not receive automatic revocation notifications.

## Architecture

- `contracts.py`: closed Compute Request validation, spatial types, identifiers and clocks; imports existing canonical JSON and digest helpers.
- `fixtures.py`: configuration and authored synthetic records, separate from generic runtime.
- `runtime.py`: per-Council SQLite transactions, local principal permissions, receipts, existing answer/passport patterns, review, metadata export/import and withdrawal.
- `providers.py`: provider Protocol, two interchangeable mocks and a denied Matrix One placeholder.
- `server.py`: loopback-only HTTP adapter, temporary bearer capability, Host/Origin checks, body limits, restrictive browser headers and explicit routes.
- `static/`: Chinese working interface; no external scripts, fonts, tiles, analytics or requests.

Public context and historical repository references are visible but not admitted as fresh Council-level environmental evidence. Historical real receipts and PR125 farm research remain unchanged.

## Exchange and governance contract

The exchange envelope is `climateos.council_bridge.v0.1.exchange`. Its body contains source Council, classification, licence and a fixed allowlist of synthetic evidence identity/revision/time/status fields. No arbitrary file upload or remote JSON import is accepted. The trusted local broker verifies source approval and digest before importing. Imported metadata is never local environmental evidence.

New source evidence revisions produce new preview digests; old releases retain their payload and can be withdrawn. Recipient status reconciliation checks source release status and expiry. This is a local prototype for federation semantics, not a signed cross-host transport.

The runtime uses a Council-scoped Principal with separate `read`, `compute`, `review`, `publish`, `exchange` and `observe` permissions. The web adapter's session represents one local operator with all those permissions. Independent users, delegated roles and professional identities are not implemented. An approval digest binds content; it is not a human digital signature.

Events and state digests detect accidental/inconsistent changes and refuse subsequent mutation after inconsistency. A privileged local attacker can rewrite both database and chain. Independent signatures, witnesses, protected backups and key rotation are future deployment requirements.

## Verification

```bash
python -m unittest tests.test_council_bridge
python -m unittest discover
node --check cczps_lite/council_bridge/static/app.js
```

See [baseline and reuse](BASELINE_AND_REUSE.md), [validation and delivery status](VALIDATION.md), and [unsent partner entry pack](PARTNER_ENTRY_UNSENT.md).
