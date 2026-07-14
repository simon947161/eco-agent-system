# ClimateOS Scale-Aware Wind Claim Evidence Protocol v0.1

Date: 2026-07-14  
Status: DOCUMENTATION_COMPLETE / NON_EXECUTABLE / NO_WIND_CONCLUSION  
Task: ClimateOS Task1581–1590

## 1. Decision

The first bounded Australian regional claim class is:

`SCALE_AWARE_WIND_TRANSLATION`

Its purpose is to prevent ClimateOS from treating planetary circulation,
modelled 10 m wind, wind gust, station wind, regional reanalysis, an official
forecast grid and a site design wind as interchangeable.

The protocol answers only:

> What evidence identity and validation chain would be required before a wind
> statement could be supported at a declared Australian scale?

It does not answer where, when or how strongly the wind blows.

## 2. Admissible and prohibited claims

| Claim class | Meaning | Status under this protocol |
|---|---|---|
| Circulation context | Broad hemispheric or continental flow regime | DESIGNABLE with exact source and period |
| Regional wind regime | Recurring regional flow characteristics | DESIGNABLE; requires historical evidence and review |
| Model field statement | Exact configuration/run/level/time wind field | METADATA READY; data use not authorized |
| Official forecast-grid statement | Exact ADFD element, issue and valid time | METADATA READY; live use not authorized |
| Station observation statement | Exact station, instrument/exposure and time statistic | METADATA READY; observation retrieval not authorized |
| Reanalysis statement | Historical model–observation synthesis at declared grid/level | METADATA READY; acquisition not authorized |
| Local-process hypothesis | Sea breeze, valley flow, downslope flow or urban effect | QUESTION ONLY; requires targeted evidence |
| Site wind-resource claim | Hub-height distribution, yield or turbine suitability | PROHIBITED |
| Structural/design wind | Code-defined design action or safety value | PROHIBITED; accountable engineer and governing standard required |
| Current warning or hazard | Operational safety statement | PROHIBITED; official warning services remain authoritative |

## 3. Official source-object register

All sources were accessed as public metadata on 2026-07-14. No linked data or
sample file was opened or downloaded.

| Object | Wind support recorded in official metadata | Role | Boundary |
|---|---|---|---|
| ACCESS-G APS4 | Global NWP; about 12 km mid-latitudes; 10 m wind, gusts and multi-level wind products are named | Continental/synoptic model context | Registered grids; not station truth or local terrain truth |
| ACCESS-C APS4 | Named city domains at about 1.5 km, including Sydney; 10 m and model-level wind products are named | City-domain process hypothesis and model comparator | Coverage is not accuracy; no Alice Springs, Snowy Valleys or Riverina named domain |
| ACCESS wind coordinates | Zonal/meridional components; 10 m, rho, hybrid-height and interpolated pressure-level products | Exact vertical/object identity | Interpolation and staggered-grid handling must be recorded |
| ADFD User Guide v23 | Official forecast grids at about 3–6 km; hourly wind magnitude/direction and several sustained-wind time semantics | Official forecast-product comparator | Blend of models, science and meteorologist input; not raw ACCESS |
| BARRA2/BARPA metadata | 12 km Australian-region and kilometre-scale domains; hourly and some sub-hourly parameters including wind speed/direction | Historical regional atmospheric context | Reanalysis is not pure observation and is not a site measurement |
| Weather Station Directory | Station/site metadata, element availability and record completeness | Observation provenance and future validation anchor | A point record may contain gaps and exposure/site changes |
| Terrain, land cover and roughness records | Topography, surface stress, roughness and land-mask fields are named in ACCESS metadata | Representativeness/context candidates | A model surface field does not replace a site survey |

Controlling sources:

- [ACCESS NWP Data Information](https://www.bom.gov.au/nwp/doc/access/NWPData.shtml)
- [ADFD User Guide v23](https://www.bom.gov.au/catalogue/adfdUserGuide.pdf)
- [Bureau atmospheric reanalysis](https://www.bom.gov.au/government-and-industry/research-and-development/research-and-development-projects/atmospheric-reanalysis)
- [About Weather Station Data](https://www.bom.gov.au/climate/data/stations/about-weather-station-data.shtml)

## 4. Wind evidence identity contract

Every wind evidence object must carry all applicable fields:

```yaml
wind_evidence_identity:
  evidence_id:
  provider:
  object_class: [model, forecast_grid, reanalysis, station, climatology]
  product_and_version:
  access_and_licence_state:

  wind_quantity:
    representation: [u_v_components, speed, direction, gust]
    vertical_support:
    reference_height_agl:
    pressure_or_model_level:
    averaging_period:
    statistic: [instantaneous, sustained, maximum, mean, percentile]
    unit:
    direction_convention:

  temporal_support:
    analysis_issue_or_observation_time:
    valid_time_or_period:
    cadence:
    accumulation_or_window:

  spatial_support:
    geometry: [point, grid_cell, domain]
    horizontal_grid_or_station_id:
    coordinate_reference:
    terrain_representation:
    land_sea_treatment:
    exposure_and_roughness_metadata:

  evidence_state:
  uncertainty_and_gaps: []
  prohibited_uses: []
  human_review_state:
```

Missing height, averaging period, unit, statistic or time support blocks the
claim. The label `wind` alone is never sufficient.

## 5. Variable and time-semantics crosswalk

| Object | Quantity | Height/level | Time semantic | Unit metadata | Non-equivalence rule |
|---|---|---|---|---|---|
| ACCESS `wind.10m` | Zonal and meridional wind components | 10 m above model ground | Exact forecast step/analysis time | Exact file unit requires selected product metadata | Components are not speed/direction until an authorized calculation |
| ACCESS group2 gust | Wind gust | 10 m named | Product-specific | UNVERIFIED without exact field guide | Gust is not sustained wind |
| ACCESS rho/model wind | Wind components | Native hybrid/rho levels | Exact model step | Product-specific | Model-level wind is not 10 m or hub-height wind |
| ACCESS pressure wind | Interpolated/extrapolated wind | Standard pressure level | Exact model step | Product-specific | Pressure-level wind is not surface wind |
| ADFD `Wind_Mag_SFC` | Sustained wind speed | 10 m AGL | Specified time; hourly grid | GRIB2 m/s; NetCDF knots | Format changes the declared unit |
| ADFD `WindOnHour` | Expected sustained wind at timestamp | 10 m AGL | Start of hour | knots or km/h product | Not the maximum sustained wind within the hour |
| ADFD `WindMaxInHour` | Expected maximum sustained speed within hour | 10 m AGL | 60-minute period centred on timestamp | knots or km/h product | Still 10-minute sustained wind, not a gust |
| ADFD `Wind_Dir_SFC` | Wind direction | Surface/10 m context | Hourly | degrees true | Circular quantity; arithmetic error treatment is invalid |
| Station wind | Observed speed/direction or maximum gust | Instrument/site specific | Minute/hourly/daily record dependent | Exact element metadata required | Point exposure and record completeness control representativeness |
| BARRA wind | Reanalysis speed/direction or components | Product/level specific | Hourly or sub-hourly | Exact archive metadata required | Synthesis field is not observation truth |

The ADFD guide defines its sustained wind speeds as 10-minute averages at 10 m
above ground. It separately distinguishes wind at the timestamp from maximum
sustained wind within the hour. These semantics must travel with every value.

## 6. Scale-support matrix

| Scale | Permissible future question | Minimum evidence chain | Unsupported leap |
|---|---|---|---|
| Hemispheric/planetary | What broad circulation context is relevant? | Exact circulation/climate-driver source, period and climatologist | Direct local wind speed or hazard |
| Australian continent | What synoptic/continental wind pattern is represented? | ACCESS-G or equivalent exact product plus observations/reanalysis and NWP review | Uniform Australian wind regime |
| State/large region | What regional gradients or regimes merit testing? | Regional forecast/reanalysis, station network, terrain and stratified validation | One global grid cell as region truth |
| Sydney/coastal metro | Can coastal/urban flow hypotheses be evaluated? | ACCESS-C Sydney, ADFD, stations, coastline/terrain/roughness and meteorologist | Street, building or airport conclusion |
| Alice Springs/arid locality | Can broad inland flow be distinguished from local exposure? | Global/official grid, station metadata, terrain/roughness and sparse-network review | Treating absence of ACCESS-C as absence of evidence or as permission to downscale |
| Snowy Valleys/complex terrain | Can ridge, valley and synoptic regimes be separated? | Terrain-aware regional sources, multiple elevations/stations and specialist review | Grid spacing as resolved valley wind |
| Riverina/production landscape | Can regional pressure/flow regimes be compared with observed exposure? | Regional grid/reanalysis, station network, land cover and seasonal stratification | Farm, crop, spray or infrastructure advice |
| Site/project | What additional measurements and standards are required? | Site instrumentation/survey, governing standard, engineering/domain owner | Any design, yield, safety or compliance value from this protocol |

## 7. Non-executable alignment plan

A future authorized study would have to pre-register:

1. exact claim, geography, period, height and statistic;
2. exact product/version and machine-field identity;
3. station eligibility, instrument/exposure history and completeness threshold;
4. grid-to-point method without assuming the station represents the grid cell;
5. terrain-height, land/sea, surface-roughness and urban-form differences;
6. temporal matching, including sustained, maximum-in-hour and gust semantics;
7. treatment of direction as circular data and calm/variable cases;
8. independent validation and holdout periods;
9. stratification by season, hour, synoptic regime and terrain/exposure class;
10. uncertainty propagation and stop rules.

No interpolation, conversion, collocation or calculation is performed here.

## 8. Candidate validation measures

Metrics are registered as a future plan, not computed results.

| Target | Candidate measures | Required caution |
|---|---|---|
| u/v components | Bias, MAE, RMSE, correlation | Same coordinate convention and height required |
| Wind speed | Bias, MAE, RMSE, quantile error | Calm and high-wind regimes must be stratified |
| Direction | Circular mean error and circular dispersion | Undefined/unstable direction near calm requires a rule |
| Gust or hourly maximum | Quantile bias, exceedance contingency measures | Match gust versus sustained definitions exactly |
| Probabilistic wind | Reliability, Brier score, rank/PIT diagnostics where applicable | Ensemble membership and event threshold must be pinned |
| Spatial structure | Gradient, regime and neighbourhood diagnostics | Finer grid is not automatic truth; avoid pointwise-only claims |

No single score admits a product. A result must be reported by region, regime,
height, statistic, lead time and evidence quality.

## 9. Uncertainty and failure gates

The future workflow must return `BLOCKED` or `INCOMPARABLE` when any material
condition applies:

- unknown product/version, unit, height, averaging period or time window;
- incompatible sustained-wind and gust definitions;
- insufficient station metadata, completeness or exposure history;
- terrain elevation or roughness mismatch not bounded;
- coastal land/sea treatment changes the meaning of a grid cell;
- pressure/model-level wind is substituted for 10 m or site wind;
- direction convention or calm handling is missing;
- model, ADFD and reanalysis objects are conflated;
- validation sample is too sparse for the declared class;
- an engineering, safety, energy-yield or operational claim is requested;
- required licence, cost, security or human approval is absent.

## 10. Human and governance gate

| Gate | Accountable role |
|---|---|
| Product and coordinate identity | Australian NWP specialist |
| Wind observation and station representativeness | Meteorologist/observation specialist |
| Climate/regime interpretation | Australian climatologist |
| Complex terrain or boundary-layer interpretation | Boundary-layer/mesoscale specialist |
| Fire, aviation, marine, energy or infrastructure use | Named domain professional |
| Site/design use | Accountable engineer and applicable governing standard |
| Licence and redistribution | Data-governance reviewer |
| Credentials, storage and endpoints | Security owner |
| Cost ceiling | Financial owner |
| Acquisition or execution admission | Founder or delegated accountable authority |

The AI may organise evidence and expose incompatibilities. It may not certify a
wind product, issue a warning or sign a professional conclusion.

## 11. Access, cost and zero-cost boundary

- Public official metadata pages and documents are the current zero-cost path.
- ACCESS machine grids remain registered-user products; FTP links and sample
  data were not accessed.
- ADFD machine products retain product-specific access and licence conditions.
- BARRA archives and station observations require a later exact acquisition
  and licence decision.
- No account, credential, request, subscription, storage allocation or paid
  commitment was created.

## 12. Readiness decision

`WIND_CLAIM_EVIDENCE_PROTOCOL_READY / ACQUISITION_VALIDATION_AND_USE_BLOCKED`

ClimateOS now has a defensible design for asking a scale-aware wind question.
It does not yet possess or authorize the evidence needed to answer one.
