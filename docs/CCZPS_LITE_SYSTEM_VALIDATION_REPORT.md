# CCZPS-Lite System Validation Report

## Validation Status

CCZPS-Lite is validated as a working concept-level, rule-based methodology demonstrator through Response Prioritisation Runtime (Task 12).

Validation basis:

- Repository: `simon947161/eco-agent-system`
- Baseline: `main` at commit `7e437a41369df11aa47408779de423ec302a1d1a`
- Task 12 final GitHub Actions run: `CCZPS-Lite Tests` run 63, successful
- Scenario generation: successful
- Python module compilation: successful
- Unit test discovery: 65 tests passed
- Generated output inspection: completed for the comparison matrix, scenario report, and governance summary

The GitHub-connected connector workspace does not expose a local Git checkout, so `git diff --check` could not be executed locally. This report is the only intended Task 13 change; runtime modules and generated outputs are unchanged.

## Current Runtime Chain

```text
Evidence Layer
    -> Runtime Fields
    -> Differential Field Runtime
    -> Forcing Layer Runtime
    -> Validation Layer Runtime
    -> Validation Feedback / Review Loop Runtime
    -> Adaptive Response Runtime
    -> Response Prioritisation Runtime
    -> CSV and Markdown governance outputs
```

The chain is orchestrated by `cczps_lite/engine/scenario_compare.py`. Each layer consumes local scenario, evidence, or context data and produces explicit fields for the next layer. The implementation remains deterministic and inspectable.

## Confirmed Modules

| Runtime layer | Module | Confirmed responsibility |
| --- | --- | --- |
| Evidence Layer | `cczps_lite/engine/evidence_layer.py` | Classifies evidence strength, source basis, uncertainty notes, and human-review need. |
| Runtime Fields | `cczps_lite/engine/runtime_fields.py` | Derives indicative risk, water, ecology, evaporation, confidence, and validation fields from scenario scores. |
| Differential Field Runtime | `cczps_lite/engine/differential_field.py` | Compares scenario scores with local representative context records and classifies gradients. |
| Forcing Layer Runtime | `cczps_lite/engine/forcing_layer.py` | Converts gradients into candidate environmental pressures and forcing priority. |
| Validation Layer Runtime | `cczps_lite/engine/validation_layer.py` | Produces an evidence-aware validation score, status, gaps, and cautious summary. |
| Validation Feedback / Review Loop Runtime | `cczps_lite/engine/review_loop.py` | Maps validation results to review action, priority, owner, triggers, and summary. |
| Adaptive Response Runtime | `cczps_lite/engine/adaptive_response.py` | Suggests candidate response options, response mode, and response priority. |
| Response Prioritisation Runtime | `cczps_lite/engine/response_prioritisation.py` | Selects one candidate response using implementation priority, urgency, and expected-benefit rules. |

Supporting orchestration, scoring, runtime reasoning, local JSON inputs, and reporting remain in place. No external runtime dependency is required.

## Confirmed Output Fields

The generated `comparison_matrix.csv` contains three scenario rows and the complete field chain.

### Identity and Scenario Scores

- `scenario_id`, `scenario_name`, `scenario_type`
- `water_security`, `energy_resilience`, `ecological_resilience`, `fire_resilience`
- `community_acceptance`, `investment_feasibility`, `implementation_complexity`, `validation_need`

### Runtime and Differential Fields

- `risk_index`, `water_balance_signal`, `ecological_signal`, `evaporation_pressure`
- `confidence_level`, `validation_required`, `runtime_reasoning`
- water, heat, vegetation, and fire gradient values and classes
- `differential_status`, `differential_summary`, `reference_record_count`

### Forcing and Evidence Fields

- `forcing_candidates`, `primary_forcing`, `forcing_priority`, `forcing_summary`
- `evidence_strength`, `source_basis`, `uncertainty_notes`, `human_review_required`

### Validation and Review Fields

- `validation_score`, `validation_status`, `validation_gaps`, `validation_summary`
- `review_action`, `review_priority`, `review_owner`, `review_triggers`, `review_summary`

### Response and Prioritisation Fields

- `response_priority`, `response_options`, `response_mode`, `response_summary`
- `implementation_priority`, `urgency_level`, `expected_benefit`
- `prioritised_response`, `prioritisation_summary`

### Scoring Fields

- `resilience_score`, `governance_score`, `risk_adjusted_score`, `recommendation_class`

List-valued CSV fields are serialized as semicolon-separated text. `prioritised_response` contains one candidate response.

## Generated Output Inspection

### Comparison Matrix

`cczps_lite/output/comparison_matrix.csv` is structurally complete and internally consistent for the three Batlow pathways:

- Water Priority proceeds to concept refinement at low implementation priority.
- Energy Resilience is held for evidence, with field evidence collection prioritised at high implementation priority.
- Ecology / Fire Buffer requires technical validation, with bushfire buffer review prioritised under Critical urgency.

### Scenario Report

`cczps_lite/output/scenario_report.md` includes per-scenario sections for every runtime layer, including:

- Validation Feedback / Review Loop
- Adaptive Response Runtime
- Response Prioritisation Runtime

The report consistently states that outputs are indicative, concept-level, locally reviewable, and not final professional advice.

### Governance Summary

`cczps_lite/output/governance_summary.md` includes aggregate readings for evidence, differential fields, forcing, validation, review, adaptive response, and response prioritisation. It identifies the highest-priority pathway and a suggested first implementation focus without claiming autonomous authority.

## Confirmed Test Coverage

The repository workflow performs:

1. `python cczps_lite/engine/scenario_compare.py`
2. JSON syntax validation for core inputs
3. Python compilation for engine and integration modules
4. `python -m unittest discover`

The final Task 12 validation run passed all 65 discovered tests. Coverage includes:

- evidence strength, source, uncertainty, and human-review rules
- runtime field derivation and scoring behavior
- differential gradient calculation and classification
- forcing candidates, priority, and cautious summaries
- validation scoring, status, domain gaps, and output fields
- review action, priority, owner routing, triggers, and report integration
- adaptive response modes, priorities, domain options, deduplication, and serialization
- response urgency, expected benefit, deterministic option ranking, and output integration
- end-to-end generation of CSV and Markdown outputs
- validity of local JSON inputs

This is meaningful rule and integration coverage. It is not evidence of scientific accuracy, field validity, performance at scale, or suitability for operational decisions.

## Current Methodology Boundary

CCZPS-Lite currently uses:

- local JSON inputs
- editable indicative scenario scores
- representative local context records
- transparent threshold and mapping rules
- deterministic Python functions
- generated CSV and Markdown outputs
- human-review language and governance routing

It does not use live environmental observations, remote sensing, GIS analysis, databases, machine learning, AI agents, world models, workflow automation, or external approval systems.

## What the System Can Do Now

CCZPS-Lite can:

- compare a small set of concept-level environmental resilience pathways
- expose the evidence basis and uncertainty attached to each pathway
- derive indicative environmental gradients against representative context records
- identify candidate forcing signals without claiming causality
- classify validation needs and identify unresolved evidence gaps
- route scenarios toward evidence, technical, local, or governance review
- suggest practical candidate response options
- prioritise one response for consideration using visible rules
- generate a reviewable comparison matrix, scenario report, and governance summary
- reproduce the same outputs from the same local inputs

## What the System Cannot Do Yet

CCZPS-Lite cannot:

- validate scientific assumptions against observed field data
- provide live weather, hydrology, fire, ecological, or infrastructure intelligence
- perform GIS, spatial, catchment, terrain, network, or asset analysis
- produce engineering calculations, construction designs, cost estimates, or schedules
- determine regulatory compliance or approval
- predict environmental outcomes or prove causal relationships
- optimise portfolios across budget, timing, dependencies, or competing objectives
- manage users, permissions, audit events, review assignments, or workflow state
- replace professional judgement, community consultation, or site-specific assessment

## Known Limitations

- Demonstrator scores and thresholds are manually defined and not calibrated against an external benchmark.
- The current validation scenarios are limited to three Batlow pathways.
- Representative context records are small, local files rather than validated datasets.
- Threshold boundaries may be sensitive to small score changes.
- Expected benefit is categorical, not quantified.
- Prioritisation is ordinal and does not model cost, feasibility, duration, dependencies, or adverse effects.
- Domain mappings are keyword and rule based; they do not cover every environmental condition or response type.
- Human-review routing identifies a reviewer category but does not create or track a real review task.
- Generated narrative quality is tested mainly through expected fields and headings, not formal document schemas.
- Current CI confirms deterministic execution and regression behavior, not scientific or policy validity.

## Recommended Next Development Direction

The next development phase should focus on validation and product hardening rather than adding another reasoning layer.

Recommended sequence:

1. Freeze and document the current rule vocabulary, thresholds, and field contracts.
2. Add fixture-based golden-output tests for representative water, heat, fire, ecology, and low-evidence cases.
3. Define a versioned input and output schema with explicit required fields, types, enumerations, and compatibility rules.
4. Conduct structured review with hydrology, microclimate, fire resilience, ecology, governance, and local stakeholders.
5. Record rule rationale, provenance, owner, review date, and change history.
6. Add broader scenario fixtures and boundary-value tests before considering operational integrations.

Live data or spatial integration should be considered only after the concept rules and validation criteria are accepted.

## Suggested v1.0 Readiness Checklist

### Methodology

- [ ] Rule thresholds have documented rationale and named domain reviewers.
- [ ] Terminology and statuses are stable and versioned.
- [ ] At least one independent technical review has been completed for each domain mapping.
- [ ] Known false-positive and false-negative cases are documented.
- [ ] The distinction between concept validation and scientific validation is explicit in all user-facing outputs.

### Data Contracts

- [ ] Input JSON schema is defined and automatically validated.
- [ ] Output CSV and report field contracts are versioned.
- [ ] Missing, malformed, extreme, and contradictory inputs have defined behavior.
- [ ] Units, scales, provenance, and update dates are explicit for every input.

### Testing

- [ ] Golden outputs cover all validation statuses, reviewer types, response modes, urgency levels, and benefit classes.
- [ ] Boundary-value tests cover every numeric threshold.
- [ ] End-to-end tests confirm outputs are deterministic and internally consistent.
- [ ] Generated files are checked for drift in CI.
- [ ] A clean Git diff check is included in CI or release validation.

### Governance and Safety

- [ ] Human approval points are documented for each review action.
- [ ] Disclaimers and methodology boundaries have legal and professional review.
- [ ] Rule changes require review, traceability, and release notes.
- [ ] No output is presented as final planning, engineering, construction, environmental, financial, or regulatory advice.

### Operational Readiness

- [ ] Release versioning and changelog policy are established.
- [ ] Reproducible installation and execution instructions are verified on supported environments.
- [ ] Failure handling and diagnostic messages are documented.
- [ ] Security, privacy, accessibility, and data-retention requirements are assessed before introducing user or external data.
- [ ] A pilot evaluation defines success criteria, feedback collection, and rollback conditions.

## Conclusion

The full CCZPS-Lite chain through Task 12 is coherent, executable, regression-tested, and appropriately cautious for a methodology demonstrator. It is ready for structured expert review, schema stabilization, broader fixtures, and pilot validation. It is not yet ready to support final environmental, planning, engineering, construction, investment, or regulatory decisions.
