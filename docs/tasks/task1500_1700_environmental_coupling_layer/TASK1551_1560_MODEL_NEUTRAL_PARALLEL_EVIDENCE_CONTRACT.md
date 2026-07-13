# Task1551–1560 — Model-Neutral Parallel Evidence Contract and Environmental Coupling Question Gate

Date: 2026-07-14

Status: DOCUMENTATION_COMPLETE / NON-EXECUTABLE / NO_MODEL_OR_DATA_ACCESS

## 1. Purpose

Task1551–1560 defines how bounded readings from different external model worlds
may later enter ClimateOS as evidence candidates without becoming automatic
truth, without being merged into one model, and without jumping from global
scale to local environmental conclusions.

This task returns the parallel-model research to the main Environmental
Coupling Layer workstream.

## 2. Roadmap realignment

The earlier Task1500–1700 roadmap reserved Task1551–1600 for a minimal UniCM
reproduction. Current Founder direction and the Multiscale Parallel Model
Perspective change the order of work:

```text
Old protected idea
UniCM source -> UniCM reproduction -> adapter -> coupling

Current governed sequence
Multiple model sources
-> model-neutral registry
-> model-neutral evidence contract
-> scale and comparison gate
-> later acquisition or execution decision
-> later adapters and coupling
```

This realignment does not reject future reproduction. It prevents reproduction
of one model from becoming the architecture of ClimateOS by default.

## 3. Inputs

Task1551–1560 uses only completed documentation:

- ClimateOS Parallel Model Registry Draft v0.1;
- NeuralGCM Source-and-Observation Research Pack;
- UniCM x NeuralGCM Multiscale Comparison Report;
- Multiscale Parallel Model Perspective CRP;
- existing External Scientific Model Reuse and Adapter Policy;
- existing Cross-Domain Evidence Contract concepts;
- existing Task1500–1700 Environmental Coupling Layer roadmap;
- current Parallel Model and Scientific Resource Discovery ACTP.

No model output is an input to this task.

## 4. Architecture position

```text
External model world
    |
    v
Model Registry Record
    |
    v
Parallel Model Evidence Candidate
    |
    +---- scale boundary
    +---- mechanism status
    +---- variable contract
    +---- forcing provenance
    +---- evaluation status
    +---- prohibited inference
    |
    v
Parallel Comparison Record
    |
    v
Environmental Coupling Question
    |
    v
Regional evidence + human scientific review
```

An adapter may later translate a model-specific output into this contract. The
contract itself does not call or run a model.

## 5. Core distinction

| Object | Meaning | Authority boundary |
|---|---|---|
| Model output | A value or field produced by a named model configuration | Not automatically evidence or truth |
| Evidence candidate | A model output or published claim with provenance and limitations | Eligible for review only |
| Reviewed evidence | Candidate assessed under a declared evaluation and human-review protocol | Valid only for the reviewed claim class |
| Coupling question | A bounded question about a possible cross-system relationship | Not a causal conclusion |
| Causal hypothesis | A mechanism proposition requiring later experimental or observational testing | Not established mechanism |
| Governance interpretation | Human-reviewed use of evidence within a declared decision boundary | Not automated by this contract |

## 6. Parallel Model Evidence Contract v0.1

The canonical documentation form is:

```yaml
parallel_model_evidence:
  evidence_id:
  record_version: "0.1"

  model_identity:
    model_record_id:
    model_name:
    record_level: [family, release, checkpoint, service_product, configuration]
    source_revision:
    checkpoint_or_product:
    provider:

  claim:
    claim_type: [published_claim, model_output, diagnostic, comparison_result]
    claim_text:
    claim_unit: [mode_index, field, tendency, event, statistic, impact_hypothesis]
    evidence_status:

  scale:
    geographic_domain:
    spatial_support:
    native_resolution:
    common_comparison_resolution:
    vertical_support:
    input_cadence:
    output_cadence:
    horizon:
    aggregation:
    scale_transfer_prohibition:

  mechanism:
    mechanism_class:
    explicit_component:
    learned_component:
    diagnostic_component:
    external_forcing_component:
    causal_status: [physical_constraint, learned_association, diagnostic, hypothesis, unknown]
    interpretation_boundary:

  variables:
    - canonical_name:
      source_name:
      role:
      unit:
      spatial_support:
      temporal_support:
      transformation:
      evidence_status:

  initialization_and_forcing:
    initial_state_resource_id:
    forcing_resource_ids: []
    forcing_scenario:
    preprocessing_revision:
    forcing_uncertainty:
    dynamically_simulated_components: []
    externally_prescribed_components: []

  evaluation:
    framework_ids: []
    reference_resource_ids: []
    baseline_ids: []
    metrics: []
    held_out_period:
    regridding_and_alignment:
    result_status:
    limitations: []

  regional_applicability:
    region_id:
    claim_class:
    native_coverage:
    local_validation_status:
    regional_anchor_ids: []
    missing_processes: []
    translation_method:
    required_human_review:

  uncertainty:
    deterministic_or_stochastic:
    ensemble_definition:
    represented_uncertainty:
    omitted_uncertainty:

  governance:
    allowed_use:
    prohibited_inferences: []
    acquisition_state:
    execution_state:
    cost_state:
    human_review_state:
    founder_gate_state:

  provenance:
    source_references: []
    created_at:
    created_by:
    reviewed_at:
    reviewed_by:
    disputes: []
```

## 7. Required-field rules

An evidence candidate is `BLOCKED` when any of these are missing:

- exact model record and record level;
- claim type and claim unit;
- source revision or explicit `UNVERIFIED` state;
- spatial and temporal support;
- variable role and unit;
- forcing and initialization boundary;
- mechanism and causal status;
- evaluation status;
- regional-use boundary;
- prohibited inferences;
- human and Founder gate state.

`BLOCKED` means incomplete for the proposed use. It does not mean the model is
scientifically worthless.

## 8. Scale Translation Gate

Every proposed translation must declare a source and target level.

| Level | Example | Direct translation status |
|---|---|---|
| L0 Planetary mode | ENSO or IOD state | May inform global-driver questions only |
| L1 Global atmospheric field | Pressure, wind, moisture or temperature field | May inform large-scale weather questions only |
| L2 Continental | Broad Australian circulation or climate regime | Requires Australian authoritative anchor |
| L3 Regional | NSW, inland Australia, coastal region or catchment | Requires regional model/observation validation |
| L4 Local | Sydney, Alice Springs, Snowy Valleys or Riverina locality | Requires location-specific evidence and translation |
| L5 Site and impact | Property, infrastructure, ecosystem or project decision | Requires domain evidence and qualified review |

Rules:

1. L0 or L1 cannot become L3–L5 evidence by geographic inclusion alone.
2. Every downward scale transition requires an explicit method and validation.
3. Multiple transitions require uncertainty propagation at each step.
4. A finer grid does not guarantee a more truthful local result.
5. Downscaling or super-resolution output is not an observation.
6. Regional agreement does not establish site-level impact causation.

## 9. Mechanism Status Gate

| Status | Meaning | Permitted wording |
|---|---|---|
| `PHYSICAL_CONSTRAINT` | Equation or conservation/balance structure is explicitly represented | “The model constrains or advances…” |
| `LEARNED_TENDENCY` | Learned component estimates a state tendency | “The model learns a tendency representation…” |
| `LEARNED_ASSOCIATION` | Statistical or attention relationship is learned | “The model associates…” |
| `DIAGNOSTIC` | Quantity is derived from states or outputs | “The diagnostic indicates…” |
| `OBSERVED_ASSOCIATION` | Relationship is estimated from governed observations | “The observations are associated under…” |
| `CAUSAL_HYPOTHESIS` | Proposed mechanism has not been established | “The candidate hypothesis is…” |
| `EXPERIMENTALLY_SUPPORTED` | Later controlled evidence supports the declared mechanism | Reserved for a separately reviewed experiment |
| `UNKNOWN` | Mechanism status is unresolved | No mechanism claim permitted |

Attention, saliency, learned embedding and forecast success cannot be promoted
to `EXPERIMENTALLY_SUPPORTED`.

## 10. Comparison and divergence gate

A comparison must produce one of five outcomes:

- `CONSISTENT`;
- `PARTIALLY_CONSISTENT`;
- `DIVERGENT`;
- `INCOMPARABLE`;
- `UNRESOLVED`.

It must also identify one or more divergence types:

- state-space divergence;
- scale divergence;
- mechanism divergence;
- forcing divergence;
- evaluation divergence;
- regional divergence;
- uncertainty divergence.

No outcome authorizes averaging. Incomparability is a valid scientific record.

## 11. Environmental Coupling Question Record v0.1

```yaml
environmental_coupling_question:
  question_id:
  question_text:
  status: [candidate, source_supported, comparison_ready, regionally_reviewed, deferred]

  source_evidence_ids: []
  source_system:
  target_system:
  proposed_relationship_type: [observed_association, lagged_signal, model_inference, causal_hypothesis]

  source_scale:
  target_scale:
  lead_lag_window:
  geography:
  time_period:

  mechanism_status:
  stationarity_warning:
  uncertainty_chain: []
  missing_variables: []
  alternative_explanations: []

  evaluation_requirements: []
  regional_anchor_ids: []
  human_review_roles: []
  prohibited_conclusions: []
  future_experiment_gate:
```

The record stores a question, not an answer.

## 12. Non-executable UniCM x NeuralGCM example

```yaml
environmental_coupling_question:
  question_id: ECQ-UNICM-NGCM-001
  question_text: >
    Does an ENSO- or IOD-related state represented in the UniCM model world
    correspond to a compatible large-scale atmospheric circulation pattern in
    a separately initialized and forced NeuralGCM model world?
  status: candidate

  source_evidence_ids:
    - model.unicm.family.v1
    - model.neuralgcm.family.v1
  source_system: coupled_climate_modes_and_ocean_state
  target_system: global_atmosphere
  proposed_relationship_type: model_inference

  source_scale: L0_planetary_mode
  target_scale: L1_global_atmospheric_field
  lead_lag_window: UNVERIFIED
  geography: global_with_australian_context_not_local_claim
  time_period: UNVERIFIED

  mechanism_status: causal_hypothesis
  stationarity_warning: required
  uncertainty_chain:
    - UniCM mode and source-data uncertainty
    - SST and sea-ice forcing uncertainty
    - NeuralGCM initialization and checkpoint uncertainty
    - temporal and spatial alignment uncertainty
  missing_variables:
    - exact cross-model forcing crosswalk
    - SAM and MJO treatment for Australian interpretation
    - regional observation anchors
  alternative_explanations:
    - different averaging windows
    - different state variables
    - forcing mismatch
    - internal atmospheric variability

  evaluation_requirements:
    - pinned model configurations
    - common period and variable crosswalk
    - independent evaluation protocol
  regional_anchor_ids:
    - bom.access.products.candidate
  human_review_roles:
    - climate_mode_scientist
    - atmospheric_dynamicist
    - australian_regional_climatologist
  prohibited_conclusions:
    - no causal proof
    - no Australian local forecast
    - no flood, fire, water or ecosystem prediction
    - no operational warning
  future_experiment_gate: separate_founder_authorization_required
```

This example does not contain a result and cannot be executed.

## 13. Adapter boundary

A future model adapter may:

- read a separately authorized stored output;
- map model-specific fields to canonical variable records;
- attach exact model, checkpoint, data and transformation provenance;
- state scale, uncertainty and prohibited use;
- produce a Parallel Model Evidence Candidate.

An adapter may not:

- download or run the model unless separately authorized;
- change model output silently;
- invent missing units or uncertainty;
- convert a model result into observed evidence;
- select a preferred model automatically;
- make regional or causal conclusions;
- bypass the evaluation, human-review or Founder gates.

## 14. Australian regional anchor rule

For Australian use, an evidence candidate must identify the exact role of:

- Bureau of Meteorology climate-driver information;
- ACCESS or other official model products;
- stations, radar, satellite or reanalysis;
- regional and local topography;
- land, water, vegetation, fire or infrastructure evidence;
- statistical or physical translation;
- qualified Australian review.

ACCESS may be both a model-family record and an official product/data-resource
record. Those objects must remain separate.

## 15. Prohibited conclusions

Task1551–1560 permanently prohibits this contract from being used to claim:

- that UniCM, NeuralGCM or another model is the ClimateOS truth model;
- that agreement proves causation;
- that disagreement should be averaged away;
- that a global cell is a local observation;
- that a benchmark establishes all-purpose superiority;
- that historical skill guarantees future-climate validity;
- that a climate mode predicts a local impact directly;
- that a model output is an official forecast or warning;
- that an AI-generated interpretation is scientific sign-off;
- that completion of this task authorizes acquisition, execution or Task1561+.

## 16. Verification result

| Requirement | Result |
|---|---|
| Model-neutral evidence structure | COMPLETE |
| Identity and provenance boundary | COMPLETE |
| Scale Translation Gate | COMPLETE |
| Mechanism Status Gate | COMPLETE |
| Variable, initialization and forcing fields | COMPLETE |
| Evaluation and divergence fields | COMPLETE |
| Regional applicability and anchor rule | COMPLETE |
| Prohibited-inference rule | COMPLETE |
| Human scientific responsibility | COMPLETE |
| Non-executable UniCM x NeuralGCM example | COMPLETE |
| Model, weight or data acquisition | NOT PERFORMED |
| Model execution or reproduction | NOT PERFORMED |
| GraphCast active research | NOT STARTED |

## 17. Task1551–1560 decision

The model-neutral Parallel Model Evidence Contract and Environmental Coupling
Question Gate are ready for Founder review as documentation foundations.

The old default move from source acquisition directly to UniCM reproduction is
superseded as the immediate next action. Any future reproduction remains a
candidate experiment behind the registry, evidence, security, cost and Founder
gates.

Task1561 and later work do not start automatically.
