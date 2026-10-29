# Atlas — authoritative continuation checkpoint

Date: 2026-10-29 Australia/Sydney.
Status: M1_A_BYTE_ANCHOR_PASS_ADMISSION_PENDING / M1_B_LOCAL_REVISIONS_BROWSER_PASS / M2_READABILITY_EXTENDED / NOT_DEPLOYED.
Repository: simon947161/eco-agent-system.
Only remote engineering branch: feature/public-strategy-atlas-web-mvp-20261029.
Draft PR130: no merge. Read its latest engineering continuation comment too.

## Founder V1.5 — quantified goal-to-work logic takes priority over additional visual polish

**Founder direction (2026-10-29):** The routes must encode the *real reasoning and work* beneath CSP and LSPS: each goal's decomposed work packages, spatial applicability, physical work volumes, staffing/resources, financing/budget vs actual spend, measurable outputs, regional environmental/economic outcomes, published evidence and review state. A pretty graph without supported accounting logic is insufficient. The new **[V1.5 Strategy-to-Work & Accounting Directive](../../docs/research/public-strategy-atlas/FOUNDER_V1_5_STRATEGY_TO_QUANTIFIED_WORK_AND_ACCOUNTING_20261029.md)** becomes highest priority for domain modelling and first official/unknown evidence pathways. V1.4 route-first remains the required presentation: **real data and work semantics before decoration, then render those semantics as routes and drill-downs**.

**Crucial verified correction:** CSP 2035 p.30 reports `CO2e emissions per capita = 29.9 tonnes`, sourced to `Snapshot Climate — Australian Emissions Profiles 2021–22`, desired trend `Decrease`. It means **29.9 t CO2e/person**, NOT `AUD 29.9/t`, a carbon credit price, an annual Council-operational emission rate, or a measured carbon saving. Source: `https://www.snowymonaro.nsw.gov.au/files/assets/public/v/4/council/ipr/csp/smrc-csp-2035-endorsed-20250501.pdf`. Preserve time/region/denominator/boundary and admission status; no formal new mapping is automatically granted.

**Next engineering action, in order:** (1) recheck remote PR HEAD; (2) bounded source-to-work/physical/financial crosswalk for environment-carbon, water/wastewater, land-use/economy; (3) implement dimensionally validated work/metric/resource/financial/review objects in **existing** Atlas model, with one real `PUBLIC_TEXT_OBSERVED` anchor and explicit UNKNOWNs; (4) add route-first station/edge breakdown and accounting inspector; (5) test/capture browser QA, save actual findings and push. Avoid a research-only report or a second graph. Current V1.4 preview and earlier code are not invalidated.

## Founder V1.4 route-first correction — highest UI priority (2026-10-29)

Founder examined `qa/workspace-desktop.jpg` and rejected the *three-column management-dashboard experience* as the principal Atlas metaphor. The core product must be a **route/line map of knowledge modules and logic**: strategic/planning spines, branching stops, visible and hidden intersections, and auditable evidence behind every connection. The editor/history/sidebar become contextual tools, not the main composition. This **does not invalidate the byte-backed CSP 6.1, local editing, two-tab conflict, 127 recursive items, or verified tests**.

- Authoritative new implementation direction: `docs/research/public-strategy-atlas/FOUNDER_UX_V1_4_ROUTE_FIRST_DIRECTIVE_20261029.md`.
- Actual exploratory code: `apps/public-strategy-atlas/route-map-preview.html`, linked from `index.html`. It imports the existing `atlas-data.js` (no parallel source dataset), draws two spatially separated route corridors, toggles the two candidate links, selects stations, gives contextual details and zoom controls. **Prototype only; not yet the default Atlas main view.**
- New `route-map.test.cjs` supplies deterministic mock-DOM regression. Connector-executed JS syntax and mock-DOM initialization/selection/candidate/filter checks PASS; **actual route preview browser/screenshot QA NOT_TESTED** at this checkpoint.
- **Next FIRST task:** implement V1.4 U1 route-first as **the actual main index page** using existing model/evidence/history editor APIs, with station→six-level-content drill-down, typed-edge inspection, optional slide-over rather than full-time sidebars, keyboard/text alternative, 1440×900 and 390px Chrome visual QA. Then U2 audit/history overlays, U3 60/200 route density. Run previous tests and preserve M1 admission gates. **Do not return another study-only deliverable.**
- Keep Draft PR #130 and the only engineering branch. Commit+push and read remote HEAD on completion. Do not merge, deploy, purchase, or access Council internal material.

## Baseline and durable handoff

Started from remote 3024a6acf597602167be8a19bead200df9dd821c and PR130 continuation comment 6491788231. Existing English recursive explorer (15 topics / 127 internal items) retained, not rebuilt. Work used an isolated local checkout branch at that remote parent without resetting research history. This file is inside the current commit; determine actual HEAD from GitHub and verify remote readback, not a self-written hash. No background execution is running.

## Implemented and actually verified

- CSP 6.1 official summary fetched as actual PDF bytes, SHA-256 verified, rendered/visually inspected and extracted using a bounded page-1 word-origin anchor. Receipt/short excerpt: sources/csp61-admission.json and tested classic-script mirror. Original PDF/page image not redistributed because reuse permission is unknown. verify-source.py reproduces the byte/anchor checks with a separately obtained PDF.
- Admission stages stay distinct. Observation/bytes/extraction PASS. Official current revision, reuse permission, legal effective scope and identified human approval remain incomplete; ADMISSION_PENDING_REVIEW, not ADMITTED. No CSP→DP/OP mapping; official graph assertions still 0.
- Local annotation editor with before/after version comparisons; immutable CORRECT/SUPERSEDE/CONTEST/RETRACT/REVERT revisions and linked correction events; target-head optimistic conflict, replay and child-linked local subtree receipts. Original source content/status never changes.
- Explicit local IndexedDB Save/Load, portable JSON import/export and independent verifier. Atomic stored-head/prefix checks reject stale tabs or overwritten/truncated history. Actual two-tab conflict test passed. No silent persistence/restoration/upload. Imported/saved annotations remain LOCAL_ANNOTATION.
- Overview labels remain 13px independent of graph zoom; observed public nodes blue, local active/contested/retracted markers distinct. History links source anchors and shows projected SUPERSEDED_HISTORY without mutating earlier versions.
- Actual desktop/390px iframe, real export/download/import and 60/200 fixtures rechecked. Details and screenshots: qa/ADMISSION_WORKSPACE_RESULTS.md.

## Run and verify

Website directory: python -m http.server 8877 --bind 127.0.0.1; open http://127.0.0.1:8877/.
Repository root:
- node apps/public-strategy-atlas/model.test.cjs
- node apps/public-strategy-atlas/content.test.cjs
- node apps/public-strategy-atlas/workspace.test.cjs
- python apps/public-strategy-atlas/verify-source.py OFFICIAL_PDF
- node apps/public-strategy-atlas/verify-workspace.cjs WORKSPACE_JSON [sha256:CHECKPOINT]
- node apps/public-strategy-atlas/audit-cli.cjs

All described tests actually ran; altered source bytes and unsupported signature/hash/promotion cases rejected. Source Python checker requires pdfplumber already present here; website adds no installed dependency. Direct-file source/browser persistence may differ by browser; HTTP tested. QA local saved workspaces are synthetic test data in the browser, not GitHub business records.

## Next executable work

1. Obtain/record an explicit permitted reuse basis and independent human review of current adopted-version equivalence/geographic/effective scope for this exact PDF digest. Keep unknown gates pending until evidence exists. The UI does not issue approvals/signatures.
2. Implement a deliberate divergent-workspace reconciliation preview (three-way base/local/import diffs) that appends resolutions without replacing retained histories. Current conflict handling rejects divergent overwrite and asks the user to preserve/export unsaved work; no automatic merge.
3. Continue keyboard/screen-reader acceptance and real-corpus readability checks; do not reinterpret synthetic density fixtures as official-content completeness.

## Limitations and boundaries

The full authoritative system is not complete. No admitted official relation, actual KPI, server collaboration, independent witness or official cryptographic signature. A privileged writer can rewrite a whole unsigned history; retain external checkpoints for stronger comparison. Browser storage can be lost; export explicitly. Full physical-mobile/Safari/Firefox/WCAG acceptance untested. Original R0-K LOCAL_UNAVAILABLE remains unchanged.

Public/synthetic only. No Council nonpublic records, employer/internal accounts or systems, personal cases, new procurement, deployment, PR129/main changes or merge. One remote writer at a time. Each verified stage: checks/privacy review, commit/push to the only remote branch, update this checkpoint and remotely verify HEAD. If sync fails, record SYNC_BLOCKED. Do not save the only handoff in Work scratch.
