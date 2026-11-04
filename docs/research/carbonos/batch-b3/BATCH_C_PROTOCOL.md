# Batch C protocol refinement — PROPOSAL_ONLY

No calculations or numerical experiments performed. Supplements [B2 protocol](../batch-b2/BATCH_C_PROTOCOL_ADDENDUM.md) and [Batch B protocol](../batch-b/EXTREME_CLIMATE_MULTIGAS_RESEARCH_PROTOCOL.md); does not alter AWT statutory formulae, scientific admission or accounting rules. The choices below are proposed research design, not established findings for these facilities.

## Questions and separated boundaries

| Stream | Response to observe later | Required controls / accounting separation |
|---|---|---|
| CH4 | generation, oxidation, collection, destruction, fugitive/effluent emissions as separate flows | organic load/age, actual reactor/landfill temperature and water, redox, cover, collection downtime, dissolved storage and transport; generation is not atmospheric emission |
| N2O | measured process and effluent-related flux with explicit system boundary | total N/ammonium/nitrite, aeration/DO, pH, temperature, residence time; do not infer N2O from CH4 or generic sewage throughput |
| CO2 | measured biogenic and fossil contributions recorded separately | carbon origin, combustion/oxidation, external fuel and material boundary; biogenic classification does not erase physical atmospheric flux |
| Energy | metered imported electricity/fuel; exported energy separately | factor jurisdiction/year/version and time basis; no automatic avoided-emissions credit or double counting flare heat as grid output |
| Refrigerants | optional separately inventoried leakage | equipment/refrigerant type and measured or documented loss; no default zero from missing records |

Gas masses retain original units and species. A later optional CO2e view would require named GWP source, assessment version and time horizon; no conversion or totals in this batch. Research mass-flow diagrams are not AWT legal equations. No parameter values are assigned from media reports.

## Spatial and temporal contract

Require verified site/physical-unit identity before linking a station, raster or catchment. Preserve original CRS, transform version, positional accuracy and feature role. A pipeline marker, outfall, reporting address or station is not a reactor coordinate. No spatial join while facility location is UNKNOWN. Record station distance/elevation/context, raster resolution and land/water representativeness only when data exist. Air temperature is a proxy, not water or landfill-body temperature; validate lag and bias with facility observations.

Store UTC timestamp, Australia/Brisbane local clock for these QLD candidates, interval start/end, observation frequency, accumulation convention and missingness; never shift a 24-hour rain total into an instantaneous observation. A future NSW comparator must handle Australia/Sydney DST explicitly. Align gas sampling/flow intervals, electricity meters, load, weather and maintenance logs before aggregation. Retain source timezone and revisions.

ENSO/IOD/SAM are potential broad-scale covariates, not local emissions causes. Separate observed indices from forecasts; store provider, issue date, valid period, lead time, revision/retrieval time. No future information in retrospective predictors. No inference that a climate-index phase proves a local event.

## Event design proposed for review, not executed

Pre-register event thresholds, reference climatology and dataset vintage before reading gas outcomes. Heat: propose local season-adjusted upper percentile plus minimum duration, with values to be justified and frozen by reviewer. Rain/flood: separate station/raster rainfall exceedance from observed site inundation; drought: distinguish rainfall deficit from process water limitation. Compound heat-drought/flood-power-loss events need separate definitions. Numeric thresholds and lag lengths remain UNSET, not tuned after viewing results.

Define pre-event baseline, event and recovery windows relative to each site's process residence time and gas transport/storage. Proposed lag sensitivity ranges must be justified physically and pre-specified before experiments. Compare within-site matched seasonal/control periods and, only if comparable, another site with similar process/loads. Control for waste composition/age, load, residence time, aeration, cover changes, maintenance, electricity outage and collection upgrades. West-to-South diversion and flare commissioning are structural changes, not weather effects. A South sewage versus Lakes Creek landfill comparison cannot identify a climate effect independent of process type.

## Quality, inference and uncertainty gates

Use calibration records, detection limits, sample support, flow alignment and completeness by event/season. Non-detect is censored, not zero. Missing data and downtime remain flagged; no imputation across event or plant shutdown without a reviewed method. Report uncertainty from sensor, sampling, source age, temporal alignment, spatial representativeness and model structure separately. Avoid pseudo-replication of repeated samples and selection of only events with observed peaks. Plan blocked time validation and a held-out event/site only once adequate data exist. Association would not establish climate-change attribution or local climate improvement.

STOP if identity, legally usable inputs, operational context, units/time support or required measurement quality are unresolved. A bounded later experiment requires a frozen protocol, authorised public data manifest, reviewed model/parameters, uncertainty plan, replay script and explicit Founder approval. Current candidates fail the measurement/geometry gate. No model fitting, simulation, emissions estimation or climate-data ingestion runs now.

## Reuse and next review

Reuse P1-A formula/source registry and Evidence Passport concepts, B2 entity separation, existing ClimateOS time-series/GIS tools and EcoEngine meteorological lineage after compatibility review. Register gaps instead of new infrastructure. No new database, agent service or collector. ChatGPT should review confounding, event definitions, gas boundaries and stop rules; Founder decides whether to authorise any later experiment. P1-A scientific admission remains PENDING.
