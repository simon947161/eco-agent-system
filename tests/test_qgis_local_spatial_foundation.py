from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from cczps_lite.qgis_local_spatial_foundation import (
    BOOKMARKS,
    DEFAULT_VIEW_EXTENT,
    PROJECT_FILENAME,
    PROJECT_LAYER_GROUPS,
    PROVISIONAL_SCOPE_STATUS,
    REVISION_PROJECT_FILENAME,
    WORKSPACE_DIRECTORIES,
    SpatialWorkspaceError,
    ensure_local_workspace,
)
from cczps_lite.qgis_local_spatial_foundation.contract import (
    START_HERE_MESSAGES,
    SYNTHETIC_LAYER_NAMES,
    TERRAIN_INFO_LAYER,
    WATER_INFO_LAYER,
)
from cczps_lite.qgis_local_spatial_foundation.synthetic_anchor import (
    ANCHOR_FILENAMES,
    SyntheticAnchorError,
    ensure_synthetic_anchor_files,
    synthetic_anchor_payloads,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = REPO_ROOT / "cczps_lite" / "qgis_local_spatial_foundation"
TASK_ROOT = REPO_ROOT / "docs" / "tasks" / "task2021_2030_qgis_local_spatial_foundation"


def _properties(filename: str) -> dict[str, object]:
    return synthetic_anchor_payloads()[filename]["features"][0]["properties"]


class QgisLocalSpatialFoundationTests(unittest.TestCase):
    def test_01_workspace_structure_and_contract_are_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            test_root = Path(temp) / "controlled"
            first = ensure_local_workspace(REPO_ROOT, test_root=test_root)
            second = ensure_local_workspace(REPO_ROOT, test_root=test_root)
            self.assertEqual(first["contract"], second["contract"])
            self.assertEqual({path.name for path in first["directories"]}, set(WORKSPACE_DIRECTORIES))
            self.assertIn("local_anchor", WORKSPACE_DIRECTORIES)
            self.assertEqual(first["revision_project_path"].name, REVISION_PROJECT_FILENAME)

    def test_02_changed_workspace_contract_is_not_overwritten(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            test_root = Path(temp) / "controlled"
            result = ensure_local_workspace(REPO_ROOT, test_root=test_root)
            result["contract_path"].write_text("{}\n", encoding="utf-8")
            with self.assertRaisesRegex(SpatialWorkspaceError, "overwrite refused"):
                ensure_local_workspace(REPO_ROOT, test_root=test_root)
            self.assertEqual(result["contract_path"].read_text(encoding="utf-8"), "{}\n")

    def test_03_project_generator_contract_has_required_groups(self) -> None:
        self.assertEqual(len(PROJECT_LAYER_GROUPS), 10)
        self.assertEqual(PROJECT_LAYER_GROUPS[0], "00_START_HERE")
        self.assertIn("02_TERRAIN", PROJECT_LAYER_GROUPS)
        self.assertIn("03_WATER", PROJECT_LAYER_GROUPS)

    def test_04_project_generator_contract_has_five_bookmarks(self) -> None:
        self.assertEqual(
            [item["name"] for item in BOOKMARKS],
            ["Cooma Town", "Wider Cooma Context", "Terrain Overview", "Main Waterways", "Catchment Context"],
        )

    def test_05_bookmark_extents_are_bounded_and_distinct(self) -> None:
        extents = {tuple(item["extent"]) for item in BOOKMARKS}
        self.assertEqual(len(extents), 5)
        for west, south, east, north in extents:
            self.assertLess(west, east)
            self.assertLess(south, north)
            self.assertGreaterEqual(west, 148.0)
            self.assertLessEqual(east, 150.0)
            self.assertGreaterEqual(south, -37.5)
            self.assertLessEqual(north, -35.0)

    def test_06_synthetic_centre_point_is_visible_geometry(self) -> None:
        payload = synthetic_anchor_payloads()[ANCHOR_FILENAMES["centre"]]
        feature = payload["features"][0]
        self.assertEqual(feature["geometry"]["type"], "Point")
        self.assertEqual(feature["properties"]["name"], "Cooma Provisional Centre")

    def test_07_provisional_extent_is_visible_polygon(self) -> None:
        payload = synthetic_anchor_payloads()[ANCHOR_FILENAMES["extent"]]
        feature = payload["features"][0]
        self.assertEqual(feature["geometry"]["type"], "Polygon")
        self.assertTrue(feature["properties"]["human_review_required"])
        self.assertEqual(feature["properties"]["boundary_warning"], "NOT_A_CATCHMENT_COUNCIL_OR_SCIENTIFIC_BOUNDARY")

    def test_08_synthetic_features_are_not_evidence(self) -> None:
        for key in ("centre", "extent"):
            properties = _properties(ANCHOR_FILENAMES[key])
            self.assertEqual(properties["scientific_status"], "NOT_EVIDENCE")
            self.assertEqual(properties["scope_status"], "PROVISIONAL")
            self.assertEqual(properties["purpose"], "LEARNING_AND_NAVIGATION_ONLY")

    def test_09_terrain_info_placeholder_is_non_spatial(self) -> None:
        payload = synthetic_anchor_payloads()[ANCHOR_FILENAMES["terrain_info"]]
        feature = payload["features"][0]
        self.assertIsNone(feature["geometry"])
        self.assertEqual(feature["properties"]["name"], TERRAIN_INFO_LAYER)
        self.assertIn("DEM", feature["properties"]["future_layers"])

    def test_10_water_info_placeholder_is_non_spatial(self) -> None:
        payload = synthetic_anchor_payloads()[ANCHOR_FILENAMES["water_info"]]
        feature = payload["features"][0]
        self.assertIsNone(feature["geometry"])
        self.assertEqual(feature["properties"]["name"], WATER_INFO_LAYER)
        self.assertIn("Rivers", feature["properties"]["future_layers"])

    def test_11_start_here_learning_layer_is_closed(self) -> None:
        properties = _properties(ANCHOR_FILENAMES["start_here"])
        self.assertEqual(properties["name"], START_HERE_MESSAGES[0])
        self.assertEqual(properties["real_data_downloaded"], "NONE")
        self.assertEqual(properties["scientific_conclusions"], "NONE")
        self.assertIn("not scientific evidence", properties["warning"])

    def test_12_synthetic_files_are_reproducible_and_refuse_changes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "local_anchor"
            first = ensure_synthetic_anchor_files(root)
            second = ensure_synthetic_anchor_files(root)
            self.assertEqual([path.read_bytes() for path in first], [path.read_bytes() for path in second])
            first[0].write_text("{}\n", encoding="utf-8")
            with self.assertRaisesRegex(SyntheticAnchorError, "overwrite refused"):
                ensure_synthetic_anchor_files(root)

    def test_13_no_real_spatial_data_is_in_synthetic_payloads(self) -> None:
        serialized = json.dumps(synthetic_anchor_payloads(), sort_keys=True)
        for prohibited in ("fake river", "fake catchment", "elevation_value", "station_observation"):
            self.assertNotIn(prohibited, serialized.lower())
        self.assertEqual(len(synthetic_anchor_payloads()), 5)

    def test_14_no_network_basemap_or_client_is_configured(self) -> None:
        source = (PACKAGE_ROOT / "project_builder.py").read_text(encoding="utf-8").lower()
        for prohibited in ("requests", "urllib.request", "httpx", "aiohttp", "openstreetmap", "google", "bing", "esri"):
            self.assertNotIn(prohibited, source)
        self.assertIn("network_basemap_count", source)

    def test_15_project_paths_and_default_extent_are_controlled(self) -> None:
        self.assertEqual(PROJECT_FILENAME, "Cooma_Spatial_Foundation_v0_1.qgz")
        self.assertEqual(REVISION_PROJECT_FILENAME, "Cooma_Spatial_Foundation_v0_1_ux_revision.qgz")
        self.assertEqual(DEFAULT_VIEW_EXTENT, (149.03, -36.31, 149.21, -36.15))
        self.assertEqual(PROVISIONAL_SCOPE_STATUS, "PROVISIONAL_SPATIAL_SCOPE / HUMAN_REVIEW_REQUIRED")

    def test_16_revision_action_is_explicit_and_reruns_refuse_overwrite(self) -> None:
        source = (PACKAGE_ROOT / "project_builder.py").read_text(encoding="utf-8")
        self.assertIn('choices=("build", "revise", "verify")', source)
        self.assertIn("project already exists; overwrite refused", source)
        launcher = (REPO_ROOT / "run_qgis_local_spatial_foundation.ps1").read_text(encoding="utf-8")
        self.assertIn('"Revise"', launcher)

    def test_17_runtime_outputs_are_ignored_and_prototype_is_out_of_scope(self) -> None:
        gitignore = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("runtime_data/", gitignore)
        source_text = "\n".join(path.read_text(encoding="utf-8") for path in PACKAGE_ROOT.glob("*.py"))
        self.assertNotIn("prototype/", source_text)

    def test_18_source_registry_remains_metadata_only(self) -> None:
        registry = json.loads((PACKAGE_ROOT / "source_registry.json").read_text(encoding="utf-8"))
        self.assertEqual(registry["registry_status"], "METADATA_ONLY_NO_DATA_RETRIEVED")
        self.assertEqual(registry["retrieval_gate"], "FOUNDER_APPROVAL_REQUIRED")
        for source in registry["sources"]:
            self.assertIsNone(source["retrieval_date"])
            self.assertIn("NOT_RETRIEVED", source["admission_status"])
        for derived in registry["derived_products"]:
            self.assertEqual(derived["status"], "NOT_CREATED")

    def test_19_guide_and_revision_governance_documents_exist(self) -> None:
        required = (
            "TASK2021_2030_QGIS_SKELETON_UX_REVISION_PREFLIGHT.md",
            "QGIS_COOMA_10_MINUTE_RESTART_GUIDE.md",
            "TASK2030_FOUNDER_GATE.md",
        )
        for filename in required:
            self.assertTrue((TASK_ROOT / filename).is_file(), filename)
        guide = (TASK_ROOT / "QGIS_COOMA_10_MINUTE_RESTART_GUIDE.md").read_text(encoding="utf-8")
        for required_text in (
            "Don't Save",
            "Cancel stops",
            "View → Panels → Spatial Bookmarks",
            "New Spatial Bookmark",
            "NOT_EVIDENCE",
        ):
            self.assertIn(required_text, guide)

    def test_20_layer_name_contract_is_exact(self) -> None:
        self.assertEqual(len(SYNTHETIC_LAYER_NAMES), 5)
        self.assertEqual(SYNTHETIC_LAYER_NAMES[0], "START HERE — QGIS Cooma Learning Guide")
        self.assertTrue(TERRAIN_INFO_LAYER.startswith("INFO —"))
        self.assertTrue(WATER_INFO_LAYER.startswith("INFO —"))


if __name__ == "__main__":
    unittest.main()
