# Task1500 UniCM Research Plan

Date: 2026-07-12
Status: Deferred research plan
Execution gate: Founder authorization at or near Task1500

## Research question

How can ClimateOS learn from UniCM’s unified modelling of coupled global climate modes and translate that method into a governed Environmental Coupling Layer linking climate state, regional environment, ecosystems and human decisions?

## Research objectives

1. Verify and understand the authoritative UniCM scientific and open-source assets.
2. Reproduce a limited published result where practical and lawful.
3. Define a model-neutral Climate Mode Evidence Adapter.
4. Represent cross-system lead-lag relationships and uncertainty without overstating causality.
5. Test one Australian regional climate-to-environment evidence chain.
6. Establish governance rules for scientific provenance, expert review and model replacement.

## Work packages

### WP1 — Source and licence verification

Evidence required:

- official repository URL;
- repository owner and institutional connection;
- licence text;
- paper-code version relationship;
- release, tag or commit reference;
- weights and dataset availability;
- citation and redistribution requirements.

Exit criterion: authoritative source identity and legal-use note completed.

### WP2 — Architecture study

Study:

- input physical fields and indices;
- climate-mode definitions;
- temporal resolution and forecast horizon;
- Globalformer / Modeformer or equivalent components;
- coupling and information-exchange mechanisms;
- loss functions and training strategy;
- ensemble, uncertainty and evaluation methods;
- known limitations.

Exit criterion: paper-to-code architecture map completed.

### WP3 — Reproducibility feasibility

Assess:

- operating system and Python/CUDA requirements;
- GPU memory, storage and runtime;
- data preprocessing burden;
- pretrained checkpoints;
- evaluation scripts;
- reproducibility blockers;
- minimum viable sample experiment.

Exit criterion: go / constrained-go / no-go recommendation.

### WP4 — Limited reproduction

Candidate experiments:

- load a published checkpoint;
- reproduce one climate-mode time series or metric;
- inspect one lead-lag relationship;
- compare output against a documented baseline;
- record all deviations and uncertainty.

Exit criterion: reproducibility report with evidence lineage. Failure to reproduce is an acceptable scientific result if documented honestly.

### WP5 — ClimateOS interface

Design a model-neutral adapter that accepts outputs from UniCM or future alternatives.

Minimum fields:

- model and version;
- issue and target time;
- climate mode;
- predicted state/index;
- probability or ensemble information;
- geographic and temporal scope;
- source datasets;
- confidence and limitations;
- Evidence Passport reference.

Exit criterion: adapter schema and validation examples.

### WP6 — Environmental Coupling Layer

Develop a graph or registry of environmental relationships with explicit evidence classes:

- observed association;
- lagged predictive signal;
- model inference;
- causal hypothesis;
- expert-confirmed mechanism.

Each relationship must record geography, period, stationarity warning, uncertainty and review status.

Exit criterion: coupling-layer schema and read-only prototype.

### WP7 — Australian pilot

Preferred initial study area: Snowy Valleys / Riverina / south-eastern Australia.

Candidate chain:

```text
ENSO + IOD + SAM
→ rainfall / temperature regime
→ soil moisture / water availability
→ vegetation stress / fire or agricultural risk
→ planning interpretation
```

The pilot should use public and traceable datasets, avoid operational warning claims, and include relevant Australian scientific review.

Exit criterion: one complete Coupled Environmental Evidence Passport.

## Evaluation framework

Evaluate five dimensions:

1. **Scientific fidelity** — alignment with published definitions and metrics.
2. **Reproducibility** — ability to repeat the workflow with recorded versions.
3. **Transferability** — usefulness beyond the original model and dataset.
4. **Decision relevance** — whether outputs can support bounded regional interpretation.
5. **Governance quality** — provenance, uncertainty, limitations and human review.

## Risks

- official repository or weights may not be publicly available;
- datasets may be too large or restricted;
- compute requirements may exceed available hardware;
- historical relationships may not remain stable under climate change;
- model correlations may be mistaken for causal mechanisms;
- regional translation may amplify uncertainty;
- later scientific models may supersede UniCM before Task1500.

Mitigation: maintain a model-neutral architecture and re-evaluate the scientific landscape at the Task1500 gate.

## Expected outputs

- UniCM Source and Licence Dossier;
- Paper-to-Code Architecture Map;
- Reproducibility Feasibility Report;
- Limited Reproduction Evidence Package;
- Climate Mode Evidence Adapter v0.1;
- Environmental Coupling Layer v0.1;
- Australian Coupled Climate–Environment Pilot;
- Task1700 Governance and Continuation Review.

## Stop conditions

Stop or return to Founder review if:

- source identity or licence cannot be verified;
- required data are inaccessible or legally unsuitable;
- compute burden is disproportionate to learning value;
- reproduction results are materially inconsistent;
- the project starts making operational or causal claims beyond evidence;
- a newer model offers a clearly stronger and more open path.

## Reminder

This research plan is deliberately deferred. Its purpose is to preserve direction, not to compete with currently authorized ClimateOS work. **Task1500 remains the formal activation point.**