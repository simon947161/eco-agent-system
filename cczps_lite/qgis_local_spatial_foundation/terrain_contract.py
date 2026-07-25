"""Closed Task2031-2040 contracts for the bounded Cooma terrain pack."""

from __future__ import annotations

from pathlib import Path

TERRAIN_PROJECT_FILENAME = "Cooma_Spatial_Foundation_v0_2_terrain.qgz"
TERRAIN_PROJECT_CRS = "EPSG:7855"
BOUNDARY_SOURCE_CRS = "EPSG:7844"
DEM_SOURCE_CRS = "EPSG:4326"

BOUNDARY_SERVICE = (
    "https://portal.spatial.nsw.gov.au/server/rest/services/"
    "NSW_Administrative_Boundaries_Theme_multiCRS/FeatureServer/2"
)
BOUNDARY_QUERY_URL = BOUNDARY_SERVICE + "/query"
BOUNDARY_WHERE = "suburbname='COOMA'"
BOUNDARY_EXPECTED_IDENTITY = {
    "suburbname": "COOMA",
    "OBJECTID": 16701,
    "cadid": 108029985,
    "shapeuuid": "42bcb472-a4e4-30cd-a949-077681669ffd",
}
BOUNDARY_LICENCE = "Creative Commons Attribution"
BOUNDARY_PRODUCT = "NSW Foundation Spatial Data Framework - Administrative Boundaries - Suburb"
BOUNDARY_LAYER = "Suburb (FeatureServer layer 2)"

DEM_URL = (
    "https://dea-public-data.s3-ap-southeast-2.amazonaws.com/projects/"
    "elevation/ga_srtm_dem1sv1_0/dems1sv1_0.tif"
)
DEM_PRODUCT = "Geoscience Australia SRTM 1 second Smoothed DEM (DEM-S) version 1.0"
DEM_PRODUCT_ID = "ga_srtm_dem1sv1_0"
DEM_CATALOGUE_ID = "72759"
DEM_LICENCE = "Creative Commons Attribution 4.0 International"
DEM_VERTICAL_DATUM = "EGM96"
DEM_NODATA = -3.4028235e38
DEM_CELL_SIZE_DEGREES = 0.0002777777777823

BUFFER_METRES = 10_000.0
TARGET_CELL_SIZE_METRES = 30.0
HILLSHADE_AZIMUTH = 315.0
HILLSHADE_ALTITUDE = 45.0
HILLSHADE_Z_FACTOR = 1.0
SLOPE_UNITS = "degrees"

NETWORK_RETRIEVAL_LIMIT = 250 * 1024 * 1024
RAW_DEM_LIMIT = 150 * 1024 * 1024
BOUNDARY_LIMIT = 20 * 1024 * 1024
SOURCE_DATA_LIMIT = 200 * 1024 * 1024
DERIVED_DATA_LIMIT = 300 * 1024 * 1024
WORKSPACE_LIMIT = 600 * 1024 * 1024

BOUNDARY_FILENAME = "cooma_locality_nsw_official_epsg7844.geojson"
STUDY_EXTENT_FILENAME = "cooma_locality_buffer_10km_epsg7855.geojson"
STUDY_EXTENT_MANIFEST = "cooma_terrain_extent.json"
BOUNDED_DEM_FILENAME = "cooma_ga_srtm_dem_s_1sec_bounded_epsg4326.tif"
PROJECTED_DEM_FILENAME = "cooma_dem_s_mga55_30m.tif"
HILLSHADE_FILENAME = "cooma_hillshade_mga55_30m.tif"
SLOPE_FILENAME = "cooma_slope_degrees_mga55_30m.tif"

TERRAIN_LAYER_NAMES = (
    "Cooma Locality Boundary — NSW official source",
    "Cooma DEM — GA SRTM 1-second — bounded",
    "Cooma Hillshade — derived from bounded GA DEM",
    "Cooma Slope Degrees — derived",
)

TERRAIN_WORKSPACE_DIRECTORIES = (
    Path("source_data/administrative_boundary"),
    Path("source_data/elevation"),
    Path("derived_data/terrain"),
    Path("manifests/retrieval"),
    Path("manifests/derivation"),
)


def size_limits() -> dict[str, int]:
    """Return the immutable byte ceilings used by retrieval and validation."""

    return {
        "network_retrieval": NETWORK_RETRIEVAL_LIMIT,
        "raw_dem": RAW_DEM_LIMIT,
        "administrative_boundary": BOUNDARY_LIMIT,
        "source_data": SOURCE_DATA_LIMIT,
        "derived_data": DERIVED_DATA_LIMIT,
        "workspace": WORKSPACE_LIMIT,
    }
