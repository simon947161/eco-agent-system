# CODEX TASK 05 — ADD TESTS AND SAMPLE OUTPUT VALIDATION

## CCZPS-Lite v0.4 Stabilization Task

Author: Simon Shu (Min Shu) + AI Dialogue System  
Repository: simon947161/eco-agent-system  
Task Type: Stabilization / Regression Protection  
Priority: High  
Status: Ready for Codex

---

## 1. Objective

Add a small but reliable test suite for the current CCZPS-Lite v0.4 prototype.

The goal is to protect the existing behaviour of:

```text
Scenario comparison
Evidence layer
Runtime fields
Runtime reasoning
Generated CSV output
Generated Markdown reports
```

This task should NOT add new product features.

This task should NOT connect external data sources.

This task should make the current engine safer to refactor later.

---

## 2. Current Architecture Context

CCZPS-Lite v0.4 currently follows this workflow:

```text
Location Profile
    ↓
Scenario Options
    ↓
Evidence Profile
    ↓
Scoring Rules
    ↓
Runtime Fields
    ↓
Runtime Reasoning
    ↓
Scenario Report
    ↓
Governance Summary
```

The prototype now combines four future layers in a compact workflow:

```text
CCZPS = scenario comparison and governance logic
EcoEngine = runtime fields and runtime reasoning
ESG++ = future institutional translation candidate
EcoChain = future evidence and trust record candidate
```

Task 05 should protect this v0.4 behaviour before new capabilities are added.

---

## 3. Required New Test Directory

Create:

```text
tests/
├── __init__.py
├── test_cczps_lite_scoring.py
├── test_cczps_lite_runtime_fields.py
├── test_cczps_lite_runtime_reasoning.py
├── test_cczps_lite_evidence_layer.py
└── test_cczps_lite_outputs.py
```

Use Python standard library only.

Use `unittest`.

Do not use pytest.

Do not add external dependencies.

---

## 4. Test Scoring Rules

Create:

```text
tests/test_cczps_lite_scoring.py
```

Test functions from:

```text
cczps_lite/engine/scoring_rules.py
```

Minimum test coverage:

- resilience score is calculated from water, energy, ecology, and fire scores;
- governance score penalizes implementation complexity;
- risk-adjusted score penalizes validation need;
- recommendation classification returns expected categories.

Use simple fixed score dictionaries.

Tests should verify values or category behaviour clearly.

---

## 5. Test Runtime Fields

Create:

```text
tests/test_cczps_lite_runtime_fields.py
```

Test functions from:

```text
cczps_lite/engine/runtime_fields.py
```

Minimum test coverage:

- high water security produces a Good or Strong water balance signal;
- low water security produces Low or Very Low water balance signal;
- strong ecological and fire scores produce Strong ecological resilience;
- weak water and ecology produce High or Extreme evaporation pressure;
- high validation need lowers confidence;
- validation_required is True when validation_need threshold is met.

---

## 6. Test Runtime Reasoning

Create:

```text
tests/test_cczps_lite_runtime_reasoning.py
```

Test functions from:

```text
cczps_lite/engine/runtime_reasoning.py
```

Minimum test coverage:

- low water security creates a water-related differential field;
- low energy resilience creates an energy-related forcing candidate;
- low fire resilience creates fire-related pressure;
- high validation need creates higher validation priority;
- runtime notes are non-empty human-readable strings;
- list-style outputs are lists, not raw strings.

Do not require exact wording for long notes unless necessary.

Prefer testing meaningful behaviour.

---

## 7. Test Evidence Layer

Create:

```text
tests/test_cczps_lite_evidence_layer.py
```

Test functions from:

```text
cczps_lite/engine/evidence_layer.py
```

Minimum test coverage:

- low evidence strength maps to Low;
- high evidence strength maps to High;
- mixed evidence produces a Mixed Sources or equivalent source basis;
- low evidence triggers human_review_required;
- uncertainty notes are generated and non-empty;
- missing or incomplete evidence records are handled safely.

---

## 8. Test Output Generation

Create:

```text
tests/test_cczps_lite_outputs.py
```

This test should run the CCZPS-Lite generator and validate generated output shape.

It may call:

```python
from cczps_lite.engine.scenario_compare import main
```

or invoke the script logic directly.

Minimum validation:

### comparison_matrix.csv

Ensure the generated CSV contains required columns:

```text
scenario_id
scenario_name
scenario_type
resilience_score
governance_score
risk_adjusted_score
recommendation_class
water_balance_signal
ecological_resilience_signal
evaporation_pressure
risk_index
confidence_level
validation_required
differential_field
forcing_candidates
validation_reason
validation_priority
runtime_notes
evidence_strength
source_basis
uncertainty_notes
human_review_required
```

Ensure it contains exactly three scenario rows for v0.4.

### scenario_report.md

Ensure the report contains:

```text
Runtime Assessment
Runtime Explanation
Evidence
Methodology Boundary
```

or equivalent headings currently used in the generated report.

### governance_summary.md

Ensure the summary contains:

```text
EcoEngine Runtime Summary
EcoEngine Runtime Interpretation
Evidence Assessment
Suggested Next Step
```

or equivalent headings currently used in the generated summary.

If current headings differ slightly, update tests to match the actual report language rather than rewriting reports unnecessarily.

---

## 9. Import Path Requirement

Tests should work when run from the repository root using:

```bash
python -m unittest discover
```

If import paths need small adjustments, use standard-library safe approaches such as:

```python
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "cczps_lite" / "engine"))
```

Do not introduce packaging tools.

Do not add setup.py or pyproject.toml in this task unless absolutely necessary.

---

## 10. Optional Small Improvement

If needed, add empty package markers:

```text
cczps_lite/__init__.py
cczps_lite/engine/__init__.py
```

Only add them if they help clean imports.

Do not restructure the project in this task.

---

## 11. Engineering Constraints

Do NOT:

```text
add new runtime features
add ESG++ translation
add EcoChain records
connect weather APIs
connect GIS
connect databases
add machine learning
add world models
refactor module boundaries
rename existing output fields
change scenario scores unnecessarily
```

Keep:

```text
Python standard library only
unittest only
current behaviour preserved
```

---

## 12. Completion Criteria

Task is complete when:

1. The new test files exist.
2. Tests run successfully with:

```bash
python -m unittest discover
```

3. Existing generator still runs successfully with:

```bash
python cczps_lite/engine/scenario_compare.py
```

4. Python files compile successfully with:

```bash
python -m compileall cczps_lite tests
```

5. Generated output files still contain three scenarios.
6. Required runtime, reasoning, and evidence columns remain present.
7. No external dependencies are introduced.

---

## 13. Suggested Commit Message

```text
Add CCZPS-Lite v0.4 stabilization tests
```

---

## 14. Strategic Purpose

Task 01 built the first scenario comparison engine.

Task 02 connected EcoEngine runtime fields.

Task 03 added runtime reasoning.

Task 04 added evidence-aware context.

Task 05 stabilizes the system.

After Task 05, the project should have regression protection before any future task adds:

```text
real weather data
Open-Meteo integration
EcoEngine v1.9.2b connection
ESG++ translation
EcoChain records
World Model interfaces
```

A small engine without tests is a tractor without brakes.

This task installs the brakes before the next hill.
