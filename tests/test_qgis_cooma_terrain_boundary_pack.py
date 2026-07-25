from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from cczps_lite.qgis_local_spatial_foundation.terrain_contract import (
    BOUNDARY_EXPECTED_IDENTITY,
    BOUNDARY_LIMIT,
    BOUNDARY_LICENCE,
    BOUNDARY_SOURCE_CRS,
    BUFFER_METRES,
    DEM_CELL_SIZE_DEGREES,
    DEM_LICENCE,
    DEM_NODATA,
    DEM_PRODUCT_ID,
    DEM_SOURCE_CRS,
    DEM_VERTICAL_DATUM,
    DERIVED_DATA_LIMIT,
    HILLSHADE_ALTITUDE,
    HILLSHADE_AZIMUTH,
    HILLSHADE_Z_FACTOR,
    NETWORK_RETRIEVAL_LIMIT,
    RAW_DEM_LIMIT,
    SLOPE_UNITS,
    SOURCE_DATA_LIMIT,
    TARGET_CELL_SIZE_METRES,
    TERRAIN_LAYER_NAMES,
    TERRAIN_PROJECT_CRS,
    TERRAIN_PROJECT_FILENAME,
    WORKSPACE_LIMIT,
    size_limits,
)
from cczps_lite.qgis_local_spatial_foundation.terrain_pack import (
    TerrainPackError,
    _assert_confined,
    _boundary_feature,
    _bounded_dem_plan,
    _ensure_regular_new_file,
    _sha256,
    load_source_registry,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = REPO_ROOT / "cczps_lite" / "qgis_local_spatial_foundation"
TASK_ROOT = REPO_ROOT / "docs" / "tasks" / "task2031_2040_qgis_cooma_terrain_boundary_pack"


def _official_feature() -> dict[str, object]:
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": dict(BOUNDARY_EXPECTED_IDENTITY),
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[149.0, -36.3], [149.2, -36.3], [149.2, -36.1], [149.0, -36.3]]],
                },
            }
        ],
    }


class QgisCoomaTerrainBoundaryPackTests(unittest.TestCase):
    def test_01_source_registry_identity_is_closed(self) -> None:
        registry = load_source_registry(PACKAGE_ROOT)
        self.assertEqual(registry["registry_status"], "CLOSED_FOUNDER_AUTHORIZED")
        self.assertEqual(len(registry["sources"]), 2)

    def test_02_every_source_requires_a_licence(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            payload = load_source_registry(PACKAGE_ROOT)
            payload["sources"][0]["licence"] = ""
            (root / "terrain_source_registry.json").write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(TerrainPackError, "licence"):
                load_source_registry(root)

    def test_03_hard_size_ceilings_are_exact(self) -> None:
        self.assertEqual(
            size_limits(),
            {
                "network_retrieval": NETWORK_RETRIEVAL_LIMIT,
                "raw_dem": RAW_DEM_LIMIT,
                "administrative_boundary": BOUNDARY_LIMIT,
                "source_data": SOURCE_DATA_LIMIT,
                "derived_data": DERIVED_DATA_LIMIT,
                "workspace": WORKSPACE_LIMIT,
            },
        )
        self.assertEqual(NETWORK_RETRIEVAL_LIMIT, 250 * 1024 * 1024)

    def test_04_bounded_extent_plan_stays_small(self) -> None:
        plan = _bounded_dem_plan({"west": 149.0, "east": 149.3, "south": -36.4, "north": -36.1})
        self.assertLess(plan["uncompressed_bytes"], RAW_DEM_LIMIT)
        self.assertLess(plan["conservative_network_bytes"], NETWORK_RETRIEVAL_LIMIT)

    def test_05_path_confinement_rejects_escape(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "controlled"
            root.mkdir()
            _assert_confined(root / "inside.tif", root)
            with self.assertRaisesRegex(TerrainPackError, "escapes"):
                _assert_confined(root.parent / "outside.tif", root)

    def test_06_checksum_is_sha256(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "fixture.bin"
            path.write_bytes(b"bounded synthetic fixture")
            self.assertEqual(len(_sha256(path)), 64)

    def test_07_new_file_only_refuses_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "existing.tif"
            path.write_bytes(b"fixture")
            with self.assertRaisesRegex(TerrainPackError, "overwrite refused"):
                _ensure_regular_new_file(path)

    def test_08_dem_metadata_contract_is_complete(self) -> None:
        self.assertEqual(DEM_PRODUCT_ID, "ga_srtm_dem1sv1_0")
        self.assertEqual(DEM_SOURCE_CRS, "EPSG:4326")
        self.assertEqual(DEM_VERTICAL_DATUM, "EGM96")
        self.assertLess(DEM_NODATA, -1e30)
        self.assertAlmostEqual(DEM_CELL_SIZE_DEGREES, 1 / 3600, places=12)
        self.assertIn("4.0", DEM_LICENCE)

    def test_09_projected_metric_crs_is_required(self) -> None:
        self.assertEqual(TERRAIN_PROJECT_CRS, "EPSG:7855")
        self.assertEqual(TARGET_CELL_SIZE_METRES, 30.0)
        self.assertNotEqual(TERRAIN_PROJECT_CRS, DEM_SOURCE_CRS)

    def test_10_hillshade_manifest_parameters_are_closed(self) -> None:
        self.assertEqual((HILLSHADE_AZIMUTH, HILLSHADE_ALTITUDE, HILLSHADE_Z_FACTOR), (315.0, 45.0, 1.0))

    def test_11_slope_units_are_degrees(self) -> None:
        self.assertEqual(SLOPE_UNITS, "degrees")
        source = (PACKAGE_ROOT / "terrain_pack.py").read_text(encoding="utf-8")
        self.assertIn('"units": SLOPE_UNITS', source)

    def test_12_scientific_conclusion_is_none(self) -> None:
        registry = load_source_registry(PACKAGE_ROOT)
        self.assertEqual(registry["scientific_conclusion"], "NONE")
        guide = (TASK_ROOT / "QGIS_COOMA_TERRAIN_REVIEW_GUIDE.md").read_text(encoding="utf-8")
        self.assertIn("NO_SCIENTIFIC_CONCLUSION", guide)

    def test_13_no_network_basemap_is_configured(self) -> None:
        source = (PACKAGE_ROOT / "terrain_pack.py").read_text(encoding="utf-8").lower()
        for prohibited in ("openstreetmap", "google earth", "bing maps"):
            self.assertNotIn(prohibited, source)
        self.assertIn('"network_basemap": "none"', source)
        self.assertIn('"type=xyz"', source)

    def test_14_real_runtime_data_is_git_ignored(self) -> None:
        self.assertIn("runtime_data/", (REPO_ROOT / ".gitignore").read_text(encoding="utf-8"))

    def test_15_qgis_verifier_checks_for_broken_layers(self) -> None:
        source = (PACKAGE_ROOT / "terrain_pack.py").read_text(encoding="utf-8")
        self.assertIn("broken terrain project layers", source)
        self.assertIn('"broken_layer_count": 0', source)

    def test_16_official_boundary_identity_is_exact(self) -> None:
        feature = _boundary_feature(_official_feature())
        self.assertEqual(feature["properties"]["OBJECTID"], 16701)
        self.assertEqual(BOUNDARY_SOURCE_CRS, "EPSG:7844")
        self.assertTrue(BOUNDARY_LICENCE)

    def test_17_boundary_identity_mismatch_is_rejected(self) -> None:
        payload = _official_feature()
        payload["features"][0]["properties"]["OBJECTID"] = 1
        with self.assertRaisesRegex(TerrainPackError, "identity mismatch"):
            _boundary_feature(payload)

    def test_18_required_terrain_layers_are_closed(self) -> None:
        self.assertEqual(len(TERRAIN_LAYER_NAMES), 4)
        self.assertIn("Hillshade", TERRAIN_LAYER_NAMES[2])
        self.assertIn("Slope Degrees", TERRAIN_LAYER_NAMES[3])

    def test_19_hydrology_remains_unavailable(self) -> None:
        source = (PACKAGE_ROOT / "terrain_pack.py").read_text(encoding="utf-8")
        self.assertIn("NOT_AUTHORIZED_NOT_RETRIEVED", source)
        self.assertIn("INFO — Hydrology data not yet retrieved", (TASK_ROOT / "QGIS_COOMA_TERRAIN_REVIEW_GUIDE.md").read_text(encoding="utf-8"))

    def test_20_prototype_is_untouched_by_terrain_code(self) -> None:
        source = "\n".join(path.read_text(encoding="utf-8") for path in PACKAGE_ROOT.glob("terrain_*.py"))
        self.assertNotIn("prototype/", source)

    def test_21_no_combined_unattended_retrieval_action(self) -> None:
        source = (PACKAGE_ROOT / "terrain_pack.py").read_text(encoding="utf-8")
        self.assertNotIn('"all"', source)
        self.assertIn('"retrieve-boundary"', source)
        self.assertIn('"retrieve-dem"', source)

    def test_22_project_filename_and_buffer_are_exact(self) -> None:
        self.assertEqual(TERRAIN_PROJECT_FILENAME, "Cooma_Spatial_Foundation_v0_2_terrain.qgz")
        self.assertEqual(BUFFER_METRES, 10_000.0)

    def test_23_guide_contains_dem_limitation_sentence(self) -> None:
        guide = (TASK_ROOT / "QGIS_COOMA_TERRAIN_REVIEW_GUIDE.md").read_text(encoding="utf-8")
        self.assertIn("This DEM supports regional terrain observation.", guide)
        self.assertIn("It does not provide building-scale detail and is not equivalent to aerial imagery.", guide)

    def test_24_required_gate_document_exists(self) -> None:
        gate = TASK_ROOT / "TASK2040_FOUNDER_QGIS_TERRAIN_GATE.md"
        self.assertTrue(gate.is_file())
        self.assertIn("DO_NOT_AUTO_MERGE", gate.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
