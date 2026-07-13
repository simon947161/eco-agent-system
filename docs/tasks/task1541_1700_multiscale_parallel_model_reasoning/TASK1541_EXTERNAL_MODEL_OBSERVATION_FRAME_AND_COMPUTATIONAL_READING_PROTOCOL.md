# Task1541 — External Model Observation Frame and Computational Reading Protocol

Date: 2026-07-14

Status: PROPOSED SPECIFICATION / NON-EXECUTABLE

## 1. Purpose

This protocol defines how ClimateOS reads an external model before using, comparing or translating its output.

It applies to UniCM and future weather, climate, hydrology, land, ecology, energy, building, carbon and socio-economic models.

## 2. Observation Frame

Every model or model output must declare:

| Dimension | Required question |
|---|---|
| observer_position | From what spatial and system position does the model observe? |
| spatial_scale | Planetary, basin/mode, continental, macroregional, locality/city, site/asset or another declared scale? |
| spatial_support | Grid, polygon, station, catchment, administrative area, asset or latent field? |
| temporal_resolution | What is the computational time step? |
| temporal_horizon | What forecast, reconstruction or scenario horizon applies? |
| data_period | Which historical or scenario period shaped the model? |
| variable_ontology | What states and indices exist in the model world? |
| drivers | Which external or internal forces can change those states? |
| mechanism_class | Physical equation, statistical association, learned representation, engineering estimate or hybrid? |
| boundary_conditions | What is held fixed, supplied externally or excluded? |
| omitted_mechanisms | What relevant process cannot be represented? |
| uncertainty_form | Ensemble, probability, interval, residual, scenario range, qualitative warning or none? |
| validation_domain | Where and when was the model evaluated? |
| human_responsibility | Who may interpret the result and for what decision class? |

A missing dimension is a visible gap, not a field to be silently inferred.

## 3. Computational Reading Record

ClimateOS shall read the route from inputs to outputs:

Source and data
→ preprocessing
→ state representation
→ information exchange
→ model transformation
→ objective or loss
→ inference or simulation
→ evaluation
→ downstream interpretation

For each step, record:

- code or publication reference;
- version;
- input and output semantics;
- scale transformation;
- assumptions;
- uncertainty effect;
- failure behaviour;
- licence and provenance;
- whether the step was inspected, reproduced or only reported by the source.

## 4. Cross-scale translation record

Any movement between scales must record:

- source scale;
- target scale;
- reason for translation;
- intermediate variables;
- aggregation, downscaling or inference method;
- calibration evidence;
- uncertainty before and after;
- omitted local or global mechanisms;
- non-stationarity warning;
- human reviewer;
- prohibited interpretations.

No direct global-to-site claim is admitted without declared intermediate bridges.

## 5. Mechanism analogy record

A candidate analogy between places or systems must state:

- compared entities;
- candidate shared mechanism;
- relevant variables;
- similarity evidence;
- difference evidence;
- scale compatibility;
- temporal compatibility;
- confounders;
- transfer limits;
- expert-review status.

Sydney and Shanghai, or Alice Springs and Karamay, may be evaluated through this record. They are never presumed equivalent.

## 6. Parallel Model Comparison Record

When two or more models address a related question, record:

- common question;
- each model’s Observation Frame;
- comparable variables;
- non-comparable variables;
- agreement;
- disagreement;
- scale mismatch;
- data-period mismatch;
- mechanism mismatch;
- uncertainty mismatch;
- possible reasons for divergence;
- unresolved questions;
- human synthesis.

A consensus value is not required. Unresolved disagreement may be the correct result.

## 7. Evidence classes

Each claim must be identified as one of:

- observation;
- authoritative derived data;
- external-model output;
- reproduced computation;
- statistical association;
- lagged predictive signal;
- engineering estimate;
- model inference;
- causal hypothesis;
- expert-confirmed mechanism;
- governance judgement.

One class must not silently transform into another.

## 8. Admission rules

An external-model output is eligible for ClimateOS reasoning only when:

- source identity and version are known;
- Observation Frame is present;
- relevant scale and variable semantics are known;
- provenance is traceable;
- uncertainty or its absence is explicit;
- omissions and limitations are recorded;
- any scale translation is declared;
- human responsibility is assigned.

Eligibility does not mean scientific truth, operational readiness or decision authority.

## 9. UniCM application

For UniCM, the first reading should focus on:

- global and basin-scale climate-mode representation;
- physical-field and mode-index inputs;
- information exchange between modes and fields;
- lead-lag and attention structures;
- reported forecast horizons and evaluation domains;
- absence or uncertainty around Australian drivers such as SAM and MJO;
- boundaries between global climate-mode skill and local environmental interpretation.

Dependency and environment analysis supports this reading but does not define its purpose.

## 10. Boundary

This protocol does not authorize installation, model execution, data acquisition, location claims, operational forecasts or policy decisions.
