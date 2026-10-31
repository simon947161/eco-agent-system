# ClimateOS Public Strategy Atlas

A route-first, local research application for exploring strategy, work, quantities, sources and audit history. It extends the original 15 stations and 127 content records. No package installation, backend, paid API or production deployment is required.

**V1.7 system acceptance: PARTIAL.** All eight engineering packs have executable public/synthetic capabilities over the existing Atlas registry. The recovered authoritative 80-task handoff is tracked in [the task registry](COI_TASK_REGISTRY_V1_7.json); VERIFIED applies only to the stated code/test scope. Current source coverage has 33 successful original-byte receipts across 52 catalogue records, with 25 attributed research notes and five published planning records. Source rights, current legal versions, complete corpus coverage and authorised admission remain pending. No official relationship, Council expenditure, achieved outcome or parcel-level legal applicability is admitted. See [the acceptance report](qa/CSOI_V1_7_SYSTEM_RESULTS.md), [the subsequent source batch](qa/CSOI_PUBLIC_SOURCE_EXTENSION_20261030.md), [NEXT_SESSION.md](NEXT_SESSION.md) and the [V1.6 taskbook](../../docs/research/public-strategy-atlas/FOUNDER_V1_6_COMPLETE_SYSTEM_BUILD_MASTER_TASKBOOK_20261029.md).

## Run

```sh
cd apps/public-strategy-atlas
python3 -m http.server 8877 --bind 127.0.0.1
```

Use a browser against the local server. Scripts are classic scripts and have no external runtime calls. Services must restart in a new task; live browser storage and processes are not durable GitHub delivery.

The route map stays the homepage. The navigation menu opens bookmarkable hash routes such as `/#/strategy/csp`, `/#/domains/phe/food`, `/#/domains/wcos/ltw`, `/#/calendar`, `/#/metrics`, `/#/sources` and `/#/compare`. Companion windows use independent public state and `noopener`; unsaved edits are transferred only through an explicitly verified snapshot import.

The Snowy River, Cooma-Monaro and Bombala DCP dossiers expose 72 source-pinned authored observations (30 Snowy / 25 Cooma / 17 Bombala), with conditions, exceptions, parent revisions and real five/eight-level evidence paths. Bombala retains its 2012 cover versus 2014 directory label, historical date conflicts and discontinuous printed page numbers. Three earlier historical 110/90/40 L/person/day design references remain separate from actual water demand, current law and admitted calculation inputs.

For the latest complete research flow, use **Pages → PHE knowledge → On-site sewage**, or `/#/domains/phe/ossm`. Six curated Snowy/Cooma reading cards open exact source/page evidence, historical clauses, a user-chosen review date, independent work cards and the Annual Calendar. Source withdrawal removes the affected new-review links while retaining historical plans; current statutory/operational linkage stays UNKNOWN. See [this batch's evidence and screenshots](qa/CSOI_PHE_BOMBALA_RESULTS_20261031.md).

An owner-private trial is now published at https://council-strategy-intelligence.minshu.chatgpt.site. Open it with the owning ChatGPT account. Sites access is custom with only the owner allowed, no editors/groups/external visitors. The earlier loopback address works only on the computer running its server. See `qa/PRIVATE_TRIAL_DEPLOYMENT_20261031.md` for deployment and verification limits.

V1.7 workspaces include public PHE source/condition chains; read-only synthetic WCOS contracts; L0–L5 lineage with independent calculation replay and source-withdrawal invalidation; service-specific workload/resource denominators; calendar/fiscal Annual Editions down to task/brief/evidence/follow-up/report; and draft-only Michele weekly/meeting preparation. Calendar/task/draft retention appends immutable revisions in the same registry. Outlook actions and formal Council decisions are disabled. The original private WCOS contract remains unavailable; no production compatibility is claimed.

## Working flows

- The route map remains primary. Select stations/connections, follow routes, open content, use the text alternative or minimap, and return without replacing the original graph.
- Every station has a **Knowledge & work dossier**. Registered entities expose typed upstream/downstream links, exact revisions, scope, data, provenance, gaps and history. Other stations explicitly report missing work/quantity/finance/evidence rather than imply completion.
- **Work breakdown & dependencies** traverses the same registry. Water/land programs, projects, tasks, roles, assets and deliverables are explicitly synthetic proposals; execution and evidence states are independent.
- **Three-ledger calculations** produces physical/environmental, financial/resource and results/evidence receipts. Inputs are revision-pinned and independently recomputed. Changed inputs invalidate current use while historical results remain auditable. Budgets are not expenditure; rates, stocks and flows are not interchangeable.
- The public carbon marker remains **29.9 t CO2e/person**, Snapshot Climate 2021–22, CSP printed p.30, desired trend decrease, `PUBLIC_TEXT_OBSERVED`/PENDING. It is not a price, Council operational inventory, proven CSP6.1→DP/OP relation or achieved reduction. Extrapolation from this unadmitted input is rejected.
- **Where & when** checks exact area, spatial grain, effective dates, source revision and legal role. Explicit synthetic wrong-region/draft/expired cases are rejected. A scope match is not legal approval. No actual GIS polygon/parcel determination is supplied.
- **Discovery & challenge** generates explainable candidates with signals, paths, alternatives, falsifiers and counterevidence. Local question/review records are versioned. `KNOWN_LINK` stays UNKNOWN without configured official admission; similarity never grants authority.
- Header search and **Search & questions** cover original content, work, quantities/units, source records and local research. Type/region/as-of filters, unknown-scope labels and result pages are explicit.
- **Coverage & source gaps** separates software tasks, public corpus, relationship review, data quality and actual outcome KPIs. The active catalogue extends the immutable original requirements with source receipts and pending statutory leads. Complete inventory coverage and actual Council KPIs stay UNKNOWN; formal source extraction, current-version confirmation and official admission remain zero.
- **Audit & receipts** shows paged base/domain/source events and field-level revision differences. No digest is an official signature, independent witness, legal opinion or proof of semantic truth.

## Content capacity and tables

Content uses indexed iterative validation/traversal/hashing/layout, not a fixed six-level schema. Source-backed leaves can have no children. Safety limits remain 100,000 content records, 200 default visible stops (500 explicit model maximum), child pages and bounded query output. Legacy receipt values remain exact. Above 128 levels, receipts use flat transport to avoid JSON/canonical stack overflow.

The UI supports 60/200/1,000/10,000-item synthetic fixtures. `?fixture=1000&shape=chain` exercises deep navigation; `?fixture=1000&table=1` exercises paginated structured tables retaining captions, column units, fiscal basis and footnotes. Native tests verify a 5,000-level chain and 10,000-item breadth. These test capacity, not public corpus completeness.

## Local editing, conflicts and portability

Original source records remain unchanged. Content annotations use the legacy immutable AtlasWorkspace; synthetic quantities use separate domain revisions. Domain challenges/questions/calculations are retained by explicit snapshot export/import. Nothing uploads, saves or restores automatically.

Workspace **Save locally / Load saved workspace** uses atomic IndexedDB expected-checkpoint and append-prefix checks. Divergent import opens BASE/LOCAL/IMPORT field choices and requires a reason. RESOLVE events append and exact imported histories are archived. The bounded format supports 2 MB, 500 primary revisions, 20 archives, nesting depth 5. Storage can be lost; export explicitly. No remote collaboration or silent merge is claimed.

**Export snapshot** includes the original base plus typed domain records, revision/event history, calculations, source catalogue and content roots. **Compare & import snapshot** verifies integrity, optional independent checkpoint and exact legacy base before explicit domain replacement. Export current state before replacing it. Legacy snapshots/workspaces remain supported.

```sh
node apps/public-strategy-atlas/verify-snapshot.cjs SNAPSHOT.json [sha256:checkpoint]
node apps/public-strategy-atlas/verify-workspace.cjs WORKSPACE.json [sha256:checkpoint]
node apps/public-strategy-atlas/verify-intake.cjs CATALOGUE.json [sha256:checkpoint]
python3 apps/public-strategy-atlas/verify-source.py OFFICIAL_SUMMARY.pdf
```

The last command needs `pdfplumber` and the separately obtained original PDF. No restricted full PDF is redistributed. The latest [runtime recovery](qa/NEW_RUNTIME_ACCESS_RECOVERY_20261030.md) records a successful original-byte/page-anchor check; that QA observation has not been promoted into catalogue admission. Public availability is not a redistribution licence.

`tools/csoi-append-receipts.cjs TEMP_BATCH.json` dry-runs an offline public-source append; `--apply` writes only after all proposed receipts validate. The command rehashes originals under `/tmp`, checks a pinned retrieved discovery directory, closes/bounds retained metadata and preserves exact source/event/observation prefixes. It rejects body/excerpt fields, private or signed URLs and caller rights/approval promotion. It performs no network request and never commits original bodies. Discovery-directory links in source pages are separate from legal or strategic relationships.

The **Compare** page reads two retained records from any registered branch, pins their exact revisions and shows typed scope/provenance/quantity/finance differences. Missing or malformed pins fail. Legacy declared version labels stay metadata; their comparison pins use payload digests. Percent denominators, financial rates, task execution states and legal-role conflicts remain distinct. Unknown/zero/unsupported structured denominators stay UNKNOWN. Comparison performs no arithmetic, merge, admission or data mutation. Source and object dossiers link directly to this page; recorded-law/work filters search available metadata rather than claim current legal applicability.

## Repeatable verification

From repository root:

```sh
node apps/public-strategy-atlas/run-tests.cjs /tmp/atlas-native.json
node --test --experimental-test-coverage --test-coverage-include='apps/public-strategy-atlas/atlas-*.js' --test-coverage-include='apps/public-strategy-atlas/csoi-*.js' apps/public-strategy-atlas/*.test.cjs
python3 apps/public-strategy-atlas/qa/run-local-browser.py run-browser-suite.py csoi-browser.py csoi-source-browser.py csoi-corpus-browser.py csoi-compare-browser.py csoi-layer-browser.py csoi-wcos-browser.py csoi-phe-browser.py csoi-work-browser.py csoi-calendar-browser.py
```

Browser tests require engineering Python Playwright and system Chromium. The harness runs a temporary localhost server for the suite lifetime. These are not app dependencies. Actual results, screenshots, runtime versions, coverage, limits and acceptance verdicts are recorded under `qa/`. Node coverage measures loaded modules and is not browser rendering coverage. Mock-DOM historical preview tests are labelled separately from real Chromium acceptance. Full professional screen-reader/WCAG, physical touch and cross-browser certification are not claimed.

Startup reads a generated default snapshot of the same registry and immutable history, verifies its input digest, complete snapshot and original base, then clones it for use. This avoids rebuilding every default research record on every page load. A stale or corrupt cache is rejected; exports/imports use the existing formats. After changing source assets or default registration code, rebuild with `node apps/public-strategy-atlas/tools/build-csoi-boot.cjs`. The native cache test compares the result with full registration, including an exact synthetic-fixture comparison.

All work remains on `feature/public-strategy-atlas-web-mvp-20261029`, Draft PR #130. The owner-private Sites trial is deployed separately; no merge, main/PR129 change, purchases, Council nonpublic records or government endorsement.

The **Typed path-set comparison** at `/#/compare/paths` reads existing assertions and governed input lineage. It independently pins all nodes/relationships, retains evidence/counterevidence and distinguishes current input pins from unreviewed law/admission. Source withdrawal invalidates current use while historical proofs remain reproducible. Export proof JSON explicitly; verify with `node verify-paths.cjs SNAPSHOT.json PATH_COMPARISON.json`. No arithmetic or official route is admitted.

Independent public source review now connects a DCP clause to a user-dated research Task and the existing Annual Calendar. Planned review hours are explicitly ASSUMED; actual hours, spend and outcomes remain UNKNOWN. The same source/clause revision pins travel through work cards, calendar navigation, path comparison and exported snapshots. No Council assignment is created. See `qa/CSOI_REVIEW_CALENDAR_RESULTS_20261030.md`.

The second DCP outline retains Cooma cover/footer, body-amendment and resolution conflicts. Independently pinned Cooma/Snowy source paths report geographic conflict, unknown admission and no arithmetic. Both feed the existing independent review/calendar flow. See `qa/CSOI_COOMA_RESULTS_20261030.md`.
