import importlib.util
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'coupling_input_gate'/'eligibility.py'
SPEC=importlib.util.spec_from_file_location('eligibility',PATH)
GATE=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)

class Task1490CouplingInputTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path=ROOT/'coupling_input_gate'/'tiny_synthetic_coupling_fixtures.json'
        cls.cases={x['case_id']:x for x in json.loads(path.read_text())['cases']}

    def test_complete_synthetic_candidate_is_structurally_valid(self):
        result=GATE.evaluate_fixture(self.cases['synthetic-complete'])
        self.assertTrue(result['valid'])
        self.assertFalse(result['record']['connection_authorized'])

    def test_limited_candidate_preserves_limitations(self):
        result=GATE.evaluate_fixture(self.cases['synthetic-limited'])
        self.assertTrue(result['valid'])
        self.assertTrue(result['record']['limitations'])

    def test_blocked_case_preserves_missing_evidence(self):
        result=GATE.evaluate_fixture(self.cases['synthetic-blocked'])
        self.assertFalse(result['valid'])
        self.assertIn('missing_evidence',{x['code'] for x in result['blockers']})

    def test_no_real_source_is_declared_ready(self):
        path=ROOT/'coupling_input_gate'/'current_source_readiness.json'
        data=json.loads(path.read_text())
        self.assertEqual('NO_REAL_SOURCE_DECLARED_READY',data['status'])

    def test_source_connection_and_coupling_are_prohibited(self):
        with self.assertRaises(PermissionError): GATE.connect_source({})
        with self.assertRaises(PermissionError): GATE.calculate_coupling({})

    def test_task1500_start_is_prohibited(self):
        with self.assertRaises(PermissionError): GATE.start_task1500()

if __name__=='__main__': unittest.main()
