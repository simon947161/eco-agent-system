"""Closed constants for the Task2021-2030 local QGIS foundation."""

from __future__ import annotations

from pathlib import Path

RUNTIME_RELATIVE_ROOT = Path("runtime_data/qgis/cooma_spatial_foundation")
PROJECT_FILENAME = "Cooma_Spatial_Foundation_v0_1.qgz"
REVISION_PROJECT_FILENAME = "Cooma_Spatial_Foundation_v0_1_ux_revision.qgz"
PROVISIONAL_SCOPE_STATUS = "PROVISIONAL_SPATIAL_SCOPE / HUMAN_REVIEW_REQUIRED"
SCIENTIFIC_CONCLUSION = "NONE"
SOURCE_DATA_STATUS = "NOT_RETRIEVED"
DERIVED_DATA_STATUS = "NONE"
SYNTHETIC_DATA_STATUS = "SYNTHETIC_NAVIGATION_ANCHOR"
DEFAULT_VIEW_EXTENT = (149.03, -36.31, 149.21, -36.15)

WORKSPACE_DIRECTORIES = (
    "project",
    "source_data",
    "derived_data",
    "styles",
    "exports",
    "notes",
    "manifests",
    "local_anchor",
)

PROJECT_LAYER_GROUPS = (
    "00_START_HERE",
    "01_BOUNDARIES",
    "02_TERRAIN",
    "03_WATER",
    "04_SETTLEMENT_AND_ROADS",
    "05_CLIMATE_STATIONS",
    "06_PUBLIC_INFRASTRUCTURE_LATER",
    "07_EVIDENCE_NOTES",
    "90_SOURCE_METADATA",
    "99_DISABLED_LATER_LAYERS",
)

# These extents are navigation aids, not admitted study boundaries or evidence.
# They intentionally remain coarse until a bounded public-data retrieval Gate.
BOOKMARKS = (
    {
        "name": "Cooma Town",
        "extent": (149.08, -36.26, 149.16, -36.20),
        "crs": "EPSG:4326",
    },
    {
        "name": "Wider Cooma Context",
        "extent": (148.78, -36.52, 149.50, -35.90),
        "crs": "EPSG:4326",
    },
    {
        "name": "Terrain Overview",
        "extent": (148.94, -36.39, 149.32, -36.06),
        "crs": "EPSG:4326",
    },
    {
        "name": "Main Waterways",
        "extent": (149.00, -36.34, 149.27, -36.11),
        "crs": "EPSG:4326",
    },
    {
        "name": "Catchment Context",
        "extent": (148.55, -36.80, 149.70, -35.65),
        "crs": "EPSG:4326",
    },
)

START_HERE_MESSAGES = (
    "START HERE — QGIS Cooma Learning Guide",
    "Cooma Provisional Centre — NOT EVIDENCE",
    "Provisional Cooma Learning Extent — NOT EVIDENCE",
)

TERRAIN_INFO_LAYER = "INFO — Terrain data not yet retrieved"
WATER_INFO_LAYER = "INFO — Hydrology data not yet retrieved"
SYNTHETIC_LAYER_NAMES = START_HERE_MESSAGES + (TERRAIN_INFO_LAYER, WATER_INFO_LAYER)


def workspace_contract() -> dict[str, object]:
    """Return the deterministic local workspace contract."""

    return {
        "schema_id": "climateos.qgis-local-spatial-workspace.v2",
        "project_filename": PROJECT_FILENAME,
        "revision_project_filename": REVISION_PROJECT_FILENAME,
        "workspace_directories": list(WORKSPACE_DIRECTORIES),
        "scope_status": PROVISIONAL_SCOPE_STATUS,
        "source_data_status": SOURCE_DATA_STATUS,
        "derived_data_status": DERIVED_DATA_STATUS,
        "scientific_conclusion": SCIENTIFIC_CONCLUSION,
        "git_policy": "RUNTIME_DATA_GIT_IGNORED",
        "overwrite_policy": "NEW_FILE_ONLY_OVERWRITE_REFUSED",
        "arbitrary_export_available": False,
        "public_data_retrieval_authorized": False,
        "private_or_council_data_allowed": False,
        "synthetic_navigation_anchor_allowed": True,
    }


def legacy_workspace_contract() -> dict[str, object]:
    """Return the exact pre-UX contract accepted without overwrite."""

    legacy_directories = [name for name in WORKSPACE_DIRECTORIES if name != "local_anchor"]
    return {
        "schema_id": "climateos.qgis-local-spatial-workspace.v1",
        "project_filename": PROJECT_FILENAME,
        "workspace_directories": legacy_directories,
        "scope_status": PROVISIONAL_SCOPE_STATUS,
        "source_data_status": SOURCE_DATA_STATUS,
        "derived_data_status": DERIVED_DATA_STATUS,
        "scientific_conclusion": SCIENTIFIC_CONCLUSION,
        "git_policy": "RUNTIME_DATA_GIT_IGNORED",
        "overwrite_policy": "NEW_FILE_ONLY_OVERWRITE_REFUSED",
        "arbitrary_export_available": False,
        "public_data_retrieval_authorized": False,
        "private_or_council_data_allowed": False,
    }
