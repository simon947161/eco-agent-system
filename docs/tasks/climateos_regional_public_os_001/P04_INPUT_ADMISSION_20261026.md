# P04 CASE001 input admission — 2026-10-26

Status: **PARTIAL_METADATA_VERIFIED / NUMERIC_JOIN_BLOCKED**. Continues the existing case; WaterNSW credentials are not a dependency for this historical-source investigation. No inferential statistics or numeric subset admission performed.

| Input | Observed official evidence | Outstanding gate / lawful next action |
|---|---|---|
| Catchment: BOM Geofabric | Official download page explicitly licenses Geofabric CC BY4.0, describes v3x services and gauging-station network nodes | PARTIAL: derive and validate the exact 410033 upstream polygon, pin network version, CRS, snapping tolerance, topology and area against1889.8km²; no council boundary substitution |
| Precipitation: AWRA historical monthly service | Live public metadata HTTP200; WGS84/4326, 0.05° pixels; `precip_month` rendering description says mm | PARTIAL: exact data revision, underlying variable/aggregation semantics, product-specific reuse/automated-access licence, cost/quota and basin weighting not verified |
| Soil moisture: same AWRA service | Live metadata includes `smpfull` percentage rendering; AWRA-L is modelled water balance, not a field soil-moisture measurement | PARTIAL: underlying variable, depth and monthly mean versus end-of-month statistic unresolved; same rights/version/space gates as precipitation; shared model inputs are not independent confirmation |
| Independent rainfall alternative: AGCD | Official description identifies a gauge-informed statistical gridded estimate, not direct basin observations | PARTIAL: select an actual free downloadable version and its licence/resolution/coverage; do not infer download rights from a public map |

## Inspectable source evidence

- [Geofabric downloads](https://www.bom.gov.au/water/geofabric/download.shtml): licence and general station-to-catchment workflow verified; exact station polygon not obtained. No large downloads or paid GIS dependency introduced.
- [AWRA monthly ImageServer](https://image.wsapi.cloud.bom.gov.au/arcgis/rest/services/awra_historical/physical_month_crf_multivariable_all_data/ImageServer?f=pjson): live bytes saved locally with SHA256 in `P04_SOURCE_METADATA_CHECK.json`. Public metadata read required no key. ArcGIS `currentVersion=10.91` is server software, not the hydrological dataset version. Blank copyright, `allowCopy=true` and `allowAnalysis=true` do not establish licensing. `timeReference=null` and default28-day display interval do not define scientific monthly aggregation. No rate guarantee inferred.
- [AGCD methods](https://www.bom.gov.au/climate/austmaps/about-agcd-maps.shtml): candidate identity only; no numeric extraction or purchase.
- [BOM drought methods](https://www.bom.gov.au/climate/drought/): published soil maps use modelled end-of-month daily values; root-zone0–1m and deep1–6m definitions apply to that product. Do not transfer them unverified to the selected monthly ImageServer variable.
- [BOM dataset licensing](https://www.bom.gov.au/metadata/catalogue/license.shtml): dataset-specific constraints matter even for no-cost products. No third-party catalogue licence was substituted for an official product licence.

## Join and uncertainty contract

The metadata time extent overlaps2000–2025 but does not prove every month is populated. No-data sentinel is3.4e38; mask and completeness must be validated before summaries. Preserve estimated/modelled status and model revision, uncertainty, input dependence, soil depth and spatial weighting. HRS records retain their original QC; E records are not silently used as reliable values. Prior24h/09:00 source-local dates cannot be joined to UTC/calendar months without an authoritative interval contract.

Next minimum action: retrieve the selected AWRA product's official licence and multidimensional variable definitions through its documented catalogue/download path, then locate Geofabric410033 network node and an inspectable upstream polygon. Record source version, permission, timestamps and geometry checksum. If licensed compatible inputs and the time contract pass, obtain one bounded local month/catchment subset and finalize a preregistered comparison protocol. Otherwise retain blocked admission. No environmental or causal conclusion is supported yet.
