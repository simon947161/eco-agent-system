"""Independent invariants and adversarial contracts, all offline and bounded."""
import copy,json,math,random,subprocess,sys,tempfile,unittest
from dataclasses import replace
from pathlib import Path
from cczps_lite.integration.earth_system_coupling import state as s,models as m,diagnostics as d,experiments as e

class StateTests(unittest.TestCase):
    def setUp(self): self.state=m.initial_state(m.default_config());self.f=self.state.fields['water']
    def rejects(self,code,fn):
        with self.assertRaises(s.Rejection) as cm:fn()
        self.assertEqual(cm.exception.code,code)
    def test_unit(self):self.rejects('UNIT_MISMATCH',lambda:replace(self.f,unit='mm/month').validate())
    def test_nonfinite(self):self.rejects('NONFINITE',lambda:replace(self.f,values=(float('nan'),1.)).validate())
    def test_missing_preserved(self):self.assertIsNone(s.remap(replace(self.f,values=(None,60.)),s.Grid.strip(4)).values[0])
    def test_covariance_psd(self):self.rejects('COVARIANCE_NOT_PSD',lambda:s.covariance_check(((1.,2.),(2.,1.)),2))
    def test_covariance_symmetric(self):self.rejects('COVARIANCE_SYMMETRY',lambda:s.covariance_check(((1.,0.),(1.,1.)),2))
    def test_covariance_diagonal(self):self.rejects('COVARIANCE_DIAGONAL',lambda:replace(self.f,uncertainty=(1.,1.),covariance=((4.,0.),(0.,4.))).validate())
    def test_covariance_propagation(self):
        f=replace(self.f,values=(40.,60.),uncertainty=(2.,3.),covariance=((4.,3.),(3.,9.)))
        g=s.remap(f,s.Grid.strip(1));self.assertEqual(g.values,(50.,));self.assertAlmostEqual(g.covariance[0][0],19/4)
    def test_area_integral(self):
        f=replace(self.f,values=(40.,60.));g=s.remap(f,s.Grid.strip(4))
        self.assertEqual(sum(x*a for x,a in zip(f.values,f.grid.areas)),sum(x*a for x,a in zip(g.values,g.grid.areas)))
    def test_extensive_weights(self):
        weights=s.conservative_weights(s.Grid.strip(2),s.Grid.strip(4),True)
        self.assertEqual(sum(sum(w*v for w,v in zip(row,(40.,60.))) for row in weights),100.)
    def test_point_area(self):self.rejects('POINT_AREA_UNSUPPORTED',lambda:s.conservative_weights(replace(self.f.grid,support='point'),s.Grid.strip(2)))
    def test_crs_area_refusal(self):self.rejects('AREA_CRS_REQUIRES_VALIDATED_TRANSFORM',lambda:replace(self.f.grid,crs='EPSG:3857').validate())
    def test_truncated_domain(self):self.rejects('TRUNCATED_DOMAIN',lambda:s.conservative_weights(s.Grid.strip(2),s.Grid.strip(2,1000)))
    def test_overlapping(self):self.rejects('OVERLAPPING_CELLS',lambda:replace(self.f.grid,cells=((0,2,0,1),(1,3,0,1))).validate())
    def test_transform_roundtrip(self):
        x,y=s.transform_point(149.13,-36.23,'EPSG:4326','EPSG:3857');lon,lat=s.transform_point(x,y,'EPSG:3857','EPSG:4326')
        self.assertAlmostEqual(lon,149.13);self.assertAlmostEqual(lat,-36.23)
    def test_transform_domain(self):self.rejects('CRS_DOMAIN',lambda:s.transform_point(0,90,'EPSG:4326','EPSG:3857'))
    def test_naive_time(self):self.rejects('NAIVE_TIME',lambda:s.TimeSupport('2000-01-01','2000-01-02').seconds())
    def test_dst_explicit_offset(self):self.assertEqual(s.TimeSupport('2026-10-04T00:00:00+10:00','2026-10-05T00:00:00+11:00').seconds(),23*3600)
    def test_unknown_calendar(self):self.rejects('CALENDAR',lambda:replace(self.f.time,calendar='360_day').seconds())
    def test_accumulate_missing(self):
        f=replace(self.f,id='rain_amount',values=(1.,None));g=replace(f,time=m.time_window(900,900),values=(2.,3.))
        out=s.accumulate([f,g],m.time_window(0,1800));self.assertEqual(out.values,(3.,None));self.assertEqual(out.uncertainty,(None,None))
    def test_temporal_gap(self):
        f=replace(self.f,id='rain_amount');g=replace(f,time=m.time_window(1800,900))
        self.rejects('TIME_GAP_OR_OVERLAP',lambda:s.accumulate([f,g],m.time_window(0,2700)))
    def test_no_disaggregation(self):self.rejects('TIME_COVERAGE',lambda:s.accumulate([replace(self.f,id='rain_amount')],m.time_window(0,100)))
    def test_future_leakage(self):self.rejects('TIME_MISMATCH',lambda:self.state.require(['rain'],time=m.time_window(900,900)))
    def test_observation_immutable(self):
        f=replace(self.f,kind='OBSERVED_STATE',source_id='FROZEN_PUBLIC_FIXTURE',evidence_level='OPEN_DATA_RECALCULATED');state=s.State([f])
        self.rejects('OBSERVATION_IMMUTABLE',lambda:state.put(replace(f,values=(1.,2.))))
    def test_synthetic_masquerade(self):self.rejects('SYNTHETIC_AS_OBSERVATION',lambda:replace(self.f,kind='OBSERVED_STATE').validate())
    def test_hash_required(self):self.rejects('SOURCE_HASH',lambda:replace(self.f,input_sha256='unverified').validate())
    def test_sparse_independence(self):
        self.state.put(replace(self.state.fields['q'],values=(None,None)))
        self.state.require(['water']);self.rejects('MISSING_DEPENDENCY',lambda:self.state.require(['q']))
    def test_snapshot(self):
        cp=self.state.checkpoint();h=self.state.hash();self.state.put(replace(self.f,values=(1.,2.)));self.state.reset(cp);self.assertEqual(self.state.hash(),h)
    def test_reversible_difference(self):
        b=s.State(self.state.fields.values());b.put(replace(self.f,values=(1.,2.)));patch=s.difference(self.state,b)
        c=s.apply_difference(self.state,patch);self.assertEqual(c.hash(),b.hash());self.assertEqual(s.apply_difference(c,patch,True).hash(),self.state.hash())
    def test_wrong_patch_base(self):
        b=s.State(self.state.fields.values());b.put(replace(self.f,values=(1.,2.)));patch=s.difference(self.state,b)
        self.rejects('DIFFERENCE_BASE_HASH',lambda:s.apply_difference(b,patch))

class PhysicsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.diag=d.compare()
    def test_four_components(self):self.assertEqual(len(m.components()),4)
    def test_saturation_official_example(self):
        # FAO56 example: es(24.5 C)=3.075 kPa, rounded published value.
        q=m.saturation(297.65,100000);e=q*100000/(.622+.378*q);self.assertAlmostEqual(e/1000,3.075,places=3)
    def test_water_conservation(self):
        for run in self.diag['runs'].values():self.assertLess(run['max_water_residual_kg_m2'],1e-8)
    def test_energy_conservation(self):
        for run in self.diag['runs'].values():self.assertLess(run['max_energy_residual_j_m2'],1e-5)
    def test_independent_analytic_inventory(self):
        r=self.diag['runs']['independent'];c=r['config'];self.assertAlmostEqual(r['final_values']['water'][0],c['water_kg_m2']+c['rain_kg_m2_s']*c['dt_s']*c['steps'])
    def test_no_rain_multiplication_by_iterations(self):
        c=dict(m.default_config(),wind_m_s=0.);r=m.simulate(c);self.assertEqual(r['status'],'COMPLETED')
        self.assertAlmostEqual(r['final_values']['water'][0],50.432,places=9)
    def test_zero_wind_equal_strategies(self):
        runs=[m.simulate(dict(m.default_config(),wind_m_s=0),x) for x in m.STRATEGIES]
        self.assertTrue(all(r['evaporation_kg_m2']==0 for r in runs));self.assertEqual(runs[0]['final_values'],runs[2]['final_values'])
    def test_air_feedback_suppresses_evaporation_in_fixed_case(self):self.assertLess(self.diag['runs']['two_way']['evaporation_kg_m2'],self.diag['runs']['one_way']['evaporation_kg_m2'])
    def test_joint_threshold(self):self.assertEqual({k:v['hot_dry_exceeded'] for k,v in self.diag['joint_scenarios'].items()},{'baseline':False,'heat_only':False,'dry_only':False,'joint_heat_dry':True})
    def test_rain_overflow(self):
        c=dict(m.default_config(),water_kg_m2=149.,rain_kg_m2_s=.003);r=m.simulate(c,'independent')
        self.assertAlmostEqual(r['runoff_kg_m2'],.003*21600-1);self.assertEqual(r['final_values']['water'],[150.,150.])
    def test_iteration_failure_atomic(self):
        c=dict(m.default_config(),max_iterations=1);st=m.initial_state(c);h=st.hash()
        with self.assertRaises(s.Rejection) as cm:m.advance(st,c,'two_way')
        self.assertEqual(cm.exception.code,'NON_CONVERGENCE');self.assertEqual(st.hash(),h)
    def test_clock_failure_no_partial_step(self):
        r=m.simulate(dict(m.default_config(),relaxation_time_s=1))
        self.assertEqual(r['failure']['code'],'ATMOSPHERE_CLOCK_STABILITY');self.assertEqual(r['initial_state_hash'],r['final_state_hash'])
    def test_initialization_failure_distinguished(self):self.assertFalse(m.simulate(dict(m.default_config(),fault='unit'))['failure']['rolled_back_failed_step'])
    def test_missing_local_keeps_global(self):
        r=m.simulate(dict(m.default_config(),fault='missing_q'));self.assertEqual(r['failure']['code'],'MISSING_DEPENDENCY')
        self.assertAlmostEqual(r['independent_slow_context']['outputs']['global_methane_erf']['ERF_W_m2'],.569344413968403)
    def test_global_to_local_rejected(self):self.assertEqual(m.simulate(dict(m.default_config(),fault='global_to_local'))['failure']['code'],'SPATIAL_MISMATCH')
    def test_slow_support_not_advanced(self):
        r=self.diag['runs']['two_way'];f=r['final_shared_state']['fields'];self.assertEqual(f['ch4']['time']['start'],'2025-01-01T00:00:00Z');self.assertEqual(f['roni']['time']['start'],'2012-09-01T00:00:00Z')
    def test_context_cannot_be_hourly(self):
        st,_,_=m.context_state();st=s.State(st.fields.values());a=m.ENSOContext().initialize(st)
        with self.assertRaises(s.Rejection):a.step(st,3600)
    def test_component_reset_clock(self):
        a=m.Atmosphere().initialize(m.initial_state(m.default_config()));cp=a.checkpoint();a.current_time=900.;a.reset(cp);self.assertEqual(a.current_time,0)
    def test_four_grid_gradient(self):self.assertEqual(len(self.diag['mediation']['temperature_gradient_K_m']),4)
    def test_gradient_linear(self):self.assertEqual(d.gradient([1.,3.,5.,7.],2),[1.]*4)
    def test_divergence_global_zero(self):self.assertAlmostEqual(sum(d.divergence([0.,10.,0.,-10.,0.],500))*500,0)
    def test_tendency(self):self.assertEqual(d.tendency([1.,3.],[3.,7.],2),[1.,2.])
    def test_space_order_two(self):
        err=[x['rms_error'] for x in self.diag['space_manufactured']];self.assertTrue(all(3.8<a/b<4.2 for a,b in zip(err,err[1:])))
    def test_time_order_one(self):
        err=[x['amplitude_error'] for x in self.diag['time_semidiscrete']];self.assertTrue(all(1.9<a/b<2.1 for a,b in zip(err,err[1:])))
    def test_coupled_dt_convergence(self):
        a,b,c=[x['final_ts_K'] for x in self.diag['dt_halving']];self.assertLess(abs(b-c),abs(a-b))
    def test_cfl_rejection(self):
        with self.assertRaises(s.Rejection):d.diffusion(32,100.)
    def test_parameter_nonidentifiability(self):self.assertEqual(self.diag['identifiability']['max_final_difference'],0.)
    def test_covariance_changes_output_spread(self):self.assertNotEqual(*[x['sd_evap_kg_m2'] for x in self.diag['uncertainty_ensembles']])
    def test_no_prediction_or_admission(self):
        r=self.diag['runs']['two_way'];self.assertIsNone(r['forecast_skill']);self.assertFalse(r['causal_real_world_validation']);self.assertEqual(r['scientific_admission'],'PENDING')

class RunnerTests(unittest.TestCase):
    def test_uniform_ports_all_four_execute(self):
        from cczps_lite.integration.earth_system_coupling.ports import demonstrate
        out=demonstrate();self.assertEqual(len(out),4);self.assertEqual(out['seasonal_enso_context']['grid'],'RONI')
        self.assertFalse(out['surface_water_and_energy']['output']['committed'])
    def test_uniform_port_missing_exchange_rolls_back(self):
        from cczps_lite.integration.earth_system_coupling.ports import ModelPort
        state=m.initial_state(m.default_config());port=ModelPort(m.Surface()).initialize(state);h=state.hash()
        with self.assertRaises(s.Rejection):port.step(900)
        self.assertEqual(state.hash(),h);self.assertEqual(port.current_time,0)
    def test_families_not_confounded_with_grids_clocks(self):
        seen={k:set() for k in e.FAMILIES};rng=random.Random(1)
        for i in range(72):family,c=e.scenario(i,rng);seen[family].add((c['grid_n'],c['dt_s']))
        self.assertTrue(all(len(x)==6 for x in seen.values()))
    def test_seed_replay_and_different_seed(self):
        with tempfile.TemporaryDirectory(dir=m.ROOT/'runtime_data') as t:
            a=e.sweep(36,91,Path(t)/'a');b=e.sweep(36,91,Path(t)/'b');c=e.sweep(36,92,Path(t)/'c')
            self.assertEqual(a['runs_sha256'],b['runs_sha256']);self.assertNotEqual(a['runs_sha256'],c['runs_sha256']);self.assertEqual(a['unique_config_strategy_hashes'],36)
    def test_budget_early_stop(self):
        with tempfile.TemporaryDirectory(dir=m.ROOT/'runtime_data') as t:
            r=e.sweep(300,1,t,max_bytes=1);self.assertEqual(r['completed_runs'],0);self.assertEqual(r['early_stop'],'OUTPUT_BYTE_BUDGET')
    def test_run_count_guard(self):
        with self.assertRaises(s.Rejection):e.sweep(100001)
    def test_all_seven_cli_commands(self):
        with tempfile.TemporaryDirectory(dir=m.ROOT/'runtime_data') as t:
            for command in ('validate-state','list-components','run-baseline','run-coupled','compare-scenarios','sweep-experiments','explain-failure'):
                args=[sys.executable,'-X','utf8','-m','cczps_lite.integration.earth_system_coupling',command,'--count','3','--output',str(Path(t)/(command if command=='sweep-experiments' else command+'.json'))]
                p=subprocess.run(args,cwd=m.ROOT,capture_output=True,text=True,encoding='utf-8');self.assertEqual(p.returncode,0,p.stderr+p.stdout)
    @classmethod
    def setUpClass(cls):(m.ROOT/'runtime_data').mkdir(exist_ok=True)

if __name__=='__main__':unittest.main()
