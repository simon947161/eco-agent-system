# Atlas V1.5 W1 — accounting slice verification report

Date: 2026-10-29 Australia/Sydney  
Repo/branch: `simon947161/eco-agent-system`, `feature/public-strategy-atlas-web-mvp-20261029`, Draft PR #130.  
Deliverable: **real JavaScript model + inspector integration + checked external source crosswalk + Node test source**. No new paid dependencies, deployment, merges or Council private data.

## Implemented (GitHub source)
- `atlas-accounting.js` exports a bounded quantitative-extension API and three typed case paths indexed by **existing AtlasData node IDs**: `csp6`, `water`, `area`. It is not a duplicate graph and has no persistence or network calls.
- Carbon observation: CSP 2035 environmental measure, **29.9 t CO2e/person**, reference source year **2021–22**, desired direction decrease. Source is Council-published full CSP p.30 and attributed to Snapshot Climate. `PUBLIC_TEXT_OBSERVED` remains **NOT ADMITTED as a real goal-to-work mapping**; no population multiplier, real DP/OP link, budget or achieved reduction.
- Water: explicit `SYNTHETIC` 12 ML volume, AUD 24,000 fictional actual expenditure, derived AUD 2,000/ML synthetic cost intensity. This is **not a current or historical Council payment**.
- Land: explicit `SYNTHETIC` 50 ha scenario, NOT a current LEP/DCP ruling/consent, real land allocation or approved resource use.
- `index.html` now loads the extension before `atlas.js`; existing station inspector appends a quantity/resource/evidence section and a `Quantities & budget` shortcut when a case exists. Original 127-content tree, local immutable edits, source admission and route-first canvas not intentionally replaced.
- `sources/STRATEGY_WORK_ACCOUNTING_CROSSWALK_20261029.md` records actual public source URLs and explicit UNKNOWNs for DP/OP/budget/LEP/DCP case-level links.

## Executed in GitHub-connected JavaScript isolate (not a browser or Node CLI)

- Read/parsed the submitted JS extension and production `atlas.js` with JavaScript parser: PASS.
- Loaded the extension as a CommonJS-shaped export in a V8 isolate: PASS.
- Three cases + CSP metric 29.9: PASS.
- Carbon per-capita × population with observation not admitted: REJECTED `UNADMITTED_INPUTS`.
- ML to ML/day conversion without a duration: REJECTED `UNIT_CONVERSION_NOT_DEFINED`.
- Forecast budget instead of actual expenditure in unit cost: REJECTED `BUDGET_IS_NOT_EXPENDITURE`.
- Shared financial allocation that sums to 200%: REJECTED `DOUBLE_COUNT_OR_UNALLOCATED`.
- Synthetic water cost intensity 24,000 / 12 = 2,000 AUD/ML: PASS.

**Tests committed for next executable Node run:** `node apps/public-strategy-atlas/accounting.test.cjs` covers 3 scenario IDs, source status, unit conversion, counterexamples for method/area/period/boundary, funding types and double counting. Do NOT mark it Node PASS until actually executed.

## Honest limitations

- **NOT TESTED IN REAL BROWSER THIS SLICE:** Quantities panel/shortcut on 1440×900 and 390×844, keyboard/screen reader, overflow/fit, all previous tests, 2-tab version conflict regression. Previous route-first U1 QA from `qa/ROUTE_FIRST_RESULTS.md` remains historical; it is not a pass for this new module.
- Original CSP summary 6.1 PDF byte-backed admission is separate. The **full CSP 2035 p.30 PDF bytes were not newly fetched or independently SHA-256 verified** in this task. The published text/table appears in public search results, but original page visual/legal reuse/revision approval must still be independently examined before full admission. `PUBLIC_TEXT_OBSERVED` is deliberate.
- The model has no currency-year adjustment or inflation engine, no actual budget/costs, no official DP/OP action mapping, no source-to-CSP 6.1 verified metric assertion, no real LEP/DCP location validation and no official KPI result.
- The local snapshot/append-only workspace applies to its existing records; the new `AtlasAccounting` layer is a *read-only derived research extension* and has not yet been added to exported base content-addressed snapshots or the immutable local revision event format. Do not present it as independently signed or fully audit-snapshotted.
- Zero external API, Council personal data, active deployment, PR merge or actual Council service outcome.

## Required next engineering step

**Priority next:** run the new Node test and all previous suites; use real Chrome to open `http://127.0.0.1:8877/`, select csp6/water/area, inspect labelled accounting panel at desktop/390px, verify fail-closed cases; fix defects. Then integrate typed accounting into the authoritative content-addressed snapshot/revision/history/export pipeline (without changing official source state), add provenance-to-relation reverse paths and three-way workspace reconciliation. Current LEP, DP/OP and resourcing documents require exact clause/edition/adoption/location verification before actual links can be asserted.

This is **PARTIAL W1 working code**, not an accepted full V1.5 source-to-work system.
