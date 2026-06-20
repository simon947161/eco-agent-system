# CRP — ClimateOS Forecast / Planning Layer and TimesFM Integration Note

**Date:** 2026-06-20  
**Project:** ClimateOS / EcoEngine / CCZPS / Forecast Layer / Planning Layer / Task100

---

## 1. Core Knowledge Points

### K1. TimesFM is a Forecast Engine, not ClimateOS

TimesFM should not be treated as ClimateOS itself, nor as EcoEngine itself.

Current positioning:

```text
TimesFM = Forecast Engine / Forecast Provider
```

Its role is to use historical time-series data to forecast future time-series behaviour.

It does not provide:

- governance
- validation
- evidence synthesis
- planning decisions
- execution logic
- cultivation outcomes

ClimateOS should therefore avoid binding itself to TimesFM as a core dependency.

---

### K2. Forecasting is useful for planning, not truth

Forecast output is not reality.

Forecast output should be treated as:

```text
Forecast Candidate
```

A forecast becomes useful only when it enters the ClimateOS chain:

```text
Forecast
↓
Validation
↓
Evidence
↓
Reasoning
↓
Planning
↓
Governance / Cultivation
```

This prevents the common AI-system error:

```text
Prediction = Truth
```

ClimateOS should instead maintain:

```text
Prediction ≠ Truth
Prediction = Input for Validation and Planning
```

---

### K3. TimesFM belongs more naturally to the Planning Layer than the Core Runtime

The key use case is not simply forecasting weather or energy values.

The real use case is helping humans, planners, communities, agents, and project teams test possible futures while preparing plans.

Example questions:

- What if a community builds 2 MW of solar?
- What if it builds 5 MW?
- What if battery storage is added?
- What if drought intensifies?
- What if rainfall shifts?
- What if water demand changes?
- What if energy prices fluctuate?

TimesFM can support the forecasting component of these planning questions, but ClimateOS must still organize the scenario, compare forecast sources, validate outputs, and connect results to governance decisions.

---

## 2. Relationship Between Forecast Engines and EcoEngine

### Forecast engines ask:

```text
What is most likely to happen?
```

### EcoEngine asks broader questions:

```text
What may happen?
What should happen?
What should not happen?
How can a better future be cultivated?
```

Therefore:

```text
TimesFM ≠ EcoEngine
TimesFM = Forecast Plugin
EcoEngine = Possibility / Scenario / Scientific Reasoning Engine
ClimateOS = Runtime that connects forecast, validation, evidence, planning, governance and cultivation
```

TimesFM should be seen as a possible forecasting assistant inside a future Planning and Scenario Layer.

---

## 3. Forecast Layer Plugin Architecture

ClimateOS should maintain a provider-neutral forecast architecture.

Possible future forecast providers:

- TimesFM
- Chronos
- Moirai
- MOMENT
- traditional statistical models
- industry forecasting models
- expert models
- future climate / hydrology / energy models

The architecture principle is:

```text
ClimateOS does not depend on one forecast model.
ClimateOS can call multiple forecast providers.
ClimateOS validates and compares forecast outputs.
```

---

## 4. Planning Layer Position

A future ClimateOS Planning Layer may use forecasting plugins as supporting tools.

Suggested chain:

```text
Observation
↓
Forecast Provider
↓
Forecast Candidate
↓
Validation
↓
Evidence
↓
Reasoning
↓
Scenario Planning
↓
Participation
↓
Governance
↓
Cultivation
```

Planning is not merely prediction.

Planning means:

- organizing possible futures
- testing scenarios
- comparing options
- identifying risks
- validating assumptions
- supporting human and AI-assisted decision-making

---

## 5. Task100 Alignment

Task100 should eventually include a forecast validation component.

Future sub-module concept:

```text
Forecast Validation Layer
```

Purpose:

- compare forecast outputs
- test forecast accuracy
- detect forecast bias
- measure forecast error
- validate forecast against later observations
- generate forecast confidence

Potential validation flow:

```text
Forecast Output
↓
Observed Reality
↓
Error / Bias / Confidence Review
↓
Validated Forecast Evidence
```

This strengthens Task100 as a validation layer rather than merely a demonstration task.

---

## 6. Forecast Resource Library

Future repository location suggestion:

```text
resources/forecast_models/
```

Initial files may include:

```text
timesfm.md
chronos.md
moirai.md
moment.md
forecast_model_comparison.md
forecast_validation_notes.md
```

Each resource note should record:

- source
- model type
- open-source status
- strengths
- limitations
- suitable scenarios
- possible ClimateOS use cases
- validation requirements
- planning-layer relevance

---

## 7. Strategic Decision

TimesFM should not be immediately embedded as a core dependency.

It should be recorded as:

```text
Forecast Plugin Candidate
```

and placed under a future:

```text
Planning and Scenario Layer
```

This preserves flexibility while ensuring ClimateOS can benefit from fast-developing external forecasting systems.

---

## 8. Future Task Reminder

Before Task100, consider creating a dedicated task such as:

```text
TaskXX — ClimateOS Forecast Resource Library and Planning Plugin Framework Foundation
```

Purpose:

- create a forecast resource library
- document TimesFM, Chronos, Moirai and MOMENT
- define forecast provider interface concepts
- define forecast validation requirements
- explain how forecast plugins support planning and scenario work
- prepare Task100 Forecast Validation integration

This task should not implement forecasting code yet.

It should establish the conceptual interface and planning-layer role.

---

## 9. Project Tags

```text
ClimateOS
EcoEngine
CCZPS
Task100
TimesFM
Forecast Layer
Forecast Plugin
Planning Layer
Scenario Planning
Forecast Validation
Forecast Resource Library
Possibility Computing
Evidence Asset
Governance Runtime
Cultivation
```

---

## Most Important Statement

Forecast engines such as TimesFM help answer what may be likely. ClimateOS must go further: it must validate forecasts, compare possibilities, connect them to evidence, and support planning, governance and cultivation. TimesFM is therefore not a core dependency, but a future planning-layer forecast plugin candidate.
