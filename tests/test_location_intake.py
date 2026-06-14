"""Tests for the local-only Location-to-Scenario Intake Runtime."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from cczps_lite.engine.location_intake import (
    build_location_intake_output,
    load_location_intakes,
    scenario_id_for,
    validate_location_record,
    write_location_intake_outputs,
)

VALID_RECORD = {
    "location_name": "Tumut NSW",
    "country": "Australia",
    "region": "New South Wales",
    "latitude": -35.3,
    "longitude": 148.22,
    "intake_context": "climate_resilience_review",
    "user_intent": "Explore a future scenario.",
}


class LocationIntakeTests(unittest.TestCase):
    def test_example_input_parses_and_generates_profiles(self) -> None:
        records = load_location_intakes()
        output = build_location_intake_output(records)
        self.assertEqual(output["profile_count"], 2)
        self.assertEqual(output["invalid_record_count"], 1)

    def test_invalid_latitude_is_reported_not_promoted(self) -> None:
        invalid = {**VALID_RECORD, "latitude": 91}
        output = build_location_intake_output([invalid])
        self.assertEqual(output["scenario_profiles"], [])
        self.assertIn(
            "latitude_must_be_between_-90_and_90",
            output["invalid_records"][0]["validation_errors"],
        )

    def test_invalid_longitude_is_reported(self) -> None:
        errors = validate_location_record({**VALID_RECORD, "longitude": -181})
        self.assertIn("longitude_must_be_between_-180_and_180", errors)

    def test_missing_location_name_is_reported(self) -> None:
        errors = validate_location_record({**VALID_RECORD, "location_name": " "})
        self.assertIn("location_name_is_required", errors)

    def test_missing_intake_context_is_reported(self) -> None:
        record = dict(VALID_RECORD)
        record.pop("intake_context")
        self.assertIn("intake_context_is_required", validate_location_record(record))

    def test_scenario_id_generation_is_deterministic(self) -> None:
        self.assertEqual(scenario_id_for("Tumut NSW"), "tumut_nsw_intake")
        self.assertEqual(
            scenario_id_for("Dunhuang Demonstration Area"),
            "dunhuang_demonstration_area_intake",
        )
        self.assertEqual(scenario_id_for("Tumut NSW"), scenario_id_for("Tumut NSW"))

    def test_valid_profile_preserves_safety_defaults(self) -> None:
        profile = build_location_intake_output([VALID_RECORD])["scenario_profiles"][0]
        self.assertEqual(profile["scenario_status"], "intake_only")
        self.assertEqual(profile["workflow_status"], "awaiting_evidence_generation")
        self.assertEqual(profile["evidence_status"], "not_generated")
        self.assertEqual(profile["meteorology_status"], "not_requested")
        self.assertEqual(profile["gis_dem_status"], "not_requested")
        self.assertEqual(profile["planning_hypothesis_status"], "not_generated")
        self.assertEqual(profile["approval_support_status"], "not_ready_for_approval")
        self.assertTrue(profile["human_review_required"])
        self.assertTrue(profile["professional_review_required"])

    def test_json_and_markdown_outputs_are_generated(self) -> None:
        output = build_location_intake_output([VALID_RECORD])
        with tempfile.TemporaryDirectory() as directory:
            json_path = Path(directory) / "profiles.json"
            md_path = Path(directory) / "profiles.md"
            write_location_intake_outputs(output, json_path, md_path)
            stored = json.loads(json_path.read_text(encoding="utf-8"))
            report = md_path.read_text(encoding="utf-8")
        self.assertEqual(stored["scenario_profiles"][0]["scenario_id"], "tumut_nsw_intake")
        self.assertIn("# Location-to-Scenario Intake Runtime", report)
        self.assertIn("not_ready_for_approval", report)

    def test_input_must_be_a_json_array(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.json"
            path.write_text('{"location_name": "Not an array"}', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "JSON array"):
                load_location_intakes(path)

    def test_runtime_contains_no_external_or_llm_clients(self) -> None:
        script = (
            Path(__file__).resolve().parents[1]
            / "cczps_lite"
            / "engine"
            / "location_intake.py"
        ).read_text(encoding="utf-8")
        for forbidden in (
            "requests.",
            "urlopen(",
            "http://",
            "https://",
            "OpenAI(",
            "anthropic.",
            "power.larc.nasa.gov",
        ):
            self.assertNotIn(forbidden, script)


if __name__ == "__main__":
    unittest.main()
