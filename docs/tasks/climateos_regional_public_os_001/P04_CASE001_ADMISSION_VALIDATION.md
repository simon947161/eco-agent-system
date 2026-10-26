# P04 CASE001: executed spatial and AWRA admission

2026-10-26; baseline `891d8a9a1893a3b0280672166fbfef973de1e9f6`; consumed [Issue128 comment6412018542](https://github.com/simon947161/eco-agent-system/issues/128#issuecomment-6412018542). Same branch/Draft PR129. **PARTIAL: publisher geometry and product metadata verified; numerical join BLOCKED.** This is an executed data audit, not a new taskbook or a scientific result.

## Actual upstream geometry

Used the production `hosting.wsapi.cloud.bom.gov.au` Geofabric V3.3 service, not staging. Its linked public item `ea9f7296abeb49c3a45430cd322400b1` explicitly licenses CC BY4.0. Eight exact response snapshots, request URLs, UTC retrieval times and SHA256 are committed under [evidence/p04_case001](evidence/p04_case001/manifest.json); document capture hashes are in [P04_DOCUMENT_EVIDENCE.json](P04_DOCUMENT_EVIDENCE.json).

| Check | Result |
|---|---|
| Identity | One stationno410033, Murrumbidgee River at Mittagang Crossing; network node HydroID43408271 |
| Upstream polygon | StationCatchments layer49, HydroID43677907; `netnodeid=43408271` exact join |
| Publisher derivation | Aggregated surface-network catchments, with some outlet catchments split; intended for regional reporting/modelling |
| Version | Published layer group V3.3; exact revision represented by snapshot hashes/item modified time, not ArcGIS server10.91 |
| Topology | Valid MultiPolygon; 2 parts and 2 holes; no repair, dissolution, simplification or administrative-boundary replacement |
| Coordinates | Polygon GDA94/EPSG4283; returned node WGS84/EPSG4326; independently projected to Australian Albers/EPSG3577 |
| Area | Computed1902.459811km²; publisher1902.459810km²; HRS reference1889.8km²; difference **+0.669902%** |
| Node position | Covered by polygon; distance to polygon boundary11.5098m |
| Confidence | Publisher code4, labelled Good by the layer domain; no undocumented promotion to higher confidence |
| Snapping | None performed. Exact station/node join reused publisher geometry. Original publisher snap tolerance is not given; `near_dist=4.76780007` is retained as a raw attribute, not assumed to be a tolerance |

The source-defined upstream boundary is recovered and technically verified. It is not proved identical to the older HRS polygon. HRS methodology explicitly describes a Geofabric V2.1 relationship; version differences are a plausible explanation for area discrepancy, **not a demonstrated cause**. The node's upstream-network area also differs from station-catchment area; retain the station polygon's dedicated outlet aggregation, do not silently substitute network-node accumulated area. Independent hydrographic review of the outlet/version/area relationship remains required for scientific equivalence. No arbitrary nearest-point snapping threshold was invented.

## AWRA admission findings

Rendered official [AWO licence](https://awo.bom.gov.au/about/overview/licence) states CC BY4.0 unless otherwise noted. [Data Access](https://awo.bom.gov.au/about/overview/dataAccess) expressly provides product NetCDF/CSV downloads and AWDS web-service connections. This resolves the previous blanket product-licence uncertainty for the inspected AWO material and published access path. Retain attribution and modification notices; no endorsement. Read-only public metadata incurred no fees and required no account. No unlimited quota, service guarantee or scheduled use is inferred; no subscription/purchase performed. The technical-report PDF has its own rights notice and is not redistributed.

Live multidimensional metadata was retrieved from the production historical monthly ImageServer. The immutable response is pinned separately from the rolling AWRA-Lv7 model identity. The service exposes501 month-end labels from1985-01-31 through2026-09-30; both selected variables contain all312 study labels2000–2025. **Labels do not prove usable data in every cell.** WGS84/4326 grid spacing is0.05°; source no-data sentinel3.4e38. A future subset must verify masks, grid-cell footprints, basin weighting and actual completeness before analysis.

| Item | Verified definition | Remaining limitation |
|---|---|---|
| `precip_month` | Rendering function, not a data-variable name | Never query it as a physical variable |
| `rain_day` | Actual variable; description Daily Rainfall; raw unit mm | Monthly product tooltip explains aggregation of near-real-time daily inputs; source daily window/month-boundary compatibility with HRS not established |
| `smpfull` | Rendering function | Not proof of storage encoding or soil depth |
| `sm_pct` | Actual variable; description Total rootzone soil moisture(0–100cm); raw unit fraction of fullness | Official UI displays percent available water. Raw fraction-to-percent encoding/scale must be confirmed; no silent multiplication/division |
| Root-zone soil water | Modelled upper+lower layer water, top1m, relative to available storage capacity; soil mapping and model assumptions apply | Not field measurement or independent corroboration of rainfall that drives the same model |
| Time statistic | Historical FAQ: period-to-date soil moisture is averaged, fluxes accumulate; precipitation tooltip explicitly aggregates daily inputs | Full-month raw `sm_pct` statistic and time bounds must be established for the exact product; a month-end label alone is not end-of-month soil state |
| Update/version | Historical model AWRA-Lv7; FAQ describes daily updates and revision as climate inputs arrive | Pin actual response/NetCDF revision; model version and server version do not identify immutable data |

Public model/FAQ explanations were read in the real browser because static HTML was only a JavaScript shell. Captures are full rendered accessibility text, **not HTTP wire bodies**, with distinct hash/type records. No full third-party document or signed outbound tracking URL is republished. The geometry and JSON metadata are supplied with CC BY4.0 attribution.

## HRS day and quality gate

The existing accepted raw CSV was rehashed: `78e8188f3f445afa33ad466dd0554e653761ef617832b6df3a9eac6b1240ca1a`. Its extraction statement describes previous24h discharge reported9am local. Header labels mix ML/day and Flow(ML), while extraction prose refers to cubic metres. Preserve these statements; do not invent a unit normalization. Reviewed official HRS FAQ/methodology pages do not settle station-specific DST handling, whether a date labels the reporting or contributing interval, or allocation of intervals crossing month boundaries. Therefore **HRS×AWRA numerical joining remains BLOCKED**.

Historical E quality codes, prior source coverage ending2026-02-28, and pending scientific review remain unchanged. No current-water, causal, supply, pollution, low-flow anomaly or correlation conclusion is produced. No numerical AWRA raster subset was prepared because the complete admission gate did not pass.

## Executable verification and tests

New `tools/verify_p04_spatial_admission.py` is offline: validates pinned content digests, exact station/node join, CRS, publisher confidence, geometry validity, area and AWRA month labels. It distinguishes rendering functions from variables, rejects changed units/missing dates/corruption, and emits a blocked research receipt. It does not retrieve or join numeric series.

Free GIS libraries were installed only into ignored `.local/p04-gis-deps`, with no production dependency changes. Reproduce in PowerShell:

```powershell
python -m pip install --target .local/p04-gis-deps --only-binary=:all: shapely==2.1.2 pyproj==3.7.2 numpy==2.5.4 certifi==2026.10.23
$env:PYTHONPATH = (Resolve-Path .local/p04-gis-deps).Path
python -B tools/verify_p04_spatial_admission.py
python -B -m unittest discover -s tests -p 'test_p04*.py' -v
python -B -m unittest discover -s tests -p 'test_monthly_evidence_links.py' -v
```

Actual results: **15 focused tests passed** (9 new admission +1 previous preflight +5 monthly references), no skips. Full `python -B -m unittest discover -s tests` ran in an isolated copy with GIS dependencies: **508 tests, OK, 1 skipped**,8.802s. Without optional libraries the four GIS tests are explicitly skipped, not claimed passed. [P04_SPATIAL_ADMISSION_RESULT.json](P04_SPATIAL_ADMISSION_RESULT.json) records the actual offline verification output.

The four original dirty reports remain hash-identical and outside this commit. July accepted records, local ingestion history, Sites owner-privatev2, PR127 and PR129 merge state are untouched. Rollback consists of reverting this scoped code/evidence/state commit; no external data or configuration was mutated. Raw originals and prior acceptance records are retained.

## Next executable work

Use the documented AWO download/catalogue path to inspect **one monthly NetCDF header/time-bounds/scale-factor contract** for `rain_day` and `sm_pct`, without extracting a numeric basin series; seek an existing official HRS410033 reporting-day/DST/month-assignment definition. If published definitions remain unavailable, prepare a precise clarification request for owner review, do not send it automatically. Record each answered field before allowing a single bounded basin/month subset. WaterNSW key restoration remains a separate owner-dependent configuration gate and was not searched this turn.

Radar: knowledge—station polygon recovered, rendering names differ from data variables; decision—preserve valid geometry and block unproven temporal/unit conversion; risk—area-version difference, model dependence, grid masks; open questions—raw soil scaling/full-month statistic, HRS day rule; next—inspect product contract; keywords—ClimateOS,T1,T2,T3,P04,410033,Geofabric,AWRA-L,provenance.
