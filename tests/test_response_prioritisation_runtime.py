"""Tests for the CCZPS-Lite Response Prioritisation Runtime."""

from __future__ import annotations

import csv
import unittest
from pathlib import Path

from cczps_lite.engine.response_prioritisation import (
    classify_urgency_level,
    derive_response_prioritisation,
    estimate_expected_benefit,
    rank_response_options,
)
from cczps_lite.engine.scenario_compare import main as run_scenario_compare

REPO_ROOT = Path(__file__).resolve().parents[1]


class ResponsePrioritisationRuntimeTests(unittest.TestCase):
    def test_insufficient_evidence_creates_high_implementation_priority(self) -> None:
        result = derive_response_prioritisation(
            {"response_priority": "High", "response_options": ["Field evidence collection plan"]},
            {"validation_status": "Insufficient Evidence"},
            {"forcing_priority": "Low", "primary_forcing": "Mixed / Unclear Forcing"},
        )
        self.assertEqual(result["implementation_priority"], "High")

    def test_urgency_classification(self) -> None:
        cases = (
            ("High", "Fire Exposure", "Critical"),
            ("High", "Water Storage Deficit", "Critical"),
            ("Medium", "Vegetation Stress", "Moderate"),
            ("Low", "Governance Consultation", "Routine"),
        )
        for priority, forcing, urgency in cases:
            with self.subTest(forcing=forcing):
                self.assertEqual(classify_urgency_level(priority, forcing), urgency)

    def test_expected_benefit_classification(self) -> None:
        cases = (
            ("Water storage audit", "Water Storage Deficit", "Hydrological resilience improvement"),
            ("Bushfire buffer review", "Fire Exposure", "Risk reduction and asset protection"),
            ("Field evidence collection plan", "", "Confidence improvement"),
        )
        for option, forcing, benefit in cases:
            with self.subTest(option=option):
                self.assertEqual(estimate_expected_benefit(option, forcing), benefit)

    def test_ranking_selects_highest_priority_response(self) -> None:
        response = rank_response_options(
            ["Governance consultation", "Soil moisture monitoring", "Water storage audit"],
            "Critical",
        )
        self.assertEqual(response, "Water storage audit")

    def test_scenario_compare_output_includes_prioritisation_fields(self) -> None:
        run_scenario_compare()
        output_dir = REPO_ROOT / "cczps_lite" / "output"
        with (output_dir / "comparison_matrix.csv").open("r", encoding="utf-8", newline="") as file_obj:
            rows = list(csv.DictReader(file_obj))
        self.assertEqual(len(rows), 8)
        for field in (
            "implementation_priority", "urgency_level", "expected_benefit",
            "prioritised_response", "prioritisation_summary",
        ):
            self.assertIn(field, rows[0])
        self.assertNotIn(";", rows[0]["prioritised_response"])
        self.assertIn("### Response Prioritisation Runtime", (output_dir / "scenario_report.md").read_text(encoding="utf-8"))
        self.assertIn("## Response Prioritisation Reading", (output_dir / "governance_summary.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
