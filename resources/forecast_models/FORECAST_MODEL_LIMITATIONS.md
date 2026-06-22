# Forecast Model Limitations

## Core Limitation

Forecast output is not truth.

Forecasts are conditional outputs shaped by input data, assumptions, model
design, time horizon, and context.

## Risks

- forecast hallucination risk
- model drift risk
- data quality risk
- wrong time horizon risk
- inappropriate model use
- overconfidence risk
- scenario assumption risk
- governance misuse risk
- treating prediction as truth
- treating external model output as ClimateOS output
- dependency on one vendor or one model
- lack of validation against observed reality

## ClimateOS Principle

```text
Best Available Forecast
+ Independent Validation
+ Evidence-Based Planning
```

## Required Boundary

Forecast providers must remain optional plugin candidates unless and until
future tasks implement, test, and validate a specific integration.

