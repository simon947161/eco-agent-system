"""Tests for the local-only Scenario Comparison Runtime."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from cczps_lite.engine import scenario_comparison as comparison


class ScenarioComparisonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.output = comparison.build_scenario_comparison()

    def test_schema_and_expected_scenarios(self) -> None:
        self.assertEqual(self.output["record_count"], 4)
        self.assertEqual(
            {record["scenario_id"] for record in self.output["records"]},
            set(comparison.SCENARIOS),
        )
        for record in self.output["records"]:
            self.assertIn(record["comparison_status"], comparison.COMPARISON_STATUSES)
            self.assertIn(record["uncertainty_level"], {"low", "medium", "high", "unknown"})

    def test_traceability_and_governance_sources_are_used(self) -> None:
        for record in self.output["records"]:
            self.assertEqual(record["traceability_status"], "available")
            self.assertEqual(record["trace_record_count"], 8)
            self.assertTrue(record["traceability_references"])
            self.assertEqual(record["internal_governance_status"], "requires_further_review")
        batlow = next(record for record in self.output["records"] if record["scenario_id"] == "batlow")
        self.assertEqual(batlow["energy_signal"], "context_relevant_requires_review")

    def test_current_review_and_approval_boundaries(self) -> None:
        for record in self.output["records"]:
            self.assertEqual(record["professional_validation_status"], "awaiting_professional_review")
            self.assertEqual(record["expert_review_status"], "not_reviewed")
            self.assertEqual(record["approval_support_status"], "not_ready_for_approval")
            self.assertTrue(record["human_review_required"])
            self.assertTrue(record["professional_review_required"])

    def test_missing_evidence_is_conservative(self) -> None:
        sources = {key: comparison._load(path) for key, path in comparison.SOURCE_PATHS.items()}
        sources["traceability"] = {"records": []}
        output = comparison.build_scenario_comparison(sources)
        for record in output["records"]:
            self.assertEqual(record["comparison_status"], "insufficient_evidence_for_comparison")
            self.assertEqual(record["evidence_strength"], "insufficient")
            self.assertEqual(record["traceability_status"], "unavailable")

    def test_missing_review_requires_professional_review(self) -> None:
        sources = {key: comparison._load(path) for key, path in comparison.SOURCE_PATHS.items()}
        sources = json.loads(json.dumps(sources))
        sources["transects"]["spatial_transects"][0]["validation"]["status"] = "valid_configured"
        sources["validation"]["reviews"].pop("batlow")
        output = comparison.build_scenario_comparison(sources)
        batlow = next(record for record in output["records"] if record["scenario_id"] == "batlow")
        self.assertEqual(batlow["comparison_status"], "requires_professional_review")
        self.assertEqual(batlow["professional_validation_status"], "awaiting_professional_review")

    def test_no_ranking_or_final_recommendation_fields(self) -> None:
        serialized = json.dumps(self.output).lower()
        for forbidden_field in ('"rank"', '"ranking"', '"winner"', '"best_scenario"', '"final_recommendation"'):
            self.assertNotIn(forbidden_field, serialized)
        self.assertNotIn("investment_ready", serialized)
        self.assertNotIn("construction_ready", serialized)

    def test_json_and_markdown_generation(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            json_path = Path(temp_dir) / "comparison.json"
            markdown_path = Path(temp_dir) / "comparison.md"
            comparison.write_scenario_comparison_outputs(self.output, json_path, markdown_path)
            self.assertEqual(json.loads(json_path.read_text()), self.output)
            report = markdown_path.read_text(encoding="utf-8")
            self.assertIn("# Scenario Comparison Runtime", report)
            self.assertIn("## Cross-Scenario Summary", report)
            self.assertIn("not_ready_for_approval", report)

    def test_runtime_has_no_network_llm_gis_or_simulation_clients(self) -> None:
        source = Path(comparison.__file__).read_text(encoding="utf-8")
        for forbidden in ("requests", "urllib", "http://", "https://", "OpenAI", "anthropic", "socket", "gdal", "rasterio", "simulation"):
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()
