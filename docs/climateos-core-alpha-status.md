# ClimateOS Core Alpha Status

This note records the recovery and validation status of the historical Eco Engine V200 core.

## Local Source

```text
D:\eco_engine_v200
```

## Current Interpretation

`eco_engine_v200` is treated as **ClimateOS Core Alpha**.

It contains the environmental computation and climate-regime decision-support engine that was previously developed as an Eco Engine Agent validation build.

## Verified on 2026-06-02

The following command was successfully executed locally:

```bash
py -3.13 run_validation.py
```

The validation completed successfully and generated the following output files:

```text
output/validation_report_20260602_215346.json
output/validation_report_20260602_215346.md
output/validation_comparison_20260602_215346.csv
```

## Confirmed Capabilities

The recovered V200 core confirms the existence of a working chain from climate-regime classification to validation reporting.

Confirmed capabilities include:

- climate regime classification
- dry inland / humid coastal distinction
- transition regime recognition
- instability pathway detection
- compound event detection
- regime-aware validation reporting
- Markdown, JSON, and CSV output generation

## Relationship to Current Project Structure

The current interpretation is:

```text
eco_engine_v200
=
ClimateOS Core Alpha

D:\EcoEngine
=
Runtime / Human Demo Layer

eco-agent-system
=
Open-source project entry, governance, roadmap, and agent framework layer
```

This means the historical V200 core should not be treated as a simple demo.

It should be treated as the first recoverable and runnable core engine for the future ClimateOS structure.

## Project Meaning

This recovery confirms that the historical Eco Engine V200 is a runnable ClimateOS Core Alpha prototype.

It has already connected:

```text
Climate Regime
→ Ecological Risk
→ Decision Support
→ Validation Output
```

The next step is to prepare a clean open-source upload of the V200 core without disrupting the current `eco-agent-system` repository.

## Next Steps

Recommended next steps:

1. Run `run_showcase.py` and confirm showcase output.
2. Run `run_daily.py` and confirm live or fallback weather behaviour.
3. Prepare a clean upload strategy for `eco_engine_v200`.
4. Decide whether V200 should become a separate `climateos-core` repository.
5. Prepare a first open-source release note for ClimateOS Core Alpha.

## Status

```text
Status: Recovered and validated locally
Date: 2026-06-02
Core identity: ClimateOS Core Alpha
Upload status: Pending clean open-source packaging
```
