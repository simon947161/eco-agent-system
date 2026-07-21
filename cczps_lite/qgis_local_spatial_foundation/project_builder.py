"""Build and verify the local QGIS skeleton and synthetic navigation anchor.

Run with QGIS-bundled Python 3.12. The module has no network client, accepts no
arbitrary output directory, and never retrieves public or private spatial data.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import zipfile

from .contract import (
    BOOKMARKS,
    DEFAULT_VIEW_EXTENT,
    PROJECT_LAYER_GROUPS,
    PROVISIONAL_SCOPE_STATUS,
    REVISION_PROJECT_FILENAME,
    SCIENTIFIC_CONCLUSION,
    START_HERE_MESSAGES,
    SYNTHETIC_LAYER_NAMES,
    TERRAIN_INFO_LAYER,
    WATER_INFO_LAYER,
)
from .synthetic_anchor import (
    ANCHOR_FILENAMES,
    SyntheticAnchorError,
    ensure_synthetic_anchor_files,
)
from .workspace import SpatialWorkspaceError, ensure_local_workspace


class SpatialProjectError(RuntimeError):
    """Raised when project generation or verification violates the contract."""


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _prepare_qgis_runtime(osgeo_root: Path, local_profile: Path) -> None:
    osgeo_root = osgeo_root.resolve()
    required = (
        osgeo_root / "bin",
        osgeo_root / "apps" / "qgis-ltr" / "bin",
        osgeo_root / "apps" / "Qt5" / "bin",
        osgeo_root / "apps" / "Python312",
    )
    missing = [str(path) for path in required if not path.is_dir()]
    if missing:
        raise SpatialProjectError(f"QGIS runtime directories missing: {missing}")
    if hasattr(os, "add_dll_directory"):
        for path in required:
            os.add_dll_directory(str(path))
    os.environ["QGIS_PREFIX_PATH"] = str(osgeo_root / "apps" / "qgis-ltr")
    os.environ["QT_PLUGIN_PATH"] = ";".join(
        (
            str(osgeo_root / "apps" / "qgis-ltr" / "qtplugins"),
            str(osgeo_root / "apps" / "Qt5" / "plugins"),
        )
    )
    os.environ["GDAL_DATA"] = str(osgeo_root / "apps" / "gdal" / "share" / "gdal")
    os.environ["PROJ_DATA"] = str(osgeo_root / "share" / "proj")
    os.environ["QGIS_CUSTOM_CONFIG_PATH"] = str(local_profile)


def _qgis_api(osgeo_root: Path, local_profile: Path) -> dict[str, object]:
    _prepare_qgis_runtime(osgeo_root, local_profile)
    from qgis.PyQt.QtGui import QColor  # type: ignore[import-not-found]
    from qgis.core import (  # type: ignore[import-not-found]
        Qgis,
        QgsApplication,
        QgsBookmark,
        QgsCoordinateReferenceSystem,
        QgsExpressionContextUtils,
        QgsFillSymbol,
        QgsMarkerSymbol,
        QgsPalLayerSettings,
        QgsProject,
        QgsProjectMetadata,
        QgsRectangle,
        QgsReferencedRectangle,
        QgsTextFormat,
        QgsVectorLayer,
        QgsVectorLayerSimpleLabeling,
    )

    return {name: value for name, value in locals().items() if name.startswith("Q")}


def _new_qgis_application(api: dict[str, object], osgeo_root: Path):
    application_class = api["QgsApplication"]
    application_class.setPrefixPath(str(osgeo_root / "apps" / "qgis-ltr"), True)
    application = application_class([], False)
    application.initQgis()
    return application


def _project_target(workspace: dict[str, object], revision: bool) -> tuple[Path, Path]:
    root = workspace["root"]
    if revision:
        return (
            workspace["revision_project_path"],
            root / "manifests" / "project_ux_revision_manifest.json",
        )
    return workspace["project_path"], root / "manifests" / "project_build_manifest.json"


def _add_local_layer(api, project, group, path: Path, name: str):
    layer = api["QgsVectorLayer"](str(path), name, "ogr")
    if not layer.isValid():
        raise SpatialProjectError(f"QGIS could not load local layer: {path}")
    project.addMapLayer(layer, False)
    group.addLayer(layer)
    return layer


def _style_anchor_layers(api, centre_layer, extent_layer) -> None:
    centre_layer.renderer().setSymbol(
        api["QgsMarkerSymbol"].createSimple(
            {
                "name": "circle",
                "color": "21,111,78,255",
                "outline_color": "255,255,255,255",
                "outline_width": "0.8",
                "size": "5.5",
            }
        )
    )
    label_settings = api["QgsPalLayerSettings"]()
    label_settings.enabled = True
    label_settings.fieldName = "'Cooma Provisional Centre' || '\\nNOT EVIDENCE'"
    label_settings.isExpression = True
    text_format = api["QgsTextFormat"]()
    text_format.setSize(10)
    text_format.setColor(api["QColor"]("#145A43"))
    label_settings.setFormat(text_format)
    centre_layer.setLabeling(api["QgsVectorLayerSimpleLabeling"](label_settings))
    centre_layer.setLabelsEnabled(True)

    extent_layer.renderer().setSymbol(
        api["QgsFillSymbol"].createSimple(
            {
                "color": "76,175,120,45",
                "outline_color": "21,111,78,255",
                "outline_width": "0.9",
            }
        )
    )


def _populate_project(api, project, groups, local_anchor_root: Path) -> tuple[object, ...]:
    start = groups["00_START_HERE"]
    learning_layer = _add_local_layer(
        api,
        project,
        start,
        local_anchor_root / ANCHOR_FILENAMES["start_here"],
        START_HERE_MESSAGES[0],
    )
    centre_layer = _add_local_layer(
        api,
        project,
        start,
        local_anchor_root / ANCHOR_FILENAMES["centre"],
        START_HERE_MESSAGES[1],
    )
    extent_layer = _add_local_layer(
        api,
        project,
        start,
        local_anchor_root / ANCHOR_FILENAMES["extent"],
        START_HERE_MESSAGES[2],
    )
    terrain_layer = _add_local_layer(
        api,
        project,
        groups["02_TERRAIN"],
        local_anchor_root / ANCHOR_FILENAMES["terrain_info"],
        TERRAIN_INFO_LAYER,
    )
    water_layer = _add_local_layer(
        api,
        project,
        groups["03_WATER"],
        local_anchor_root / ANCHOR_FILENAMES["water_info"],
        WATER_INFO_LAYER,
    )
    _style_anchor_layers(api, centre_layer, extent_layer)
    return learning_layer, centre_layer, extent_layer, terrain_layer, water_layer


def _build_project(repo_root: Path, osgeo_root: Path, *, revision: bool) -> dict[str, object]:
    workspace = ensure_local_workspace(repo_root)
    root = workspace["root"]
    project_path, manifest_path = _project_target(workspace, revision)
    if project_path.exists():
        raise SpatialProjectError(f"project already exists; overwrite refused: {project_path}")
    if manifest_path.exists():
        raise SpatialProjectError(f"project manifest already exists; overwrite refused: {manifest_path}")

    anchor_paths = ensure_synthetic_anchor_files(root / "local_anchor")
    profile = root / ".qgis-profile"
    profile.mkdir(exist_ok=True)
    os.chdir(root)
    api = _qgis_api(osgeo_root, profile)
    application = _new_qgis_application(api, osgeo_root)
    project = None
    try:
        project = api["QgsProject"]()
        project.setFilePathStorage(api["Qgis"].FilePathType.Relative)
        crs = api["QgsCoordinateReferenceSystem"]("EPSG:4326")
        project.setCrs(crs)

        metadata = api["QgsProjectMetadata"]()
        metadata.setTitle("Cooma Spatial Foundation v0.1")
        metadata.setAuthor("ClimateOS — Founder-authorized local QGIS foundation")
        metadata.setAbstract(
            "SKELETON + SYNTHETIC NAVIGATION ANCHOR. Real data downloaded: NONE. "
            "Scientific conclusions: NONE. The visible point and rectangle are "
            "learning aids, not scientific evidence or true study boundaries."
        )
        project.setMetadata(metadata)

        root_group = project.layerTreeRoot()
        groups = {name: root_group.addGroup(name) for name in PROJECT_LAYER_GROUPS}
        groups["06_PUBLIC_INFRASTRUCTURE_LATER"].setItemVisibilityChecked(False)
        groups["99_DISABLED_LATER_LAYERS"].setItemVisibilityChecked(False)
        _populate_project(api, project, groups, root / "local_anchor")

        variables = {
            "climateos_scope_status": PROVISIONAL_SCOPE_STATUS,
            "climateos_project_state": "SKELETON + SYNTHETIC NAVIGATION ANCHOR",
            "climateos_source_data_status": "NOT_RETRIEVED",
            "climateos_derived_data_status": "NONE",
            "climateos_scientific_conclusion": SCIENTIFIC_CONCLUSION,
            "climateos_public_data_retrieval_gate": "FOUNDER_APPROVAL_REQUIRED",
            "climateos_bookmark_status": "PROVISIONAL NAVIGATION BOOKMARKS",
        }
        for name, value in variables.items():
            api["QgsExpressionContextUtils"].setProjectVariable(project, name, value)

        bookmark_manager = project.bookmarkManager()
        for index, item in enumerate(BOOKMARKS, start=1):
            bookmark_crs = api["QgsCoordinateReferenceSystem"](item["crs"])
            referenced_extent = api["QgsReferencedRectangle"](
                api["QgsRectangle"](*item["extent"]), bookmark_crs
            )
            bookmark = api["QgsBookmark"]()
            bookmark.setId(f"climateos-cooma-bookmark-{index}")
            bookmark.setName(item["name"])
            bookmark.setGroup("PROVISIONAL NAVIGATION BOOKMARKS — NOT EVIDENCE")
            bookmark.setExtent(referenced_extent)
            if not bookmark_manager.addBookmark(bookmark):
                raise SpatialProjectError(f"failed to add bookmark: {item['name']}")

        project.viewSettings().setDefaultViewExtent(
            api["QgsReferencedRectangle"](api["QgsRectangle"](*DEFAULT_VIEW_EXTENT), crs)
        )
        project.viewSettings().setPresetFullExtent(
            api["QgsReferencedRectangle"](api["QgsRectangle"](*BOOKMARKS[-1]["extent"]), crs)
        )
        if not project.write(str(project_path)):
            raise SpatialProjectError("QGIS refused to write the project")
    finally:
        if project is not None:
            project.clear()
            del project
        application.exitQgis()
        del application

    digest = hashlib.sha256(project_path.read_bytes()).hexdigest()
    anchor_records = [
        {
            "filename": path.name,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "status": "SYNTHETIC_NAVIGATION_ANCHOR_NOT_EVIDENCE",
        }
        for path in anchor_paths
    ]
    manifest = {
        "schema_id": "climateos.qgis-project-ux-revision-manifest.v1",
        "project_filename": project_path.name,
        "project_sha256": digest,
        "qgis_version_required": "3.44.11",
        "source_data": [],
        "derived_data": [],
        "synthetic_navigation_files": anchor_records,
        "layer_groups": list(PROJECT_LAYER_GROUPS),
        "layers": list(SYNTHETIC_LAYER_NAMES),
        "bookmarks": [item["name"] for item in BOOKMARKS],
        "scope_status": PROVISIONAL_SCOPE_STATUS,
        "scientific_conclusion": SCIENTIFIC_CONCLUSION,
        "network_basemap": "NONE",
        "public_data_retrieval": "NONE",
        "revision_safe_output": revision,
    }
    with manifest_path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(manifest, handle, indent=2, sort_keys=True, ensure_ascii=False)
        handle.write("\n")
    return {
        "project_path": str(project_path),
        "project_sha256": digest,
        "synthetic_layer_count": len(SYNTHETIC_LAYER_NAMES),
        "revision_safe_output": revision,
    }


def _feature_properties(layer) -> dict[str, object]:
    feature = next(layer.getFeatures(), None)
    if feature is None:
        raise SpatialProjectError(f"layer contains no feature: {layer.name()}")
    return {field.name(): feature[field.name()] for field in layer.fields()}


def _same_extent(first, second: tuple[float, float, float, float]) -> bool:
    observed = (first.xMinimum(), first.yMinimum(), first.xMaximum(), first.yMaximum())
    return all(abs(left - right) < 1e-8 for left, right in zip(observed, second))


def _verify_project(repo_root: Path, osgeo_root: Path) -> dict[str, object]:
    workspace = ensure_local_workspace(repo_root)
    root = workspace["root"]
    project_path = (
        workspace["revision_project_path"]
        if workspace["revision_project_path"].is_file()
        else workspace["project_path"]
    )
    manifest_path = (
        root / "manifests" / "project_ux_revision_manifest.json"
        if project_path.name == REVISION_PROJECT_FILENAME
        else root / "manifests" / "project_build_manifest.json"
    )
    if not project_path.is_file():
        raise SpatialProjectError(f"project does not exist: {project_path}")

    profile = root / ".qgis-profile"
    profile.mkdir(exist_ok=True)
    os.chdir(root)
    api = _qgis_api(osgeo_root, profile)
    application = _new_qgis_application(api, osgeo_root)
    project = None
    try:
        project = api["QgsProject"]()
        if not project.read(str(project_path)):
            raise SpatialProjectError("QGIS could not reopen the project")
        groups = [child.name() for child in project.layerTreeRoot().children()]
        if groups != list(PROJECT_LAYER_GROUPS):
            raise SpatialProjectError(f"layer group mismatch: {groups}")

        bookmarks = project.bookmarkManager().bookmarks()
        bookmark_names = [bookmark.name() for bookmark in bookmarks]
        if bookmark_names != [item["name"] for item in BOOKMARKS]:
            raise SpatialProjectError(f"bookmark mismatch: {bookmark_names}")
        bookmark_extents = {
            (
                bookmark.extent().xMinimum(),
                bookmark.extent().yMinimum(),
                bookmark.extent().xMaximum(),
                bookmark.extent().yMaximum(),
            )
            for bookmark in bookmarks
        }
        if len(bookmark_extents) != len(BOOKMARKS):
            raise SpatialProjectError("bookmark extents must all be visibly distinct")

        layers = {layer.name(): layer for layer in project.mapLayers().values()}
        if set(layers) != set(SYNTHETIC_LAYER_NAMES):
            raise SpatialProjectError(f"project layer mismatch: {sorted(layers)}")
        invalid = [name for name, layer in layers.items() if not layer.isValid()]
        if invalid:
            raise SpatialProjectError(f"broken layers found: {invalid}")
        for name, layer in layers.items():
            if layer.providerType() != "ogr":
                raise SpatialProjectError(f"unexpected layer provider for {name}: {layer.providerType()}")
            source_path = Path(layer.source().split("|", 1)[0]).resolve()
            if root not in source_path.parents or source_path.parent != root / "local_anchor":
                raise SpatialProjectError(f"layer source escapes controlled local_anchor: {source_path}")

        centre = _feature_properties(layers[START_HERE_MESSAGES[1]])
        extent = _feature_properties(layers[START_HERE_MESSAGES[2]])
        for properties in (centre, extent):
            if properties.get("scientific_status") != "NOT_EVIDENCE":
                raise SpatialProjectError("synthetic feature is missing NOT_EVIDENCE")
            if properties.get("scope_status") != "PROVISIONAL":
                raise SpatialProjectError("synthetic feature is missing PROVISIONAL scope")
            if properties.get("purpose") != "LEARNING_AND_NAVIGATION_ONLY":
                raise SpatialProjectError("synthetic feature purpose is not closed")
        if not _same_extent(project.viewSettings().defaultViewExtent(), DEFAULT_VIEW_EXTENT):
            raise SpatialProjectError("project does not open at the provisional Cooma extent")
        if project.filePathStorage() != api["Qgis"].FilePathType.Relative:
            raise SpatialProjectError("project path storage is not relative")
    finally:
        if project is not None:
            project.clear()
            del project
        application.exitQgis()
        del application

    with zipfile.ZipFile(project_path) as archive:
        qgs_names = [name for name in archive.namelist() if name.endswith(".qgs")]
        if len(qgs_names) != 1:
            raise SpatialProjectError("QGZ must contain exactly one QGS document")
        xml = archive.read(qgs_names[0]).decode("utf-8")
    lowered = xml.lower()
    if str(root).lower() in lowered:
        raise SpatialProjectError("project contains an uncontrolled absolute workspace path")
    network_check_xml = lowered.replace("http://mrcc.com/qgis.dtd", "")
    for prohibited in (
        "http://",
        "https://",
        "type=xyz",
        "<provider>wms</provider>",
        "<provider>wfs</provider>",
    ):
        if prohibited in network_check_xml:
            raise SpatialProjectError(f"network basemap or service found: {prohibited}")
    for layer_name in SYNTHETIC_LAYER_NAMES:
        if layer_name not in xml:
            raise SpatialProjectError(f"missing project layer: {layer_name}")

    digest = hashlib.sha256(project_path.read_bytes()).hexdigest()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest["project_sha256"] != digest:
        raise SpatialProjectError("project digest does not match its build manifest")
    if list((root / "source_data").glob("**/*")):
        raise SpatialProjectError("source_data must remain empty")
    if list((root / "derived_data").glob("**/*")):
        raise SpatialProjectError("derived_data must remain empty")
    return {
        "project_path": str(project_path),
        "project_sha256": digest,
        "roundtrip": "PASS",
        "relative_paths": "PASS",
        "default_extent": "PASS",
        "broken_layer_count": 0,
        "network_basemap_count": 0,
        "public_data_download_count": 0,
        "derived_scientific_layer_count": 0,
        "synthetic_layer_count": len(SYNTHETIC_LAYER_NAMES),
        "bookmark_extent_count": len(BOOKMARKS),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("build", "revise", "verify"))
    parser.add_argument("--osgeo-root", default="D:\\")
    args = parser.parse_args(argv)
    try:
        if args.action == "build":
            result = _build_project(_repo_root(), Path(args.osgeo_root), revision=False)
        elif args.action == "revise":
            result = _build_project(_repo_root(), Path(args.osgeo_root), revision=True)
        else:
            result = _verify_project(_repo_root(), Path(args.osgeo_root))
    except (
        OSError,
        SpatialProjectError,
        SpatialWorkspaceError,
        SyntheticAnchorError,
        ValueError,
    ) as exc:
        print(json.dumps({"status": "ERROR", "error": str(exc)}, ensure_ascii=False))
        return 1
    print(json.dumps({"status": "PASS", **result}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
