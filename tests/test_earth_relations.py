"""Behavioral and independent numerical constraints for Issue154, families A-J."""
import unittest,copy,math,json,hashlib
from pathlib import Path
from dataclasses import replace
from unittest.mock import patch
from cczps_lite.integration.earth_relations.graph import sandbox_graph,Graph,Node,Edge
from cczps_lite.integration.earth_relations.runtime import Runtime,defaults,compare_scenarios
from cczps_lite.integration.earth_relations.coupling import CoupledPorts
from cczps_lite.integration.earth_system_coupling import models as m
from cczps_lite.integration.earth_system_coupling.state import Rejection

class RelationTests(unittest.TestCase):
    def config(self,**kw):return dict(defaults(),steps=3,**kw)
    def test_archive_integrity_and_source_versions(self):
        from cczps_lite.integration.earth_relations.experiments import TASK,public_hashes,comparison_metrics
        summary=json.loads((TASK/'evidence/benchmark_final/summary.json').read_text(encoding='utf-8'))
        raw=(TASK/'evidence/benchmark_final/runs.jsonl').read_bytes().replace(b'\r\n',b'\n')
        self.assertEqual(hashlib.sha256(raw).hexdigest(),summary['runs_sha256'])
        closure=json.loads((TASK/'evidence/review_closure.json').read_text(encoding='utf-8'))
        self.assertEqual(public_hashes(),closure['source_hashes'])
        self.assertEqual(summary['source_hashes'],closure['historical_source_hashes'])
        rows=[json.loads(line) for line in raw.splitlines()]
        self.assertEqual(len(rows),120)
        for row in rows:
            a,b=row['modes']['selective'],row['modes']['full_safe']
            self.assertEqual(closure['rows'][row['id']],{'id':row['id'],**comparison_metrics(a,b)})
            self.assertEqual(a['final_values'],b['final_values'])
            self.assertEqual(a['output'],b['output'])
            self.assertEqual(a['failure'],b['failure'])
            self.assertEqual(a['science'],'PENDING')
    def test_A_fork_join_shared_source(self):
        r=Runtime(self.config(),targets=('question','lag_water')).run()
        self.assertEqual(r['status'],'COMPLETED')
        self.assertEqual(r['executions']['forcing'],3);self.assertEqual(r['executions']['coupled'],3)
        self.assertEqual(len(set(r['plan']['order'])),len(r['plan']['order']))
        self.assertIn('water_hot',[e['id'] for e in r['plan']['edges'] if e['status']=='EXECUTE'])
    def test_B_actual_ports_equal_original_kernel(self):
        c=self.config();s=m.initial_state(c);p=CoupledPorts(s,c);t=m.initial_state(c)
        info=p.step();reference=m.advance(t,c,'two_way')
        for key in ('ta','ts','q','water','evap','runoff'):self.assertEqual(s.fields[key].values,t.fields[key].values)
        self.assertEqual(info['iterations'],reference['iterations']);self.assertEqual(p.calls,2*info['iterations'])
        self.assertEqual(p.air.current_time,c['dt_s']);self.assertEqual(p.land.current_time,c['dt_s'])
    def test_B_conservation_independent_inventory(self):
        c=self.config();s=m.initial_state(c);old={k:list(f.values) for k,f in s.fields.items()};info=CoupledPorts(s,c).step()
        M=c['pressure_pa']/(m.RD*c['ta_k'])*c['mixing_height_m'];dt=c['dt_s']
        for i in range(c['grid_n']):
            water=s.fields['water'].values[i]-old['water'][i]+M*(s.fields['q'].values[i]-old['q'][i])
            expected=(old['rain'][i]-s.fields['runoff'].values[i])*dt-info['vented_water_kg_m2'][i]
            self.assertAlmostEqual(water,expected,places=10)
        energy=sum(c['surface_heat_capacity']*(s.fields['ts'].values[i]-old['ts'][i])+M*m.CP*(s.fields['ta'].values[i]-old['ta'][i])+m.LV*M*(s.fields['q'].values[i]-old['q'][i]) for i in range(c['grid_n']))
        expected=sum(old['rn'])*dt+sum(info['boundary_heat_j_m2'])-m.LV*sum(info['vented_water_kg_m2'])
        self.assertAlmostEqual(energy,expected,places=5)
    def test_B_no_convergence_rollback(self):
        c=self.config(max_iterations=1);s=m.initial_state(c);before=s.hash();p=CoupledPorts(s,c)
        with self.assertRaisesRegex(Rejection,'NON_CONVERGENCE'):p.step()
        self.assertEqual(s.hash(),before);self.assertEqual(p.air.current_time,0);self.assertEqual(p.land.current_time,0)
    def test_B_unexpected_port_exception_rollback(self):
        c=self.config();s=m.initial_state(c);before=s.hash();p=CoupledPorts(s,c)
        with patch.object(p.air,'step',side_effect=RuntimeError('injected')):
            with self.assertRaises(RuntimeError):p.step()
        self.assertEqual(s.hash(),before);self.assertEqual(p.land.current_time,0)

    def test_review_pulse_nonconvergence_restores_whole_state(self):
        c=self.config(max_iterations=1,rain_kg_m2_s=.003)
        initial=m.initial_state(c);r=Runtime(c,pulse=True);result=r.run()
        self.assertEqual(result['failure']['code'],'NON_CONVERGENCE')
        self.assertEqual(r.state.inspect(),initial.inspect())
        self.assertEqual(r.state.hash(),initial.hash())
        self.assertEqual(r.ports.air.current_time,0);self.assertEqual(r.ports.land.current_time,0)
        self.assertEqual(result['rollback']['contract'],'WHOLE_STEP_BEFORE_FORCING_SYNC')
        # A subsequent physical solve starts from the restored forcing/inventories.
        r.ports.config['max_iterations']=defaults()['max_iterations']
        reference=m.initial_state(c);m.advance(reference,r.ports.config,'two_way')
        r.ports.step()
        self.assertEqual(r.state.inspect(),reference.inspect())

    def test_review_late_pulse_exception_restores_then_retry(self):
        c=self.config(rain_kg_m2_s=.003);r=Runtime(c,pulse=True)
        original=CoupledPorts.step;before=[];clocks=[]
        # Capture whole-step checkpoint before forcing, including its metadata/revision.
        original_checkpoint=m.State.checkpoint
        def checkpoint(state):
            cp=original_checkpoint(state)
            if state is r.state and r.ports and r.ports.air.current_time==2*c['dt_s'] and state.fields['ta'].time==m.time_window(2*c['dt_s'],c['dt_s']) and not before:
                before.append((cp,state.inspect(),state.hash()));clocks.append((r.ports.air.current_time,r.ports.land.current_time))
            return cp
        def fail_later(ports,lag=None):
            if ports.air.current_time==2*c['dt_s']:
                original(ports,lag)  # failure after a real physical commit must also roll back
                raise RuntimeError('injected after proposal commit')
            return original(ports,lag)
        with patch.object(m.State,'checkpoint',checkpoint),patch.object(CoupledPorts,'step',fail_later):
            with self.assertRaisesRegex(RuntimeError,'injected'):r.run()
        self.assertEqual(r.state.inspect(),before[0][1]);self.assertEqual(r.state.hash(),before[0][2])
        self.assertEqual((r.ports.air.current_time,r.ports.land.current_time),clocks[0])
        self.assertTrue(r.last_rollback['state_equal'])
        # Retry the failed dry part of the pulse versus a clean clone of the checkpoint.
        clone=m.State();clone.reset(before[0][0])
        for state in (r.state,clone):
            f=state.fields['rain'];state.put(replace(f,values=(0.,)*c['grid_n'],lineage=('SYNTHETIC_TWO_INTERVAL_PULSE',)))
        original(r.ports);m.advance(clone,c,'two_way')
        self.assertEqual(r.state.inspect(),clone.inspect())

    def test_review_differences_are_calculated_not_assumed(self):
        from cczps_lite.integration.earth_relations.experiments import comparison_metrics
        a=Runtime(self.config()).run();b=copy.deepcopy(a)
        b['final_values']['ta'][0]+=1.25;b['final_values']['water'][1]-=.5
        d=comparison_metrics(a,b)
        self.assertFalse(d['equality_asserted'])
        self.assertEqual(d['final_value_differences']['ta'],{'unit':'K','count':2,'missing_pairs':0,'max_abs_delta':1.25})
        self.assertEqual(d['final_value_differences']['water']['max_abs_delta'],.5)
        b['final_values']['q'][0]=None
        self.assertEqual(comparison_metrics(a,b)['final_value_differences']['q']['missing_pairs'],1)
        b['final_values']['q'][0]=float('nan')
        with self.assertRaisesRegex(Rejection,'DIFFERENCE_NONFINITE'):comparison_metrics(a,b)
        empty={'output':{},'final_values':{}}
        self.assertEqual(comparison_metrics(empty,empty)['numeric_status'],'NOT_COMPARABLE')
    def test_B_other_factor_cannot_borrow_ledger(self):
        g=sandbox_graph();nodes=list(g.nodes.values())+[Node('other','PHYSICAL_PROCESS','coupled')]
        edges=list(g.edges.values())+[replace(g.edges['drivers'],id='other_drivers',target='other')]
        r=Runtime(self.config(),Graph(nodes,edges),targets=('other',)).run()
        self.assertEqual(r['failure']['code'],'PHYSICAL_CLOSURE_REQUIRED')
    def test_J_context_support_cannot_be_relabelled(self):
        g=sandbox_graph();nodes=[replace(n,scope='local_area') if n.id=='CH4' else n for n in g.nodes.values()]
        with self.assertRaisesRegex(Rejection,'NODE_SUPPORT_CONTRACT'):Graph(nodes,g.edges.values())
    def test_B_never_skip_half_ledger(self):
        for name in ('evap_exchange','heat_exchange'):
            g=sandbox_graph();g=g.with_edge(replace(g.edges[name],revoked=True))
            r=Runtime(self.config(),g).run();self.assertEqual(r['failure']['code'],'PHYSICAL_CLOSURE_REQUIRED');self.assertEqual(r['native_physical_port_calls'],0)
    def test_B_zero_exchange_hand_limit(self):
        c=self.config(wind_m_s=0.,rain_kg_m2_s=0.,radiation_w_m2=0.,diffusivity_m2_s=0.)
        s=m.initial_state(c);old=s.fields.copy();CoupledPorts(s,c).step()
        for k in ('ta','ts','q','water'):self.assertEqual(s.fields[k].values,old[k].values)
    def test_C_actual_previous_water(self):
        r=Runtime(self.config(lag_steps=1),targets=('question','lag_water')).run()
        self.assertEqual(r['status'],'COMPLETED')
        self.assertEqual(r['trace'][1]['lag_water']['water'],r['trace'][0]['values']['water'])
        self.assertEqual(r['trace'][0]['lag_water']['water'],[50.,50.])
        self.assertEqual(r['trace'][1]['ledger']['port_clocks_s'],[1800.,1800.])
    def test_C_wrong_lag_and_clock(self):
        g=sandbox_graph();e=g.edges['water_hot']
        self.assertEqual(g.admission(replace(e,lag_steps=1)),'TIME_LAG_UNSUPPORTED')
        self.assertEqual(g.admission(replace(e,clock='annual')),'TIME_SUPPORT_MISMATCH')
    def test_D_unit_space_semantics(self):
        g=sandbox_graph();e=g.edges['water_hot']
        self.assertEqual(g.admission(replace(e,source_unit='mm/month')),'UNIT_CONVERSION_UNSUPPORTED')
        self.assertEqual(g.admission(replace(e,source_scope='point')),'SPATIAL_MISMATCH')
        self.assertEqual(g.admission(replace(e,source_field='unknown')),'FIELD_SEMANTICS')
    def test_E_association_cannot_be_promoted(self):
        g=sandbox_graph();e=g.edges['enso_rain_claim']
        self.assertEqual(g.admission(e),'UNSUPPORTED_NUMERIC_LINK')
        self.assertEqual(g.admission(replace(e,relation='DECLARED_PROCESS_DEPENDENCY')),'CONTEXT_CANNOT_FORCE')
        self.assertEqual(g.admission(g.edges['enso_background']),'CONTEXT_ONLY')
    def test_F_missing_and_nonfinite(self):
        r=Runtime(self.config(fault='missing_q')).run();self.assertEqual(r['failure']['code'],'MISSING_DEPENDENCY')
        self.assertTrue(r['rollback']['state_equal'])
        r=Runtime(self.config(wind_m_s=float('nan'))).run();self.assertEqual(r['failure']['code'],'CONFIG_NONFINITE')
    def test_F_no_unique_cause_inference(self):
        a=Runtime(self.config()).run();b=Runtime(self.config(wind_m_s=6.,transfer_coefficient=.001)).run()
        self.assertEqual(a['final_values'],b['final_values']);self.assertFalse(a['causal_attribution'])
    def test_G_full_safe_equivalence(self):
        for extra in (0,8):
            c=self.config();g=sandbox_graph(extra=extra)
            a=Runtime(c,g).run();b=Runtime(c,g,full=True).run()
            self.assertEqual(a['final_values'],b['final_values']);self.assertEqual(a['output'],b['output'])
            self.assertEqual(a['native_physical_port_calls'],b['native_physical_port_calls'])
            self.assertLess(a['total_node_executions'],b['total_node_executions'])
    def test_G_all_requested_no_compute_gain(self):
        g=sandbox_graph();c=self.config();targets=tuple(g.nodes)
        a=Runtime(c,g,targets).run();b=Runtime(c,g,targets,full=True).run()
        self.assertEqual(a['total_node_executions'],b['total_node_executions'])
    def test_H_shared_diamonds_no_enumeration(self):
        g=sandbox_graph(extra=0,diamond_levels=30);t=g.trace('diamond_29_a')
        self.assertLess(t['node_count'],80);self.assertEqual(t['path_count_capped'],1000000)
        self.assertFalse(t['paths_enumerated']);self.assertEqual(len(t['unique_nodes']),len(set(t['unique_nodes'])))
    def test_H_cycle_rejected(self):
        g=sandbox_graph(extra=0,diamond_levels=3)
        e=Edge('badcycle','diamond_2_a','diamond_0_a','DIAGNOSTIC_DERIVATION','value','right','1','1')
        g=Graph(g.nodes.values(),list(g.edges.values())+[e])
        with self.assertRaisesRegex(Rejection,'UNREGISTERED_CYCLE'):g.plan(('diamond_2_a',))
    def test_D_updated_edge_cannot_leave_stale_adjacency(self):
        g=sandbox_graph();g=g.with_edge(replace(g.edges['water_hot'],revoked=True))
        r=Runtime(self.config(),g).run();self.assertEqual(r['failure']['code'],'MISSING_REQUIRED_EDGE')
        with self.assertRaises(TypeError):g.edges['x']=g.edges['drivers']
    def test_H_graph_budget(self):
        with self.assertRaisesRegex(Rejection,'GRAPH_BUDGET'):sandbox_graph(extra=260)
    def test_I_joint_threshold_and_pulse(self):
        r=compare_scenarios()['runs']
        self.assertFalse(any(r['BASELINE']['output']['question']['answer']['hot_dry']))
        self.assertTrue(all(r['HEAT_DRY_WIND']['output']['question']['answer']['hot_dry']))
        self.assertTrue(all(r['RAIN_HEAT']['output']['question']['answer']['saturated']))
        self.assertNotEqual(r['RAIN_HEAT']['trace'][0]['values']['water'][0],r['RAIN_HEAT']['trace'][0]['values']['water'][1])
    def test_I_condition_suppressed(self):
        r=Runtime(self.config(),targets=('hot_detail',)).run()
        self.assertEqual(r['skips']['hot_detail'],3);self.assertNotIn('hot_detail',r['executions'])
    def test_J_context_retains_original_support(self):
        r=Runtime(self.config(),targets=('CH4','ENSO')).run()
        self.assertEqual(r['status'],'COMPLETED');self.assertEqual(r['native_physical_port_calls'],0)
        self.assertAlmostEqual(r['output']['CH4']['erf'],.569344413968403)
        self.assertEqual(r['executions'],{'CH4':1,'ENSO':1})
    def test_J_initial_source_faults(self):
        for fault,code in [('unit','UNIT_MISMATCH'),('time','TIME_MISMATCH'),('global_to_local','SPATIAL_MISMATCH'),('synthetic_as_observed','SYNTHETIC_AS_OBSERVATION')]:
            r=Runtime(self.config(fault=fault)).run();self.assertEqual(r['failure']['code'],code)

if __name__=='__main__':unittest.main()
