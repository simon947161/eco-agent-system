# Task2021–2026 — First Implementation Slice Report

Status: `LOCAL_SKELETON_IMPLEMENTED / PUBLIC_DATA_NOT_RETRIEVED`

## Delivered controls

- fixed, git-ignored workspace under
  `runtime_data/qgis/cooma_spatial_foundation/`;
- new-file-only project creation and changed-contract overwrite refusal;
- explicit source/derived-data separation;
- metadata-only public source registry with licence uncertainty preserved;
- provisional Cooma scope contract;
- QGIS project generator and independent reopen verifier;
- required layer-group and bookmark contracts;
- visible no-data and Founder-Gate prompts inside the layer tree;
- Chinese 10-minute restart guide;
- spatial observation template with `scientific_conclusion: NONE`;
- unit tests using temporary synthetic directories only.

## Local workspace structure

```text
runtime_data/qgis/cooma_spatial_foundation/
├── project/
├── source_data/
├── derived_data/
├── styles/
├── exports/
├── notes/
└── manifests/
```

The generated `.qgz`, isolated QGIS profile and local manifests remain ignored
runtime material. Only source contracts, generator code, documentation and
synthetic tests belong in Git.

## Project contract

Project: `Cooma_Spatial_Foundation_v0_1.qgz`

Groups:

1. `00_START_HERE`
2. `01_BOUNDARIES`
3. `02_TERRAIN`
4. `03_WATER`
5. `04_SETTLEMENT_AND_ROADS`
6. `05_CLIMATE_STATIONS`
7. `06_PUBLIC_INFRASTRUCTURE_LATER`
8. `07_EVIDENCE_NOTES`
9. `90_SOURCE_METADATA`
10. `99_DISABLED_LATER_LAYERS`

Bookmarks: `Cooma Town`, `Wider Cooma Context`, `Terrain Overview`,
`Main Waterways`, and `Catchment Context`.

The project contains zero data layers. Bookmarks are provisional navigation
aids. Terrain, water and other groups are intentionally empty until a separate
bounded retrieval approval.

## Retrieval and derivation ledger

| Item | Result |
|---|---|
| Spatial datasets downloaded | 0 |
| DEM/raster tiles downloaded | 0 |
| Vector features downloaded | 0 |
| GeoPackage/Shapefile created | 0 |
| Hillshade created | 0 |
| Slope created | 0 |
| Hydrology derived | 0 |
| Scientific conclusions | 0 |

## Known pre-flight risk

The installed `python-qgis-ltr.bat` does not by itself register all Qt DLL
directories in this environment. The repository launcher explicitly registers
the QGIS, Qt5, Python and OSGeo4W DLL directories and is the supported local
entry. This is an environment lifecycle contract, not a modification to QGIS.
