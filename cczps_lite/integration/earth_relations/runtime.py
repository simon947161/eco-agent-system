"""Execute a dependency closure once per clock; reuse PR152 Field/State only."""
import copy, time
from dataclasses import replace
from ..earth_system_coupling import models as m
from ..earth_system_coupling.ports import ModelPort
from ..earth_system_coupling.state import Field, State, need, Rejection, digest
from .coupling import CoupledPorts
from .graph import sandbox_graph

LOCAL=('ta','ts','q','pressure','u','v','rain','rn','water','evap','runoff')

def serial(value):
    if isinstance(value,Field):return value.metadata()
    if isinstance(value,dict):return {k:serial(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [serial(v) for v in value]
    return value

def defaults():
    c=m.default_config();c.update(steps=8,ta_k=298.,water_kg_m2=50.)
    return c

class Runtime:
    def __init__(self, config=None, graph=None, targets=('question',), full=False, pulse=False):
        self.config=copy.deepcopy(defaults() if config is None else config)
        self.graph=graph or sandbox_graph(lag_steps=self.config['lag_steps'])
        self.targets=tuple(targets);self.full=full;self.pulse=pulse
        self.state=None;self.ports=None;self.events=[]

    def run(self):
        start=time.perf_counter();calls={};skips={};steps=[];failure=None;outputs={};plan=None
        peak_water=peak_energy=0.;first_hash=None;rollback=None
        try:
            m.validate_config(self.config)
            plan=self.graph.plan(self.targets,self.full,self.config['lag_steps'])
            self.state=m.initial_state(self.config)
            first_hash=self.state.hash();self.ports=CoupledPorts(self.state,self.config)
            history=[{k:list(self.state.fields[k].values) for k in ('ta','ts','q','water')}]
            context_cache={}
            for step in range(self.config['steps']):
                need(time.perf_counter()-start<120,'RUNTIME_TIME_BUDGET')
                c=self.config; t=step*c['dt_s']; outputs={};executed=[];inactive=[];info=None
                # A disclosed synthetic two-cell precipitation pulse, not observations.
                if self.pulse:
                    f=self.state.fields['rain'];amp=c['rain_kg_m2_s'] if step<2 else 0.
                    self.state.put(replace(f,values=tuple(amp*(1+.2*i) for i in range(c['grid_n'])),
                        lineage=('SYNTHETIC_TWO_INTERVAL_PULSE',)))
                cp=self.state.checkpoint();clocks=(self.ports.air.current_time,self.ports.land.current_time)
                before_hash=self.state.hash()
                try:
                    for nodeid in plan['order']:
                        node=self.graph.nodes[nodeid];op=node.operation
                        dependencies=[e for e in self.graph.incoming[nodeid] if self.graph.admission(e,c['lag_steps'])=='ACCEPTED' and e.source!=nodeid]
                        inputs={e.target_field:outputs[e.source][e.source_field] for e in dependencies}
                        if op=='detail' and not any(inputs['flag']):
                            outputs[nodeid]={'detail':None,'status':'CONDITION_FALSE'};inactive.append(nodeid);skips[nodeid]=skips.get(nodeid,0)+1;continue
                        if op.startswith('context_') and nodeid in context_cache:
                            outputs[nodeid]=context_cache[nodeid];continue
                        if op=='forcing':
                            self.state.require(('rain','rn','ta','u','q'),grid=self.state.fields['ts'].grid,time=self.state.fields['ts'].time)
                            result={'drivers':{k:self.state.fields[k] for k in ('rain','rn','ta','u','q')},'rain':self.state.fields['rain']}
                        elif op=='coupled':
                            for k,f in inputs['drivers'].items():need(f==self.state.fields[k],'STALE_DRIVER',k)
                            lag=history[max(0,len(history)-1-c['lag_steps'])] if c['lag_steps'] else None
                            info=self.ports.step(lag)
                            result={'water':self.state.fields['water'],'heat':self.state.fields['ta'],
                                    'humidity':self.state.fields['q'],'state':{k:self.state.fields[k] for k in LOCAL}}
                        elif op in ('water','heat','humidity'):result={op:inputs[op]}
                        elif op=='hotdry':result={'flag':[T>303.15 and W/c['capacity_kg_m2']<.25 for T,W in zip(inputs['heat'].values,inputs['water'].values)],'threshold':'ASSUMED_NOT_VALIDATED'}
                        elif op=='saturation':result={'flag':[W/c['capacity_kg_m2']>=.95 for W in inputs['water'].values],'threshold':'ASSUMED_NOT_VALIDATED'}
                        elif op=='question':result={'answer':{'hot_dry':inputs['hotdry'],'saturated':inputs['saturation']},'action':'NONE_RESEARCH_ONLY'}
                        elif op=='lag_water':result={'water':history[-1]['water'],'sample_end_s':t,'lag_steps':1,'warmup':step==0}
                        elif op=='detail':result={'detail':list(inputs['humidity'].values)}
                        elif op=='extra':
                            # Real cheap diagnostic queries, not sleep or padded work.
                            fields=inputs['state'];result={'summary':{'water_mean':sum(fields['water'].values)/c['grid_n'],
                                'temperature_range':max(fields['ts'].values)-min(fields['ts'].values),
                                'rain_mean':sum(inputs['rain'].values)/c['grid_n']}}
                        elif op=='identity':
                            # Do not add duplicated ancestor contributions at a diamond join.
                            result={'value':inputs['left']}
                        elif op in ('context_enso','context_ch4'):
                            context=State(m.context_state()[0].fields.values())
                            kernel=m.ENSOContext() if op=='context_enso' else m.MethaneERF()
                            port=ModelPort(kernel).initialize(context,c)
                            value=port.step(context.fields[port.required_fields[0]].time.seconds())
                            result={'enso':value['phase']} if op=='context_enso' else {'erf':value['ERF_W_m2']}
                            context_cache[nodeid]=result
                        else:raise Rejection('UNREGISTERED_OPERATION',op)
                        outputs[nodeid]=result;executed.append(nodeid);calls[nodeid]=calls.get(nodeid,0)+1
                    current={k:list(self.state.fields[k].values) for k in ('ta','ts','q','water')}
                    if info:
                        peak_water=max(peak_water,info['water_residual_kg_m2']);peak_energy=max(peak_energy,info['energy_residual_j_m2'])
                    # Ledger-bearing edges are executed by the whole atomic factor.
                    active=[x['id'] for x in plan['edges'] if x['status']=='EXECUTE' and self.graph.edges[x['id']].target not in inactive]
                    steps.append({'index':step,'start_s':t,'end_s':t+c['dt_s'],'executed_nodes':executed,
                        'inactive_nodes':inactive,'active_edges':active,'values':current,'ledger':info,
                        'question':outputs.get('question'),'lag_water':outputs.get('lag_water'),
                        'humidity_history_index':max(0,len(history)-1-c['lag_steps']) if c['lag_steps'] else None})
                    history.append(current)
                    for k in LOCAL:
                        f=self.state.fields[k]
                        if k not in ('evap','runoff'):self.state.put(replace(f,time=m.time_window(t+c['dt_s'],c['dt_s'])))
                except Exception:
                    self.state.reset(cp);self.ports.air.kernel.reset(clocks[0]);self.ports.land.kernel.reset(clocks[1])
                    rollback={'state_equal':self.state.hash()==before_hash,'port_clocks_equal':(self.ports.air.current_time,self.ports.land.current_time)==clocks,'failed_step':step}
                    raise
        except Rejection as e:failure={'code':e.code,'detail':e.detail}
        result={'status':'REJECTED' if failure else 'COMPLETED','failure':failure,
            'config':self.config,'pulse':self.pulse,'plan':plan,'graph_hash':self.graph.hash(),
            'targets':list(self.targets),'completed_steps':len(steps),'trace':steps,
            'output':{k:serial(outputs[k]) for k in self.targets if k in outputs} if not failure else {},
            'executions':calls,'skips':skips,'total_node_executions':sum(calls.values()),
            'native_physical_port_calls':self.ports.calls if self.ports else 0,
            'initial_state_hash':first_hash,'final_state_hash':self.state.hash() if self.state else None,
            'final_values':{k:list(self.state.fields[k].values) for k in ('ta','ts','q','water')} if self.state else {},
            'max_water_residual_kg_m2':peak_water,'max_energy_residual_j_m2':peak_energy,
            'rollback':rollback,'seconds':time.perf_counter()-start,
            'evidence':'SYNTHETIC_PHYSICAL_SANDBOX','science':'PENDING',
            'causal_attribution':False,'forecast_skill':None}
        return result


def compare_scenarios():
    c=defaults()
    scenarios={'BASELINE':(c,False),'HEAT_DRY_WIND':(dict(c,ta_k=305.,water_kg_m2=20.,wind_m_s=5.),False),
               'RAIN_HEAT':(dict(c,ta_k=304.,water_kg_m2=145.,rain_kg_m2_s=.003),True)}
    runs={k:Runtime(cfg,targets=('question','hot_detail','lag_water'),pulse=p).run() for k,(cfg,p) in scenarios.items()}
    base=runs['BASELINE']
    deltas={k:{f:[b-a for a,b in zip(base['final_values'][f],r['final_values'][f])] for f in base['final_values']} for k,r in runs.items()}
    return {'runs':runs,'delta_from_baseline':deltas,'interpretation':'joint synthetic scenario differences, not identified causal effects'}
