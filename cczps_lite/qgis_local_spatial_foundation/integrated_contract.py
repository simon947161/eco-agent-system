"""Closed Task2051-2060 contracts for the integrated Cooma QGIS experience."""

from __future__ import annotations

from pathlib import Path

INTEGRATED_BASE_HEAD = "4ed5afc98d547acb1cddb688fdca53c9a5fc975e"
INTEGRATED_PROJECT_FILENAME = "Cooma_Spatial_Foundation_v0_4_integrated.qgz"
INTEGRATED_PROJECT_CRS = "EPSG:7855"
HYDROLOGY_BASE_PROJECT_FILENAME = "Cooma_Spatial_Foundation_v0_3_hydrology.qgz"

ROAD_PUBLISHER = "NSW Spatial Services"
ROAD_PRODUCT = "NSW Foundation Spatial Data Framework — Transport Theme"
ROAD_LAYER = "RoadSegment (FeatureServer layer 5)"
ROAD_SERVICE = (
    "https://portal.spatial.nsw.gov.au/server/rest/services/"
    "NSW_Transport_Theme/FeatureServer/5"
)
ROAD_QUERY_URL = ROAD_SERVICE + "/query"
ROAD_LICENCE = "Creative Commons Attribution"
ROAD_SOURCE_CRS = "EPSG:4326"
ROAD_RAW_FILENAME = "nsw_road_segments_cooma_10km_epsg4326.geojson"
ROAD_DERIVED_FILENAME = "cooma_road_segments_nsw_official_epsg7855.gpkg"
ROAD_LAYER_NAME = "Roads — NSW official RoadSegment"

IMAGERY_PUBLISHER = "NSW Spatial Services"
IMAGERY_PRODUCT = "NSWWebImagery"
IMAGERY_SERVICE = "https://portal.spatial.nsw.gov.au/aid/tile/rest/services/NSWWebImagery/MapServer"
IMAGERY_TILE_URL = IMAGERY_SERVICE + "/tile/{z}/{y}/{x}"
IMAGERY_LAYER_NAME = "Aerial imagery — NSWWebImagery — online"
IMAGERY_CRS = "EPSG:3857"
IMAGERY_MIN_ZOOM = 0
IMAGERY_MAX_ZOOM = 23

AUTHORIZED_LONGITUDE_LATITUDE_EXTENT = {
    "west": 148.9359628223,
    "east": 149.2892495063,
    "south": -36.3977706857,
    "north": -36.0986116526,
}

NETWORK_RETRIEVAL_LIMIT = 100 * 1024 * 1024
RAW_ROAD_LIMIT = 75 * 1024 * 1024
DERIVED_ROAD_LIMIT = 100 * 1024 * 1024
WORKSPACE_LIMIT = 1_000 * 1024 * 1024

INTEGRATED_WORKSPACE_DIRECTORIES = (
    Path("source_data/roads"),
    Path("derived_data/roads"),
    Path("manifests/retrieval"),
    Path("manifests/derivation"),
    Path("project"),
    Path("exports"),
)

INTEGRATED_BOOKMARKS = (
    "Integrated Cooma Overview",
    "Satellite and Roads",
    "Terrain and Water Together",
)

DEFAULT_VISIBLE_LAYERS = (
    IMAGERY_LAYER_NAME,
    ROAD_LAYER_NAME,
    "Cooma Locality Boundary — NSW official source",
    "Main Rivers and Watercourses — Geofabric official Major",
    "Named Water Features — Geofabric waterbodies",
)


def integrated_size_limits() -> dict[str, int]:
    return {
        "network_retrieval": NETWORK_RETRIEVAL_LIMIT,
        "raw_roads": RAW_ROAD_LIMIT,
        "derived_roads": DERIVED_ROAD_LIMIT,
        "workspace": WORKSPACE_LIMIT,
    }
