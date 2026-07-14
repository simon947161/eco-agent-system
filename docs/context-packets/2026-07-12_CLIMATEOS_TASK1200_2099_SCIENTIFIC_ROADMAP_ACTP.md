# ACTP — ClimateOS Task1200–2099 Scientific Roadmap Transfer Packet

Date: 2026-07-12
Status: Draft transfer packet for ClimateOS main thread
Source thread scope: UniCM, PhysMetrics.Weather, AICON, TianJi-Environ, ClimateOS scientific roadmap integration
Repository: simon947161/eco-agent-system
Review branch: agent/task1500-unicm-coupling-roadmap
Review PR: #42

---

## 1. Transfer purpose

This ACTP transfers the conclusions and roadmap decisions from the current research discussion into the main ClimateOS conversation thread.

The receiving ClimateOS thread should understand that the Founder has approved preservation of a long-range scientific development path for ClimateOS. This path does not authorize immediate implementation. It creates protected future return gates and reference architectures so that the ideas are not lost.

The long-term objective is to evolve ClimateOS from an environmental-agent and evidence-governance platform into a scientifically governed Earth-system intelligence operating system capable of:

- evaluating whether models are statistically and physically trustworthy;
- operating physical and AI forecast sources together;
- representing coupled climate–water–land–life relationships;
- testing environmental mechanism hypotheses through controlled numerical experiments;
- producing reproducible and auditable scientific evidence;
- retaining human scientific and governance approval.

---

## 2. Founder decision preserved

The following roadmap is now the intended long-range sequence:

```text
Task1200–1299
Model Assurance Foundation

Task1300–1499
Hybrid Weather Intelligence Runtime

Task1500–1700
Environmental Coupling Layer

Task1701–1899
Mechanism Experiment Layer

Task1900–2099
Environmental AI Scientist Runtime
```

The reasoning order is mandatory:

```text
First evaluate model trustworthiness
→ then integrate and orchestrate models
→ then represent cross-system coupling
→ then test mechanisms experimentally
→ only then consider a bounded AI scientist runtime
```

The roadmap must not be interpreted as permission to skip existing nearer-term ClimateOS tasks.

---

## 3. Five permanent return gates

### Task1200 — Model Assurance Foundation

Return topic:

- model registry;
- model version, licence and provenance;
- WeatherBench-style statistical evaluation;
- PhysMetrics-style physical-consistency evaluation;
- extreme-event and regional-suitability review;
- Model Evidence Passport;
- Model Admission Gate.

No model should enter later ClimateOS scientific layers merely because it has low RMSE or a strong publication claim.

### Task1300 — Hybrid Weather Intelligence Runtime

Return topic:

- physical NWP and AI weather-model parallel operation;
- common data contracts;
- model divergence comparison;
- high-frequency AI updates;
- physical-model fallback;
- human review and operational boundaries.

AICON is a reference for this operating philosophy. It is not an automatic code dependency.

### Task1500 — Environmental Coupling Layer

Return topic:

- UniCM and global climate-mode coupling;
- ENSO, IOD, SAM, MJO and other relevant modes;
- Climate Mode Evidence Adapter;
- lagged and cross-system relationships;
- uncertainty propagation;
- Australian south-eastern climate–water–soil–life pilot.

Task1500 remains the formal return point for UniCM research and Environmental Coupling Layer work.

### Task1701 — Mechanism Experiment Layer

Return topic:

- structured environmental mechanism hypotheses;
- baseline, perturbation and sensitivity experiments;
- professional numerical-model execution contracts;
- mechanism diagnostics;
- Mechanism Evidence Passport;
- evidence states including supported, partial, incomplete, contradicted and model failure.

TianJi-Environ is the main reference pattern for this layer. It is not one merged development task.

### Task1900 — Environmental AI Scientist Runtime

Return topic:

- bounded Literature, Hypothesis, Experiment Planning, Configuration, Execution, Diagnostic, Evidence Critic and Human Review roles;
- least-privilege tools;
- immutable experiment records;
- human approval before scientific execution and before conclusions;
- no autonomous public warnings or unreviewed scientific claims.

---

## 4. Independent reference frameworks

The following references are deliberately kept separate.

### 4.1 PhysMetrics.Weather

ClimateOS role:

- independent model-assurance reference;
- physical consistency in addition to RMSE/ACC;
- conservation drift, effective resolution, spectra, dynamical balance and vertical structure;
- future Model Admission Gate input.

It must not be merged with AICON or TianJi-Environ into one development package.

### 4.2 AICON

ClimateOS role:

- independent operational-architecture reference;
- demonstrates a national meteorological-service pattern of AI and physical-model coexistence;
- informs high-frequency AI forecast updates, comparison, fallback and expert supervision.

It is a governance and operational reference unless later code, data and licence review explicitly authorizes more.

### 4.3 TianJi-Environ

ClimateOS role:

- independent mechanism-research workflow reference;
- converts hypotheses into controlled numerical experiments and auditable evidence chains;
- informs future WRF-Chem or other professional-model orchestration;
- legitimizes incomplete evidence and failed mechanisms as valid outputs.

It must not be treated as permission to run WRF-Chem now.

### 4.4 UniCM

ClimateOS role:

- principal scientific reference for the Task1500–1700 coupling roadmap;
- motivates joint representation of global climate modes and emergent predictability;
- supports a model-neutral Climate Mode Evidence Adapter rather than permanent vendor or model lock-in.

The official UniCM repository, licence, weights and reproducibility requirements must be reverified at Task1500.

---

## 5. Existing GitHub records to read

The receiving ClimateOS thread should inspect the files on PR #42, especially:

```text
docs/tasks/task1200_1499_model_assurance_hybrid_weather/
TASK1200_1499_MODEL_ASSURANCE_AND_HYBRID_WEATHER_ROADMAP.md

docs/tasks/task1500_1700_environmental_coupling_layer/
TASK1500_1700_UNICM_ENVIRONMENTAL_COUPLING_LAYER_ROADMAP.md
TASK1500_UNICM_CRP.md
TASK1500_UNICM_ICTP.md
TASK1500_UNICM_RESEARCH_PLAN.md

docs/tasks/task1701_2099_mechanism_scientist_runtime/
TASK1701_2099_MECHANISM_EXPERIMENT_AND_ENVIRONMENTAL_AI_SCIENTIST_ROADMAP.md

docs/references/climateos_scientific_frameworks/
PHYSMETRICS_WEATHER_REFERENCE_FRAMEWORK.md
AICON_REFERENCE_FRAMEWORK.md
TIANJI_ENVIRON_REFERENCE_FRAMEWORK.md
```

Also preserve the relationship to:

```text
docs/tasks/task601_life_system_module/
TASK601_LIFE_SYSTEM_MODULE_ROADMAP.md
```

Task601 established Living Evidence and the Life System Module. Task1500 later connects these life-system responses to climate, water, land and human-system coupling.

---

## 6. Instructions for the receiving ClimateOS thread

The receiving thread should:

1. acknowledge this as a long-range Founder roadmap decision;
2. record the five return gates in its working context or PROJECT_CONTEXT.md when appropriate;
3. avoid starting Task1200 or later work merely because this ACTP exists;
4. continue the currently authorized ClimateOS task range without scope diversion;
5. when approaching any return gate, retrieve the relevant roadmap and reference files;
6. re-check the latest scientific literature, official repositories, licences, datasets, compute needs and current ClimateOS architecture;
7. prepare a fresh bounded preflight and Founder authorization before implementation;
8. retain model-neutral adapters, evidence lineage, uncertainty and human approval throughout.

The receiving thread should not merge all reference systems into a single monolithic model or task.

---

## 7. Current boundaries

This ACTP does not authorize:

- training or deploying a global weather or climate model;
- cloning or integrating unverified UniCM code;
- integrating AICON as a runtime dependency;
- running WRF-Chem or TianJi-Environ experiments;
- public weather or hazard warnings;
- automatic causal conclusions;
- autonomous scientific publication;
- interruption of active nearer-term ClimateOS work;
- automatic progression from one gate to the next.

All current records remain Draft / roadmap / research-planning material pending Founder review and future gate-specific authorization.

---

## 8. Immediate receiving-thread action

The immediate action is not implementation.

The ClimateOS main thread should preserve this transfer packet as strategic context and add a reminder similar to:

> ClimateOS has a protected scientific roadmap from Task1200 to Task2099. When approaching Task1200, Task1300, Task1500, Task1701 or Task1900, retrieve PR #42 and this ACTP, reverify current science and repository state, then request fresh Founder authorization.

---

## 9. CRP harvest block

### Core knowledge points

- ClimateOS now has a staged scientific roadmap spanning model assurance, hybrid forecasting, environmental coupling, mechanism experiments and a bounded AI scientist runtime.
- PhysMetrics.Weather, AICON and TianJi-Environ are independent reference frameworks with different architectural roles.
- UniCM remains the central reference for Task1500 Environmental Coupling Layer work.

### Idea points

- ClimateOS should become scientifically governed rather than merely model-rich.
- Prediction, physical assurance, coupled-system understanding and mechanism validation should form one traceable evidence chain.
- Human scientific review remains part of the architecture, not an external afterthought.

### Desire points

- Build ClimateOS into a genuine environmental science operating system.
- Connect global climate states to regional environmental processes and governed decisions.
- Enable future AI-assisted scientific experimentation without sacrificing reproducibility or responsibility.

### Reasoning points

- Model assurance must precede model integration.
- Operational model orchestration must precede environmental coupling.
- Coupling representation must precede mechanism experiments.
- Mechanism protocols must precede any environmental AI scientist runtime.

### Key decisions

- Preserve five future return gates: Task1200, Task1300, Task1500, Task1701 and Task1900.
- Keep PhysMetrics.Weather, AICON and TianJi-Environ as separate reference records.
- Use PR #42 as the current unified review and handoff package.

### Unresolved questions

- When should PR #42 be merged into main?
- How will future PROJECT_CONTEXT and task indexes surface the five gates?
- Which model and Australian regional case should become the first bounded pilots?
- What minimum compute, data and expert-review capacity will exist at each gate?

### Next actions

- Transfer this ACTP to the ClimateOS main conversation.
- Ask that thread to acknowledge and preserve, not execute, the roadmap.
- Continue current authorized ClimateOS work.
- Revisit the roadmap only at the relevant future gate or on explicit Founder request.

### Project keywords

ClimateOS; ACTP; Task1200; Task1300; Task1500; Task1701; Task1900; Task2099; PhysMetrics.Weather; AICON; UniCM; TianJi-Environ; Model Assurance; Hybrid Weather Intelligence; Environmental Coupling Layer; Mechanism Experiment Layer; Environmental AI Scientist; Evidence Passport; Scientific Governance.
