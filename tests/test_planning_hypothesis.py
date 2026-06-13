"""Tests for the cautious Planning Hypothesis Runtime."""
from __future__ import annotations
import tempfile
import unittest
from pathlib import Path
from cczps_lite.engine.planning_hypothesis import HYPOTHESIS_STATUSES, build_planning_hypotheses, classify_hypothesis_status, derive_failure_conditions, derive_planning_hypothesis, derive_validation_indicators, write_planning_hypothesis_outputs

PROFILE = {"hypothesis_id": "test_hypothesis", "scenario": "Test", "scenario_ids": ["TEST"], "problem_statement": "A local stress may affect resilience.", "planning_assumption": "A tested buffer may reduce the stress.", "intervention_logic": "Test the buffer with local evidence.", "expected_effect": "Indicators may improve if the assumption is supported."}


class PlanningHypothesisTests(unittest.TestCase):
    def test_generated_output_has_required_schema_and_scenarios(self) -> None:
        output = build_planning_hypotheses()
        self.assertEqual(output["schema_version"], "1.0")
        self.assertEqual(set(output["hypotheses"]), {"batlow", "kunlun", "iraq", "baiyangdian_xiongan"})
        for hypothesis in output["hypotheses"].values():
            for field in ("hypothesis_id", "hypothesis_status", "problem_statement", "planning_assumption", "intervention_logic", "expected_effect", "validation_indicators", "failure_conditions", "human_review_required", "hypothesis_summary"):
                self.assertIn(field, hypothesis)
            self.assertIn(hypothesis["hypothesis_status"], HYPOTHESIS_STATUSES)
            self.assertTrue(hypothesis["human_review_required"])

    def test_status_classification_covers_conservative_states(self) -> None:
        self.assertEqual(classify_hypothesis_status([], [], None, None), "insufficient_evidence")
        self.assertEqual(classify_hypothesis_status(["Medium"], ["Requires Technical Validation"], "sufficient_observations", "valid_configured"), "requires_validation")
        self.assertEqual(classify_hypothesis_status(["Medium"], ["Validated Enough for Concept Review"], "insufficient_data", "valid_configured"), "concept_level")
        self.assertEqual(classify_hypothesis_status(["High"], ["Validated Enough for Concept Review"], "sufficient_observations", "valid_configured"), "evidence_supported")
        self.assertEqual(classify_hypothesis_status(["High"], ["Validated Enough for Concept Review"], "sufficient_observations", "valid_configured", 2), "not_supported")

    def test_indicators_and_failure_conditions_are_explicit(self) -> None:
        context = {"focus": ["water balance", "ecological restoration", "flood resilience"], "missing_spatial_data": True}
        indicators = derive_validation_indicators(context)
        failures = derive_failure_conditions(context)
        self.assertIn("water balance or soil moisture evidence", indicators)
        self.assertIn("vegetation or ecological condition evidence", indicators)
        self.assertIn("hazard-specific technical review", indicators)
        self.assertIn("required spatial context remains incomplete", failures)

    def test_human_review_defaults_true_for_concept_hypothesis(self) -> None:
        hypothesis = derive_planning_hypothesis(PROFILE, {"evidence_strengths": ["Medium"], "validation_statuses": ["Validated Enough for Concept Review"], "trend_status": "insufficient_data", "spatial_status": "valid_configured"})
        self.assertEqual(hypothesis["hypothesis_status"], "concept_level")
        self.assertTrue(hypothesis["human_review_required"])
        self.assertIn("not a recommendation", hypothesis["hypothesis_summary"])

    def test_markdown_and_json_outputs_are_written(self) -> None:
        output = build_planning_hypotheses()
        with tempfile.TemporaryDirectory() as directory:
            json_path = Path(directory) / "planning_hypotheses.json"
            md_path = Path(directory) / "planning_hypotheses.md"
            write_planning_hypothesis_outputs(output, json_path, md_path)
            self.assertTrue(json_path.is_file())
            report = md_path.read_text(encoding="utf-8")
        self.assertIn("# Planning Hypothesis Runtime", report)
        self.assertIn("## Batlow", report)
        self.assertIn("Human review required: True", report)

    def test_runtime_contains_no_live_or_llm_clients(self) -> None:
        script = (Path(__file__).resolve().parents[1] / "cczps_lite" / "engine" / "planning_hypothesis.py").read_text(encoding="utf-8")
        for forbidden in ("urlopen(", "requests.", "OpenAI(", "anthropic.", "chat.completions", "power.larc.nasa.gov"):
            self.assertNotIn(forbidden, script)


if __name__ == "__main__":
    unittest.main()
