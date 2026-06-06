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
    """Verify implementation priority, urgency, benefits, and ranking."""

    def test_insufficient_evidence_creates_high_implementation_priority(self) -> None:
        result = derive_response_prioritisation(
            {
                "response_priority": "High",
                "response_options": ["Field evidence collection plan"],
            },
            {"validation_status": "Insufficient Evidence"},
            {"forcing_priority": "Low", "primary_forcing": "Mixed / Unclear Forcing"},
        )
        self.assertEqual(result["implementation_priority"], "High")

    def test_fire_exposure_is_critical(self) -> None:
        self.assertEqual(classify_urgency_level("High", "Fire Exposure"), "Critical")

    def test_water_storage_deficit_is_critical(self) -> None:
        self.assertEqual(
            classify_urgency_level("High", "Water Storage Deficit"),
            "Critical",
        )

    def test_vegetation_stress_is_moderate(self) -> None:
        self.assertEqual(
            classify_urgency_level("Medium", "Vegetation Stress"),
            "Moderate",
        )

    def test_governance_consultation_is_routine(self) -> None:
        self.assertEqual(
            classify_urgency_level("Low", "Governance Consultation"),
            "Routine",
        )

    def test_water_response_estimates_hydrological_benefit(self) -> None:
        self.assertEqual(
            estimate_expected_benefit("Water storage audit", "Water Storage Deficit"),
            "Hydrological resilience improvement",
        )

    def test_fire_response_estimates_risk_reduction_benefit(self) -> None:
        self.assertEqual(
            estimate_expected_benefit("Bushfire buffer review", "Fire Exposure"),
            "Risk reduction and asset protection",
        )

    def test_evidence_collection_estimates_confidence_benefit(self) -> None:
        self.assertEqual(
            estimate_expected_benefit("Field evidence collection plan", ""),
            "Confidence improvement",
        )

    def test_ranking_selects_highest_priority_response(self) -> None:
        response = rank_response_options(
            [
                "Governance consultation",
                "Soil moisture monitoring",
                "Water storage audit",
            ],
            "Critical",
        )
        self.assertEqual(response, "Water storage audit")

    def test_scenario_compare_output_includes_prioritisation_fields(self) -> None:
        run_scenario_compare()
        output_dir = REPO_ROOT / "cczps_lite" / "output"
        with (output_dir / "comparison_matrix.csv").open(
            "r", encoding="utf-8", newline=""
        ) as file_obj:
            rows = list(csv.DictReader(file_obj))

        self.assertEqual(len(rows), 3)
        for field in (
            "implementation_priority",
            "urgency_level",
            "expected_benefit",
            "prioritised_response",
            "prioritisation_summary",
        ):
            self.assertIn(field, rows[0])
        self.assertNotIn(";", rows[0]["prioritised_response"])

        scenario_report = (output_dir / "scenario_report.md").read_text(encoding="utf-8")
        governance_summary = (output_dir / "governance_summary.md").read_text(encoding="utf-8")
        self.assertIn("### Response Prioritisation Runtime", scenario_report)
        self.assertIn("## Response Prioritisation Reading", governance_summary)


if __name__ == "__main__":
    unittest.main()
