# CODEX TASK 06 — CONNECT ECOENGINE V1.9.2B

## Bridge EcoEngine Scenario Validation Output into CCZPS-Lite Runtime

Author: Simon Shu (Min Shu) + AI Dialogue System  
Repository: simon947161/eco-agent-system  
Task Type: Integration Bridge / Compatibility Layer  
Priority: High  
Status: Ready for Codex

---

## 1. Objective

Connect CCZPS-Lite v0.4 with EcoEngine v1.9.2b through a small, safe compatibility bridge.

The goal is NOT to rewrite CCZPS-Lite.

The goal is NOT to migrate the full EcoEngine v1.9.2b codebase into this repository.

The goal is to create a lightweight adapter that can read EcoEngine-style scenario validation records and map them into CCZPS-Lite runtime fields.

This task should preserve the current green GitHub Actions workflow.

---

## 2. Current Stable Baseline

CCZPS-Lite v0.4 is now operational and automatically tested.

Current working flow:

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

Current successful validation:

```bash
python cczps_lite/engine/scenario_compare.py
python -m unittest tests/test_cczps_lite.py
```

GitHub Actions workflow:

```text
CCZPS-Lite Tests
```

is green.

Task 06 must not break this.

---

## 3. EcoEngine v1.9.2b Context

EcoEngine v1.9.2b is a scenario validation build focused on Great Dividing Range west/east climate regime validation.

It checks:

- climate regime classification,
- dry inland / humid coastal / transition distinction,
- instability pathways,
- compound events,
- regime-adjusted intensities,
- scenario weather systems,
- JSON / CSV / Markdown validation outputs.

Typical conceptual fields include:

```text
climate_regime
instability_pathways
compound_events
regime_adjusted_intensity
risk_index
water_balance_signal
ecological_resilience
evaporation_pressure
priority_level
validation_required
confidence_level
```

The exact v1.9.2b output schema may vary.

Therefore, Task 06 should use a tolerant adapter design.

---

## 4. Required New Directory

Create:

```text
cczps_lite/integration/
```

Add:

```text
cczps_lite/integration/__init__.py
cczps_lite/integration/ecoengine_v192b_adapter.py
cczps_lite/input/ecoengine_sample_output.json
```

---

## 5. Sample EcoEngine Output

Create:

```text
cczps_lite/input/ecoengine_sample_output.json
```

Use a small sample record that resembles EcoEngine v1.9.2b style output.

Example structure:

```json
{
  "source": "ecoengine_v1_9_2b_sample",
  "location_id": "batlow_nsw_001",
  "location_name": "Batlow, NSW",
  "climate_regime": "dry_inland",
  "instability_pathways": [
    "evaporation_dominated",
    "soil_degradation",
    "wind_exposed_dry"
  ],
  "compound_events": [
    "dry_wind",
    "heat_dry"
  ],
  "regime_adjusted_intensity": 7.2,
  "runtime_fields": {
    "risk_index": 4.1,
    "water_balance_signal": "watch",
    "ecological_resilience": "moderate",
    "evaporation_pressure": "high",
    "confidence_level": "medium",
    "validation_required": true
  },
  "notes": "Indicative sample record for bridge testing only."
}
```

This is a sample only.

Do not claim this is validated live EcoEngine output.

---

## 6. Adapter Module Requirements

Create:

```text
cczps_lite/integration/ecoengine_v192b_adapter.py
```

Required functions:

```python
def load_ecoengine_record(path):
    pass


def map_ecoengine_to_runtime_fields(record):
    pass


def summarize_ecoengine_bridge(record):
    pass
```

Use Python standard library only.

No external APIs.

No GIS.

No weather calls.

No full EcoEngine import.

---

## 7. Mapping Rules

The adapter should be tolerant.

It should accept fields either at root level or under `runtime_fields`.

### risk_index

Use in order:

1. `record["runtime_fields"]["risk_index"]`
2. `record["risk_index"]`
3. fallback: `None`

### water_balance_signal

Use in order:

1. `record["runtime_fields"]["water_balance_signal"]`
2. `record["water_balance_signal"]`
3. infer from instability pathways:
   - if `evaporation_dominated` or `wind_exposed_dry` exists → `watch`
4. fallback: `unknown`

### ecological_signal

Use in order:

1. `record["runtime_fields"]["ecological_resilience"]`
2. `record["ecological_resilience"]`
3. infer from `soil_degradation`:
   - if present → `limited`
4. fallback: `unknown`

### evaporation_pressure

Use in order:

1. `record["runtime_fields"]["evaporation_pressure"]`
2. `record["evaporation_pressure"]`
3. infer from `evaporation_dominated`:
   - if present → `high`
4. fallback: `unknown`

### confidence_level

Use in order:

1. `record["runtime_fields"]["confidence_level"]`
2. `record["confidence_level"]`
3. fallback: `low`

### validation_required

Use in order:

1. `record["runtime_fields"]["validation_required"]`
2. `record["validation_required"]`
3. if confidence_level is `low` → true
4. fallback: true

---

## 8. Bridge Summary

`summarize_ecoengine_bridge(record)` should return a short human-readable sentence.

Example:

```text
EcoEngine v1.9.2b bridge detected dry_inland regime with evaporation_dominated and wind_exposed_dry instability pathways. Runtime mapping suggests water balance watch, high evaporation pressure, and validation_required=True.
```

Keep the language cautious.

Do not overclaim.

---

## 9. Optional Report Output

Create a simple bridge report generator script if useful:

```text
cczps_lite/integration/run_ecoengine_bridge.py
```

This is optional.

If added, it should read:

```text
cczps_lite/input/ecoengine_sample_output.json
```

and generate:

```text
cczps_lite/output/ecoengine_bridge_report.md
```

Do not make this required if it complicates the task.

---

## 10. Tests Required

Add or update tests under:

```text
tests/test_ecoengine_v192b_bridge.py
```

Minimum tests:

1. sample EcoEngine record loads successfully;
2. nested runtime fields map correctly;
3. root-level fallback fields map correctly;
4. instability pathway fallback infers water_balance_signal and evaporation_pressure;
5. low confidence triggers validation_required;
6. bridge summary is non-empty and contains climate regime or instability information.

Run with:

```bash
python -m unittest discover
```

---

## 11. Update GitHub Actions

Update:

```text
.github/workflows/cczps-lite-tests.yml
```

so it runs:

```bash
python -m unittest discover
```

instead of only:

```bash
python -m unittest tests/test_cczps_lite.py
```

This ensures future bridge tests are included automatically.

Keep existing JSON validation, compile, and generator steps.

---

## 12. Engineering Constraints

Do NOT:

```text
rewrite CCZPS-Lite
break current output files
import external EcoEngine package
add external dependencies
connect live weather
connect GIS
add database
add dashboard
add ML or world model
rename existing runtime fields
remove existing tests
```

Use:

```text
Python standard library only
small adapter module
clear tests
cautious wording
```

---

## 13. Completion Criteria

Task is complete when:

1. `cczps_lite/integration/ecoengine_v192b_adapter.py` exists.
2. `cczps_lite/input/ecoengine_sample_output.json` exists.
3. Adapter maps EcoEngine-style records into CCZPS-Lite runtime fields.
4. Bridge summary function works.
5. Bridge tests exist and pass.
6. Existing CCZPS-Lite tests still pass.
7. GitHub Actions uses `python -m unittest discover`.
8. Workflow remains green.

---

## 14. Suggested Commit Message

```text
Connect EcoEngine v1.9.2b bridge to CCZPS-Lite runtime
```

---

## 15. Strategic Purpose

CCZPS-Lite v0.4 is currently a working governance runtime prototype.

Task 06 begins connecting it to the older EcoEngine v1.9.2b validation logic.

This creates the first bridge between:

```text
EcoEngine climate-regime validation
        ↓
CCZPS-Lite runtime interpretation
        ↓
Governance scenario comparison
```

The bridge should be small, stable, and reversible.

Do not rebuild the house.

Build the doorway.
