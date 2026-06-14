# Location-to-Scenario Intake Runtime

Location intake only. This runtime does not perform geocoding, environmental analysis, meteorology retrieval, GIS / DEM processing, planning assessment, professional review, approval assessment, or recommendation generation.

- Valid preliminary profiles: 2
- Invalid input records: 1

## Tumut NSW

- Scenario ID: `tumut_nsw_intake`
- Country / region: Australia / New South Wales
- Coordinates: -35.3, 148.22
- Intake context: `climate_resilience_review`
- Scenario status: `intake_only`
- Workflow status: `awaiting_evidence_generation`
- Evidence status: `not_generated`
- Meteorology status: `not_requested`
- GIS / DEM status: `not_requested`
- Approval support status: `not_ready_for_approval`
- Human review required: True
- Professional review required: True

### Recommended Next Steps

- run governed meteorology refresh
- prepare GIS / DEM validation requirements
- generate planning hypothesis after evidence exists
- request professional review before any planning decision

### Limitations

- Location intake only
- No planning conclusion generated
- No GIS / DEM validation performed
- No meteorology retrieval performed unless separately triggered
- Not ready for approval

## Dunhuang Demonstration Area

- Scenario ID: `dunhuang_demonstration_area_intake`
- Country / region: China / Gansu
- Coordinates: 40.1421, 94.6619
- Intake context: `dryland_restoration_review`
- Scenario status: `intake_only`
- Workflow status: `awaiting_evidence_generation`
- Evidence status: `not_generated`
- Meteorology status: `not_requested`
- GIS / DEM status: `not_requested`
- Approval support status: `not_ready_for_approval`
- Human review required: True
- Professional review required: True

### Recommended Next Steps

- run governed meteorology refresh
- prepare GIS / DEM validation requirements
- generate planning hypothesis after evidence exists
- request professional review before any planning decision

### Limitations

- Location intake only
- No planning conclusion generated
- No GIS / DEM validation performed
- No meteorology retrieval performed unless separately triggered
- Not ready for approval

## Invalid Records

### Invalid Coordinate Example

- Input index: 2
- Validation errors: latitude_must_be_between_-90_and_90
- Promotion status: not promoted to a scenario profile
