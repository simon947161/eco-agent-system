# Governed Location-to-Meteorology Pipeline

## Purpose

Task 43 connects valid Task 42 intake profiles to the existing governed NASA
POWER meteorology path:

```text
Location intake
-> Usage and Cost Governance
-> Budget Guard
-> Cache-first meteorology retrieval
-> Separate intake-location evidence output
```

This answers only whether a valid intake location can receive governed
meteorology evidence. It does not assess site suitability or create a planning
conclusion.

## Local Use

From the repository root:

```bash
python cczps_lite/engine/location_meteorology_pipeline.py \
  --date 20250501 \
  --manual-approval
```

Multiple dates and selected intake IDs are supported:

```bash
python cczps_lite/engine/location_meteorology_pipeline.py \
  --dates 20250501,20250508,20250515 \
  --selected-intake-ids tumut_nsw_intake \
  --manual-approval
```

Windows users may replace `python` with `py`.

## Manual Approval

Live retrieval requires the explicit `--manual-approval` flag. Without it,
uncached records are marked `manual_approval_required` and no NASA POWER call
occurs.

Cache hits remain readable without live approval because they consume no
external resource. Their output records `from_cache: true` and
`usage_governance_status: cache_only`.

## Governance And Budget Guard

Each selected location/date pair receives its own Usage and Cost Governance and
Budget Guard result. Uncached call accounting uses the complete number of
selected uncached location/date pairs.

The runtime allows at most five locations and ten dates per run. These limits
are checked before retrieval. If any pair returns `stop_required`, all remaining
uncached pairs are marked blocked or not retrieved. Later cache hits may still
be read because they do not create live calls.

## Cache-First Behavior

The pipeline reuses the existing `meteorology_cache.json` key format:

```text
scenario_id|YYYYMMDD
```

It also reuses the existing NASA POWER fetch and parsing functions. Task 43 does
not create a second meteorology connector.

## Outputs

The separate evidence-only outputs are:

- `cczps_lite/output/location_meteorology_evidence.json`
- `cczps_lite/output/location_meteorology_evidence.md`

Intake locations are not appended to permanent scenario packs, planning
hypotheses, governance decisions, approval-support records, or the existing
meteorology time-series store. Trend status remains `not_generated`.

## Manual Workflow

`Location Meteorology Refresh` is a `workflow_dispatch`-only action. It requires
manual approval before running and supports optional selected intake IDs,
force-refresh, artifact download, and tightly allowlisted output commits.

There is no cron, schedule, or automatic refresh.

## Evidence Boundary

The pipeline adds meteorology evidence only. Every result remains
`not_ready_for_approval`, with human and professional review required.

It adds no geocoding, map UI, location discovery, GIS / DEM runtime, hydrology,
wind or satellite analysis, simulation, language-model call, automatic planning
hypothesis, approval decision, engineering decision, or recommendation.

A future Task 44 may connect manually governed GIS / DEM profiles without
changing this evidence-only boundary.
