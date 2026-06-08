"""Tests for the Spatial Context & Transect Runtime."""
from __future__ import annotations
import tempfile
import unittest
from pathlib import Path
from cczps_lite.engine.spatial_transect_runtime import REFERENCE_ROLES, build_spatial_transect_output, load_transect_configuration, validate_transect, write_spatial_transect_outputs


class SpatialTransectRuntimeTests(unittest.TestCase):
    def test_default_configuration_loads_required_scenarios(self) -> None:
        output = build_spatial_transect_output()
        scenario_ids = {transect["scenario_id"] for transect in output["spatial_transects"]}
        self.assertIn("batlow", scenario_ids)
        self.assertIn("kunlun", scenario_ids)
        self.assertIn("iraq", scenario_ids)
        self.assertIn("baiyangdian_xiongan", scenario_ids)
        self.assertEqual(set(REFERENCE_ROLES), set(output["supported_point_roles"]) - {"core"})

    def test_role_validation_is_deterministic(self) -> None:
        transect = {"transect_id": "invalid_role", "scenario_id": "example", "core_location": {"point_id": "core", "role": "core", "coordinates": {"latitude": 1, "longitude": 2}}, "reference_points": [{"point_id": "bad_role", "role": "river_magic", "coordinates": {"latitude": 1.1, "longitude": 2.1}}]}
        reading = validate_transect(transect)
        self.assertEqual(reading["validation"]["status"], "configured_with_validation_issues")
        self.assertIn("reference:bad_role:invalid_role:river_magic", reading["validation"]["errors"])

    def test_missing_coordinates_are_preserved_without_inference(self) -> None:
        transect = {"transect_id": "missing_coordinates", "scenario_id": "example", "core_location": {"point_id": "core", "role": "core", "coordinates": {"latitude": 1, "longitude": 2}}, "reference_points": [{"point_id": "upwind_reference", "role": "upwind", "coordinates": None, "direction_label": "configured externally"}]}
        reading = validate_transect(transect)
        reference = reading["reference_points"][0]
        self.assertIsNone(reference["coordinates"])
        self.assertEqual(reference["missing_data_status"], "missing_coordinates")
        self.assertEqual(reading["relationship_summary"]["relationship_inference"], "not_performed")
        self.assertIn("upwind_reference", reading["relationship_summary"]["missing_data_points"])

    def test_duplicate_point_ids_are_reported(self) -> None:
        transect = {"transect_id": "duplicate_points", "scenario_id": "example", "core_location": {"point_id": "same", "role": "core", "coordinates": {"latitude": 1, "longitude": 2}}, "reference_points": [{"point_id": "same", "role": "lateral", "coordinates": {"latitude": 1.2, "longitude": 2.2}}]}
        reading = validate_transect(transect)
        self.assertIn("reference:same:duplicate_point_id:same", reading["validation"]["errors"])

    def test_direction_labels_are_preserved_not_generated(self) -> None:
        output = build_spatial_transect_output({"transects": [{"transect_id": "direction_labels", "scenario_id": "example", "core_location": {"point_id": "core", "role": "core", "coordinates": {"latitude": 1, "longitude": 2}}, "reference_points": [{"point_id": "with_label", "role": "downwind", "coordinates": {"latitude": 1.1, "longitude": 2.1}, "direction_label": "southeast"}, {"point_id": "without_label", "role": "upstream", "coordinates": {"latitude": 1.2, "longitude": 2.2}}]}]})
        references = output["spatial_transects"][0]["reference_points"]
        self.assertEqual(references[0]["direction_label"], "southeast")
        self.assertIsNone(references[1]["direction_label"])

    def test_output_files_include_json_and_markdown(self) -> None:
        output = build_spatial_transect_output(load_transect_configuration())
        with tempfile.TemporaryDirectory() as directory:
            json_path = Path(directory) / "spatial_transects.json"
            md_path = Path(directory) / "spatial_transects.md"
            write_spatial_transect_outputs(output, json_path, md_path)
            self.assertIn("Spatial Context & Transect Runtime", md_path.read_text(encoding="utf-8"))
            self.assertIn("baiyangdian_xiongan", json_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
