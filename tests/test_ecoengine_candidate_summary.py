"""Public summary/guard tests; cannot certify or reproduce local private runs."""
from pathlib import Path
import copy,importlib.util,json,unittest
TASK=Path(__file__).resolve().parents[1]/'docs/tasks/ecoengine_v200_private_method_comparison_001'
def load(name):
    spec=importlib.util.spec_from_file_location(name,TASK/'scripts'/f'{name}.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

class CandidateExportTests(unittest.TestCase):
    def setUp(self):
        self.gate=load('privacy_gate')
        self.a=json.loads((TASK/'evidence/local-candidate-attestation.json').read_text(encoding='utf-8'))
    def test_minimal_attestation(self):self.gate.check_attestation(self.a)
    def test_private_field_injection_rejected(self):
        self.a['source_snippet']='private content'
        with self.assertRaises(AssertionError):self.gate.check_attestation(self.a)
    def test_private_payload_rejected(self):
        for key,value in [('private_payload',{'raw_inputs':[1,2,3]}),('native_exact_replay','unexpected text')]:
            with self.subTest(key=key):
                a=copy.deepcopy(self.a);a[key]=value
                with self.assertRaises(AssertionError):self.gate.check_attestation(a)
    def test_promotion_or_ranking_rejected(self):
        for key,value in [('scientific_admission','ADMITTED'),('winner','LEGACY'),('paired_prediction_accuracy_comparisons',10)]:
            with self.subTest(key=key):
                a=copy.deepcopy(self.a);a[key]=value
                with self.assertRaises(AssertionError):self.gate.check_attestation(a)
    def test_count_misrepresentation_rejected(self):
        self.a['call_attempts']=18
        with self.assertRaises(AssertionError):self.gate.check_attestation(self.a)
    def test_failure_erasure_rejected(self):
        self.a['boundary_outcomes'][1]['result']='PASS'
        with self.assertRaises(AssertionError):self.gate.check_attestation(self.a)
    def test_public_contracts_reproduce(self):
        fresh=load('public_boundary_checks').run()
        saved=json.loads((TASK/'evidence/public-boundary-checks.json').read_text(encoding='utf-8'))
        self.assertEqual(fresh,saved);self.assertEqual(fresh['trajectory_runs'],0)
    def test_all_public_export_gates(self):self.assertEqual(self.gate.gate()['status'],'PASS_PUBLIC_EXPORT_GATES')
    def test_raw_graph_injection_rejected(self):
        a=json.loads((TASK/'evidence/mechanism-audit-attestation.json').read_text(encoding='utf-8'))
        a['private_graph']={'nodes':['private']}
        with self.assertRaises(AssertionError):self.gate.check_mechanism_attestation(a)
    def test_mechanism_overclaim_rejected(self):
        a=json.loads((TASK/'evidence/mechanism-audit-attestation.json').read_text(encoding='utf-8'))
        a['automatic_scientific_relationship_discovery_proven']=True
        with self.assertRaises(AssertionError):self.gate.check_mechanism_attestation(a)

if __name__=='__main__':unittest.main()
