# Location-to-Scenario Intake Runtime

## Purpose

The Location-to-Scenario Intake Runtime converts a user-supplied local JSON
record into a structured preliminary CCZPS-Lite scenario profile.

It answers:

- what place is being considered;
- where it is located;
- what context the user wants to explore;
- what evidence is still missing; and
- what governed review workflow may happen next.

Location intake is not environmental analysis.

## Local Use

From the repository root:

```bash
python cczps_lite/engine/location_intake.py \
  --input cczps_lite/input/location_intake_examples.json
```

On Windows:

```text
py cczps_lite/engine/location_intake.py --input cczps_lite/input/location_intake_examples.json
```

The runtime writes:

- `cczps_lite/output/location_intake_profiles.json`
- `cczps_lite/output/location_intake_profiles.md`

## Validation

The runtime requires a non-empty location name, numeric latitude from -90 to
90, numeric longitude from -180 to 180, and a non-empty intake context.
Country, region, and user intent are optional but recommended.

Invalid coordinates are not repaired. Invalid records remain visible under
`invalid_records` and are not promoted into `scenario_profiles`.

## Intake Profile Versus Validated Scenario

An intake profile is always marked `intake_only`. Its evidence and planning
hypothesis have not been generated, meteorology and GIS / DEM workflows have
not been requested, and approval support remains `not_ready_for_approval`.

The runtime does not inject new locations into existing scenario comparison,
planning hypothesis, evidence traceability, governance, or approval-support
outputs. A future governed task may explicitly promote selected intake records.

## Future Application Layers

FarmerOS, GardenOS, WaterOS, and ClimateOS may eventually use the intake profile
as a common first record before requesting evidence generation. Those future
workflows must preserve resource governance, consent, evidence quality,
professional review, and approval boundaries.

## Safety Boundary

This runtime performs no geocoding, location search, map rendering, external API
call, meteorology retrieval, GIS / DEM download, hydrology analysis, wind or
satellite analysis, simulation, language-model call, automatic planning
hypothesis, professional conclusion, recommendation, or approval decision.

Human and professional review remain required before any planning decision.
