"""Build one integrated Cooma QGIS project from the accepted spatial packs.

The project inherits the accepted v0.3 terrain/hydrology project, retrieves only
bounded NSW official road vectors, and adds the exact NSWWebImagery tile service
as an optional online basemap. Runtime spatial data remains git-ignored.
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

from .hydrology_contract import HYDROLOGY_LAYER_NAMES, HYDROLOGY_PROJECT_FILENAME
from .hydrology_pack import _hydrology_qgis_api
from .integrated_contract import (
    AUTHORIZED_LONGITUDE_LATITUDE_EXTENT,
    DEFAULT_VISIBLE_LAYERS,
    DERIVED_ROAD_LIMIT,
    HYDROLOGY_BASE_PROJECT_FILENAME,
    IMAGERY_CRS,
    IMAGERY_LAYER_NAME,
    IMAGERY_MAX_ZOOM,
    IMAGERY_MIN_ZOOM,
    IMAGERY_PRODUCT,
    IMAGERY_PUBLISHER,
    IMAGERY_SERVICE,
    IMAGERY_TILE_URL,
    INTEGRATED_BASE_HEAD,
    INTEGRATED_BOOKMARKS,
    INTEGRATED_PROJECT_CRS,
    INTEGRATED_PROJECT_FILENAME,
    INTEGRATED_WORKSPACE_DIRECTORIES,
    NETWORK_RETRIEVAL_LIMIT,
    RAW_ROAD_LIMIT,
    ROAD_DERIVED_FILENAME,
    ROAD_LAYER,
    ROAD_LAYER_NAME,
    ROAD_LICENCE,
    ROAD_PRODUCT,
    ROAD_PUBLISHER,
    ROAD_QUERY_URL,
    ROAD_RAW_FILENAME,
    ROAD_SOURCE_CRS,
    WORKSPACE_LIMIT,
    integrated_size_limits,
)
from .project_builder import SpatialProjectError, _new_qgis_application
from .terrain_contract import STUDY_EXTENT_FILENAME, STUDY_EXTENT_MANIFEST, TERRAIN_LAYER_NAMES
from .workspace import SpatialWorkspaceError, ensure_local_workspace


class IntegratedExperienceError(RuntimeError):
    """Raised when the unified-project source, path, size or QGIS gate fails."""


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
        raise IntegratedExperienceError(f"new-file-only overwrite refused: {path}")


def _assert_confined(path: Path, root: Path) -> None:
    resolved, controlled = path.resolve(), root.resolve()
    if resolved != controlled and controlled not in resolved.parents:
        raise IntegratedExperienceError(f"path escapes controlled QGIS workspace: {path}")


def _write_json_new(path: Path, payload: object) -> None:
    _ensure_new_file(path)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True, ensure_ascii=False)
        handle.write("\n")


def _directory_size(path: Path) -> int:
    return sum(item.stat().st_size for item in path.rglob("*") if item.is_file())


def _layout(repo_root: Path) -> dict[str, Path]:
    root = ensure_local_workspace(repo_root)["root"]
    for relative in INTEGRATED_WORKSPACE_DIRECTORIES:
        destination = root / relative
        _assert_confined(destination, root)
        destination.mkdir(parents=True, exist_ok=True)
    return {
        "root": root,
        "base_project": root / "project" / HYDROLOGY_BASE_PROJECT_FILENAME,
        "study_extent": root / "derived_data" / "terrain" / STUDY_EXTENT_FILENAME,
        "extent_manifest": root / "manifests" / "derivation" / STUDY_EXTENT_MANIFEST,
        "road_raw": root / "source_data" / "roads" / ROAD_RAW_FILENAME,
        "road_derived": root / "derived_data" / "roads" / ROAD_DERIVED_FILENAME,
        "retrieval_manifest": root / "manifests" / "retrieval" / "cooma_integrated_roads_retrieval.json",
        "derivation_manifest": root / "manifests" / "derivation" / "cooma_integrated_roads_derivation.json",
        "project": root / "project" / INTEGRATED_PROJECT_FILENAME,
        "project_manifest": root / "manifests" / "derivation" / "cooma_integrated_project.json",
    }


def _sizes(layout: dict[str, Path]) -> dict[str, int]:
    observed = {
        "raw_roads": _directory_size(layout["root"] / "source_data" / "roads"),
        "derived_roads": _directory_size(layout["root"] / "derived_data" / "roads"),
        "workspace": _directory_size(layout["root"]),
    }
    limits = integrated_size_limits()
    for key, size in observed.items():
        if size > limits[key]:
            raise IntegratedExperienceError(f"{key} size ceiling exceeded: {size} > {limits[key]}")
    return observed


def _road_query_parameters() -> dict[str, str]:
    extent = AUTHORIZED_LONGITUDE_LATITUDE_EXTENT
    return {
        "f": "geojson",
        "where": "1=1",
        "outFields": "*",
        "returnGeometry": "true",
        "geometry": f'{extent["west"]},{extent["south"]},{extent["east"]},{extent["north"]}',
        "geometryType": "esriGeometryEnvelope",
        "inSR": "4326",
        "outSR": "4326",
        "spatialRel": "esriSpatialRelIntersects",
        "orderByFields": "objectid",
    }


def _fetch_json(parameters: dict[str, str], *, ceiling: int) -> tuple[dict[str, object], int]:
    url = ROAD_QUERY_URL + "?" + urlencode(parameters)
    request = Request(url, headers={"User-Agent": "ClimateOS-QGIS-Integrated-Cooma/1.0"})
    with urlopen(request, timeout=120) as response:  # nosec B310 - exact closed HTTPS source
        content = response.read(ceiling + 1)
    if len(content) > ceiling:
        raise IntegratedExperienceError("bounded road response exceeded byte ceiling")
    payload = json.loads(content.decode("utf-8"))
    return payload, len(content)


def retrieve(repo_root: Path) -> dict[str, object]:
    layout = _layout(repo_root)
    for path in (layout["road_raw"], layout["retrieval_manifest"]):
        _assert_confined(path, layout["root"])
        _ensure_new_file(path)

    count_parameters = _road_query_parameters()
    count_parameters.update({"f": "json", "returnCountOnly": "true", "returnGeometry": "false"})
    count_payload, count_bytes = _fetch_json(count_parameters, ceiling=1024 * 1024)
    expected_count = int(count_payload.get("count", -1))
    if expected_count < 1:
        raise IntegratedExperienceError("bounded NSW road query returned no features")

    features: list[object] = []
    network_bytes = count_bytes
    page_size = 2000
    for offset in range(0, expected_count, page_size):
        parameters = _road_query_parameters()
        parameters.update({"resultOffset": str(offset), "resultRecordCount": str(page_size)})
        payload, page_bytes = _fetch_json(parameters, ceiling=NETWORK_RETRIEVAL_LIMIT - network_bytes)
        if payload.get("type") != "FeatureCollection" or not isinstance(payload.get("features"), list):
            raise IntegratedExperienceError("road response is not a GeoJSON FeatureCollection")
        features.extend(payload["features"])
        network_bytes += page_bytes
    if len(features) != expected_count:
        raise IntegratedExperienceError(
            f"road pagination mismatch: expected {expected_count}, received {len(features)}"
        )

    collection = {"type": "FeatureCollection", "features": features}
    encoded = (json.dumps(collection, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
    if len(encoded) > RAW_ROAD_LIMIT:
        raise IntegratedExperienceError("retained bounded road GeoJSON exceeds raw ceiling")
    with layout["road_raw"].open("xb") as handle:
        handle.write(encoded)
    manifest = {
        "schema_id": "climateos.qgis-integrated-road-retrieval.v1",
        "created_at": _utc_now(),
        "publisher": ROAD_PUBLISHER,
        "product": ROAD_PRODUCT,
        "layer": ROAD_LAYER,
        "query_url": ROAD_QUERY_URL,
        "licence": ROAD_LICENCE,
        "requested_extent": AUTHORIZED_LONGITUDE_LATITUDE_EXTENT,
        "source_crs": ROAD_SOURCE_CRS,
        "feature_count": len(features),
        "network_bytes": network_bytes,
        "file_size": len(encoded),
        "sha256": _sha256(layout["road_raw"]),
        "local_path": layout["road_raw"].relative_to(layout["root"]).as_posix(),
        "scientific_conclusion": "NONE",
    }
    _write_json_new(layout["retrieval_manifest"], manifest)
    return {"retrieval": manifest, "workspace_sizes": _sizes(layout)}


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


def derive(repo_root: Path) -> dict[str, object]:
    layout = _layout(repo_root)
    required = (layout["road_raw"], layout["study_extent"], layout["extent_manifest"])
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise IntegratedExperienceError(f"integrated road derivation inputs missing: {missing}")
    _ensure_new_file(layout["road_derived"])
    _ensure_new_file(layout["derivation_manifest"])

    ogr, osr = _osgeo()
    extent_source = ogr.Open(str(layout["study_extent"]), 0)
    extent_feature = extent_source.GetLayer(0).GetNextFeature() if extent_source else None
    clip = extent_feature.GetGeometryRef().Clone() if extent_feature else None
    extent_source = None
    if clip is None or clip.IsEmpty():
        raise IntegratedExperienceError("authorized Cooma +10 km clipping geometry is missing")
    target_crs = _spatial_reference(osr, 7855)
    clip.AssignSpatialReference(target_crs)

    source = ogr.Open(str(layout["road_raw"]), 0)
    if source is None:
        raise IntegratedExperienceError("GDAL could not open bounded road GeoJSON")
    source_layer = source.GetLayer(0)
    source_definition = source_layer.GetLayerDefn()
    source_crs = _spatial_reference(osr, 4326)
    transform = osr.CoordinateTransformation(source_crs, target_crs)

    output = ogr.GetDriverByName("GPKG").CreateDataSource(str(layout["road_derived"]))
    output_layer = output.CreateLayer("cooma_roads", target_crs, ogr.wkbUnknown)
    for index in range(source_definition.GetFieldCount()):
        output_layer.CreateField(source_definition.GetFieldDefn(index))
    output_definition = output_layer.GetLayerDefn()
    source_count = output_count = 0
    for source_feature in source_layer:
        source_count += 1
        geometry = source_feature.GetGeometryRef()
        if geometry is None or geometry.IsEmpty():
            continue
        projected = geometry.Clone()
        projected.AssignSpatialReference(source_crs)
        projected.Transform(transform)
        clipped = projected.Intersection(clip)
        if clipped is None or clipped.IsEmpty():
            continue
        feature = ogr.Feature(output_definition)
        for index in range(source_definition.GetFieldCount()):
            feature.SetField(index, source_feature.GetField(index))
        feature.SetGeometry(clipped)
        output_layer.CreateFeature(feature)
        feature = None
        output_count += 1
    output_layer.SyncToDisk()
    output_layer = None
    output = None
    source = None
    if output_count < 1:
        raise IntegratedExperienceError("road clipping produced no features")
    if layout["road_derived"].stat().st_size > DERIVED_ROAD_LIMIT:
        raise IntegratedExperienceError("derived road layer exceeds byte ceiling")

    manifest = {
        "schema_id": "climateos.qgis-integrated-road-derivation.v1",
        "created_at": _utc_now(),
        "source_feature_count": source_count,
        "derived_feature_count": output_count,
        "project_crs": INTEGRATED_PROJECT_CRS,
        "clipping": "existing official COOMA locality plus 10 km EPSG:7855 polygon",
        "local_path": layout["road_derived"].relative_to(layout["root"]).as_posix(),
        "file_size": layout["road_derived"].stat().st_size,
        "sha256": _sha256(layout["road_derived"]),
        "scientific_conclusion": "NONE",
    }
    _write_json_new(layout["derivation_manifest"], manifest)
    return {"derivation": manifest, "workspace_sizes": _sizes(layout)}


def _integrated_qgis_api(osgeo_root: Path, profile: Path) -> dict[str, object]:
    api = _hydrology_qgis_api(osgeo_root, profile)
    from qgis.core import QgsLineSymbol, QgsRasterLayer  # type: ignore[import-not-found]

    api.update({"QgsLineSymbol": QgsLineSymbol, "QgsRasterLayer": QgsRasterLayer})
    return api


def build_project(repo_root: Path, osgeo_root: Path) -> dict[str, object]:
    layout = _layout(repo_root)
    required = (layout["base_project"], layout["road_derived"], layout["extent_manifest"])
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise IntegratedExperienceError(f"integrated project inputs missing: {missing}")
    for path in (layout["project"], layout["project_manifest"]):
        _ensure_new_file(path)

    extent = json.loads(layout["extent_manifest"].read_text(encoding="utf-8"))["projected_extent"]
    profile = layout["root"] / ".qgis-profile-integrated"
    profile.mkdir(exist_ok=True)
    os.chdir(layout["root"])
    api = _integrated_qgis_api(osgeo_root, profile)
    application = _new_qgis_application(api, osgeo_root)
    project = None
    try:
        project = api["QgsProject"]()
        if not project.read(str(layout["base_project"])):
            raise IntegratedExperienceError("QGIS could not open accepted v0.3 hydrology project")
        project.setFilePathStorage(api["Qgis"].FilePathType.Relative)
        metadata = project.metadata()
        metadata.setTitle("Cooma Spatial Foundation v0.4 Integrated")
        metadata.setAuthor("ClimateOS — Founder-authorized integrated spatial experience")
        metadata.setAbstract(
            "ONE PROJECT / LAYERED VIEW / TERRAIN + HYDROLOGY + OFFICIAL ROADS + OPTIONAL "
            "ONLINE NSW IMAGERY. Spatial orientation only; scientific and engineering conclusion: NONE."
        )
        project.setMetadata(metadata)

        groups = {
            child.name(): child
            for child in project.layerTreeRoot().children()
            if hasattr(child, "name")
        }
        settlement = groups.get("04_SETTLEMENT_AND_ROADS")
        if settlement is None:
            raise IntegratedExperienceError("accepted settlement-and-roads group is missing")

        road = api["QgsVectorLayer"](
            str(layout["road_derived"]), ROAD_LAYER_NAME, "ogr"
        )
        if not road.isValid():
            raise IntegratedExperienceError("QGIS could not load bounded NSW official roads")
        road.renderer().setSymbol(
            api["QgsLineSymbol"].createSimple(
                {"color": "72,62,50,235", "width": "0.75", "capstyle": "round", "joinstyle": "round"}
            )
        )
        project.addMapLayer(road, False)
        settlement.addLayer(road)

        imagery_uri = (
            f"type=xyz&url={IMAGERY_TILE_URL}&zmin={IMAGERY_MIN_ZOOM}&zmax={IMAGERY_MAX_ZOOM}"
            f"&crs={IMAGERY_CRS}"
        )
        imagery = api["QgsRasterLayer"](imagery_uri, IMAGERY_LAYER_NAME, "wms")
        if not imagery.isValid():
            raise IntegratedExperienceError("QGIS could not initialize exact NSWWebImagery service")
        imagery.setCustomProperty("climateos_source", f"{IMAGERY_PUBLISHER} — {IMAGERY_PRODUCT}")
        imagery.setCustomProperty("climateos_online_only", "TRUE")
        imagery.setCustomProperty("climateos_service", IMAGERY_SERVICE)
        project.addMapLayer(imagery, False)
        settlement.addLayer(imagery)

        for layer in project.mapLayers().values():
            node = project.layerTreeRoot().findLayer(layer.id())
            if node is not None:
                node.setItemVisibilityChecked(layer.name() in DEFAULT_VISIBLE_LAYERS)
        settlement.setItemVisibilityChecked(True)
        settlement.findLayer(road.id()).setItemVisibilityChecked(True)
        settlement.findLayer(imagery.id()).setItemVisibilityChecked(True)

        for name, value in {
            "climateos_integrated_base_head": INTEGRATED_BASE_HEAD,
            "climateos_integrated_project": "TRUE",
            "climateos_roads_source": f"{ROAD_PUBLISHER} — {ROAD_PRODUCT} — {ROAD_LAYER}",
            "climateos_imagery_source": f"{IMAGERY_PUBLISHER} — {IMAGERY_PRODUCT}",
            "climateos_imagery_online_only": "TRUE",
            "climateos_offline_core_available": "TERRAIN_HYDROLOGY_ROADS",
            "climateos_scientific_conclusion": "NONE",
        }.items():
            api["QgsExpressionContextUtils"].setProjectVariable(project, name, value)

        west, east = extent["west"], extent["east"]
        south, north = extent["south"], extent["north"]
        width, height = east - west, north - south
        bookmark_extents = (
            (INTEGRATED_BOOKMARKS[0], (west, south, east, north)),
            (INTEGRATED_BOOKMARKS[1], (west + 0.20 * width, south + 0.20 * height, east - 0.20 * width, north - 0.20 * height)),
            (INTEGRATED_BOOKMARKS[2], (west + 0.05 * width, south + 0.12 * height, east - 0.05 * width, north - 0.12 * height)),
        )
        manager = project.bookmarkManager()
        project_crs = api["QgsCoordinateReferenceSystem"](INTEGRATED_PROJECT_CRS)
        for index, (name, values) in enumerate(bookmark_extents, start=1):
            bookmark = api["QgsBookmark"]()
            bookmark.setId(f"climateos-integrated-bookmark-{index}")
            bookmark.setName(name)
            bookmark.setGroup("COOMA INTEGRATED EXPERIENCE")
            bookmark.setExtent(
                api["QgsReferencedRectangle"](api["QgsRectangle"](*values), project_crs)
            )
            if not manager.addBookmark(bookmark):
                raise IntegratedExperienceError(f"failed to add integrated bookmark: {name}")

        if not project.write(str(layout["project"])):
            raise IntegratedExperienceError("QGIS refused to write the integrated project")
    finally:
        if project is not None:
            project.clear()
            del project
        application.exitQgis()
        del application

    manifest = {
        "schema_id": "climateos.qgis-integrated-project.v1",
        "created_at": _utc_now(),
        "project_filename": INTEGRATED_PROJECT_FILENAME,
        "project_sha256": _sha256(layout["project"]),
        "project_crs": INTEGRATED_PROJECT_CRS,
        "base_project": HYDROLOGY_PROJECT_FILENAME,
        "terrain_layers": list(TERRAIN_LAYER_NAMES),
        "hydrology_layers": list(HYDROLOGY_LAYER_NAMES),
        "road_layer": ROAD_LAYER_NAME,
        "imagery_layer": IMAGERY_LAYER_NAME,
        "imagery_service": IMAGERY_SERVICE,
        "bookmarks": list(INTEGRATED_BOOKMARKS),
        "default_visible_layers": list(DEFAULT_VISIBLE_LAYERS),
        "network_layers": [IMAGERY_LAYER_NAME],
        "scientific_conclusion": "NONE",
    }
    _write_json_new(layout["project_manifest"], manifest)
    return {"project": manifest, "project_path": str(layout["project"]), "workspace_sizes": _sizes(layout)}


def verify(repo_root: Path, osgeo_root: Path) -> dict[str, object]:
    layout = _layout(repo_root)
    required = (
        layout["road_raw"], layout["road_derived"], layout["retrieval_manifest"],
        layout["derivation_manifest"], layout["project"], layout["project_manifest"],
    )
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise IntegratedExperienceError(f"integrated verification files missing: {missing}")
    retrieval = json.loads(layout["retrieval_manifest"].read_text(encoding="utf-8"))
    derivation = json.loads(layout["derivation_manifest"].read_text(encoding="utf-8"))
    manifest = json.loads(layout["project_manifest"].read_text(encoding="utf-8"))
    if retrieval["sha256"] != _sha256(layout["road_raw"]):
        raise IntegratedExperienceError("road raw checksum mismatch")
    if derivation["sha256"] != _sha256(layout["road_derived"]):
        raise IntegratedExperienceError("road derived checksum mismatch")
    if manifest["project_sha256"] != _sha256(layout["project"]):
        raise IntegratedExperienceError("integrated project checksum mismatch")

    profile = layout["root"] / ".qgis-profile-integrated-verify"
    profile.mkdir(exist_ok=True)
    os.chdir(layout["root"])
    api = _integrated_qgis_api(osgeo_root, profile)
    application = _new_qgis_application(api, osgeo_root)
    project = None
    try:
        project = api["QgsProject"]()
        if not project.read(str(layout["project"])):
            raise IntegratedExperienceError("QGIS could not reopen integrated project")
        layers = {layer.name(): layer for layer in project.mapLayers().values()}
        for name in (*TERRAIN_LAYER_NAMES, *HYDROLOGY_LAYER_NAMES, ROAD_LAYER_NAME, IMAGERY_LAYER_NAME):
            if name not in layers:
                raise IntegratedExperienceError(f"integrated project layer missing: {name}")
        invalid = [name for name, layer in layers.items() if not layer.isValid()]
        if invalid:
            raise IntegratedExperienceError(f"broken integrated layers: {invalid}")
        network_layers = [name for name, layer in layers.items() if layer.providerType() in {"wms", "wfs"}]
        if network_layers != [IMAGERY_LAYER_NAME]:
            raise IntegratedExperienceError(f"unexpected network layer set: {network_layers}")
        if IMAGERY_SERVICE not in layers[IMAGERY_LAYER_NAME].source():
            raise IntegratedExperienceError("imagery service is not the exact closed NSW source")
        bookmark_names = [item.name() for item in project.bookmarkManager().bookmarks()]
        for name in INTEGRATED_BOOKMARKS:
            if name not in bookmark_names:
                raise IntegratedExperienceError(f"integrated bookmark missing: {name}")
        if project.crs().authid() != INTEGRATED_PROJECT_CRS:
            raise IntegratedExperienceError("integrated project CRS is not EPSG:7855")
        if project.filePathStorage() != api["Qgis"].FilePathType.Relative:
            raise IntegratedExperienceError("integrated project local paths are not relative")
    finally:
        if project is not None:
            project.clear()
            del project
        application.exitQgis()
        del application

    with zipfile.ZipFile(layout["project"]) as archive:
        qgs_names = [name for name in archive.namelist() if name.endswith(".qgs")]
        if len(qgs_names) != 1:
            raise IntegratedExperienceError("integrated QGZ must contain one QGS document")
        xml = archive.read(qgs_names[0]).decode("utf-8")
    if xml.count("type=xyz") != 1 or IMAGERY_SERVICE not in xml:
        raise IntegratedExperienceError("integrated project must contain exactly one closed imagery XYZ source")
    return {
        "project_path": str(layout["project"]),
        "project_sha256": _sha256(layout["project"]),
        "broken_layer_count": 0,
        "network_layer_count": 1,
        "offline_core": ["terrain", "hydrology", "roads"],
        "online_optional": ["NSWWebImagery"],
        "scientific_conclusion": "NONE",
        "workspace_sizes": _sizes(layout),
    }


def plan(repo_root: Path) -> dict[str, object]:
    layout = _layout(repo_root)
    return {
        "base_head": INTEGRATED_BASE_HEAD,
        "base_project": str(layout["base_project"]),
        "project_destination": str(layout["project"]),
        "road_source": ROAD_QUERY_URL,
        "imagery_source": IMAGERY_SERVICE,
        "extent": AUTHORIZED_LONGITUDE_LATITUDE_EXTENT,
        "size_limits": integrated_size_limits(),
        "one_project": True,
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
        OSError, ValueError, KeyError, json.JSONDecodeError,
        IntegratedExperienceError, SpatialWorkspaceError, SpatialProjectError,
    ) as exc:
        print(json.dumps({"status": "ERROR", "error": str(exc)}, ensure_ascii=False))
        return 1
    print(json.dumps({"status": "PASS", **result}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
