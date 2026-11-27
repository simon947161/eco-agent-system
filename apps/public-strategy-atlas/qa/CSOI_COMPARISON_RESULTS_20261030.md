# V1.7 retained-record comparison checkpoint — PARTIAL system acceptance

This batch continues COI-074 from remote `94234d3a2f7eb6cc32733e1afed227d083452d28`. It delivers a real `/#/compare` workspace, recorded-law/work filters and source/object entry links using the existing AtlasExecution registry. It does not add a parallel graph, edit a record, create a relationship, calculate a variance or grant official authority.

## Executable behavior

Users can select two retained stations, content records, domain entities/assertions or source records from different branches, inspect exact revisions, compare typed facts and follow source/strategy context. The page provides revision-pinned permalinks, independent companions and a stacked mobile layout. Suggestions are bounded to 200 public IDs; exact retained IDs remain directly selectable.

`AtlasExecution.compareRecords()` verifies and clones the snapshot before resolving either record. Historical domain revisions must match the requested logical identity and hash. A missing pin never silently resolves to today's record. Legacy records use canonical payload digests for comparison pins; their declared version labels remain separate metadata. A reused label on changed legacy content fails the old digest pin. Malformed, duplicate or empty URL revision pins are rejected instead of being discarded.

The result shows MATCH / CONFLICT / UNKNOWN for identity, source, region, boundary, spatial grain, recorded period, unit, stock/flow/rate nature, denominator, observed/target/execution role, financial role, currency basis, cost class and applicable legal roles. Equal missing values do not establish compatibility. Zero/negative and unsupported structured denominators stay UNKNOWN; zero observation values remain zero. `AUD/ML` rates retain financial basis/cost semantics. Actual calendar `executionStatus` distinguishes planned research from recorded execution, without inferring an achieved outcome.

Privacy screening includes nested classification, security, privacy, permission and confidentiality markers, PII, self-claimed releases and hidden original-body fields. Text renders through DOM `textContent`. Arithmetic remains `NOT_PERFORMED`, `arithmeticAllowed:false`; official relationships remain UNKNOWN. Metadata matches do not authorise a calculation, establish equivalence/causation or determine legal applicability.

Recorded-law and work filters search the available reference text, IDs and types, alongside existing year/region/source/domain/unit/state filters. Unknown scope is excluded when a scope filter is requested. A textual law match is not a current-law applicability check. Source corpus, legal consolidation and human review remain independently incomplete.

## Actual verification

| Check | Result | Evidence |
| --- | --- | --- |
| Complete native files | PASS, 31/31 | `csoi/native-comparison.json`, `native-comparison.log` |
| Comparison adversarial groups | PASS, 12 groups plus invariant checks | `comparison.test.cjs`: current/historical pins; missing/wrong/tampered pins; legacy digest pins; no dataset mutation; privacy/body guards; unknown/zero/structured denominators; percent, currency-rate, period/region, target/actual/task and legal-role conflicts |
| Router/filter negatives | PASS | `csoi-router.test.cjs`: allowed recorded-law/work filters; malformed/duplicate pins; unsafe identities; no current-version substitution |
| Real comparison browser | PASS, desktop/mobile | `csoi/browser-comparison.json`: actual Bombala/Cooma source revisions, exact permalink and companion, missing/malformed pin rejection, budget/expenditure types, real OP planned-volume boundary, law/work filters |
| Navigation/responsive regression | PASS, 23 pages × five viewports | Latest `csoi/browser-h.json`: 390×844, 1440×900, 1600×900, 2560×1080 and 3840×1080; keyboard focus, reload/back/forward, HTML rejection, touch emulation and companions |
| Affected real source pages | PASS, desktop/mobile | `csoi/browser-source-extension.json`, `browser-b.json`: directory→original→note, geographic/revision conflicts, planning facts, source/filter/coverage and companion checks |
| Loaded-module Node coverage | PASS: 91.28% lines / 84.74% branches / 95.06% functions | `csoi/coverage-comparison.txt`; scope is loaded `atlas-*.js` / `csoi-*.js`, not browser renderer or command-tool coverage |
| PR state | Draft observed, read-only | `csoi/pr130-draft-readback.json`: public Draft icon and visible label; no PR state mutation |
| Physical/cross-browser/professional assistive technology | NOT_TESTED | Chromium emulation is not hardware or professional certification |

Screenshots: `csoi/comparison-source-1440.png`, `comparison-source-390.png`. Native tests independently confirm the dataset digest is unchanged by comparison. The current default dataset remains `sha256:4023b091396d03acf391be78d2b2148bfc825651519a1114cd5ed129d9cff62a`, including the original 15 stations / 127 items, 59 domain entities and 48 assertions.

## Separate acceptance and continuation

**Software/system PARTIAL; public corpus PARTIAL; official admission PENDING.** Task counts remain 49 VERIFIED / 28 PARTIAL / 3 BLOCKED. COI-074 gains verified two-record comparison and recorded-law/work filters, but stays PARTIAL for complete source-backed obligation indexing and full path-set comparison. No full task or complete-system acceptance is inferred from these tests.

Source coverage is unchanged by this software batch: **51 records / 31 families, 32 successful byte receipts (12 PDF / 20 HTML), 24 own research notes across 22 sources and five published OP planning records**. There are 25 retrieved document revisions, seven retrieved directories and 17 unresolved requirements; complete inventory coverage is UNKNOWN. Eight source-reported candidates remain pending; official admitted documents/relationships, catalogue extraction/current-version/reuse approval remain zero. Actual spending, delivery, compliance and environmental outcomes stay UNKNOWN.

The next executable public batch is exact Snowy River DCP original intake and legitimately permitted chapter/work-item structuring, then obligation/path-set indexing with source and applicability review gates. The large Jindabyne lead needs an explicitly bounded transfer path. Do not retry known statutory 403 responses repeatedly or bypass restrictions. Private WCOS compatibility remains blocked without its independently authorised contract/environment. Keep Draft PR #130: no deployment, merge, main/PR129 change, paid service or Council nonpublic data.
