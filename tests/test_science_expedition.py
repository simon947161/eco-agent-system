"""Public teaching interface and learning-archive integrity, Issue156."""
import importlib.util,json,unittest,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('expedition_interface',ROOT/'apps/earth-science-expedition/research/interface_experiment.py')
exp=importlib.util.module_from_spec(spec);spec.loader.exec_module(exp)

class ExpeditionInterfaceTests(unittest.TestCase):
    def model(self):
        a=exp.TeachingAdapter();a.initialize();return a
    def test_three_actual_cases_reproduce_archive(self):
        result=exp.run_experiment()
        archived=json.loads((ROOT/'docs/research/world-science-expedition/evidence/interface-results.json').read_text(encoding='utf-8'))
        self.assertEqual(result,archived)
        self.assertEqual(len(result['cases']),3)
        for row in result['cases']:
            self.assertGreater(row['native_port_calls'],0)
            self.assertEqual(row['runtime_reference_status'],'COMPLETED')
            self.assertTrue(all(v==0 for v in row['max_abs_difference_by_field'].values()))
    def test_bare_port_counterexample(self):
        r=exp.run_experiment()['direct_rename_counterexample']
        self.assertTrue(r['state_unchanged']);self.assertFalse(r['committed'])
        self.assertTrue(r['water_proposal_differs']);self.assertGreater(r['clock_advanced_s'],0)
    def test_get_value_is_copy_not_alias(self):
        a=self.model();before=a.state.hash();dest=[0.,0.];out=a.get_value('water',dest);self.assertIs(out,dest);out[0]=-10
        self.assertEqual(a.state.hash(),before)
        with self.assertRaises(NotImplementedError):a.get_value_ptr('water')
    def test_fixed_clock_and_lifecycle(self):
        a=self.model();a.update_until(1800.);self.assertEqual(a.get_current_time(),1800.)
        self.assertEqual(a.get_time_units(),'s');self.assertEqual(a.get_end_time(),3600.)
        with self.assertRaisesRegex(exp.Rejection,'FRACTIONAL'):a.update_until(1900.)
        with self.assertRaisesRegex(exp.Rejection,'TARGET_TIME'):a.update_until(0.)
        a.update_until(a.get_end_time())
        with self.assertRaisesRegex(exp.Rejection,'END_TIME'):a.update()
        a.finalize()
        with self.assertRaisesRegex(exp.Rejection,'NOT_INITIALIZED'):a.get_value('water',[0.,0.])
    def test_near_integer_target_does_not_overstep(self):
        a=self.model();a.update_until(1800.+1e-10);self.assertEqual(a.get_current_time(),1800.)
    def test_set_value_validation_before_mutation(self):
        a=self.model();before=a.state.hash()
        for name,src in [('water',[0.,0.]),('rain',[-1.,0.]),('rn',[float('nan'),0.]),('rain',[1.])]:
            with self.assertRaises(exp.Rejection):a.set_value(name,src)
            self.assertEqual(a.state.hash(),before)
        a.set_value('rain',[.001,.002]);a.update();self.assertNotEqual(a.get_value('water',[0.,0.])[0],a.get_value('water',[0.,0.])[1])
    def test_metadata_are_explicit_local_subset(self):
        a=self.model();self.assertEqual(a.get_var_units('water'),'kg m-2')
        self.assertEqual(a.get_grid_shape(0,[0,0]),[1,2]);self.assertEqual(a.get_grid_x(0,[0.,0.]),[500.,1500.])
        with self.assertRaisesRegex(exp.Rejection,'UNKNOWN_VARIABLE'):a.get_var_units('soil_water_content')
        with self.assertRaisesRegex(exp.Rejection,'UNKNOWN_GRID'):a.get_grid_type(1)
    def test_update_failure_preserves_inventory_and_clock(self):
        a=exp.TeachingAdapter();a.initialize(dict(exp.defaults(),steps=4,max_iterations=1));before=a.state.hash()
        with self.assertRaisesRegex(exp.Rejection,'NON_CONVERGENCE'):a.update()
        self.assertEqual(a.state.hash(),before);self.assertEqual(a.get_current_time(),0.)

class ExpeditionArchiveTests(unittest.TestCase):
    def data(self):
        s=importlib.util.spec_from_file_location('expedition_data',ROOT/'apps/earth-science-expedition/build_data.py')
        module=importlib.util.module_from_spec(s);s.loader.exec_module(module);return module.bundle()
    def test_sources_and_claims_have_resolvable_read_boundaries(self):
        d=self.data();schema=json.loads((ROOT/'apps/earth-science-expedition/schema.json').read_text())
        sources={s['id']:s for s in d['sources']}
        self.assertEqual(len(sources),23);self.assertEqual(sum(s['evidence_status']=='BLOCKED' for s in sources.values()),5)
        for s in sources.values():
            self.assertTrue(set(schema['required'])<=s.keys())
            self.assertTrue(s['canonical_url'].startswith('https://'))
            self.assertIn(s['evidence_status'],['SOURCE_READ','BLOCKED'])
            self.assertIsNone(s['source_hash_if_legally_retained'])
        for c in d['claims']:
            self.assertTrue(c['source_ids'])
            if c['status']=='OFFICIAL_VERIFIED':self.assertTrue(any(sources[i]['evidence_status']=='SOURCE_READ' for i in c['source_ids']))
        for s in d['stations']:
            self.assertTrue(s['unknown']);self.assertTrue(s['counterexample'])
            for k in s['known']:self.assertTrue(set(k['source_ids'])<=sources.keys())
    def test_generated_browser_data_matches_canonical_research(self):
        raw=(ROOT/'apps/earth-science-expedition/data.js').read_text(encoding='utf-8')
        data=json.loads(raw.removeprefix('window.EXPEDITION_DATA = ').strip().removesuffix(';'))
        self.assertEqual(data,self.data())
        for name,key in [('SOURCE_REGISTER.json','sources'),('CLAIM_LEDGER.json','claims'),('STATION_REGISTER.json','stations')]:
            self.assertEqual(json.loads((ROOT/'docs/research/world-science-expedition'/name).read_text(encoding='utf-8')),data[key])
    def test_routes_are_learning_paths_not_admitted_causal_edges(self):
        d=self.data();ids={s['id'] for s in d['stations']}
        self.assertEqual(len(d['routes']),5);self.assertEqual(d['science'],'PENDING')
        for route in d['routes']:
            self.assertTrue(set(route['stations'])<=ids)
            for step in route['steps']:self.assertIn(step['station'],ids)
        self.assertEqual(d['experiment']['status'],'TECHNICALLY_TESTED_SUBSET')
    def test_vision_preserved_from_taskbook_branch(self):
        p='docs/research/world-science-expedition/FOUNDER_VISION_AND_DIALOGUE_20261111_ZH.md'
        # Independently read with git show at the fixed taskbook HEAD during intake.
        self.assertEqual(hashlib.sha256((ROOT/p).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
                         '908a494b16f8581080a1538d87542bbd39e37ea371ceb3f2de263da29728decf')

if __name__=='__main__':unittest.main()
