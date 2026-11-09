"""Reproduce approved synthetic chain, route refusals and decision-weight study."""
from pathlib import Path
import json
import sys
import time
import platform
import tracemalloc
TASK=Path(__file__).resolve().parent
sys.path.insert(0,str(TASK.parents[2]))
from cczps_lite.integration import methane_knowledge_engine as m


def main():
    request=json.loads((TASK/'input.json').read_text(encoding='utf-8'))
    out=TASK/'evidence';out.mkdir(exist_ok=True)
    def write(name,data):
        (out/name).write_text(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    tracemalloc.start();start=time.perf_counter();result=m.execute(request)
    elapsed=time.perf_counter()-start;_,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
    assert result['status']=='SYNTHETIC_ONLY',result
    write('chain-a.json',result)
    write('routes.json',[{'question':q,'result':m.execute({**request,'question':q})} for q in m.QUESTIONS])
    graph=json.loads((TASK/'MECHANISM_GRAPH.json').read_text(encoding='utf-8'))
    ids=[n['factor_id'] for n in graph['factors']]+graph['equation_nodes']
    assert len(ids)==len(set(ids))
    missing=[e for e in graph['edges'] if e['from'] not in ids or e['to'] not in ids]
    assert not missing
    write('graph-diagnostics.json',{'unique_nodes':len(ids),'edges':len(graph['edges']),'dangling_edges':missing,
          'runtime_path':result['path'],'conceptual_feedback':'E06 -> F_A04 -> E06 is unvalidated heat/decomposition hypothesis; no solver',
          'physical_breaks':['Henry equilibrium to flux missing k_L and interface','FOD inventory to pure-CH4 P2 has composition/time/boundary mismatch','emission to global response lacks transport/chemistry validation']})
    # Research-management judgement scores, never measured physical contributions.
    scores={'state_and_mass':[3,5,5,5,2,5,5],'generation_and_capture':[5,5,3,3,5,3,3],
            'water_gas_transfer':[4,4,3,3,3,3,3],'transport_chemistry':[5,4,2,2,1,1,2],
            'global_response':[5,3,1,2,1,1,1]}
    weights={'equal':[1]*7,'evidence_first':[1,1,2,3,1,1,3],'control_first':[2,2,1,1,4,1,1]}
    ranking={name:sorted([{'mechanism':k,'score':sum(a*b for a,b in zip(v,w))/sum(w)} for k,v in scores.items()],key=lambda x:(-x['score'],x['mechanism'])) for name,w in weights.items()}
    write('research-ranking.json',{'dimensions':['scope','question_relevance','observability','evidence','controllability','affordability','validation_feasibility'],
          'scale':'1 low to 5 high; author judgements grounded in SCIENCE_FOUNDATION_REALITY; not empirical effect sizes',
          'scores':scores,'weights':weights,'rankings':ranking})
    write('runtime.json',{'python':platform.python_version(),'elapsed_seconds':elapsed,'peak_python_allocated_bytes':peak,
          'scope':'execute only, not total process RSS or development time','hardware_cost':'UNKNOWN','new_dependencies':[]})
    print(json.dumps({'status':result['status'],'output':result['output'],'uncertainty':result['uncertainty'],'runtime_seconds':elapsed},ensure_ascii=True))


if __name__=='__main__':main()
