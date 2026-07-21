"""Closed Task2041-2050 contracts for the bounded Cooma hydrology pack."""

from __future__ import annotations

from pathlib import Path

HYDROLOGY_PROJECT_FILENAME = "Cooma_Spatial_Foundation_v0_3_hydrology.qgz"
TERRAIN_BASE_HEAD = "57e71468514253c188c9a744e3532a67903b0272"
STACKED_PR_BASE = "agent/task2031-2040-qgis-cooma-terrain-boundary-pack"
HYDROLOGY_PROJECT_CRS = "EPSG:7855"
HYDROLOGY_SOURCE_CRS = "EPSG:4283"
HYDROLOGY_PRODUCT = "Australian Hydrological Geospatial Fabric (Geofabric)"
HYDROLOGY_VERSION = "V3.3"
HYDROLOGY_PUBLISHER = "Commonwealth of Australia, Bureau of Meteorology"
HYDROLOGY_LICENCE = "Creative Commons Attribution 4.0 International (CC BY 4.0)"
HYDROLOGY_ATTRIBUTION = "© Commonwealth of Australia (Bureau of Meteorology) 2022"
HYDROLOGY_SERVICE = (
    "https://hosting.wsapi.cloud.bom.gov.au/arcgis/rest/services/ahgf/"
    "Geofabric_V3x_All_Products/FeatureServer"
)
HYDROLOGY_METADATA_DATE = "2022"
HYDROLOGY_FEATURE_SCALE = "approximately 1:100,000 foundation mapping; layer scale rules vary"

# Exact official FeatureServer layers. No NSW fallback is mixed into this pack.
HYDROLOGY_SOURCES = (
    {
        "id": "network_stream",
        "layer_id": 6,
        "product_component": "Geofabric Surface Hydrology Network - V3.3",
        "layer": "AHGFNetworkStream - All",
        "geometry_type": "esriGeometryPolyline",
        "filename": "geofabric_v3_3_network_stream_all_cooma_10km_epsg4283.geojson",
    },
    {
        "id": "contracted_catchment",
        "layer_id": 31,
        "product_component": "Geofabric Hydrology Reporting Catchments - V3.3",
        "layer": "AHGFContractedCatchment",
        "geometry_type": "esriGeometryPolygon",
        "filename": "geofabric_v3_3_contracted_catchment_cooma_10km_epsg4283.geojson",
    },
    {
        "id": "stream_segment_catchment",
        "layer_id": 33,
        "product_component": "Geofabric Surface Catchments - V3.3",
        "layer": "AHGFCatchment (SH_Catchments)",
        "geometry_type": "esriGeometryPolygon",
        "filename": "geofabric_v3_3_stream_segment_catchment_cooma_10km_epsg4283.geojson",
    },
    {
        "id": "waterbody",
        "layer_id": 27,
        "product_component": "Geofabric Surface Hydrology Cartography - V3.3",
        "layer": "AHGFWaterbody (SH_Cartography)",
        "geometry_type": "esriGeometryPolygon",
        "filename": "geofabric_v3_3_waterbody_cooma_10km_epsg4283.geojson",
    },
)

AUTHORIZED_LONGITUDE_LATITUDE_EXTENT = {
    "west": 148.9359628223,
    "east": 149.2892495063,
    "south": -36.3977706857,
    "north": -36.0986116526,
}

NETWORK_RETRIEVAL_LIMIT = 150 * 1024 * 1024
RAW_HYDROLOGY_LIMIT = 100 * 1024 * 1024
DERIVED_HYDROLOGY_LIMIT = 150 * 1024 * 1024
WORKSPACE_LIMIT = 800 * 1024 * 1024

HYDROLOGY_WORKSPACE_DIRECTORIES = (
    Path("source_data/hydrology"),
    Path("derived_data/hydrology"),
    Path("manifests/retrieval"),
    Path("manifests/derivation"),
    Path("project"),
    Path("notes"),
    Path("exports"),
)

DERIVED_FILES = {
    "main_watercourses": "cooma_main_watercourses_geofabric_major_epsg7855.gpkg",
    "secondary_streams": "cooma_secondary_streams_geofabric_minor_epsg7855.gpkg",
    "catchment_context": "cooma_contracted_catchment_context_epsg7855.gpkg",
    "subcatchment_context": "cooma_stream_segment_catchment_context_epsg7855.gpkg",
    "named_water_features": "cooma_named_water_features_epsg7855.gpkg",
}

HYDROLOGY_LAYER_NAMES = (
    "Main Rivers and Watercourses — Geofabric official Major",
    "Secondary Streams — Geofabric official Minor",
    "Cooma Catchment Context — Geofabric contracted catchments",
    "Cooma Subcatchment Context — Geofabric stream-segment catchments",
    "Named Water Features — Geofabric waterbodies",
    "INFO — Hydrology source and limitations",
)

HYDROLOGY_BOOKMARKS = (
    "Cooma Watercourses",
    "Cooma Catchment Context",
    "Terrain and Water Relationship",
)


def hydrology_size_limits() -> dict[str, int]:
    return {
        "network_retrieval": NETWORK_RETRIEVAL_LIMIT,
        "raw_hydrology": RAW_HYDROLOGY_LIMIT,
        "derived_hydrology": DERIVED_HYDROLOGY_LIMIT,
        "workspace": WORKSPACE_LIMIT,
    }
