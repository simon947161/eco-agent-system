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
        {
            "validation_status": status,
            "validation_score": score,
            "validation_gaps": gaps or [],
        },
        {},
        {"primary_forcing": "Mixed / Unclear Forcing"},
    )


class ReviewLoopRuntimeTests(unittest.TestCase):
    """Verify review actions, routing, priorities, and generated fields."""

    def test_insufficient_evidence_holds_pathway(self) -> None:
        self.assertEqual(
            review_for("Insufficient Evidence", 3)["review_action"],
            "Hold and collect evidence",
        )

    def test_technical_validation_escalates(self) -> None:
        self.assertEqual(
            review_for("Requires Technical Validation")["review_action"],
            "Escalate to technical review",
        )

    def test_local_validation_routes_to_local_review(self) -> None:
        self.assertEqual(
            review_for("Requires Local Validation")["review_action"],
            "Send to local review",
        )

    def test_concept_ready_pathway_proceeds(self) -> None:
        self.assertEqual(
            review_for("Validated Enough for Concept Review", 8)["review_action"],
            "Proceed to concept review",
        )

    def test_hydrology_gap_maps_to_water_reviewer(self) -> None:
        self.assertEqual(
            derive_review_owner(["Need hydrological or soil moisture validation"], ""),
            "Water / hydrology reviewer",
        )

    def test_evaporation_gap_maps_to_microclimate_reviewer(self) -> None:
        self.assertEqual(
            derive_review_owner(["Need local temperature, humidity, and evaporation observation"], ""),
            "Microclimate reviewer",
        )

    def test_fire_gap_maps_to_fire_resilience_reviewer(self) -> None:
        self.assertEqual(
            derive_review_owner(["Need bushfire exposure and vegetation management review"], ""),
            "Fire resilience reviewer",
        )

    def test_ecology_gap_maps_to_ecology_reviewer(self) -> None:
        self.assertEqual(
            derive_review_owner(["Need ecological condition and canopy-cover review"], ""),
            "Ecology reviewer",
        )

    def test_scenario_compare_output_includes_review_fields(self) -> None:
        run_scenario_compare()
        output_dir = REPO_ROOT / "cczps_lite" / "output"
        with (output_dir / "comparison_matrix.csv").open(
            "r", encoding="utf-8", newline=""
        ) as file_obj:
            rows = list(csv.DictReader(file_obj))

        self.assertEqual(len(rows), 3)
        for field in (
            "review_action",
            "review_priority",
            "review_owner",
            "review_triggers",
            "review_summary",
        ):
            self.assertIn(field, rows[0])
        self.assertNotIn("[", rows[0]["review_triggers"])

        scenario_report = (output_dir / "scenario_report.md").read_text(encoding="utf-8")
        governance_summary = (output_dir / "governance_summary.md").read_text(encoding="utf-8")
        self.assertIn("### Validation Feedback / Review Loop", scenario_report)
        self.assertIn("## Review Loop Reading", governance_summary)


if __name__ == "__main__":
    unittest.main()
