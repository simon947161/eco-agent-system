# Climate evidence matrix

All values below are transcribed published observations, not new calculations. Source IDs resolve in [SOURCES](SOURCES.json). Exact daily QC flags/raw series are not available in this package.

| ID | Region / station | Window | Reported variable | Evidence limit |
|---|---|---|---|---|
| E1 / C1 | Cooma / 070217 | 2019-01-16 to 2019-01-16 | 37.9 degC — daily maximum air temperature | Hot-day observation within a record-warm January; not a newly calculated heatwave threshold or reactor temperature. |
| E2 / C2 | Rockhampton / 039083 | 2018-11-25 to 2018-11-25 | 41.5 degC — daily maximum air temperature | Monthly report high-temperature day; no facility heat exposure or emissions inferred. |
| E3 / C3 | Cooma / 070217 | 2019-01-01 to 2019-12-31 | 318.6 mm — annual rainfall total | Lowest annual rainfall in cited 30-year record; meteorological deficit context, not soil-water/process drought proof. |
| E4 / C4 | Rockhampton / 039083 | 2019-01-01 to 2019-12-31 | 295.8 mm — annual rainfall total | Lowest annual rainfall in cited 79-year record; no facility moisture or water-balance observation. |
| E5 / C5 | Cooma / 070217 | 2016-06-06 to 2016-06-06 | 86.0 mm — daily rainfall total | Reported June daily record; no measured landfill inundation. Site ID corroborated by C11. |
| E6 / C6 | Rockhampton / 039083 | 2017-03-01 to 2017-03-31 | 409.4 mm — monthly rainfall total | Very-high monthly rank; source describes Debbie landfall on 28 March and flooding. Daily local event total/window remains UNKNOWN. |

## Evidence relationships, not causal results

| Link | State | Missing gate |
|---|---|---|
| BOM summary to dated station assertion | SUPPORTED_SCOPED | Daily source QC and version replay remain partial |
| Annual rainfall deficit to regional drought context | PARTIAL | Not a formally reconstructed drought duration, soil moisture or facility water balance |
| ENSO/IOD/SAM phase to event | CONTEXT_ONLY | Daily observed index, valid time and analysis design; never direct gas multiplier |
| Station to facility weather exposure | BLOCKED | Verified facility geometry, representativeness, station history, clock alignment |
| Weather exposure to process response | HYPOTHESIS_ONLY | Actual process temperature, moisture, load, residence time, redox and controls |
| Process response to CH4/N2O/CO2 flux | BLOCKED | Gas sampling, flow, calibration, capture/destruction and storage/transport data |
| Facility activity to energy emissions | BLOCKED | Metered energy/fuel, factor vintage and boundary; no export credit assumed |

SUPPORTED_SCOPED is an internal evidence label, not scientific admission or external acceptance. B3 is ACCEPT_WITH_LIMITS; this new C package is awaiting review.
