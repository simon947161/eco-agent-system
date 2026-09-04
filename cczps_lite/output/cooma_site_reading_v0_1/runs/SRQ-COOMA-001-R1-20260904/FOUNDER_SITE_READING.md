# Cooma Site Reading v0.1 - R1

## 1. Question asked
What can admitted evidence currently support as a bounded environmental Site Reading for Cooma, and what remains blocked or unknown?
Decision use: Founder review, evidence-gap prioritisation and preparation of later professional review; not approval or operational action

## 2. Place and spatial boundary
Cooma, New South Wales, Australia. Cooma locality and +10 km orientation context; Mittagang gauge 410033 remains station-bounded; no catchment-wide inference

- **LOCALITY_BOUNDARY** (`COOMA-LOCALITY`): Official NSW Cooma locality; not an LGA, catchment, hydrological boundary or final scientific study boundary.
- **TERRAIN_DEM** (`COOMA-TERRAIN-DEM`): Bounded GA SRTM DEM and derived terrain context within the locality plus 10 km orientation extent.
- **HYDROLOGY_WATERCOURSE** (`COOMA-WATERCOURSES`): Official main-watercourse spatial context; presence is not flow, quality or condition.
- **CATCHMENT_CONTEXT** (`COOMA-CATCHMENTS`): Contracted and stream-segment catchment context; none is identified as a drinking-water supply catchment.
- **ROADS_SETTLEMENT** (`COOMA-ROADS-SETTLEMENT`): Official roads and locality context bounded to the Cooma plus 10 km orientation extent.

**Boundary:** Spatial presence does not itself establish environmental condition.

## 3. Direct observations
`OBSERVED: NONE_ADMITTED_FOR_THIS_READING`. No direct human/instrument observation with observation time, method and geometry was admitted.

## 4. Known from admitted official evidence
- The admitted BoM product records 27 dated rows covering 2026-07-1 to 2026-07-27.
- The admitted Mittagang 410033 historical answer covers 1964-03-01/2024-02-29 at S0/L2 with cutoff 2024-02-29.

## 5. Historical hydrology at L2
The admitted Mittagang 410033 TBEA is `S0 / L2`, covers `1964-03-01/2024-02-29`, and has cutoff `2024-02-29`. It is historical only, not a current-flow statement.

## 6. Current hydrology boundary
`ADMISSION_BLOCKED_MISSING_RAW_RESPONSE`; `NOT_COMPARABLE_YET`; `TREND_DEFERRED`. No current flow value is inferred.

## 7. Derived result
Historical L2 context exists, but the missing exact near-current response prevents a current comparison.

## 8. Inferred interpretation
Spatial references help scope later evidence requests but do not establish environmental condition.

## 9. Unknowns
Current Mittagang flow and current Cooma catchment condition are unknown.

## 10. Conflicting or blocked evidence
Exact near-current WaterNSW response bytes and qualified hydrology review are missing. Historical quality-screen sensitivity is preserved rather than averaged away.

## 11. Maturity and authority ceiling
Evidence maturity `S0`; conclusion ceiling `L2`; intervention ceiling `A0`.

## 12. Expiry and triggers
Issued: `2026-09-04T02:00:00Z`. Evidence cutoff: `2026-07-27`. Valid until: `2026-12-04 or earlier upon any update, demotion or stop trigger`.

- Update: new admitted evidence; source or method version change; spatial context revision; professional review finding.
- Demote: source identity/provenance failure; calculation or contract error; evidence expiry; material professional-review defect.
- Stop: attempted A1+ use; attempted current flow/trend claim; unresolved identity mismatch; attempted engineering/regulatory/procurement/public-warning use.

## 13. Permitted low-regret A0 action
Preserve records, request missing evidence and prepare qualified review. Allowed: MONITORING_PREPARATION, EVIDENCE_REQUEST, RECORD_PRESERVATION, REVIEW_PREPARATION. Status: `READY_FOR_HUMAN_REVIEW`.

## 14. Prohibited conclusions and actions
A1_OR_HIGHER; ENGINEERING; REGULATORY; PROCUREMENT; PUBLIC_WARNING. No engineering, regulatory, procurement or public-warning action is authorised.

## 15. Evidence to obtain next
- Exact WaterNSW 410033 near-current response and receipt
- Qualified hydrology review
- Admitted local ecological/soil/land-cover observations

## 16. Human/professional review
Founder review and PR #115 hydrology professional gate remain pending. No H1-H8 sign-off is simulated.

## 17. Audit artifacts
- Time-Bounded Answer: `time_bounded_environmental_answer.json`
- Environmental Evidence Passport: `evidence_passport.json`
- A0 Action Passport: `action_passport.json`
- Run Receipt: `run_receipt.json`
- PC-01-PC-04 contracts: `planner_contracts.json`
