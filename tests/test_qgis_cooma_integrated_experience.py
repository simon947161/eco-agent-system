from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from cczps_lite.qgis_local_spatial_foundation.integrated_contract import (
    AUTHORIZED_LONGITUDE_LATITUDE_EXTENT,
    DEFAULT_VISIBLE_LAYERS,
    HYDROLOGY_BASE_PROJECT_FILENAME,
    IMAGERY_LAYER_NAME,
    IMAGERY_SERVICE,
    IMAGERY_TILE_URL,
    INTEGRATED_BASE_HEAD,
    INTEGRATED_BOOKMARKS,
    INTEGRATED_PROJECT_CRS,
    INTEGRATED_PROJECT_FILENAME,
    ROAD_LAYER_NAME,
    ROAD_QUERY_URL,
    WORKSPACE_LIMIT,
    integrated_size_limits,
)
from cczps_lite.qgis_local_spatial_foundation.integrated_pack import (
    IntegratedExperienceError,
    _assert_confined,
    _ensure_new_file,
    _road_query_parameters,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = REPO_ROOT / "cczps_lite" / "qgis_local_spatial_foundation"
TASK_ROOT = REPO_ROOT / "docs" / "tasks" / "task2051_2060_qgis_cooma_integrated_experience"


class QgisCoomaIntegratedExperienceTests(unittest.TestCase):
    def test_01_base_is_accepted_hydrology_main(self) -> None:
        self.assertEqual(INTEGRATED_BASE_HEAD, "4ed5afc98d547acb1cddb688fdca53c9a5fc975e")
        self.assertEqual(HYDROLOGY_BASE_PROJECT_FILENAME, "Cooma_Spatial_Foundation_v0_3_hydrology.qgz")

    def test_02_one_new_integrated_project_filename(self) -> None:
        self.assertEqual(INTEGRATED_PROJECT_FILENAME, "Cooma_Spatial_Foundation_v0_4_integrated.qgz")
        self.assertEqual(INTEGRATED_PROJECT_CRS, "EPSG:7855")

    def test_03_roads_use_exact_nsw_official_layer(self) -> None:
        self.assertEqual(
            ROAD_QUERY_URL,
            "https://portal.spatial.nsw.gov.au/server/rest/services/NSW_Transport_Theme/FeatureServer/5/query",
        )
        self.assertIn("NSW official RoadSegment", ROAD_LAYER_NAME)

    def test_04_imagery_uses_exact_nsw_service(self) -> None:
        self.assertEqual(
            IMAGERY_SERVICE,
            "https://portal.spatial.nsw.gov.au/aid/tile/rest/services/NSWWebImagery/MapServer",
        )
        self.assertEqual(IMAGERY_TILE_URL, IMAGERY_SERVICE + "/tile/{z}/{y}/{x}")
        self.assertIn("online", IMAGERY_LAYER_NAME)

    def test_05_bounded_road_query_is_exact(self) -> None:
        self.assertEqual(
            AUTHORIZED_LONGITUDE_LATITUDE_EXTENT,
            {"west": 148.9359628223, "east": 149.2892495063, "south": -36.3977706857, "north": -36.0986116526},
        )
        query = _road_query_parameters()
        self.assertEqual(query["geometry"], "148.9359628223,-36.3977706857,149.2892495063,-36.0986116526")
        self.assertEqual(query["outSR"], "4326")

    def test_06_integrated_size_ceiling_is_bounded(self) -> None:
        self.assertEqual(WORKSPACE_LIMIT, 1_000 * 1024 * 1024)
        self.assertEqual(integrated_size_limits()["workspace"], WORKSPACE_LIMIT)

    def test_07_path_escape_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "controlled"
            root.mkdir()
            _assert_confined(root / "inside.gpkg", root)
            with self.assertRaisesRegex(IntegratedExperienceError, "escapes"):
                _assert_confined(root.parent / "outside.gpkg", root)

    def test_08_overwrite_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "existing.qgz"
            path.write_text("fixture", encoding="utf-8")
            with self.assertRaisesRegex(IntegratedExperienceError, "overwrite refused"):
                _ensure_new_file(path)

    def test_09_default_view_is_readable_not_everything_on(self) -> None:
        self.assertIn(IMAGERY_LAYER_NAME, DEFAULT_VISIBLE_LAYERS)
        self.assertIn(ROAD_LAYER_NAME, DEFAULT_VISIBLE_LAYERS)
        self.assertIn("Main Rivers and Watercourses", " ".join(DEFAULT_VISIBLE_LAYERS))
        self.assertNotIn("Cooma Slope Degrees — derived", DEFAULT_VISIBLE_LAYERS)

    def test_10_three_integrated_bookmarks_are_closed(self) -> None:
        self.assertEqual(
            INTEGRATED_BOOKMARKS,
            ("Integrated Cooma Overview", "Satellite and Roads", "Terrain and Water Together"),
        )

    def test_11_builder_inherits_then_adds_layers(self) -> None:
        source = (PACKAGE_ROOT / "integrated_pack.py").read_text(encoding="utf-8")
        self.assertIn('project.read(str(layout["base_project"]))', source)
        self.assertIn('groups.get("04_SETTLEMENT_AND_ROADS")', source)
        self.assertIn('api["QgsRasterLayer"](imagery_uri', source)
        self.assertIn('api["QgsVectorLayer"](', source)

    def test_12_imagery_is_only_network_layer(self) -> None:
        source = (PACKAGE_ROOT / "integrated_pack.py").read_text(encoding="utf-8")
        self.assertIn('network_layers != [IMAGERY_LAYER_NAME]', source)
        self.assertNotIn("tile.openstreetmap.org", source)
        self.assertNotIn("Google", source)
        self.assertNotIn("Bing", source)

    def test_13_offline_core_is_explicit(self) -> None:
        source = (PACKAGE_ROOT / "integrated_pack.py").read_text(encoding="utf-8")
        self.assertIn('"climateos_offline_core_available": "TERRAIN_HYDROLOGY_ROADS"', source)
        self.assertIn('"climateos_imagery_online_only": "TRUE"', source)

    def test_14_no_scientific_conclusion(self) -> None:
        source = (PACKAGE_ROOT / "integrated_pack.py").read_text(encoding="utf-8")
        self.assertIn('"scientific_conclusion": "NONE"', source)
        self.assertNotIn("flood risk conclusion", source.lower())

    def test_15_runtime_data_is_not_tracked(self) -> None:
        tracked = subprocess.run(
            ["git", "ls-files", "runtime_data"], cwd=REPO_ROOT, check=True, text=True, capture_output=True
        ).stdout.strip()
        self.assertEqual(tracked, "")

    def test_16_prototype_is_untouched(self) -> None:
        source = "\n".join(
            path.read_text(encoding="utf-8") for path in PACKAGE_ROOT.glob("integrated_*.py")
        )
        self.assertNotIn("prototype/", source)

    def test_17_launcher_has_single_open_entrypoint(self) -> None:
        launcher = (REPO_ROOT / "run_qgis_cooma_integrated_experience.ps1").read_text(encoding="utf-8")
        self.assertIn("Cooma_Spatial_Foundation_v0_4_integrated.qgz", launcher)
        self.assertIn('[ValidateSet("Plan", "Retrieve", "Derive", "BuildProject", "Verify", "Open")]', launcher)

    def test_18_required_task_documents_exist(self) -> None:
        for name in (
            "TASK2051_2060_QGIS_COOMA_INTEGRATED_EXPERIENCE_REPORT.md",
            "QGIS_COOMA_INTEGRATED_FOUNDER_REVIEW_GUIDE.md",
            "TASK2060_FOUNDER_QGIS_INTEGRATED_GATE.md",
        ):
            self.assertTrue((TASK_ROOT / name).is_file())

    def test_19_gate_remains_independent(self) -> None:
        gate = (TASK_ROOT / "TASK2060_FOUNDER_QGIS_INTEGRATED_GATE.md").read_text(encoding="utf-8")
        self.assertIn("READY_FOR_FOUNDER_QGIS_INTEGRATED_REVIEW", gate)
        self.assertIn("DO_NOT_AUTO_MERGE", gate)

    def test_20_user_mental_model_is_one_map_many_layers(self) -> None:
        guide = (TASK_ROOT / "QGIS_COOMA_INTEGRATED_FOUNDER_REVIEW_GUIDE.md").read_text(encoding="utf-8")
        self.assertIn("one project", guide.lower())
        self.assertIn("layer", guide.lower())
        self.assertIn("offline", guide.lower())


if __name__ == "__main__":
    unittest.main()
