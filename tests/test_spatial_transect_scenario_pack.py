"""Tests for the Task 28 transect scenario pack."""
from __future__ import annotations
import tempfile
import unittest
from pathlib import Path
from cczps_lite.engine.spatial_transect_runtime import REFERENCE_ROLES, build_scenario_pack_output, build_spatial_transect_output, load_transect_configuration, render_scenario_pack_report, write_spatial_transect_outputs


class SpatialTransectScenarioPackTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = load_transect_configuration()
        self.output = build_spatial_transect_output(self.config)
        self.pack = build_scenario_pack_output(self.output)

    def test_scenario_pack_covers_all_required_contexts(self) -> None:
        scenario_ids = {scenario["scenario_id"] for scenario in self.pack["scenarios"]}
        self.assertEqual({"batlow", "kunlun", "iraq", "baiyangdian_xiongan"}, scenario_ids)
        self.assertEqual(self.pack["scenario_count"], 4)

    def test_reference_roles_are_allowed_and_declared(self) -> None:
        allowed_roles = set(REFERENCE_ROLES)
        for scenario in self.pack["scenarios"]:
            for point in scenario["reference_points"]:
                self.assertIn(point["role"], allowed_roles)
                self.assertIn(point["role"], scenario["configured_reference_roles"])
                self.assertIn(point["status"], {"configured_not_validated", "missing_coordinates"})

    def test_dashboard_compatible_output_is_local_and_transparent(self) -> None:
        self.assertTrue(self.pack["dashboard_compatible"])
        self.assertIn("No automatic point selection", self.pack["safety_boundary"])
        for scenario in self.pack["scenarios"]:
            self.assertEqual(scenario["dashboard_section"], "spatial_transect_scenario_pack")
            self.assertEqual(scenario["field_validation_claim"], "not_claimed")
            self.assertIn("not field validated", scenario["scenario_report"])

    def test_missing_data_handling_remains_explicit(self) -> None:
        kunlun = next(scenario for scenario in self.pack["scenarios"] if scenario["scenario_id"] == "kunlun")
        self.assertIn("kunlun_upwind_reference", kunlun["missing_data_points"])
        missing_point = next(point for point in kunlun["reference_points"] if point["point_id"] == "kunlun_upwind_reference")
        self.assertIsNone(missing_point["coordinates"])
        self.assertEqual(missing_point["missing_data_status"], "missing_coordinates")

    def test_scenario_report_mentions_all_contexts_without_conclusions(self) -> None:
        report = render_scenario_pack_report(self.pack)
        for label in ("Batlow", "Kunlun", "Iraq", "Baiyangdian-Xiong'an"):
            self.assertIn(label, report)
        self.assertIn("No field validation", report)
        self.assertNotIn("recommendation", report.lower())

    def test_write_outputs_creates_scenario_pack_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            json_path = Path(directory) / "spatial_transects.json"
            md_path = Path(directory) / "spatial_transects.md"
            write_spatial_transect_outputs(self.output, json_path, md_path)
            pack_json = json_path.parent / "spatial_transect_scenario_pack.json"
            pack_md = json_path.parent / "spatial_transect_scenario_pack.md"
            self.assertIn("spatial_transect_scenario_pack", pack_json.read_text(encoding="utf-8"))
            self.assertIn("Transect Scenario Pack", pack_md.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
