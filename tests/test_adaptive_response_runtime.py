"""Tests for the CCZPS-Lite Adaptive Response Runtime."""

from __future__ import annotations

import csv
import unittest
from pathlib import Path

from cczps_lite.engine.adaptive_response import derive_adaptive_response, derive_response_options
from cczps_lite.engine.scenario_compare import main as run_scenario_compare

REPO_ROOT = Path(__file__).resolve().parents[1]


def response_for(status: str, owner="Governance reviewer") -> dict:
    return derive_adaptive_response(
        {"validation_status": status, "validation_gaps": []},
        {"review_priority": "Medium", "review_owner": owner},
        {"forcing_priority": "Medium", "primary_forcing": ""}, {},
    )


class AdaptiveResponseRuntimeTests(unittest.TestCase):
    def test_validation_status_maps_to_response_mode(self) -> None:
        cases = (
            ("Insufficient Evidence", "Evidence coordinator", "Evidence-building response"),
            ("Requires Technical Validation", "Governance reviewer", "Technical validation response"),
            ("Requires Local Validation", "Governance reviewer", "Local consultation response"),
            ("Validated Enough for Concept Review", "Governance reviewer", "Concept refinement response"),
        )
        for status, owner, mode in cases:
            with self.subTest(status=status):
                self.assertEqual(response_for(status, owner)["response_mode"], mode)

    def test_forcing_signals_add_domain_options(self) -> None:
        cases = (
            ("Water Storage Deficit", "Water storage audit"),
            ("Evaporation Pressure", "Microclimate shade strategy"),
            ("Fire Exposure", "Bushfire buffer review"),
            ("Vegetation Stress", "Ecological buffer restoration"),
        )
        for forcing, option in cases:
            with self.subTest(forcing=forcing):
                self.assertIn(option, derive_response_options([], "", forcing))

    def test_no_major_gap_adds_refinement_options(self) -> None:
        options = derive_response_options(
            ["No major validation gap identified at concept level"], "Governance reviewer", ""
        )
        self.assertIn("Concept design refinement", options)
        self.assertIn("Governance consultation", options)

    def test_scenario_compare_output_includes_response_fields(self) -> None:
        run_scenario_compare()
        output_dir = REPO_ROOT / "cczps_lite" / "output"
        with (output_dir / "comparison_matrix.csv").open("r", encoding="utf-8", newline="") as file_obj:
            rows = list(csv.DictReader(file_obj))
        self.assertEqual(len(rows), 8)
        for field in ("response_priority", "response_options", "response_mode", "response_summary"):
            self.assertIn(field, rows[0])
        self.assertNotIn("[", rows[0]["response_options"])
        self.assertIn("### Adaptive Response Runtime", (output_dir / "scenario_report.md").read_text(encoding="utf-8"))
        self.assertIn("## Adaptive Response Reading", (output_dir / "governance_summary.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
