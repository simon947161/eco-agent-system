"""Tests for the CCZPS-Lite Validation Feedback / Review Loop Runtime."""

from __future__ import annotations

import csv
import unittest
from pathlib import Path

from cczps_lite.engine.review_loop import derive_review_action, derive_review_owner
from cczps_lite.engine.scenario_compare import main as run_scenario_compare

REPO_ROOT = Path(__file__).resolve().parents[1]


def review_for(status: str, score: float = 5.0, gaps=None) -> dict:
    return derive_review_action(
        {"validation_status": status, "validation_score": score, "validation_gaps": gaps or []},
        {}, {"primary_forcing": "Mixed / Unclear Forcing"},
    )


class ReviewLoopRuntimeTests(unittest.TestCase):
    def test_review_actions_follow_validation_status(self) -> None:
        cases = (
            ("Insufficient Evidence", 3, "Hold and collect evidence"),
            ("Requires Technical Validation", 5, "Escalate to technical review"),
            ("Requires Local Validation", 6, "Send to local review"),
            ("Validated Enough for Concept Review", 8, "Proceed to concept review"),
        )
        for status, score, action in cases:
            with self.subTest(status=status):
                self.assertEqual(review_for(status, score)["review_action"], action)

    def test_domain_gaps_map_to_review_owners(self) -> None:
        cases = (
            ("Need hydrological or soil moisture validation", "Water / hydrology reviewer"),
            ("Need local temperature, humidity, and evaporation observation", "Microclimate reviewer"),
            ("Need bushfire exposure and vegetation management review", "Fire resilience reviewer"),
            ("Need ecological condition and canopy-cover review", "Ecology reviewer"),
        )
        for gap, owner in cases:
            with self.subTest(gap=gap):
                self.assertEqual(derive_review_owner([gap], ""), owner)

    def test_scenario_compare_output_includes_review_fields(self) -> None:
        run_scenario_compare()
        output_dir = REPO_ROOT / "cczps_lite" / "output"
        with (output_dir / "comparison_matrix.csv").open("r", encoding="utf-8", newline="") as file_obj:
            rows = list(csv.DictReader(file_obj))
        self.assertEqual(len(rows), 8)
        for field in ("review_action", "review_priority", "review_owner", "review_triggers", "review_summary"):
            self.assertIn(field, rows[0])
        self.assertNotIn("[", rows[0]["review_triggers"])
        self.assertIn("### Validation Feedback / Review Loop", (output_dir / "scenario_report.md").read_text(encoding="utf-8"))
        self.assertIn("## Review Loop Reading", (output_dir / "governance_summary.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
