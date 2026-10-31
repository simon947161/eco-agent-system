# Atlas V1.5 — Public-source-to-work/quantity/finance crosswalk
**Date:** 2026-10-29 (Australia/Sydney)  
**Scope:** independent public research; not Council official; not a legal, scientific or public-finance assurance opinion.  
**Engineering:** `atlas-accounting.js` reuses existing AtlasData node IDs `csp6`, `water`, `area`; `accounting.test.cjs` checks bounded data and rejection of incompatible claims. No new knowledge graph.

## Formal pathways (not a single automatic hierarchy)

- NSW OLG IP&R: **CSP → Delivery Program → annual Operational Plan**, with Resourcing Strategy (workforce, asset management, long-term financial) and budgets enabling actions. Source: https://www.olg.nsw.gov.au/councils/policy-and-legislation/integrated-planning-and-reporting. OLG explicitly expects DP/OP work and resource requirements to line up; do not assume every community ambition is fully delivered by Council alone.
- NSW Planning: **LSPS links community/regional planning priorities to land-use actions** and informs the evolution of LEP controls; DCP performs a distinct control/guidance role. Source: https://www.planning.nsw.gov.au/the-planning-system/environmental-planning-and-assessment-act-1979/strategic-planning. This is *not* evidence that any specific CSP 6.1 clause automatically imposes a particular LEP provision or OP work package.
- SMRC public IP&R directory: https://www.snowymonaro.nsw.gov.au/Council/Integrated-Planning-and-Reporting. It identifies CSP 2035 (adopted 1 May 2025), DP 2025–2029 2026 revision and OP 2026–2027 (adopted 26 June 2026), 2026 revised Resourcing Strategy, and water/wastewater asset management plans. **No line-item programme, current works budget or actual expenditure has been admitted from these listed documents into this Atlas slice.**
- SMRC LSPS public overview: https://www.snowymonaro.nsw.gov.au/Building-and-Planning/Strategic-Planning/Land-Use-Planning. LSPS first adopted 21 May 2020; a current applicable LEP/DCP clause by time/place is NOT verified by this directory.

## A. Regional emissions (real, attributed observation; no implementation mapping)

| Field | Value | Status |
|---|---|---|
| Statement | CO2e emissions per capita; desired trend decrease | `PUBLIC_TEXT_OBSERVED` |
| Baseline | **29.9 t CO2e/person** | Source attribution, NOT reviewed/admitted KPI mapping |
| Data source period | **2021–22** | Published source year label; exact inventory interval not independently confirmed |
| Source | CSP 2035 published environmental measures table, printed p. 30; attributed to Snapshot Climate Australian Emissions Profiles 2021–22 | https://www.snowymonaro.nsw.gov.au/files/assets/public/v/4/council/ipr/csp/smrc-csp-2035-endorsed-20250501.pdf |
| Population denominator | Population concept embedded in per-capita intensity; exact count to recompute totals not admitted | `UNKNOWN` |
| Geographic/sector boundary | Regional Snowy Monaro context; not Council operations inventory | `REGIONAL_COMMUNITY_INVENTORY` concept, method/scope subject to review |
| Direct Goal 6.1 → this indicator | Thematic Atlas demo placement only; not evidenced official clause mapping | `UNKNOWN` |
| DP/OP actions, work quantity, budget, paid cost, achieved reduction | No specific official connection verified in this slice | `UNKNOWN` |
| Council endorsement / reviewer | No independent identified official review of linkage | `ADMISSION_PENDING_REVIEW` |

**Failure to prevent:** misreading 29.9 as AUD/t, a carbon credit price, annual Council operational t CO2e, a quantified saving or a current-year result; extrapolation to total tonnes without matching year, region, denominator and inventory methods.

## B. Water and wastewater

- Current source *register* exists at SMRC IPR directory: latest adopted DP/OP and Asset Management Plans for Water/Wastewater. Specific action IDs, volume data, annual expenditure and allocation by CSP goal are not yet verified.
- Existing Atlas `water` is a **synthetic node**. The new `water-service-work-demo` illustrates 12 ML throughput and AUD 24,000 simulated ACTUAL_EXPENDITURE for the same **synthetic** FY and boundary, giving AUD 2,000/ML synthetic intensity. **These are invented fixture numbers for dimensional/reconciliation tests only**, and **not a Council service target or finance report**.
- Distinguish `ML` (volume), `ML/day` (capacity/flow rate), `ML/year` (annual rate/period), budget commitments vs actual spend, delivered outputs vs environmental/service outcomes.
- Future intake: take one *exact* current OP water/wastewater activity and its budget table, independently anchor and review them, then attach only permitted and verified parts. Do not use internal LTW, Backflow or asset-management work systems.

## C. Land use, people and regional economy

- LSPS 2020 gives land-use priorities and time/geography context; verify separately the **currently operative applicable LEP/DCP** by land parcel and as-of date. A similar paragraph does not prove legal applicability. The existing planning nodes are synthetic modelling objects.
- `land-use-work-demo` is an explicit hypothetical 50 ha review scenario, not a zoning approval, actual land availability, economic output, projected population requirement or published Council programme.
- Do not assert how many homes/jobs/resources will be produced without provenance and scope-comparable methods. Never sum existing areas with incompatible land-use classifications or unreviewed overlaps.

## Testable contract for the next stage

1. **Quantified object**: logical ID, revision, source, date/period, place/area, boundary, metric unit, value OR UNKNOWN, method/denominator, review status; observed baseline distinct from actual achieved result.
2. **Resource/finance**: keep physical stock/flow separate, budget/commitment/expenditure types separate, per-service intensity requires actual comparable output and cost, allocation must sum to 100% before an amount is distributed across several goals.
3. **Semantic links**: each assertion independently carries evidence anchors, reviewer, predicate, time/geography and counterevidence. `THEMATIC_CONTEXT_ONLY_NOT_OFFICIAL_MAPPING` never upgrades to `IMPLEMENTED_BY` just because a UI card is opened.
4. **Quantitative UI**: route-first station inspector provides Why/Work/Where/How much/Resources/Funding/Output/Evidence, unknowns explicit; original recursive content, snapshot verification and local edits remain untouched.
5. **Future source admission**: for the current DP/OP and LEP/DCP, obtain exact PDF/document revision and permission, page/table/section, dates, geography, units and reviewer. Leave admission pending where legal/ownership/quality status is not confirmed.

**Current delivery limitation:** Crosswalk is a bounded research-to-code schema input, not a complete reading of the latest 36–46 MB Council planning/budget corpus. No real new annual budget has been entered, and no official goal-to-cost relationship is claimed.
