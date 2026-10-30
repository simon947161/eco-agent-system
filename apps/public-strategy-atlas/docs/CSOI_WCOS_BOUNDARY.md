# WCOS abstract bridge and research work accounting

The bridge is an independently authored, read-only **plan-level interface**. No private WCOS repository, Council record, Outlook account, actual roster or internal technical contract was read, cloned, copied, modified or contacted. The private professional system remains the authority for its own operational records. There is no sync implementation in these modules.

COI-002 (original WCOS inventory), COI-031 (mapping to an authorised original WCOS technical contract), and COI-040 (non-destructive original WCOS/Outlook compatibility rehearsal) remain **BLOCKED: authorised technical contracts and a permitted test environment were not supplied**. The synthetic interface tests do not verify compatibility with the original WCOS.

## Executable interfaces

`csoi-wcos.js` exposes `AtlasCSOIWcos` (alias `CsoiWcos`). `syntheticFixture()` returns the authored Mission → Operating Year → Quarter → Month → Week → Day → Task → Premises → Field Brief → Execution → Follow-up → Annual Report concept chain. `adapt()` accepts that exact authored fixture, or strict public-rule metadata only when a caller-supplied trusted source verifier approves it. An arbitrary payload carrying a synthetic flag is rejected. Public-source review callbacks are a trusted host boundary, not evidence supplied by an imported record.

The adapter rejects writes, personal/private, Council-protected, unknown and self-claimed approved-release classifications. It does not accept customer, address, account, employee or credential fields. Existing non-identifying public metadata can be connected by the host after provenance verification. Real business-record aggregation is denied entirely; small samples are not released. Synthetic fixture summaries are explicitly labelled and never report Council KPIs.

`conditionalServices()` evaluates independent factual conditions for Food, LTW and Backflow research pathways. A restaurant or property name does not grant or require three approvals. Unknown discharge, sewer connection, device or activity facts remain UNKNOWN. `ltwWorkflow()` provides ten proposed research stages, including classification, approval/concurrence evidence, pretreatment, monitoring, rectification, reinspection and reporting. It is not a Council SOP and does not assign A/B/C/S classifications or an accountable officer.

`backflowDue()` requires a known testable device type, valid last-test date and explicitly applicable interval. A synthetic device/rule can rehearse scheduling, including leap-day anniversaries. A public rule must match the independently compiled `CsoiPhe.backflowRule()` and pass current-version, anchor and scope gates; self-asserted flags cannot establish a current legal obligation. The Council public page's annual-testing wording for installed testable devices does not create a blanket annual rule for every property or establish official compliance. Missing effective-version evidence remains UNKNOWN.

`judgment()` keeps RULE, EVIDENCE_INFERENCE, DISCRETION and FORMAL_DECISION distinct. Formal decisions are blocked, and every other output requires human review. No signature, government approval, concurrence, statutory conclusion or Council workflow authorisation is issued.

## Work and resource accounting

`csoi-work.js` exposes `AtlasCSOIWork` (alias `CsoiWork`). Its default `syntheticFixture()` contains five regulatory objects across two fictional properties, two proposed tasks, six effort phases and a labelled annual productive-hours assumption. It contains no names, addresses or real case data.

`coverage(items, asOf)` deduplicates by service + entity type + entity ID. It separately reports registered objects, approval-required/unknown, known eligible, planned, completed requirements, overdue, unknown eligibility/requirements, due devices, distinct inspection events and open/closed issues. One property can contain several business activities, discharge activities and devices; these denominators are not interchangeable. Conflicting duplicate records, reused event IDs, future completions, missing evidence, mixed periods/regions and unsupported closure claims fail validation. Unknown requirements do not become zero visits. Inspection coverage and issue closure never imply compliance, risk elimination or environmental outcomes.

`workload()` retains preparation, field, travel, documentation, reinspection and administration hours, with ESTIMATED, MEASURED and ASSUMED totals separated. Missing phases stay UNKNOWN. `resources()` provides skill counts, vehicle/training/facility hours and capacity-scenario FTE equivalents only when the caller supplies a positive annual productive-hours basis. It does not create headcount, appointments, rosters, budget or actual expenditure.

`ledgerSummary()`, `derive()`, `verifyDerivation()` and `reverseTrace()` reuse the existing AtlasModel and AtlasExecution identities, measurement rules and content-addressed input revisions. The existing public-observed 29.9 t CO2e/person remains a regional per-capita observation, not a carbon price, total Council inventory or achieved reduction. The 12 ML/AUD24,000 water and 50 ha land cases remain synthetic. Unsupported strategy mappings stop at UNKNOWN.

`receipt()` binds permitted input versions to a SHA-256 input digest and self-attested receipt. `verifyReceipt()` detects corruption and reports STALE_INPUT_RECALCULATE when inputs change. These are local integrity checks, not independent signatures or semantic attestations. Protected/private classifications and sensitive fields are rejected before receipt creation.

## Validation

Run from the repository root:

```
node apps/public-strategy-atlas/csoi-wcos.test.cjs
node apps/public-strategy-atlas/csoi-work.test.cjs
```

The native suites cover conditional service negative cases, forged permissions, public-metadata gates, LTW decision boundaries, backflow date/interval/scope checks, duplicate denominators/events, evidence and closure gates, unknown values, effort/resource separation, mixed-scope rejection, source-aware reverse traces, input invalidation, and inherited unit/accounting counterexamples. Browser integration and original private WCOS compatibility are distinct acceptance steps; neither is established by these native tests.
