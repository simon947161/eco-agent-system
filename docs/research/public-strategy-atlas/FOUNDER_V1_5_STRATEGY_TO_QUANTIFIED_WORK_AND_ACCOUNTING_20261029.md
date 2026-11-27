# ClimateOS Public Strategy Atlas — Founder V1.5: Strategy-to-Work, Spatial Logic & Quantified Accounting
**Issued:** 2026-10-29 Australia/Sydney  
**Status:** FOUNDER REPRIORITISATION / ACTUAL WEBSITE DEVELOPMENT AUTHORIZED / SOURCE-LED ENGINEERING  
**Repo:** `simon947161/eco-agent-system`  
**Sole engineering branch:** `feature/public-strategy-atlas-web-mvp-20261029` / Draft PR #130  
**Authoritative resume:** `apps/public-strategy-atlas/NEXT_SESSION.md`  
**Predecessors:** Founder V1.3 build/continuity, V1.4 route-first visual directive, V1.2 verifiable knowledge, V1.1 O2 organic layout. Preserve the completed English 127-item recursive explorer, local workspaces, hashes, source bytes/checkpoints, snapshots, edits, tests, candidate links, and UI. No reset and no extra PR.

## 0. Critical Founder correction — DATA LOGIC BEFORE VISUAL DECORATION

The Atlas cannot be judged by how elegant a route diagram looks. Each route must convey **what a strategic goal asks to achieve, what concrete work is needed, where that work takes place, how much is required, which resources and budgets support it, what was delivered, which measurable environmental/economic/social outcomes followed, and what evidence supports each inference**.

Founder vision: every CSP vision/goal can branch into multiple implementation mechanisms. The land-use LSPS, legal LEP/DCP/SEPP controls, Delivery Program (DP), Operational Plan (OP), Resourcing Strategy, asset management plans, workforce plans, revenue/budget schedules, annual reports and datasets are interconnected **but not interchangeable and not universally hierarchical**. Atlas must preserve multi-parent, multi-path, place-specific and time-specific typed relationships. Physical/financial/environmental accounting is the common quantitative evidence layer. Let users start at any end (a goal, map area, water volume, budget line, work package, carbon intensity, evidence event) and follow both directions to see gaps, mismatches, hidden candidate paths, change history and unresolved questions.

**Founder mandate:** Codex must first study the *actual contents* and meaning of these documents and task domains, then implement a smallest complete, testable source-to-work-to-quantity UI slice using existing Atlas data and model. Do not merely add synthetic descendants or draw a decorative metro map. **No new research-only freeze:** actual code, tests and GitHub commits are required as evidence allows.

## 1. Source-backed NSW legal/administrative conceptual map

### Formal IP&R accountability path (do not guess clause mappings)
`CSP (community outcomes) → Delivery Program (Council initiatives) → Operational Plan (annual actions/services) → actual resources, outputs, outcomes and reports`.
- Resourcing Strategy (Long-Term Financial Plan, Asset Management Strategy/Plans, Workforce Management Plan), revenue policy, budget and progress reporting are **parallel enabling/accountability structures**, not direct substitutes for DP/OP clauses.
- Council may be one contributor among many to CSP community outcomes; do not automatically assign all responsibilities or environmental results to Council operations.
- OLG IP&R guidance recommends specific linking of CSP goals, DP and OP activities, and resourcing/maintenance budgets where appropriate. Source: https://www.olg.nsw.gov.au/councils/policy-and-legislation/integrated-planning-and-reporting/the-process
- Council IPR documents: https://www.snowymonaro.nsw.gov.au/Council/Integrated-Planning-and-Reporting ; CSP 2035 adopted 2025-05-01; adopted DP 2025–29 2026 Revision and OP 2026–27 adopted 2026-06-26. Do not use earlier drafts as latest adopted versions.

### Land-use/spatial planning path
`CSP priority --may inform/align with--> LSPS --guides future controls/strategy--> applicable LEP/DCP/SEPP [as-of region/date] --constrains/enables--> development/planning decisions`.
- NSW planning department says LSPS advances regional/district priorities and the council's CSP priorities; influences the evolution of LEP controls. This **does not** mean every CSP goal is legally a child/parent of an LSPS clause. Source: https://www.planning.nsw.gov.au/the-planning-system/environmental-planning-and-assessment-act-1979/strategic-planning
- SMRC land-use planning site confirms LSPS 2020 adopted 2020-05-21 and 12 planning priorities, including economic growth, environment, land use and infrastructure. https://www.snowymonaro.nsw.gov.au/Building-and-Planning/Strategic-Planning/Land-Use-Planning
- The Council strategic planning page explicitly describes resource competition and prioritised DP/OP projects, and legacy Bombala/Cooma-Monaro/Snowy River LEP amendment contexts. https://www.snowymonaro.nsw.gov.au/Building-and-Planning/Strategic-Planning
- LEP/DCP provide different legal roles, and legacy/current jurisdiction & applicable date matter. Plan proposals and aspirational LSPS actions are **not** adopted controls by default.

### Source version/legal citation rule
Every claim requires link to exact official document/revision/page/section, publisher, adopted/effective/observed dates, geographic boundary, method and verification state. Admission stages remain separate: DIRECTORY → PUBLIC_TEXT_OBSERVED → RAW_BYTES_VERIFIED → CLAUSE_ANCHORED → VERSION_SCOPE_CONFIRMED → HUMAN_REVIEWED → ADMITTED. Not every document needs every stage but an uncompleted gate never counts as official mapping.

## 2. One real numerical anchor — important correction to a prior misconception

CSP 2035 full-document published **page 30** (printed page) includes:
- Measure: **CO2e emissions per capita**;
- source: **Snapshot Climate — Australian Emissions Profiles 2021–22**;
- baseline: **29.9 tonnes** (in the *per capita* metric column context, interpret as `29.9 t CO2e / person`, not AUD per tonne);
- desired direction: **Decrease**;
- exact source: https://www.snowymonaro.nsw.gov.au/files/assets/public/v/4/council/ipr/csp/smrc-csp-2035-endorsed-20250501.pdf
- original emissions-data context for independent comparison: https://snapshotclimate.com.au/locality/municipality/australia/new-south-wales/snowy-monaro-regional/2021/fy

**Never turn 29.9 into a carbon market price, Council operating emissions, a verified current-year emissions number, mandatory emission reduction target, financial liability or Council-delivered carbon saving.** Research previously mentioned Gina communicating this number, but this conversation does not grant access to personal/office messages or authority to copy them. The published CSP metric is sufficient for a controlled public-source research anchor; retain exact document provenance. Distinguish metric's data period (2021–22), CSP adoption (2025-05-01), research observation (2026-10-29), and future reports. Quantitative comparison to a new year requires a matching methodology, population denominator and boundary.

Context from the same CSP table may include economic and water service measures; **do not infer attribution, targets or costs from proximity on the page**. Cite actual clauses and units. If the 24 MB PDF cannot legally be saved or reused, record metadata/short authorized quote & independently check the source; original byte admission can remain PENDING. Do not copy entire PDF into public repo.

## 3. Work Decomposition & Accounting ontology — implement using existing IDs/schema

The core should support **multiple nested levels**, without prescribing that a document is always six levels or that a policy relationship is always a direct descendant.

**Entities (retain immutable source/revision and explicit uncertainty):**
- `StrategicOutcome/Goal`: wording, document revision & anchor, responsible context (community vs Council), location, horizon, desired direction.
- `ImplementationMechanism`: DP/OP initiative, LSPS planning priority, LEP/DCP control, voluntary program, regulatory obligation, capital project; typed authority role.
- `WorkPackage/Activity`: task, rationale, prerequisite, service domain, planned vs actual, effort unit, outputs, schedule, role/responsibility **only where publicly evidenced**, geographic footprint.
- `AssetOrResource`: land area, parcel/use class, water source & wastewater stream, energy carrier, emissions scope, infrastructure/service asset, population/customer base, economic sector, labor/time and budget source.
- `MetricDefinition`: measured variable, unit, dimensions, direction_of_good, target/baseline/actual provenance, aggregation rule, observation boundary, denominator, quality, method/version, uncertainty, currency-year where relevant.
- `QuantifiedObservation`: exact value OR unknown, calendar/fiscal period, spatial boundary, populations/sector coverage, source page/table/URL/byte digest, verification state, raw vs estimated vs derived, unit conversion.
- `FinancialAllocation/Expenditure`: approved budget vs revised budget vs actual expenditure vs committed contract vs estimate; AUD fiscal year, CAPEX/OPEX, cost center/project/public reference, allocation and potential double-count status.
- `PhysicalFlow/Stock`: area ha/km², installed capacity ML/day, water volumes ML/year, treatment volumes ML, rainfall mm over catchment, energy MWh, emissions t CO2e/year; stock/flow and physical boundary must be explicit.
- `Output/Outcome/Impact`: what was built/delivered, service/output levels, observed community/environmental change, plausible contribution not automatic attribution, counterfactual/causal limitations.
- `Evidence/Assumption/Gap`: source, method, check, contradictory evidence, incomplete denominator, missing revision, unresolved reviewer questions, provisional status.
- `RelationshipAssertion/ChangeEvent`: leverage existing model. A claim with several goals or cost centres must have explicit allocation method or `MULTI_PARENT_UNALLOCATED` rather than duplicating a budget/benefit.

**Relationship vocabulary (typed, directional and supported):**
`STATES_GOAL`, `ALIGNS_WITH_STRATEGY`, `IMPLEMENTED_BY`, `ENABLED_BY_LAND_USE`, `APPLIES_IN_AREA`, `CONSTRAINED_BY_LEP`, `GUIDED_BY_DCP`, `RESOURCED_BY`, `FUNDED_BY`, `MEASURED_BY`, `BASELINE_FOR`, `TARGETS`, `OBSERVES`, `PRODUCES_OUTPUT`, `CONTRIBUTES_TO_OUTCOME`, `EVIDENCED_BY`, `COSTS`, `CHALLENGED_BY`, `SUPERSEDED_BY`, `RESEARCH_CANDIDATE`.
A mere thematic match must be `RESEARCH_CANDIDATE`; legal force, causal effectiveness and official attribution require their own separately reviewed assertions.

### Three simultaneous but independently auditable ledgers
1. **Financial ledger:** funding authorisation, budget, committed amount, actual paid, outstanding balance/variance, fiscal year, inflation basis, project shares and rounding. A budget is not actual spending.
2. **Physical/environmental ledger:** land area/use, water supply/treatment, energy consumption, regional vs operational greenhouse gas inventory, waste/asset stocks and throughput. A physical quantity is not a currency amount or a result percentage.
3. **Outcome and evidence ledger:** baseline → target → verified actual → observed change; distinguish reportable output, measured outcome and attributable effect. Some CSP outcomes cannot be fully quantified or causally attributed; preserve qualitative evidence and UNKNOWN.

**Do not silently multiply or aggregate incompatible quantities.** E.g. `t CO2e/person × persons = t CO2e` is permitted **only with matching population definition, geography, period, sector/scope and methods**; regional inventory ≠ Council operations; ML ≠ ML/day; km² ≠ ha without explicit conversion; AUD 2025 ≠ AUD 2026 without stated basis. A missing denominator ≠ zero. Disjoint categories must be checked before sum; multi-parent benefits/costs require allocation fractions summing to 1 or marked unresolved.

### Candidate formulas (not outputs until inputs verified)
- `Coverage = reviewed_in_scope / defined_eligible_relationships`, otherwise COUNT_ONLY/UNKNOWN.
- `Budget variance = actual_expenditure - approved_budget`, only same cost scope, year and accounting basis.
- `Cost per service unit = eligible_actual_cost / eligible_verified_output`, same year/service boundary.
- `Per-capita rate = compatible_total / compatible_population`; report population source and year.
- `Emissions = activity_data × matching_emission_factor`, with factor version, fuel/sector boundary, scope and uncertainty; observed published per-capita metric may be displayed without reverse-engineering its factor.
- `Progress = current outcome vs admitted baseline and target` only for a metric explicitly defined with comparable values and favourable direction; elapsed time never substitutes completion.

## 4. Mandatory three vertical evidence pathways

**V-A: Environment / carbon**
- Start from official CSP 2035 environmental KPI **29.9 t CO2e/person** and desired trend decrease, source page 30; use **observed/admission-pending**, not ADMITTED, until source gates actually passed.
- Ask which CSP goal(s), DP/OP actions, LSPS Priority 4 carbon-neutral planning, real measures and physical/financial resources support it. The alignment of an LSPS planning priority to a specific CSP goal should start as a hypothesis until exact official evidence is cited.
- Capture **municipal-wide accounting vs Council operations**, population denominator, emissions scope, factor/methodology, source years and uncertainty. If amount of Council responsibility or budget is not proven, display `UNKNOWN`, not an invented share.
- Test rejecting mistaken parsing of 29.9 as `AUD/t CO2e`, annual Council emissions or an already achieved reduction.

**V-B: Water, wastewater and infrastructure**
- Choose one legitimately public CSP/DP/OP water-service or environmental infrastructure line; follow to a real public budget or annual service output **only if** exact documents, action IDs and table references can be verified.
- Model the candidate work packages (inspection/maintenance/treatment/service capacity etc) as **synthetic templates unless the public OP explicitly names them**.
- Explore paired quantities: population served/connection count, water ML per year, wastewater ML, service capacity vs actual throughput, financial CAPEX/OPEX, service outcomes; remain UNKNOWN if not public.
- No WCOS internal LTW/backflow customer cases, Council work records, internal systems or personal data.

**V-C: Land use, regional economy and facilities**
- Follow an LSPS 2020 planning priority to the *applicable as-of legal* LEP/DCP where verified; identify the spatial overlay, proposed vs in-force control, quantified land area ha, housing/population/demand scenarios, infrastructure capacity and budget implications.
- Cross-check plan years and jurisdiction (Bombala/Cooma-Monaro/Snowy River legacy boundaries), regional economics (employment, output, sector data) and opportunity costs without inventing local values.
- Demonstrate a **false link** rejected because of mismatched region, date, unit or unsupported legal relationship; do not infer a development consent/approval from any planning route.

Each pathway's output must include a source-to-claim-to-work-to-quantity-to-cost-to-outcome-to-review **trace sheet**, plus a counterevidence/gap sheet. Unknowns are valid data fields.

## 5. Engineering order: source analysis + running website, not more plans

### W0 — Examine substantive sources and existing model (bounded, no rewrite)
- From latest HEAD read `NEXT_SESSION.md`, `DATA_CONTRACT.md`, existing `AtlasData`, `AtlasModel`, `AtlasWorkspace`, CSP admission, earlier QA, and V1.4 route-first design. Identify what is **actually implemented**, what is synthetic, what is official observation, and what relation is merely posited.
- Build an evidence mapping for three pathways using the **latest official approved** public IP&R/LSPS/planning sources and annual/financial performance docs. Prefer exact extraction with page/table anchor and version; cite external URLs, do not upload raw copyright-restricted PDFs.
- Produce a **small crosswalk file** of work/activity, accounting units, budgets, sources and UNKNOWN before coding, so code implements meaningful domain objects. No need to wait for all documents before moving to W1.

### W1 — Implement measurable Strategy-to-Work objects in existing model
- Add an extension module (or fields on existing model) for WorkPackage, MetricDefinition, QuantifiedObservation, ResourceAccount, FinancialEntry, OutcomeObservation, ContributionAssertion, with validator schemas, immutable revision IDs, event linking and field-level provenance. **Extend existing model, never launch a second knowledge graph.**
- Implement dimensional checks, territory/year/sector/attribution checks, no-source/no-approved mapping, allocation double-count controls, legal-vs-strategic edge typing, explicit UNKNOWN and missing denominator, unit/error tests.
- At least one source-backed observation (29.9 t CO2e/person, page-anchored, admission pending), two wholly synthetic work-accounting examples, and one rejected incompatible aggregation. Preserve document provenance and status.

### W2 — Connect accounting to the O2 route-first UI
- Keep continuous route as primary graphic and attach evidence/resources/quantities as **interactive data layers** selectable per station and connection: `Why?` / `What work?` / `Where?` / `How much?` / `How funded?` / `What changed?` / `Show source`.
- Selecting a CSP goal must be able to show an actual hierarchical work breakdown plus audited cross-links, not only a fixed six-level synthetic content tree. Selecting a unit-labeled budget/volume should reverse-trace to its goal and proof; a click on the line shows relation type, rationale, reviewer status and counterevidence.
- Show real numerators/denominators only where admitted, otherwise visible question marks/UNKNOWN, **never blank-space or guessed 0%**. Surface exact units and time/region in the map tooltip/inspector without overwhelming the screen.
- Preserve full English 127-content recursion, local editor, version diff and hash receipts; maintain route-first readability, contextual inspector, accessible text alternative, keyboard/touch controls.
- No fake success progress lines: route *color* may signal domain and *line fill* may signal selected, provable measure; "amount of work" needs actual quantity and target, not arbitrary percentage.

### W3 — Verify & ship checkpoint
- Actual Node tests, source-byte checks and screenshot/browser validation of first vertical slice and 3 failure cases; new tests for metric dimensionality, per-capita vs per-tonne, geography/time compatibility, budget-vs-expense and multi-parent allocation.
- Re-run all previously passing Atlas tests and local revision two-tab tests or honestly mark NOT_TESTED.
- Confirm no Council private data/hidden keys/copyright-restricted original PDFs were committed; no new paid deps.
- Commit+push to same PR #130, update `NEXT_SESSION.md`, verify remote HEAD, report one next executable task. **Do not pause coding until a whole policy corpus has been extracted**; ship a thin end-to-end working vertical slice with clear UNKNOWN.

## 6. Acceptance criteria
- Demonstrate **why** a CSP goal branches into DP/OP actions, an independently typed LSPS land-use planning pathway, resources, work and outcomes; all claims traced or explicitly unknown. The UI must not imply a statutory `CSP→LSPS→LEP→DCP→OP` hierarchy.
- **Real meaning at every point:** action, measured amount, unit, time frame, place, funding or gap, outcome and evidence status. No blind synthetic pseudo-precision.
- 29.9 anchored accurately as **t CO2e per capita**, with 2021–22 source; not a price or Council operational emissions claim. A test must reject `AUD/t` mislabel.
- Three vertical test cases; at least one user can reverse from a metric/cost/physical quantity to the stated source and, if evidence actually exists, to the strategy goal. Broken/unsupported chains stop visibly rather than fabricate an answer.
- All old functional tests still pass, the route-first UI remains primary direction, and the new feature is real code in the existing repo (not only Markdown).
- Accurate QA and persistent `NEXT_SESSION.md` on remote head.

## 7. Hard boundaries and coordination
**Permitted:** independent, personally authorised public/synthetic research; actual frontend/data-model engineering and tests on isolated GitHub PR #130, no paid dependencies, 0 new procurement.

**Not permitted:** Council nonpublic/employee-only files or apps, internal records, real customers, credentials, confidential message attachments, assumed Council endorsement, external signing/issuance, official performance attribution, new vendor contracts, deployment, main/PR #129 changes, merging PR #130. Do not claim R0-K original source recovered.

**Founder decisions:** This V1.5 data-logic directive has **higher priority than visual polishing** when both compete for effort; V1.4 remains mandatory route-first UX for map semantics. This is a change of next work order, not new authorization to deploy or legally declare compliance.

**Codex exact instruction:** Read latest PR #130 HEAD & NEXT_SESSION, V1.4 route-first and this V1.5. First analyse real CSP/LSPS/DP/OP/resource/budget contents and the existing Atlas schema; then **implement the smallest source-backed work–resource–quantity–cost–outcome chain, with type-safe measurement and evidence gates**, in the existing English website. Include regional 29.9 t CO2e/person as an observed, not fully admitted source marker and reject the false AUD/t interpretation. Prove what links are official and which are inferred/unknown; add tests and visible UI drilldown. Do not sacrifice the route-first map, regression features or cross-device GitHub checkpoint. Commit/push actual engineering and update NEXT_SESSION; do not send only another planning document.
