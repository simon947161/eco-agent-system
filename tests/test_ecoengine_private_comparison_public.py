"""Public side only; these tests do not access or verify any private system."""
from pathlib import Path
import importlib.util,json,math,unittest
TASK=Path(__file__).resolve().parents[1]/'docs/tasks/ecoengine_v200_private_method_comparison_001'
def load(name):
    spec=importlib.util.spec_from_file_location(name,TASK/'scripts'/f'{name}.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

class PublicComparisonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod=load('public_controls');cls.export=load('privacy_gate');cls.saved=json.loads((TASK/'evidence/public_controls.json').read_text(encoding='utf-8'));cls.replay=cls.mod.run()
    def row(self,n):return self.saved['rows'][n-1]['new']
    def test_protocol_fixed(self):self.assertEqual(self.mod.protocol(),json.loads((TASK/'PUBLIC_CASE_PROTOCOL.json').read_text(encoding='utf-8')))
    def test_counts_are_not_legacy_comparison(self):
        self.assertEqual(self.saved['case_count'],8);self.assertEqual(self.saved['public_execution_count'],48);self.assertEqual(self.saved['legacy_execution_count'],0)
    def test_deterministic_public_replay(self):
        # run() checks exact repeats on this host. Cross-platform libm can differ
        # in last bits, so compare archived values in their declared units.
        for saved,replayed in zip(self.saved['rows'],self.replay['rows']):
            for name in ('independent','one_way','two_way'):
                a,b=saved['new'][name],replayed['new'][name]
                self.assertEqual(a['status'],b['status']);self.assertEqual(a['completed_steps'],b['completed_steps'])
                self.assertEqual(a['failure']['code'] if a['failure'] else None,b['failure']['code'] if b['failure'] else None)
                for key in a['final_values']:
                    for x,y in zip(a['final_values'][key],b['final_values'][key]):
                        if x is None:self.assertIsNone(y)
                        else:self.assertTrue(math.isclose(x,y,rel_tol=1e-12,abs_tol=1e-10))
    def test_baseline_bounded_error_not_accuracy_claim(self):
        for r in self.row(1).values():self.assertLess(r['max_water_residual_kg_m2'],1e-8);self.assertLess(r['max_energy_residual_j_m2'],1e-5);self.assertIsNone(r['forecast_skill'])
    def test_zero_wind_limit(self):
        runs=self.row(2);self.assertEqual(runs['independent']['final_values'],runs['two_way']['final_values']);self.assertTrue(all(r['evaporation_kg_m2']==0 for r in runs.values()))
    def test_sparse_dependency(self):
        self.assertEqual(self.row(4)['independent']['status'],'COMPLETED')
        for name in ('one_way','two_way'):self.assertEqual(self.row(4)[name]['failure']['code'],'MISSING_DEPENDENCY')
    def test_time_and_space_refusal(self):
        for n,code in ((5,'TIME_MISMATCH'),(6,'SPATIAL_MISMATCH')):
            for r in self.row(n).values():self.assertEqual(r['failure']['code'],code)
    def test_extreme_boundary_positive_runoff(self):
        for r in self.row(7).values():self.assertEqual(r['status'],'COMPLETED');self.assertGreater(r['runoff_kg_m2'],0)
    def test_iterative_failure_is_retained(self):
        self.assertEqual(self.row(8)['two_way']['failure']['code'],'NON_CONVERGENCE');self.assertEqual(self.row(8)['one_way']['status'],'COMPLETED')
    def test_public_export_labels(self):self.assertEqual(self.export.gate()['status'],'PASS_PUBLIC_EXPORT_GATES')
    def test_local_path_rejected(self):
        with self.assertRaises(AssertionError):self.export.check_text('Z'+':'+chr(92)+'example')
    def test_no_winner_without_old_evidence(self):self.assertTrue(all(r['winner']=='UNKNOWN' and r['legacy'] is None for r in self.saved['rows']))

if __name__=='__main__':unittest.main()
