# ACTP — ClimateOS Parallel Model and Scientific Resource Discovery

Date: 2026-07-14
Status: DRAFT_FOR_FOUNDER_REVIEW / NOT_EXECUTABLE
Project: ClimateOS / Eco-Agent-System
Primary context: UniCM-inspired multi-model, multi-scale, multi-system architecture
Target reader: ClimateOS implementation / programming thread, Codex, future research agents

---

## 1. Transfer purpose

This ACTP transfers the models, evaluation frameworks, scientific platforms and data resources discussed in the source conversation into one structured discovery package for the ClimateOS implementation thread.

The Founder’s intent is not to select one model as the single truth. ClimateOS is being designed from a global, system-level viewpoint and therefore needs a governed architecture able to observe several parallel model worlds, compare them, preserve disagreement and use different models for different scales and purposes.

The core architectural principle is:

> ClimateOS should not become a wrapper around UniCM or any other single model. It should become a model-neutral orchestration, comparison, evidence and interpretation system in which several climate, weather, downscaling, mechanism and domain models can operate in parallel.

This packet is a discovery and architecture input. It does not authorize downloads, integration, inference, training, cloud spending, operational forecasts, scientific conclusions or changes to the currently authorized ClimateOS task sequence.

---

## 2. Founder intent

The Founder wants the ClimateOS thread to study which of the models and resources listed here may support a future parallel-model architecture.

The desired capability is not simply an ensemble average. ClimateOS should eventually be able to:

1. register multiple models as independent scientific viewpoints;
2. identify their spatial, temporal and disciplinary scopes;
3. compare agreements, disagreements and missing variables;
4. preserve provenance, version, licence and uncertainty;
5. prevent one model from silently overriding another;
6. translate model outputs into common evidence contracts;
7. connect global climate state, weather evolution, regional detail and environmental impacts;
8. support human interpretation and Founder approval;
9. replace or add models without rebuilding the ClimateOS core;
10. maintain the concept of multiple parallel model worlds rather than assuming a single universally correct representation.

---

## 3. Mandatory distinction: models, frameworks and resources

The implementation thread must not mix all named items into one category.

### 3.1 Predictive or simulation models

These generate forecasts, climate-mode states, simulations, downscaled fields or mechanism experiments.

### 3.2 Evaluation and assurance frameworks

These test whether models are statistically skillful, physically consistent, robust under operational conditions or useful for decisions.

### 3.3 Data and scientific resource platforms

These supply observations, reanalysis, scenarios, land-cover information, environmental layers or reference data.

### 3.4 Scientific orchestration patterns

These show how AI agents, numerical models and evidence chains may be combined into a research workflow.

ClimateOS should create separate registries and contracts for these categories.

---

# 4. Candidate model inventory

## 4.1 UniCM — coupled global climate-mode model

Category: Climate-mode prediction / coupled climate intelligence

Primary role:
- learn interactions among global ocean-atmosphere climate modes;
- represent lead-lag and cross-basin predictive relationships;
- support seasonal to interannual climate-state interpretation;
- provide the principal scientific inspiration for the Task1500–1700 Environmental Coupling Layer.

Potential ClimateOS use:
- Climate Mode Evidence Adapter;
- ENSO / IOD / other mode-state inputs;
- coupled-state comparison with other seasonal forecast systems;
- representation of emergent predictability across modes.

Important boundary:
- UniCM is not a complete Earth System Model;
- it must not become a hard dependency of ClimateOS core;
- official repository, licence, data, weights and reproducibility must be reverified at the Task1500 gate.

Priority: Core research candidate for Task1500.

---

## 4.2 ArchesWeather / ArchesWeatherGen and AIMIP

Category: AI atmospheric model / long-run climate simulation research / model-intercomparison framework

Primary role:
- adapt AI weather models into forced atmospheric simulations;
- test whether AI atmospheric models can maintain stable climate statistics over long periods;
- provide an AI Model Intercomparison Project pattern analogous to model comparison in conventional climate science.

Potential ClimateOS use:
- long-horizon atmospheric-model candidate;
- model-world comparison;
- historical climate-statistics simulation;
- future registry for AI climate simulation capabilities.

Important boundary:
- forced atmosphere is not a fully coupled Earth System Model;
- prescribed SST and sea ice do not equal future coupled prediction;
- AIMIP is an evaluation ecosystem, not one model.

Priority: Secondary research candidate; compare with UniCM rather than merge with it.

---

## 4.3 NeuralGCM

Category: Hybrid or machine-learning atmospheric / climate model

Primary role:
- combine learned components with physical dynamical structure;
- bridge weather prediction and longer atmospheric simulations.

Potential ClimateOS use:
- reference model for hybrid physics-AI design;
- comparison candidate against purely data-driven and conventional models;
- possible future input to ClimateOS climate-state and weather layers.

Important boundary:
- repository, accessible weights, licence, variables and compute requirements require current verification.

Priority: Research-watch candidate.

---

## 4.4 GraphCast

Category: Global AI weather prediction model

Primary role:
- medium-range global weather-state evolution;
- graph-based representation of global atmospheric fields.

Potential ClimateOS use:
- global weather driver;
- comparison input alongside conventional NWP and other AI models;
- upstream field for regional downscaling;
- historical or event-based comparison.

Important boundary:
- weather forecasting is not climate prediction;
- accessible implementation, initialization source and licence must be verified;
- it should be ingested through an adapter, not embedded in ClimateOS core.

Priority: High-value comparison candidate.

---

## 4.5 Pangu-Weather

Category: Global AI weather prediction model

Primary role:
- rapid deterministic global weather forecasting;
- three-dimensional AI weather-state evolution.

Potential ClimateOS use:
- parallel forecast model;
- comparison with GraphCast, FuXi, AICON, ICON, ACCESS and IFS;
- extreme-event and physical-consistency evaluation candidate.

Important boundary:
- verify accessible code, weights, input data contract and licensing;
- deterministic forecasts may smooth uncertainty and extremes.

Priority: High-value comparison candidate.

---

## 4.6 FuXi

Category: Global AI weather prediction model

Primary role:
- medium-range global prediction;
- multi-stage or multi-model AI forecasting approaches.

Potential ClimateOS use:
- independent AI weather model world;
- divergence analysis against Pangu, GraphCast and conventional NWP;
- candidate for variable and lead-time comparison.

Priority: High-value comparison candidate, subject to access verification.

---

## 4.7 FourCastNet

Category: Global AI weather prediction model

Primary role:
- fast data-driven global forecasts;
- early large-scale neural weather modelling reference.

Potential ClimateOS use:
- baseline or historical comparison model;
- spectral-performance research;
- architecture comparison.

Priority: Secondary baseline candidate.

---

## 4.8 GenCast

Category: Probabilistic AI weather model

Primary role:
- probabilistic or ensemble-style medium-range weather prediction;
- representation of forecast uncertainty and multiple plausible futures.

Potential ClimateOS use:
- probability-aware forecast source;
- contrast with deterministic GraphCast, Pangu and FuXi outputs;
- uncertainty propagation into WaterOS, Fire, Energy and other impact layers.

Important boundary:
- confirm current access, output format, ensemble semantics and licence.

Priority: High-value candidate because ClimateOS needs multiple plausible futures, not one deterministic path.

---

## 4.9 Aurora

Category: Earth-system foundation model / multi-domain environmental model

Primary role:
- adaptation to multiple Earth-system prediction tasks;
- weather and other environmental domains through a foundation-model approach.

Potential ClimateOS use:
- reference for reusable cross-domain representation;
- candidate for weather, air-quality or other environmental output adapters;
- comparison with specialist models.

Important boundary:
- a foundation model is not automatically authoritative across all domains;
- each adapted task needs independent validation.

Priority: Strategic research candidate.

---

## 4.10 AICON-Global

Category: Operational AI global weather model / institutional deployment pattern

Primary role:
- AI forecasting operated by the German Weather Service alongside physical ICON;
- illustrate an operational physical-plus-AI dual-track architecture.

Potential ClimateOS use:
- reference for hybrid operational architecture;
- model-source candidate if access becomes available;
- pattern for high-frequency AI updates, physical-model comparison, fallback and expert oversight.

Important boundary:
- AICON’s greatest value may be the operational pattern rather than downloadable code;
- do not assume public weights or unrestricted access;
- do not treat it as a replacement for ICON.

Priority: Architecture reference and possible future model source.

---

## 4.11 ICON

Category: Conventional numerical weather prediction model

Primary role:
- physical global and regional numerical forecast reference;
- independent comparison against AICON and other AI systems.

Potential ClimateOS use:
- physical baseline;
- hybrid forecast runtime;
- divergence and fallback reference;
- physics-based event investigation.

Important boundary:
- model products, source availability, licences and operational feeds vary;
- ClimateOS may use published products without running the full model.

Priority: Important conventional-model reference.

---

## 4.12 IFS / ECMWF operational forecast products

Category: Conventional global NWP / ensemble forecast system

Primary role:
- high-quality physical-model and ensemble forecast reference;
- source of analysis, forecasts and reanalysis ecosystem.

Potential ClimateOS use:
- authoritative comparison source;
- multi-model divergence analysis;
- seasonal or medium-range forecast inputs;
- reference for event reconstruction.

Important boundary:
- distinguish open datasets from restricted operational products;
- record exact product, licence, cycle and resolution.

Priority: High-value physical reference.

---

## 4.13 ACCESS family

Category: Australian Bureau of Meteorology numerical weather / climate model family

Primary role:
- Australian operational and regional context;
- potentially more relevant to Australian impacts than global foreign products alone.

Potential ClimateOS use:
- Australian baseline for Snowy Valleys, Riverina, NSW and national studies;
- comparison with ECMWF, ICON and AI weather models;
- regional fitness assessment.

Important boundary:
- current product access, licence, variables and delivery mechanisms require official verification.

Priority: Very high for Australian ClimateOS applications.

---

## 4.14 AirCast-SR

Category: AI weather super-resolution / regional downscaling model

Primary role:
- downscale coarse global weather forecasts to kilometre-scale near-surface variables;
- generate hourly regional fields;
- explore zero-shot regional transfer.

Potential ClimateOS use:
- regional translation layer between global forecasts and impact agents;
- compare downscaled outputs from several global model inputs;
- support water, fire, agriculture, urban and infrastructure analysis.

Important boundary:
- super-resolution does not create observations;
- generated small-scale detail must be validated locally;
- zero-shot transfer claims must not be assumed to hold in Australia.

Priority: High-value downscaling research candidate.

---

## 4.15 ObsCast

Category: Observation-driven regional high-resolution weather prediction

Primary role:
- use satellite, radar and surface observations directly for short-range regional prediction;
- reduce dependence on conventional NWP input during training or inference.

Potential ClimateOS use:
- local observation layer;
- short-range correction or independent forecast world;
- comparison against NWP-driven and downscaled products.

Important boundary:
- observation availability and quality determine portability;
- regional retraining or infrastructure may be required;
- short-range capability should not be confused with seasonal or climate forecasting.

Priority: Strategic observation-driven candidate.

---

## 4.16 TianJi-Environ

Category: Autonomous scientific-workflow framework using WRF-Chem

Primary role:
- translate mechanism hypotheses into controlled numerical experiments;
- configure, run and diagnose atmospheric-chemistry simulations;
- produce auditable mechanism evidence chains.

Potential ClimateOS use:
- reference for the future Mechanism Experiment Layer;
- pattern for hypothesis, experiment, diagnostic and evidence contracts;
- possible future integration with WRF-Chem or other domain models.

Important boundary:
- it is not primarily a forecast model;
- it must remain separate from UniCM and weather-model adapters;
- numerical experiments require scientific and compute governance.

Priority: Future mechanism-research reference, not current runtime model.

---

## 4.17 WRF-Chem

Category: Physics and chemistry regional numerical model

Primary role:
- controlled atmospheric chemistry and pollution experiments;
- mechanism testing and regional simulation.

Potential ClimateOS use:
- future experiment engine under a tightly controlled mechanism layer;
- air pollution, aerosol-radiation, boundary-layer and emission sensitivity studies.

Important boundary:
- high configuration complexity;
- emissions, chemistry options and boundary conditions strongly affect results;
- expert review is mandatory.

Priority: Future specialist model, not near-term core.

---

# 5. Evaluation and assurance inventory

## 5.1 WeatherBench / WeatherBench 2

Category: Statistical weather-model benchmark

Role:
- standardized datasets and forecast metrics;
- RMSE, ACC and related skill comparison.

ClimateOS use:
- statistical-skill component of a broader admission dossier.

Boundary:
- insufficient by itself for physics, extremes, operational robustness or decision value.

---

## 5.2 PhysMetrics.Weather

Category: Physical-consistency evaluation framework

Role:
- dry-air mass, water mass and total-energy drift;
- effective resolution and spectra;
- hydrostatic, geostrophic and lapse-rate consistency.

ClimateOS use:
- future Scientific Assurance Layer;
- model physical-consistency passport;
- compare AI weather models beyond pixel-level errors.

Boundary:
- physical consistency is not the same as forecast accuracy;
- ERA5 or other references are not perfect truth.

---

## 5.3 RealBench

Category: Operational and out-of-distribution weather benchmark

Role:
- leakage-resistant evaluation on later data;
- extreme-event and realistic operational stress testing;
- evaluate generalization beyond training climate and historical periods.

ClimateOS use:
- future Task2100 benchmark layer;
- operational robustness and extreme-event assessment;
- input to model admission and decision validation.

Boundary:
- deliberately deferred; must not interrupt the current roadmap.

---

## 5.4 AIMIP

Category: AI climate-model intercomparison framework

Role:
- compare long-run AI atmospheric models under shared protocols;
- establish a climate-statistics rather than weather-only evaluation culture.

ClimateOS use:
- future model-world registry and climate-simulation comparison;
- inspiration for multi-model evidence packages.

---

## 5.5 ClimateOS Decision Benchmark — proposed future concept

Category: ClimateOS-native decision-value evaluation

Role:
- evaluate not only model error but impact on warnings, planning, environmental interpretation and governance decisions;
- track lead time, uncertainty communication, false reassurance, missed events and downstream consequences.

Boundary:
- this is a ClimateOS design direction, not an existing validated benchmark;
- deferred to future scientific-governance stages.

---

# 6. Data and scientific resource inventory

## 6.1 Copernicus Climate Data Store (CDS)

Category: Global climate-data platform

Primary resource families:
- ERA5;
- ERA5-Land;
- seasonal forecasts;
- climate projections and indicators;
- selected CMIP-related products.

Potential ClimateOS use:
- global historical climate and land-surface background;
- model initialization or evaluation where permitted;
- coupling analysis;
- regional extraction for Australia and China;
- scientific evidence lineage.

Important boundary:
- reanalysis is model-plus-observation, not pure observation;
- API, account, licence, request limits and storage must be governed;
- no large uncontrolled download.

Roadmap location:
- Task3500 Future Science Data Infrastructure Library.

---

## 6.2 ERA5

Category: Global atmospheric reanalysis

Potential ClimateOS use:
- historical atmospheric states;
- training/evaluation reference;
- climate-mode and weather-event analysis;
- multi-model normalization.

Required metadata:
- product version;
- variables;
- pressure or single levels;
- temporal resolution;
- spatial resolution;
- extraction date;
- licence and citation;
- transformation history.

---

## 6.3 ERA5-Land

Category: Global land-surface reanalysis

Potential ClimateOS use:
- soil moisture, temperature, runoff, evaporation and land-surface analysis;
- WaterOS, LandOS, Fire and Life System links;
- regional environmental coupling.

Boundary:
- higher grid resolution does not equal local site observation;
- validate against Australian or Chinese local data where possible.

---

## 6.4 CMIP / CMIP6 families

Category: Multi-model climate-projection archive and intercomparison ecosystem

Potential ClimateOS use:
- future climate scenarios;
- multi-model spread and scenario analysis;
- external parallel model worlds;
- compare structural uncertainty rather than select one projection.

Important boundary:
- distinguish scenarios, experiments, models, ensembles and bias-corrected products;
- ClimateOS must preserve model identity and not average away meaningful disagreement.

---

## 6.5 RESDC — Resource and Environmental Science Data Platform

Website: www.resdc.cn

Category: China-focused resource, environment, land-use and geospatial data platform

Potential resource families:
- land-use and land-cover monitoring;
- administrative boundaries;
- terrain and geomorphology;
- ecological and vegetation data;
- resource and environmental regional layers;
- possible climate, soil, population and socio-economic spatial products, subject to verification.

Potential ClimateOS use:
- China regional layer;
- LandOS, WaterOS, CarbonOS and BiodiversityOS;
- China administrative and governance aggregation;
- Xinjiang / Kunlun / other regional studies;
- complement global datasets with locally relevant layers.

Important boundary:
- dataset-by-dataset licence, price, registration, format, CRS, resolution and redistribution rules must be verified;
- platform data must not automatically be treated as legal cadastral, engineering or real-time operational data.

Roadmap location:
- Task3500 future scientific-resource registry candidate.

---

## 6.6 Additional future source families to investigate

These were not analyzed in equal depth in the source conversation but were identified as relevant future families:

- Australian Bureau of Meteorology datasets;
- CSIRO data and climate services;
- Geoscience Australia;
- Atlas of Living Australia;
- GBIF;
- NASA Earth observation;
- NOAA;
- JAXA;
- national and state hydrology, land, ecology and fire datasets.

These remain discovery candidates only.

---

# 7. Proposed ClimateOS parallel-model architecture

The implementation thread should study a layered, model-neutral architecture similar to the following:

```text
Scientific Data and Observation Sources
CDS / ERA5 / ERA5-Land / CMIP / RESDC / Australian sources
                          ↓
Source Registry + Provenance + Licence + Evidence Passport
                          ↓
Climate-State Models
UniCM / seasonal systems / coupled-mode models
                          ↓
Global Weather Model Worlds
GraphCast / Pangu / FuXi / GenCast / Aurora / AICON / ICON / IFS / ACCESS
                          ↓
Regional Translation Worlds
AirCast-SR / regional NWP / statistical downscaling / ObsCast
                          ↓
Environmental Coupling Layer
Water / Land / Soil / Vegetation / Fire / Carbon / Energy / Building / Life
                          ↓
Mechanism Experiment Layer
TianJi-Environ pattern / WRF-Chem / future specialist numerical models
                          ↓
Assurance and Benchmark Layer
WeatherBench / PhysMetrics / RealBench / climate-model intercomparison
                          ↓
Human Interpretation + Evidence Passport + Founder Governance
```

The architecture must allow lateral comparison at each level rather than forcing all outputs through one preferred model.

---

# 8. Required common model contract

The ClimateOS thread should consider a common registry schema before model integration.

```yaml
model_id:
model_name:
model_family:
model_category:
provider:
official_source:
repository:
licence:
version_or_commit:
release_date:

scientific_scope:
  domain:
  spatial_scope:
  temporal_scope:
  forecast_horizon:
  resolution:
  vertical_levels:

input_contract:
  variables:
  units:
  grid:
  initialization_source:
  required_history:

output_contract:
  variables:
  units:
  grid:
  deterministic_or_probabilistic:
  ensemble_semantics:

access:
  public_code:
  public_weights:
  api_or_data_feed:
  account_required:
  cost:
  compute_requirements:

validation:
  statistical_benchmarks:
  physical_consistency:
  extreme_event_evidence:
  regional_fitness:
  known_failures:

climateos_role:
  layer:
  adapter_status:
  decision_use_boundary:
  evidence_passport_id:

review_status:
founder_authorization:
```

---

# 9. Required data-resource contract

```yaml
resource_id:
resource_name:
provider:
official_url:
dataset_family:
licence:
citation_requirement:
commercial_use:
redistribution:
registration_required:
cost:

geographic_scope:
temporal_coverage:
update_frequency:
spatial_resolution:
data_format:
coordinate_reference_system:
variables_or_layers:
methodology:
observed_reanalysis_modelled_or_derived:

known_limitations:
quality_control:
access_method:
storage_estimate:
controlled_sample_available:

climateos_use_cases:
evidence_passport_id:
review_status:
```

---

# 10. Parallel-model comparison principles

The future implementation must preserve the following rules:

1. No single model is declared the truth source merely because it is newer or has a lower published RMSE.
2. AI, physical and hybrid models must remain distinguishable.
3. Deterministic and probabilistic outputs must not be silently mixed.
4. Grid resolution and effective physical resolution must be separately recorded.
5. Forecast skill, physical consistency, operational robustness and decision value are separate dimensions.
6. Reanalysis, observations and model simulations must retain different evidence labels.
7. Model disagreement is an output to preserve, not an error to hide.
8. Averaging is not always the correct resolution of disagreement.
9. Regional suitability must be assessed independently for Australia, China and other target regions.
10. All transformations, bias corrections and downscaling steps require lineage records.
11. ClimateOS should prefer adapters and evidence contracts over direct code fusion.
12. External models should be replaceable without changing ClimateOS governance logic.

---

# 11. Discovery questions for the ClimateOS implementation thread

The receiving thread should research and answer, without immediately implementing:

## 11.1 Model accessibility

- Which models have official public repositories?
- Which have downloadable weights?
- Which provide APIs or only papers?
- Which licences permit research, commercial use, modification and redistribution?
- Which can run on available local or affordable cloud hardware?

## 11.2 Input compatibility

- Which models accept ERA5-like fields?
- Which require proprietary analyses or operational initialization?
- Can a common normalized weather-state contract serve several models?
- Which require pressure levels, model levels, static fields or historical context?

## 11.3 Output compatibility

- Which variables overlap?
- How should vertical levels, grids, forecast steps and units be normalized?
- How should ensembles and probabilistic outputs be represented?
- What information would be lost during normalization?

## 11.4 Multi-scale orchestration

- How should seasonal climate-mode outputs condition weather-model interpretation?
- How should global forecasts feed regional downscaling without claiming false precision?
- How should observation-driven models such as ObsCast coexist with NWP-driven forecasts?
- How should impact agents receive uncertainty and model disagreement?

## 11.5 Scientific assurance

- Which models can be tested with WeatherBench, PhysMetrics and RealBench-style protocols?
- What constitutes minimum admission evidence?
- How can ClimateOS record physical inconsistency, OOD weakness and regional failure?

## 11.6 Resource infrastructure

- Which CDS and RESDC products are the highest-priority small samples?
- What metadata and licence evidence must be stored before downloading?
- What storage and compute budgets would be required?
- Which Australian official sources should be preferred over global substitutes?

---

# 12. Recommended output of the receiving thread

The receiving ClimateOS thread should produce a research-only package, not integration code:

1. **ClimateOS Parallel Model Registry Draft v0.1**
2. **Model Accessibility and Licence Matrix**
3. **Common Input / Output Variable Crosswalk**
4. **Parallel Model Layer Map**
5. **Candidate Adapter Priority Ranking**
6. **Scientific Assurance Matrix**
7. **Data Resource Registry Draft**
8. **Compute, Storage and Cost Risk Note**
9. **Recommendation: NOW / LATER / WATCH / NOT SUITABLE** for each item
10. **Founder Review Gate** before any clone, download or runtime work

Suggested prioritization labels:

- `NOW_RESEARCH_ONLY`
- `NEAR_TERM_ADAPTER_CANDIDATE`
- `TASK1500_CANDIDATE`
- `FUTURE_MECHANISM_CANDIDATE`
- `FUTURE_INFRASTRUCTURE_CANDIDATE`
- `WATCH_ONLY`
- `BLOCKED_BY_ACCESS`
- `NOT_SUITABLE`

---

# 13. Current strategic priority

Because ClimateOS is presently advancing through the UniCM-related multi-scale and multi-model interpretation phase, the most immediately relevant research set is:

### Tier 1 — direct parallel-model architecture candidates

- UniCM
- GraphCast
- Pangu-Weather
- FuXi
- GenCast
- Aurora
- ICON / IFS / ACCESS products
- AICON as operational architecture reference

### Tier 2 — regional translation and observation candidates

- AirCast-SR
- ObsCast
- regional NWP and controlled downscaling approaches

### Tier 3 — long-run climate simulation and intercomparison

- ArchesWeather / ArchesWeatherGen
- AIMIP
- NeuralGCM
- CMIP model families

### Tier 4 — scientific mechanism and experiment references

- TianJi-Environ
- WRF-Chem

### Tier 5 — assurance and benchmark frameworks

- WeatherBench / WeatherBench 2
- PhysMetrics.Weather
- RealBench

### Tier 6 — scientific data infrastructure

- Copernicus CDS
- ERA5
- ERA5-Land
- CMIP archives
- RESDC
- Australian official datasets

---

# 14. Non-execution boundary

This ACTP does not authorize the receiving thread or Codex to:

- clone external repositories;
- fork models;
- download model weights;
- register external accounts;
- create API keys;
- download ERA5, CMIP or RESDC datasets;
- run inference or training;
- provision cloud or GPU resources;
- alter the active ClimateOS task sequence;
- merge external model dependencies into ClimateOS;
- produce operational forecasts;
- claim scientific equivalence between models;
- select a preferred model without Founder review.

The immediate action is discovery, classification and architecture analysis only.

---

# 15. Receiving-thread handoff instruction

The receiving ClimateOS implementation thread should respond with:

> ACTP received. The model, benchmark and data-resource inventory will be treated as a research candidate set for a model-neutral parallel-model architecture. No external model, weights, dataset or runtime will be integrated without current source verification and explicit Founder authorization.

It should then:

1. relate this inventory to the current authoritative ClimateOS task and HEAD;
2. identify which existing ClimateOS registries and adapters already cover parts of the requirement;
3. avoid duplicating completed work;
4. propose a bounded research packet and gate;
5. keep current authorized execution moving unless the Founder explicitly changes priority.

---

# 16. CRP Harvest Block

## Core knowledge points

- ClimateOS needs several parallel model worlds rather than dependence on UniCM alone.
- Climate, weather, regional downscaling, mechanisms, benchmarks and data resources are distinct architectural categories.
- UniCM is the principal coupled-climate reference, but not the ClimateOS core.
- Global AI weather candidates include GraphCast, Pangu, FuXi, GenCast, Aurora and others.
- Conventional physical references such as ICON, IFS and ACCESS remain necessary.
- AirCast-SR and ObsCast occupy regional translation and observation-driven layers.
- TianJi-Environ and WRF-Chem belong to a later mechanism-experiment layer.
- WeatherBench, PhysMetrics and RealBench measure different dimensions of quality.
- CDS, ERA5, ERA5-Land, CMIP and RESDC are resources, not predictive models.

## Idea points

- Create a ClimateOS Parallel Model Registry.
- Use adapters and common evidence contracts instead of code fusion.
- Preserve disagreement as a first-class product.
- Build a model-accessibility and licence matrix before choosing candidates.
- Connect global climate states, weather worlds, regional detail and environmental impacts without pretending they operate at the same scale.

## Desire points

- ClimateOS should become a global-view scientific system able to inspect multiple representations of Earth-system behaviour.
- The system should help the Founder compare models, not force the Founder to trust one opaque answer.
- ClimateOS should remain scientifically replaceable, traceable and governable as models evolve.

## Reasoning points

- No model covers all spatial scales, time horizons and environmental domains.
- Parallel comparison reduces dependence on one model’s structural errors.
- Model disagreement may reveal uncertainty, regime change or missing mechanisms.
- Data access and licensing may determine practical usefulness more than paper performance.
- A common schema must preserve differences rather than flatten them.

## Key decisions

- Treat the listed models and resources as a research candidate inventory.
- Do not create one giant combined model task.
- Keep UniCM as a key Task1500 reference while actively looking for parallel candidates.
- Separate predictive models, assurance frameworks, data resources and scientific orchestration patterns.
- Require a fresh Founder gate before external acquisition or runtime integration.

## Open questions

- Which models are truly accessible now?
- Which can run within available compute and storage?
- Which outputs are compatible enough for a common adapter?
- Which are scientifically useful for Australia and China?
- How should ClimateOS represent multi-model divergence and confidence?
- Which official data sources should serve as evaluation references?

## Next actions

- Receiving ClimateOS thread prepares a read-only discovery matrix.
- Compare candidates against existing ClimateOS source registries and tasks.
- Rank candidates as NOW / LATER / WATCH / NOT SUITABLE.
- Present the matrix to the Founder before any integration step.

## Project keywords

ClimateOS; UniCM; parallel models; multi-model architecture; model worlds; GraphCast; Pangu-Weather; FuXi; FourCastNet; GenCast; Aurora; AICON; ICON; IFS; ECMWF; ACCESS; NeuralGCM; ArchesWeather; AIMIP; AirCast-SR; ObsCast; TianJi-Environ; WRF-Chem; WeatherBench; PhysMetrics.Weather; RealBench; Copernicus CDS; ERA5; ERA5-Land; CMIP; RESDC; Environmental Coupling Layer; Model Registry; Evidence Passport; uncertainty; divergence; scientific governance.
