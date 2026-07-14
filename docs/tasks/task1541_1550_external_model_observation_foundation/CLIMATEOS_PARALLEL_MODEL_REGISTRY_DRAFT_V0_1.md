# ClimateOS Parallel Model Registry Draft v0.1

Date: 2026-07-14

Status: DRAFT / DOCUMENTATION-ONLY / NON-EXECUTABLE / FOUNDER REVIEW REQUIRED

## 1. Purpose

The ClimateOS Parallel Model Registry records external scientific models as
bounded computational perspectives. It allows ClimateOS to compare what each
model represents, at which scale, by which mechanism, with which variables and
forcings, and under which evaluation and regional-use limits.

The registry is model-neutral. It does not make UniCM, NeuralGCM, GraphCast or
any other candidate the ClimateOS default model.

The registry supports the Multiscale Parallel Model Perspective:

> An external model is a partial computational world. ClimateOS reads its
> assumptions, mechanisms, scales, strengths and blind spots, then compares
> those bounded readings with other models, observations and human science.

## 2. Non-purpose and current boundary

Draft v0.1 is a human-readable research contract. It is not:

- a runtime registry, database, API, adapter or orchestration service;
- an authorization to clone, download, install or execute a model;
- an authorization to obtain weights, checkpoints or scientific datasets;
- a ranking engine, automatic selector or model router;
- a scientific-validation or operational-admission decision;
- a weather service, warning system or climate projection service;
- a substitute for an evaluation framework, authoritative observation source,
  regional model or qualified scientist;
- an authorization for GraphCast or any other third model to enter active
  research.

No external asset, runtime, live data connection, account or paid commitment is
created by this document.

## 3. Architecture position

```text
Official sources and fixed revisions
             |
             v
Parallel Model Registry -------- Model identity, mechanism and scale
             |
             +---- Evaluation Framework Registry
             |
             +---- Data Resource Registry
             |
             v
Parallel Comparison Record ------ Agreement, divergence and incomparability
             |
             v
Regional evidence and human scientific review
             |
             v
Founder-gated admission decision
```

Registration, evaluation, comparison, acquisition, execution and admission are
separate actions. Completion of one never authorizes the next.

## 4. Registry object types

Draft v0.1 defines four linked record types.

| Object type | Purpose | Must remain separate from |
|---|---|---|
| `MODEL_RECORD` | Describes one model family, version or checkpoint-specific computational perspective | Evaluation score, dataset licence and operational approval |
| `EVALUATION_FRAMEWORK_RECORD` | Describes how one class of claim may be tested | The model being evaluated and the data used as reference truth |
| `DATA_RESOURCE_RECORD` | Describes a dataset, product family, catalogue or authoritative observation resource | Model identity, model output and automatic fitness decisions |
| `PARALLEL_COMPARISON_RECORD` | Records a bounded comparison between two or more model claims | Model merging, averaging, ranking or automatic selection |

### 4.1 Required relationship types

| Relationship | From | To | Meaning |
|---|---|---|---|
| `TRAINED_ON` | Model | Data resource | Data contributed to parameter learning |
| `INITIALIZED_FROM` | Model | Data resource | Data provides an initial state |
| `FORCED_BY` | Model | Data resource | Data supplies external boundary or forcing values |
| `EVALUATED_BY` | Model or model claim | Evaluation framework | Framework defines an evaluation protocol |
| `COMPARED_AGAINST` | Model or output | Model, baseline or data resource | Bounded comparison reference |
| `REGIONALLY_CHECKED_AGAINST` | Model claim | Data resource or official product | Regional applicability anchor |
| `IMPLEMENTS_OR_REFERENCES` | Model | Paper, repository or method | Scientific and code lineage |
| `PRODUCES` | Model configuration | Output variable or product | Configuration-specific output contract |
| `TRANSLATED_BY` | Model claim | Future governed method | Global-to-regional or cross-variable translation |
| `REVIEWED_BY` | Record or claim | Human-review role | Named responsibility, not automated authority |

Relationships require evidence references and review status. A relationship
must not be inferred only because two resources use similar variable names.

## 5. Controlled status vocabularies

### 5.1 Evidence status

| Status | Meaning |
|---|---|
| `UNVERIFIED` | No current authoritative evidence has been inspected |
| `CANDIDATE_SOURCE` | A possible source has been identified but not authenticated |
| `OFFICIAL_SOURCE_VERIFIED` | Ownership and authoritative location have been checked |
| `VERSION_PINNED` | Exact release, tag or commit is recorded |
| `DECLARED_BY_PROVIDER` | Statement is recorded from the provider but not independently reproduced |
| `PUBLISHED_CLAIM` | Statement is supported by a paper but not reproduced by ClimateOS |
| `METADATA_VERIFIED` | Public metadata has been checked without acquiring the asset |
| `ASSET_INTEGRITY_VERIFIED` | A separately authorized bounded asset has passed integrity checks |
| `CLIMATEOS_REPRODUCED` | A separately authorized experiment reproduced a specified result |
| `EXTERNALLY_REVIEWED` | A named qualified reviewer has completed the declared review |
| `DISPUTED` | Material counter-evidence or unresolved disagreement exists |
| `SUPERSEDED` | A newer governed record replaces this record |

`PUBLISHED_CLAIM` and `DECLARED_BY_PROVIDER` must never be rendered as
`CLIMATEOS_REPRODUCED`.

### 5.2 Research priority

| Priority | Meaning |
|---|---|
| `NOW` | Read-only research is currently justified and within an authorized package |
| `LATER` | Potentially useful after named prerequisites are complete |
| `WATCH` | Track scientific, access, licence or maturity developments; no active work |
| `NOT_SUITABLE` | Not suitable for the stated registry role; reason and review date required |

Research priority does not authorize acquisition, execution or admission.

### 5.3 Lifecycle and admission state

| State | Meaning |
|---|---|
| `INVENTORY_ONLY` | Candidate name only; no scientific fitness conclusion |
| `SOURCE_ORIENTATION` | Official public sources are being read |
| `SOURCE_VERIFIED` | Required source identity and fixed revision are recorded |
| `ACQUISITION_MANIFEST_READY` | A non-executable asset and security plan exists |
| `SOURCE_ACQUIRED_ISOLATED` | Source-only acquisition was separately authorized and verified |
| `ASSET_ACQUISITION_AUTHORIZED` | Founder has authorized named weights or data under hard limits |
| `EXECUTION_AUTHORIZED` | Founder has authorized a named bounded experiment |
| `RESEARCH_EXECUTED` | Authorized experiment completed; no fitness implied |
| `EVALUATION_REVIEWED` | Results and protocol received scientific review |
| `REGIONALLY_ADMITTED` | Named regional claim class was explicitly admitted after local validation |
| `OPERATIONALLY_ADMITTED` | Named operational use was explicitly admitted by competent authority |
| `BLOCKED` | A named control prevents progress |
| `REJECTED` | Evidence supports exclusion from a named use |
| `RETIRED` | Record is no longer active and has a replacement or closure reason |

No state transition is automatic. Draft v0.1 creates no transition beyond
documentation-level orientation.

## 6. Model Record schema

Every model record must identify whether it describes a family, source release,
checkpoint, service product or configuration. Claims from one level must not be
silently inherited by another.

### 6.1 Identity and provenance

| Field | Requirement |
|---|---|
| `model_id` | Stable ClimateOS identifier |
| `record_level` | `FAMILY`, `RELEASE`, `CHECKPOINT`, `SERVICE_PRODUCT` or `CONFIGURATION` |
| `name` | Official model name |
| `aliases` | Names, abbreviations and prior repository names |
| `provider_or_maintainer` | Responsible organization or maintainers |
| `scientific_purpose` | Bounded scientific question the model addresses |
| `model_class` | Controlled mechanism class or classes |
| `canonical_paper` | DOI or authoritative publication reference |
| `canonical_repository` | Official repository URL, if public |
| `documentation_url` | Official documentation location |
| `version` | Release or package version; `UNVERIFIED` when absent |
| `source_revision` | Exact tag and commit SHA |
| `source_verification_date` | Date of current-source inspection |
| `code_licence` | Exact licence and evidence status |
| `weight_licence` | Exact checkpoint licence and evidence status |
| `data_terms_dependency` | Required third-party data terms |
| `source_access` | Public, registration, request, restricted, paid or unknown |
| `evidence_references` | Paper, repository, documentation and review records |
| `record_owner` | ClimateOS human responsibility role |
| `review_state` | Draft, reviewed, disputed, superseded or closed |

### 6.2 Scale

| Field | Requirement |
|---|---|
| `geographic_domain` | Global, continental, regional, city, site or other bounded domain |
| `native_horizontal_representation` | Grid, mesh, spectral form, regional boxes or other support |
| `native_horizontal_resolution` | Resolution and configuration dependency |
| `vertical_representation` | Pressure, sigma, hybrid, height, surface-only or not applicable |
| `vertical_levels` | Number and definition where verified |
| `native_time_step` | Numerical or learned transition step where verified |
| `input_cadence` | Cadence of input states |
| `input_history` | Required historical context |
| `forecast_or_simulation_horizon` | Checkpoint- and task-specific horizon |
| `output_cadence` | Frequency of retained output |
| `training_time_coverage` | Training period and exclusions |
| `evaluation_time_coverage` | Held-out or evaluation period |
| `scale_validity_statement` | Claims that are meaningful at the declared scale |
| `scale_transfer_prohibition` | Finer-scale or longer-horizon claims that are not supported |

Degrees, kilometres, grid cells, region boxes and named locations must not be
treated as interchangeable units of spatial support.

### 6.3 Mechanism

| Field | Requirement |
|---|---|
| `mechanism_class` | `PHYSICS_NUMERICAL`, `HYBRID_PHYSICS_ML`, `DATA_DRIVEN`, `FOUNDATION_MODEL`, `STATISTICAL`, `DOWNSCALING`, `OBSERVATION_TRANSLATION`, `ORCHESTRATION_REFERENCE` or `OTHER` |
| `represented_system` | Atmosphere, ocean, land, coupled modes, waves, chemistry or other system |
| `explicit_equations_or_rules` | Verified resolved equations or deterministic rules |
| `learned_components` | Learned dynamics, tendencies, encoders, decoders, attention or other components |
| `coupling_location` | Where components, variables or domains interact |
| `stochasticity` | Deterministic, stochastic, ensemble construction or unknown |
| `data_assimilation_role` | None, initialization-only, learned, external, coupled or unknown |
| `mechanism_evidence_status` | Published, source-mapped, reproduced or disputed |
| `interpretability_boundary` | What internal values can and cannot support |
| `causal_status` | Explicitly distinguishes causal mechanism, physical constraint, learned association and diagnostic |

Attention, feature importance, learned tendency and forecast agreement are not
causal proof unless a separately reviewed causal design supports that claim.

### 6.4 Variables and transformations

Each variable must be a separate entry, not an unqualified name in prose.

| Field | Requirement |
|---|---|
| `canonical_variable_name` | ClimateOS canonical label |
| `source_variable_name` | Exact upstream name |
| `role` | `PROGNOSTIC`, `DIAGNOSTIC`, `INPUT`, `FORCING`, `TARGET`, `OUTPUT`, `STATIC` or `MASK` |
| `physical_quantity` | Scientific interpretation |
| `unit` | Native and output units |
| `vertical_support` | Surface, level, column, integrated or other |
| `spatial_support` | Native grid, region or aggregation |
| `temporal_support` | Instantaneous, accumulated, mean or other interval |
| `normalization` | Verified normalization or standardization |
| `transformation` | Regridding, interpolation, anomaly, index derivation or other operation |
| `missing_value_and_mask_rule` | Masking and imputation behaviour |
| `configuration_scope` | Family, release, checkpoint or configuration |
| `evidence_status` | Source of the variable declaration |
| `comparison_compatibility` | Direct, transform-required, conceptual-only or incomparable |

Matching names do not establish matching units, grids, averaging windows,
reference climatologies or physical meaning.

### 6.5 Initialization and forcing

| Field | Requirement |
|---|---|
| `initial_state_source` | Exact data resource and version |
| `boundary_forcings` | External forcing variables and providers |
| `static_fields` | Orography, land-sea mask and other fixed fields |
| `forcing_update_cadence` | Persistence, observed history, scenario or forecast cadence |
| `forcing_scenario` | Historical, prescribed, forecast, counterfactual or unknown |
| `coordinate_mapping` | Source-to-model coordinate transformation |
| `preprocessing_revision` | Exact script or method revision |
| `forcing_uncertainty` | Known uncertainty and propagation method |
| `missing_forcing_behaviour` | Error, persistence, fallback or unknown |
| `coupling_boundary` | Components that are externally prescribed rather than dynamically simulated |

### 6.6 Evaluation links

| Field | Requirement |
|---|---|
| `claim_being_evaluated` | Exact claim unit and configuration |
| `evaluation_framework_ids` | Links to independent framework records |
| `truth_or_reference_resource_ids` | Links to data-resource records |
| `baseline_ids` | Models, climatology or operational references |
| `metrics` | Exact metric definitions |
| `regridding_and_alignment` | Spatial and temporal alignment procedure |
| `held_out_period` | Evaluation period excluded from training where applicable |
| `published_result_status` | Provider claim, published claim, reproduced or disputed |
| `regional_evaluation_status` | Region and claim class actually tested |
| `evaluation_limitations` | Truth-source, metric and comparison limits |

### 6.7 Regional applicability

Regional suitability is recorded per region and per claim class. A model cannot
receive one universal regional-suitability label.

| Field | Requirement |
|---|---|
| `region_id` | Country, state, region, city, catchment or site identifier |
| `claim_class` | Weather field, climate driver, extreme, impact, planning hypothesis or other |
| `native_coverage` | Whether the model grid or domain includes the region |
| `effective_spatial_support` | Actual model support after regridding or aggregation |
| `known_relevant_processes` | Processes represented at the relevant scale |
| `known_missing_processes` | Drivers or local processes omitted or unresolved |
| `regional_anchor_ids` | Authoritative data and product records |
| `translation_method` | Governed global-to-regional method, if any |
| `local_validation_status` | Not assessed, blocked, evaluated or admitted |
| `uncertainty_statement` | Regional uncertainty and non-stationarity |
| `required_human_review` | Discipline and authority needed |
| `regional_prohibited_inferences` | Claims that must not be made |

`native_coverage = true` does not imply `local_validation_status = admitted`.

### 6.8 Access, compute, security and cost

| Field | Requirement |
|---|---|
| `source_asset_manifest` | Named files, byte limits and hashes |
| `weight_asset_manifest` | Named checkpoints, licences, sizes and hashes |
| `data_volume_estimate` | Subset and total-volume estimate |
| `dependency_lock_status` | Exact dependency closure |
| `hardware_requirement` | CPU, GPU, TPU, memory and storage evidence |
| `runtime_estimate` | Bounded configuration-specific estimate |
| `serialization_risk` | Pickle or other unsafe-loading boundary |
| `network_isolation_plan` | Network state during inspection and execution |
| `estimated_external_cost` | Cost basis and ceiling |
| `cost_owner` | Responsible human or organization |
| `paid_commitment_status` | None, proposed or explicitly authorized |
| `stop_and_deletion_rule` | Stop conditions and asset disposal plan |

Unknown cost or security status blocks acquisition and execution.

### 6.9 Prohibited inference

Every model record must contain explicit prohibitions. The minimum set is:

- no model output is automatic truth;
- no published result is a ClimateOS reproduction;
- no global-grid value is automatically a local observation;
- no attention weight, learned representation or feature importance is causal
  proof;
- no learned physical tendency is a complete observed mechanism;
- no benchmark score establishes general scientific superiority;
- no reanalysis agreement establishes independent observational truth for all
  purposes;
- no deterministic trajectory represents full uncertainty;
- no ensemble spread guarantees complete or calibrated uncertainty outside its
  evaluated protocol;
- no historical skill establishes unrestricted future-climate extrapolation;
- no weather skill establishes climate-projection fitness;
- no climate-mode skill establishes local weather or impact skill;
- no model result is an official warning, engineering conclusion, regulatory
  decision, financial commitment or planning approval;
- no registry priority or lifecycle state authorizes the next gate.

Model-specific prohibited inferences must be added rather than replacing this
minimum set.

## 7. Evaluation Framework Record schema

| Field | Requirement |
|---|---|
| `framework_id` | Stable ClimateOS identifier |
| `name` | Official framework name |
| `owner_or_maintainer` | Responsible organization |
| `canonical_source` | Paper, repository and documentation |
| `version_and_revision` | Exact release or commit |
| `licence` | Code and data terms |
| `evaluation_purpose` | Claim classes the framework evaluates |
| `supported_model_classes` | Applicable model types |
| `required_variables` | Variable, level, unit and cadence contract |
| `required_data_resources` | Linked truth and reference resources |
| `metrics` | Metric definitions and aggregation |
| `regridding_protocol` | Grid and coordinate treatment |
| `temporal_protocol` | Initialization dates, lead times and aggregation |
| `baseline_protocol` | Baseline models and truth-source differences |
| `physical_consistency_scope` | Constraints or diagnostics actually assessed |
| `regional_scope` | Regions actually evaluated |
| `known_limitations` | Metric, truth, sampling and generalization limits |
| `result_interpretation_boundary` | Claims scores do not support |
| `priority` | NOW, LATER, WATCH or NOT_SUITABLE |
| `evidence_status` | Current verification state |

Framework registration never validates a model automatically.

## 8. Data Resource Record schema

| Field | Requirement |
|---|---|
| `resource_id` | Stable ClimateOS identifier |
| `name` | Official dataset, product or catalogue name |
| `resource_type` | Reanalysis, observation, projection, forecast, model output, catalogue or regional product |
| `provider` | Authoritative provider |
| `canonical_url` | Official landing page |
| `product_and_version` | Exact product, edition and revision |
| `licence_and_terms` | Licence, registration and redistribution conditions |
| `access_method` | Public file, registered download, API, FTP, cloud object or other method |
| `cost_and_egress` | Access, transfer and requester-pays conditions |
| `variables` | Variable contract and units |
| `spatial_coverage` | Domain, grid and resolution |
| `temporal_coverage` | Period, cadence and update status |
| `quality_and_uncertainty` | Provider quality statements and known limits |
| `preprocessing_requirements` | Subset, regrid, mask and transformation |
| `estimated_volume` | File-level or subset estimate |
| `integrity_metadata` | Provider checksum, local hash and verification date |
| `authorized_use` | Training, initialization, forcing, evaluation or regional anchor |
| `prohibited_reuse` | Redistribution, operational or unsupported uses |
| `human_review_requirement` | Domain and data-governance review |
| `evidence_status` | Current verification state |

CDS is a catalogue and access service; ERA5 is a data product. They require
separate records even when one is accessed through the other.

## 9. Parallel Comparison Record schema

| Field | Requirement |
|---|---|
| `comparison_id` | Stable comparison identifier |
| `scientific_question` | One bounded comparison question |
| `model_record_ids` | Exact model configurations compared |
| `claim_unit` | Field, index, tendency, event, statistic or impact hypothesis |
| `common_scale` | Spatial and temporal support after alignment |
| `variable_crosswalk` | Direct, transformed, conceptual-only or incomparable |
| `mechanism_crosswalk` | Explicit, learned, diagnostic or forcing relationship |
| `evaluation_framework_ids` | Independent evaluation methods used |
| `data_resource_ids` | Inputs, truth and regional anchors |
| `agreement_class` | Consistent, partially consistent, divergent, incomparable or unresolved |
| `divergence_class` | State-space, scale, mechanism, forcing, evaluation, regional or uncertainty divergence |
| `prohibited_synthesis` | Averaging, ranking or translation that must not occur |
| `human_interpretation` | Reviewer role, reasoning and dissent |
| `decision_effect` | Research implication only; no automatic action |

Incomparability is a valid result. Missing values must not be converted to zero
or neutral scores.

## 10. Initial Model Registry records

### 10.1 `model.unicm.family.v1`

| Field | Registry value |
|---|---|
| Name | UniCM |
| Record level | `FAMILY` with inspected v1.0 source orientation |
| Provider | Paper authors and official public repository maintainers |
| Scientific purpose | Learn local climate-mode dynamics and global inter-mode coupling |
| Mechanism class | `DATA_DRIVEN` |
| Represented system | Selected coupled climate modes and gridded upper-ocean physical fields |
| Source status | Official source and v1.0 release metadata verified in prior ClimateOS work; source-only integrity record exists |
| Code licence | MIT, verified in prior source review |
| Weight status | Availability and integrity not established; no weight admitted |
| Native time perspective | Monthly; inspected defaults use 12 historical and 24 forecast steps |
| Spatial perspective | Fixed climate-mode regions and coarsened gridded fields |
| Principal variables | SST, zonal and meridional wind stress, upper-ocean thermal/heat-content representation and 20-degree-isotherm depth/height |
| Principal coupling | Learned relationship between local mode dynamics, mode representations and selected physical-field branches |
| Initialization and forcing | Preprocessed CMIP6 and ocean/reanalysis data families; exact end-to-end preprocessing remains incomplete |
| Evaluation references | ERA5, ORAS5, SODA and GODAS are visible in the inspected evaluation path; results remain published or provider claims |
| Australian relevance | Promising macro-driver reference through ENSO- and IOD-related modes |
| Australian gap | SAM and MJO were not identified in the inspected mode registry; no local-impact admission |
| Research priority | `NOW` for bounded comparison already authorized |
| Lifecycle state | `SOURCE_ACQUIRED_ISOLATED` for the previously authorized source-only ZIP; weights, data and execution remain blocked |
| Prohibited inference | Attention is not mechanism proof; mode skill is not NSW rainfall, fire, ecology, water or infrastructure skill |
| Human review | Climate-mode, ocean-atmosphere and Australian regional expertise required |

### 10.2 `model.neuralgcm.family.v1`

| Field | Registry value |
|---|---|
| Name | NeuralGCM |
| Record level | `FAMILY`; current research snapshot and stable tag are distinguished |
| Provider | NeuralGCM organization / Google research authors |
| Scientific purpose | Hybrid atmospheric modelling for weather and atmosphere-only climate simulation |
| Mechanism class | `HYBRID_PHYSICS_ML` |
| Represented system | Global moist atmosphere |
| Source status | Official repository verified; research snapshot `e139660de68ef3125658e7097e81407d43dd5074`; stable comparison tag `v1.2.2` |
| Version distinction | Inspected current `main` declares 1.2.3; no release status is inferred |
| Code licence | Apache-2.0 |
| Weight licence | CC BY-SA 4.0 as declared by official documentation |
| Native time perspective | Weather trajectories from days to published 1–15-day comparisons; forced atmosphere-only simulations from months to decades |
| Spatial perspective | Global 2.8, 1.4 and 0.7 degree model configurations |
| Explicit mechanism | Hydrostatic moist primitive-equation dynamical core with pseudo-spectral horizontal representation and sigma vertical coordinates |
| Learned mechanism | Column-local learned physical tendencies, encoder/decoder corrections and stochastic components in ensemble variants |
| Prognostic variables | Vorticity, divergence, temperature, surface pressure, specific humidity, ice-cloud water and liquid-cloud water |
| Boundary forcing | SST, sea ice and solar input; climate runs are not dynamically coupled ocean simulations |
| Initialization | ERA5 pressure-level state mapped to internal coordinates |
| Evaluation references | WeatherBench2-style evaluation, ERA5, ECMWF references, GraphCast and Pangu comparisons, plus climate-statistics references |
| Australian relevance | Large-scale atmospheric-circulation context over Australia |
| Australian gap | Global grids do not establish city, catchment or site skill; separate ACCESS/BoM and observation anchors required |
| Security issue | Official checkpoints use pickle; deserialization is blocked without a separate isolation gate |
| Dependency issue | Inspected current `main` uses an unpinned Git dependency for Dinosaur |
| Research priority | `NOW` for completed source-and-observation comparison |
| Lifecycle state | `SOURCE_ORIENTATION`; no source, checkpoint or data acquisition occurred in this batch |
| Prohibited inference | Learned tendencies are not complete observed mechanisms; atmosphere-only climate simulation is not unrestricted future Earth-system projection |
| Human review | Atmospheric dynamics, ML weather, benchmark and Australian regional expertise required |

### 10.3 Pair record `comparison.unicm-neuralgcm.v1`

| Field | Registry value |
|---|---|
| Scientific question | Does NeuralGCM provide a mechanism- and scale-distinct second perspective for reading UniCM climate-mode interpretations? |
| Claim unit | Source-and-observation architecture, not numerical forecast output |
| Common scale | Planetary to continental conceptual comparison; no local numerical comparison |
| Variable relationship | Ocean-state variables may act as mode inputs in UniCM and boundary forcing context for NeuralGCM; not direct output equivalence |
| Mechanism relationship | Learned inter-mode relationships versus explicit atmospheric dynamics plus learned unresolved-process tendencies |
| Agreement class | `PARTIALLY_COMPARABLE` |
| Principal divergence | State-space, scale, mechanism, forcing and evaluation divergence |
| Decision | NeuralGCM retained as second research model world |
| Prohibited synthesis | No score averaging, output fusion, causal claim, regional forecast or operational selection |
| Evidence status | Source-and-observation comparison complete; no execution or reproduction |

## 11. Candidate inventory and current research position

These entries are inventory classifications, not verified model records.

| Candidate | Provisional registry role | Priority | Current reason and prerequisite |
|---|---|---|---|
| UniCM | Climate-mode relationship model | `NOW` | Baseline research world; source-only and observation work completed under prior gates |
| NeuralGCM | Hybrid atmosphere model | `NOW` | Second research world; source-and-observation pack completed |
| ACCESS | Australian global/regional model family and official product anchor | `NOW` for metadata anchor only | Needed to check Australian scale and product reality; code/runtime access is a separate question |
| WeatherBench2 | Evaluation framework, not a model | `NOW` for framework registration | Relevant to weather evaluation; does not evaluate all UniCM claims |
| GraphCast | Data-driven global weather model | `LATER` | Potential third model after v0.1 registry review and explicit Founder authorization |
| GenCast | Probabilistic global weather model | `LATER` | Useful uncertainty perspective after deterministic/hybrid comparison controls mature |
| ICON | Physics-based numerical weather/climate family | `LATER` | Potential explicit-physics reference; exact open configuration and access require verification |
| IFS | Operational numerical weather family | `LATER` | Important benchmark and mechanism reference; product, code and access layers must be separated |
| Pangu-Weather | Data-driven global weather model | `WATCH` | Source, licence, weight and current access verification required |
| FuXi | Data-driven weather model family | `WATCH` | Version, official repository, licence and checkpoint verification required |
| Aurora | Cross-domain Earth-system foundation model | `WATCH` | Broad variable/domain value; exact licence and non-academic/commercial boundaries require review |
| ArchesWeather / ArchesWeatherGen | Weather or climate model candidate | `WATCH` | Identity, version, repository and role require source verification |
| AirCast-SR | Regional or super-resolution candidate | `WATCH` | Better treated as a translation/downscaling layer until verified |
| ObsCast | Observation-oriented model candidate | `WATCH` | Better treated as observation translation until verified |
| AICON | Operational architecture or orchestration reference | `NOT_SUITABLE` as a model record; `WATCH` as architecture reference | Do not force an orchestration pattern into the model registry |

`NOT_SUITABLE` here applies only to the stated object role. It is not a general
scientific rejection.

## 12. Initial Evaluation Framework inventory

| Framework | Object status | Priority | Boundary |
|---|---|---|---|
| WeatherBench2 | `EVALUATION_FRAMEWORK_RECORD` candidate | `NOW` | Weather forecast evaluation; truth-source and regridding differences must remain visible |
| PhysMetrics.Weather | `EVALUATION_FRAMEWORK_RECORD` candidate | `WATCH` pending current source verification | Physical-consistency diagnostics do not establish complete physical validity |
| RealBench | `EVALUATION_FRAMEWORK_RECORD` candidate | `LATER` | Real-world benchmark and decision relevance require an independent future gate |
| AIMIP or other AI-model intercomparison work | `EVALUATION_FRAMEWORK_RECORD` candidate | `WATCH` | Exact identity, scope and current authority require verification |

## 13. Initial Data Resource inventory

| Resource | Resource type | Priority | Boundary |
|---|---|---|---|
| Copernicus Climate Data Store | Catalogue and access service | `NOW` for metadata | Not itself equivalent to ERA5, ERA5-Land or CMIP6 |
| ERA5 | Global atmospheric reanalysis | `NOW` for metadata and provenance | Reanalysis is model-observation synthesis, not pure observation truth |
| ERA5-Land | Land reanalysis | `LATER` | Land-focused product; variable and scale mapping required |
| CMIP6 | Multi-model projection and experiment archive | `LATER` | Model ensemble is not observation truth; experiment and member identity required |
| ORAS5 | Ocean reanalysis | `NOW` for UniCM provenance | Exact product, variable and preprocessing mapping required |
| SODA | Ocean reanalysis family | `WATCH` | Exact version and terms required |
| GODAS | Ocean data-assimilation/reanalysis product | `WATCH` | Exact product and file terms required |
| RESDC | Scientific data-resource candidate | `WATCH` | Authoritative identity, scope, licence and access require verification |
| Bureau of Meteorology ACCESS products | Official forecast/model-output resource | `NOW` for Australian metadata anchor | Registered-user and product-access conditions remain distinct from public charts |
| Australian stations, radar and climate products | Official or governed regional observation resources | `LATER` | Exact product records and permitted access methods require separate authorization |

## 14. Minimum completeness rules

A Model Record is not complete unless it contains:

1. exact identity and source evidence;
2. record level and configuration scope;
3. spatial and temporal scale;
4. mechanism class and causal-status boundary;
5. variable and transformation contract;
6. initialization and forcing contract;
7. independent evaluation links;
8. regional-applicability record for every proposed regional use;
9. access, licence, compute, security and cost status;
10. global and model-specific prohibited inferences;
11. evidence status for every material claim;
12. human responsibility and review state.

Missing material fields result in `BLOCKED`, not an assumed default.

## 15. Comparison rules

1. Compare one claim unit at a time.
2. Preserve native scale before constructing a common scale.
3. Record every regrid, interpolation, anomaly and aggregation.
4. Separate model state, diagnostic, forcing and observation.
5. Separate published skill from ClimateOS-reproduced evidence.
6. Preserve deterministic and stochastic interpretations.
7. Record disagreement and incomparability as first-class outputs.
8. Do not convert categorical evidence states into hidden numeric scores.
9. Do not rank models across different scientific tasks.
10. Do not promote global agreement to regional or local confidence.
11. Require an independent evaluation framework where a performance claim is
    made.
12. Require qualified human review for mechanism, regional and consequential
    interpretation.

## 16. Human scientific responsibility

The registry may organize evidence but cannot assume scientific responsibility.

Required roles depend on the claim and may include:

- atmospheric dynamicist;
- ocean-atmosphere and climate-mode scientist;
- numerical weather prediction specialist;
- ML weather-model specialist;
- benchmark and verification specialist;
- Australian regional climatologist or meteorologist;
- hydrology, fire, ecology, infrastructure or other impact-domain expert;
- data-governance and licence reviewer;
- security and reproducibility reviewer;
- Founder or delegated governance authority.

Reviewer identity, scope, date, disagreement and unresolved questions must be
recorded. An AI-generated registry entry is not human scientific sign-off.

## 17. Draft v0.1 verification checklist

- [x] Model identity is separated from evaluation and data resources.
- [x] Scale has explicit spatial, temporal and transfer-boundary fields.
- [x] Mechanism separates equations, learned components, associations and
  diagnostics.
- [x] Variables require units, support, transformation and configuration scope.
- [x] Initialization and external forcing are explicit.
- [x] Evaluation frameworks are independent registry objects.
- [x] Regional applicability is per region and per claim class.
- [x] Prohibited inference is mandatory.
- [x] Access, licence, compute, security and cost are blocking fields.
- [x] Research priority is separated from lifecycle and admission.
- [x] UniCM and NeuralGCM have initial bounded records.
- [x] GraphCast remains deferred.
- [x] No model, weight, dataset or runtime was acquired or executed.

## 18. Founder review questions

1. Does the three-layer separation of Model, Evaluation Framework and Data
   Resource reflect the intended ClimateOS architecture?
2. Should the first implementation remain a documentation registry, or should
   a later gate propose machine-readable schemas and fixtures?
3. Is ACCESS correctly positioned as both a model-family record and an
   Australian official-product anchor, with those objects kept separate?
4. Should GraphCast remain `LATER` until the UniCM-NeuralGCM fields receive
   scientific and Founder review?
5. Which human scientific roles should be mandatory before any regional
   comparison is designed?

## 19. Closure and next gate

ClimateOS Parallel Model Registry Draft v0.1 is complete as a non-executable
research contract.

The next safe step is Founder review of the schema, the two initial model
records, the candidate classifications and the GraphCast deferral. Creating a
JSON schema, runtime registry, adapter, acquisition plan, third-model research
pack or experiment remains a separate Founder-gated action.

Deferred `LATER` and `WATCH` candidates are routed by:

- `docs/context-packets/2026-07-14_CLIMATEOS_PARALLEL_MODEL_LATER_WATCH_PRI_METRICS_MISSION_CONTROL_HANDOFF.md`.
