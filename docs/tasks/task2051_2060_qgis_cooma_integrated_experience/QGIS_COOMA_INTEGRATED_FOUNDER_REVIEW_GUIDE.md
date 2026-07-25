# QGIS Cooma Integrated Founder Review Guide

## Purpose

Confirm that the new v0.4 file behaves as **one project with many layers**, not
as another disconnected map. This review checks usability and source behaviour;
it does not make scientific or engineering conclusions.

## Open the one primary project

```powershell
cd D:\Codex\ClimateOS\eco-agent-system-codex-working
.\run_qgis_cooma_integrated_experience.ps1 -Action Open -OsgeoRoot D:\
```

Expected title:

```text
Cooma Spatial Foundation v0.4 Integrated
```

## Review A — one-project completeness

In the Layers panel confirm the same project contains:

- Boundary;
- DEM, Hillshade and Slope;
- Main and Secondary Watercourses;
- Catchment and Subcatchment Context;
- Named Water Features;
- NSW official Roads;
- NSW online Aerial Imagery.

Pass phrase:

```text
INTEGRATED_ONE_PROJECT_COMPLETE_PASS
```

## Review B — default readability and ordering

On first open, imagery should sit at the visual bottom. Roads, boundary, main
watercourses and named water features should be visible above it. DEM, hillshade,
slope, secondary streams and catchment polygons should be present but off.

Toggle layers individually and confirm one layer does not remove or replace the
others. The map should remain readable rather than showing every analytical
surface at once.

Pass phrase:

```text
INTEGRATED_LAYER_ORDER_VISIBILITY_PASS
```

## Review C — satellite and road experience

1. Click `Satellite and Roads` bookmark.
2. Confirm aerial imagery loads when internet is available.
3. Toggle aerial imagery off and on.
4. Toggle official roads off and on.
5. Select the Roads layer and use Identify on several road segments.
6. Confirm non-empty official attributes appear, such as road name,
   function hierarchy, surface or operational status where populated.

Imagery is visual reference only. Do not infer capture date, land-cover change or
current site condition from this review.

Pass phrase:

```text
INTEGRATED_IMAGERY_ROADS_PASS
```

## Review D — combined terrain and water experience

1. Click `Terrain and Water Together` bookmark.
2. Toggle Hillshade on and imagery off.
3. Confirm roads and main watercourses remain distinguishable.
4. Toggle Slope on, then off.
5. Toggle Catchment Context on, then off.
6. Confirm the existing DEM, Slope, watercourse and catchment Identify functions
   remain available.

Pass phrase:

```text
INTEGRATED_TERRAIN_HYDROLOGY_PASS
```

## Review E — bookmarks, CRS and offline core

Confirm:

- all three new integrated bookmarks respond;
- accepted terrain and hydrology bookmarks remain available;
- project CRS shows EPSG:7855;
- if imagery is unavailable or manually disabled, Terrain, Hydrology and Roads
  remain visible and usable from local runtime data;
- no broken-layer red exclamation mark appears for local layers.

Pass phrase:

```text
INTEGRATED_BOOKMARK_CRS_OFFLINE_CORE_PASS
```

## Founder review result

Only after all five pass phrases are recorded may the review be closed as:

```text
FOUNDER_QGIS_INTEGRATED_REVIEW_PASS
```

A review pass is not merge authorization. The Draft PR must remain unmerged until
the Founder separately authorizes merging.
