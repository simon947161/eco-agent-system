# Task2031-2040 QGIS Cooma Terrain and Administrative Boundary Pack Report

Status: `READY_FOR_FOUNDER_QGIS_TERRAIN_REVIEW / BOUNDED_PUBLIC_DATA / TERRAIN_OBSERVATION_ONLY / NO_SCIENTIFIC_CONCLUSION / DO_NOT_AUTO_MERGE`

## Scope and governance result

- PR #94 was verified at the authorized head `22575d7996ab89dade2d85e1edbb4187e74c2cfe`, with a clean merge state and successful required checks, then merged by merge commit `a543b104e5951f61fbfc527414b82765325bb738`.
- `main` and `origin/main` were both verified at `a543b104e5951f61fbfc527414b82765325bb738` before the terrain branch was created.
- Work was isolated on `agent/task2031-2040-qgis-cooma-terrain-boundary-pack`.
- Only the two Founder-authorized public sources were retrieved. No hydrology, roads, climate stations, infrastructure, imagery, or other public spatial data was downloaded.
- `prototype/` was not read, modified, staged, or committed.
- Runtime rasters, GeoJSON, QGZ, receipts, manifests, and QGIS profiles remain under the git-ignored local runtime workspace. They are not repository payload.
- No scientific, hydrological, risk, engineering, drought, fire, infrastructure, or building-scale conclusion is formed.

## Exact public sources

### NSW administrative boundary

- Publisher: NSW Spatial Services / Department of Customer Service
- Product: `NSW Foundation Spatial Data Framework - Administrative Boundaries - Suburb`
- Service layer: `NSW_Administrative_Boundaries_Theme_multiCRS`, FeatureServer layer 2 `Suburb`
- Closed query: `suburbname='COOMA'`, one GeoJSON feature, output CRS `EPSG:7844`
- Exact identity: `OBJECTID=16701`, `cadid=108029985`, `shapeuuid=42bcb472-a4e4-30cd-a949-077681669ffd`, `suburbname=COOMA`
- Licence: Creative Commons Attribution
- Retained file size: `36,947 bytes`
- SHA-256: `d71195670ec46ad99b1b79e5283c240fd8a92f5f8d38e219d6785aef0e8e13e9`

### Geoscience Australia elevation

- Publisher: Geoscience Australia
- Product: `GA SRTM 1 second Smoothed DEM (DEM-S) version 1.0`
- Product ID: `ga_srtm_dem1sv1_0`; catalogue ID: `72759`
- Closed source object: `dems1sv1_0.tif`
- Source CRS: `EPSG:4326`; vertical datum: `EGM96`; nominal cell size: one arc-second, approximately 30 metres
- Licence: Creative Commons Attribution 4.0 International
- Retrieval method: GDAL `/vsicurl/` range read cropped to the authorized bounding box; the 38.3 GB national source object was not downloaded
- Measured unique HTTP range bytes: `10,523,984 bytes`
- Retained bounded DEM size: `3,160,953 bytes`
- Retained bounded DEM SHA-256: `9064834f0cc231cebbc6908555f1838e8edd123c717f4d61457d5b68ab9e0b1b`
- Retained bounded DEM dimensions and observed raster range: `1273 x 1078`, `709.0745849609375 to 1237.71728515625 m`

## Authorized extent

The retrieval extent is the official COOMA locality polygon plus a 10,000 metre projected buffer.

- Longitude/latitude bounds: west `148.93596282232357`, east `149.28924950629394`, south `-36.39777068570377`, north `-36.09861165255777`
- EPSG:7855 bounds: west `673874.0292297722`, east `705782.3523817627`, south `5969790.319669124`, north `6002993.464142044`
- Width: `31,908.32315199054 m`
- Height: `33,203.144472920336 m`
- Buffered polygon area: `831.8529661775686 km2`

The extent is a retrieval and orientation boundary only. It is not a catchment, hydrological boundary, risk zone, or final scientific study boundary.

## Derived terrain products

All products were derived with GDAL `3.13.0 "Iowa City"`, target CRS `GDA2020 / MGA zone 55 (EPSG:7855)`, and 30 metre target cells.

| Product | Method | Size | SHA-256 | Observed raster range |
| --- | --- | ---: | --- | --- |
| Projected DEM | `gdalwarp`, bilinear, target-aligned, cut to buffered extent | 2,181,010 B | `01f8a50af0396d89c89477aaed61f186ea82237ed5a962b76c01e3f42a6f40d8` | 709.109619140625-1175.8284912109375 m |
| Hillshade | `gdaldem hillshade`, azimuth 315 degrees, altitude 45 degrees, z=1, compute edges | 550,776 B | `423da3c3f1970cfbbd2333bc36b9566023cad37d2d076d686cca3dd02876d39f` | 30-252 |
| Slope | `gdaldem slope`, Horn, degrees, metre horizontal and EGM96 metre vertical units, compute edges | 3,014,157 B | `4fd67659b6ddfa3e3f8a51e681e8e3a57255a3f8e21c284e37c0528df75a65ce` | 0.004736830946058035-47.02226257324219 degrees |

Contours were intentionally omitted to keep the pack lightweight. No terrain value was converted into a hazard or risk class.

## Local workspace and QGIS project

- Source-data total: `3,197,900 bytes`
- Derived-data total: `5,758,963 bytes`
- Complete local workspace total: `11,899,573 bytes`
- Workspace limit remains enforced at runtime; QGIS profiles account for the remaining local-only workspace files.
- Project: `runtime_data/qgis/cooma_spatial_foundation/project/Cooma_Spatial_Foundation_v0_2_terrain.qgz`
- Project SHA-256: `d68b4016c8086ec44e9cc8001a8d972c5010953e17c06ddf36fd599e6ddbb17c`
- Project CRS: `EPSG:7855`
- Network basemaps/providers: `0`
- Broken layers: `0`
- Official boundary features: `1`
- Hydrology: `NOT_AUTHORIZED_NOT_RETRIEVED`
- Scientific conclusion: `NONE`

Default presentation keeps the official locality boundary and hillshade visible, with DEM and slope available but off. The project contains `Cooma Locality` and `Cooma + 10 km Terrain` bookmarks.

## Windows QGIS manual validation

QGIS Desktop `3.44.11` successfully opened the QGZ. The title, `EPSG:7855` project CRS, official boundary, local hillshade, and required layer groups rendered without a broken-layer or network error.

- Hillshade default rendering: PASS
- Slope toggle and green degree styling: PASS
- `Cooma Locality` bookmark: PASS; displayed scale approximately `1:87,710`
- `Cooma + 10 km Terrain` bookmark: PASS; displayed scale approximately `1:220,549`
- DEM Identify Features sample: PASS; `753.27386 m`
- Slope Identify Features sample: PASS; `1.374641 degrees`
- Review-only visibility and bookmark changes were discarded on close; the QGZ was not saved from the UI

The QGIS process on this Windows installation can leave a windowless residual process after GUI close. This did not alter the QGZ or any source/derived artifact and is recorded as an application lifecycle observation, not a pack data failure.

## Automated validation

- Terrain-pack suite: `24 tests`, PASS
- Complete repository suite: `387 tests`, PASS, `1 skipped`
- Python compile validation: PASS
- `git diff --check`: PASS

The automated verifier reopens the QGZ using the QGIS API, validates all local layers, confirms relative paths, checks the two retained-source/three-derived checksums, rejects web providers, enforces size ceilings and new-file-only behavior, and confirms `scientific_conclusion=NONE`.

## Independent Founder Gate

Recommendation:

`READY_FOR_FOUNDER_QGIS_TERRAIN_REVIEW / BOUNDED_PUBLIC_DATA / TERRAIN_OBSERVATION_ONLY / NO_SCIENTIFIC_CONCLUSION / DO_NOT_AUTO_MERGE`

The terrain-pack pull request must remain Draft. Founder review is required before any merge or any authorization for hydrology, additional datasets, analysis, or conclusions.
