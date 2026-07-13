# NeuralGCM Source-and-Observation Research Pack

Date: 2026-07-14

Status: RESEARCH_COMPLETE / SOURCE_AND_METADATA_ONLY / NO_ACQUISITION / NO_EXECUTION

## 1. Purpose

This pack records NeuralGCM as a bounded research candidate for the ClimateOS
model-neutral parallel-model architecture. It asks what NeuralGCM observes,
what mechanisms it represents, which scales it can address, and where its
published and documented limits begin.

The pack does not admit NeuralGCM as a ClimateOS runtime, data source,
forecasting service, regional decision tool, or scientific authority.

## 2. Authorized boundary

This batch was limited to public papers, official repository metadata, official
documentation, licence text, dependency declarations, checkpoint names, and
published evaluation descriptions.

The following actions did not occur:

- cloning or downloading the NeuralGCM repository;
- installing Python, JAX, Dinosaur, Haiku, or other model dependencies;
- downloading or deserializing checkpoints;
- opening ERA5, CMIP6, WeatherBench2, or other large data stores;
- running inference, training, evaluation, notebooks, or model code;
- using a live weather or climate API;
- creating an account, subscription, paid trial, or chargeable resource;
- making an Australian regional, operational, safety, or planning claim.

## 3. Executive research finding

NeuralGCM is suitable as the second model world in the ClimateOS parallel-model
research programme because it differs materially from UniCM in both mechanism
and scale.

NeuralGCM is a hybrid atmospheric general circulation model. It combines a
differentiable dynamical core with learned representations of unresolved
physical processes. Its published scope spans medium-range weather and
atmosphere-only climate simulation. This makes it useful for reading how a
model with explicit large-scale atmospheric dynamics represents evolving
fields across weather and climate timescales.

Current admission is:

`NOW — READ-ONLY SCIENTIFIC ORIENTATION`

The following admissions remain blocked:

- source acquisition;
- checkpoint acquisition;
- data acquisition;
- dependency installation;
- checkpoint deserialization;
- model execution;
- benchmark reproduction;
- Australian regional interpretation;
- operational or consequential use.

## 4. Authoritative source registry

| Source object | Authoritative location | Verified finding | Status |
|---|---|---|---|
| Peer-reviewed paper | https://doi.org/10.1038/s41586-024-07744-y | *Neural general circulation models for weather and climate*, published in *Nature* on 2024-07-22 | VERIFIED |
| Official code repository | https://github.com/neuralgcm/neuralgcm | Public repository under the `neuralgcm` organization | VERIFIED |
| Repository snapshot inspected | https://github.com/neuralgcm/neuralgcm/commit/e139660de68ef3125658e7097e81407d43dd5074 | Current inspected `main` commit, dated 2026-07-08 | PINNED FOR THIS PACK |
| Declared package version at inspected `main` | `pyproject.toml` at the pinned commit | `1.2.3` | VERIFIED DECLARATION / RELEASE STATUS NOT ASSUMED |
| Stable comparison tag inspected | https://github.com/neuralgcm/neuralgcm/tree/v1.2.2 | Tag declares package version `1.2.2` | VERIFIED TAG |
| Official documentation | https://neuralgcm.readthedocs.io/ | Inference-oriented documentation, checkpoint registry and data-preparation guidance | VERIFIED |
| Code licence | Repository `LICENSE` | Apache License 2.0 | VERIFIED |
| Trained-weight licence | Official README and checkpoint documentation | Creative Commons Attribution-ShareAlike 4.0 International | VERIFIED DECLARATION |
| Evaluation framework | https://weatherbench2.readthedocs.io/ | WeatherBench2 is identified for forecast evaluation and archived comparisons | VERIFIED REFERENCE |

### 4.1 Version distinction

The current inspected `main` declaration and the inspected stable tag are not
the same version:

- current inspected `main`: package version `1.2.3`;
- inspected stable tag: `v1.2.2`.

This pack does not infer that `1.2.3` is a published release. A future source
acquisition gate must select one exact commit or release and must not use a
floating `main` branch.

### 4.2 Dependency distinction

At `v1.2.2`, the package declaration includes a version-constrained Dinosaur
dependency. At the current inspected `main`, Dinosaur is declared through a
Git repository URL without an exact commit in the dependency line. The current
`main` therefore has an additional reproducibility risk if installed without a
separately pinned Dinosaur commit.

No dependency was installed in this batch.

## 5. Paper-to-mechanism orientation map

| Scientific or architectural concept | Published or documented representation | ClimateOS reading |
|---|---|---|
| Hybrid atmospheric model | Differentiable atmospheric dynamical core plus learned physics | NeuralGCM is neither a conventional all-physics GCM nor a purely data-driven forecast network. |
| Resolved dynamics | Hydrostatic primitive equations with moisture, horizontal pseudo-spectral discretization and vertical sigma coordinates | Large-scale atmospheric motion is advanced through an explicit numerical structure. |
| Learned unresolved processes | A neural network acts on individual atmospheric columns | Cloud, radiation, precipitation and other sub-grid effects are represented through learned tendencies rather than resolved directly. |
| End-to-end interaction | Learned components are trained while interacting with the dynamical core | The model learns parameterized effects in the context of evolving resolved dynamics. |
| Initial-state translation | Encoder maps pressure-level ERA5 fields to the model state; decoder maps outputs back | The model's internal coordinates and externally readable pressure-level fields are not identical. |
| Deterministic mode | One trajectory from an initialized state | Suitable for bounded trajectory comparisons, not calibrated uncertainty by itself. |
| Stochastic mode | Random fields enter learned components and a CRPS-based training objective supports ensemble behaviour | Represents multiple plausible atmospheric trajectories, subject to model and evaluation limits. |
| Climate simulation | Historical SST and sea-ice concentration are prescribed | The published climate use is atmosphere-only and externally forced, not a coupled ocean-atmosphere projection system. |

Published descriptions are recorded as published evidence. They have not been
independently reproduced by ClimateOS.

## 6. Represented state, inputs and outputs

### 6.1 Prognostic state identified in the paper

The published methods describe seven prognostic variable families:

- horizontal-wind vorticity;
- horizontal-wind divergence;
- temperature;
- surface pressure;
- specific humidity;
- specific ice-cloud water content;
- specific liquid-cloud water content.

### 6.2 Learned-physics inputs identified in the paper

The learned physics component receives information including:

- the prognostic variables in one atmospheric column;
- horizontal gradients of prognostic variables;
- total incident solar radiation;
- sea-ice concentration;
- sea-surface temperature;
- stochastic random fields for stochastic model variants.

### 6.3 Initialization and forcing

The official inference guide initializes model state from ERA5 fields. Climate
simulations require externally supplied SST and sea-ice concentration. The
official checkpoint guide states that NeuralGCM currently models only the
atmosphere.

Consequently, a NeuralGCM result is conditional on:

- the initialization analysis or reanalysis;
- the chosen checkpoint;
- the forcing history and persistence assumptions;
- regridding and coordinate transformation;
- deterministic or stochastic configuration;
- output interval and rollout duration.

### 6.4 Output boundary

The model advances an atmospheric state and can decode predictions to pressure
levels. The learned physics module produces tendencies, not direct proof of an
individual real-world causal process.

The paper notes a version-specific hydrological limitation: the reported model
can diagnose precipitation minus evaporation but cannot, in that configuration,
separate the two contributions directly. Official documentation now also lists
special 2.8-degree stochastic checkpoints trained to predict precipitation and
evaporation, with stated trade-offs. These checkpoint families must not be
silently treated as interchangeable.

## 7. Scale registry

| Dimension | Verified range or form | Observation consequence |
|---|---|---|
| Horizontal model grids | 2.8, 1.4 and 0.7 degrees in the paper and checkpoint registry | Global atmospheric structure can be represented; site and neighbourhood detail cannot be inferred directly. |
| Weather horizon | Published comparisons from 1 to 15 days, depending on deterministic or ensemble question | Medium-range weather behaviour is within the published study scope. |
| Seasonal and climate horizon | Months to multi-decadal atmosphere-only simulations with prescribed boundary forcing | Long runs test stability and climate statistics, not free coupled climate prediction. |
| Internal time integration | Dynamical core advanced with an implicit-explicit ODE solver; learned tendencies commonly held for multiple steps | Output cadence is not the same as the numerical integration step. |
| Vertical representation | Sigma coordinates internally, with pressure-level interfaces | Vertical interpolation and encoding are part of the evidence chain. |
| Geographic domain | Global | Australia is present as part of a global grid, not as a validated local product. |

## 8. Checkpoint manifest from official documentation

The following names and object paths were recorded from official documentation.
No object was accessed.

| Checkpoint family | Official object path | Documented orientation |
|---|---|---|
| 0.7-degree deterministic | `v1/deterministic_0_7_deg.pkl` | Higher-resolution deterministic weather use; documented as slower |
| 1.4-degree deterministic | `v1/deterministic_1_4_deg.pkl` | Weather use and bounded extended simulation |
| 2.8-degree deterministic | `v1/deterministic_2_8_deg.pkl` | Coarser atmosphere and climate orientation |
| 1.4-degree stochastic | `v1/stochastic_1_4_deg.pkl` | Officially recommended for many weather metrics, especially beyond five days |
| 2.8-degree stochastic precipitation | `v1_precip/stochastic_precip_2_8_deg.pkl` | Predicts precipitation and evaporation with documented temporal trade-offs |
| 2.8-degree stochastic evaporation | `v1_precip/stochastic_evap_2_8_deg.pkl` | Predicts precipitation and evaporation; documentation warns of slightly negative precipitation rates |

Official documentation places these objects under `gs://neuralgcm/models/` and
declares CC BY-SA 4.0 for the checkpoints.

The following acquisition facts remain `UNVERIFIED`:

- object byte sizes;
- object generation dates;
- provider checksums;
- cryptographic signatures;
- serialization-library and Python-version compatibility for every object;
- whether all checkpoint licences and embedded metadata are identical;
- retention, egress and service conditions applicable at acquisition time.

## 9. Evaluation orientation

The paper reports comparison with ERA5, ECMWF-HRES, ECMWF-ENS, GraphCast and
Pangu for weather questions, and with climate-model or global
cloud-resolving-model references for climate questions.

The weather evaluation uses WeatherBench2-style questions including:

- root-mean-square error;
- root-mean-square bias;
- continuous ranked probability score;
- spread-skill ratio;
- spatial patterns;
- spectral behaviour;
- geostrophic balance;
- water-budget diagnostics;
- selected weather-phenomenon case studies.

For the reported 2020 weather evaluation, forecasts were regridded to a common
1.5-degree grid. Regridded benchmark equality is not native-resolution equality.

Climate evaluation includes seasonal cycles, stability, long-run bias,
temperature trends and emergent phenomena under prescribed SST and sea ice.
The paper reports both successful and unstable long simulations. Stability is
therefore an evaluated property, not a permanent guarantee.

## 10. Compute, storage, security and cost orientation

### 10.1 Compute

The official quick-start documentation recommends a GPU or TPU because of high
memory and compute requirements. The paper reports very high simulation
throughput on a TPU relative to a conventional comparison system, but that is a
published hardware-specific comparison and not a ClimateOS budget estimate.

No CPU-only viability, local memory requirement, accelerator model, wall-clock
runtime or energy use has been verified for a ClimateOS-controlled environment.

### 10.2 Storage and data movement

The checkpoint sizes are not stated in the inspected checkpoint page. ERA5 and
the comparison datasets are large scientific resources. A small checkpoint
does not imply a small reproducibility exercise because initialization,
forcing, reference trajectories, regridding and evaluation data also consume
storage and transfer capacity.

No storage allocation or data transfer is authorized.

### 10.3 Serialization security

The documented checkpoint objects use the `.pkl` form and the official example
loads them through Python pickle. Pickle deserialization can execute code and
must be treated as an untrusted-code boundary even when an object is hosted by
an official project.

Any future acquisition plan must require, before deserialization:

1. an exact allowlisted object name;
2. a declared byte-size ceiling;
3. provider metadata capture;
4. SHA-256 calculation after bounded download;
5. isolated storage outside the ClimateOS runtime;
6. static inspection where feasible;
7. a disposable, network-disabled execution environment;
8. an explicit Founder gate for deserialization and execution.

### 10.4 Cost

Public visibility is not a zero-cost guarantee. Potential cost surfaces include
cloud egress, ERA5 acquisition, local or cloud storage, accelerator time,
evaluation time and human scientific review.

Current cost status is:

`ZERO COMMITMENT / NO BUDGET AUTHORIZED / COST UNVERIFIED`

## 11. Australian and local applicability

NeuralGCM can represent global atmospheric circulation over Australia, but its
published global-grid skill does not establish skill for Sydney, Alice Springs,
Snowy Valleys, Riverina, a catchment, a property or a project site.

Important missing or separately governed layers include:

- Australian operational analyses and forecasts;
- local topography and urban form;
- radar and station observations;
- catchment, soil, vegetation and fire-domain state;
- regional downscaling or translation;
- local extremes and observation uncertainty;
- qualified Australian scientific review.

ACCESS and other Bureau of Meteorology resources should be registered as an
Australian regional calibration anchor. They should not be represented as a
NeuralGCM component or as proof that NeuralGCM is locally valid.

Current regional classification:

`GLOBAL ATMOSPHERIC RESEARCH REFERENCE / NOT REGIONALLY ADMITTED`

## 12. Source-and-observation risk register

| ID | Risk | Evidence | Severity | Required control |
|---|---|---|---|---|
| NG01 | Floating-source drift | `main` changes and currently declares a different version from the inspected stable tag | High | Pin an exact release and commit before acquisition |
| NG02 | Dependency drift | Current `main` declares Dinosaur through an unpinned Git URL | High | Pin and separately verify every Git dependency |
| NG03 | Weight-integrity uncertainty | Official checkpoint page does not publish inspected checksums or sizes | Critical | Asset manifest, hard size limit and SHA-256 gate |
| NG04 | Unsafe deserialization | Official checkpoints are pickle objects | Critical | No deserialization outside an explicitly authorized sandbox |
| NG05 | Data-volume uncertainty | ERA5 and evaluation datasets are large | High | File-level subset and storage plan before access |
| NG06 | Boundary-forcing dependency | SST and sea ice must be supplied | Critical | Record exact forcing product, version and treatment |
| NG07 | Atmosphere-only boundary | Ocean, land and atmospheric chemistry are not dynamically coupled in the published system | Critical | Do not claim full Earth-system simulation |
| NG08 | Long-run instability | Official documentation gives checkpoint-specific stability limits; the paper reports failed long runs | Critical | Ensemble stability protocol and stop conditions |
| NG09 | Future-climate extrapolation | The paper reports divergence and drift under sufficiently large SST changes | Critical | Do not use as an unrestricted future-climate projector |
| NG10 | Hydrological interpretation | Checkpoint families differ in precipitation treatment | High | Keep checkpoint-specific output contracts |
| NG11 | Benchmark comparability | Some references use different analysis truth and all forecasts may be regridded | High | Preserve benchmark protocol and truth-source differences |
| NG12 | Hardware uncertainty | Official examples recommend accelerator hardware | High | Static local resource estimate before any run gate |
| NG13 | Global-to-local overreach | Coarse global output may be mistaken for local Australian evidence | Critical | Independent regional translation and validation |
| NG14 | Operational misuse | Research output may be mistaken for an official forecast or warning | Critical | Permanent research-only and non-warning labels |
| NG15 | Human authority gap | Code and paper review are not regional scientific validation | Critical | Qualified domain review before consequential use |

## 13. ClimateOS observation frame

| Observation-frame field | NeuralGCM reading |
|---|---|
| Model identity | Hybrid neural general circulation model for the atmosphere |
| Primary object observed | Evolution of the global atmospheric state |
| Native perspective | Dynamical atmospheric fields and learned unresolved-process tendencies |
| Time perspective | Weather trajectories through atmosphere-only climate statistics |
| Space perspective | Global grids at several coarse-to-medium angular resolutions |
| Explicit mechanism | Hydrostatic moist primitive-equation dynamical core |
| Learned mechanism | Column-local learned physical tendencies, plus stochastic components in ensemble variants |
| External boundary | Initialization, SST, sea ice, solar forcing, data transformations |
| Strength for ClimateOS | Bridges weather and climate scales while exposing a meaningful physics/ML boundary |
| Principal blind spot | It is not a coupled ocean-land-chemistry Earth-system model and is not locally validated |
| Uncertainty form | Deterministic trajectory or checkpoint-specific stochastic ensemble |
| Prohibited inference | A global field or learned tendency is not a site fact, causal proof, official warning, or planning approval |
| Human-review need | Atmospheric science, benchmark, Australian regional and domain-impact review |

## 14. Reproducibility position

NeuralGCM has a strong public research surface: paper, code, documentation,
named checkpoints and evaluation references are visible. That is not the same
as end-to-end reproducibility readiness.

Current status by layer:

| Layer | Status |
|---|---|
| Paper identity | VERIFIED |
| Official repository identity | VERIFIED |
| Code licence | VERIFIED |
| Weight-licence declaration | VERIFIED |
| Exact research snapshot | PINNED FOR DOCUMENT REVIEW |
| Exact future acquisition snapshot | NOT SELECTED |
| Checkpoint names | VERIFIED FROM DOCUMENTATION |
| Checkpoint sizes and hashes | UNVERIFIED |
| Dependency closure | UNVERIFIED |
| Data subset and volume | UNVERIFIED |
| Local compute feasibility | UNVERIFIED |
| Model execution | NOT AUTHORIZED / NOT PERFORMED |
| Published-result reproduction | NOT ATTEMPTED |
| Australian regional validation | BLOCKED |

## 15. Gate decision

NeuralGCM is admitted only as a second parallel-model research reference.

The immediate permitted next use is the static UniCM x NeuralGCM multiscale
comparison. Any acquisition or execution task requires a new brief specifying
the exact release, dependency closure, checkpoint object, byte ceiling,
checksums, data subset, compute ceiling, isolation design, zero-cost plan,
scientific question and stop conditions.
