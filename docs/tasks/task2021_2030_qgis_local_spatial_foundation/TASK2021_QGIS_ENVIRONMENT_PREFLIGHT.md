# Task2021 — QGIS Environment Pre-flight Record

Status: `PASS_WITH_DOCUMENTED_LAUNCH_CONTRACT`

Recorded: 2026-07-20 (Australia/Sydney)

## Repository identity

| Check | Observed result |
|---|---|
| Repository | `D:\Codex\ClimateOS\eco-agent-system-codex-working` |
| Origin | `https://github.com/simon947161/eco-agent-system.git` |
| Authoritative baseline branch | `main` |
| Baseline local HEAD | `8db70d7e96c0e4ff331fd465ce646d46f663925e` |
| Fetched `origin/main` | `8db70d7e96c0e4ff331fd465ce646d46f663925e` |
| Implementation branch | `agent/task2021-2030-qgis-local-spatial-foundation` |
| Existing exception | untracked `prototype/`; content not opened, and directory not modified, moved, deleted or staged |

The branch was created only after a fresh `git fetch origin` and exact baseline
alignment. PR #92 was already merged. No new PR was created or merged.

## QGIS environment

| Component | Verified value |
|---|---|
| QGIS Desktop | `3.44.11-Solothurn` (`f8f5812197f`) |
| Desktop executable | `D:\bin\qgis-ltr-bin.exe` |
| QGIS prefix | `D:\apps\qgis-ltr` |
| QGIS-bundled Python | `3.12.13` at `D:\bin\python.exe` |
| GDAL/OGR | `3.13.0` |
| PROJ | `9.8.1`; EPSG registry `v12.029 (2025-10-02)` |
| Qt | `5.15.13` |
| GEOS | `3.14.1-CAPI-1.20.5` |
| SQLite reported by QGIS | `3.53.0` |
| Desktop state at authorization | `Untitled Project — QGIS`, running and responsive |

`qgis_process-qgis-ltr.bat --version` verified the bundled Python, GDAL and
PROJ stack. The stock `python-qgis-ltr.bat` did not independently discover Qt
DLLs in this Windows environment. Importing `qgis.core` succeeds when the
OSGeo4W `bin`, QGIS, Qt5 and Python DLL directories are registered explicitly.
The repository launcher preserves that exact local contract without changing
the system installation.

## Controlled local workspace

The authorized path is:

`runtime_data/qgis/cooma_spatial_foundation/`

The repository's existing `.gitignore` ignores `runtime_data/`. The workspace
creator is fixed to this path in production, rejects symlink components,
creates only named subdirectories, and refuses to overwrite a changed contract
or existing QGIS project.

## Safety observations

- Founder private GIS files were not accessed.
- Git status/path enumeration saw the pre-existing `prototype/` path only; its
  file contents were not opened and no command targeted it for writing.
- Council non-public, customer and personal data were not accessed.
- No spatial dataset, tile, feature service response or weather observation was downloaded.
- No DEM, GeoPackage, Shapefile, hillshade, slope or hydrology result was created.
- No Cooma scientific, operational or engineering conclusion was formed.
- The earlier planning-only roadmap is superseded only for this specifically
  authorized local skeleton; its evidence and human-review boundaries remain.

## Pre-flight judgment

`READY_FOR_EMPTY_SYNTHETIC_PROJECT_SKELETON / NO_PUBLIC_DATA_RETRIEVAL`
