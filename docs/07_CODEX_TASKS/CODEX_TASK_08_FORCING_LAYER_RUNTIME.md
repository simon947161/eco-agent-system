# CODEX TASK 08 — FORCING LAYER RUNTIME

## EcoEngine V2 Runtime Core: From Differential Signals to Candidate Environmental Forcing

Author: Simon Shu (Min Shu) + AI Dialogue System  
Repository: simon947161/eco-agent-system  
Task Type: Runtime Method Implementation  
Priority: High  
Status: Ready for Codex

---

## 1. Objective

Implement the first lightweight **Forcing Layer Runtime** for CCZPS-Lite.

Task 07 added Differential Field Runtime. It allows the prototype to detect representative gradients:

```text
water_gradient
heat_gradient
vegetation_gradient
fire_gradient
```

Task 08 should add a cautious interpretation layer that asks:

```text
What environmental pressure may explain this differential?
```

This task should not implement Validation Layer Runtime yet.

This task should not connect live weather, GIS, databases, machine learning, or world models.

The goal is a small, transparent, testable rule-based forcing layer.

---

## 2. Architecture Context

Current flow after Task 07:

```text
Scenario Scores
    ↓
Differential Field Runtime
    ↓
Gradient Signals
    ↓
Runtime / Evidence / Governance Output
```

Task 08 adds:

```text
Differential Field Runtime
    ↓
Forcing Layer Runtime
    ↓
Candidate Environmental Pressures
```

Conceptual distinction:

```text
Differential Field = what is different?
Forcing Layer = what may be driving the difference?
Validation Layer = how confident are we and what evidence is required?
```

Task 08 only addresses the second question.

---

## 3. Current Stable Baseline

Current repository includes:

```text
cczps_lite/engine/differential_field.py
cczps_lite/input/differential_context.json
cczps_lite/engine/scenario_compare.py
tests/test_differential_field_runtime.py
```

Existing commands should continue to pass:

```bash
python cczps_lite/engine/scenario_compare.py
python -m unittest discover
```

GitHub Actions should remain green.

---

## 4. Required New Module

Create:

```text
cczps_lite/engine/forcing_layer.py
```

Required functions:

```python
def derive_forcing_candidates(differential_result, scenario_scores=None):
    pass


def classify_forcing_priority(candidates):
    pass


def summarize_forcing_layer(forcing_result):
    pass
```

Use Python standard library only.

---

## 5. Forcing Candidate Logic

The function should accept the output of:

```python
derive_differential_field()
```

and return candidate forcing signals.

### 5.1 Suggested Candidate Types

Use a small controlled vocabulary:

```text
Evaporation Pressure
Heat Exposure
Water Storage Deficit
Vegetation Stress
Fire Exposure
Microclimate Buffer Loss
Mixed / Unclear Forcing
```

---

## 6. Suggested Mapping Rules

### Rule A — Water Stress with Heat Pressure

If:

```text
water_gradient_class is moderate_negative or strong_negative
AND
heat_gradient_class is moderate_positive or strong_positive
```

Add:

```text
Water Storage Deficit
Heat Exposure
Evaporation Pressure
```

---

### Rule B — High Heat Gradient

If:

```text
heat_gradient_class is moderate_positive or strong_positive
```

Add:

```text
Heat Exposure
Evaporation Pressure
```

---

### Rule C — Vegetation Decline

If:

```text
vegetation_gradient_class is moderate_negative or strong_negative
```

Add:

```text
Vegetation Stress
Microclimate Buffer Loss
```

---

### Rule D — Fire Exposure

If:

```text
fire_gradient_class is moderate_positive or strong_positive
```

Add:

```text
Fire Exposure
Vegetation Stress
```

---

### Rule E — Water Advantage with Heat Relief

If:

```text
differential_status == water_advantage_with_heat_relief
```

Add:

```text
Microclimate Buffer Support
```

Note: this is a positive / protective forcing signal.

---

### Rule F — No Strong Signal

If no specific candidates are found:

```text
Mixed / Unclear Forcing
```

---

## 7. Required Output Fields

`derive_forcing_candidates()` should return a dictionary:

```json
{
  "forcing_candidates": [
    "Heat Exposure",
    "Evaporation Pressure"
  ],
  "primary_forcing": "Heat Exposure",
  "forcing_priority": "Medium",
  "forcing_summary": "Forcing layer cautiously identifies heat exposure and evaporation pressure as candidate drivers."
}
```

The candidate list should avoid duplicates while preserving logical order.

---

## 8. Forcing Priority

Implement:

```python
def classify_forcing_priority(candidates):
    pass
```

Suggested logic:

```text
If candidates include Fire Exposure and Heat Exposure:
    High

If candidates include Water Storage Deficit and Evaporation Pressure:
    High

If candidate count >= 2:
    Medium

If only Mixed / Unclear Forcing:
    Low

Otherwise:
    Medium
```

Keep this simple and explainable.

---

## 9. Forcing Summary

`summarize_forcing_layer()` should produce a short cautious sentence.

Example:

```text
Forcing layer cautiously identifies heat exposure and evaporation pressure as candidate drivers behind the observed differential field.
```

If the signal is protective:

```text
Forcing layer cautiously identifies microclimate buffer support as a possible protective influence.
```

If unclear:

```text
Forcing layer does not identify a dominant candidate driver from the current representative gradients.
```

Do not overclaim causality.

Use words such as:

```text
cautiously
candidate
possible
indicative
```

---

## 10. Integrate with Scenario Compare

Update:

```text
cczps_lite/engine/scenario_compare.py
```

After deriving the differential field, call:

```python
derive_forcing_candidates(differential, scores)
```

Add to each scenario row:

```text
forcing_candidates
primary_forcing
forcing_priority
forcing_summary
```

For CSV, store `forcing_candidates` as semicolon-separated text.

---

## 11. Update Reports

### 11.1 scenario_report.md

For each scenario, add:

```text
### Forcing Layer Runtime

- Primary forcing: ...
- Forcing candidates: ...
- Forcing priority: ...
- Forcing summary: ...
```

Place this after Differential Field Runtime.

---

### 11.2 governance_summary.md

Add:

```text
## Forcing Layer Reading
```

Include:

```text
- Highest forcing priority: ...
- Most common candidate forcing: ...
- Scenarios with Fire Exposure forcing: ...
- Scenarios with Microclimate Buffer Support: ...
```

Keep wording cautious.

---

## 12. Tests Required

Create:

```text
tests/test_forcing_layer_runtime.py
```

Minimum tests:

1. water stress + heat pressure produces Water Storage Deficit, Heat Exposure, and Evaporation Pressure;
2. positive heat gradient produces Heat Exposure and Evaporation Pressure;
3. negative vegetation gradient produces Vegetation Stress and Microclimate Buffer Loss;
4. positive fire gradient produces Fire Exposure;
5. water_advantage_with_heat_relief produces Microclimate Buffer Support;
6. unclear differentials produce Mixed / Unclear Forcing;
7. forcing priority classification returns High for combined heat/fire or water/evaporation signals;
8. forcing summary is non-empty and cautious;
9. `python -m unittest discover` still passes.

Update existing tests if needed to assert new CSV/report/governance fields are present.

Do not remove existing tests.

---

## 13. GitHub Actions

Existing workflow already runs:

```bash
python -m unittest discover
```

No major workflow change is required unless new files need JSON validation.

If no new input JSON is added, do not modify workflow unnecessarily.

---

## 14. Engineering Constraints

Do NOT:

```text
add external dependencies
connect live weather
connect GIS
connect database
add machine learning
add world model
implement Validation Layer Runtime
rewrite Differential Field Runtime
rewrite EcoEngine bridge
rename existing columns unless necessary
break current tests
```

Use:

```text
Python standard library only
small transparent functions
controlled vocabulary
cautious wording
```

---

## 15. Completion Criteria

Task is complete when:

1. `cczps_lite/engine/forcing_layer.py` exists.
2. Scenario comparison output includes forcing layer columns.
3. Scenario report includes Forcing Layer Runtime sections.
4. Governance summary includes Forcing Layer Reading.
5. Forcing layer tests exist and pass.
6. Existing tests still pass.
7. GitHub Actions remains green.

---

## 16. Suggested Commit Message

```text
Add Forcing Layer Runtime to CCZPS-Lite
```

---

## 17. Strategic Purpose

Task 07 allowed the system to ask:

```text
What is different?
```

Task 08 allows the system to ask:

```text
What may be driving the difference?
```

This is the second major runtime step toward EcoEngine V2.

The goal is not scientific proof.

The goal is a cautious, transparent candidate-forcing layer that can later be tested by the Validation Layer Runtime.

Do not prove causality.

Identify candidate pressure.
