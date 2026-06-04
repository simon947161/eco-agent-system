# CODEX TASK 07 — DIFFERENTIAL FIELD RUNTIME

## EcoEngine V2 Runtime Core: Representative Differentials for CCZPS-Lite

Author: Simon Shu (Min Shu) + AI Dialogue System  
Repository: simon947161/eco-agent-system  
Task Type: Runtime Method Implementation  
Priority: High  
Status: Ready for Codex

---

## 1. Objective

Implement the first lightweight **Differential Field Runtime** for CCZPS-Lite.

The purpose is to move the current prototype from simple scenario labels toward EcoEngine-style environmental field reasoning.

Current system:

```text
Scenario Scores
    ↓
Runtime Fields
    ↓
Runtime Reasoning
    ↓
Governance Output
```

Task 07 adds:

```text
Representative Context
    ↓
Differential Field Runtime
    ↓
Gradient Signals
    ↓
Runtime Interpretation
```

This task should not implement Forcing Layer Runtime yet.

This task should not implement Validation Layer Runtime yet.

Task 07 only detects and summarizes differentials.

---

## 2. Architecture Context

The conceptual method is defined in:

```text
docs/03_RUNTIME_LAYER/DIFFERENTIAL_FIELD_INFERENCE.md
```

Core principle:

```text
A point is never interpreted alone.
A field can be inferred through representative differentials.
```

In practical terms, CCZPS-Lite should begin comparing a scenario or site against representative context records.

The first implementation should be small, transparent, and fully testable.

---

## 3. Current Stable Baseline

Current stable system includes:

```text
cczps_lite/input/location_profile.json
cczps_lite/input/scenario_options.json
cczps_lite/input/evidence_profile.json
cczps_lite/input/ecoengine_sample_output.json
cczps_lite/engine/scenario_compare.py
cczps_lite/integration/ecoengine_v192b_adapter.py
tests/test_cczps_lite.py
tests/test_ecoengine_v192b_bridge.py
.github/workflows/cczps-lite-tests.yml
```

GitHub Actions currently runs:

```bash
python cczps_lite/engine/scenario_compare.py
python -m unittest discover
```

Task 07 must preserve the green workflow.

---

## 4. Required New Input File

Create:

```text
cczps_lite/input/differential_context.json
```

This file should contain a small representative context set for Batlow.

Example structure:

```json
{
  "location_id": "batlow_nsw_001",
  "context_type": "representative_differential_sample",
  "records": [
    {
      "record_id": "batlow_orchard_reference",
      "label": "Orchard reference area",
      "terrain_position": "mid_slope",
      "water_security": 7,
      "heat_exposure": 6,
      "vegetation_condition": 7,
      "fire_exposure": 6,
      "evidence_strength": "Medium"
    },
    {
      "record_id": "batlow_dry_exposed_edge",
      "label": "Dry exposed edge",
      "terrain_position": "ridge_edge",
      "water_security": 4,
      "heat_exposure": 8,
      "vegetation_condition": 5,
      "fire_exposure": 8,
      "evidence_strength": "Low"
    },
    {
      "record_id": "batlow_valley_buffer",
      "label": "Valley buffer area",
      "terrain_position": "valley_floor",
      "water_security": 8,
      "heat_exposure": 5,
      "vegetation_condition": 8,
      "fire_exposure": 5,
      "evidence_strength": "Medium"
    }
  ],
  "notes": "Indicative representative differential context for CCZPS-Lite testing only."
}
```

These values are indicative.

Do not claim they are validated field measurements.

---

## 5. Required New Module

Create:

```text
cczps_lite/engine/differential_field.py
```

Required functions:

```python
def load_differential_context(path):
    pass


def calculate_gradient(target_value, reference_value):
    pass


def classify_gradient(value):
    pass


def derive_differential_field(scenario_scores, context_records):
    pass


def summarize_differential_field(differential_result):
    pass
```

Use Python standard library only.

---

## 6. Differential Logic

### 6.1 Target

For each scenario, use its existing scores as the target condition:

```text
water_security
ecological_resilience
fire_resilience
```

For heat exposure, derive a simple proxy:

```text
heat_exposure = 10 - water_security
```

This is only an indicative proxy.

Do not treat it as physical modelling.

---

### 6.2 Reference Context

Compare the scenario target against the average of the representative context records.

Fields to compare:

```text
water_security
heat_exposure
vegetation_condition
time-independent fire_exposure
```

Mapping:

```text
scenario.water_security -> context.water_security
scenario.ecological_resilience -> context.vegetation_condition
scenario.fire_resilience -> context.fire_exposure
scenario heat proxy -> context.heat_exposure
```

---

### 6.3 Gradient Calculation

Use:

```text
gradient = target_value - reference_average
```

Positive gradient means target is higher than reference.

Negative gradient means target is lower than reference.

---

### 6.4 Gradient Classification

Suggested classes:

```text
strong_positive
moderate_positive
neutral
moderate_negative
strong_negative
```

Suggested thresholds:

```text
>= 2.0       strong_positive
>= 0.75      moderate_positive
> -0.75      neutral
> -2.0       moderate_negative
<= -2.0      strong_negative
```

---

## 7. Differential Output Fields

`derive_differential_field()` should return a dictionary such as:

```json
{
  "water_gradient": 1.5,
  "water_gradient_class": "moderate_positive",
  "heat_gradient": -1.2,
  "heat_gradient_class": "moderate_negative",
  "vegetation_gradient": 0.3,
  "vegetation_gradient_class": "neutral",
  "fire_gradient": -0.4,
  "fire_gradient_class": "neutral",
  "differential_status": "water_advantage_with_heat_relief",
  "reference_record_count": 3
}
```

---

## 8. Differential Status

Create a simple `differential_status` label.

Suggested rules:

```text
if water_gradient_class is positive and heat_gradient_class is negative:
    water_advantage_with_heat_relief

if water_gradient_class is negative and heat_gradient_class is positive:
    water_stress_with_heat_pressure

if vegetation_gradient_class is positive and fire_gradient_class is negative:
    vegetation_buffer_advantage

if fire_gradient_class is positive:
    elevated_fire_exposure

otherwise:
    mixed_or_neutral_differential
```

Keep the logic simple and explainable.

---

## 9. Differential Summary

`summarize_differential_field()` should produce one short sentence.

Example:

```text
Differential field indicates moderate water advantage with reduced heat pressure compared with representative Batlow context.
```

Use cautious wording.

Do not claim validated measurement.

---

## 10. Integrate with Scenario Compare

Update:

```text
cczps_lite/engine/scenario_compare.py
```

Add loading of:

```text
cczps_lite/input/differential_context.json
```

For each scenario row, add:

```text
water_gradient
water_gradient_class
heat_gradient
heat_gradient_class
vegetation_gradient
vegetation_gradient_class
fire_gradient
fire_gradient_class
differential_status
differential_summary
reference_record_count
```

Add these columns to `comparison_matrix.csv`.

Add a short section to each scenario in `scenario_report.md`:

```text
### Differential Field Runtime

- Differential status: ...
- Water gradient: ...
- Heat gradient: ...
- Vegetation gradient: ...
- Fire gradient: ...
- Differential summary: ...
```

Add a short section to `governance_summary.md`:

```text
## Differential Field Reading

- Strongest water advantage: ...
- Highest heat pressure: ...
- Strongest vegetation buffer: ...
- Highest fire exposure: ...
```

---

## 11. Tests Required

Create:

```text
tests/test_differential_field_runtime.py
```

Minimum tests:

1. differential context JSON loads successfully;
2. `calculate_gradient()` returns target minus reference;
3. `classify_gradient()` classifies thresholds correctly;
4. `derive_differential_field()` returns all required fields;
5. positive water and negative heat gradient can produce `water_advantage_with_heat_relief`;
6. negative water and positive heat gradient can produce `water_stress_with_heat_pressure`;
7. summary is non-empty and cautious;
8. `python -m unittest discover` still passes.

Update existing tests if necessary to include new output columns.

Do not remove existing tests.

---

## 12. GitHub Actions

The existing workflow already runs:

```bash
python -m unittest discover
```

Update JSON validation in:

```text
.github/workflows/cczps-lite-tests.yml
```

to include:

```bash
python -m json.tool cczps_lite/input/differential_context.json >/dev/null
```

Keep other workflow steps unchanged.

---

## 13. Engineering Constraints

Do NOT:

```text
add external dependencies
connect live weather
connect GIS
connect database
add machine learning
add world model
implement Forcing Layer Runtime
implement Validation Layer Runtime
rewrite EcoEngine bridge
rename existing columns unless necessary
break current tests
```

Use:

```text
Python standard library only
small transparent functions
clear fallback behaviour
cautious wording
```

---

## 14. Completion Criteria

Task is complete when:

1. `cczps_lite/input/differential_context.json` exists.
2. `cczps_lite/engine/differential_field.py` exists.
3. Scenario comparison output includes differential field columns.
4. Scenario report includes Differential Field Runtime section.
5. Governance summary includes Differential Field Reading section.
6. Differential field tests exist and pass.
7. Existing tests still pass.
8. GitHub Actions remains green.

---

## 15. Suggested Commit Message

```text
Add Differential Field Runtime to CCZPS-Lite
```

---

## 16. Strategic Purpose

Task 07 is the first operational implementation of the EcoEngine v2 principle:

```text
A point is never interpreted alone.
A field can be inferred through representative differentials.
```

Task 06 created the EcoEngine bridge.

Task 07 begins the real EcoEngine v2 runtime.

This task should remain modest but meaningful:

```text
Representative Context
    ↓
Differential Gradient
    ↓
Runtime Field Reading
    ↓
Governance Interpretation
```

Do not build the whole mountain.

Place the first reliable stone.
