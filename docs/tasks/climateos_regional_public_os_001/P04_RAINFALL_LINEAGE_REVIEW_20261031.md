# P04 rainfall-only continuation — bounded source review

**PARTIAL research progress; exact daily/monthly lineage remains BLOCKED. This bounded batch is stopped.** No new rainfall values, soil calculations, source substitution, scientific admission or cross-source join were produced. Baseline: `7940f3ab0c992cf1b406571d46ecce77bf81a26a`, independently accepted by the parent reviewer. Same cell (36.25°S, 149.10°E; NCI525/742), July2000, and previously captured monthly rainfall **11.300000190734863mm** are retained.

## What changed

An official **daily rainfall candidate exists** in the Bureau's Australian Water Data Service:

[awra_historical/physical_day_crf_multivariable_archive_1985_2004_data/ImageServer](https://image.wsapi.cloud.bom.gov.au/arcgis/rest/services/awra_historical/physical_day_crf_multivariable_archive_1985_2004_data/ImageServer).

Its public service directory and dimension metadata expose `rain_day`, units `mm`, regular one-day intervals spanning 1985-01-01 through 2004-12-31, Float32 pixels, EPSG4326 and approximately0.05° spacing. Grid extent is compatible with the NCI registration. This supports a candidate covering July2000; it does not establish complete valid values at the selected cell or equivalence to the exact NCI monthly revision.

The public metadata declares `noDataValue=3.4E38`, LERC2D compression and default Bilinear resampling, unlike the captured NCI fill value−999. Any future approved sample must explicitly preserve missingness, original spatial support and the sampling method; simply querying the displayed map is not adequate.

The Bureau's [precipitation explanation](https://awo.bom.gov.au/app/hydrovarinfo9.cbe9cb1a.chunk.js), discovered through the live AWO application's variable-info route, says that AWRA precipitation uses near-real-time daily climate grids and that monthly/annual precipitation aggregates those inputs. It distinguishes separate monthly climate grids that incorporate later additional rain-gauge observations. Thus a generic final monthly rainfall or a convenient AGCD/AWAP archive cannot be treated as the exact counterpart without documenting the input edition and processing history.

The [AWO data-access page](https://awo.bom.gov.au/about/overview/dataAccess) presents AWO downloads, AWDS services and NCI as access routes for the AWO data family. Its daily climate-input discussion also includes projections; it does not identify a historical July2000 input file or revision. The [NCI historical collection record](https://geonetwork.nci.org.au/geonetwork/srv/eng/catalog.search#/metadata/f0536_4866_6103_7890) documents historical AWRA-Lv7 outputs driven by Bureau climate forcing. These facts establish common provider/product-family context, **not an explicit mapping from this AWDS archive to the exact NCI `historical/v1/AWRALv7/processed/values/month/rain_day.nc` capture**.

The daily service's [metadata resource](https://image.wsapi.cloud.bom.gov.au/arcgis/rest/services/awra_historical/physical_day_crf_multivariable_archive_1985_2004_data/ImageServer/info/metadata) contains only a service title and generic/empty descriptive fields. Neither it nor the inspected service JSON declares the source rainfall file/edition, version of daily inputs, or transformation/revision linking it to the NCI monthly file. The common variable name, grid, time coverage and model-family declaration are insufficient to close that exact-source gap. No physical candidate sample was fetched merely to seek a coincidental numerical agreement.

## Exact blocked action and outcome

The AWO frontend points to its download inventory as the source of file selection. A read-only request for this inventory's schema was made:

`https://hosting.wsapi.cloud.bom.gov.au/arcgis/rest/services/Hosted/file_download_inventory_multivariable_all_data/FeatureServer/0?f=pjson`

The response was HTTP200 with an ArcGIS application error **499, `Token Required`**. The exact80-byte body, timestamp and SHA256 are retained. **Outcome: confirmed application-level access denial, not pending or uncertain.** This action was stopped without retry, token acquisition, credential lookup, permission changes or an alternate route to the restricted inventory. This was a provider response, not an automatic-approval-review rejection. The independent public service/documentation review above was completed within existing authorization.

The old NCI `rain_day_2000.nc.dds` 404 was **not retried**. Its saved receipt remains the evidence for that specific unavailable path; it must not be interpreted as absence of all official daily rainfall.

## Remaining source question — prepared, not sent

For the exact NCI historical/v1/AWRALv7 monthly `rain_day.nc` revision captured on2026-10-31 (Last-Modified2026-10-30 13:59:40GMT), which daily precipitation dataset/edition and processing revision generated July2000, and what documented public endpoint exposes those daily inputs at NCI cell525/742? Specifically, is AWDS `physical_day_crf_multivariable_archive_1985_2004_data` the matching input representation, with what revision, missing-value, time-label and resampling/compression rules?

A product-level public mapping or clarification is the missing evidence. A shared brand, similar filename, single matching monthly number or general AWRA-Lv7 reference does not establish the input revision. No provider contact, account/token request or payment was made. No Founder credential action is requested by this batch.

## Evidence, checks and resource use

[Manifest](evidence/p04_rain_lineage_20261031/manifest.json) records17 bounded public HTTP requests, exact source URLs, UTC timestamps, selected headers, lengths and SHA256 values;1,218,392 response-body bytes in total. **Zero physical sample requests, zero known404 retries and zero authenticated requests.** Eight complete service/collection/error responses and a derived [candidate-result.json](evidence/p04_rain_lineage_20261031/candidate-result.json) are committed. Website JavaScript bundles and an incomplete metadata prefix remain ignored local diagnostics; their original URLs and hash receipts are retained, without redistributing third-party application code.

One metadata request used an incorrect `returnDimensionValues=false` parameter and hit its512KiB body cap. That truncated prefix is not used as evidence. The [Esri API reference](https://developers.arcgis.com/rest/services-reference/enterprise/multidimensional-info/) specifies `always`, `never` or `ifIrregular`; a corrected `never` request returned complete62,256-byte dimension metadata. This was a bounded metadata correction, not a retry of the denied inventory or old404. No national physical dataset was downloaded.

Checks executed: hashes, byte lengths and completeness of all eight committed HTTP bodies; machine-readable candidate facts and application error; fixed cell/month identity; all new JSON parses; retained `scientific_admission=false`, absent daily sample and BLOCKED join. Existing soil result/code/tests remain unchanged. This documentation-only continuation adds no runtime code or dependency, so it does not repeat the soil experiment or claim a new local full-suite run. The previous reviewed533-test result belongs to baseline7940f3a; any new GitHub CI outcome is reported separately after push.

Generated outputs: this review, candidate JSON, source manifest/responses, execution-state and handoff updates. Producer is bounded official metadata discovery and deterministic extraction of the recorded source fields; no operational component or website consumes them. Raw evidence is immutable in this batch; failed/missing input is retained as failure, never zero data. Local probes are in ignored `.local/p04-rain-lineage-20261031`.

This stops the requested bounded search with an exact unresolved question. Resume the rainfall reproduction only when product-specific source mapping is supplied or established from new official evidence. The prior soil empirical result remains accepted; HRS daily/DST alignment, monthly QC/completeness and catchment numeric/scientific admission remain independently unresolved. Sitesv2, PR#130, WaterNSW credentials and schedules are untouched.
