"""Reproduce public native gates; never load or certify private legacy code."""
from pathlib import Path
import copy,importlib.util,json,math,unittest
TASK=Path(__file__).resolve().parents[1]/'docs/tasks/ecoengine_v200_private_method_comparison_001'
def load(name):
    spec=importlib.util.spec_from_file_location(name,TASK/'scripts'/f'{name}.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

class PairwiseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pub=load('pairwise_public');cls.gate=load('privacy_gate');cls.summary=json.loads((TASK/'evidence/pairwise-summary.json').read_text(encoding='utf-8'))
    def test_same_inputs_and_honest_counts(self):
        self.gate.check_pairwise(self.summary);design=self.pub.design()
        self.assertEqual(design,json.loads((TASK/'PAIRWISE_PROTOCOL.json').read_text(encoding='utf-8')))
        self.assertEqual(self.summary['protocol_sha256'],self.pub.digest(design))
        for c,r in zip(design['cases'],self.summary['rows']):
            self.assertEqual(self.pub.digest(c),r['canonical_input_sha256']);self.assertEqual(self.pub.reference(c),r['reference'])
    def test_new_native_side_reproduces(self):
        fresh=self.pub.run();saved=json.loads((TASK/'evidence/pairwise-new-results.json').read_text(encoding='utf-8'))
        self.assertEqual(fresh['source_hashes'],saved['source_hashes']);self.assertEqual(fresh['protocol_sha256'],saved['protocol_sha256'])
        expected=[None,'MISSING_DEPENDENCY','NONFINITE','MISSING_DEPENDENCY','UNIT_MISMATCH','TIME_MISMATCH']
        def equal(a,b):
            if isinstance(a,dict):
                self.assertEqual(set(a),set(b))
                for k in a:equal(a[k],b[k])
            elif isinstance(a,list):
                self.assertEqual(len(a),len(b))
                for x,y in zip(a,b):equal(x,y)
            elif isinstance(a,float):self.assertTrue(math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-10))
            else:self.assertEqual(a,b)
        for a,b,code in zip(fresh['rows'],saved['rows'],expected):
            self.assertEqual(a['new']['code'],code);equal(self.pub.stable(a['new']),self.pub.stable(b['new']))
        self.assertEqual(fresh['rows'][0]['new']['native_nodes_started'],['atmosphere','surface'])
        self.assertTrue(fresh['rows'][0]['new']['state_unmodified'])
    def test_private_payload_and_extra_keys_rejected(self):
        for key,value in [('private_payload',{'source':'private'}),('raw_graph',[])]:
            a=copy.deepcopy(self.summary);a[key]=value
            with self.assertRaises(AssertionError):self.gate.check_pairwise(a)
    def test_incompatible_groups_cannot_be_counted_complete(self):
        a=copy.deepcopy(self.summary);a['completed_comparable_groups']=6
        with self.assertRaises(AssertionError):self.gate.check_pairwise(a)
    def test_metadata_loss_cannot_be_erased(self):
        a=copy.deepcopy(self.summary);a['rows'][4]['comparability']='COMPARABLE_NUMERIC_INPUT_GOVERNANCE'
        with self.assertRaises(AssertionError):self.gate.check_pairwise(a)
    def test_no_accuracy_or_science_promotion(self):
        for key,value in [('paired_prediction_accuracy_comparisons',4),('science','ADMITTED')]:
            a=copy.deepcopy(self.summary);a[key]=value
            with self.assertRaises(AssertionError):self.gate.check_pairwise(a)

if __name__=='__main__':unittest.main()
