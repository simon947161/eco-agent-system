"""Regression tests for the CCZPS-Lite v0.4 stabilized prototype."""

from __future__ import annotations

import csv
import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ENGINE_DIR = REPO_ROOT / "cczps_lite" / "engine"
if str(ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(ENGINE_DIR))

from evidence_layer import (  # noqa: E402
    derive_evidence_strength,
    derive_human_review_required,
    derive_source_basis,
    derive_uncertainty_notes,
)
from scenario_compare import main as run_scenario_compare  # noqa: E402


class EvidenceLayerTests(unittest.TestCase):
    """Verify evidence derivation rules remain transparent and stable."""

    def test_low_evidence_requires_human_review(self) -> None:
        evidence = {
            "strength": "low",
            "source": "concept study",
            "notes": "No formal assessment yet.",
        }
        self.assertEqual(derive_evidence_strength(evidence), "Low")
        self.assertEqual(derive_source_basis(evidence), "Concept Study")
        self.assertEqual(derive_uncertainty_notes(evidence), "Concept-level assumptions only.")
        self.assertTrue(derive_human_review_required(evidence))

    def test_mixed_pathway_uses_weakest_strength_and_mixed_sources(self) -> None:
        evidence = {
            "ecology": {"strength": "medium", "source": "regional understanding"},
            "fire": {"strength": "high", "source": "historical bushfire experience"},
        }
        self.assertEqual(derive_evidence_strength(evidence), "Medium")
        self.assertEqual(derive_source_basis(evidence), "Mixed Sources")
        self.assertFalse(derive_human_review_required(evidence))


class ScenarioCompareOutputTests(unittest.TestCase):
    """Verify generated outputs include the evidence-aware governance fields."""

    def test_generated_outputs_include_evidence_fields(self) -> None:
        run_scenario_compare()
        output_dir = REPO_ROOT / "cczps_lite" / "output"
        comparison_path = output_dir / "comparison_matrix.csv"
        scenario_report_path = output_dir / "scenario_report.md"
        governance_summary_path = output_dir / "governance_summary.md"

        with comparison_path.open("r", encoding="utf-8", newline="") as file_obj:
            rows = list(csv.DictReader(file_obj))

        self.assertEqual(len(rows), 3)
        expected_fields = (
            "evidence_strength", "source_basis", "uncertainty_notes",
            "human_review_required", "water_gradient", "differential_status",
            "differential_summary", "forcing_candidates", "primary_forcing",
            "forcing_priority", "forcing_summary", "validation_score",
            "validation_status", "validation_gaps", "validation_summary",
            "review_action", "review_priority", "review_owner",
            "review_triggers", "review_summary",
        )
        for field in expected_fields:
            self.assertIn(field, rows[0])

        energy_row = next(row for row in rows if row["scenario_id"] == "BATLOW_ENERGY_RESILIENCE")
        self.assertEqual(energy_row["evidence_strength"], "Low")
        self.assertEqual(energy_row["human_review_required"], "True")

        scenario_report = scenario_report_path.read_text(encoding="utf-8")
        self.assertIn("## Notes on Confidence and Validation", scenario_report)
        self.assertIn("Evidence strength: Low", scenario_report)
        self.assertIn("### Differential Field Runtime", scenario_report)
        self.assertIn("### Forcing Layer Runtime", scenario_report)
        self.assertIn("### Validation Layer Runtime", scenario_report)
        self.assertIn("### Validation Feedback / Review Loop", scenario_report)
        self.assertIn("Review action:", scenario_report)
        self.assertIn("Validation layer cautiously", scenario_report)

        governance_summary = governance_summary_path.read_text(encoding="utf-8")
        self.assertIn("## Evidence Assessment", governance_summary)
        self.assertIn("## Differential Field Reading", governance_summary)
        self.assertIn("## Forcing Layer Reading", governance_summary)
        self.assertIn("## Validation Layer Runtime", governance_summary)
        self.assertIn("## Review Loop Reading", governance_summary)
        self.assertIn("Highest review priority pathway:", governance_summary)
        self.assertIn("Suggested next governance action:", governance_summary)
        self.assertIn("Scenarios requiring human review: Energy Resilience Pathway.", governance_summary)

    def test_input_json_files_are_valid(self) -> None:
        input_dir = REPO_ROOT / "cczps_lite" / "input"
        for path in input_dir.glob("*.json"):
            with self.subTest(path=path.name):
                with path.open("r", encoding="utf-8") as file_obj:
                    self.assertIsInstance(json.load(file_obj), dict)


if __name__ == "__main__":
    unittest.main()
