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
    def test_generated_outputs_include_complete_runtime_fields(self) -> None:
        run_scenario_compare()
        output_dir = REPO_ROOT / "cczps_lite" / "output"
        with (output_dir / "comparison_matrix.csv").open(
            "r", encoding="utf-8", newline=""
        ) as file_obj:
            rows = list(csv.DictReader(file_obj))

        self.assertEqual(len(rows), 8)
        expected_fields = (
            "validation_context", "geography", "geographic_scale",
            "watershed_stage", "watershed_continuity", "evidence_strength",
            "source_basis", "uncertainty_notes", "human_review_required",
            "water_gradient", "differential_status", "forcing_candidates",
            "primary_forcing", "forcing_priority", "validation_score",
            "validation_status", "validation_gaps", "review_action",
            "review_priority", "review_owner", "review_triggers",
            "response_priority", "response_options", "response_mode",
            "implementation_priority", "urgency_level", "expected_benefit",
            "prioritised_response", "prioritisation_summary",
        )
        for field in expected_fields:
            self.assertIn(field, rows[0])

        ids = {row["scenario_id"] for row in rows}
        for scenario_id in (
            "BATLOW_ENERGY_RESILIENCE",
            "KUNLUN_ECO_WATER",
            "IRAQ_AGRICULTURE_RECOVERY",
            "XIONGAN_WUTAI_HEADWATERS",
            "XIONGAN_BAIYANGDIAN_WETLAND",
            "XIONGAN_DOWNSTREAM_URBAN",
        ):
            self.assertIn(scenario_id, ids)

        energy_row = next(row for row in rows if row["scenario_id"] == "BATLOW_ENERGY_RESILIENCE")
        self.assertEqual(energy_row["evidence_strength"], "Low")
        self.assertEqual(energy_row["human_review_required"], "True")
        self.assertEqual(energy_row["implementation_priority"], "High")

        watershed_rows = [row for row in rows if row["scenario_id"].startswith("XIONGAN_")]
        self.assertEqual(len(watershed_rows), 3)
        self.assertEqual(
            {row["watershed_continuity"] for row in watershed_rows},
            {"Moderate Continuity"},
        )

        scenario_report = (output_dir / "scenario_report.md").read_text(encoding="utf-8")
        governance_summary = (output_dir / "governance_summary.md").read_text(encoding="utf-8")
        validation_pack = (output_dir / "scenario_validation_pack.md").read_text(encoding="utf-8")
        self.assertIn("### Response Prioritisation Runtime", scenario_report)
        self.assertIn("## Multi-Scale Scenario Validation", scenario_report)
        self.assertIn("### Watershed Continuity Reading", scenario_report)
        self.assertIn("## Multi-Scale Validation Reading", governance_summary)
        self.assertIn("# CCZPS-Lite Multi-Scale Scenario Validation Pack", validation_pack)
        self.assertIn("Scenario B — Kunlun Eco-Water System", validation_pack)
        self.assertIn("Scenario C — Iraq Agriculture Recovery", validation_pack)
        self.assertIn("Moderate Continuity", validation_pack)
        self.assertIn("human review required", validation_pack)

    def test_input_json_files_are_valid(self) -> None:
        input_dir = REPO_ROOT / "cczps_lite" / "input"
        for path in input_dir.glob("*.json"):
            with self.subTest(path=path.name):
                with path.open("r", encoding="utf-8") as file_obj:
                    data = json.load(file_obj)
                if path.name == "location_intake_examples.json":
                    self.assertIsInstance(data, list)
                    self.assertTrue(all(isinstance(record, dict) for record in data))
                else:
                    self.assertIsInstance(data, dict)


if __name__ == "__main__":
    unittest.main()
