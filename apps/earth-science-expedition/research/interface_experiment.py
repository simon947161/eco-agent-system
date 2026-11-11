"""BMI-shaped teaching subset wrapping the public, atomic ClimateOS coupler.

Not an installed BMI implementation, no full BMI conformance or forecast claim.
ModelPort.step alone returns a proposal: renaming it update would be incorrect.
"""
from pathlib import Path
import sys,json,copy,hashlib,math
from dataclasses import replace
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
from cczps_lite.integration.earth_system_coupling import models as m
from cczps_lite.integration.earth_system_coupling.state import need,CATALOG,Rejection
from cczps_lite.integration.earth_system_coupling.ports import ModelPort
from cczps_lite.integration.earth_relations.coupling import CoupledPorts
from cczps_lite.integration.earth_relations.runtime import Runtime,defaults,LOCAL

class TeachingAdapter:
    """Local alias variables, seconds, fixed strip, copied values. Deliberate subset."""
    inputs=('rain','rn')
    outputs=('ta','ts','q','water','evap','runoff')
    def __init__(self):self.active=False;self.finished=False
    def initialize(self,config=None):
        need(not self.active and not self.finished,'LIFECYCLE')
        self.config=copy.deepcopy(config or dict(defaults(),steps=4))
        m.validate_config(self.config)
        need(self.config['lag_steps']==0,'ADAPTER_LAG_UNSUPPORTED')
        self.state=m.initial_state(self.config);self.ports=CoupledPorts(self.state,self.config)
        self.active=True
    def check(self):need(self.active,'NOT_INITIALIZED_OR_FINALIZED')
    def get_current_time(self):
        self.check();need(self.ports.air.current_time==self.ports.land.current_time,'CLOCK_DIVERGENCE')
        return self.ports.air.current_time
    def get_start_time(self):self.check();return 0.
    def get_end_time(self):self.check();return self.config['dt_s']*self.config['steps']
    def get_time_step(self):self.check();return self.config['dt_s']
    def get_time_units(self):self.check();return 's'
    def get_input_var_names(self):self.check();return self.inputs
    def get_output_var_names(self):self.check();return self.outputs
    def variable(self,name):self.check();need(name in self.inputs+self.outputs,'UNKNOWN_VARIABLE');return self.state.fields[name]
    def get_var_units(self,name):return self.variable(name).unit
    def get_value(self,name,dest):
        values=self.variable(name).values
        need(isinstance(dest,list) and len(dest)==len(values),'DESTINATION_SHAPE')
        dest[:]=values;return dest
    def set_value(self,name,src):
        f=self.variable(name);need(name in self.inputs,'READ_ONLY_STATE')
        need(len(src)==len(f.values),'INPUT_SHAPE')
        need(all(type(v) in (float,int) and math.isfinite(v) for v in src),'INPUT_NONFINITE')
        lo,hi=(0.,.01) if name=='rain' else (-100.,1000.)
        need(all(lo<=v<=hi for v in src),'INPUT_DOMAIN')
        self.state.put(replace(f,values=tuple(src),lineage=f.lineage+('TEACHING_INPUT_ONLY',)))
    def get_value_ptr(self,name):
        self.variable(name);raise NotImplementedError('No mutable pointer: immutable Field/evidence contract')
    def get_var_grid(self,name):self.variable(name);return 0
    def get_grid_type(self,grid):self.check();need(grid==0,'UNKNOWN_GRID');return 'uniform_rectilinear'
    def get_grid_shape(self,grid,shape):
        self.get_grid_type(grid);need(len(shape)==2,'GRID_RANK');shape[:]=[1,self.config['grid_n']];return shape
    def get_grid_x(self,grid,x):
        self.get_grid_type(grid);need(len(x)==self.config['grid_n'],'GRID_SHAPE')
        x[:]=[(a+b)/2 for a,b,_,_ in self.state.fields['water'].grid.cells];return x
    def update(self):
        t=self.get_current_time();need(t<self.get_end_time(),'END_TIME')
        cp=self.state.checkpoint();clocks=(self.ports.air.current_time,self.ports.land.current_time)
        try:
            info=self.ports.step()
            for k in LOCAL:
                f=self.state.fields[k]
                if k not in ('evap','runoff'):self.state.put(replace(f,time=m.time_window(t+self.get_time_step(),self.get_time_step())))
            return info
        except Exception:
            self.state.reset(cp);self.ports.air.kernel.reset(clocks[0]);self.ports.land.kernel.reset(clocks[1]);raise
    def update_until(self,time):
        t=self.get_current_time();dt=self.get_time_step()
        need(type(time) in (int,float) and math.isfinite(time) and t<=time<=self.get_end_time(),'TARGET_TIME')
        steps=round((time-t)/dt)
        need(abs((time-t)/dt-steps)<1e-12,'FRACTIONAL_STEP_UNSUPPORTED')
        for _ in range(steps):self.update()
    def finalize(self):self.check();self.active=False;self.finished=True

def run_experiment():
    c=dict(defaults(),steps=4)
    fixtures={'baseline':c,'hot_dry':dict(c,ta_k=305.,water_kg_m2=20.,wind_m_s=5.),
              'wet':dict(c,rain_kg_m2_s=.003,water_kg_m2=145.)}
    cases=[]
    for name,cfg in fixtures.items():
        adapter=TeachingAdapter();adapter.initialize(cfg);trace=[]
        for _ in range(cfg['steps']):
            ledger=adapter.update()
            trace.append({'time_s':adapter.get_current_time(),'fields':{k:{'unit':adapter.get_var_units(k),'values':adapter.get_value(k,[0.]*cfg['grid_n'])} for k in adapter.outputs},
                          'water_residual_kg_m2':ledger['water_residual_kg_m2'],'energy_residual_j_m2':ledger['energy_residual_j_m2']})
        direct=Runtime(cfg).run()
        differences={k:max(abs(a-b) for a,b in zip(direct['final_values'][k],adapter.get_value(k,[0.]*cfg['grid_n']))) for k in ('ta','ts','q','water')}
        need(all(v==0 for v in differences.values()),'ADAPTER_CHANGED_PHYSICS')
        cases.append({'id':name,'config':cfg,'trace':trace,'max_abs_difference_by_field':differences,'native_port_calls':adapter.ports.calls,'runtime_reference_status':direct['status']})
        adapter.finalize()
    # An actual counterexample to the tempting direct rename ModelPort.step->update.
    state=m.initial_state(c);before=state.hash();port=ModelPort(m.Surface()).initialize(state,c)
    values={k:list(f.values) for k,f in state.fields.items()}
    port.exchange=m.Atmosphere().fluxes(values,c,values,c['dt_s']);proposal=port.step(c['dt_s'])
    counter={'clock_advanced_s':port.current_time,'state_unchanged':before==state.hash(),'committed':proposal['committed'],
             'water_proposal_differs':proposal['proposal']['water']!=list(state.fields['water'].values),
             'interpretation':'Bare port advances its clock but not shared inventory; cannot be relabelled as a state-updating BMI component.'}
    files=[Path(__file__),ROOT/'cczps_lite/integration/earth_system_coupling/ports.py',ROOT/'cczps_lite/integration/earth_system_coupling/models.py',ROOT/'cczps_lite/integration/earth_relations/coupling.py',ROOT/'cczps_lite/integration/earth_relations/runtime.py']
    return {'status':'TECHNICALLY_TESTED_SUBSET','science':'PENDING','fixture_type':'SYNTHETIC_NOT_OBSERVATIONS',
            'parent_pr155':'a2863dbf3543f7e74f6b6a6a4725cb99f6fefe30','parent_pr152':'cf91e4a061341bc33d16400bcf4c6a2c2817aa65',
            'actual_cases':3,'steps_each':4,'cases':cases,'direct_rename_counterexample':counter,
            'not_implemented':['full BMI conformance','external BMI model installation','mutable value pointers','unstructured grids','fractional timesteps','real-world predictive validation'],
            'source_sha256':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest() for p in files}}

if __name__=='__main__':
    out=ROOT/'docs/research/world-science-expedition/evidence/interface-results.json'
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(run_experiment(),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('3 fixtures x 4 steps; actual ModelPorts; exact reference agreement; science PENDING')
