import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "model_admission" / "admission_gate.py"
SPEC = importlib.util.spec_from_file_location("task1290_admission_gate", MODULE_PATH)
GATE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)


class Task1290AdmissionGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = ROOT / "model_admission" / "tiny_synthetic_admission_fixtures.json"
        cls.cases = {case["id"]: case for case in json.loads(path.read_text())["cases"]}

    def test_complete_fixture_is_structurally_complete(self):
        result = GATE.assess_completeness(self.cases["synthetic_complete"])
        self.assertTrue(result["complete"])
        self.assertEqual([], result["blockers"])

    def test_blocked_fixture_preserves_missing_evidence(self):
        result = GATE.assess_completeness(self.cases["synthetic_blocked"])
        self.assertFalse(result["complete"])
        codes = {item["code"] for item in result["blockers"]}
        self.assertIn("missing_evidence", codes)
        self.assertIn("licence_or_provenance_blocked", codes)

    def test_system_cannot_decide_real_model(self):
        with self.assertRaises(PermissionError):
            GATE.automatic_real_model_decision({})

    def test_human_identity_is_required(self):
        record = self.cases["synthetic_complete"]
        with self.assertRaises(ValueError):
            GATE.record_human_decision(record, {
                "state": "REQUIRES_FURTHER_EVIDENCE",
                "reason": "expert review required",
                "evidence_snapshot_id": record["evidence_snapshot_id"],
                "decided_at": "2026-07-12T00:00:00Z",
            })

    def test_favourable_decision_refuses_blocked_evidence(self):
        record = self.cases["synthetic_blocked"]
        with self.assertRaises(ValueError):
            GATE.record_human_decision(record, {
                "state": "ADMITTED_FOR_RESEARCH",
                "reason": "test only",
                "responsible_human": "synthetic-reviewer",
                "evidence_snapshot_id": record["evidence_snapshot_id"],
                "decided_at": "2026-07-12T00:00:00Z",
            })

    def test_human_decision_is_append_only(self):
        record = self.cases["synthetic_disputed"]
        decision = {
            "state": "REQUIRES_FURTHER_EVIDENCE",
            "reason": "open physical and OOD questions",
            "responsible_human": "synthetic-reviewer",
            "evidence_snapshot_id": record["evidence_snapshot_id"],
            "decided_at": "2026-07-12T00:00:00Z",
        }
        result = GATE.record_human_decision(record, decision)
        self.assertEqual(1, len(result["decision_history"]))
        self.assertNotIn("decision_history", record)


if __name__ == "__main__":
    unittest.main()
