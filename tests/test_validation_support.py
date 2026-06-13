"""Tests for the local-only validation support sprint."""
from __future__ import annotations
import json
import tempfile
import unittest
from pathlib import Path
from cczps_lite.engine.validation_support import REVIEW_CATEGORIES,build_validation_support_outputs,write_validation_support_outputs

class ValidationSupportTests(unittest.TestCase):
    def setUp(self): self.outputs=build_validation_support_outputs()
    def test_all_artifacts_are_generated(self):
        self.assertEqual(set(self.outputs),{"gis_dem_access_plan","professional_validation_interface","expert_review_records","planning_approval_support_report"})
    def test_gis_governance_and_metadata(self):
        plan=self.outputs["gis_dem_access_plan"][0]; governance=plan["governance"]
        self.assertEqual(plan["implementation_status"],"planning_only")
        self.assertTrue(governance["usage_cost_governance_required"]); self.assertTrue(governance["budget_guard_required"]); self.assertTrue(governance["manual_approval_for_external_or_paid_resources"]); self.assertFalse(governance["hidden_cost_absorption_permitted"])
        for field in ("data source","retrieval status","spatial resolution","license or access condition","uncertainty notes","cost owner","confidence level"): self.assertIn(field,plan["connector_metadata"])
    def test_validation_categories_and_human_signoff(self):
        interface=self.outputs["professional_validation_interface"][0]
        for review in interface["reviews"].values():
            self.assertEqual(set(review["review_categories"]),set(REVIEW_CATEGORIES)); self.assertEqual(review["review_status"],"awaiting_professional_review"); self.assertTrue(review["human_sign_off_required"])
    def test_expert_records_are_blank_auditable_templates(self):
        required={"reviewer_role","review_date","reviewed_scenario_or_module","review_category","finding","evidence_reference","confidence_level","required_follow_up","decision_status"}
        for record in self.outputs["expert_review_records"][0]["records"]:
            self.assertTrue(required.issubset(record)); self.assertEqual(record["record_status"],"template"); self.assertEqual(record["decision_status"],"not_reviewed"); self.assertIsNone(record["finding"])
    def test_approval_report_preserves_human_boundary(self):
        report=self.outputs["planning_approval_support_report"][0]; self.assertTrue(report["human_approval_required"])
        for scenario in report["scenarios"]:
            self.assertEqual(scenario["gis_dem_readiness"],"planning_only_not_acquired"); self.assertEqual(scenario["approval_support_status"],"not_ready_for_approval"); self.assertIn("cannot grant",scenario["human_approval_boundary"])
    def test_json_and_markdown_outputs_are_valid(self):
        with tempfile.TemporaryDirectory() as directory:
            output_dir=Path(directory); write_validation_support_outputs(self.outputs,output_dir)
            for name in self.outputs:
                self.assertEqual(json.loads((output_dir/f"{name}.json").read_text(encoding="utf-8"))["schema_version"],"1.0"); self.assertTrue((output_dir/f"{name}.md").read_text(encoding="utf-8").startswith("# "))
    def test_no_network_or_llm_clients(self):
        script=(Path(__file__).resolve().parents[1]/"cczps_lite"/"engine"/"validation_support.py").read_text(encoding="utf-8")
        for forbidden in ("urlopen(","requests.","OpenAI(","anthropic.","chat.completions","http://","https://"): self.assertNotIn(forbidden,script)
if __name__=="__main__": unittest.main()
