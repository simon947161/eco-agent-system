"""Tests for the CCZPS-Lite Adaptive Response Runtime."""

from __future__ import annotations

import csv
import unittest
from pathlib import Path

from cczps_lite.engine.adaptive_response import (
    derive_adaptive_response,
    derive_response_options,
)
from cczps_lite.engine.scenario_compare import main as run_scenario_compare

REPO_ROOT = Path(__file__).resolve().parents[1]


def response_for(status: str, gaps=None, owner="Governance reviewer", forcing="") -> dict:
    return derive_adaptive_response(
        {"validation_status": status, "validation_gaps": gaps or []},
        {"review_priority": "Medium", "review_owner": owner},
        {"forcing_priority": "Medium", "primary_forcing": forcing},
        {},
    )


class AdaptiveResponseRuntimeTests(unittest.TestCase):
    """Verify response modes, priorities, options, and generated outputs."""

    def test_insufficient_evidence_uses_evidence_building_mode(self) -> None:
        result = response_for("Insufficient Evidence", owner="Evidence coordinator")
        self.assertEqual(result["response_mode"], "Evidence-building response")
        self.assertEqual(result["response_priority"], "High")

    def test_technical_validation_uses_technical_mode(self) -> None:
        self.assertEqual(
            response_for("Requires Technical Validation")["response_mode"],
            "Technical validation response",
        )

    def test_local_validation_uses_consultation_mode(self) -> None:
        self.assertEqual(
            response_for("Requires Local Validation")["response_mode"],
            "Local consultation response",
        )

    def test_concept_ready_uses_refinement_mode(self) -> None:
        result = derive_adaptive_response(
            {"validation_status": "Validated Enough for Concept Review", "validation_gaps": []},
            {"review_priority": "Low", "review_owner": "Governance reviewer"},
            {"forcing_priority": "Low", "primary_forcing": ""},
            {},
        )
        self.assertEqual(result["response_mode"], "Concept refinement response")
        self.assertEqual(result["response_priority"], "Low")

    def test_water_storage_deficit_adds_water_options(self) -> None:
        options = derive_response_options([], "", "Water Storage Deficit")
        self.assertIn("Water storage audit", options)
        self.assertIn("Soil moisture monitoring", options)

    def test_heat_and_evaporation_add_microclimate_options(self) -> None:
        options = derive_response_options([], "", "Evaporation Pressure")
        self.assertIn("Microclimate shade strategy", options)
        self.assertIn("Evaporation reduction planting", options)

    def test_fire_exposure_adds_bushfire_options(self) -> None:
        options = derive_response_options([], "", "Fire Exposure")
        self.assertIn("Bushfire buffer review", options)
        self.assertIn("Vegetation fuel management review", options)

    def test_vegetation_stress_adds_ecological_options(self) -> None:
        options = derive_response_options([], "", "Vegetation Stress")
        self.assertIn("Canopy-cover assessment", options)
        self.assertIn("Ecological buffer restoration", options)

    def test_no_major_gap_adds_refinement_options(self) -> None:
        options = derive_response_options(
            ["No major validation gap identified at concept level"],
            "Governance reviewer",
            "",
        )
        self.assertIn("Concept design refinement", options)
        self.assertIn("Governance consultation", options)

    def test_scenario_compare_output_includes_response_fields(self) -> None:
        run_scenario_compare()
        output_dir = REPO_ROOT / "cczps_lite" / "output"
        with (output_dir / "comparison_matrix.csv").open(
            "r", encoding="utf-8", newline=""
        ) as file_obj:
            rows = list(csv.DictReader(file_obj))

        self.assertEqual(len(rows), 3)
        for field in (
            "response_priority",
            "response_options",
            "response_mode",
            "response_summary",
        ):
            self.assertIn(field, rows[0])
        self.assertNotIn("[", rows[0]["response_options"])

        scenario_report = (output_dir / "scenario_report.md").read_text(encoding="utf-8")
        governance_summary = (output_dir / "governance_summary.md").read_text(encoding="utf-8")
        self.assertIn("### Adaptive Response Runtime", scenario_report)
        self.assertIn("## Adaptive Response Reading", governance_summary)


if __name__ == "__main__":
    unittest.main()
