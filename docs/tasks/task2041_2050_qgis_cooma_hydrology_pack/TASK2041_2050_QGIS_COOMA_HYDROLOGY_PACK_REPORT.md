# Task2041–2050 QGIS Cooma Hydrology Pack Report

## Result

The bounded Cooma Hydrology Pack is technically review-ready as stacked work on
the unmerged terrain branch. It is a local spatial-orientation and GIS-relearning
artifact only. Scientific conclusion: **NONE**.

## Git and stacking

- PR #95 state at authorization: `OPEN / DRAFT / NOT MERGED`
- exact terrain Head used: `57e71468514253c188c9a744e3532a67903b0272`
- hydrology branch: `agent/task2041-2050-qgis-cooma-hydrology-pack`
- required stacked base: `agent/task2031-2040-qgis-cooma-terrain-boundary-pack`
- neither PR is authorized for automatic merge.

## Official source decision

- Publisher: Commonwealth of Australia, Bureau of Meteorology
- Product: Australian Hydrological Geospatial Fabric (Geofabric)
- Version: V3.3
- Service: `Geofabric_V3x_All_Products` FeatureServer through AWDS
- Licence: Creative Commons Attribution 4.0 International (CC BY 4.0)
- Requested attribution: `© Commonwealth of Australia (Bureau of Meteorology) 2022`
- Source CRS: EPSG:4283 (GDA94)
- Access method: bounded ArcGIS FeatureServer GeoJSON queries
- Approximate foundation scale: 1:100,000; individual service-layer scale rules vary
- Currency statement: V3.3 service with BOM 2022 attribution; documented inputs
  include ANUDEM 5.3.0 dated 3 November 2016 and AusHydro V2.
- NSW Spatial Services fallback was not used or combined.

Exact layers:

| ID | Product component | Layer | Raw features | Raw bytes | SHA-256 |
|---:|---|---|---:|---:|---|
| 6 | Surface Hydrology Network V3.3 | AHGFNetworkStream - All | 348 | 1,430,773 | `cb2bf376e8ec948a5b7ddea57d08707eeb6cea58464d1f050a31e8d7dd87b44b` |
| 31 | Hydrology Reporting Catchments V3.3 | AHGFContractedCatchment | 55 | 1,672,027 | `abe240f187e4129ba7812f7dfd305c64fe20cd142950ecb679b96cf9a821cd50` |
| 33 | Surface Catchments V3.3 | AHGFCatchment (SH_Catchments) | 483 | 3,934,331 | `95da735409bdd82f83a92ad167e88cde0bbc768c1d2d0be73f0d6a366282ccac` |
| 27 | Surface Hydrology Cartography V3.3 | AHGFWaterbody (SH_Cartography) | 15 | 37,523 | `f792917f68f034234fa2dfb337142ab2c64abfe9d816604e5c3571ebce9b83e4` |

Total new network retrieval and retained raw hydrology: **7,074,654 bytes**.
This is below both the 150 MB network ceiling and 100 MB raw ceiling.

## Bounded extent

The request and all retained derived geometries use the existing authorized
official Cooma locality plus 10 km buffer only.

- longitude: 148.9359628223 to 149.2892495063
- latitude: -36.3977706857 to -36.0986116526
- EPSG:7855: 673874.03–705782.35 E; 5969790.32–6002993.46 N

FeatureServer `intersects` responses can contain whole features whose source
geometry crosses the request envelope. Every derived geometry was therefore
reprojected from EPSG:4283 to EPSG:7855 and intersected with the existing exact
authorized terrain polygon.

## Derived hydrology

| Local layer | Selection | Features | Bytes | SHA-256 |
|---|---|---:|---:|---|
| Main Rivers and Watercourses | official `hierarchy=Major` | 55 | 192,512 | `a0308a517b5db9a278135ff1d6a1d8c95ac4cacee56cd91ca0e86adff9e404b9` |
| Secondary Streams | official `hierarchy=Minor` | 212 | 524,288 | `ad08b0875450c2ad355753b04fc2ab103bf7825ea7653e479f9daf2badf337f8` |
| Cooma Catchment Context | AHGFContractedCatchment | 44 | 466,944 | `cbcde39c1d869540628154a0e00f47662284def39dfecc6616e3ffc5c266de85` |
| Cooma Subcatchment Context | AHGFCatchment stream-segment units | 384 | 1,380,352 | `c5de1196b4e5853ac433549ca9ae510c838a39d57c9d9856426e86b84dae538f` |
| Named Water Features | waterbody source Name populated | 3 | 98,304 | `47328b2862c569e5e6c6fec5cf717292881ae6f72adc00a6a4526e6a2842d1e5` |

Derived hydrology total: **2,662,400 bytes**, below the 150 MB ceiling.
Observed workspace during technical verification: **23,567,907 bytes**, below
the 800 MB ceiling.

The three retained named water features are the official source identities
`ARABLE LAKE`, `GREEN LAKE`, and `THURBERGAL LAKE`. Their source records describe
them as non-perennial lakes. This is an attribute record, not a conclusion about
present water, availability, quality, storage or security.

## Catchment identities and limitations

The 44 clipped contracted-catchment features include official identities such as
Cooma Creek, Cooma Back Creek, Murrumbidgee River, Numeralla River, Rock Flat
Creek and other named or unnamed Geofabric units. Multiple features can share a
stream name because they represent different contracted units and HydroIDs.

- The official Cooma locality polygon is an administrative locality, not a catchment.
- The terrain extent is the locality plus 10 km buffer, not a catchment.
- `AHGFContractedCatchment` is an aggregation to persistent contracted nodes.
- `AHGFCatchment` is a lower-level stream-segment catchment derived from DEM-S;
  “Subcatchment Context” is a project display label, not a renamed official product.
- No Council boundary is present in this pack.
- None of these polygons is identified as a drinking-water supply catchment.

## QGIS v0.3 project

- Local path: `runtime_data/qgis/cooma_spatial_foundation/project/Cooma_Spatial_Foundation_v0_3_hydrology.qgz`
- CRS: EPSG:7855
- SHA-256: `e3add6f05a0252c73aa2ccb456cea685e5e0eeb4221c5866f7c25dfb29a94765`
- Broken layers: 0
- Network-backed providers: 0
- Terrain layers retained: boundary, DEM, hillshade and slope
- Hydrology default visibility: Main watercourses ON; catchment context ON;
  named water features ON; slope OFF; secondary streams OFF; stream-segment
  catchments OFF.

Hydrology bookmarks:

1. `Cooma Watercourses`
2. `Cooma Catchment Context`
3. `Terrain and Water Relationship`

Their technical extents are distinct. Existing `Cooma Locality` and
`Cooma + 10 km Terrain` bookmarks remain in the project.

## Windows QGIS validation

QGIS Desktop 3.44.11 opened the local project at EPSG:7855. Boundary, terrain,
water group, main watercourses, transparent contracted catchments and named
waterbodies loaded. Layer visibility toggles changed the rendered view.

- Watercourses bookmark: approximately 1:183,775
- Catchment bookmark: approximately 1:262,536
- Terrain/water bookmark: approximately 1:212,404
- Watercourse Identify: `COOMA BACK CREEK`, HydroID `43554300`, official
  hierarchy `Major`, source type `Watercourse`
- Catchment Identify: `COOMA CREEK`, HydroID `43671861`, ConCatID `449785`,
  conlevel `2`

The automated QGIS verifier independently reopened the QGZ, found zero broken
layers and zero web providers. The manual close action reached QGIS's unsaved
view-state prompt; the project was not saved or changed. Clicking `Discard` was
left to the human because desktop safety policy requires action-time confirmation
for discarding local app state. Consequently, the manual close/reopen substep is
recorded as deferred, while the automated reopen and local-only provider checks pass.

## Safety result

- Hydrology focused suite: 29 tests passed.
- Complete repository suite: 416 tests passed, 1 skipped.
- `python -m compileall cczps_lite`: passed.
- `git diff --check`: passed.
- No climate, fire, wastewater or engineering data added.
- No water availability, drought, flood, supply-security or scientific conclusion made.
- No real GeoJSON, GeoPackage, raster, QGZ, cache or runtime file is committed.
- `runtime_data/` remains ignored.
- `prototype/` remains untouched.
- PR #95 remains Founder-unaccepted and unmerged.

## Gate

```text
READY_FOR_FOUNDER_QGIS_HYDROLOGY_REVIEW
/ STACKED_ON_UNMERGED_PR95
/ BOUNDED_PUBLIC_DATA
/ SPATIAL_OBSERVATION_ONLY
/ NO_SCIENTIFIC_CONCLUSION
/ DO_NOT_AUTO_MERGE
```
