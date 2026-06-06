# CCZPS-Lite Runtime Capability Map

## 1. System Overview

### Purpose

CCZPS-Lite is a transparent, rule-based methodology demonstrator for comparing concept-level environmental resilience and governance pathways. It converts local scenario scores, evidence descriptions, and representative context records into explicit runtime fields, candidate environmental pressures, validation readings, review routes, response options, and a prioritised response for human consideration.

### Scope

The current scope includes:

- local JSON scenario, evidence, and context inputs
- deterministic Python functions and visible threshold rules
- evidence and uncertainty classification
- indicative environmental differential readings
- candidate forcing identification
- concept-level validation and review routing
- candidate adaptive responses and response prioritisation
- CSV and Markdown reporting
- multi-scale scenario fixtures for Batlow, Kunlun, Iraq, and Baiyangdian-Xiong'an

### Current Prototype Status

CCZPS-Lite is a working concept-level prototype. The complete runtime chain is executable and regression-tested. It demonstrates consistent rule execution across the current scenario fixtures, but it has not been calibrated or scientifically validated against authoritative field datasets.

The system is suitable for methodology review, rule inspection, fixture-based testing, and structured governance discussion. It is not suitable for final environmental, engineering, planning, investment, construction, emergency, or regulatory decisions.

### Governance Philosophy

The runtime follows four principles:

1. **Transparency:** material classifications and thresholds are encoded in inspectable functions.
2. **Traceability:** each scenario row carries evidence, runtime, validation, review, response, and prioritisation fields.
3. **Caution:** outputs use candidate, indicative, concept-level, and review-oriented language.
4. **Human authority:** the runtime recommends review routes and candidate actions but does not approve, assign, or implement decisions.

### Limitations

CCZPS-Lite does not include live observations, external APIs, databases, GIS, remote sensing, physical simulation, forecasting, machine learning, autonomous agents, workflow execution, or approval tracking. Scores and representative records are manually supplied fixtures. Thresholds are demonstrator rules rather than calibrated scientific standards.

## 2. Runtime Architecture

### Evidence Layer

**Purpose:** Convert one or more evidence records into a conservative, standardised evidence reading.

**Inputs:** Scenario-linked evidence records containing strength and source descriptions.

**Outputs:** Evidence quality, provenance category, uncertainty language, and the low-evidence human-review flag.

**Key fields:**

- `evidence_strength`
- `source_basis`
- `uncertainty_notes`
- `human_review_required`

**Current logic boundary:** The weakest supplied evidence strength controls grouped evidence. The layer classifies metadata only; it does not authenticate sources or test evidence quality externally.

### Runtime Fields

**Purpose:** Derive compact operational signals from editable scenario scores.

**Inputs:** `water_security`, `ecological_resilience`, `fire_resilience`, and `validation_need` scores.

**Outputs:** Indicative risk, water balance, ecology, evaporation, confidence, and validation-need readings.

**Key fields:**

- `risk_index`
- `water_balance_signal`
- `ecological_signal`
- `evaporation_pressure`
- `confidence_level`
- `validation_required`
- `runtime_reasoning`

**Current logic boundary:** Values are threshold-based interpretations of scenario scores, not measurements, forecasts, or simulation results.

### Differential Field Runtime

**Purpose:** Compare scenario values with representative context records and expose relative gradients.

**Inputs:** Scenario scores and local context records for water security, heat exposure, vegetation condition, and fire exposure.

**Outputs:** Numeric gradients, threshold classes, a combined differential status, and a cautious summary.

**Key fields:**

- `water_gradient`, `water_gradient_class`
- `heat_gradient`, `heat_gradient_class`
- `vegetation_gradient`, `vegetation_gradient_class`
- `fire_gradient`, `fire_gradient_class`
- `differential_status`
- `differential_summary`
- `reference_record_count`

**Current logic boundary:** Gradients are relative to small representative fixtures. They are not validated field measurements and do not model spatial or temporal processes.

### Forcing Layer Runtime

**Purpose:** Translate differential classes into candidate environmental pressures or protective influences.

**Inputs:** Differential gradient classes and differential status.

**Outputs:** Candidate forcings, one primary forcing, forcing priority, and explanatory text.

**Key fields:**

- `forcing_candidates`
- `primary_forcing`
- `forcing_priority`
- `forcing_summary`

**Current logic boundary:** Forcings are rule-based candidates such as Water Storage Deficit, Heat Exposure, Evaporation Pressure, Vegetation Stress, Fire Exposure, and Microclimate Buffer Support. They do not prove causality.

### Validation Layer Runtime

**Purpose:** Combine evidence quality, runtime confidence, validation need, human-review need, and forcing priority into a concept-level validation reading.

**Inputs:** Runtime fields, differential results, forcing results, and evidence results.

**Outputs:** A bounded score, governance status, domain validation gaps, and a cautious explanation.

**Key fields:**

- `validation_score`
- `validation_status`
- `validation_gaps`
- `validation_summary`

**Status vocabulary:**

- `Insufficient Evidence`
- `Requires Technical Validation`
- `Requires Local Validation`
- `Validated Enough for Concept Review`

**Current logic boundary:** "Validated Enough" means only that a pathway may advance to concept review. It is not scientific, engineering, regulatory, or implementation validation.

### Validation Feedback Loop

**Purpose:** Convert validation results into an explicit next-review route.

**Inputs:** Validation status, validation score, validation gaps, evidence result, and primary forcing.

**Outputs:** Review action, priority, reviewer category, triggers, and summary.

**Key fields:**

- `review_action`
- `review_priority`
- `review_owner`
- `review_triggers`
- `review_summary`

**Current routes:**

- hold and collect evidence
- escalate to technical review
- send to local review
- proceed to concept review

**Current logic boundary:** Reviewer categories are recommendations only. The runtime does not create tasks, notify reviewers, store feedback, or track workflow state.

### Adaptive Response Runtime

**Purpose:** Translate validation gaps and review signals into ordered candidate response options.

**Inputs:** Validation result, review result, forcing result, and evidence result.

**Outputs:** Response priority, response mode, candidate options, and a cautious summary.

**Key fields:**

- `response_priority`
- `response_options`
- `response_mode`
- `response_summary`

**Current response modes:**

- evidence-building response
- technical validation response
- local consultation response
- concept refinement response

**Current logic boundary:** Options are rule-mapped suggestions. They are not designs, instructions, approvals, schedules, budgets, or autonomous actions.

### Response Prioritisation Runtime

**Purpose:** Select one candidate response for first consideration using visible priority, urgency, and expected-benefit rules.

**Inputs:** Adaptive response results, validation status, forcing priority, and primary forcing.

**Outputs:** Implementation priority, urgency, expected benefit, one prioritised response, and an explanation.

**Key fields:**

- `implementation_priority`
- `urgency_level`
- `expected_benefit`
- `prioritised_response`
- `prioritisation_summary`

**Current logic boundary:** Ranking is categorical and ordinal. It does not optimise cost, duration, dependencies, resource availability, trade-offs, adverse effects, or portfolio value.

## 3. Runtime Flow Diagram

```text
Local JSON Input
  - scenario scores
  - evidence records
  - representative context records
  - validation fixture metadata
        |
        v
Evidence Layer
  evidence strength, source basis, uncertainty, human-review flag
        |
        v
Runtime Fields
  risk, water, ecology, evaporation, confidence, validation need
        |
        v
Differential Field Runtime
  water, heat, vegetation, and fire gradients
        |
        v
Forcing Layer Runtime
  candidate pressures, primary forcing, forcing priority
        |
        v
Validation Layer Runtime
  validation score, status, gaps, summary
        |
        v
Validation Feedback Loop
  review action, priority, owner, triggers
        |
        v
Adaptive Response Runtime
  response mode, priority, candidate response options
        |
        v
Response Prioritisation Runtime
  implementation priority, urgency, benefit, first response
        |
        v
Outputs
  comparison matrix
  scenario report
  governance summary
  system validation report
  scenario validation pack
  runtime capability map
```

The system validation report and runtime capability map document the runtime; they are not additional decision layers.

## 4. Output Capability Matrix

| Output | Purpose | Intended audience | Primary content | Limitations |
| --- | --- | --- | --- | --- |
| `comparison_matrix.csv` | Provide one structured row per baseline or validation scenario with the complete field chain. | Developers, analysts, reviewers, and test maintainers. | Scenario identity and context; scores; evidence; runtime; gradients; forcing; validation; review; response; prioritisation; aggregate scoring. | Flat-file snapshot; list fields use semicolon-separated text; no schema enforcement, provenance ledger, database history, or approval state. |
| `scenario_report.md` | Explain baseline pathways and multi-scale validation contexts in readable form. | Governance reviewers, domain specialists, local stakeholders, and methodology reviewers. | Per-scenario runtime readings, validation, review route, responses, prioritisation, limitations, and watershed continuity section. | Generated narrative follows templates and current fixtures; it is not professional advice or a substitute for local assessment. |
| `governance_summary.md` | Aggregate scenario readings into a concise governance-oriented overview. | Governance leads, project sponsors, and review coordinators. | Highest-priority pathways, common review or response signals, suggested first focus, multi-scale validation reading. | Uses simple aggregation and categorical ranking; no deliberation record, approval workflow, or stakeholder weighting. |
| `system_validation_report.md` | Describe end-to-end system validation, methodology boundaries, test coverage, limitations, and readiness. | Maintainers, reviewers, auditors, and release decision-makers. | Runtime chain, confirmed modules and fields, test coverage, capability boundary, known limitations, and v1.0 checklist. | The current canonical artifact is manually maintained at `docs/CCZPS_LITE_SYSTEM_VALIDATION_REPORT.md`; it is not generated by `scenario_compare.py` and may require periodic reconciliation with later tasks. |
| `scenario_validation_pack.md` | Demonstrate runtime consistency across multiple geographic and governance contexts. | Domain reviewers, governance teams, and prototype evaluators. | Batlow, Kunlun, Iraq, and three Baiyangdian-Xiong'an records; assumptions; outputs; review requirements; limitations; watershed continuity reading. | Fixtures are illustrative, not authoritative local datasets. Cross-context execution does not establish scientific transferability or outcome accuracy. |
| `runtime_capability_map.md` | Provide the current architecture, data flow, field inventory, scenario coverage, capability assessment, and readiness map. | Maintainers, technical reviewers, governance reviewers, and prospective pilot teams. | Layer-by-layer architecture, text flow diagram, output matrix, scenario map, gaps, and readiness checklist. | Documentation snapshot only; it adds no runtime behavior and must be updated when field contracts or scenarios change. |

## 5. Scenario Coverage

### Batlow

**Purpose:** Compare local and regional resilience pathways for water security, energy continuity, ecological recovery, fire buffering, and agricultural continuity.

**Scale:** Local town, orchard landscape, and regional agricultural continuity context in New South Wales, Australia.

**Primary risks:** Drought, heat, evaporation pressure, bushfire exposure, water security, emergency energy continuity, and vegetation condition.

**Runtime applicability:** Exercises all runtime layers through three baseline pathways and the Batlow Energy Resilience validation record. It demonstrates concept-review progression, evidence hold, and technical-review routing.

### Kunlun

**Purpose:** Test dryland ecological governance and adaptation under constrained water availability.

**Scale:** Regional dryland ecological system.

**Primary risks:** Drought pressure, water-storage deficit, evaporation pressure, ecological degradation, and climate adaptation uncertainty.

**Runtime applicability:** Exercises high-priority water forcing, low-evidence validation, hydrology review routing, and prioritisation of a water storage audit.

### Iraq

**Purpose:** Test concept-level environmental and agricultural recovery pathways.

**Scale:** Regional agricultural landscape.

**Primary risks:** Desertification, irrigation-system condition, low water security, agricultural productivity constraints, ecological restoration needs, and high implementation complexity.

**Runtime applicability:** Exercises insufficient-evidence handling, high-priority hydrological review, critical urgency, and evidence-aware response prioritisation.

### Baiyangdian-Xiong'an

**Purpose:** Test watershed-scale ecological continuity from mountain source through wetland storage to downstream urban consumption.

**Scale:** Three linked validation points: Wutai Mountain headwaters, Baiyangdian wetland core, and Xiong'an/downstream urban region.

**Primary risks:** Rainfall and runoff uncertainty, forest retention, watershed protection, wetland persistence, evaporation pressure, water balance, urban demand, flood resilience, ecological connectivity, and long-term sustainability.

**Runtime applicability:** Exercises the existing runtime chain at headwater, wetland, and downstream scales. It also produces a diagnostic Watershed Continuity Reading of High, Moderate, or Fragmented Continuity from relative water-security, ecological-resilience, and evidence bands.

The continuity reading is not a runtime layer or predictive model. River transport is represented as a diagnostic connection only; no hydrological routing, allocation, flood, or demand forecast is performed.

## 6. Capability Assessment

### Current Strengths

- Complete deterministic chain from evidence to prioritised response.
- Explicit fields make intermediate reasoning visible and testable.
- Conservative evidence handling carries uncertainty into validation and review.
- Domain-oriented review routing covers water, microclimate, fire, ecology, evidence, and governance.
- Generated CSV and Markdown outputs support technical and non-technical inspection.
- Multi-scale fixtures exercise contrasting geographic, ecological, and governance contexts.
- The same local inputs produce reproducible outputs.
- No external dependency is required for the current runtime.

### Current Limitations

- Inputs are illustrative scores and representative records rather than validated observations.
- Thresholds and category mappings are not externally calibrated.
- Differential readings do not model geography, time, seasonality, uncertainty distributions, or physical processes.
- Candidate forcing labels do not establish causality.
- Response ranking does not model cost, feasibility, duration, dependencies, benefits distribution, or adverse effects.
- Human review is recommended but not assigned, recorded, or closed within the system.
- Generated narratives and CSV fields do not yet have versioned formal schemas.
- The system validation report predates the multi-scale pack and needs reconciliation during a future documentation refresh.

### Known Gaps

- Versioned input and output contracts.
- Rule provenance, rationale, ownership, and change history.
- Golden-output drift checks for all generated artifacts.
- Boundary tests for every numeric threshold and category transition.
- Independent domain review of water, microclimate, fire, ecology, evidence, and governance mappings.
- Authoritative field datasets and agreed validation criteria.
- Formal review records and auditability, if later required.
- Cost, resource, dependency, trade-off, and adverse-impact assessment.
- Accessibility and usability review of generated reports.

### Recommended Future Directions

1. Freeze and version the current vocabulary, fields, thresholds, and report contracts.
2. Reconcile the system validation report with the multi-scale scenario pack and this capability map.
3. Add schema validation and golden-output drift checks without changing runtime meaning.
4. Expand boundary and malformed-input tests.
5. Conduct structured reviews with relevant domain specialists and local stakeholders.
6. Record rule rationale, provenance, reviewer, approval date, and revision history.
7. Define pilot success criteria before considering live-data, spatial, workflow, or forecasting integrations.

Future development should strengthen validation, traceability, and product reliability before adding new reasoning capability.

## 7. CCZPS-Lite v1.0 Readiness

### Architecture

- [x] Runtime layers have distinct modules and responsibilities.
- [x] The end-to-end rule chain is deterministic and inspectable.
- [x] Scenario generation is orchestrated from a single entry point.
- [ ] Input and output contracts are formally versioned.
- [ ] Error handling for malformed, missing, extreme, and contradictory data is specified.

### Testing

- [x] Unit and end-to-end regression tests cover the current runtime chain.
- [x] Multi-scale fixtures exercise all current layers.
- [x] Watershed continuity bands have regression coverage.
- [ ] Every numeric boundary and category transition has explicit tests.
- [ ] CI checks generated artifacts for unexpected drift.
- [ ] Release validation includes a clean diff and supported-environment matrix.

### Transparency

- [x] Key runtime fields and narrative summaries are exposed.
- [x] Candidate forcings and response options are distinguishable from facts.
- [x] Methodology boundaries appear in user-facing documents.
- [ ] Every rule has documented rationale, provenance, owner, and review date.
- [ ] Field definitions, types, units, and enumerations have a published data dictionary.

### Governance

- [x] Low evidence can require human review.
- [x] Validation outcomes map to explicit review actions and reviewer categories.
- [x] Outputs preserve human authority and cautious language.
- [ ] Human approval points and escalation responsibilities are formally documented.
- [ ] Rule changes require traceable review and release notes.
- [ ] Disclaimers and governance language have professional review.

### Validation

- [x] The complete runtime executes consistently against current fixtures.
- [x] Validation statuses, gaps, review routes, and response priorities are tested.
- [ ] Thresholds and mappings have independent domain review.
- [ ] Performance is assessed against agreed reference cases or field evidence.
- [ ] False-positive, false-negative, and ambiguous cases are documented.
- [ ] Concept validation and scientific validation criteria are formally separated.

### Scenario Coverage

- [x] Batlow water, energy, ecology, and fire pathways are represented.
- [x] Kunlun dryland ecological governance is represented.
- [x] Iraq agricultural recovery is represented.
- [x] Baiyangdian-Xiong'an headwater, wetland, and downstream points are represented.
- [ ] Additional boundary, counterexample, and contradictory-evidence fixtures are defined.
- [ ] Local experts and stakeholders review assumptions for each named geography.

### Documentation

- [x] A system validation report exists.
- [x] A multi-scale scenario validation pack exists.
- [x] This runtime capability map documents the current architecture and boundaries.
- [ ] Documentation versions are tied to runtime releases.
- [ ] The system validation report is updated for the multi-scale runtime state.
- [ ] Installation, execution, troubleshooting, and release procedures are verified.

## Readiness Summary

CCZPS-Lite has a coherent and testable architecture for a transparent concept-level methodology demonstrator. The main v1.0 work is not another runtime layer. It is contract stabilisation, comprehensive boundary testing, rule provenance, independent domain validation, documentation reconciliation, and formal governance review.
