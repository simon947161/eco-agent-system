# ClimateOS Public Strategy Atlas

English, local-first interactive knowledge route map. Follow continuous strategic/planning routes, then open contextual evidence and the internal network inside each station. The main graph has 15 synthetic topics; the internal model has 127 items, including separately labelled public-source observations.

**Status:** working research prototype; M0 retained, M1 validation extended, M2 recursive-content slice verified. Not a complete authoritative knowledge system. No deployment, official endorsement or real Council KPI.

## Founder V1.4: route-first redesign now active

The 2026-10-29 Founder review determined the existing three-column dashboard **does not express the central line/route logic strongly enough**. Read [Founder V1.4 Route-First Directive](../../docs/research/public-strategy-atlas/FOUNDER_UX_V1_4_ROUTE_FIRST_DIRECTIVE_20261029.md) before further UI work. This is an **implementation decision**, not a research hold.

A standalone functional **[Route Map Preview](route-map-preview.html)** uses **the same existing AtlasData** (15 synthetic nodes / 16 typed edges). It gives a large route-first canvas with strategy/planning lines, a separately enabled hypothesis crossover, selectable stations, focus/filter, contextual details and zoom. From the current main website, use **Explore route map** to open it. The preview does **not** yet integrate the full recursive content editor/history/cross-device state into its own overlay. Keep the original main application fully operational while making this visual the **default main-page experience** in the next controlled engineering stage.

Preview contract: `node apps/public-strategy-atlas/route-map.test.cjs` (mock-DOM smoke; real-browser/screenshots and accessibility still required). Do not mistake coloured lines for real strategic progress or approved legal mappings.

## Founder V1.5: quantified work, resources and evidence (W1 first slice)

The active implementation now includes `atlas-accounting.js` (loaded before the route renderer) and a **station-context accounting breakdown**. Select a synthetic **Objective 6.1** theme (`csp6`), **Water action** (`water`) or **Geographic scope** (`area`) station. The contextual inspector shows **Why / Work / Where / Quantity / Resources / Budget vs actual / Outcome / Evidence gaps**, and a **Quantities & budget** shortcut. These are **model cases bound to existing node IDs**, not a second knowledge graph.

- **Carbon** is an attributed *published observation*: **29.9 t CO2e/person** in CSP 2035 printed p.30, citing Snapshot Climate 2021–22, desired trend decrease. Its position next to the synthetic Objective 6.1 station **does not validate that specific goal-to-metric link**, its output or funding. **NOT** AUD/t, Council operational emissions, carbon cost, total emissions or verified outcome.
- **Water and land** are fully **synthetic fixtures** with purpose-labelled quantities and optional synthetic cost intensity. No Council project/spend/land-use permission has been inferred.
- `assertComparable`, `totalFromPerCapita`, `costPerOutput`, `validateAllocations` and `unitConvert` enforce time, geography, scope, unit, methodology, cost class, and allocation constraints. Missing official data stays `UNKNOWN`.

Read [V1.5 source/work crosswalk](sources/STRATEGY_WORK_ACCOUNTING_CROSSWALK_20261029.md) and [first-slice QA](qa/QUANT_ACCOUNTING_FIRST_SLICE_RESULTS.md). This is a bounded, read-only accounting layer and **is not yet included in portable content-addressed snapshots/revision event histories**. It does not complete official source admission or a real CSP→DP→OP financial chain.

Run from repo root:

```bash
node apps/public-strategy-atlas/accounting.test.cjs
```

**The new Node and Chrome suite needs to be run in a suitable engineering/browser environment.** Connector V8 smoke checks have run; the new browser acceptance and prior regression suites have **not** been re-executed in this particular development slice.

## Run

Keep this entire directory together. No package installation is required.

```bash
cd apps/public-strategy-atlas
python -m http.server 8877 --bind 127.0.0.1
```

Open `http://127.0.0.1:8877/`. Direct `index.html` opening also uses classic scripts; final browser checks used HTTP. The portable SHA-256 implementation supports contexts without Web Crypto.

## Explore

1. Select a station in the default **Route map** to inspect its source entry and upstream/downstream links. Links themselves are also keyboard-selectable.
2. In **Inside this topic**, expand the nested disclosure controls or select any content item.
3. **Explore inside** displays the selected station's internal route. Synthetic paths can run through topic → section → clause → action → indicator → evidence. These are demonstration breakdowns, not extracted Council provisions.
4. Follow the breadcrumb trail or **Parent content**, **Focus this subtree**, and **Back to relationship topic**. Leaves explicitly state that no further content has been admitted.
5. Search titles and internal text. Results show their topic context, with up to 12 displayed matches. Other topics remain accessible through the graph.
6. Use **Expand progressively**, **Expand selected**, **Reset expansion**, **Fit scope**, and zoom. Reduced zoom is an overview; use normal zoom and the inspector to read details.
7. **Tools & views → Public sources** opens five dated observations. The CSP one-page summary observation decomposes into document → Objective 6 → clause 6.1, preserving its exact public locator and observation status. It has no invented downstream actions.
8. **Find a crossing** computes bounded cross-root structural convergence, shows the actual paths and evidence count, and retains authored hypotheses and synthetic counterexamples. Structural detection is not semantic or legal validation.
9. **Tools & views → Synthetic density rehearsal** loads explicitly synthetic 60/200-item fixtures. They test rendering and selection, not the completeness or usability of real policy data.

## Content addressing and portable evidence

Each content item has separate logical and version IDs. Item hashes protect the serialized item. Child-linked subtree hashes propagate a changed descendant into ancestor receipts while leaving unrelated roots unchanged. This is a local hierarchical hash structure, not a blockchain deployment or an independent attestation.

**Export snapshot** downloads a public/synthetic JSON bundle with the dataset, audit result and content-root receipts. Verify it offline:

```bash
node apps/public-strategy-atlas/verify-snapshot.cjs PATH_TO_EXPORTED_JSON
node apps/public-strategy-atlas/verify-snapshot.cjs PATH_TO_EXPORTED_JSON sha256:EXPECTED_CHECKPOINT
```

A digest retained separately provides a comparison checkpoint. A receipt stored alongside editable content is not an independent witness. No signatures, statutory conclusions or tamper-proof guarantee are claimed. Git retains committed source history; the separate local workspace now offers explicitly saved annotation revisions and conflict detection; it does not edit official source records.

## Tests

Run from the repository root:

```bash
node apps/public-strategy-atlas/model.test.cjs
node apps/public-strategy-atlas/content.test.cjs
node apps/public-strategy-atlas/audit-cli.cjs
node --check apps/public-strategy-atlas/atlas.js
```

`qa/ENGLISH_CONTENT_RESULTS.md` records actual browser checks, limitations and screenshots. `qa/narrow-screen.html` is a 390px iframe harness, not physical-device certification. Older QA reports are historical evidence and remain unchanged.

## Evidence and continuity

Current official graph mappings: **0**. The CSP 6.1 chain now verifies original bytes and a bounded extraction; reuse-permission, formal-version, geographic/effective scope and human-review admission remain incomplete. Actual KPI remains UNKNOWN; coverage and elapsed-time demonstrations remain separate.

Read [NEXT_SESSION.md](NEXT_SESSION.md) before continuing from the latest remote HEAD. Development authority remains [V1.3](../../docs/research/public-strategy-atlas/PROJECT_TASKBOOK_V1_3_BUILD_AND_CONTINUITY_20261029.md); it has not been rewritten.

Use only public/synthetic material. Do not upload Council nonpublic records, personal cases or employer system data. No new procurement, deployment, changes to PR129/main, or merge is authorised. Commit verified stages to `feature/public-strategy-atlas-web-mvp-20261029`, push through authorised GitHub access, and read back remote HEAD.

## CSP 6.1 source admission

**CSP 6.1 admission** opens the first byte-backed source-to-anchor chain. The actual official summary PDF was retrieved (416,031 bytes), hashed, rendered and checked against a bounded word-origin anchor on page 1. The original PDF/page image are not redistributed in this repository. The short excerpt and metadata are in `sources/csp61-admission.json`; its classic-script mirror is test-checked for equality.

Reproduce the checks with a separately obtained official PDF:

```bash
python apps/public-strategy-atlas/verify-source.py PATH_TO_OFFICIAL_PDF
```

The engineering checker requires `pdfplumber` (already present in the Work runtime); the website itself requires no added dependency. An altered byte stream fails before extraction. Stage fields separate observation, byte verification, extraction, official revision confirmation, pending review and admission. Current result is **ADMISSION_PENDING_REVIEW**, not ADMITTED. Reuse permission, current adopted-version equivalence, effective scope and human approval are unconfirmed. No CSP→DP/OP mapping is created. Public availability is not taken as a reuse licence.

## Local annotation workspace

Inside any content item, choose **Edit local annotation / compare versions**. Edit only the local title/text, enter a reason, compare and append a CORRECT, SUPERSEDE, CONTEST or RETRACT event. A revert selects an earlier annotation or the original base and appends a new REVERT version. Original observed/synthetic records and source statuses never change. Local annotations have a separate classification and graph marker.

The contextual editor compares retained versions and computes a local subtree receipt binding source-item identities to the separate local view. Earlier versions remain immutable in the application model; replay can reconstruct any retained step. Whole-history replacement by a privileged local writer is not cryptographically prevented without an external checkpoint.

**Local workspace** provides explicit **Save locally**, **Load saved workspace**, import and export. There is no automatic persistence, restoration, network upload or remote collaboration. Local IndexedDB saves use an atomic read/write transaction, an expected saved checkpoint and an append-only lineage check. A stale tab or rewritten/truncated saved history is rejected. Export an unsaved conflicting branch before resolving it; this release intentionally does not silently merge or overwrite divergent histories.

Browser storage belongs to that browser/origin and can be lost. Export workspace JSON for portability and verify against this exact base dataset:

```bash
node apps/public-strategy-atlas/verify-workspace.cjs WORKSPACE.json [sha256:EXPECTED_CHECKPOINT]
node apps/public-strategy-atlas/workspace.test.cjs
```

Imports are bounded at 2 MB / 500 revisions, validate the base dataset, version/event chains and allowed annotation fields, and reject unsupported signature claims and official-status promotion. The exported base snapshot, source-admission receipt and local workspace are separate artifacts with distinct verification contracts.

At overview zoom, an unscaled row of readable content labels opens the full-size inspector. Public observations are blue, unaudited hypotheses dashed, active local annotations purple, contested ones dashed amber and retracted local views grey/dashed. Prior versions are labelled SUPERSEDED_HISTORY without rewriting the stored revisions. See `qa/ADMISSION_WORKSPACE_RESULTS.md` for actual tests and limits.

## Default route-first experience — Founder V1.4

`index.html` is now the actual route-map application, not a link to a separate visual experiment. Two continuous synthetic corridors, circular stations, branches and explicit amber hypothesis connections occupy the main viewport. `atlas-route-layout.js` is a deterministic display projection of the existing AtlasData nodes/edges, not a parallel data model. The older route-map-preview.html is retained as a historical experiment.

Select a station for its contextual slide-over; use **Follow route**, **Explore inside** or **Compare paths**. Internal content becomes a station sub-route, preserving the existing 127 records and receipts. **Back to route map** restores the prior route selection, zoom and pan. Connections are keyboard-selectable and open their real typed assertion IDs. Candidate links remain HYPOTHESIS_ONLY and can be hidden again.

**Tools & views** contains sources/admission, local workspace/history, audit, portable snapshot export, a linear **Text route guide**, progress semantics and synthetic density fixtures. The inspector is closed initially. On a 390px viewport it becomes a scrollable bottom sheet with bounded keyboard focus and Escape-to-station return. Arrow-key scroll, mouse dragging on map background, native touch scrolling, zoom and a pan guide expose offscreen routes. Physical touch hardware is not certified by the browser tests.

Default lines indicate category only, not progress. Explicit demo review/demo time modes use a separate white fill and conspicuous SYNTHETIC DEMO explanation; actual KPI stays UNKNOWN with no progress fill. Public observations and local annotation states are visually distinct; local revision markers never confer Council authority.

60/200-item fixtures now start with progressive branches at 100% zoom. Search can focus a bounded ancestor corridor for deep items; normal labels remain 14px before optional zoom. This is bounded synthetic route acceptance, not full real-corpus or ultrawide accessibility certification.

Executed acceptance and screenshots: `qa/ROUTE_FIRST_RESULTS.md`. Additional production projection test: `node apps/public-strategy-atlas/route-main.test.cjs`; the older `route-map.test.cjs` still tests only the historical preview. All previous model/content/workspace tests remain required.
