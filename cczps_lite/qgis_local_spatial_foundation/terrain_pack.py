"""Retrieve, derive, build, and verify the bounded Cooma terrain pack.

Every network action is explicit. There is no combined unattended retrieval action.
All real data remains below the git-ignored controlled QGIS runtime workspace.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import zipfile

from .contract import (
    PROJECT_LAYER_GROUPS,
    SCIENTIFIC_CONCLUSION,
    START_HERE_MESSAGES,
    TERRAIN_INFO_LAYER,
    WATER_INFO_LAYER,
)
from .project_builder import (
    SpatialProjectError,
    _new_qgis_application,
    _populate_project,
    _qgis_api as _base_qgis_api,
)
from .synthetic_anchor import ensure_synthetic_anchor_files
from .terrain_contract import (
    BOUNDARY_EXPECTED_IDENTITY,
    BOUNDARY_FILENAME,
    BOUNDARY_LAYER,
    BOUNDARY_LICENCE,
    BOUNDARY_LIMIT,
    BOUNDARY_PRODUCT,
    BOUNDARY_QUERY_URL,
    BOUNDARY_SOURCE_CRS,
    BOUNDARY_WHERE,
    BOUNDED_DEM_FILENAME,
    BUFFER_METRES,
    DEM_CATALOGUE_ID,
    DEM_CELL_SIZE_DEGREES,
    DEM_LICENCE,
    DEM_NODATA,
    DEM_PRODUCT,
    DEM_PRODUCT_ID,
    DEM_SOURCE_CRS,
    DEM_URL,
    DEM_VERTICAL_DATUM,
    DERIVED_DATA_LIMIT,
    HILLSHADE_ALTITUDE,
    HILLSHADE_AZIMUTH,
    HILLSHADE_FILENAME,
    HILLSHADE_Z_FACTOR,
    NETWORK_RETRIEVAL_LIMIT,
    PROJECTED_DEM_FILENAME,
    RAW_DEM_LIMIT,
    SLOPE_FILENAME,
    SLOPE_UNITS,
    SOURCE_DATA_LIMIT,
    STUDY_EXTENT_FILENAME,
    STUDY_EXTENT_MANIFEST,
    TARGET_CELL_SIZE_METRES,
    TERRAIN_LAYER_NAMES,
    TERRAIN_PROJECT_CRS,
    TERRAIN_PROJECT_FILENAME,
    TERRAIN_WORKSPACE_DIRECTORIES,
    size_limits,
)
from .workspace import SpatialWorkspaceError, ensure_local_workspace


class TerrainPackError(RuntimeError):
    """Raised when a source, size, path, overwrite, or derivation gate fails."""


def load_source_registry(package_root: Path | None = None) -> dict[str, object]:
    """Load and validate the closed, repository-safe source identity registry."""

    root = package_root or Path(__file__).resolve().parent
    path = root / "terrain_source_registry.json"
    registry = json.loads(path.read_text(encoding="utf-8"))
    if registry.get("registry_status") != "CLOSED_FOUNDER_AUTHORIZED":
        raise TerrainPackError("terrain source registry is not closed and authorized")
    if registry.get("scientific_conclusion") != "NONE":
        raise TerrainPackError("terrain source registry contains a scientific conclusion")
    sources = registry.get("sources")
    if not isinstance(sources, list) or len(sources) != 2:
        raise TerrainPackError("terrain source registry must contain exactly two sources")
    for source in sources:
        if not isinstance(source, dict) or not source.get("licence"):
            raise TerrainPackError("every terrain source requires an explicit licence")
        if not str(source.get("source_url", "")).startswith("https://"):
            raise TerrainPackError("every terrain source requires a closed HTTPS URL")
    return registry


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _ensure_regular_new_file(path: Path) -> None:
    if path.exists() or path.is_symlink():
        raise TerrainPackError(f"new-file-only overwrite refused: {path}")


def _assert_confined(path: Path, root: Path) -> None:
    resolved = path.resolve()
    controlled = root.resolve()
    if resolved != controlled and controlled not in resolved.parents:
        raise TerrainPackError(f"path escapes controlled QGIS workspace: {path}")
    current = resolved.parent
    while current != controlled.parent:
        if current.exists() and current.is_symlink():
            raise TerrainPackError(f"controlled path contains symlink: {current}")
        if current == controlled:
            break
        current = current.parent


def _write_json_new(path: Path, payload: object) -> None:
    _ensure_regular_new_file(path)
    serialized = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(serialized)


def _layout(repo_root: Path) -> dict[str, Path]:
    workspace = ensure_local_workspace(repo_root)
    root = workspace["root"]
    for relative in TERRAIN_WORKSPACE_DIRECTORIES:
        destination = root / relative
        _assert_confined(destination, root)
        destination.mkdir(parents=True, exist_ok=True)
    return {
        "root": root,
        "boundary": root / "source_data" / "administrative_boundary" / BOUNDARY_FILENAME,
        "bounded_dem": root / "source_data" / "elevation" / BOUNDED_DEM_FILENAME,
        "terrain_root": root / "derived_data" / "terrain",
        "study_extent": root / "derived_data" / "terrain" / STUDY_EXTENT_FILENAME,
        "extent_manifest": root / "manifests" / "derivation" / STUDY_EXTENT_MANIFEST,
        "boundary_receipt": root / "manifests" / "retrieval" / "cooma_boundary_receipt.json",
        "dem_receipt": root / "manifests" / "retrieval" / "cooma_dem_receipt.json",
        "derivation_manifest": root / "manifests" / "derivation" / "cooma_terrain_derivation.json",
        "project": root / "project" / TERRAIN_PROJECT_FILENAME,
        "project_manifest": root / "manifests" / "derivation" / "cooma_terrain_project.json",
    }


def _directory_size(path: Path) -> int:
    return sum(item.stat().st_size for item in path.rglob("*") if item.is_file())


def _enforce_workspace_sizes(layout: dict[str, Path]) -> dict[str, int]:
    root = layout["root"]
    sizes = {
        "source_data": _directory_size(root / "source_data"),
        "derived_data": _directory_size(root / "derived_data"),
        "workspace": _directory_size(root),
    }
    limits = size_limits()
    for name, observed in sizes.items():
        if observed > limits[name]:
            raise TerrainPackError(f"{name} size ceiling exceeded: {observed} > {limits[name]}")
    return sizes


def _boundary_feature(payload: dict[str, object]) -> dict[str, object]:
    features = payload.get("features")
    if not isinstance(features, list) or len(features) != 1:
        raise TerrainPackError("official boundary query must return exactly one COOMA feature")
    feature = features[0]
    if not isinstance(feature, dict) or feature.get("type") != "Feature":
        raise TerrainPackError("official boundary response is not one GeoJSON Feature")
    properties = feature.get("properties")
    if not isinstance(properties, dict):
        raise TerrainPackError("official boundary feature has no properties")
    for field, expected in BOUNDARY_EXPECTED_IDENTITY.items():
        if properties.get(field) != expected:
            raise TerrainPackError(
                f"official boundary identity mismatch for {field}: {properties.get(field)!r}"
            )
    if not isinstance(feature.get("geometry"), dict):
        raise TerrainPackError("official boundary feature has no geometry")
    return feature


def _osgeo():
    from osgeo import gdal, ogr, osr  # type: ignore[import-not-found]

    gdal.UseExceptions()
    ogr.UseExceptions()
    return gdal, ogr, osr


def _spatial_reference(osr, epsg: int):
    reference = osr.SpatialReference()
    reference.ImportFromEPSG(epsg)
    if hasattr(reference, "SetAxisMappingStrategy"):
        reference.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
    return reference


def _boundary_extent_products(boundary_path: Path, extent_path: Path) -> dict[str, object]:
    _, ogr, osr = _osgeo()
    source = ogr.Open(str(boundary_path), 0)
    if source is None:
        raise TerrainPackError("GDAL could not open the retained boundary")
    layer = source.GetLayer(0)
    if layer.GetFeatureCount() != 1:
        raise TerrainPackError("retained boundary does not contain exactly one feature")
    feature = layer.GetNextFeature()
    geometry = feature.GetGeometryRef().Clone()
    if geometry is None or geometry.IsEmpty():
        raise TerrainPackError("retained boundary geometry is empty")
    if not geometry.IsValid():
        raise TerrainPackError("retained boundary geometry is invalid")

    source_crs = _spatial_reference(osr, 7844)
    projected_crs = _spatial_reference(osr, 7855)
    wgs84 = _spatial_reference(osr, 4326)
    geometry.AssignSpatialReference(source_crs)
    projected = geometry.Clone()
    projected.Transform(osr.CoordinateTransformation(source_crs, projected_crs))
    boundary_envelope = projected.GetEnvelope()
    buffered = projected.Buffer(BUFFER_METRES)
    if buffered is None or buffered.IsEmpty() or not buffered.IsValid():
        raise TerrainPackError("10 km projected boundary buffer is invalid")
    projected_extent = buffered.GetEnvelope()
    lonlat = buffered.Clone()
    lonlat.Transform(osr.CoordinateTransformation(projected_crs, wgs84))
    lonlat_extent = lonlat.GetEnvelope()

    _ensure_regular_new_file(extent_path)
    driver = ogr.GetDriverByName("GeoJSON")
    output = driver.CreateDataSource(str(extent_path))
    output_layer = output.CreateLayer("cooma_locality_buffer_10km", projected_crs, ogr.wkbPolygon)
    for field_name in ("scope_status", "scientific_conclusion", "source_feature"):
        output_layer.CreateField(ogr.FieldDefn(field_name, ogr.OFTString))
    output_feature = ogr.Feature(output_layer.GetLayerDefn())
    output_feature.SetField("scope_status", "OFFICIAL_LOCALITY_PLUS_10KM_BUFFER")
    output_feature.SetField("scientific_conclusion", "NONE")
    output_feature.SetField("source_feature", "COOMA locality OBJECTID 16701")
    output_feature.SetGeometry(buffered)
    output_layer.CreateFeature(output_feature)
    output_feature = None
    output_layer = None
    output = None
    source = None

    west, east, south, north = projected_extent
    lon_west, lon_east, lat_south, lat_north = lonlat_extent
    return {
        "selection_reason": "official COOMA locality polygon plus 10 km projected buffer",
        "source_boundary_crs": BOUNDARY_SOURCE_CRS,
        "projected_crs": TERRAIN_PROJECT_CRS,
        "buffer_metres": BUFFER_METRES,
        "boundary_projected_extent": {
            "west": boundary_envelope[0],
            "east": boundary_envelope[1],
            "south": boundary_envelope[2],
            "north": boundary_envelope[3],
        },
        "projected_extent": {"west": west, "east": east, "south": south, "north": north},
        "longitude_latitude_extent": {
            "west": lon_west,
            "east": lon_east,
            "south": lat_south,
            "north": lat_north,
        },
        "width_metres": east - west,
        "height_metres": north - south,
        "area_square_kilometres": buffered.GetArea() / 1_000_000.0,
        "geometry_valid": True,
        "scientific_conclusion": "NONE",
    }


def retrieve_boundary(repo_root: Path) -> dict[str, object]:
    layout = _layout(repo_root)
    boundary_path = layout["boundary"]
    extent_path = layout["study_extent"]
    extent_manifest_path = layout["extent_manifest"]
    receipt_path = layout["boundary_receipt"]
    for path in (boundary_path, extent_path, extent_manifest_path, receipt_path):
        _assert_confined(path, layout["root"])
        _ensure_regular_new_file(path)

    parameters = {
        "f": "geojson",
        "where": BOUNDARY_WHERE,
        "outFields": "*",
        "returnGeometry": "true",
        "outSR": "7844",
    }
    source_url = BOUNDARY_QUERY_URL + "?" + urlencode(parameters)
    request = Request(source_url, headers={"User-Agent": "ClimateOS-QGIS-Terrain-Pack/1.0"})
    with urlopen(request, timeout=60) as response:  # nosec B310 - closed HTTPS registry URL
        declared = response.headers.get("Content-Length")
        if declared is not None and int(declared) > BOUNDARY_LIMIT:
            raise TerrainPackError("boundary response exceeds the 20 MB ceiling")
        content = response.read(BOUNDARY_LIMIT + 1)
    if len(content) > BOUNDARY_LIMIT:
        raise TerrainPackError("boundary response exceeded the 20 MB ceiling while reading")
    payload = json.loads(content.decode("utf-8"))
    _boundary_feature(payload)
    with boundary_path.open("xb") as handle:
        handle.write(content)

    extent = _boundary_extent_products(boundary_path, extent_path)
    extent_manifest = {
        "schema_id": "climateos.qgis-cooma-terrain-extent.v1",
        "created_at": _utc_now(),
        **extent,
    }
    _write_json_new(extent_manifest_path, extent_manifest)
    receipt = {
        "schema_id": "climateos.spatial-retrieval-receipt.v1",
        "retrieval_id": "QGIS-TERRAIN-BOUNDARY-001",
        "publisher": "NSW Spatial Services / Department of Customer Service",
        "product": BOUNDARY_PRODUCT,
        "layer": BOUNDARY_LAYER,
        "source_url": source_url,
        "retrieved_at": _utc_now(),
        "licence": BOUNDARY_LICENCE,
        "requested_extent": "single exact feature where suburbname='COOMA'",
        "returned_extent": extent["longitude_latitude_extent"],
        "content_length": len(content),
        "sha256": _sha256(boundary_path),
        "local_path": boundary_path.relative_to(layout["root"]).as_posix(),
        "raw_retained": True,
        "feature_identity": BOUNDARY_EXPECTED_IDENTITY,
        "source_crs": BOUNDARY_SOURCE_CRS,
        "geometry_valid": True,
        "scientific_conclusion": "NONE",
    }
    _write_json_new(receipt_path, receipt)
    sizes = _enforce_workspace_sizes(layout)
    return {"boundary_receipt": receipt, "extent": extent_manifest, "workspace_sizes": sizes}


_CONTENT_RANGE = re.compile(r"content-range:\s*bytes\s+(\d+)-(\d+)/(\d+|\*)", re.I)


def _bounded_dem_plan(extent: dict[str, float]) -> dict[str, int]:
    width_pixels = math.ceil((extent["east"] - extent["west"]) / DEM_CELL_SIZE_DEGREES)
    height_pixels = math.ceil((extent["north"] - extent["south"]) / DEM_CELL_SIZE_DEGREES)
    uncompressed = width_pixels * height_pixels * 4
    source_blocks = math.ceil(width_pixels / 512) * math.ceil(height_pixels / 512)
    conservative_network = source_blocks * 512 * 512 * 4 + 24 * 1024 * 1024
    return {
        "width_pixels": width_pixels,
        "height_pixels": height_pixels,
        "uncompressed_bytes": uncompressed,
        "conservative_network_bytes": conservative_network,
    }


def _run_range_limited_translate(command: list[str], partial: Path) -> tuple[int, str]:
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        shell=False,
    )
    ranges: set[tuple[int, int]] = set()
    stderr_tail: list[str] = []
    assert process.stderr is not None
    for line in process.stderr:
        stderr_tail.append(line.rstrip())
        stderr_tail = stderr_tail[-80:]
        match = _CONTENT_RANGE.search(line)
        if match:
            byte_range = (int(match.group(1)), int(match.group(2)))
            ranges.add(byte_range)
            measured = sum(end - start + 1 for start, end in ranges)
            if measured > NETWORK_RETRIEVAL_LIMIT:
                process.kill()
                process.wait()
                if partial.exists():
                    partial.unlink()
                raise TerrainPackError("measured HTTP range retrieval exceeded 250 MB ceiling")
    stdout = process.stdout.read() if process.stdout is not None else ""
    return_code = process.wait()
    if return_code != 0:
        if partial.exists():
            partial.unlink()
        raise TerrainPackError(
            "bounded GDAL translate failed: " + "\n".join(stderr_tail[-20:] + [stdout])
        )
    measured = sum(end - start + 1 for start, end in ranges)
    return measured, "\n".join(stderr_tail)


def _raster_info(path: Path) -> dict[str, object]:
    gdal, _, _ = _osgeo()
    dataset = gdal.Open(str(path), gdal.GA_ReadOnly)
    if dataset is None:
        raise TerrainPackError(f"GDAL could not open raster: {path}")
    band = dataset.GetRasterBand(1)
    minimum, maximum = band.ComputeRasterMinMax(False)
    transform = dataset.GetGeoTransform()
    nodata = band.GetNoDataValue()
    info = {
        "width": dataset.RasterXSize,
        "height": dataset.RasterYSize,
        "geotransform": list(transform),
        "projection": dataset.GetProjection(),
        "nodata": nodata,
        "minimum": minimum,
        "maximum": maximum,
        "block_size": list(band.GetBlockSize()),
    }
    dataset = None
    return info


def retrieve_dem(repo_root: Path, osgeo_root: Path) -> dict[str, object]:
    layout = _layout(repo_root)
    destination = layout["bounded_dem"]
    receipt_path = layout["dem_receipt"]
    _assert_confined(destination, layout["root"])
    _ensure_regular_new_file(destination)
    _ensure_regular_new_file(receipt_path)
    if not layout["extent_manifest"].is_file():
        raise TerrainPackError("official boundary extent manifest is required before DEM retrieval")
    extent_manifest = json.loads(layout["extent_manifest"].read_text(encoding="utf-8"))
    extent = extent_manifest["longitude_latitude_extent"]
    plan = _bounded_dem_plan(extent)
    if plan["uncompressed_bytes"] > RAW_DEM_LIMIT:
        raise TerrainPackError("planned bounded DEM exceeds the 150 MB raw DEM ceiling")
    if plan["conservative_network_bytes"] > NETWORK_RETRIEVAL_LIMIT:
        raise TerrainPackError("planned HTTP ranges exceed the 250 MB network ceiling")

    gdal_translate = osgeo_root.resolve() / "bin" / "gdal_translate.exe"
    if not gdal_translate.is_file():
        raise TerrainPackError(f"gdal_translate not found: {gdal_translate}")
    partial = destination.with_name(destination.stem + ".partial.tif")
    _ensure_regular_new_file(partial)
    remote = "/vsicurl/" + DEM_URL
    command = [
        str(gdal_translate),
        "--config",
        "CPL_CURL_VERBOSE",
        "YES",
        "--config",
        "CPL_VSIL_CURL_ALLOWED_EXTENSIONS",
        ".tif",
        "--config",
        "GDAL_HTTP_MAX_RETRY",
        "2",
        "-projwin",
        str(extent["west"]),
        str(extent["north"]),
        str(extent["east"]),
        str(extent["south"]),
        "-projwin_srs",
        DEM_SOURCE_CRS,
        "-of",
        "GTiff",
        "-co",
        "TILED=YES",
        "-co",
        "COMPRESS=DEFLATE",
        "-co",
        "PREDICTOR=3",
        remote,
        str(partial),
    ]
    measured_network, _ = _run_range_limited_translate(command, partial)
    if partial.stat().st_size > RAW_DEM_LIMIT:
        partial.unlink()
        raise TerrainPackError("bounded DEM output exceeds the 150 MB ceiling")
    partial.replace(destination)
    raster = _raster_info(destination)
    if raster["maximum"] <= raster["minimum"]:
        raise TerrainPackError("bounded DEM is blank or all nodata")
    receipt = {
        "schema_id": "climateos.spatial-retrieval-receipt.v1",
        "retrieval_id": "QGIS-TERRAIN-DEM-001",
        "publisher": "Geoscience Australia",
        "product": DEM_PRODUCT,
        "product_id": DEM_PRODUCT_ID,
        "catalogue_id": DEM_CATALOGUE_ID,
        "layer": "dem_s",
        "source_url": DEM_URL,
        "retrieved_at": _utc_now(),
        "licence": DEM_LICENCE,
        "requested_extent": extent,
        "returned_extent": extent,
        "content_length": destination.stat().st_size,
        "measured_unique_http_range_bytes": measured_network,
        "network_measurement_note": (
            "sum of unique Content-Range responses observed by GDAL; zero means the HTTP stack did not expose range headers"
        ),
        "planned_conservative_network_bytes": plan["conservative_network_bytes"],
        "source_object_content_length": 38304075388,
        "source_object_etag": "34c2ac3927ece1035fd7dd588d8b127c-4567",
        "sha256": _sha256(destination),
        "local_path": destination.relative_to(layout["root"]).as_posix(),
        "raw_retained": True,
        "source_crs": DEM_SOURCE_CRS,
        "vertical_datum": DEM_VERTICAL_DATUM,
        "cell_size_degrees": DEM_CELL_SIZE_DEGREES,
        "nodata": DEM_NODATA,
        "raster": raster,
        "scientific_conclusion": "NONE",
    }
    _write_json_new(receipt_path, receipt)
    sizes = _enforce_workspace_sizes(layout)
    return {"dem_receipt": receipt, "workspace_sizes": sizes}


def _run_gdal_new_file(command: list[str], destination: Path) -> None:
    _ensure_regular_new_file(destination)
    partial = destination.with_name(destination.stem + ".partial" + destination.suffix)
    _ensure_regular_new_file(partial)
    adjusted = [str(partial) if item == "{OUTPUT}" else item for item in command]
    result = subprocess.run(adjusted, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if result.returncode != 0:
        if partial.exists():
            partial.unlink()
        raise TerrainPackError(f"GDAL derivation failed: {result.stderr or result.stdout}")
    if not partial.is_file() or partial.stat().st_size == 0:
        raise TerrainPackError("GDAL derivation produced no output")
    partial.replace(destination)


def derive_terrain(repo_root: Path, osgeo_root: Path) -> dict[str, object]:
    layout = _layout(repo_root)
    if not layout["bounded_dem"].is_file() or not layout["study_extent"].is_file():
        raise TerrainPackError("bounded DEM and 10 km study extent are required before derivation")
    manifest_path = layout["derivation_manifest"]
    _ensure_regular_new_file(manifest_path)
    terrain_root = layout["terrain_root"]
    projected_dem = terrain_root / PROJECTED_DEM_FILENAME
    hillshade = terrain_root / HILLSHADE_FILENAME
    slope = terrain_root / SLOPE_FILENAME
    for output in (projected_dem, hillshade, slope):
        _assert_confined(output, layout["root"])
        _ensure_regular_new_file(output)

    bin_root = osgeo_root.resolve() / "bin"
    gdalwarp = bin_root / "gdalwarp.exe"
    gdaldem = bin_root / "gdaldem.exe"
    if not gdalwarp.is_file() or not gdaldem.is_file():
        raise TerrainPackError("required gdalwarp/gdaldem executables are unavailable")
    common_creation = ["-co", "TILED=YES", "-co", "COMPRESS=DEFLATE", "-co", "PREDICTOR=3"]
    _run_gdal_new_file(
        [
            str(gdalwarp),
            "-overwrite",
            "-t_srs",
            TERRAIN_PROJECT_CRS,
            "-tr",
            str(TARGET_CELL_SIZE_METRES),
            str(TARGET_CELL_SIZE_METRES),
            "-tap",
            "-r",
            "bilinear",
            "-cutline",
            str(layout["study_extent"]),
            "-crop_to_cutline",
            "-dstnodata",
            "-9999",
            *common_creation,
            str(layout["bounded_dem"]),
            "{OUTPUT}",
        ],
        projected_dem,
    )
    _run_gdal_new_file(
        [
            str(gdaldem),
            "hillshade",
            str(projected_dem),
            "{OUTPUT}",
            "-az",
            str(HILLSHADE_AZIMUTH),
            "-alt",
            str(HILLSHADE_ALTITUDE),
            "-z",
            str(HILLSHADE_Z_FACTOR),
            "-compute_edges",
            "-co",
            "TILED=YES",
            "-co",
            "COMPRESS=DEFLATE",
        ],
        hillshade,
    )
    _run_gdal_new_file(
        [
            str(gdaldem),
            "slope",
            str(projected_dem),
            "{OUTPUT}",
            "-compute_edges",
            "-co",
            "TILED=YES",
            "-co",
            "COMPRESS=DEFLATE",
            "-co",
            "PREDICTOR=3",
        ],
        slope,
    )
    raster_info = {
        "dem": _raster_info(projected_dem),
        "hillshade": _raster_info(hillshade),
        "slope": _raster_info(slope),
    }
    if raster_info["dem"]["maximum"] <= raster_info["dem"]["minimum"]:
        raise TerrainPackError("projected DEM is blank")
    if raster_info["hillshade"]["maximum"] <= raster_info["hillshade"]["minimum"]:
        raise TerrainPackError("hillshade is blank")
    if raster_info["slope"]["maximum"] <= raster_info["slope"]["minimum"]:
        raise TerrainPackError("slope is blank")

    gdal, _, _ = _osgeo()
    files = {}
    for name, path in (("dem", projected_dem), ("hillshade", hillshade), ("slope", slope)):
        files[name] = {
            "local_path": path.relative_to(layout["root"]).as_posix(),
            "size": path.stat().st_size,
            "sha256": _sha256(path),
            "raster": raster_info[name],
        }
    manifest = {
        "schema_id": "climateos.qgis-terrain-derivation.v1",
        "created_at": _utc_now(),
        "source_dem_sha256": _sha256(layout["bounded_dem"]),
        "source_dem_product": DEM_PRODUCT,
        "source_crs": DEM_SOURCE_CRS,
        "target_crs": TERRAIN_PROJECT_CRS,
        "target_cell_size_metres": TARGET_CELL_SIZE_METRES,
        "reprojection": "gdalwarp bilinear, target-aligned pixels, cut to official locality + 10 km buffer",
        "hillshade": {
            "algorithm": "GDAL gdaldem hillshade",
            "azimuth_degrees": HILLSHADE_AZIMUTH,
            "altitude_degrees": HILLSHADE_ALTITUDE,
            "z_factor": HILLSHADE_Z_FACTOR,
            "edge_handling": "compute_edges",
        },
        "slope": {
            "algorithm": "GDAL gdaldem slope Horn",
            "units": SLOPE_UNITS,
            "nodata_handling": "input nodata -9999 retained",
            "edge_handling": "compute_edges",
            "horizontal_units": "metres",
            "vertical_units": "metres EGM96",
        },
        "contours": {"created": False, "reason": "optional layer omitted to keep the pack lightweight"},
        "gdal_version": gdal.VersionInfo("--version"),
        "files": files,
        "scientific_conclusion": "NONE",
        "risk_classification": "NONE",
    }
    _write_json_new(manifest_path, manifest)
    sizes = _enforce_workspace_sizes(layout)
    return {"derivation": manifest, "workspace_sizes": sizes}


def _terrain_qgis_api(osgeo_root: Path, profile: Path) -> dict[str, object]:
    api = _base_qgis_api(osgeo_root, profile)
    from qgis.PyQt.QtGui import QColor  # type: ignore[import-not-found]
    from qgis.core import (  # type: ignore[import-not-found]
        QgsColorRampShader,
        QgsRasterLayer,
        QgsRasterShader,
        QgsSingleBandGrayRenderer,
        QgsSingleBandPseudoColorRenderer,
    )

    api.update({name: value for name, value in locals().items() if name.startswith("Q")})
    return api


def _add_vector(api, project, group, path: Path, name: str):
    layer = api["QgsVectorLayer"](str(path), name, "ogr")
    if not layer.isValid():
        raise TerrainPackError(f"QGIS could not load vector layer: {path}")
    project.addMapLayer(layer, False)
    group.addLayer(layer)
    return layer


def _add_raster(api, project, group, path: Path, name: str):
    layer = api["QgsRasterLayer"](str(path), name, "gdal")
    if not layer.isValid():
        raise TerrainPackError(f"QGIS could not load raster layer: {path}")
    project.addMapLayer(layer, False)
    group.addLayer(layer)
    return layer


def _style_slope(api, layer, minimum: float, maximum: float) -> None:
    shader_function = api["QgsColorRampShader"]()
    shader_function.setColorRampType(api["QgsColorRampShader"].Interpolated)
    upper = max(30.0, float(maximum))
    items = [
        api["QgsColorRampShader"].ColorRampItem(0.0, api["QColor"]("#f7fcf5"), "0°"),
        api["QgsColorRampShader"].ColorRampItem(5.0, api["QColor"]("#c7e9c0"), "5°"),
        api["QgsColorRampShader"].ColorRampItem(15.0, api["QColor"]("#74c476"), "15°"),
        api["QgsColorRampShader"].ColorRampItem(30.0, api["QColor"]("#238b45"), "30°"),
        api["QgsColorRampShader"].ColorRampItem(upper, api["QColor"]("#00441b"), f"{upper:.1f}°"),
    ]
    shader_function.setColorRampItemList(items)
    raster_shader = api["QgsRasterShader"]()
    raster_shader.setRasterShaderFunction(shader_function)
    renderer = api["QgsSingleBandPseudoColorRenderer"](
        layer.dataProvider(), 1, raster_shader
    )
    renderer.setClassificationMin(float(minimum))
    renderer.setClassificationMax(float(maximum))
    layer.setRenderer(renderer)


def build_project(repo_root: Path, osgeo_root: Path) -> dict[str, object]:
    layout = _layout(repo_root)
    project_path = layout["project"]
    project_manifest_path = layout["project_manifest"]
    _ensure_regular_new_file(project_path)
    _ensure_regular_new_file(project_manifest_path)
    required = {
        "boundary": layout["boundary"],
        "dem": layout["terrain_root"] / PROJECTED_DEM_FILENAME,
        "hillshade": layout["terrain_root"] / HILLSHADE_FILENAME,
        "slope": layout["terrain_root"] / SLOPE_FILENAME,
    }
    missing = [str(path) for path in required.values() if not path.is_file()]
    if missing:
        raise TerrainPackError(f"terrain project inputs missing: {missing}")
    ensure_synthetic_anchor_files(layout["root"] / "local_anchor")
    extent = json.loads(layout["extent_manifest"].read_text(encoding="utf-8"))
    derivation = json.loads(layout["derivation_manifest"].read_text(encoding="utf-8"))

    profile = layout["root"] / ".qgis-profile-terrain"
    profile.mkdir(exist_ok=True)
    os.chdir(layout["root"])
    api = _terrain_qgis_api(osgeo_root, profile)
    application = _new_qgis_application(api, osgeo_root)
    project = None
    try:
        project = api["QgsProject"]()
        project.setFilePathStorage(api["Qgis"].FilePathType.Relative)
        project_crs = api["QgsCoordinateReferenceSystem"](TERRAIN_PROJECT_CRS)
        project.setCrs(project_crs)
        metadata = api["QgsProjectMetadata"]()
        metadata.setTitle("Cooma Spatial Foundation v0.2 Terrain")
        metadata.setAuthor("ClimateOS — Founder-authorized bounded public-data pack")
        metadata.setAbstract(
            "BOUNDED PUBLIC DATA / TERRAIN OBSERVATION ONLY / NO SCIENTIFIC "
            "CONCLUSION. Administrative locality, DEM-S, hillshade and slope are "
            "orientation layers, not hydrological, risk or engineering evidence."
        )
        project.setMetadata(metadata)
        root_group = project.layerTreeRoot()
        groups = {name: root_group.addGroup(name) for name in PROJECT_LAYER_GROUPS}
        groups["06_PUBLIC_INFRASTRUCTURE_LATER"].setItemVisibilityChecked(False)
        groups["99_DISABLED_LATER_LAYERS"].setItemVisibilityChecked(False)
        synthetic_layers = _populate_project(
            api, project, groups, layout["root"] / "local_anchor"
        )
        terrain_info = synthetic_layers[3]
        groups["02_TERRAIN"].findLayer(terrain_info.id()).setItemVisibilityChecked(False)

        boundary = _add_vector(api, project, groups["01_BOUNDARIES"], required["boundary"], TERRAIN_LAYER_NAMES[0])
        boundary.renderer().setSymbol(
            api["QgsFillSymbol"].createSimple(
                {
                    "color": "255,255,255,0",
                    "outline_color": "33,76,63,255",
                    "outline_width": "1.1",
                }
            )
        )
        dem = _add_raster(api, project, groups["02_TERRAIN"], required["dem"], TERRAIN_LAYER_NAMES[1])
        hillshade = _add_raster(
            api, project, groups["02_TERRAIN"], required["hillshade"], TERRAIN_LAYER_NAMES[2]
        )
        slope = _add_raster(api, project, groups["02_TERRAIN"], required["slope"], TERRAIN_LAYER_NAMES[3])
        dem.setRenderer(api["QgsSingleBandGrayRenderer"](dem.dataProvider(), 1))
        hillshade.setRenderer(api["QgsSingleBandGrayRenderer"](hillshade.dataProvider(), 1))
        slope_info = derivation["files"]["slope"]["raster"]
        _style_slope(api, slope, slope_info["minimum"], slope_info["maximum"])
        groups["02_TERRAIN"].findLayer(dem.id()).setItemVisibilityChecked(False)
        groups["02_TERRAIN"].findLayer(hillshade.id()).setItemVisibilityChecked(True)
        groups["02_TERRAIN"].findLayer(slope.id()).setItemVisibilityChecked(False)

        variables = {
            "climateos_scope_status": "OFFICIAL_COOMA_LOCALITY_PLUS_10KM_BUFFER",
            "climateos_project_state": "BOUNDED_PUBLIC_DATA_TERRAIN_OBSERVATION_ONLY",
            "climateos_scientific_conclusion": SCIENTIFIC_CONCLUSION,
            "climateos_boundary_identity": "COOMA OBJECTID 16701",
            "climateos_hydrology_status": "NOT_AUTHORIZED_NOT_RETRIEVED",
            "climateos_project_crs": TERRAIN_PROJECT_CRS,
        }
        for name, value in variables.items():
            api["QgsExpressionContextUtils"].setProjectVariable(project, name, value)

        projected_extent = extent["projected_extent"]
        boundary_extent = extent["boundary_projected_extent"]
        bookmark_specs = (
            ("Cooma Locality", boundary_extent),
            ("Cooma + 10 km Terrain", projected_extent),
        )
        manager = project.bookmarkManager()
        for index, (name, values) in enumerate(bookmark_specs, start=1):
            rectangle = api["QgsRectangle"](
                values["west"], values["south"], values["east"], values["north"]
            )
            bookmark = api["QgsBookmark"]()
            bookmark.setId(f"climateos-terrain-bookmark-{index}")
            bookmark.setName(name)
            bookmark.setGroup("COOMA TERRAIN CONTEXT — OBSERVATION ONLY")
            bookmark.setExtent(api["QgsReferencedRectangle"](rectangle, project_crs))
            if not manager.addBookmark(bookmark):
                raise TerrainPackError(f"failed to add terrain bookmark: {name}")
        full_rectangle = api["QgsRectangle"](
            projected_extent["west"],
            projected_extent["south"],
            projected_extent["east"],
            projected_extent["north"],
        )
        referenced = api["QgsReferencedRectangle"](full_rectangle, project_crs)
        project.viewSettings().setDefaultViewExtent(referenced)
        project.viewSettings().setPresetFullExtent(referenced)
        if not project.write(str(project_path)):
            raise TerrainPackError("QGIS refused to write the terrain project")
    finally:
        if project is not None:
            project.clear()
            del project
        application.exitQgis()
        del application

    manifest = {
        "schema_id": "climateos.qgis-terrain-project.v1",
        "created_at": _utc_now(),
        "project_filename": TERRAIN_PROJECT_FILENAME,
        "project_sha256": _sha256(project_path),
        "project_crs": TERRAIN_PROJECT_CRS,
        "layer_groups": list(PROJECT_LAYER_GROUPS),
        "terrain_layers": list(TERRAIN_LAYER_NAMES),
        "bookmarks": ["Cooma Locality", "Cooma + 10 km Terrain"],
        "network_basemap": "NONE",
        "hydrology": "NOT_AUTHORIZED_NOT_RETRIEVED",
        "scientific_conclusion": "NONE",
    }
    _write_json_new(project_manifest_path, manifest)
    sizes = _enforce_workspace_sizes(layout)
    return {"project": manifest, "project_path": str(project_path), "workspace_sizes": sizes}


def verify(repo_root: Path, osgeo_root: Path) -> dict[str, object]:
    layout = _layout(repo_root)
    required_files = (
        layout["boundary"],
        layout["bounded_dem"],
        layout["terrain_root"] / PROJECTED_DEM_FILENAME,
        layout["terrain_root"] / HILLSHADE_FILENAME,
        layout["terrain_root"] / SLOPE_FILENAME,
        layout["project"],
        layout["boundary_receipt"],
        layout["dem_receipt"],
        layout["derivation_manifest"],
        layout["project_manifest"],
    )
    missing = [str(path) for path in required_files if not path.is_file()]
    if missing:
        raise TerrainPackError(f"terrain verification files missing: {missing}")
    boundary_payload = json.loads(layout["boundary"].read_text(encoding="utf-8"))
    _boundary_feature(boundary_payload)
    dem_receipt = json.loads(layout["dem_receipt"].read_text(encoding="utf-8"))
    if dem_receipt["sha256"] != _sha256(layout["bounded_dem"]):
        raise TerrainPackError("bounded DEM checksum does not match receipt")
    derivation = json.loads(layout["derivation_manifest"].read_text(encoding="utf-8"))
    for name, filename in (
        ("dem", PROJECTED_DEM_FILENAME),
        ("hillshade", HILLSHADE_FILENAME),
        ("slope", SLOPE_FILENAME),
    ):
        path = layout["terrain_root"] / filename
        if derivation["files"][name]["sha256"] != _sha256(path):
            raise TerrainPackError(f"derived {name} checksum mismatch")
        raster = _raster_info(path)
        if raster["maximum"] <= raster["minimum"]:
            raise TerrainPackError(f"derived {name} is blank")
    if derivation["slope"]["units"] != "degrees":
        raise TerrainPackError("slope derivation is not in degrees")
    if derivation["scientific_conclusion"] != "NONE":
        raise TerrainPackError("terrain derivation contains a scientific conclusion")

    profile = layout["root"] / ".qgis-profile-terrain-verify"
    profile.mkdir(exist_ok=True)
    os.chdir(layout["root"])
    api = _terrain_qgis_api(osgeo_root, profile)
    application = _new_qgis_application(api, osgeo_root)
    project = None
    try:
        project = api["QgsProject"]()
        if not project.read(str(layout["project"])):
            raise TerrainPackError("QGIS could not reopen the terrain project")
        group_names = [child.name() for child in project.layerTreeRoot().children()]
        if group_names != list(PROJECT_LAYER_GROUPS):
            raise TerrainPackError(f"terrain project group mismatch: {group_names}")
        layers = {layer.name(): layer for layer in project.mapLayers().values()}
        for name in (*TERRAIN_LAYER_NAMES, WATER_INFO_LAYER, TERRAIN_INFO_LAYER):
            if name not in layers:
                raise TerrainPackError(f"terrain project layer missing: {name}")
        invalid = [name for name, layer in layers.items() if not layer.isValid()]
        if invalid:
            raise TerrainPackError(f"broken terrain project layers: {invalid}")
        for name, layer in layers.items():
            source = layer.source().split("|", 1)[0]
            if source.lower().startswith(("http://", "https://")):
                raise TerrainPackError(f"network-backed layer is prohibited: {name}")
        if project.crs().authid() != TERRAIN_PROJECT_CRS:
            raise TerrainPackError("terrain project CRS is not EPSG:7855")
        if project.filePathStorage() != api["Qgis"].FilePathType.Relative:
            raise TerrainPackError("terrain project paths are not relative")
    finally:
        if project is not None:
            project.clear()
            del project
        application.exitQgis()
        del application

    with zipfile.ZipFile(layout["project"]) as archive:
        qgs_names = [name for name in archive.namelist() if name.endswith(".qgs")]
        if len(qgs_names) != 1:
            raise TerrainPackError("terrain QGZ must contain exactly one QGS document")
        xml = archive.read(qgs_names[0]).decode("utf-8")
    provider_xml = xml.lower().replace("http://mrcc.com/qgis.dtd", "")
    for prohibited in ("type=xyz", "<provider>wms</provider>", "<provider>wfs</provider>"):
        if prohibited in provider_xml:
            raise TerrainPackError(f"network provider found in terrain project: {prohibited}")
    project_manifest = json.loads(layout["project_manifest"].read_text(encoding="utf-8"))
    if project_manifest["project_sha256"] != _sha256(layout["project"]):
        raise TerrainPackError("terrain project checksum mismatch")
    sizes = _enforce_workspace_sizes(layout)
    return {
        "project_path": str(layout["project"]),
        "project_sha256": _sha256(layout["project"]),
        "broken_layer_count": 0,
        "network_basemap_count": 0,
        "official_boundary_feature_count": 1,
        "dem_present": True,
        "hillshade_present": True,
        "slope_degrees_present": True,
        "hydrology_status": "NOT_AUTHORIZED_NOT_RETRIEVED",
        "scientific_conclusion": "NONE",
        "workspace_sizes": sizes,
    }


def plan(repo_root: Path) -> dict[str, object]:
    load_source_registry()
    layout = _layout(repo_root)
    return {
        "boundary_source_url": BOUNDARY_QUERY_URL,
        "boundary_where": BOUNDARY_WHERE,
        "boundary_destination": str(layout["boundary"]),
        "dem_source_url": DEM_URL,
        "dem_destination": str(layout["bounded_dem"]),
        "project_destination": str(layout["project"]),
        "project_crs": TERRAIN_PROJECT_CRS,
        "buffer_metres": BUFFER_METRES,
        "size_limits": size_limits(),
        "scientific_conclusion": "NONE",
        "combined_unattended_retrieval_available": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "action",
        choices=("plan", "retrieve-boundary", "retrieve-dem", "derive", "build-project", "verify"),
    )
    parser.add_argument("--osgeo-root", default="D:\\")
    args = parser.parse_args(argv)
    try:
        repo_root = _repo_root()
        if args.action == "plan":
            result = plan(repo_root)
        elif args.action == "retrieve-boundary":
            result = retrieve_boundary(repo_root)
        elif args.action == "retrieve-dem":
            result = retrieve_dem(repo_root, Path(args.osgeo_root))
        elif args.action == "derive":
            result = derive_terrain(repo_root, Path(args.osgeo_root))
        elif args.action == "build-project":
            result = build_project(repo_root, Path(args.osgeo_root))
        else:
            result = verify(repo_root, Path(args.osgeo_root))
    except (
        OSError,
        ValueError,
        KeyError,
        json.JSONDecodeError,
        TerrainPackError,
        SpatialWorkspaceError,
        SpatialProjectError,
    ) as exc:
        print(json.dumps({"status": "ERROR", "error": str(exc)}, ensure_ascii=False))
        return 1
    print(json.dumps({"status": "PASS", **result}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
