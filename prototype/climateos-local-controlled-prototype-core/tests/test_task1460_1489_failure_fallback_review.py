import importlib.util
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'failure_fallback_review'/'governance.py'
SPEC=importlib.util.spec_from_file_location('fallback_governance',PATH)
GOV=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GOV)

class Task1460FallbackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path=ROOT/'failure_fallback_review'/'tiny_synthetic_failure_fixtures.json'
        cls.cases={x['event_id']:x for x in json.loads(path.read_text())['cases']}

    def test_stale_primary_preserves_primary_and_inactive_fallback(self):
        result=GOV.validate_event(self.cases['failure-stale'])
        self.assertTrue(result['valid'])
        self.assertEqual('ai-primary',result['record']['primary_source_id'])
        self.assertFalse(result['record']['fallback_active'])

    def test_no_eligible_source_requires_stop(self):
        result=GOV.validate_event(self.cases['failure-none'])
        self.assertTrue(result['valid'])
        self.assertEqual('STOP_REQUIRED',result['record']['failure_state'])

    def test_recovery_remains_pending_without_evidence(self):
        result=GOV.validate_event(self.cases['failure-recovery'])
        self.assertEqual('RECOVERY_PENDING',result['record']['failure_state'])

    def test_human_identity_is_required(self):
        with self.assertRaises(ValueError): GOV.record_human_ack(self.cases['failure-stale'],{'action':'STOP'})

    def test_automatic_failover_is_prohibited(self):
        with self.assertRaises(PermissionError): GOV.automatic_failover({})

    def test_warning_and_evidence_free_recovery_are_prohibited(self):
        with self.assertRaises(PermissionError): GOV.public_warning({})
        with self.assertRaises(PermissionError): GOV.accept_recovery_without_evidence({})

if __name__=='__main__': unittest.main()
