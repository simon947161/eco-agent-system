# Task1500–1700 — UniCM-Inspired Environmental Coupling Layer Roadmap

Date: 2026-07-12
Status: Long-range founder roadmap / research authorization seed
Primary milestone: **Task1500**
Planning horizon: Task1500–1700
Project: ClimateOS / Eco-Agent-System

## 1. Founder intention

ClimateOS shall preserve a long-range development objective beginning at **Task1500**: study, reproduce where feasible, and responsibly adapt the scientific ideas and open-source implementation associated with UniCM, the unified global climate-mode prediction model described in:

Yuan, Y., Ding, J., Qiu, Z. et al. *Learning the coupled dynamics of global climate modes*. Nature Machine Intelligence (2026). DOI: https://doi.org/10.1038/s42256-026-01245-5

This objective is not an authorization to immediately build or claim a working climate model. It is a protected roadmap target so that the idea is not lost while ClimateOS completes nearer-term tasks.

## 2. Strategic reason

ClimateOS should not remain a collection of isolated climate, water, land, carbon, ecology and infrastructure agents. Its long-term value depends on understanding how environmental systems influence one another across time and space.

UniCM provides an important architectural lesson: predictive information may emerge from the coupled relationships among several climate modes rather than from any one mode in isolation.

ClimateOS should therefore develop an **Environmental Coupling Layer (ECL)** that can represent, test and govern relationships such as:

```text
Global climate modes
    ↕
Regional weather regimes
    ↕
Hydrology and soil moisture
    ↕
Vegetation and ecosystem response
    ↕
Fire, agriculture, energy and infrastructure risk
    ↕
Human and governance decisions
```

## 3. Position inside the wider ClimateOS science roadmap

Task1500–1700 is the central coupling workstream, but it must not stand alone.

```text
Task1200–1499
Model assurance + hybrid weather runtime
        ↓
Task1500–1700
Environmental Coupling Layer
        ↓
Task1701–1899
Mechanism Experiment Layer
        ↓
Task1900–2099
Environmental AI Scientist Runtime
```

The logic is deliberate:

1. first determine whether models are scientifically and operationally trustworthy;
2. then connect physical and AI forecast sources in a governed runtime;
3. then represent cross-system environmental relationships;
4. then test mechanisms through controlled numerical experiments;
5. only after that consider a broader autonomous environmental scientist runtime.

Related roadmap files:

- `docs/tasks/task1200_1499_model_assurance_hybrid_weather/TASK1200_1499_MODEL_ASSURANCE_AND_HYBRID_WEATHER_ROADMAP.md`
- `docs/tasks/task1701_2099_mechanism_scientist_runtime/TASK1701_2099_MECHANISM_EXPERIMENT_AND_ENVIRONMENTAL_AI_SCIENTIST_ROADMAP.md`

## 4. Relationship to existing ClimateOS roadmap

Task601 established the future Life System Module and Living Evidence concept. Task1500 extends that direction by adding a system-level coupling architecture.

```text
Task601: Life System Module
    ↓
Living Evidence and ecological response
    ↓
Task1200–1499: model assurance and hybrid forecast inputs
    ↓
Task1500: Environmental Coupling Layer
    ↓
Task1701–2099: mechanism validation and AI scientist runtime
```

Task601 asks how living systems respond to environmental change. Task1500 asks how climate, water, land, life and human systems jointly evolve and exchange predictive information.

## 5. Proposed ClimateOS position

The Environmental Coupling Layer should sit above specialist models and below mechanism experimentation and decision governance.

```text
Climate State Layer
- ENSO, IOD, SAM, MJO and other climate modes
- UniCM-inspired coupled-mode representation

Weather and Forecast Input Layer
- physical forecast systems
- AI forecast systems
- regional downscaling and observation updates
- model comparison and provenance

Environmental Coupling Layer
- lagged relationships
- cross-system state exchange
- uncertainty propagation
- causal-hypothesis registry
- evidence lineage

Domain Layers
- WaterOS
- LandOS
- CarbonOS
- Life System Module
- EnergyOS
- BuildingOS

Mechanism Experiment Layer
- controlled perturbation experiments
- WRF-Chem / WRF-Hydro / land and ecological models
- evidence-chain diagnostics

Decision and Governance Layer
- scenario comparison
- Evidence Passport
- human approval
- limitations and confidence reporting
```

## 6. Independent reference frameworks

The following are separate reference frameworks. They are not one combined development task and must not be treated as interchangeable products.

### 6.1 UniCM — coupled climate-state reference

Role: long-range climate-mode representation and coupled predictability.

ClimateOS use: inspiration for the Environmental Coupling Layer and Climate Mode Evidence Adapter.

### 6.2 PhysMetrics.Weather — model assurance reference

Role: evaluate physical consistency beyond RMSE and ACC, including mass, energy, spectra and balance diagnostics.

ClimateOS use: upstream scientific admission and continuous model assurance. It belongs primarily in Task1200–1299, not inside the ECL implementation itself.

Reference record:

- `docs/references/climateos_scientific_frameworks/PHYSMETRICS_WEATHER_REFERENCE_FRAMEWORK.md`

### 6.3 AICON — hybrid operational forecast reference

Role: demonstrate how a national meteorological service can run an AI forecast model alongside a physics-based operational model, with higher-frequency updates and human oversight.

ClimateOS use: architecture reference for Task1300–1499 Hybrid Weather Intelligence Runtime.

Reference record:

- `docs/references/climateos_scientific_frameworks/AICON_REFERENCE_FRAMEWORK.md`

### 6.4 TianJi-Environ — mechanism experiment reference

Role: convert atmospheric-environment hypotheses into controlled WRF-Chem experiments, diagnostics and auditable evidence chains.

ClimateOS use: architecture reference for Task1701–1899 Mechanism Experiment Layer and Task1900–2099 Environmental AI Scientist Runtime.

Reference record:

- `docs/references/climateos_scientific_frameworks/TIANJI_ENVIRON_REFERENCE_FRAMEWORK.md`

## 7. Task1500 entry gate

Task1500 shall begin only after an explicit Founder authorization and a preflight review covering:

1. current ClimateOS architecture and repository state;
2. completion or bounded readiness of the Task1200–1499 assurance and forecast-input foundations;
3. official UniCM publication, code repository, licence and model/data availability;
4. compute and storage requirements;
5. scientific and legal constraints;
6. whether reproduction is feasible on available hardware;
7. a bounded pilot that does not interrupt active ClimateOS delivery.

The official UniCM source repository has **not yet been reliably verified in this planning record**. No code shall be cloned or incorporated until the repository identity and licence are confirmed from an authoritative source.

## 8. Task roadmap

### Task1500–1520 — Source verification and scientific orientation

- verify the official UniCM repository and maintainers;
- record licence, citation, model weights, datasets and dependencies;
- map the paper’s inputs, outputs, climate modes and evaluation metrics;
- distinguish published claims from ClimateOS interpretation;
- prepare a reproducibility risk register;
- confirm that upstream model-assurance rules are available.

**Deliverable:** UniCM Source and Reproducibility Dossier.

### Task1521–1550 — Safe repository acquisition and environment setup

- fork or vendor only after licence review;
- preserve upstream origin and commit hash;
- create a separate experimental environment;
- produce dependency lock files and hardware notes;
- prohibit silent modification of scientific baselines.

**Deliverable:** isolated UniCM research workspace with provenance record.

### Task1551–1600 — Minimal reproduction study

- run published inference or evaluation on a bounded sample;
- reproduce one or two reported climate-mode metrics where feasible;
- document failures, missing data and compute limits;
- compare observations, reanalysis and model outputs;
- apply available statistical and physical assurance checks;
- avoid operational forecasting claims.

**Deliverable:** limited reproduction report and evidence package.

### Task1601–1640 — ClimateOS adapter design

Develop a read-only adapter rather than directly merging UniCM code into the ClimateOS core.

Candidate interface:

```yaml
climate_mode_state:
  mode_name:
  issue_time:
  target_period:
  predicted_index:
  ensemble_or_probability:
  confidence:
  source_model:
  source_version:
  input_dataset:
  spatial_scope:
  limitations:
  assurance_status:
  evidence_passport_id:
```

**Deliverable:** Climate Mode Evidence Adapter v0.1.

### Task1641–1670 — Environmental Coupling Layer prototype

- create a coupling graph schema;
- represent lead-lag relationships without claiming causality;
- connect climate-mode states to WaterOS, LandOS and Life System evidence;
- track uncertainty transformations;
- require human review for scientific interpretation;
- register candidate mechanisms for later testing without pretending they are proven.

Candidate relationship record:

```yaml
coupling_relation_id:
source_state:
target_state:
relationship_type: [observed_association, lagged_signal, model_inference, causal_hypothesis]
lead_lag_window:
geography:
time_period:
evidence_sources:
model_method:
confidence:
stationarity_warning:
expert_review_status:
future_mechanism_test_id:
```

**Deliverable:** Environmental Coupling Layer prototype v0.1.

### Task1671–1700 — Australian regional pilot and transition gate

Preferred pilot chain:

```text
ENSO / IOD / SAM climate background
→ south-eastern Australian rainfall and heat regime
→ Snowy Valleys / Riverina soil moisture and water stress
→ vegetation, fire, agriculture or biodiversity response
→ planning and governance interpretation
```

The pilot must clearly separate:

- climate-mode prediction;
- regional translation;
- impact modelling;
- expert interpretation;
- governance recommendation;
- candidate mechanisms requiring later controlled experiments.

**Deliverable:** Australian Coupled Climate–Environment Evidence Pilot and Task1700 transition review.

Task1700 does not authorize WRF-Chem or other high-cost mechanism experiments automatically. It prepares a bounded candidate list for the Task1701 gate.

## 9. Learning and open-source study method

```text
Paper
→ official repository
→ licence and provenance
→ README and environment
→ data pipeline
→ model architecture
→ inference path
→ evaluation path
→ statistical and physical assurance
→ minimal reproduction
→ adapter
→ bounded ClimateOS pilot
```

Rules:

- do not begin by rewriting the model;
- do not copy code without preserving licence and attribution;
- do not merge experimental dependencies into ClimateOS core;
- do not interpret attention or correlation as established causation;
- do not claim operational climate prediction from a research reproduction;
- keep all source, model and transformation lineage in an Evidence Passport;
- transfer unproven mechanisms to the later Mechanism Experiment Layer.

## 10. Success criteria

Task1500–1700 succeeds if ClimateOS can:

1. ingest a climate-mode prediction with traceable provenance;
2. represent cross-system relationships and lead-lag signals;
3. propagate uncertainty rather than hide it;
4. connect global climate state to a bounded Australian regional evidence chain;
5. expose scientific assumptions for expert and Founder review;
6. remain modular so UniCM can be replaced or compared with later models;
7. produce a disciplined list of mechanism hypotheses for later experiment, without claiming causality prematurely.

It does not require ClimateOS to train a global foundation model from scratch.

## 11. Boundaries

This roadmap does not authorize:

- operational public warnings;
- deterministic claims about floods, fires, droughts or ecosystems;
- automated policy decisions;
- unreviewed causal conclusions;
- redistribution of restricted datasets or weights;
- premature expansion of current tasks before the Task1500 gate;
- automatic launch of Task1701 mechanism experiments.

## 12. Permanent reminders

> **Task1200 is the formal return point for model assurance foundations.**

> **Task1300 is the formal return point for hybrid physical-plus-AI forecast runtime design.**

> **Task1500 is the formal return point for UniCM and the Environmental Coupling Layer.**

> **Task1701 is the formal return point for mechanism experiment protocols.**

> **Task1900 is the formal return point for the Environmental AI Scientist Runtime.**

When ClimateOS approaches any of these gates, retrieve the relevant roadmap and reference records, verify the current scientific and repository state, and prepare a fresh executable authorization. Historical roadmap text must never be treated as automatic implementation approval.

## Project keywords

ClimateOS; Task1200; Task1300; Task1500; Task1701; Task1900; Task1500–1700; UniCM; PhysMetrics.Weather; AICON; TianJi-Environ; Environmental Coupling Layer; Model Assurance; Hybrid Weather Runtime; Mechanism Experiment Layer; Environmental AI Scientist Runtime; ENSO; IOD; SAM; MJO; Evidence Passport; Australian climate risk; Snowy Valleys; Riverina.