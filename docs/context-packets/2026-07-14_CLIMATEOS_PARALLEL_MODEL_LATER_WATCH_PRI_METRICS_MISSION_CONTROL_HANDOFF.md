# ClimateOS Parallel Model LATER/WATCH Handoff to PRI and Metrics Mission Control

Date: 2026-07-14

Status: FUTURE_RESEARCH_HANDOFF / NON-OPERATIONAL / NO_AUTOMATION

## 1. Purpose

This handoff parks the deferred ClimateOS parallel-model candidates in a form
that a future PRI / Matrix routing layer and Metrics Mission Control may observe
without interrupting the active ClimateOS Task1500–1700 workstream.

PRI is a routing and governance layer. It does not become ClimateOS, does not
create scientific authority, and does not authorize research or implementation.
Metrics Mission Control may later display review state and trigger conditions;
it must not automatically promote, acquire, execute or rank candidates.

## 2. Source decision

The authoritative research source for this handoff is:

- `CLIMATEOS_PARALLEL_MODEL_REGISTRY_DRAFT_V0_1.md`;
- `NEURALGCM_SOURCE_AND_OBSERVATION_RESEARCH_PACK.md`;
- `UNICM_NEURALGCM_MULTISCALE_COMPARISON_REPORT.md`;
- `2026-07-14_CLIMATEOS_PARALLEL_MODEL_AND_SCIENTIFIC_RESOURCE_DISCOVERY_ACTP.md`.

The current active pair is UniCM plus NeuralGCM. All entries below are deferred
unless a fresh Founder authorization changes their state.

## 3. PRI routing contract

Each future candidate should be routed as a Knowledge Object candidate with:

| Field | Meaning |
|---|---|
| `candidate_id` | Stable registry identifier |
| `object_type` | Model, evaluation framework, data resource or architecture reference |
| `queue_class` | `LATER` or `WATCH` |
| `scientific_question` | Why ClimateOS may need the object |
| `activation_trigger` | Evidence or milestone required before research starts |
| `current_blocker` | Licence, source, access, variables, compute, maturity or task-sequence blocker |
| `last_source_review` | Date of authoritative-source review |
| `freshness_due` | Date or event requiring recheck |
| `required_human_role` | Scientific, licence, security, cost or regional reviewer |
| `prohibited_actions` | Actions not allowed while parked |
| `promotion_authority` | Founder or explicitly delegated human authority |
| `destination_gate` | Named ClimateOS task or future research gate |

PRI routing must preserve the original evidence and must not convert missing
fields into assumed readiness.

## 4. Metrics Mission Control display contract

Metrics Mission Control may later expose only governance and research-readiness
metrics for this queue:

- candidate count by object type and queue class;
- official-source verification coverage;
- exact-version coverage;
- licence and weight-licence verification coverage;
- variable-contract completeness;
- regional-fitness evidence coverage;
- compute, storage, security and cost-estimate coverage;
- number of active blockers;
- date of last human source review;
- next scheduled review event;
- Founder gate state.

It must not display:

- a universal model score;
- an automatic winner or recommended production model;
- invented readiness percentages derived from unknown fields;
- benchmark values detached from model version and evaluation protocol;
- an implied authorization to download, execute or integrate;
- a local forecast or operational warning.

## 5. LATER queue

| Candidate | Object type | Future question | Activation trigger | Current blocker |
|---|---|---|---|---|
| GraphCast | Model | What does a primarily data-driven global weather model add after UniCM and NeuralGCM? | Founder approves third-model read-only research after Registry v0.1 review | Third-model scope not authorized |
| GenCast | Model | How should probabilistic global weather worlds enter uncertainty propagation? | Deterministic/stochastic comparison protocol and exact source review exist | Source, weight, ensemble and compute verification pending |
| ICON | Model family / product family | What explicit-physics reference is accessible for comparison and fallback? | Exact open configuration, licence and product boundary verified | Family/product/source layers not separated |
| IFS | Model family / product family | Which analysis, deterministic and ensemble products can serve as physical references? | Exact cycle, product, access and terms selected | Open and restricted resources may be confused |
| RealBench | Evaluation framework | How should real-world and decision relevance be evaluated independently? | Separate Founder gate defines claim classes and human review | Current pair is source-level, not real-world benchmark-ready |
| ERA5-Land | Data resource | Which land variables can support later regional translation? | Exact product, variable subset and licence review | No data access authorized |
| CMIP6 | Data resource | Which experiment/member records support climate comparison without becoming truth? | Exact experiment, ensemble member and purpose defined | Archive scale and model-ensemble interpretation |
| Australian stations, radar and climate products | Data resources | Which official observations can anchor regional claims? | Named regional question and lawful access plan | Product-specific access and human responsibility pending |

## 6. WATCH queue

| Candidate | Object type | Watch reason | Promotion evidence required |
|---|---|---|---|
| Pangu-Weather | Model | High-value deterministic global weather comparison | Current official source, licence, weights, variables and input contract |
| FuXi | Model family | Independent medium-range AI-weather world | Exact model identity, repository, licence and checkpoint availability |
| Aurora | Foundation-model family | Cross-domain atmospheric and environmental representation | Exact task-specific licence, weights, variables and commercial boundary |
| ArchesWeather / ArchesWeatherGen | Model family | Long-run AI atmosphere and climate-statistics research | Official source identity, release, forcing and stability evidence |
| AirCast-SR | Downscaling model | Possible global-to-regional translation layer | Australian transfer evidence, variables, licence and local validation design |
| ObsCast | Observation-driven model | Possible short-range observation world | Observation infrastructure, portability, source and licence verification |
| PhysMetrics.Weather | Evaluation framework | Physical-consistency evaluation beyond aggregate forecast error | Current paper/repository version and metric applicability crosswalk |
| AIMIP | Intercomparison framework | Pattern for comparing long-running AI atmosphere models | Exact framework identity, protocol, source and governance review |
| RESDC | Data/scientific platform | Possible regional or environmental data resource | Authoritative identity, coverage, licence and access verified |
| AICON | Architecture reference | Physical-plus-AI operational dual-track pattern | Current institutional documentation and exact available product boundary |

## 7. Permanent parked-state prohibitions

While an entry remains `LATER` or `WATCH`, PRI and Metrics Mission Control must
not:

- clone a repository;
- download code, weights or data;
- invoke a model or external API;
- create an account, trial or paid commitment;
- change ClimateOS runtime or adapters;
- rank candidates automatically;
- infer scientific readiness from popularity;
- convert a watch signal into a task authorization;
- bypass Founder or human scientific review.

## 8. Promotion rule

Promotion from `WATCH` to `LATER`, or from `LATER` to `NOW`, requires:

1. a bounded scientific question;
2. current official-source verification;
3. a named task and non-scope;
4. licence, access, variables, regional relevance, security and cost preflight;
5. a human responsibility assignment;
6. explicit Founder authorization.

Promotion is a governance decision, not a metric threshold.

## 9. Active-track separation

This handoff removes deferred-candidate monitoring from the active Task1551–1560
work. The active ClimateOS thread returns to the Environmental Coupling Layer
and the Model-Neutral Parallel Evidence Contract.
