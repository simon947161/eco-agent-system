"""python -m cczps_lite.integration.earth_relations --help"""
import argparse,json
from pathlib import Path
from .graph import sandbox_graph
from .runtime import Runtime,compare_scenarios,defaults
from .experiments import sweep,ROOT

def main():
    p=argparse.ArgumentParser();p.add_argument('command',choices=['inspect-relations','plan-subgraph','run-graph','compare-scenarios','trace-influences','audit-failures','benchmark'])
    p.add_argument('--targets',default='question');p.add_argument('--full',action='store_true');p.add_argument('--output');p.add_argument('--lag',type=int,default=0);p.add_argument('--diamonds',type=int,default=0)
    a=p.parse_args();c=defaults();c['lag_steps']=a.lag;g=sandbox_graph(lag_steps=a.lag,diamond_levels=a.diamonds);targets=tuple(a.targets.split(','))
    if a.command=='inspect-relations':r={**g.inspect_raw(),'admission':{e.id:g.admission(e,a.lag) for e in g.edges.values()}}
    elif a.command=='plan-subgraph':r=g.plan(targets,a.full,a.lag)
    elif a.command=='run-graph':r=Runtime(c,g,targets,a.full).run()
    elif a.command=='compare-scenarios':r=compare_scenarios()
    elif a.command=='trace-influences':r=g.trace(targets[0],a.lag)
    elif a.command=='audit-failures':
        r={'links':[{'id':e.id,'reason':g.admission(e,a.lag)} for e in g.edges.values() if g.admission(e,a.lag)!='ACCEPTED'],
           'runtime':{fault:Runtime(dict(c,fault=fault)).run()['failure'] for fault in ('missing_q','unit','time','global_to_local')}}
    else:r=sweep(a.output or ROOT/'runtime_data/earth_relations/benchmark')
    text=json.dumps(r,ensure_ascii=False,indent=2,allow_nan=False)+'\n'
    if a.output and a.command!='benchmark':
        out=Path(a.output).resolve()
        if not out.is_relative_to(ROOT):p.error('output must stay in public workspace')
        out.parent.mkdir(parents=True,exist_ok=True);out.write_text(text,encoding='utf-8')
        print(json.dumps({'output':out.relative_to(ROOT).as_posix(),'status':r.get('status','WRITTEN')}))
    elif a.command=='benchmark':print(json.dumps({k:v for k,v in r.items() if k!='rows'},indent=2))
    else:print(text)
if __name__=='__main__':main()
