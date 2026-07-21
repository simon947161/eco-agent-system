"""Repository-authored, reproducible GeoJSON for QGIS learning and navigation."""

from __future__ import annotations

import json
from pathlib import Path

from .contract import TERRAIN_INFO_LAYER, WATER_INFO_LAYER

CRS84 = {
    "type": "name",
    "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"},
}
PROVISIONAL_CENTRE = (149.13, -36.235)
PROVISIONAL_EXTENT = (149.04, -36.30, 149.20, -36.16)

ANCHOR_FILENAMES = {
    "centre": "cooma_provisional_centre.geojson",
    "extent": "provisional_cooma_learning_extent.geojson",
    "start_here": "start_here_qgis_cooma_learning_guide.geojson",
    "terrain_info": "terrain_data_not_yet_retrieved.geojson",
    "water_info": "hydrology_data_not_yet_retrieved.geojson",
}

COMMON_STATUS = {
    "evidence_status": "SYNTHETIC_NAVIGATION_ANCHOR",
    "scientific_status": "NOT_EVIDENCE",
    "scope_status": "PROVISIONAL",
    "purpose": "LEARNING_AND_NAVIGATION_ONLY",
}


class SyntheticAnchorError(ValueError):
    """Raised when an existing local anchor differs from the closed template."""


def _collection(properties: dict[str, object], geometry: dict[str, object] | None) -> dict[str, object]:
    return {
        "type": "FeatureCollection",
        "name": str(properties["name"]),
        "crs": CRS84,
        "features": [
            {
                "type": "Feature",
                "properties": properties,
                "geometry": geometry,
            }
        ],
    }


def synthetic_anchor_payloads() -> dict[str, dict[str, object]]:
    """Return all five closed local GeoJSON payloads without file I/O."""

    west, south, east, north = PROVISIONAL_EXTENT
    centre = _collection(
        {
            "name": "Cooma Provisional Centre",
            **COMMON_STATUS,
            "human_review_required": True,
        },
        {"type": "Point", "coordinates": list(PROVISIONAL_CENTRE)},
    )
    extent = _collection(
        {
            "name": "Provisional Cooma Learning Extent",
            **COMMON_STATUS,
            "human_review_required": True,
            "boundary_warning": "NOT_A_CATCHMENT_COUNCIL_OR_SCIENTIFIC_BOUNDARY",
        },
        {
            "type": "Polygon",
            "coordinates": [
                [
                    [west, south],
                    [east, south],
                    [east, north],
                    [west, north],
                    [west, south],
                ]
            ],
        },
    )
    start_here = _collection(
        {
            "name": "START HERE — QGIS Cooma Learning Guide",
            "current_project_state": "SKELETON + SYNTHETIC NAVIGATION ANCHOR",
            "real_data_downloaded": "NONE",
            "scientific_conclusions": "NONE",
            "how_to_use": "Expand groups; open Spatial Bookmarks; double-click a bookmark; pan and zoom; identify the provisional centre or extent; read status attributes.",
            "warning": "The visible point and rectangle are navigation aids, not scientific evidence.",
            **COMMON_STATUS,
        },
        None,
    )
    terrain = _collection(
        {
            "name": TERRAIN_INFO_LAYER,
            "data_status": "DATA_NOT_YET_RETRIEVED",
            "future_layers": "DEM; Hillshade; Slope; Contours",
            "interaction": "Expand this group with the arrow; double-clicking a group does not open data.",
            "scientific_status": "NOT_EVIDENCE",
        },
        None,
    )
    water = _collection(
        {
            "name": WATER_INFO_LAYER,
            "data_status": "DATA_NOT_YET_RETRIEVED",
            "future_layers": "Rivers; Streams; Waterbodies; Catchment boundaries",
            "interaction": "Expand this group with the arrow; double-clicking a group does not open data.",
            "scientific_status": "NOT_EVIDENCE",
        },
        None,
    )
    return {
        ANCHOR_FILENAMES["centre"]: centre,
        ANCHOR_FILENAMES["extent"]: extent,
        ANCHOR_FILENAMES["start_here"]: start_here,
        ANCHOR_FILENAMES["terrain_info"]: terrain,
        ANCHOR_FILENAMES["water_info"]: water,
    }


def ensure_synthetic_anchor_files(local_anchor_root: Path) -> tuple[Path, ...]:
    """Create exact ignored GeoJSON files, reusing only byte-identical files."""

    local_anchor_root.mkdir(parents=True, exist_ok=True)
    if local_anchor_root.is_symlink():
        raise SyntheticAnchorError("local_anchor must not be a symlink")
    paths: list[Path] = []
    for filename, payload in synthetic_anchor_payloads().items():
        path = local_anchor_root / filename
        serialized = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
        if path.exists():
            if not path.is_file() or path.is_symlink():
                raise SyntheticAnchorError(f"anchor path must be a regular file: {path}")
            if path.read_text(encoding="utf-8") != serialized:
                raise SyntheticAnchorError(f"existing synthetic anchor differs; overwrite refused: {path}")
        else:
            with path.open("x", encoding="utf-8", newline="\n") as handle:
                handle.write(serialized)
        paths.append(path)
    return tuple(paths)
