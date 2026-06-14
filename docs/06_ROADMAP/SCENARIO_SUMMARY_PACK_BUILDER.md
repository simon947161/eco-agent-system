# Scenario Summary Pack Builder

## Purpose

The Scenario Summary Pack is the first external-facing consolidated output in
the CCZPS-Lite v0.6 Minimal Core Sprint. It gives normal users, project
partners, local government officers, community stakeholders, and
non-technical collaborators one cautious summary for each available scenario
or intake profile.

It reduces the need to read many separate JSON and Markdown files. Detailed
runtime artifacts remain available for audit, testing, provenance, and
specialist review.

## Local Use

From the repository root:

```bash
python cczps_lite/engine/scenario_summary_pack.py
```

Windows users may replace `python` with `py`.

The builder writes:

```text
cczps_lite/output/consolidated/scenario_summary_pack.json
cczps_lite/output/consolidated/scenario_summary_pack.md
```

The output directory is created when it does not already exist.

## Local Data Sources

The builder reads available local copies of:

- `location_intake_profiles.json`
- `location_meteorology_evidence.json`
- `meteorology_evidence.json`
- `meteorology_trends.json`
- `planning_hypotheses.json`
- `evidence_traceability.json`
- `governance_decision_records.json`
- `scenario_comparison.json`
- `planning_approval_support_report.json`

Optional missing files do not stop generation. Relevant fields remain
`not_available`, `not_generated`, `insufficient_evidence`, or
`requires_further_review`, depending on the available source records.

## Minimal Core Model

Task 44 defines the minimal core model in
`CCZPS_LITE_MINIMAL_CORE_MODEL_AND_OUTPUT_CONSOLIDATION_PLAN.md`.

The Scenario Summary Pack applies it as:

```text
Scenario -> scenario identity and context
Evidence -> current evidence summary
Hypothesis -> planning hypothesis summary
Review -> human, professional, and governance status
Report -> plain-language scenario summary
```

The pack is a Report assembled from the other four objects. It does not create
a parallel scenario system.

## Status Preservation

The builder preserves conservative source states and defaults to review
required when an optional source is absent.

Every generated scenario record remains:

```text
human_review_required = true
professional_review_required = true
approval_support_status = not_ready_for_approval
```

The pack does not rank scenarios, identify a winner, upgrade approval status,
or produce a final recommendation.

## Summary Boundary

The builder only consolidates, translates, and reorganises existing local
outputs. It adds no environmental analysis, planning hypothesis logic,
governance decision logic, scenario comparison logic, GIS / DEM runtime,
geocoding, simulation, API call, language-model call, professional
certification, engineering conclusion, regulatory conclusion, investment
advice, approval decision, or recommendation.

The generated Markdown uses plain language, but simpler wording does not
increase the strength or authority of the underlying evidence.

## Dashboard

Task 45 does not change the dashboard. This keeps the first consolidated pack
focused on deterministic generation and compatibility. A later dashboard
simplification task can read the local consolidated JSON without adding
browser-side API calls or redesigning the current dashboard prematurely.
