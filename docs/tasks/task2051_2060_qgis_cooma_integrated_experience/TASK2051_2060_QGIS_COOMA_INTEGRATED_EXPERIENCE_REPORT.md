# Task2051–2060 QGIS Cooma Integrated Experience Report

## Outcome

Task2051–2060 establishes one primary Cooma QGIS project containing the accepted
Terrain and Hydrology layers plus bounded NSW official roads and optional NSW
aerial imagery. The user model is **one project, many independently switchable
layers**. Scientific and engineering conclusion: **NONE**.

## Task allocation

| Task | Result |
|---|---|
| 2051 | Freeze accepted `main@4ed5afc98d547acb1cddb688fdca53c9a5fc975e` as the integration base |
| 2052 | Close the NSW official RoadSegment source and Cooma +10 km retrieval boundary |
| 2053 | Add paginated, bounded, new-file-only road retrieval with byte ceilings |
| 2054 | Reproject and clip road vectors to EPSG:7855 and the accepted study extent |
| 2055 | Close the exact NSWWebImagery cached tile service as the only online layer |
| 2056 | Build `Cooma_Spatial_Foundation_v0_4_integrated.qgz` from accepted v0.3 |
| 2057 | Add one PowerShell launcher for plan/retrieve/derive/build/verify/open |
| 2058 | Add experience, source, path, network and non-conclusion tests |
| 2059 | Add Founder review guide for layer order, visibility, Identify and offline behaviour |
| 2060 | Return an independent Founder QGIS Integrated Review Gate |

## Single-project structure

The integrated project inherits all accepted v0.3 layers and bookmarks. It adds
both new layers to the existing `04_SETTLEMENT_AND_ROADS` group:

1. `Roads — NSW official RoadSegment`
2. `Aerial imagery — NSWWebImagery — online`

The complete project therefore contains:

- Cooma official locality boundary;
- bounded DEM;
- hillshade;
- slope in degrees;
- main watercourses;
- secondary streams;
- contracted catchments;
- stream-segment catchments;
- named water features;
- bounded official road segments;
- online NSW aerial imagery;
- source and limitation information layers.

Old v0.2 and v0.3 projects remain as immutable stage artefacts. The v0.4 project
is the intended daily entry point once Founder review passes.

## Default visibility and layer order

The default view prioritises readability rather than switching every layer on:

- ON: NSW aerial imagery;
- ON: NSW official roads;
- ON: Cooma locality boundary;
- ON: main watercourses;
- ON: named water features;
- OFF but present: DEM, hillshade, slope, secondary streams, catchments and
  stream-segment catchments.

The imagery is the visual base. Roads and accepted evidence layers render above
it. Every layer can be enabled or disabled independently in QGIS.

## Official roads

- Publisher: NSW Spatial Services
- Product: NSW Foundation Spatial Data Framework — Transport Theme
- Layer: `RoadSegment`, FeatureServer layer 5
- Geometry: polyline
- Service capability: query
- Bounded extent: accepted official Cooma locality plus 10 km only
- Retrieval: ordered, paginated GeoJSON queries; no statewide export
- Retained runtime form: raw bounded GeoJSON plus clipped EPSG:7855 GeoPackage
- Git policy: runtime vectors are not committed
- Identify fields include official road name, function hierarchy, surface,
  operational status and related source attributes where populated.

## Official imagery

- Publisher: NSW Spatial Services
- Product: NSWWebImagery
- Service: cached ArcGIS MapServer tiles
- CRS: EPSG:3857
- Available levels: 0–23 as declared by the service
- Runtime mode: online display only
- Bulk download: prohibited by this implementation
- Git policy: no tiles or imagery cache committed

The imagery layer supports visual orientation. It is not treated as a dated
scientific observation unless later metadata work establishes capture date and
fitness for a specific use.

## Online and offline behaviour

With network access, the v0.4 project displays the exact NSWWebImagery service.
Without network access, imagery may be blank or unavailable, but the accepted
Terrain, Hydrology and bounded official roads remain local and usable. The
project contains only one online layer.

## Integrated bookmarks

1. `Integrated Cooma Overview`
2. `Satellite and Roads`
3. `Terrain and Water Together`

All accepted terrain and hydrology bookmarks are retained.

## Build and open workflow

From the repository root in PowerShell:

```powershell
.\run_qgis_cooma_integrated_experience.ps1 -Action Plan -OsgeoRoot D:\
.\run_qgis_cooma_integrated_experience.ps1 -Action Retrieve -OsgeoRoot D:\
.\run_qgis_cooma_integrated_experience.ps1 -Action Derive -OsgeoRoot D:\
.\run_qgis_cooma_integrated_experience.ps1 -Action BuildProject -OsgeoRoot D:\
.\run_qgis_cooma_integrated_experience.ps1 -Action Verify -OsgeoRoot D:\
.\run_qgis_cooma_integrated_experience.ps1 -Action Open -OsgeoRoot D:\
```

The generated project path is:

```text
runtime_data/qgis/cooma_spatial_foundation/project/Cooma_Spatial_Foundation_v0_4_integrated.qgz
```

## Safety and scope

- accepted Terrain and Hydrology project is inherited, not rewritten;
- exact Cooma +10 km extent is reused;
- road retrieval is bounded and paginated;
- imagery is one allowlisted online reference layer;
- runtime spatial data remains ignored by Git;
- `prototype/` is untouched;
- no flood, water-quality, transport-safety, access, engineering, planning,
  bushfire, ecological or other scientific conclusion is made;
- Draft PR and independent Founder Gate remain required.

## Gate

```text
READY_FOR_TECHNICAL_VALIDATION
/ THEN_FOUNDER_QGIS_INTEGRATED_REVIEW
/ ONE_PROJECT_MANY_LAYERS
/ BOUNDED_OFFICIAL_ROADS
/ OPTIONAL_OFFICIAL_ONLINE_IMAGERY
/ NO_SCIENTIFIC_CONCLUSION
/ DO_NOT_AUTO_MERGE
```
