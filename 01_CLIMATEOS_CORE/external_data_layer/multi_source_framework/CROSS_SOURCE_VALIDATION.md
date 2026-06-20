# Cross-Source Validation

## Purpose

Cross-source validation defines how ClimateOS may compare complementary
observation resources from multiple providers.

## Major Focus

ClimateOS should be capable of treating different providers as complementary
observation resources.

Example:

```text
NASA
-> Soil Moisture

BOM
-> Rainfall

Local Sensors
-> Water Level

Community Observation
-> Vegetation Stress
```

Together, these resources may support a richer picture of environmental reality.

## Review Questions

- Do sources describe the same location or system?
- Do sources describe the same time period?
- Are units, scale, and resolution compatible?
- Do sources support or challenge the same relationship?
- Are differences explainable by method, timing, or uncertainty?
- Does human review identify missing context?

## Boundary

No cross-source validation algorithm, scoring model, or automated decision
system is implemented.
