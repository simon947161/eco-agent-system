# Evidence Review Pack Builder

## Purpose

The Evidence Review Pack is the technical counterpart to the Task 45 Scenario
Summary Pack. It gives planners, researchers, consultants, environmental
reviewers, and professional collaborators one structured view of available
evidence, provenance, uncertainty, missing information, and validation needs.

It reduces external-facing complexity without replacing detailed runtime
artifacts. Source files remain available for audit, testing, and specialist
inspection.

## Local Use

From the repository root:

```bash
python cczps_lite/engine/evidence_review_pack.py
```

Windows users may replace `python` with `py`.

The builder writes:

```text
cczps_lite/output/consolidated/evidence_review_pack.json
cczps_lite/output/consolidated/evidence_review_pack.md
```

The existing consolidated directory is reused, or created when absent.

## Local Data Sources

The builder reads available local copies of:

- `meteorology_evidence.json`
- `location_meteorology_evidence.json`
- `meteorology_timeseries.json`
- `meteorology_trends.json`
- `spatial_transect_scenario_pack.json`
- `gis_dem_access_plan.json`
- `planning_hypotheses.json`
- `evidence_traceability.json`
- `professional_validation_interface.json`
- `planning_approval_support_report.json`
- `consolidated/scenario_summary_pack.json`

The Scenario Summary Pack supplies the scenario directory and identity only.
Task 46 does not duplicate its full general-user narrative.

## Evidence Coverage

The pack uses conservative coverage states:

```text
available
partially_available
planning_only
not_generated
not_available
insufficient_evidence
requires_further_review
```

`available` means a local source record can be referenced. It does not mean
that the evidence is scientifically confirmed or professionally accepted.

Configured transects remain configured spatial context. A GIS / DEM access
plan remains `planning_only`; it is not treated as acquired, processed,
field-verified, or professionally reviewed spatial evidence.

Missing optional files do not stop generation. Missing or incomplete evidence
defaults to conservative states, insufficient evidence strength, high
uncertainty, and further review.

## Minimal Core Model

Task 44 defines the minimal core model in
`CCZPS_LITE_MINIMAL_CORE_MODEL_AND_OUTPUT_CONSOLIDATION_PLAN.md`.

The Evidence Review Pack applies it as:

```text
Scenario -> scenario identity and context
Evidence -> meteorology, trends, spatial context, GIS / DEM status, traceability
Hypothesis -> evidence references supporting planning hypotheses
Review -> professional validation and missing review status
Report -> technical evidence review package
```

## Review Boundary

Every record remains:

```text
evidence_review_status = requires_further_review
human_review_required = true
professional_review_required = true
approval_support_status = not_ready_for_approval
```

The pack preserves traceability identifiers and professional validation
states. It does not increase evidence strength or confidence.

## Safety Boundary

The builder only organises, cross-references, and explains existing local
outputs. It adds no environmental analysis, meteorology calculation, GIS /
DEM runtime, planning hypothesis logic, governance decision logic, scenario
comparison logic, geocoding, simulation, API call, language-model call,
scientific confirmation, professional certification, engineering or
regulatory conclusion, approval decision, recommendation, investment advice,
or scenario ranking.

## Dashboard

Task 46 does not change the dashboard. A later dashboard simplification task
may link to the local consolidated output without adding browser-side API
calls, external dependencies, or a dashboard redesign.
