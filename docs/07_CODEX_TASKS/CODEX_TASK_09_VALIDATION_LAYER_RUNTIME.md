# CODEX TASK 09 — VALIDATION LAYER RUNTIME

## EcoEngine V2 Runtime Core: From Candidate Forcing to Evidence-Aware Validation

Author: Simon Shu (Min Shu) + AI Dialogue System  
Repository: simon947161/eco-agent-system  
Task Type: Runtime Method Implementation  
Priority: High  
Status: Ready for Codex

---

## 1. Objective

Implement the first lightweight **Validation Layer Runtime** for CCZPS-Lite.

Task 07 added Differential Field Runtime:

```text
What is different?
```

Task 08 added Forcing Layer Runtime:

```text
What may be driving the difference?
```

Task 09 should add:

```text
How credible is this interpretation?
What evidence supports it?
What still needs to be checked?
```

This is not a scientific validation engine yet.

It is a transparent, cautious, rule-based validation layer that combines:

```text
Evidence Layer
Differential Field Runtime
Forcing Layer Runtime
Runtime Fields
```

into a first validation reading.

---

## 2. Architecture Context

Current runtime stack:

```text
Scenario Scores
    ↓
Runtime Fields
    ↓
Differential Field Runtime
    ↓
Forcing Layer Runtime
    ↓
Evidence Layer
    ↓
Governance Output
```

Task 09 adds:

```text
Validation Layer Runtime
```

New stack:

```text
Scenario Scores
    ↓
Runtime Fields
    ↓
Differential Field Runtime
    ↓
Forcing Layer Runtime
    ↓
Evidence Layer
    ↓
Validation Layer Runtime
    ↓
Governance Output
```

Core principle:

```text
A candidate forcing is not a conclusion until evidence quality, uncertainty, and validation needs are checked.
```

---

## 3. Current Stable Baseline

Current repository includes:

```text
cczps_lite/engine/differential_field.py
cczps_lite/engine/forcing_layer.py
cczps_lite/engine/evidence_layer.py
cczps_lite/engine/runtime_fields.py
cczps_lite/engine/scenario_compare.py
```

Existing commands should pass:

```bash
python cczps_lite/engine/scenario_compare.py
python -m unittest discover
```

Before starting Task 09, ensure Task 08 forcing fields are fully integrated into `scenario_compare.py` and GitHub Actions is green.

If Actions is red because `scenario_compare.py` does not yet output forcing fields, fix that first.

---

## 4. Required New Module

Create:

```text
cczps_lite/engine/validation_layer.py
```

Required functions:

```python
def derive_validation_reading(runtime_fields, differential_result, forcing_result, evidence_result):
    pass


def classify_validation_status(validation_score, validation_required, evidence_strength):
    pass


def summarize_validation_layer(validation_result):
    pass
```

Use Python standard library only.

---

## 5. Input Expectations

The validation layer should accept dictionaries already produced by existing layers.

### runtime_fields

Expected keys may include:

```text
risk_index
confidence_level
validation_required
water_balance_signal
ecological_signal
evaporation_pressure
```

### differential_result

Expected keys may include:

```text
water_gradient_class
heat_gradient_class
vegetation_gradient_class
fire_gradient_class
differential_status
```

### forcing_result

Expected keys may include:

```text
forcing_candidates
primary_forcing
forcing_priority
forcing_summary
```

`forcing_candidates` may be either a list or a semicolon-separated string.

### evidence_result

Expected keys may include:

```text
evidence_strength
source_basis
uncertainty_notes
human_review_required
```

---

## 6. Validation Score

Produce a simple numeric score from 0–10.

Suggested starting point:

```text
base = 6.0
```

Adjustments:

### Evidence adjustment

```text
High evidence      +2
Medium evidence    +1
Low evidence       -2
```

### Confidence adjustment

```text
confidence_level == medium  +1
confidence_level == low     -1
```

### Runtime validation need

```text
validation_required == True  -1
```

### Human review

```text
human_review_required == True  -1
```

### Forcing priority

```text
High forcing priority with Low evidence  -1
High forcing priority with Medium/High evidence  +0
```

Clamp final score to 0–10.

Return as rounded value with two decimals.

---

## 7. Validation Status

Implement:

```python
def classify_validation_status(validation_score, validation_required, evidence_strength):
    pass
```

Suggested labels:

```text
Validated Enough for Concept Review
Requires Local Validation
Requires Technical Validation
Insufficient Evidence
```

Suggested rules:

```text
if evidence_strength == Low and validation_score < 5:
    Insufficient Evidence

if validation_required is True and validation_score < 6:
    Requires Technical Validation

if validation_score >= 7:
    Validated Enough for Concept Review

otherwise:
    Requires Local Validation
```

Keep wording cautious.

---

## 8. Evidence Gaps

`derive_validation_reading()` should also return a list:

```text
validation_gaps
```

Suggested gap rules:

### Low evidence

If evidence strength is Low:

```text
Need stronger field evidence or technical assessment
```

### High heat / evaporation forcing

If forcing candidates include:

```text
Heat Exposure
Evaporation Pressure
```

Add:

```text
Need local temperature, humidity, and evaporation observation
```

### Water storage deficit

If forcing candidates include:

```text
Water Storage Deficit
```

Add:

```text
Need hydrological or soil moisture validation
```

### Fire exposure

If forcing candidates include:

```text
Fire Exposure
```

Add:

```text
Need bushfire exposure and vegetation management review
```

### Vegetation stress

If forcing candidates include:

```text
Vegetation Stress
Microclimate Buffer Loss
```

Add:

```text
Need ecological condition and canopy-cover review
```

### No gaps

If no gaps are identified:

```text
No major validation gap identified at concept level
```

Avoid duplicates.

---

## 9. Required Output Fields

`derive_validation_reading()` should return:

```json
{
  "validation_score": 6.0,
  "validation_status": "Requires Local Validation",
  "validation_gaps": [
    "Need local temperature, humidity, and evaporation observation"
  ],
  "validation_summary": "Validation layer cautiously rates this interpretation as requiring local validation because evidence is medium and forcing remains candidate-only."
}
```

For CSV, `validation_gaps` should be serialized as semicolon-separated text.

---

## 10. Validation Summary

`summarize_validation_layer()` should create one cautious sentence.

Examples:

```text
Validation layer cautiously rates this pathway as requiring technical validation due to low evidence and unresolved forcing assumptions.
```

```text
Validation layer cautiously considers this pathway sufficient for concept review, but local consultation and site checks remain necessary.
```

Must avoid overclaiming.

Use words such as:

```text
cautiously
requires
concept-level
candidate
local validation
technical validation
```

---

## 11. Integrate with Scenario Compare

Update:

```text
cczps_lite/engine/scenario_compare.py
```

After evidence, runtime, differential, and forcing are derived, call:

```python
derive_validation_reading(runtime, differential, forcing, evidence_result)
```

Where `evidence_result` is a dictionary such as:

```python
evidence_result = {
    "evidence_strength": derive_evidence_strength(scenario_evidence),
    "source_basis": derive_source_basis(scenario_evidence),
    "uncertainty_notes": derive_uncertainty_notes(scenario_evidence),
    "human_review_required": derive_human_review_required(scenario_evidence),
}
```

Add to each scenario row:

```text
validation_score
validation_status
validation_gaps
validation_summary
```

For CSV, store `validation_gaps` as semicolon-separated text.

---

## 12. Update Reports

### 12.1 scenario_report.md

For each scenario, add after Forcing Layer Runtime:

```text
### Validation Layer Runtime

- Validation score: ...
- Validation status: ...
- Validation gaps: ...
- Validation summary: ...
```

---

### 12.2 governance_summary.md

Add:

```text
## Validation Layer Reading
```

Include:

```text
- Highest validation score: ...
- Lowest validation score: ...
- Pathways requiring technical validation: ...
- Most common validation gap: ...
```

Keep language cautious.

---

## 13. Tests Required

Create:

```text
tests/test_validation_layer_runtime.py
```

Minimum tests:

1. high evidence and medium confidence can produce a higher validation score;
2. low evidence reduces validation score;
3. low evidence plus validation required can produce Insufficient Evidence or Requires Technical Validation;
4. heat / evaporation forcing produces temperature-humidity-evaporation validation gap;
5. Water Storage Deficit produces hydrological / soil moisture validation gap;
6. Fire Exposure produces bushfire / vegetation management validation gap;
7. Vegetation Stress produces ecological / canopy review gap;
8. validation summary is non-empty and cautious;
9. scenario_compare output includes validation_score, validation_status, validation_gaps, validation_summary;
10. `python -m unittest discover` still passes.

Update existing regression tests if needed to assert new validation fields and report sections are present.

Do not remove existing tests.

---

## 14. GitHub Actions

No new workflow dependency is required.

Existing workflow should already run:

```bash
python -m unittest discover
```

Keep workflow unchanged unless necessary.

---

## 15. Engineering Constraints

Do NOT:

```text
add external dependencies
connect live weather
connect GIS
connect database
add machine learning
add world model
replace Evidence Layer
replace Differential Field Runtime
replace Forcing Layer Runtime
rewrite scenario engine unnecessarily
claim scientific validation
```

Use:

```text
Python standard library only
small transparent functions
controlled vocabulary
cautious wording
evidence-aware scoring
```

---

## 16. Completion Criteria

Task is complete when:

1. `cczps_lite/engine/validation_layer.py` exists.
2. Scenario comparison output includes validation fields.
3. Scenario report includes Validation Layer Runtime sections.
4. Governance summary includes Validation Layer Reading.
5. Validation layer tests exist and pass.
6. Existing evidence, differential, forcing, bridge tests still pass.
7. GitHub Actions remains green.

---

## 17. Suggested Commit Message

```text
Add Validation Layer Runtime to CCZPS-Lite
```

---

## 18. Strategic Purpose

Task 09 is the first runtime layer that gives CCZPS-Lite an environmental judgement discipline.

Differential Runtime asks:

```text
What is different?
```

Forcing Runtime asks:

```text
What may be driving the difference?
```

Validation Runtime asks:

```text
Why should we trust this interpretation, and what must be checked before action?
```

This is where EcoEngine begins to move from a comparison tool toward a governance-grade reasoning system.

Do not overclaim.

Do not prove causality.

Create the first disciplined validation gate.
