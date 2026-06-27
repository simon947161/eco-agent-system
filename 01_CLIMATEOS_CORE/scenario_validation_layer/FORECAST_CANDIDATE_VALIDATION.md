# Forecast Candidate Validation

## Purpose

Forecast Candidate Validation defines how forecast outputs may participate in
Scenario Validation.

## Forecast Candidate

A Forecast Candidate is a forecast output that may inform a scenario.

It is not truth until reviewed against evidence, observations, assumptions, and
validation context.

## Validation Questions

- Which forecast provider or plugin produced the candidate?
- What assumptions were used?
- What evidence supports the forecast candidate?
- What evidence conflicts with it?
- What time horizon applies?
- What uncertainty remains?
- Is the candidate suitable for scenario review?

## Plugin Boundary

Forecast providers remain optional plugins.

ClimateOS should remain provider-independent and should not trust prediction
models automatically.

## Boundary

No forecast execution, model integration, API, plugin runtime, or automated
forecast validation is implemented.

