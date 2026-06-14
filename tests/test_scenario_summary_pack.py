"""Tests for the local-only Scenario Summary Pack Builder."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from cczps_lite.engine import scenario_summary_pack as summary_pack


class ScenarioSummaryPackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.pack = summary_pack.build_scenario_summary_pack()

    def test_expected_scenarios_and_intakes_are_included(self) -> None:
        self.assertEqual(self.pack["scenario_count"], 6)
        self.assertEqual(
            {record["scenario_id"] for record in self.pack["scenarios"]},
            {
                "batlow",
                "kunlun",
                "iraq",
                "baiyangdian_xiongan",
                "tumut_nsw_intake",
                "dunhuang_demonstration_area_intake",
            },
        )

    def test_required_summary_fields_are_present(self) -> None:
        required = {
            "scenario_id",
            "scenario_name",
            "location_name",
            "scenario_status",
            "workflow_status",
            "evidence_status",
            "meteorology_status",
            "planning_hypothesis_status",
            "evidence_traceability_status",
            "internal_governance_status",
            "expert_review_status",
            "professional_review_status",
            "approval_support_status",
            "plain_language_summary",
            "what_the_system_currently_knows",
            "what_the_system_cannot_conclude_yet",
            "next_human_review_actions",
            "limitations",
        }
        for record in self.pack["scenarios"]:
            self.assertTrue(required.issubset(record))

    def test_conservative_statuses_and_review_boundaries_are_preserved(self) -> None:
        for record in self.pack["scenarios"]:
            self.assertEqual(record["approval_support_status"], "not_ready_for_approval")
            self.assertTrue(record["human_review_required"])
            self.assertTrue(record["professional_review_required"])
        intakes = [
            record
            for record in self.pack["scenarios"]
            if record["scenario_id"].endswith("_intake")
        ]
        self.assertTrue(all(record["scenario_status"] == "intake_only" for record in intakes))
        self.assertTrue(
            all(record["planning_hypothesis_status"] == "not_generated" for record in intakes)
        )

    def test_no_ranking_or_final_recommendation_fields_exist(self) -> None:
        serialized = json.dumps(self.pack).lower()
        for forbidden_field in (
            '"rank"',
            '"ranking"',
            '"winner"',
            '"best_scenario"',
            '"final_recommendation"',
        ):
            self.assertNotIn(forbidden_field, serialized)
        for forbidden_status in (
            '"approved"',
            '"ready_for_approval"',
            '"implementation_ready"',
            '"construction_ready"',
            '"investment_ready"',
        ):
            self.assertNotIn(forbidden_status, serialized)

    def test_missing_optional_files_are_handled_conservatively(self) -> None:
        sources = {key: None for key in summary_pack.SOURCE_PATHS}
        sources["intake"] = {
            "scenario_profiles": [
                {
                    "scenario_id": "example_intake",
                    "location_name": "Example",
                    "scenario_status": "intake_only",
                }
            ]
        }
        pack = summary_pack.build_scenario_summary_pack(sources)
        record = pack["scenarios"][0]
        self.assertEqual(pack["scenario_count"], 1)
        self.assertEqual(record["meteorology_status"], "not_available")
        self.assertEqual(record["evidence_status"], "not_generated")
        self.assertEqual(record["internal_governance_status"], "requires_further_review")
        self.assertEqual(record["approval_support_status"], "not_ready_for_approval")

    def test_empty_optional_directory_does_not_crash(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            sources = summary_pack.load_sources(Path(directory))
        self.assertTrue(all(value is None for value in sources.values()))
        self.assertEqual(summary_pack.build_scenario_summary_pack(sources)["scenarios"], [])

    def test_json_markdown_and_consolidated_directory_are_generated(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output_path = Path(directory) / "consolidated" / "scenario_summary_pack.json"
            report_path = Path(directory) / "consolidated" / "scenario_summary_pack.md"
            summary_pack.write_scenario_summary_outputs(
                self.pack, output_path, report_path
            )
            self.assertTrue(output_path.is_file())
            self.assertTrue(report_path.is_file())
            self.assertEqual(json.loads(output_path.read_text()), self.pack)
            report = report_path.read_text(encoding="utf-8")
        self.assertIn("# CCZPS-Lite Scenario Summary Pack", report)
        self.assertIn("## Scenario: Tumut NSW", report)
        self.assertIn("### What the system currently knows", report)
        self.assertIn("### What the system cannot conclude yet", report)
        self.assertIn("### Next human review actions", report)

    def test_minimal_core_mapping_is_explicit(self) -> None:
        self.assertEqual(
            set(self.pack["minimal_core_mapping"]),
            {"Scenario", "Evidence", "Hypothesis", "Review", "Report"},
        )

    def test_builder_has_no_api_llm_gis_or_simulation_dependency(self) -> None:
        source = Path(summary_pack.__file__).read_text(encoding="utf-8")
        for forbidden in (
            "requests",
            "urllib",
            "http://",
            "https://",
            "OpenAI",
            "anthropic",
            "socket",
            "gdal",
            "rasterio",
        ):
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()
