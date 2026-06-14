"""Tests for the local-only Evidence Review Pack Builder."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from cczps_lite.engine import evidence_review_pack


class EvidenceReviewPackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.pack = evidence_review_pack.build_evidence_review_pack()

    def test_expected_scenarios_and_intakes_are_included(self) -> None:
        self.assertEqual(self.pack["record_count"], 6)
        self.assertEqual(
            {record["scenario_id"] for record in self.pack["review_records"]},
            {
                "batlow",
                "kunlun",
                "iraq",
                "baiyangdian_xiongan",
                "tumut_nsw_intake",
                "dunhuang_demonstration_area_intake",
            },
        )

    def test_established_evidence_coverage_is_preserved(self) -> None:
        batlow = next(
            record for record in self.pack["review_records"]
            if record["scenario_id"] == "batlow"
        )
        self.assertEqual(batlow["meteorology_evidence_status"], "available")
        self.assertEqual(batlow["meteorology_time_series_status"], "available")
        self.assertEqual(batlow["meteorology_trend_status"], "available")
        self.assertEqual(batlow["spatial_transect_status"], "available")
        self.assertTrue(batlow["traceability_references"])

    def test_intake_evidence_is_not_overstated(self) -> None:
        tumut = next(
            record for record in self.pack["review_records"]
            if record["scenario_id"] == "tumut_nsw_intake"
        )
        self.assertEqual(tumut["meteorology_evidence_status"], "available")
        self.assertEqual(tumut["meteorology_time_series_status"], "not_available")
        self.assertEqual(tumut["meteorology_trend_status"], "not_available")
        self.assertEqual(tumut["evidence_strength"], "insufficient")
        self.assertEqual(tumut["uncertainty_level"], "high")

    def test_gis_dem_plan_is_not_treated_as_evidence(self) -> None:
        for record in self.pack["review_records"]:
            self.assertEqual(record["gis_dem_evidence_status"], "planning_only")
            self.assertIn(
                "professional GIS / DEM evidence and verification",
                record["missing_evidence"],
            )

    def test_professional_validation_status_is_preserved(self) -> None:
        established = [
            record for record in self.pack["review_records"]
            if not record["scenario_id"].endswith("_intake")
        ]
        self.assertTrue(
            all(
                record["professional_validation_status"]
                == "awaiting_professional_review"
                for record in established
            )
        )

    def test_review_and_approval_boundaries_remain_conservative(self) -> None:
        for record in self.pack["review_records"]:
            self.assertEqual(record["evidence_review_status"], "requires_further_review")
            self.assertEqual(record["approval_support_status"], "not_ready_for_approval")
            self.assertTrue(record["human_review_required"])
            self.assertTrue(record["professional_review_required"])

    def test_missing_optional_files_are_handled(self) -> None:
        sources = {key: None for key in evidence_review_pack.SOURCE_PATHS}
        sources["scenario_summary"] = {
            "scenarios": [{
                "scenario_id": "example_intake",
                "scenario_name": "Example",
                "scenario_status": "intake_only",
            }]
        }
        pack = evidence_review_pack.build_evidence_review_pack(sources)
        record = pack["review_records"][0]
        self.assertEqual(record["meteorology_evidence_status"], "not_available")
        self.assertEqual(record["gis_dem_evidence_status"], "not_available")
        self.assertEqual(record["professional_validation_status"], "not_available")
        self.assertEqual(record["evidence_strength"], "insufficient")
        self.assertEqual(record["uncertainty_level"], "high")

    def test_empty_source_directory_does_not_crash(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            sources = evidence_review_pack.load_sources(Path(directory))
        self.assertTrue(all(value is None for value in sources.values()))
        pack = evidence_review_pack.build_evidence_review_pack(sources)
        self.assertEqual(pack["review_records"], [])

    def test_json_markdown_and_directory_reuse(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            consolidated = Path(directory) / "consolidated"
            consolidated.mkdir()
            json_path = consolidated / "evidence_review_pack.json"
            md_path = consolidated / "evidence_review_pack.md"
            evidence_review_pack.write_evidence_review_outputs(
                self.pack, json_path, md_path
            )
            evidence_review_pack.write_evidence_review_outputs(
                self.pack, json_path, md_path
            )
            self.assertEqual(json.loads(json_path.read_text()), self.pack)
            report = md_path.read_text(encoding="utf-8")
        self.assertIn("# CCZPS-Lite Evidence Review Pack", report)
        self.assertIn("## Scenario: Batlow", report)
        self.assertIn("### Evidence coverage", report)
        self.assertIn("### GIS / DEM status", report)
        self.assertIn("### Professional review requirements", report)

    def test_no_authoritative_or_ranking_fields_exist(self) -> None:
        serialized = json.dumps(self.pack).lower()
        for forbidden_field in (
            '"validated"',
            '"approved"',
            '"ready_for_approval"',
            '"scientifically_confirmed"',
            '"engineering_ready"',
            '"regulatory_ready"',
            '"implementation_ready"',
            '"construction_ready"',
            '"investment_ready"',
            '"best_scenario"',
            '"winner"',
            '"final_recommendation"',
        ):
            self.assertNotIn(forbidden_field, serialized)

    def test_minimal_core_mapping_is_explicit(self) -> None:
        self.assertEqual(
            set(self.pack["minimal_core_mapping"]),
            {"Scenario", "Evidence", "Hypothesis", "Review", "Report"},
        )

    def test_builder_has_no_api_llm_gis_or_simulation_dependency(self) -> None:
        source = Path(evidence_review_pack.__file__).read_text(encoding="utf-8")
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
