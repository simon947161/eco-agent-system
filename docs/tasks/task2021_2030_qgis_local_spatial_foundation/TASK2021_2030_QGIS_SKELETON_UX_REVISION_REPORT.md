# Task2021-2030 QGIS Skeleton UX Revision Report

Status: `READY_FOR_FOUNDER_QGIS_SKELETON_RETEST`

Boundary: `SYNTHETIC_NAVIGATION_ANCHOR / NO_PUBLIC_DATA_RETRIEVAL / NO_SCIENTIFIC_CONCLUSION / DO_NOT_AUTO_MERGE`

## Founder issues and root causes

The first skeleton opened without an immediately readable spatial anchor, its five bookmarks used the same extent, empty future-data groups looked broken rather than intentionally empty, and the restart guide did not make the recovery path sufficiently concrete for a returning GIS learner.

The root causes were presentation and onboarding gaps, not missing scientific data: the project contained only structural notes, bookmark extents were duplicated, empty groups had no visible explanation, and the guide did not clearly distinguish viewing an existing bookmark from creating a new bookmark.

## Revision delivered

- A new revision-safe project is generated as `Cooma_Spatial_Foundation_v0_1_ux_revision.qgz`; the original project is not overwritten.
- A synthetic point and rectangular learning extent provide an immediate Cooma-oriented navigation anchor.
- Both spatial anchors are explicitly marked `SYNTHETIC_NAVIGATION_ANCHOR`, `NOT_EVIDENCE`, `PROVISIONAL`, and `LEARNING_AND_NAVIGATION_ONLY`.
- The learning extent additionally states `NOT_A_CATCHMENT_COUNCIL_OR_SCIENTIFIC_BOUNDARY`.
- Five project bookmarks have distinct provisional navigation extents: Cooma Town, Wider Cooma Context, Terrain Overview, Main Waterways, and Catchment Context.
- `02_TERRAIN` and `03_WATER` contain visible INFO layers explaining that data has not yet been retrieved.
- `00_START_HERE` contains a visible learning-guide layer.
- Later data groups remain disabled by default.
- The 10-minute restart guide now gives explicit panel, bookmark, navigation, Identify, and safe-exit instructions.

## Runtime verification

- Local revision project: `runtime_data/qgis/cooma_spatial_foundation/project/Cooma_Spatial_Foundation_v0_1_ux_revision.qgz`
- Revision SHA-256: `3573dd052fd3cf62de27d049147e3352611768362056c0879e67c014920b4065`
- Synthetic layer count: 5
- Broken layer count: 0
- Network basemap count: 0
- Public spatial data download count: 0
- Derived scientific layer count: 0
- Source-data file count: 0
- Derived-data file count: 0

The generated project and synthetic GeoJSON files remain under ignored `runtime_data/` and are excluded from Git.

## Automated validation

- QGIS foundation tests: 20 passed.
- Full repository tests: 363 passed, 1 skipped, 0 failures, 0 errors.
- Python compile validation: passed.
- Project round-trip, relative-path, default-extent, bookmark, controlled-provider, no-network, and empty-data-boundary verification: passed.

## Manual Windows QGIS validation

Validated with QGIS Desktop 3.44.11-Solothurn on Windows:

1. Closed the prior project and explicitly discarded its unrelated unsaved UI state.
2. Opened the revision-safe project in a clean QGIS session.
3. Confirmed the provisional centre, learning extent, START HERE layer, terrain INFO layer, hydrology INFO layer, and disabled future groups were visible and understandable.
4. Confirmed all five project bookmarks were discoverable under the provisional navigation bookmark group.
5. Activated `Cooma Town` and `Wider Cooma Context`; the canvas changed from approximately 1:26,422 to 1:273,130.
6. Confirmed mouse-wheel zoom and map-pan interaction.
7. Used Identify on the point and polygon; both exposed the required synthetic/not-evidence/provisional fields, and the polygon exposed the non-scientific-boundary warning.
8. Closed QGIS, restarted it, and reopened the revision from Recent Projects.
9. Confirmed the project reopened with the spatial anchor visible and without broken-layer or repeated-error dialogs.
10. Closed QGIS cleanly after validation.

## Included and excluded scope

Included: generator code, synthetic-anchor contract, safety verification, launcher, tests, Founder guidance, and governance documentation.

Excluded: real DEM, hydrology, catchment, station, road, infrastructure, or other public spatial data; network basemaps; real observations; scientific analysis; annual reporting; and any change to `prototype/`.

## Gate

Founder Gate recommendation: `READY_FOR_FOUNDER_QGIS_SKELETON_RETEST`.

This is a retest gate only. The Draft PR must not be automatically merged.
