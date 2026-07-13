# ClimateOS Task1561–1570 — Australian Regional Anchor Inventory v0.1

Date: 2026-07-14  
Status: DOCUMENTATION_COMPLETE / METADATA_ONLY / NON_EXECUTABLE  
Repository target: `simon947161/eco-agent-system`  
Branch target: `agent/task1500-unicm-coupling-roadmap`  
Draft PR: `#42`

## 1. Scope and control result

This inventory verifies public official metadata for Australian weather and
climate model products, climate drivers, observations and regional resources.
It does not retrieve a forecast, observation, model output, grid file or API
response. It does not diagnose current conditions or make a prediction for any
Australian place.

Control result:

- PR #42 was Draft, open and unmerged at entry;
- entry Head was `650e3357e74ae33ba0e1d5350b30d4f29e37c367`, identical to the transferred Head;
- Task1551–1560 was closed and Task1561–1570 had not been executed;
- all pre-entry PR changes were Markdown documentation;
- GraphCast remained `LATER`;
- no account, subscription, FTP session, cloud object, API, model, weight,
  executable or scientific dataset was accessed.

All sources below were accessed as public webpages or public document views on
2026-07-14. A link records metadata evidence; it is not permission to acquire
the linked data.

## 2. Australian anchor object taxonomy

| Object | Definition in this inventory | Must not be confused with |
|---|---|---|
| Model family | Named scientific modelling family, such as ACCESS | A particular release, chart or data feed |
| Model configuration | Named domain, resolution and deterministic/ensemble configuration | The provider's complete service |
| Analysis | Model state at the initialization time, commonly forecast hour 000 | Observation truth |
| Deterministic forecast | One forecast trajectory from a declared configuration | Probability distribution or official edited forecast |
| Ensemble forecast | Multiple trajectories used to represent a bounded class of uncertainty | Complete uncertainty or guaranteed probability |
| Public chart | Human-viewable rendering of selected model fields | Downloadable grid or official local forecast |
| Registered gridded product | Machine-readable fields distributed under product-specific access terms | Public-domain material or free commercial reuse |
| Official forecast grid | Bureau forecast product that may blend models, science and meteorologist input, such as ADFD | Raw ACCESS output |
| Reanalysis | Observation–model synthesis reconstructing past atmospheric states | Pure observation |
| Station observation | Measurement attached to a station, instrument, time and quality-control history | Area-wide grid-cell truth |
| Radar/satellite observation product | Remotely sensed signal or derived image/product | Direct surface measurement or forecast |
| Climate-driver information | Monitored index, phase, explanatory material or outlook about large-scale variability | A local forecast or impact diagnosis |
| Climate projection/scenario resource | Conditional future-climate experiment or downscaled projection | Weather forecast, observation or prediction for a particular site |

The Bureau's [ACCESS overview](https://www.bom.gov.au/australia/charts/about/about_access.shtml)
explicitly separates maps from gridded products. The [ACCESS NWP data page](https://www.bom.gov.au/nwp/doc/access/NWPData.shtml)
also distinguishes analysis time (`000`) from later forecast hours and states
that registered grids use GRIB2 or NetCDF-4.

## 3. ACCESS model-and-product metadata registry

### 3.1 Current public evidence

| Record | Role | Publicly documented version/status | Domain and nominal resolution | Time support | Output/access class | Evidence state |
|---|---|---|---|---|---|---|
| ACCESS-G | Deterministic global NWP configuration | APS4 | Global; about 12.5 km in chart summary; native grid documented as 0.17578125° longitude × 0.1171875° latitude, about 12 km mid-latitudes and 17 km tropics | Charts: 6-hour steps to 240 h; 00Z and 12Z runs listed | Selected public charts; registered GRIB2/NetCDF-4 grids | VERIFIED_METADATA |
| ACCESS-GE | Global NWP ensemble configuration | APS4 | Global; about 33 km | Public chart summary groups it with the 240 h horizon | Selected public charts; registered grids | VERIFIED_METADATA; member count not verified in this task |
| ACCESS-C | Deterministic city/regional NWP configurations | APS4 technical upgrade; products reported unchanged from APS3 | About 0.0135° / 1.5 km; domains around Sydney, Victoria/Tasmania, Brisbane, Perth, Adelaide, Darwin and North Queensland | Forecast charts/metadata: 3-hour steps to 36 h; analysis sequence 1-hour steps to 42 h; four run cycles listed | Gridded data only on chart overview; registered products | VERIFIED_METADATA |
| ACCESS-CE | City ensemble configurations | APS4 technical upgrade | About 0.0198° / 2 km on data page; about 2.2 km on chart page; same named city-domain set | Exact product horizon and ensemble size not independently verified | Registered gridded product; no public chart authority inferred | PARTIALLY_VERIFIED; resolution wording differs by official page |
| ACCESS-S2 | Coupled atmosphere–ocean–land–ice weekly-to-seasonal system | Bureau calls ACCESS-S2 the latest version and says it has produced seasonal outlooks since October 2021 | Global coupled system; spatial grid not verified here | 99-member real-time ensemble; weeks to seasons; hindcasts 1981–2018 named | Public outlook products; real-time data by request; research hindcast location named by Bureau | VERIFIED_METADATA; acquisition not assessed or attempted |
| ACCESS-A / ACCESS-AE | Proposed nationwide kilometre-scale deterministic/ensemble successors to ACCESS-C/CE | Bureau 2024–25 annual report says ACCESS-A will replace ACCESS-C; 2023–24 report described pre-operational trials for potential 2026 implementation | Nationwide kilometre scale, according to annual-report material | Operational cycle/horizon not verified | Future/transition product boundary unknown | UNVERIFIED_OPERATIONAL_STATUS; do not call operational |
| ACCESS climate/Earth-system configurations | Climate simulation/projection family use | Configuration-specific; not an APS4 weather-product synonym | Global coupled climate/Earth-system experiments | Multi-year to climate timescales | Research archives/experiments under separate terms | OUT_OF_CURRENT_PRODUCT_REGISTRY; exact configuration required |

Principal official sources:

- [About the ACCESS model](https://www.bom.gov.au/australia/charts/about/about_access.shtml)
- [ACCESS NWP Data Information](https://www.bom.gov.au/nwp/doc/access/NWPData.shtml)
- [ACCESS-S climate forecast system](https://www.bom.gov.au/government-and-industry/research-and-development/research-and-development-projects/access-s-climate-forecast-system)
- [About the Bureau's ACCESS-S long-range model](https://www.bom.gov.au/climate/ahead/about/model/access.shtml)
- [Bureau Annual Report 2024–25](https://www.bom.gov.au/sites/default/files/2025-10/bureau-of-meteorology-annual-report-2024-25-full%5B1%5D_0.pdf)
- [Bureau Annual Report 2023–24](https://www.bom.gov.au/sites/default/files/2024-10/bureau-of-meteorology-annual-report-2023-24.pdf)

### 3.2 Product separation rules

1. An ACCESS family name is not a product licence.
2. An APS4 version label does not mean all configurations have identical
   science changes; the Bureau says the C/CE move was a technical upgrade.
3. Public ACCESS charts expose selected fields and views, not the complete
   registered grid catalogue.
4. Registered grids are machine-readable products with their own access and
   licence conditions.
5. An ACCESS analysis is model/data-assimilation output, not a station
   observation.
6. ACCESS-S2 ensemble outlooks are not deterministic daily weather forecasts.
7. ADFD and MetEye are official forecast-product layers with blending and
   meteorologist input; they must not be relabelled raw ACCESS output.
8. ACCESS-A/AE remains blocked until an official operational notice and current
   product guide are verified.

## 4. Australian climate-driver source registry

This section registers definitions and metadata only. No current index value or
phase is reproduced.

| Driver | Official meaning/source object | Core metadata | Spatial/temporal meaning | Interpretation boundary |
|---|---|---|---|---|
| ENSO | Coupled Pacific Ocean–atmosphere cycle with El Niño, neutral and La Niña phases | Niño3/Niño3.4 SST anomaly is expressed in °C; SOI is a separate atmospheric index; Bureau monitoring combines ocean and atmosphere indicators | Tropical Pacific driver; typically seasonal-to-interannual influence | A phase is a broad climate influence, not a local rainfall, fire, water or asset forecast |
| IOD | Year-to-year contrast in tropical western and eastern Indian Ocean SST | Dipole Mode Index is west-minus-east SST anomaly in °C; official regions are 50–70°E, 10°S–10°N and 90–110°E, 10°S–0° | Indian Ocean driver, most meaningful in its active season | The index does not determine a location outcome; interactions and other drivers remain material |
| SAM | North–south movement of Southern Hemisphere mid/high-latitude westerly wind belt | SAM index/phase; exact dataset provenance and numeric unit require product-specific verification | Extratropical Southern Hemisphere; effects vary by Australian region and season | Predictability and impact vary; no direct site translation |
| MJO | Eastward-moving tropical pulse/cycle of wind, pressure, cloud and rainfall | RMM1/RMM2, phase and amplitude; operational monitoring uses daily series; typical recurrence 30–60 days | Tropical, weekly-to-monthly variability | Weak/strong index state is not a deterministic local event forecast |
| Climate Driver Update | Bureau synthesis page covering multiple drivers | Periodic monitoring/outlook narrative and linked charts | Broad Australian context | Bureau itself warns ENSO/IOD and other drivers are broad indicators and points users to long-range forecasts for local-pattern guidance |

Official sources:

- [El Niño and La Niña / ENSO](https://www.bom.gov.au/resources/learn-and-explore/climate-knowledge-centre/climate-factors/el-nino-and-la-nina)
- [ENSO monitoring indices](https://www.bom.gov.au/climate/enso/indices.shtml)
- [Indian Ocean Dipole knowledge page](https://www.bom.gov.au/resources/learn-and-explore/climate-knowledge-centre/climate-factors/indian-ocean-dipole)
- [IOD monitoring](https://www.bom.gov.au/climate/iod/)
- [Southern Annular Mode](https://www.bom.gov.au/climate/sam/)
- [Madden–Julian Oscillation monitoring](https://www.bom.gov.au/climate/mjo/)
- [Climate Driver Update](https://www.bom.gov.au/climate/enso/)

Freshness rule: definitions may be stable, but index construction, baseline,
threshold, update cadence, model panel and product presentation must be
rechecked at the time of any future use. Current conditions must never be
copied into a static registry as if they were enduring metadata.

## 5. Observation and regional-resource candidate inventory

| Candidate | Object class | Coverage/support | Public metadata finding | Access boundary | Permitted future anchor role |
|---|---|---|---|---|---|
| Climate Data Online (CDO) | Station archive interface | Point stations; daily/monthly observations and statistics | Location/station search and some free historical data | Public browsing/download for some data; extraction requests may attract charges | Station history and local validation candidate, subject to station metadata and QC review |
| Weather Station Directory and station metadata reports | Station metadata | Individual instrument sites | Detailed site PDFs and available-observation metadata | Public metadata; some data free, custom extraction charged | Provenance, relocation, instrument and record-availability anchor |
| ACORN-SAT | Homogenised reference network dataset | 112 selected Australian stations for long-term temperature monitoring | Designed for national long-term temperature trends | Dataset-specific terms apply | Climate-trend reference, not general local weather truth |
| AGCD monthly rainfall | Gridded analysis | Australia; gauge observations plus statistical modelling | Official monthly gridded rainfall analysis since September 2020, replacing monthly AWAP | Maps and some grids public; highest-resolution/special supply may require request | Continental/state/regional historical rainfall analysis; not a station observation |
| Daily rainfall grids / AWAP lineage | Gridded analysis | Australia; daily series from 1900 named in metadata | Current Bureau rainfall-map page says daily and monthly products have different dataset lineage | Product-specific metadata and download/request path | Historical daily rainfall candidate; exact version and resolution must be pinned |
| BARRA/BARRA2 | Regional reanalysis | 12 km Australian-region grid plus kilometre-scale Australian domains; hourly and some sub-hourly parameters | Observation–model synthesis with nearly 100 parameters | Data location and licence must be separately verified; no acquisition here | Past-weather atmospheric context and regional comparison, never pure observation |
| ADFD | Official forecast grid | Australia, about 3–6 km | Blend of Australian/international model data, science and meteorologist input; GRIB2/NetCDF, MetEye images and some WMS | Registered product/charges may apply; public MetEye view is a different object | Official forecast-product comparator in a future live-use gate |
| MetEye | Public visualisation | Locations across Australia | Displays observations and official forecasts; forecast blend updated routinely | Public viewer; display reuse/licensing separate | Human viewing and product discovery; not machine-readable evidence by implication |
| Weather radar network/images | Remote-sensing product | Radar-dependent footprints; new web display described as 1 km grid | Radar detects precipitation patterns; display resolution is not measurement accuracy | Public display; high-resolution/specialised content may require licence | Event-scale precipitation context after coverage, blockage, attenuation and QC review |
| Satellite-derived products | Remote-sensing/derived analysis | Broad Australian region | Product-specific algorithms; solar products explicitly derive estimates from satellite imagery | Public charts and specialised data have distinct terms | Cloud/radiation context with algorithm and licence provenance |
| Australian Water Outlook / AWRA-L | Modelled hydrological resource | National 0.05° (~5 km) daily landscape water balance in published model description | Soil moisture, runoff, evapotranspiration, deep drainage and precipitation are modelled variables | Website interface and registered/request pathways differ | Regional hydrological context; not observed soil moisture at a property |
| Climate averages/normals grids | Climatology | Australia, element-specific grids and baseline periods | Metadata gives units, resolution, generation and extent by element | Some grids public; special resolutions may be by request | Baseline context, not current observation or forecast |
| National/downscaled climate projections | Scenario/projection resource | Region and hazard dependent | Conditional ensemble/scenario evidence with bias-adjustment/downscaling methods | Separate project, data and licence gates | Long-horizon risk framing after scenario, model and expert review |

Official sources include [Climate Data Online](https://www.bom.gov.au/climate/data/),
[weather station metadata](https://www.bom.gov.au/climate/data/stations/about-weather-station-data.shtml),
[ACORN-SAT](https://www.bom.gov.au/climate/data/acorn-sat/),
[AGCD](https://www.bom.gov.au/climate/austmaps/about-agcd-maps.shtml),
[BARRA](https://www.bom.gov.au/government-and-industry/research-and-development/research-and-development-projects/atmospheric-reanalysis),
[ADFD user guide](https://www.bom.gov.au/catalogue/adfdUserGuide.pdf),
[MetEye FAQ](https://www.bom.gov.au/australia/meteye/includes/meteye-faq-body.html),
[weather radar knowledge](https://www.bom.gov.au/resources/learn-and-explore/radar-and-equipment-knowledge-centre/weather-radars),
and [Australian Water Outlook](https://awo.bom.gov.au/about).

## 6. Multiscale Australian support matrix

| Scale | Example | What the registered sources may support | What they cannot support directly | Minimum additional anchor/review |
|---|---|---|---|---|
| L2 continental | Australia | Broad circulation, national forecast/climate-product context, national gridded analyses | Uniform conditions across Australia or a local impact | Exact product/version, variable, period, verification and Australian meteorological review |
| L2.5 state/territory | NSW or NT | State-scale summaries and gridded context where product coverage exists | Subregional terrain, coast, catchment or asset response | State/regional observations, product skill and relevant domain review |
| L3 region | Riverina or Snowy Valleys | Candidate regional context from ADFD, BARRA, AGCD, stations and domain resources | A single grid cell as area truth; property/catchment impact | Regional station network, topography, hydrology/land evidence and qualified review |
| L4 locality | Sydney or Alice Springs | Location-centred official products and station/radar metadata; Sydney also lies within a named ACCESS-C domain | Exact street, suburb, infrastructure or ecosystem outcome | Local observations, product verification, exposure/vulnerability evidence and meteorologist |
| L5 site/project | Property, facility, catchment asset or project site | Question definition and source-discovery only | Prediction, design value, warning, impact, compliance or investment conclusion | Site instruments/survey, engineering/environmental data, lawful acquisition, uncertainty analysis and accountable domain professional |

### 6.1 Non-executable examples

#### Sydney

The ACCESS NWP data page names a Sydney ACCESS-C domain at about 1.5 km and an
ACCESS-CE city-ensemble family at about 2 km. This establishes product coverage,
not local accuracy. Coastal gradients, urban form and convective processes can
vary below or across grid support. A future Sydney question would need the
exact run/product, ADFD or official forecast layer, relevant station/radar
metadata, verification evidence and human meteorological interpretation.

#### Alice Springs

Alice Springs is not listed among the current ACCESS-C/CE city domains on the
official NWP metadata page. ACCESS-G, ADFD/MetEye, station observations and
regional satellite/radar availability may supply different layers of context.
None turns a global grid into a local arid-site conclusion. The future chain
must record sparse-network, land-surface, heat and terrain limitations.

#### Snowy Valleys

Snowy Valleys is not a named ACCESS-C domain. Complex elevation, snow, rain,
orographic flow, catchment hydrology and land cover make scale transfer
especially sensitive. ADFD's 3–6 km official grid and BARRA's 12 km regional
reanalysis can be candidates, but their grid spacing cannot resolve every
valley, slope or project site. Station, elevation, catchment, snow/hydrology and
local professional review are required.

#### Riverina

Riverina is not a named ACCESS-C domain. ACCESS-G, official forecast grids,
AGCD, stations and AWRA-L may provide distinct atmospheric, historical rainfall
and modelled water-balance perspectives. Irrigation, soils, land management,
heat and local rainfall variability require separate evidence. No regional
agricultural, water or infrastructure conclusion follows from a climate-driver
index or global model field alone.

## 7. Variable, unit, cadence and coordinate crosswalk

`UNVERIFIED` is intentional where the public page did not establish a single
product-wide field definition. A future acquisition gate must use the exact
product guide and file metadata.

| Canonical variable | Official objects located | Unit metadata verified here | Time support | Horizontal/vertical support | Blocking note |
|---|---|---|---|---|---|
| Air temperature | ACCESS 2 m and pressure levels; stations; ADFD; BARRA; climate grids | ACCESS chart unit not stated on overview; climate/station display often °C but exact machine field remains UNVERIFIED | Instantaneous/forecast-step, daily extrema, monthly averages depending object | ACCESS lat/lon; hybrid height or interpolated pressure levels; point stations; analysis grids | Do not silently convert K/°C or mix instantaneous, mean, max and min |
| Pressure | ACCESS MSLP and pressure-level fields; stations | hPa is documented for chart pressure levels; grid storage unit UNVERIFIED | Run/forecast step or observation cadence | Surface/MSL and pressure levels; ACCESS native hybrid-height coordinates | MSLP, surface pressure and level coordinate are different objects |
| Wind | ACCESS 10 m, gradient and pressure levels; stations; ADFD; BARRA | Exact grid units UNVERIFIED | Instantaneous/period/product specific | Vector with height/pressure support; point or grid | Speed, gust, direction and vector components are not interchangeable |
| Humidity | ACCESS relative humidity and 2 m dew point; stations; BARRA | Relative humidity normally percent but exact field contract UNVERIFIED | Product specific | 2 m and pressure levels named | RH, specific humidity and dew point require separate canonical fields |
| Precipitation | ACCESS 3/6-hour chart accumulation; ADFD 3-hour/daily grids; station rainfall; AGCD/AWAP; BARRA | ACCESS chart rainfall in mm; ADFD chance fields in %, threshold-specific; accumulation grids in product-defined units | Sub-hourly/hourly, 3/6-hour, daily, monthly and longer depending object | Point, grid cell, radar pixel and analysis grid | Preserve accumulation window, threshold, probability and analysis/forecast status |
| Sea-surface temperature | ENSO/IOD monitoring; ACCESS-S coupled system | Anomalies in °C for Niño and DMI products | Weekly/monthly/index-product specific | Defined ocean index boxes or coupled grid | Absolute SST, anomaly, relative index and baseline must not be mixed |
| Soil moisture | ACCESS-S initialization description; BARRA; AWRA-L/AWO | AWRA-L web metadata uses percent-full layers for some outputs; exact ACCESS/BARRA units UNVERIFIED | Daily/hourly/product specific | Layer depth and grid are product specific; AWRA-L about 0.05° | Modelled soil moisture is not an in-situ observation |
| Runoff/evapotranspiration/deep drainage | AWRA-L/AWO; BARRA includes evaporation | Published AWRA-L interfaces commonly use mm for fluxes; exact aggregation contract required | Daily/model period | National ~0.05° AWRA-L grid | Water-balance model output needs hydrological validation |
| ENSO indices | Niño3/Niño3.4 SST anomaly and SOI | Niño anomaly °C; SOI is an index, unitless treatment to be verified in exact record | Weekly/monthly and rolling SOI windows | Tropical Pacific boxes / station-pressure relationship | Threshold and baseline version must be pinned |
| IOD/DMI | West-minus-east SST anomaly | °C | Weekly/monthly/seasonal monitoring | Two defined Indian Ocean boxes | Seasonal applicability and baseline required |
| SAM index | SAM monitoring | Numeric index; exact normalization/unit UNVERIFIED | Daily/forecast-product specific | Hemispheric annular-mode representation | Dataset/provider and forecast source must be pinned |
| MJO RMM1/RMM2 | MJO phase-space monitoring | Dimensionless indices by scientific convention; official page does not state a physical unit | Daily series; 30–60 day characteristic recurrence | Tropical multivariate phase space, not a geographic grid | Phase/amplitude and source preprocessing must remain together |

ACCESS registered grids use evenly spaced latitude/longitude horizontally and
native hybrid-height coordinates vertically; pressure-level products are
interpolated or extrapolated from hybrid-height data. This transformation must
be recorded rather than hidden.

## 8. Access, licence, safety, cost and zero-cost matrix

| Source/product class | Access condition found | Licence/redistribution boundary | Cost surface | Zero-cost bounded path | Security/retention rule |
|---|---|---|---|---|---|
| Public Bureau webpages/charts | Unregistered browser access | General copyright/attribution rules; specialised content may be excluded | No access charge identified | Record metadata and direct link only | Do not scrape live products into the registry |
| Bureau Data Catalogue records | Metadata public | Each dataset has attribution, redistribution and commercial-use constraints | Catalogue defines unregistered free, registered free and charged classes | Use catalogue metadata without obtaining data | Preserve dataset-level terms; provider identity is not a blanket licence |
| ACCESS registered NWP grids | Registered User subscriber; FTP distribution named | Product-specific agreement/user guide | Possible subscription/charges; not accepted here | Public ACCESS chart and technical metadata only | No credentials, FTP, automated retrieval or retained grid |
| ADFD machine grids | NetCDF/GRIB2; registered-service details and charges referenced | Official forecast data terms; display and machine grids are separate | Possible registered-user charge | Public MetEye/guide metadata only | No WMS/API/FTP request; warnings remain authoritative public channel |
| Real-time data services | Subscription/registered service for forecast grids, satellite, radar and geospatial products | Data licence agreement | Paid service explicitly described | Public website viewing and static metadata | No account, trial, key, credential or live endpoint |
| CDO/station data | Some monthly/daily downloads free; custom extraction request available | Dataset/site-specific terms | Extraction charges possible | Public station directory and freely exposed metadata | Do not retain personal account/request details |
| Radar/high-resolution maps | Public display exists; specialised material may require licence | Bureau copyright page warns radar/high-resolution maps may be restricted | Licence/service cost possible | Record network/display metadata only | No image harvesting, republishing or operational feed |
| ACCESS-S2 real-time/hindcast data | Real-time data by request; research hindcast location named | Terms at supply/archive must be checked | Unknown until request; no request made | Public model/outlook metadata | No NCI/account access, data request or file retention |
| BARRA, AGCD, AWO and projections | Product/project-specific public, request, registered or archive paths | Exact record terms required | Free and charged pathways may coexist | Public method, resolution and lineage pages | No endpoint calls or bulk download |

The controlling official pages are [Data access and licences](https://www.bom.gov.au/metadata/catalogue/license.shtml),
[Bureau data services](https://www.bom.gov.au/resources/data-services),
and [Bureau copyright](https://www.bom.gov.au/copyright).

Safety controls for any future intake:

1. pin product ID, version, issue/valid time and licence;
2. use least-privilege credentials kept outside evidence records;
3. prohibit deserialisation of untrusted executable/model objects;
4. define storage, retention, deletion and redistribution before download;
5. estimate file volume, egress and requester-pays surfaces before access;
6. separate public warning channels from research data pipelines;
7. stop if terms require acceptance or payment not separately authorized.

## 9. Australian regional science and human responsibility map

| Decision point | Required human role | Responsibility | AI/registry boundary |
|---|---|---|---|
| Model/product identity | Bureau-source researcher or NWP specialist | Confirm exact configuration, cycle, domain, horizon and product status | May organise citations; cannot infer an undocumented version |
| Climate-driver interpretation | Australian climatologist/climate-mode scientist | Interpret index construction, interactions, seasonality and limits | Cannot turn driver phase into local outcome |
| NWP analysis/forecast use | Operational meteorologist/NWP specialist | Assess run, initialization, ensemble, skill and forecast-product relationship | Cannot issue or override official forecast/warning |
| Regional scale translation | Australian regional climatologist/meteorologist | Select defensible anchors and validation method | Finer grid cannot be treated as automatic local truth |
| Hydrology/water | Hydrologist/catchment specialist | Review rainfall–runoff, soil moisture, catchment and water-balance evidence | AWRA/BARRA output is not site measurement |
| Fire/ecology/agriculture | Relevant domain specialist | Review exposure, vulnerability, biological/land processes and consequences | No impact or management recommendation from atmospheric metadata |
| Infrastructure/project site | Engineer, planner and site-domain professional | Establish design basis, survey/site data, standards and accountable conclusion | Registry cannot supply design values or compliance sign-off |
| Data rights and governance | Licence/data-governance reviewer | Confirm use, redistribution, commercial and retention terms | Public visibility does not equal reuse permission |
| Security/cost | Security and financial owner | Approve credentials, endpoints, storage and cost ceiling | No autonomous account, subscription or paid retrieval |
| Final admission/use | Founder or delegated accountable authority | Authorize exact acquisition, experiment or decision use after scientific review | Documentation completion is not execution authority |

No reviewer was appointed and no scientific sign-off occurred in this task.

## 10. Inventory decision

The Australian anchor inventory is sufficient to support a later, separately
authorized **regional translation design** at the schema and validation-plan
level. It is **not** sufficient to execute regional translation, acquire data,
evaluate model skill or make a regional/local conclusion.

Readiness classification:

- object taxonomy: READY;
- ACCESS product metadata registry: READY WITH BLOCKERS;
- climate-driver registry: READY FOR METADATA USE;
- observation/resource candidate inventory: READY FOR SOURCE-SELECTION DESIGN;
- live or historical data intake: NOT AUTHORIZED;
- regional translation execution: PREMATURE;
- site/project conclusion: PROHIBITED WITHOUT NEW EVIDENCE AND ACCOUNTABLE REVIEW.

Material blockers:

1. ACCESS-A/AE operational release and exact product guide remain unverified;
2. registered product licences, charges and redistribution rights are
   product-specific and were not accepted;
3. exact machine-field names, units, ensemble membership, cadence and vertical
   coordinates require selected product guides/files;
4. location-specific station/radar coverage and verification were not queried;
5. no regional scientific reviewer or impact-domain reviewer has been assigned;
6. no acquisition, retention, security or cost plan is authorized.

## 11. Source register

All accessed 2026-07-14:

1. [About the ACCESS model](https://www.bom.gov.au/australia/charts/about/about_access.shtml)
2. [ACCESS NWP Data Information](https://www.bom.gov.au/nwp/doc/access/NWPData.shtml)
3. [ACCESS-S climate forecast system](https://www.bom.gov.au/government-and-industry/research-and-development/research-and-development-projects/access-s-climate-forecast-system)
4. [About long-range forecasts](https://www.bom.gov.au/climate/ahead/about/)
5. [ENSO knowledge page](https://www.bom.gov.au/resources/learn-and-explore/climate-knowledge-centre/climate-factors/el-nino-and-la-nina)
6. [ENSO monitoring indices](https://www.bom.gov.au/climate/enso/indices.shtml)
7. [IOD knowledge page](https://www.bom.gov.au/resources/learn-and-explore/climate-knowledge-centre/climate-factors/indian-ocean-dipole)
8. [IOD monitoring](https://www.bom.gov.au/climate/iod/)
9. [SAM monitoring](https://www.bom.gov.au/climate/sam/)
10. [MJO monitoring](https://www.bom.gov.au/climate/mjo/)
11. [Climate Data Online](https://www.bom.gov.au/climate/data/)
12. [Weather Station Directory](https://www.bom.gov.au/climate/data/stations/)
13. [ACORN-SAT](https://www.bom.gov.au/climate/data/acorn-sat/)
14. [AGCD maps and grids](https://www.bom.gov.au/climate/austmaps/about-agcd-maps.shtml)
15. [BARRA atmospheric reanalysis](https://www.bom.gov.au/government-and-industry/research-and-development/research-and-development-projects/atmospheric-reanalysis)
16. [ADFD user guide](https://www.bom.gov.au/catalogue/adfdUserGuide.pdf)
17. [MetEye FAQ](https://www.bom.gov.au/australia/meteye/includes/meteye-faq-body.html)
18. [Weather radars](https://www.bom.gov.au/resources/learn-and-explore/radar-and-equipment-knowledge-centre/weather-radars)
19. [Australian Water Outlook](https://awo.bom.gov.au/about)
20. [Data access and licences](https://www.bom.gov.au/metadata/catalogue/license.shtml)
21. [Data services](https://www.bom.gov.au/resources/data-services)
22. [Copyright](https://www.bom.gov.au/copyright)

## 12. Permanent non-executable boundary

This document is not a forecast, warning, climate diagnosis, model evaluation,
data licence, regional suitability decision or professional sign-off. It does
not authorize GraphCast, Task1571+, data acquisition, model execution,
downscaling, regridding, an API, an account, payment or PR merge.
