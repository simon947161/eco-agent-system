# Atlas data, revision and trust contract

## Original base and additive migration

`AtlasData` remains unchanged: `atlas-1`, 15 synthetic strategy/planning stations, 127 internal records and separately labelled observations. Its frozen digest is `sha256:13e765c81f1340918322b1e985da85f2362da3c72e1997804f952865edf365d2`.

`await AtlasModel.migrateDataset(base, AtlasAccounting.cases, catalogue)` returns an additive `domain` registry. `legacyBase` strips only that registry so original workspaces and source receipts keep their base identity. Density fixtures have their own different base identity. Migration is deterministic/idempotent; it does not modify the original source object.

`domain.format = atlas-domain-1`, `algorithmVersion = atlas-domain-sha256-1`. Entities bind existing station IDs. Typed semantic assertions extend the existing model and can have multiple parents/cycles. Containment is separately acyclic. There is no second route graph.

## Identities and immutable history

- Legacy content logical/version labels are preserved. Canonical item and child-linked subtree digests provide their content identity; a declared version label alone is not cryptographic proof.
- Domain entities/assertions carry stable `id`, kind/predicate, station, classification, research state, admission boundary, scope, data, provenance/gaps and `revisionId`.
- A domain revision hashes `{logicalId, parentRevision, record}`; parent links refer to earlier revisions of the same object. Entity heads match their exact revision payload.
- Every domain revision is bound to a linked AtlasModel change event. Snapshot audit checks revision/event integrity, endpoints, all referenced input versions and optional source catalogue.
- Assertions pin both endpoint revisions, predicate, method, scope, issuer/reviewer, support and counterevidence. A pinned old revision remains historical rather than silently rewritten to today's record.
- `canonical` is sorted-key JSON with ordered arrays, finite numbers and UTF-8; it is not claimed RFC canonicalisation. SHA-256 uses Web Crypto or the offline fallback. An editable whole chain can be replaced without an independently retained checkpoint.

## Type and authority boundaries

The extensible vocabulary includes strategy/policy, work/project/task/dependency, area/asset/role/resource, observation/metric/baseline/target/output/outcome, finance/allocation, source/evidence, hypothesis/review and audit receipt families. Runtime validation covers identities, references, supported classes/states, financial/quantity basics and provenance; this is not a complete regulatory ontology or legal validation system.

Classes: `SYNTHETIC_SCENARIO`, `PUBLIC_TEXT_OBSERVED`, `LOCAL_RESEARCH`. Research states include PROPOSED, SOURCE_OBSERVED, IN_REVIEW, APPROVED_FOR_RESEARCH, CONTESTED, SUPERSEDED, RETRACTED and UNKNOWN. `APPROVED_FOR_RESEARCH` is never Council approval. Admission is PENDING or NOT_APPLICABLE; official promotion is unavailable without a separately authorised authority/review integration. Caller-supplied role strings cannot confer it.

`domainIndex`, `domainForStation`, `queryRelationships`, `commitDomainRevision`, `registerScenario`, `appendCalculation` and `recordResearchReview` operate on this registry. Numeric scenario edits are synthetic only; public observed values cannot be overwritten. Scenario/reference fixtures do not become actual financial/performance records through import.

## Content and structured tables

Content preserves parent/owner/revision/observation/status consistency. Duplicate identities, dangling parents, cycles, mixed source scope and unsupported official laundering are rejected. Validation, trails, subtree search, receipts and layouts are iterative. Safety bounds: 100,000 records; model layout maximum 500, UI default 200; child pages 50. Deep receipts use `atlas-content-receipt-flat-2` above 128 levels while retaining exact child-linked hashes. Legacy receipts are unchanged.

Tables retain caption, columns/units, rows, fiscal basis and footnotes inside the hashed item. Values are text/finite numbers and rendering escapes them. Table rows are paginated. Current table fixtures are synthetic; no unavailable official page/number is filled with generated text.

## Source catalogue and admission

`atlas-source-catalogue-1` includes family/publisher, exact known URL or discovery directory, rights/reuse basis, media type, raw digest when held, retrieval/adoption/effective/amendment/supersession/current-as-of fields, geography, parser/extraction/anchors, lineage, corroboration and access evidence. Missing values remain null/UNKNOWN. JSON/classic-script mirrors are equality tested.

`registerSource` appends a new immutable source/document revision and DISCOVERED event while retaining prior records/events; supersession lineage must point to earlier registered IDs. It does not overwrite the old document.

Intake states: DISCOVERED → DIRECTORY_OBSERVED → SOURCE_RETRIEVED → RAW_BYTES_VERIFIED → EXTRACTED → ANCHOR_VERIFIED → CURRENT_VERSION_AND_SCOPE_CHECKED → REVIEW_PENDING → ADMITTED. Gates are ordered; rights, raw/extraction/anchor digests and version/scope evidence are distinct. Corrections append downgrade events. Official ADMITTED is blocked without a configured independently authorised review mechanism. Source availability or local claims are not permission/authority.

`sourceStatus` and `sourceGaps` derive recorded availability and the next review action from replayed intake evidence. Retained SOURCE_RETRIEVED evidence reports AVAILABLE at its retrieval time, separately from immutable `historicalAccess`; it does not assert current live connectivity. A correction withdrawing retrieval reports NOT_CHECKED and requires a new check. Corrections above retrieval retain it. Rights and reviewer gaps remain separate, and synthetic sources can never receive official admission.

The original `public-catalogue.json` stays immutable at 15 requirements / 14 families. The active `csoi-catalogue.json` extends that same catalogue to 51 records / 31 families: 27 document revisions, seven directories and 17 requirements. Current receipts cover 25 retrieved documents plus seven directories (12 PDF / 20 HTML original-byte receipts). The 2024–25 annual report retry and subsequent nine-source DCP/Water AMP batch append after prior immutable records/events/observations. Prefix proofs are in `qa/csoi/annual-prefix-proof.json` and `source-extension-prefix-20261030.json`. There are no catalogue EXTRACTED, ANCHOR_VERIFIED, current-version-confirmed or ADMITTED documents. Full inventory denominator is UNKNOWN. The separately byte/page-anchor-verified CSP6.1 admission receipt remains immutable and pending. No original PDF/HTML source body is shipped; own bounded attributed research wording is not formal source extraction or a source reuse licence.

`csoi-intake.js` registers 24 own research notes and five OP p.27 planning records in the same domain registry. The food-program quantities 168 optimal, 84 funded and 84 target retain UNKNOWN volume units; the 98 percent priority service figure is a target with an UNKNOWN actual denominator. Fiscal planning context is 2026–27, not a legal effective period. Each record binds the reviewed OP raw digest and anchor digest. Eight source-reported research candidate edges remain PENDING; none establishes an official CSP implementation relationship. Published planning figures never become achieved outputs, expenditure or authorised calculation inputs.

The offline `tools/csoi-append-receipts.cjs` command accepts only bounded, closed metadata for queryless official-public Council URLs and rehashes temporary original bytes before appending. Retrieved-directory references are pinned by URL/digest. Record dates and rights are not inferred from a filename or observed adoption line: adopted/effective/current-as-of fields stay unset; observed revision wording and conflicts are separate. Source pages traverse observed directory hyperlinks without creating admitted legal or implementation assertions. Selected request-attempt counts are not total HTTP exchange counts; same-host redirects can add uninstrumented exchanges.

## V1.7 governed research and work capsules

The L0–L5 analytical layer is orthogonal to `PUBLIC`, `PERSONAL_PRIVATE`, `COUNCIL_PROTECTED` and `APPROVED_RELEASE`. Public export, display, import and summary require independent classification/rights/provenance screening; caller release flags cannot confer authority. Complete envelopes, including nested content and historical revisions, are checked. `AUTHORED_RESEARCH` covers only this application's own limited factual research wording. It grants no licence over original source bodies. See `docs/CSOI_CONTRACTS.md`.

Governed records retain stable logical IDs, content/revision digests, pinned input versions, scope, method, known gaps and immutable domain events. Independent L3 replay rejects re-signed false calculations; source withdrawal or current input revision changes invalidate downstream use without deleting historical evidence. Typed quantified mirrors must equal their governed measurement receipt.

Calendar and assistant capsules are public synthetic research only. Annual Edition projections support calendar/fiscal years, ISO weeks, leap days and multiple month/week parents. Task plans, briefs, execution/evidence/follow-up/report are distinct states. Caller-supplied statutory approval/assignment flags are rejected; actual obligations and manager agreement stay UNKNOWN. Retained plan/draft edits append revisions, require expected heads and do not change dates silently. Outlook/account writes, formal decisions and private WCOS ingestion are disabled. The source catalogue, tasks, research notes and accounting all remain in the original Atlas snapshot; no competing graph is introduced.

## Calculations, execution and scope

AtlasExecution uses the same identities for bounded forward/reverse/both paths, work breakdown/dependency order, search and candidate discovery. KNOWN_LINK returns UNKNOWN without authority-backed admitted assertions. Candidate signals/paths retain alternatives, falsifiers, rejection reasons and counterevidence; no confidence score becomes official proof.

`atlas-derivation-1` binds request/formula/method version, ordered input IDs and exact immutable revisions/provenance. Independent recomputation checks result and historical inputs. A current-head change yields INVALIDATED_INPUT_REVISION without destroying the old receipt. Receipts are versioned AuditReceipt entities and EVIDENCED_BY input assertions. Missing units/denominators, fiscal/boundary incompatibility, budget-as-spend, duplicate/unallocated costs and unsupported conversions fail closed. Real unadmitted inputs cannot be extrapolated; all current calculated verticals are synthetic. Results comparison is not causal attribution.

Spatial/effective-time indexes keep area/grain, effective dates, source revision and legal role separate. Historical as-of queries preserve conflicts. Missing scope is UNKNOWN; draft, expired, wrong-region/grain/revision/role are rejected. Matching synthetic metadata is SYNTHETIC_ONLY, not legal applicability. Actual polygons and official controls remain unavailable/unadmitted.

## Portable snapshots and local workspace

`atlas-public-snapshot-1` includes dataset, audit and recomputed content-root receipts, including the additive domain. Legacy and flat deep receipt transports verify independently; CLI/UI imports are bounded at 10 MB and can compare an external checkpoint. Same-base UI replacement requires explicit action; annotations are retained separately. A self-consistent supplied bundle is SELF_ATTESTED, RECEIPT_NOT_PRESENT, EXTERNAL_WITNESS_UNKNOWN.

`atlas-local-workspace-1` retains the original title/text-only annotation model, immutable revisions/events, source-item digests, replay, revert, contest/retract and expected-head checks. Optional mergeRecords archive exact imported workspaces with checkpoint-bound three-way previews/field choices. RESOLVE appends instead of rewriting histories. Archive/receipt/event corruption, stale previews, unsupported fields/signatures and official promotion are rejected. Limits: 2 MB total, 500 primary revisions, 20 archives, depth 5. IndexedDB saves are atomic and append-prefix guarded, including archives. No auto save/load/upload or remote sync.

Hashes prove supplied content integrity, not source rights, truth, official adoption, regulatory validity, outcome causation or independent witnessing. `NEXT_SESSION.md` and executed QA state which capabilities/corpus checks passed, were blocked or remain untested.
