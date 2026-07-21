from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from cczps_lite.qgis_local_spatial_foundation.hydrology_contract import (
    AUTHORIZED_LONGITUDE_LATITUDE_EXTENT,
    DERIVED_FILES,
    DERIVED_HYDROLOGY_LIMIT,
    HYDROLOGY_BOOKMARKS,
    HYDROLOGY_LAYER_NAMES,
    HYDROLOGY_LICENCE,
    HYDROLOGY_PROJECT_CRS,
    HYDROLOGY_PROJECT_FILENAME,
    HYDROLOGY_SOURCE_CRS,
    HYDROLOGY_SOURCES,
    HYDROLOGY_VERSION,
    NETWORK_RETRIEVAL_LIMIT,
    RAW_HYDROLOGY_LIMIT,
    STACKED_PR_BASE,
    TERRAIN_BASE_HEAD,
    WORKSPACE_LIMIT,
    hydrology_size_limits,
)
from cczps_lite.qgis_local_spatial_foundation.hydrology_pack import (
    HydrologyPackError,
    _assert_confined,
    _ensure_new_file,
    _query_parameters,
    _sha256,
    _validate_geojson,
    load_source_registry,
)
from cczps_lite.qgis_local_spatial_foundation.terrain_contract import TERRAIN_LAYER_NAMES


REPO_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = REPO_ROOT / "cczps_lite" / "qgis_local_spatial_foundation"
TASK_ROOT = REPO_ROOT / "docs" / "tasks" / "task2041_2050_qgis_cooma_hydrology_pack"


class QgisCoomaHydrologyPackTests(unittest.TestCase):
    def test_01_source_identity_is_closed(self) -> None:
        registry = load_source_registry(PACKAGE_ROOT)
        self.assertEqual(registry["registry_status"], "CLOSED_FOUNDER_AUTHORIZED")
        self.assertEqual(registry["product"], "Australian Hydrological Geospatial Fabric (Geofabric)")

    def test_02_version_and_licence_are_exact(self) -> None:
        self.assertEqual(HYDROLOGY_VERSION, "V3.3")
        self.assertEqual(HYDROLOGY_LICENCE, "Creative Commons Attribution 4.0 International (CC BY 4.0)")

    def test_03_layer_set_is_exact(self) -> None:
        self.assertEqual([item["layer_id"] for item in HYDROLOGY_SOURCES], [6, 31, 33, 27])

    def test_04_no_silent_nsw_fallback(self) -> None:
        registry = load_source_registry(PACKAGE_ROOT)
        self.assertEqual(registry["source_policy"], "BOM_GEOFABRIC_ONLY_NO_SILENT_FALLBACK_COMBINATION")

    def test_05_bounded_extent_is_exact(self) -> None:
        self.assertEqual(
            AUTHORIZED_LONGITUDE_LATITUDE_EXTENT,
            {"west": 148.9359628223, "east": 149.2892495063, "south": -36.3977706857, "north": -36.0986116526},
        )

    def test_06_size_ceilings_are_exact(self) -> None:
        self.assertEqual(NETWORK_RETRIEVAL_LIMIT, 150 * 1024 * 1024)
        self.assertEqual(RAW_HYDROLOGY_LIMIT, 100 * 1024 * 1024)
        self.assertEqual(DERIVED_HYDROLOGY_LIMIT, 150 * 1024 * 1024)
        self.assertEqual(WORKSPACE_LIMIT, 800 * 1024 * 1024)
        self.assertEqual(hydrology_size_limits()["workspace"], WORKSPACE_LIMIT)

    def test_07_path_confinement_rejects_escape(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "controlled"
            root.mkdir()
            _assert_confined(root / "inside.gpkg", root)
            with self.assertRaisesRegex(HydrologyPackError, "escapes"):
                _assert_confined(root.parent / "outside.gpkg", root)

    def test_08_checksum_is_sha256(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "fixture.bin"
            path.write_bytes(b"synthetic hydrology fixture")
            self.assertEqual(len(_sha256(path)), 64)

    def test_09_overwrite_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "existing.gpkg"
            path.write_bytes(b"fixture")
            with self.assertRaisesRegex(HydrologyPackError, "overwrite refused"):
                _ensure_new_file(path)

    def test_10_query_is_bbox_confined(self) -> None:
        query = _query_parameters()
        self.assertEqual(query["geometry"], "148.9359628223,-36.3977706857,149.2892495063,-36.0986116526")
        self.assertEqual(query["geometryType"], "esriGeometryEnvelope")

    def test_11_crs_handling_is_explicit(self) -> None:
        self.assertEqual(HYDROLOGY_SOURCE_CRS, "EPSG:4283")
        self.assertEqual(HYDROLOGY_PROJECT_CRS, "EPSG:7855")

    def test_12_geojson_validation_rejects_non_collection(self) -> None:
        with self.assertRaisesRegex(HydrologyPackError, "FeatureCollection"):
            _validate_geojson({"type": "Feature"}, HYDROLOGY_SOURCES[0])

    def test_13_expected_layer_names_are_closed(self) -> None:
        self.assertEqual(len(HYDROLOGY_LAYER_NAMES), 6)
        self.assertIn("Main Rivers and Watercourses", HYDROLOGY_LAYER_NAMES[0])
        self.assertIn("source and limitations", HYDROLOGY_LAYER_NAMES[-1])

    def test_14_no_fabricated_stream_classification(self) -> None:
        source = (PACKAGE_ROOT / "hydrology_pack.py").read_text(encoding="utf-8")
        self.assertIn('fields.get("hierarchy") == "Major"', source)
        self.assertIn('fields.get("hierarchy") == "Minor"', source)
        self.assertIn("PRESERVE_OFFICIAL_GEOFABRIC_FIELDS_NO_FABRICATED_CLASSIFICATION", source)

    def test_15_locality_and_catchment_are_distinct(self) -> None:
        source = (PACKAGE_ROOT / "hydrology_pack.py").read_text(encoding="utf-8")
        self.assertIn('"locality_is_catchment": False', source)
        self.assertIn('"climateos_locality_is_catchment": "FALSE"', source)

    def test_16_council_boundary_is_not_implied(self) -> None:
        source = (PACKAGE_ROOT / "hydrology_pack.py").read_text(encoding="utf-8")
        self.assertIn('"council_boundary_present": False', source)

    def test_17_terrain_layers_remain_required(self) -> None:
        source = (PACKAGE_ROOT / "hydrology_pack.py").read_text(encoding="utf-8")
        for name in TERRAIN_LAYER_NAMES:
            self.assertIn(name, TERRAIN_LAYER_NAMES)
        self.assertIn("*TERRAIN_LAYER_NAMES", source)

    def test_18_project_filename_is_new(self) -> None:
        self.assertEqual(HYDROLOGY_PROJECT_FILENAME, "Cooma_Spatial_Foundation_v0_3_hydrology.qgz")

    def test_19_bookmarks_are_exact(self) -> None:
        self.assertEqual(
            HYDROLOGY_BOOKMARKS,
            ("Cooma Watercourses", "Cooma Catchment Context", "Terrain and Water Relationship"),
        )

    def test_20_no_web_provider(self) -> None:
        source = (PACKAGE_ROOT / "hydrology_pack.py").read_text(encoding="utf-8").lower()
        self.assertIn('"network_provider": "none"', source)
        for prohibited in ("openstreetmap", "google earth", "bing maps"):
            self.assertNotIn(prohibited, source)

    def test_21_no_scientific_conclusion(self) -> None:
        registry = load_source_registry(PACKAGE_ROOT)
        self.assertEqual(registry["scientific_conclusion"], "NONE")

    def test_22_runtime_data_is_ignored(self) -> None:
        self.assertIn("runtime_data/", (REPO_ROOT / ".gitignore").read_text(encoding="utf-8"))

    def test_23_no_real_hydrology_data_is_tracked(self) -> None:
        tracked = subprocess.run(
            ["git", "ls-files", "runtime_data"], cwd=REPO_ROOT, check=True, text=True, capture_output=True
        ).stdout.strip()
        self.assertEqual(tracked, "")

    def test_24_prototype_is_not_referenced(self) -> None:
        source = "\n".join(path.read_text(encoding="utf-8") for path in PACKAGE_ROOT.glob("hydrology_*.py"))
        self.assertNotIn("prototype/", source)

    def test_25_stacked_pr_base_is_exact(self) -> None:
        self.assertEqual(STACKED_PR_BASE, "agent/task2031-2040-qgis-cooma-terrain-boundary-pack")
        self.assertEqual(TERRAIN_BASE_HEAD, "57e71468514253c188c9a744e3532a67903b0272")

    def test_26_derived_paths_are_fixed(self) -> None:
        self.assertEqual(set(DERIVED_FILES), {"main_watercourses", "secondary_streams", "catchment_context", "subcatchment_context", "named_water_features"})

    def test_27_required_documents_exist(self) -> None:
        for name in (
            "TASK2041_2050_QGIS_COOMA_HYDROLOGY_PACK_REPORT.md",
            "TASK2050_FOUNDER_QGIS_HYDROLOGY_GATE.md",
            "TASK2040_FOUNDER_TERRAIN_RETEST_REMINDER.md",
        ):
            self.assertTrue((TASK_ROOT / name).is_file())

    def test_28_gate_language_is_exact(self) -> None:
        gate = (TASK_ROOT / "TASK2050_FOUNDER_QGIS_HYDROLOGY_GATE.md").read_text(encoding="utf-8")
        self.assertIn("READY_FOR_FOUNDER_QGIS_HYDROLOGY_REVIEW", gate)
        self.assertIn("STACKED_ON_UNMERGED_PR95", gate)
        self.assertIn("DO_NOT_AUTO_MERGE", gate)

    def test_29_terrain_retest_remains_deferred(self) -> None:
        reminder = (TASK_ROOT / "TASK2040_FOUNDER_TERRAIN_RETEST_REMINDER.md").read_text(encoding="utf-8")
        for phrase in ("second bookmark", "layer differentiation", "DEM Identify", "Slope Identify"):
            self.assertIn(phrase, reminder)
        self.assertIn("PR #95 remains unaccepted", reminder)


if __name__ == "__main__":
    unittest.main()
