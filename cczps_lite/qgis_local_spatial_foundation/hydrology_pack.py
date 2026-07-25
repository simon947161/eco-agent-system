"""Build the Founder-authorized bounded Cooma Geofabric hydrology pack.

Network access is confined to four closed BOM FeatureServer layers and the
existing Cooma-locality-plus-10-kilometre extent. Generated spatial data stays
inside the git-ignored QGIS runtime workspace.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import zipfile

from .contract import PROJECT_LAYER_GROUPS, SCIENTIFIC_CONCLUSION, WATER_INFO_LAYER
from .hydrology_contract import (
    AUTHORIZED_LONGITUDE_LATITUDE_EXTENT,
    DERIVED_FILES,
    DERIVED_HYDROLOGY_LIMIT,
    HYDROLOGY_ATTRIBUTION,
    HYDROLOGY_BOOKMARKS,
    HYDROLOGY_FEATURE_SCALE,
    HYDROLOGY_LAYER_NAMES,
    HYDROLOGY_LICENCE,
    HYDROLOGY_METADATA_DATE,
    HYDROLOGY_PRODUCT,
    HYDROLOGY_PROJECT_CRS,
    HYDROLOGY_PROJECT_FILENAME,
    HYDROLOGY_PUBLISHER,
    HYDROLOGY_SERVICE,
    HYDROLOGY_SOURCE_CRS,
    HYDROLOGY_SOURCES,
    HYDROLOGY_VERSION,
    HYDROLOGY_WORKSPACE_DIRECTORIES,
    NETWORK_RETRIEVAL_LIMIT,
    RAW_HYDROLOGY_LIMIT,
    STACKED_PR_BASE,
    TERRAIN_BASE_HEAD,
    WORKSPACE_LIMIT,
    hydrology_size_limits,
)
from .project_builder import SpatialProjectError, _new_qgis_application
from .terrain_contract import (
    HILLSHADE_FILENAME,
    PROJECTED_DEM_FILENAME,
    SLOPE_FILENAME,
    STUDY_EXTENT_FILENAME,
    STUDY_EXTENT_MANIFEST,
    TERRAIN_LAYER_NAMES,
    TERRAIN_PROJECT_FILENAME,
)
from .terrain_pack import _terrain_qgis_api
from .workspace import SpatialWorkspaceError, ensure_local_workspace


class HydrologyPackError(RuntimeError):
    """Raised when a source, extent, overwrite, path or project gate fails."""


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _ensure_new_file(path: Path) -> None:
    if path.exists() or path.is_symlink():
        raise HydrologyPackError(f"new-file-only overwrite refused: {path}")


def _assert_confined(path: Path, root: Path) -> None:
    resolved = path.resolve()
    controlled = root.resolve()
    if resolved != controlled and controlled not in resolved.parents:
        raise HydrologyPackError(f"path escapes controlled QGIS workspace: {path}")
    current = resolved.parent
    while current != controlled.parent:
        if current.exists() and current.is_symlink():
            raise HydrologyPackError(f"controlled path contains symlink: {current}")
        if current == controlled:
            break
        current = current.parent


def _write_json_new(path: Path, payload: object) -> None:
    _ensure_new_file(path)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def _directory_size(path: Path) -> int:
    return sum(item.stat().st_size for item in path.rglob("*") if item.is_file())


def _layout(repo_root: Path) -> dict[str, object]:
    workspace = ensure_local_workspace(repo_root)
    root = workspace["root"]
    for relative in HYDROLOGY_WORKSPACE_DIRECTORIES:
        destination = root / relative
        _assert_confined(destination, root)
        destination.mkdir(parents=True, exist_ok=True)
    raw = {
        source["id"]: root / "source_data" / "hydrology" / source["filename"]
        for source in HYDROLOGY_SOURCES
    }
    derived = {
        key: root / "derived_data" / "hydrology" / filename
        for key, filename in DERIVED_FILES.items()
    }
    return {
        "root": root,
        "raw": raw,
        "derived": derived,
        "terrain_project": root / "project" / TERRAIN_PROJECT_FILENAME,
        "project": root / "project" / HYDROLOGY_PROJECT_FILENAME,
        "study_extent": root / "derived_data" / "terrain" / STUDY_EXTENT_FILENAME,
        "extent_manifest": root / "manifests" / "derivation" / STUDY_EXTENT_MANIFEST,
        "retrieval_manifest": root / "manifests" / "retrieval" / "cooma_hydrology_retrieval.json",
        "derivation_manifest": root / "manifests" / "derivation" / "cooma_hydrology_derivation.json",
        "project_manifest": root / "manifests" / "derivation" / "cooma_hydrology_project.json",
    }


def _workspace_sizes(layout: dict[str, object]) -> dict[str, int]:
    root = layout["root"]
    sizes = {
        "raw_hydrology": _directory_size(root / "source_data" / "hydrology"),
        "derived_hydrology": _directory_size(root / "derived_data" / "hydrology"),
        "workspace": _directory_size(root),
    }
    limits = hydrology_size_limits()
    for key, observed in sizes.items():
        if observed > limits[key]:
            raise HydrologyPackError(f"{key} size ceiling exceeded: {observed} > {limits[key]}")
    return sizes


def load_source_registry(package_root: Path | None = None) -> dict[str, object]:
    root = package_root or Path(__file__).resolve().parent
    registry = json.loads((root / "hydrology_source_registry.json").read_text(encoding="utf-8"))
    if registry.get("registry_status") != "CLOSED_FOUNDER_AUTHORIZED":
        raise HydrologyPackError("hydrology source registry is not closed and authorized")
    if registry.get("scientific_conclusion") != "NONE":
        raise HydrologyPackError("hydrology source registry contains a scientific conclusion")
    if registry.get("version") != HYDROLOGY_VERSION:
        raise HydrologyPackError("hydrology source version mismatch")
    if registry.get("licence") != HYDROLOGY_LICENCE:
        raise HydrologyPackError("hydrology source licence mismatch")
    layers = registry.get("layers")
    if not isinstance(layers, list) or [item.get("id") for item in layers] != [6, 31, 33, 27]:
        raise HydrologyPackError("hydrology layer registry is not the closed four-layer set")
    return registry


def _query_parameters() -> dict[str, str]:
    extent = AUTHORIZED_LONGITUDE_LATITUDE_EXTENT
    return {
        "f": "geojson",
        "where": "1=1",
        "outFields": "*",
        "returnGeometry": "true",
        "geometry": f'{extent["west"]},{extent["south"]},{extent["east"]},{extent["north"]}',
        "geometryType": "esriGeometryEnvelope",
        "inSR": "4326",
        "outSR": "4283",
        "spatialRel": "esriSpatialRelIntersects",
    }


def _coordinate_extent(payload: dict[str, object]) -> dict[str, float] | None:
    values: list[tuple[float, float]] = []

    def walk(item: object) -> None:
        if isinstance(item, list):
            if len(item) >= 2 and all(isinstance(value, (int, float)) for value in item[:2]):
                values.append((float(item[0]), float(item[1])))
            else:
                for child in item:
                    walk(child)

    for feature in payload.get("features", []):
        if isinstance(feature, dict) and isinstance(feature.get("geometry"), dict):
            walk(feature["geometry"].get("coordinates"))
    if not values:
        return None
    xs, ys = zip(*values)
    return {"west": min(xs), "east": max(xs), "south": min(ys), "north": max(ys)}


def _validate_geojson(payload: dict[str, object], source: dict[str, object]) -> int:
    if payload.get("type") != "FeatureCollection":
        raise HydrologyPackError(f'{source["id"]} response is not a GeoJSON FeatureCollection')
    features = payload.get("features")
    if not isinstance(features, list):
        raise HydrologyPackError(f'{source["id"]} response has no feature list')
    for feature in features:
        if not isinstance(feature, dict) or feature.get("type") != "Feature":
            raise HydrologyPackError(f'{source["id"]} contains a non-Feature object')
        if not isinstance(feature.get("geometry"), dict):
            raise HydrologyPackError(f'{source["id"]} contains missing geometry')
        if not isinstance(feature.get("properties"), dict):
            raise HydrologyPackError(f'{source["id"]} contains missing properties')
    return len(features)


def retrieve(repo_root: Path) -> dict[str, object]:
    registry = load_source_registry()
    layout = _layout(repo_root)
    destinations = list(layout["raw"].values()) + [layout["retrieval_manifest"]]
    for path in destinations:
        _assert_confined(path, layout["root"])
        _ensure_new_file(path)

    parameters = _query_parameters()
    receipts: list[dict[str, object]] = []
    network_bytes = 0
    for source in HYDROLOGY_SOURCES:
        destination = layout["raw"][source["id"]]
        source_url = f'{HYDROLOGY_SERVICE}/{source["layer_id"]}/query?' + urlencode(parameters)
        request = Request(source_url, headers={"User-Agent": "ClimateOS-QGIS-Hydrology-Pack/1.0"})
        remaining = NETWORK_RETRIEVAL_LIMIT - network_bytes
        with urlopen(request, timeout=120) as response:  # nosec B310 - closed HTTPS registry
            declared = response.headers.get("Content-Length")
            if declared is not None and int(declared) > remaining:
                raise HydrologyPackError("declared hydrology response exceeds network ceiling")
            content = response.read(min(remaining, RAW_HYDROLOGY_LIMIT) + 1)
        if len(content) > remaining:
            raise HydrologyPackError("total hydrology network retrieval exceeded 150 MB")
        if len(content) > RAW_HYDROLOGY_LIMIT:
            raise HydrologyPackError("single hydrology response exceeded raw retention ceiling")
        payload = json.loads(content.decode("utf-8"))
        feature_count = _validate_geojson(payload, source)
        with destination.open("xb") as handle:
            handle.write(content)
        network_bytes += len(content)
        receipts.append(
            {
                "source_id": source["id"],
                "publisher": HYDROLOGY_PUBLISHER,
                "product": HYDROLOGY_PRODUCT,
                "version": HYDROLOGY_VERSION,
                "product_component": source["product_component"],
                "layer_id": source["layer_id"],
                "layer": source["layer"],
                "source_url": source_url,
                "licence": HYDROLOGY_LICENCE,
                "attribution": HYDROLOGY_ATTRIBUTION,
                "retrieved_at": _utc_now(),
                "requested_extent": AUTHORIZED_LONGITUDE_LATITUDE_EXTENT,
                "returned_extent": _coordinate_extent(payload),
                "source_crs": HYDROLOGY_SOURCE_CRS,
                "feature_count": feature_count,
                "file_size": len(content),
                "sha256": _sha256(destination),
                "local_path": destination.relative_to(layout["root"]).as_posix(),
                "scientific_conclusion": "NONE",
            }
        )
    manifest = {
        "schema_id": "climateos.qgis-hydrology-retrieval.v1",
        "created_at": _utc_now(),
        "access_method": "bounded ArcGIS FeatureServer GeoJSON queries",
        "network_retrieval_bytes": network_bytes,
        "network_retrieval_limit": NETWORK_RETRIEVAL_LIMIT,
        "source_registry": registry["schema_id"],
        "receipts": receipts,
        "scientific_conclusion": "NONE",
    }
    _write_json_new(layout["retrieval_manifest"], manifest)
    return {"retrieval": manifest, "workspace_sizes": _workspace_sizes(layout)}


def _osgeo():
    from osgeo import ogr, osr  # type: ignore[import-not-found]

    ogr.UseExceptions()
    return ogr, osr


def _spatial_reference(osr, epsg: int):
    reference = osr.SpatialReference()
    reference.ImportFromEPSG(epsg)
    if hasattr(reference, "SetAxisMappingStrategy"):
        reference.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
    return reference


def _clip_geometry(layout: dict[str, object]):
    ogr, osr = _osgeo()
    source = ogr.Open(str(layout["study_extent"]), 0)
    if source is None:
        raise HydrologyPackError("existing authorized terrain extent could not be opened")
    layer = source.GetLayer(0)
    feature = layer.GetNextFeature()
    geometry = feature.GetGeometryRef().Clone() if feature else None
    source = None
    if geometry is None or geometry.IsEmpty():
        raise HydrologyPackError("existing authorized terrain extent is empty")
    geometry.AssignSpatialReference(_spatial_reference(osr, 7855))
    return geometry


def _copy_clipped(
    source_path: Path,
    destination: Path,
    layer_name: str,
    predicate,
    clip_geometry,
) -> dict[str, object]:
    ogr, osr = _osgeo()
    source_dataset = ogr.Open(str(source_path), 0)
    if source_dataset is None:
        raise HydrologyPackError(f"GDAL could not open hydrology source: {source_path}")
    source_layer = source_dataset.GetLayer(0)
    source_definition = source_layer.GetLayerDefn()
    source_crs = _spatial_reference(osr, 4283)
    target_crs = _spatial_reference(osr, 7855)
    transform = osr.CoordinateTransformation(source_crs, target_crs)
    _ensure_new_file(destination)
    output_dataset = ogr.GetDriverByName("GPKG").CreateDataSource(str(destination))
    # Clipping can split a LineString/Polygon into a multi-part geometry. A
    # generic GPKG geometry declaration preserves that valid result without
    # mis-declaring the layer as single-part.
    output_layer = output_dataset.CreateLayer(layer_name, target_crs, ogr.wkbUnknown)
    for index in range(source_definition.GetFieldCount()):
        output_layer.CreateField(source_definition.GetFieldDefn(index))
    output_definition = output_layer.GetLayerDefn()
    source_count = 0
    output_count = 0
    for source_feature in source_layer:
        source_count += 1
        properties = {
            source_definition.GetFieldDefn(index).GetName(): source_feature.GetField(index)
            for index in range(source_definition.GetFieldCount())
        }
        if not predicate(properties):
            continue
        geometry = source_feature.GetGeometryRef()
        if geometry is None or geometry.IsEmpty():
            continue
        projected = geometry.Clone()
        projected.AssignSpatialReference(source_crs)
        projected.Transform(transform)
        clipped = projected.Intersection(clip_geometry)
        if clipped is None or clipped.IsEmpty():
            continue
        output_feature = ogr.Feature(output_definition)
        for index in range(source_definition.GetFieldCount()):
            output_feature.SetField(index, source_feature.GetField(index))
        output_feature.SetGeometry(clipped)
        output_layer.CreateFeature(output_feature)
        output_feature = None
        output_count += 1
    output_layer.SyncToDisk()
    output_layer = None
    output_dataset = None
    source_dataset = None
    return {
        "source_feature_count": source_count,
        "derived_feature_count": output_count,
        "crs": HYDROLOGY_PROJECT_CRS,
        "file_size": destination.stat().st_size,
        "sha256": _sha256(destination),
    }


def derive(repo_root: Path) -> dict[str, object]:
    layout = _layout(repo_root)
    required = [*layout["raw"].values(), layout["study_extent"], layout["extent_manifest"]]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise HydrologyPackError(f"hydrology derivation inputs missing: {missing}")
    for path in [*layout["derived"].values(), layout["derivation_manifest"]]:
        _assert_confined(path, layout["root"])
        _ensure_new_file(path)

    clip = _clip_geometry(layout)
    specifications = (
        (
            "main_watercourses",
            "main_watercourses",
            "network_stream",
            lambda fields: fields.get("hierarchy") == "Major",
            "official hierarchy = Major",
        ),
        (
            "secondary_streams",
            "secondary_streams",
            "network_stream",
            lambda fields: fields.get("hierarchy") == "Minor",
            "official hierarchy = Minor",
        ),
        (
            "catchment_context",
            "contracted_catchment_context",
            "contracted_catchment",
            lambda fields: True,
            "official AHGFContractedCatchment; no supply-catchment interpretation",
        ),
        (
            "subcatchment_context",
            "stream_segment_catchment_context",
            "stream_segment_catchment",
            lambda fields: True,
            "official AHGFCatchment stream-segment units; subcatchment is a project display label",
        ),
        (
            "named_water_features",
            "named_water_features",
            "waterbody",
            lambda fields: bool(str(fields.get("name") or "").strip()),
            "official waterbodies filtered only where the source Name field is populated",
        ),
    )
    files: dict[str, object] = {}
    for key, layer_name, source_id, predicate, classification in specifications:
        result = _copy_clipped(
            layout["raw"][source_id], layout["derived"][key], layer_name, predicate, clip
        )
        files[key] = {
            **result,
            "source_id": source_id,
            "local_path": layout["derived"][key].relative_to(layout["root"]).as_posix(),
            "clipping": "intersected with existing official COOMA locality plus 10 km EPSG:7855 polygon",
            "reprojection": f"{HYDROLOGY_SOURCE_CRS} to {HYDROLOGY_PROJECT_CRS}",
            "classification": classification,
        }
    sizes = _workspace_sizes(layout)
    manifest = {
        "schema_id": "climateos.qgis-hydrology-derivation.v1",
        "created_at": _utc_now(),
        "requested_extent": AUTHORIZED_LONGITUDE_LATITUDE_EXTENT,
        "clip_source": layout["study_extent"].relative_to(layout["root"]).as_posix(),
        "files": files,
        "classification_policy": "PRESERVE_OFFICIAL_GEOFABRIC_FIELDS_NO_FABRICATED_CLASSIFICATION",
        "locality_is_catchment": False,
        "council_boundary_present": False,
        "scientific_conclusion": "NONE",
        "workspace_sizes": sizes,
    }
    _write_json_new(layout["derivation_manifest"], manifest)
    return {"derivation": manifest, "workspace_sizes": _workspace_sizes(layout)}


def _add_vector(api, project, group, path: Path, name: str):
    layer = api["QgsVectorLayer"](str(path), name, "ogr")
    if not layer.isValid():
        raise HydrologyPackError(f"QGIS could not load hydrology layer: {path}")
    project.addMapLayer(layer, False)
    group.addLayer(layer)
    return layer


def _hydrology_qgis_api(osgeo_root: Path, profile: Path) -> dict[str, object]:
    api = _terrain_qgis_api(osgeo_root, profile)
    from qgis.core import QgsLineSymbol  # type: ignore[import-not-found]

    api["QgsLineSymbol"] = QgsLineSymbol
    return api


def build_project(repo_root: Path, osgeo_root: Path) -> dict[str, object]:
    layout = _layout(repo_root)
    required = [layout["terrain_project"], layout["extent_manifest"], *layout["derived"].values()]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise HydrologyPackError(f"hydrology project inputs missing: {missing}")
    for path in (layout["project"], layout["project_manifest"]):
        _assert_confined(path, layout["root"])
        _ensure_new_file(path)

    extent = json.loads(layout["extent_manifest"].read_text(encoding="utf-8"))["projected_extent"]
    profile = layout["root"] / ".qgis-profile-hydrology"
    profile.mkdir(exist_ok=True)
    os.chdir(layout["root"])
    api = _hydrology_qgis_api(osgeo_root, profile)
    application = _new_qgis_application(api, osgeo_root)
    project = None
    try:
        project = api["QgsProject"]()
        if not project.read(str(layout["terrain_project"])):
            raise HydrologyPackError("QGIS could not open the v0.2 terrain project")
        project.setFilePathStorage(api["Qgis"].FilePathType.Relative)
        metadata = project.metadata()
        metadata.setTitle("Cooma Spatial Foundation v0.3 Hydrology")
        metadata.setAuthor("ClimateOS — Founder-authorized bounded public-data pack")
        metadata.setAbstract(
            "STACKED ON UNMERGED PR95 / BOUNDED PUBLIC DATA / SPATIAL OBSERVATION ONLY / "
            "NO SCIENTIFIC CONCLUSION. Geofabric watercourses and catchments support GIS "
            "orientation, not water availability, flood, drought, supply or engineering conclusions."
        )
        project.setMetadata(metadata)
        groups = {
            child.name(): child
            for child in project.layerTreeRoot().children()
            if hasattr(child, "name")
        }
        if list(groups) != list(PROJECT_LAYER_GROUPS):
            raise HydrologyPackError("v0.2 terrain project group structure changed")
        water_group = groups["03_WATER"]
        existing_info = next(
            (layer for layer in project.mapLayers().values() if layer.name() == WATER_INFO_LAYER), None
        )
        if existing_info is None:
            raise HydrologyPackError("terrain hydrology placeholder layer is missing")
        existing_info.setName(HYDROLOGY_LAYER_NAMES[5])
        existing_info.setCustomProperty("climateos_source", f"{HYDROLOGY_PRODUCT} {HYDROLOGY_VERSION}")
        existing_info.setCustomProperty(
            "climateos_limitations",
            "No water availability, drought, supply, flood, wastewater, fire or engineering conclusion.",
        )
        water_group.findLayer(existing_info.id()).setItemVisibilityChecked(False)

        main = _add_vector(
            api, project, water_group, layout["derived"]["main_watercourses"], HYDROLOGY_LAYER_NAMES[0]
        )
        secondary = _add_vector(
            api, project, water_group, layout["derived"]["secondary_streams"], HYDROLOGY_LAYER_NAMES[1]
        )
        catchment = _add_vector(
            api, project, water_group, layout["derived"]["catchment_context"], HYDROLOGY_LAYER_NAMES[2]
        )
        subcatchment = _add_vector(
            api, project, water_group, layout["derived"]["subcatchment_context"], HYDROLOGY_LAYER_NAMES[3]
        )
        waterbody = _add_vector(
            api, project, water_group, layout["derived"]["named_water_features"], HYDROLOGY_LAYER_NAMES[4]
        )
        main.renderer().setSymbol(
            api["QgsLineSymbol"].createSimple({"color": "25,94,166,255", "width": "1.15"})
        )
        secondary.renderer().setSymbol(
            api["QgsLineSymbol"].createSimple({"color": "91,155,213,220", "width": "0.55"})
        )
        catchment.renderer().setSymbol(
            api["QgsFillSymbol"].createSimple(
                {"color": "94,164,214,28", "outline_color": "43,122,176,220", "outline_width": "0.7"}
            )
        )
        subcatchment.renderer().setSymbol(
            api["QgsFillSymbol"].createSimple(
                {"color": "255,255,255,0", "outline_color": "107,174,214,130", "outline_width": "0.25"}
            )
        )
        waterbody.renderer().setSymbol(
            api["QgsFillSymbol"].createSimple(
                {"color": "107,174,214,170", "outline_color": "33,113,181,255", "outline_width": "0.4"}
            )
        )
        water_group.findLayer(main.id()).setItemVisibilityChecked(True)
        water_group.findLayer(secondary.id()).setItemVisibilityChecked(False)
        water_group.findLayer(catchment.id()).setItemVisibilityChecked(True)
        water_group.findLayer(subcatchment.id()).setItemVisibilityChecked(False)
        water_group.findLayer(waterbody.id()).setItemVisibilityChecked(True)

        for name, value in {
            "climateos_hydrology_source": f"{HYDROLOGY_PRODUCT} {HYDROLOGY_VERSION}",
            "climateos_hydrology_extent": "OFFICIAL_COOMA_LOCALITY_PLUS_10KM_BUFFER",
            "climateos_hydrology_classification": "OFFICIAL_GEOFABRIC_FIELDS_ONLY",
            "climateos_locality_is_catchment": "FALSE",
            "climateos_council_boundary_present": "FALSE",
            "climateos_scientific_conclusion": SCIENTIFIC_CONCLUSION,
            "climateos_stacked_pr_base": STACKED_PR_BASE,
        }.items():
            api["QgsExpressionContextUtils"].setProjectVariable(project, name, value)

        west, east = extent["west"], extent["east"]
        south, north = extent["south"], extent["north"]
        width, height = east - west, north - south
        bookmark_extents = (
            (HYDROLOGY_BOOKMARKS[0], (west + 0.18 * width, south + 0.15 * height, east - 0.18 * width, north - 0.15 * height)),
            (HYDROLOGY_BOOKMARKS[1], (west, south, east, north)),
            (HYDROLOGY_BOOKMARKS[2], (west + 0.05 * width, south + 0.28 * height, east - 0.05 * width, north - 0.22 * height)),
        )
        manager = project.bookmarkManager()
        project_crs = api["QgsCoordinateReferenceSystem"](HYDROLOGY_PROJECT_CRS)
        for index, (name, values) in enumerate(bookmark_extents, start=1):
            bookmark = api["QgsBookmark"]()
            bookmark.setId(f"climateos-hydrology-bookmark-{index}")
            bookmark.setName(name)
            bookmark.setGroup("COOMA HYDROLOGY CONTEXT — OBSERVATION ONLY")
            rectangle = api["QgsRectangle"](*values)
            bookmark.setExtent(api["QgsReferencedRectangle"](rectangle, project_crs))
            if not manager.addBookmark(bookmark):
                raise HydrologyPackError(f"failed to add hydrology bookmark: {name}")
        if not project.write(str(layout["project"])):
            raise HydrologyPackError("QGIS refused to write the v0.3 hydrology project")
    finally:
        if project is not None:
            project.clear()
            del project
        application.exitQgis()
        del application

    manifest = {
        "schema_id": "climateos.qgis-hydrology-project.v1",
        "created_at": _utc_now(),
        "project_filename": HYDROLOGY_PROJECT_FILENAME,
        "project_sha256": _sha256(layout["project"]),
        "project_crs": HYDROLOGY_PROJECT_CRS,
        "terrain_base_project": TERRAIN_PROJECT_FILENAME,
        "terrain_layers": list(TERRAIN_LAYER_NAMES),
        "hydrology_layers": list(HYDROLOGY_LAYER_NAMES),
        "bookmarks": list(HYDROLOGY_BOOKMARKS),
        "network_provider": "NONE",
        "scientific_conclusion": "NONE",
    }
    _write_json_new(layout["project_manifest"], manifest)
    return {"project": manifest, "project_path": str(layout["project"]), "workspace_sizes": _workspace_sizes(layout)}


def verify(repo_root: Path, osgeo_root: Path) -> dict[str, object]:
    layout = _layout(repo_root)
    required = [
        layout["project"],
        layout["retrieval_manifest"],
        layout["derivation_manifest"],
        layout["project_manifest"],
        *layout["raw"].values(),
        *layout["derived"].values(),
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise HydrologyPackError(f"hydrology verification files missing: {missing}")
    retrieval = json.loads(layout["retrieval_manifest"].read_text(encoding="utf-8"))
    for receipt in retrieval["receipts"]:
        path = layout["root"] / receipt["local_path"]
        if receipt["sha256"] != _sha256(path):
            raise HydrologyPackError(f'hydrology source checksum mismatch: {receipt["source_id"]}')
    derivation = json.loads(layout["derivation_manifest"].read_text(encoding="utf-8"))
    for key, file_info in derivation["files"].items():
        if file_info["sha256"] != _sha256(layout["derived"][key]):
            raise HydrologyPackError(f"hydrology derived checksum mismatch: {key}")
    if derivation["scientific_conclusion"] != "NONE":
        raise HydrologyPackError("hydrology derivation contains a scientific conclusion")

    profile = layout["root"] / ".qgis-profile-hydrology-verify"
    profile.mkdir(exist_ok=True)
    os.chdir(layout["root"])
    api = _hydrology_qgis_api(osgeo_root, profile)
    application = _new_qgis_application(api, osgeo_root)
    project = None
    try:
        project = api["QgsProject"]()
        if not project.read(str(layout["project"])):
            raise HydrologyPackError("QGIS could not reopen the v0.3 hydrology project")
        layers = {layer.name(): layer for layer in project.mapLayers().values()}
        for name in (*TERRAIN_LAYER_NAMES, *HYDROLOGY_LAYER_NAMES):
            if name not in layers:
                raise HydrologyPackError(f"hydrology project layer missing: {name}")
        invalid = [name for name, layer in layers.items() if not layer.isValid()]
        if invalid:
            raise HydrologyPackError(f"broken hydrology project layers: {invalid}")
        for name, layer in layers.items():
            if layer.source().split("|", 1)[0].lower().startswith(("http://", "https://")):
                raise HydrologyPackError(f"network-backed layer is prohibited: {name}")
        bookmark_names = [item.name() for item in project.bookmarkManager().bookmarks()]
        for name in (*HYDROLOGY_BOOKMARKS, "Cooma Locality", "Cooma + 10 km Terrain"):
            if name not in bookmark_names:
                raise HydrologyPackError(f"hydrology project bookmark missing: {name}")
        extents = [
            tuple(round(value, 3) for value in (item.extent().xMinimum(), item.extent().yMinimum(), item.extent().xMaximum(), item.extent().yMaximum()))
            for item in project.bookmarkManager().bookmarks()
            if item.name() in HYDROLOGY_BOOKMARKS
        ]
        if len(set(extents)) != 3:
            raise HydrologyPackError("hydrology bookmark extents are not visibly distinct")
        if project.crs().authid() != HYDROLOGY_PROJECT_CRS:
            raise HydrologyPackError("hydrology project CRS is not EPSG:7855")
        if project.filePathStorage() != api["Qgis"].FilePathType.Relative:
            raise HydrologyPackError("hydrology project paths are not relative")
    finally:
        if project is not None:
            project.clear()
            del project
        application.exitQgis()
        del application

    with zipfile.ZipFile(layout["project"]) as archive:
        qgs_names = [name for name in archive.namelist() if name.endswith(".qgs")]
        if len(qgs_names) != 1:
            raise HydrologyPackError("hydrology QGZ must contain exactly one QGS document")
        xml = archive.read(qgs_names[0]).decode("utf-8").lower()
    xml = xml.replace("http://mrcc.com/qgis.dtd", "")
    for prohibited in ("type=xyz", "<provider>wms</provider>", "<provider>wfs</provider>"):
        if prohibited in xml:
            raise HydrologyPackError(f"network provider found in hydrology project: {prohibited}")
    manifest = json.loads(layout["project_manifest"].read_text(encoding="utf-8"))
    if manifest["project_sha256"] != _sha256(layout["project"]):
        raise HydrologyPackError("hydrology project checksum mismatch")
    return {
        "project_path": str(layout["project"]),
        "project_sha256": _sha256(layout["project"]),
        "broken_layer_count": 0,
        "network_provider_count": 0,
        "terrain_layers_present": True,
        "hydrology_bookmarks_present": list(HYDROLOGY_BOOKMARKS),
        "scientific_conclusion": "NONE",
        "workspace_sizes": _workspace_sizes(layout),
    }


def plan(repo_root: Path) -> dict[str, object]:
    load_source_registry()
    layout = _layout(repo_root)
    return {
        "product": HYDROLOGY_PRODUCT,
        "version": HYDROLOGY_VERSION,
        "publisher": HYDROLOGY_PUBLISHER,
        "licence": HYDROLOGY_LICENCE,
        "source_crs": HYDROLOGY_SOURCE_CRS,
        "feature_scale": HYDROLOGY_FEATURE_SCALE,
        "temporal_currency": HYDROLOGY_METADATA_DATE,
        "layers": [{"id": item["layer_id"], "name": item["layer"]} for item in HYDROLOGY_SOURCES],
        "extent": AUTHORIZED_LONGITUDE_LATITUDE_EXTENT,
        "size_limits": hydrology_size_limits(),
        "project_destination": str(layout["project"]),
        "terrain_base_head": TERRAIN_BASE_HEAD,
        "stacked_pr_base": STACKED_PR_BASE,
        "scientific_conclusion": "NONE",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("plan", "retrieve", "derive", "build-project", "verify"))
    parser.add_argument("--osgeo-root", default="D:\\")
    args = parser.parse_args(argv)
    try:
        repo_root = _repo_root()
        if args.action == "plan":
            result = plan(repo_root)
        elif args.action == "retrieve":
            result = retrieve(repo_root)
        elif args.action == "derive":
            result = derive(repo_root)
        elif args.action == "build-project":
            result = build_project(repo_root, Path(args.osgeo_root))
        else:
            result = verify(repo_root, Path(args.osgeo_root))
    except (
        OSError,
        ValueError,
        KeyError,
        json.JSONDecodeError,
        HydrologyPackError,
        SpatialWorkspaceError,
        SpatialProjectError,
    ) as exc:
        print(json.dumps({"status": "ERROR", "error": str(exc)}, ensure_ascii=False))
        return 1
    print(json.dumps({"status": "PASS", **result}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
