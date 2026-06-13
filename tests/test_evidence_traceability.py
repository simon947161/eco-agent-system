"""Tests for the deterministic Evidence Traceability Layer."""
from __future__ import annotations
import json
import tempfile
import unittest
from pathlib import Path
from cczps_lite.engine.evidence_traceability import REQUIRED_FIELDS,SCENARIOS,SOURCE_PATHS,build_evidence_traceability,write_evidence_traceability_outputs

class EvidenceTraceabilityTests(unittest.TestCase):
    def test_schema_and_required_fields(self):
        output=build_evidence_traceability(); self.assertEqual(output["schema_version"],"1.0"); self.assertEqual(output["record_count"],len(SCENARIOS)*len(SOURCE_PATHS)); self.assertEqual(len(output["records"]),output["record_count"])
        for record in output["records"]: self.assertTrue(set(REQUIRED_FIELDS).issubset(record)); self.assertTrue(record["human_review_required"])
    def test_records_link_to_existing_artifacts(self):
        for record in build_evidence_traceability()["records"]:
            path=Path(__file__).resolve().parents[1]/record["evidence_source"].split("#",1)[0]; self.assertTrue(path.is_file(),record["trace_id"])
    def test_missing_evidence_is_insufficient(self):
        output=build_evidence_traceability({key:None for key in SOURCE_PATHS})
        for record in output["records"]: self.assertEqual(record["evidence_strength"],"insufficient_evidence"); self.assertEqual(record["review_status"],"not_reviewed"); self.assertTrue(record["human_review_required"])
    def test_approval_trace_does_not_upgrade_status(self):
        records=[x for x in build_evidence_traceability()["records"] if x["artifact_type"]=="planning_approval_support_report"]; self.assertEqual(len(records),len(SCENARIOS))
        for record in records: self.assertEqual(record["review_status"],"not_ready_for_approval"); self.assertIn("cannot grant"," ".join(record["limitations"]))
    def test_markdown_and_json_are_generated(self):
        output=build_evidence_traceability()
        with tempfile.TemporaryDirectory() as directory:
            json_path=Path(directory)/"evidence_traceability.json"; markdown_path=Path(directory)/"evidence_traceability.md"; write_evidence_traceability_outputs(output,json_path,markdown_path); loaded=json.loads(json_path.read_text(encoding="utf-8")); markdown=markdown_path.read_text(encoding="utf-8")
        self.assertEqual(loaded["record_count"],output["record_count"]); self.assertIn("# Evidence Traceability Layer",markdown); self.assertIn("## Batlow",markdown)
    def test_runtime_has_no_network_or_llm_clients(self):
        script=(Path(__file__).resolve().parents[1]/"cczps_lite"/"engine"/"evidence_traceability.py").read_text(encoding="utf-8")
        for forbidden in ("urlopen(","requests.","OpenAI(","anthropic.","chat.completions","http://","https://"): self.assertNotIn(forbidden,script)
if __name__=="__main__": unittest.main()
