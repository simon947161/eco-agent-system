# QGIS Cooma Terrain Review Guide

Status: `BOUNDED_PUBLIC_DATA / TERRAIN_OBSERVATION_ONLY / NO_SCIENTIFIC_CONCLUSION`

## Open the project

Open the local project:

`runtime_data/qgis/cooma_spatial_foundation/project/Cooma_Spatial_Foundation_v0_2_terrain.qgz`

The project should open without a network connection because every active layer is a local file. No web basemap is configured.

## What the layers mean

- `Cooma Locality Boundary — NSW official source` is the gazetted NSW locality/suburb feature named COOMA. It is not the Snowy Monaro LGA, a catchment, a hydrological boundary, or a final scientific study boundary.
- `Cooma DEM — GA SRTM 1-second — bounded` is the retained bounded source elevation surface, reprojected to the metric project grid for use in QGIS.
- `Cooma Hillshade — derived from bounded GA DEM` is a visual relief rendering.
- `Cooma Slope Degrees — derived` reports local slope angle in degrees. It is not a hazard, engineering, access, erosion, fire, or risk classification.
- `INFO — Hydrology data not yet retrieved` remains visible because hydrology is outside this authorization.

This DEM supports regional terrain observation.
It does not provide building-scale detail and is not equivalent to aerial imagery.

## Five-minute review

1. Confirm the project CRS is `GDA2020 / MGA zone 55 (EPSG:7855)`.
2. In `01_BOUNDARIES`, confirm the Cooma locality outline is visible but not dominant.
3. In `02_TERRAIN`, leave hillshade on and toggle slope on and off.
4. Toggle the DEM on only when identifying an approximate elevation cell.
5. Use Identify Features on one DEM cell and one slope cell.
6. Open Project Bookmarks and activate `Cooma Locality` and `Cooma + 10 km Terrain`.
7. Confirm scale and coordinates remain visible while panning and zooming.

## Safe interpretation

Permitted: describe visible elevation, relief, ridge/valley form, and slope variation as observations from this bounded terrain surface.

Not permitted: infer drought, fire danger, catchment function, water security, wastewater performance, infrastructure suitability, building-scale elevation, or engineering conclusions.

Close QGIS without saving review-only UI changes. Normal reopen must not retrieve data.
