# Task1541–1542 — External Model Observation Frame v0.1

Date: 2026-07-14

Status: COMPLETE / NON-EXECUTABLE SPECIFICATION

## 1. Governing principle

An external-model output is never admitted as a free-standing number.

It must remain attached to the computational world that produced it.

## 2. Required identity fields

| Field | Meaning |
|---|---|
| observation_frame_id | stable ClimateOS identifier |
| model_name | upstream model name |
| model_version | release, tag or semantic version |
| source_commit | immutable source identity |
| publication | authoritative scientific source |
| licence | declared code licence and boundary |
| output_identity | exact index, field, probability, scenario or estimate |
| evidence_class | observation, derived data, model output, reproduced computation or other governed class |

## 3. Observation coordinates

| Dimension | Required record |
|---|---|
| observer_position | where the model conceptually observes from |
| spatial_scale | planetary, basin/mode, continental, macroregional, locality/city, site/asset or declared alternative |
| spatial_support | grid, polygon, station, catchment, administrative area, asset or latent field |
| temporal_resolution | model time step |
| temporal_context | history or assimilation window |
| temporal_horizon | forecast, reconstruction or scenario horizon |
| data_period | period represented by training, calibration and evaluation data |
| variable_ontology | states, fields, indices and derived concepts |
| drivers | internal and external state-changing forces |
| mechanism_class | physical, statistical, learned, engineering, hybrid or unknown |
| boundary_conditions | externally supplied, fixed or excluded states |
| omitted_mechanisms | relevant processes not represented |
| uncertainty_form | ensemble, probability, interval, residual, scenario range, warning or none |
| validation_domain | evaluated regions, periods, data and metrics |
| human_responsibility | named review role and allowed decision class |

Unknown is an admissible value. Silent inference is not.

## 4. Cross-scale translation record

Every movement between scales requires:

- source frame and scale;
- target frame and scale;
- scientific reason;
- intermediate variables;
- aggregation, downscaling, inference or analogy method;
- calibration or comparison evidence;
- uncertainty before and after;
- omitted local and global mechanisms;
- non-stationarity warning;
- prohibited interpretations;
- human reviewer.

A global-to-site statement without intermediate bridges is ineligible.

## 5. Mechanism analogy record

A proposed analogy requires:

- compared entities;
- shared candidate mechanism;
- variables expressing the mechanism;
- evidence of similarity;
- evidence of difference;
- scale and time compatibility;
- confounders;
- transfer limits;
- expert-review status.

Names, national labels, climate labels and single metrics cannot establish equivalence.

## 6. Disagreement record

When models differ, ClimateOS records:

- common question;
- each Observation Frame;
- comparable and non-comparable variables;
- agreements;
- disagreements;
- scale, period, data, mechanism and uncertainty mismatches;
- unresolved explanations;
- human synthesis.

Disagreement must not be silently averaged away.

## 7. Admission states

| State | Meaning |
|---|---|
| IDENTIFIED | source and output identity known |
| FRAME_INCOMPLETE | one or more observation coordinates missing |
| FRAME_READY | observation coordinates documented |
| TRANSLATION_REQUIRED | target claim is at another scale |
| COMPARISON_ELIGIBLE | sufficiently aligned for bounded comparison |
| RESEARCH_ONLY | may inform research reasoning, not operations |
| OPERATIONALLY_BLOCKED | cannot support warnings or automated decisions |
| REJECTED | source, scale, provenance or governance failure |

## 8. Minimum admission rule

An output may enter ClimateOS research reasoning only when source identity, scale, variable semantics, provenance, uncertainty status, omissions and human responsibility are explicit.

This does not establish truth, causality, regional validity or operational readiness.
