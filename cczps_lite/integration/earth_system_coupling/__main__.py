"""Offline CLI. No service, network client or persistent agent."""
import argparse,json
from dataclasses import fields
from pathlib import Path
from .state import State,Field,Grid,TimeSupport,Rejection,canonical,need
from .models import default_config,initial_state,simulate,components,context_snapshot,STRATEGIES
from .diagnostics import compare
from .experiments import sweep

FAILURES={
 'NON_CONVERGENCE':'Rollback the attempted step; inspect dt, mixing depth, exchange coefficient, relaxation and iteration budget; do not hide failures by retuning the archived batch.',
 'DIFFUSION_CFL':'Explicit diffusion requires kappa*dt/dx^2 <= 0.5; reduce dt under a new recorded configuration.',
 'TIME_MISMATCH':'Different source support intervals cannot be treated as simultaneous forcing.',
 'MISSING_DEPENDENCY':'Only dependent local edge is blocked; annual CH4 and seasonal ENSO diagnostics remain separate.',
 'UNIT_MISMATCH':'No implicit conversion from monthly amount into instantaneous local flux.',
 'SPATIAL_MISMATCH':'Global/point/area supports require a justified mediator; global ERF is not local surface net radiation.',
 'SYNTHETIC_AS_OBSERVATION':'Simulation inputs cannot be labelled observed.',
 'ENERGY_CONSERVATION':'Check equal-and-opposite exchange, latent storage and external boundaries before accepting the step.',
 'TEMPERATURE_DOMAIN':'The idealised water-only saturation/slab model is out of its declared temperature domain.',
 'HUMIDITY_DOMAIN':'Mixed-layer humidity exceeds the declared model range; no clipping or false convergence.',
 'ATMOSPHERE_CLOCK_STABILITY':'Fast explicit relaxation substep violates its monotone stability bound.'}
def decode_state(obj):
    selected={f.name for f in fields(Field)};items=[]
    for name,raw in obj['fields'].items():
        d={k:v for k,v in raw.items() if k in selected};g=d['grid'];g['cells']=tuple(tuple(c) for c in g['cells']);d['grid']=Grid(**g);d['time']=TimeSupport(**d['time'])
        for k in ('values','uncertainty','lineage'):d[k]=tuple(d[k])
        if d.get('covariance') is not None:d['covariance']=tuple(tuple(row) for row in d['covariance'])
        need(name==d['id'],'FIELD_ID');items.append(Field(**d))
    return State(items)
def main():
    p=argparse.ArgumentParser();p.add_argument('command',choices=['validate-state','list-components','run-baseline','run-coupled','compare-scenarios','sweep-experiments','explain-failure'])
    p.add_argument('--input',type=Path);p.add_argument('--output',type=Path);p.add_argument('--strategy',choices=STRATEGIES,default='two_way');p.add_argument('--count',type=int,default=300);p.add_argument('--seed',type=int,default=20261110);p.add_argument('--seconds',type=float,default=1200);p.add_argument('--code',default='NON_CONVERGENCE');a=p.parse_args()
    try:
        if a.command=='list-components':result=components()
        elif a.command=='validate-state':
            state=decode_state(json.loads(a.input.read_text(encoding='utf-8'))) if a.input else initial_state(default_config());result={'status':'VALID_SCHEMA_NOT_SCIENTIFIC_ADMISSION','fields':len(state.fields),'hash':state.hash()}
        elif a.command=='run-baseline':result={'observational_read_only':context_snapshot(),'uncoupled_sandbox':simulate(strategy='independent')}
        elif a.command=='run-coupled':result=simulate(json.loads(a.input.read_text(encoding='utf-8')) if a.input else None,a.strategy)
        elif a.command=='compare-scenarios':result=compare()
        elif a.command=='explain-failure':need(a.code in FAILURES,'UNKNOWN_FAILURE');result={'code':a.code,'explanation':FAILURES[a.code],'scientific_admission':'PENDING'}
        else:
            result=sweep(a.count,a.seed,a.output,a.seconds)
            print(canonical({k:v for k,v in result.items() if k not in ('pairs','source_hashes')}));return
        if a.output:
            a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8',newline='\n');print(canonical({'command':a.command,'output':str(a.output)}))
        else:print(canonical(result))
    except Rejection as e:print(canonical({'status':'REJECTED','code':e.code,'detail':e.detail}));raise SystemExit(2)
if __name__=='__main__':main()
