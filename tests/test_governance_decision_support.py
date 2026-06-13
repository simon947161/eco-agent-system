"""Tests for the deterministic internal governance decision support layer."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from cczps_lite.engine import governance_decision_support as support


class GovernanceDecisionSupportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.output = support.build_governance_decision_records()

    def test_schema_and_scenarios(self) -> None:
        self.assertEqual(self.output["record_count"], 4)
        self.assertEqual(
            {record["scenario_id"] for record in self.output["records"]},
            set(support.SCENARIOS),
        )
        required = {
            "decision_record_id", "scenario_id", "scenario_name",
            "internal_decision_status", "external_approval_status",
            "evidence_trace_ids", "planning_hypothesis_reference",
            "validation_references", "evidence_summary",
            "unresolved_evidence_gaps", "unresolved_risks",
            "required_human_actions", "human_review_required",
            "professional_review_required", "limitations",
        }
        for record in self.output["records"]:
            self.assertTrue(required.issubset(record))

    def test_current_records_require_further_review(self) -> None:
        self.assertEqual(
            {record["internal_decision_status"] for record in self.output["records"]},
            {"requires_further_review"},
        )
        for record in self.output["records"]:
            self.assertIn(record["internal_decision_status"], support.ALLOWED_STATUSES)
            self.assertTrue(record["evidence_trace_ids"])
            self.assertTrue(record["planning_hypothesis_reference"])

    def test_approval_and_review_boundaries_are_mandatory(self) -> None:
        for record in self.output["records"]:
            self.assertEqual(record["external_approval_status"], "not_ready_for_approval")
            self.assertTrue(record["human_review_required"])
            self.assertTrue(record["professional_review_required"])

    def test_missing_traceability_is_deferred(self) -> None:
        sources = {key: support._load(path) for key, path in support.SOURCE_PATHS.items()}
        sources["traceability"] = {"records": []}
        output = support.build_governance_decision_records(sources)
        for record in output["records"]:
            self.assertEqual(record["internal_decision_status"], "deferred")
            self.assertIn("Missing evidence traceability.", record["unresolved_evidence_gaps"])

    def test_not_supported_hypothesis_stays_not_supported(self) -> None:
        sources = {key: support._load(path) for key, path in support.SOURCE_PATHS.items()}
        sources = json.loads(json.dumps(sources))
        sources["hypotheses"]["hypotheses"]["batlow"]["hypothesis_status"] = "not_supported"
        output = support.build_governance_decision_records(sources)
        batlow = next(record for record in output["records"] if record["scenario_id"] == "batlow")
        self.assertEqual(batlow["internal_decision_status"], "not_supported_by_current_evidence")

    def test_outputs_are_valid_json_and_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            json_path = Path(temp_dir) / "records.json"
            md_path = Path(temp_dir) / "records.md"
            support.write_governance_decision_outputs(self.output, json_path, md_path)
            self.assertEqual(json.loads(json_path.read_text()), self.output)
            report = md_path.read_text(encoding="utf-8")
            self.assertIn("# Internal Governance Decision Support", report)
            self.assertIn("not_ready_for_approval", report)
            for scenario in support.SCENARIOS.values():
                self.assertIn(f"## {scenario}", report)

    def test_runtime_has_no_network_or_llm_clients(self) -> None:
        source = Path(support.__file__).read_text(encoding="utf-8")
        for forbidden in ("requests", "urllib", "http://", "https://", "OpenAI", "anthropic", "socket"):
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()
