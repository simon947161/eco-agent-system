"""Preregistered, bounded structural comparison. No downloads or real predictions."""
from pathlib import Path
import csv,json,time,random,hashlib,statistics,collections
from dataclasses import replace
from . import BASELINE,VERSION
from .runtime import Runtime,defaults,compare_scenarios
from .graph import sandbox_graph
from ..earth_system_coupling.state import need,digest
ROOT=Path(__file__).resolve().parents[3]
TASK=ROOT/'docs/tasks/climateos_adaptive_earth_relations_runtime_001'
FAMILIES=('nominal','heat_dry','rain_pulse','zero_wind','lagged','missing_q','unit','time','global_to_local','iteration_limit','stiff','revoked')

def configs(count,seed):
    rng=random.Random(seed)
    for i in range(count):
        family=FAMILIES[i%len(FAMILIES)];block=i//len(FAMILIES);c=defaults()
        c.update(steps=4+block%3,grid_n=2 if block%2==0 else 4,dt_s=(450.,900.)[block%2],
                 ta_k=rng.uniform(294,302),wind_m_s=rng.uniform(1,5),water_kg_m2=rng.uniform(35,90),radiation_w_m2=rng.uniform(100,300))
        if family=='heat_dry':c.update(ta_k=305.,water_kg_m2=20.)
        if family=='rain_pulse':c.update(water_kg_m2=145.,rain_kg_m2_s=.003)
        if family=='zero_wind':c['wind_m_s']=0.
        if family=='lagged':c['lag_steps']=1+block%3
        if family in ('missing_q','unit','time','global_to_local'):c['fault']=family
        if family=='iteration_limit':c['max_iterations']=1
        if family=='stiff':c['diffusivity_m2_s']=10000.
        levels=block%4;g=sandbox_graph(extra=(0,6,18)[block%3],lag_steps=c['lag_steps'],diamond_levels=levels)
        if family=='revoked':g=g.with_edge(replace(g.edges['evap_exchange'],revoked=True))
        target=(f'diamond_{levels-1}_a',) if levels else ('question',)
        yield i,family,c,g,target,family=='rain_pulse'

def scientific_record(r):
    return {k:v for k,v in r.items() if k!='seconds'}

def public_hashes():
    paths=list(Path(__file__).parent.glob('*.py'))+[ROOT/'cczps_lite/integration/earth_system_coupling/models.py']
    return {p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest() for p in sorted(paths)}

def sweep(output,count=120,seed=15420261111,repeats=3):
    need(type(count) is int and 100<=count<=1000,'CONFIG_BUDGET')
    need(repeats==3,'REPEAT_PROTOCOL')
    out=Path(output).resolve();need(out.is_relative_to(ROOT),'OUTPUT_OUTSIDE_WORKSPACE');out.mkdir(parents=True,exist_ok=True)
    protocol=json.loads((TASK/'EXPERIMENT_PROTOCOL.json').read_text(encoding='utf-8'))
    need(count==protocol['configurations'] and seed==protocol['seed'],'PROTOCOL_MISMATCH')
    Runtime().run() # disclosed cache warmup, excluded from benchmark counters
    start=time.perf_counter();rows=[];summaries=[];failures=collections.Counter();raw_bytes=0;stopped=None
    with (out/'runs.jsonl').open('wb') as f:
        for i,family,c,g,target,pulse in configs(count,seed):
            if time.perf_counter()-start>protocol['wall_seconds']:stopped='WALL_BUDGET';break
            pair={};times={'selective':[],'full_safe':[]};hashes={}
            for repeat in range(repeats):
                modes=('selective','full_safe') if (i+repeat)%2==0 else ('full_safe','selective')
                for mode in modes:
                    r=Runtime(c,g,target,full=mode=='full_safe',pulse=pulse).run()
                    h=digest(scientific_record(r));need(mode not in hashes or hashes[mode]==h,'REPLAY_MISMATCH');hashes[mode]=h
                    times[mode].append(r['seconds']);pair[mode]=r
            a,b=pair['selective'],pair['full_safe']
            need(a['status']==b['status'] and a['failure']==b['failure'],'STATUS_MISMATCH')
            need(a['output']==b['output'] and a['final_values']==b['final_values'],'SELECTIVE_RESULT_MISMATCH')
            record={'id':i,'family':family,'config':c,'graph':g.inspect_raw(),'targets':target,'pulse':pulse,
                    'modes':{k:scientific_record(v) for k,v in pair.items()},'timing_seconds':times,'replay_hashes':hashes}
            payload=(json.dumps(record,sort_keys=True,allow_nan=False)+'\n').encode()
            if raw_bytes+len(payload)>protocol['archive_max_bytes']:stopped='ARCHIVE_BUDGET';break
            f.write(payload);raw_bytes+=len(payload)
            code=a['failure']['code'] if a['failure'] else 'COMPLETED';failures[code]+=1
            row={'id':i,'family':family,'status':code,'graph_nodes':len(g.nodes),'graph_edges':len(g.edges),
                 'selected_nodes':len(a['plan']['selected_nodes']) if a['plan'] else 0,
                 'selective_executions':a['total_node_executions'],'full_executions':b['total_node_executions'],
                 'port_calls_each':a['native_physical_port_calls'],'max_output_delta':0.,
                 'selective_seconds_median':statistics.median(times['selective']),
                 'full_seconds_median':statistics.median(times['full_safe']),
                 'water_residual':a['max_water_residual_kg_m2'],'energy_residual':a['max_energy_residual_j_m2']}
            rows.append(row)
    with (out/'runs.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    done=[r for r in rows if r['status']=='COMPLETED']
    ratios=[r['selective_seconds_median']/r['full_seconds_median'] for r in done]
    # Counterexample: requesting every result removes any pruning benefit.
    g=sandbox_graph(extra=6);targets=tuple(g.nodes);c=defaults()
    all_a=Runtime(c,g,targets).run();all_b=Runtime(c,g,targets,full=True).run()
    results={'version':VERSION,'baseline':BASELINE,'protocol_sha256':digest(protocol),'seed':seed,
        'unique_configurations':len(rows),'paired_modes':2,'repetitions_per_mode':repeats,'actual_runtime_invocations':len(rows)*2*repeats,
        'warmup_invocations_excluded':1,'all_targets_counterexample_invocations_excluded':2,
        'source_hashes':public_hashes(),'elapsed_seconds':time.perf_counter()-start,'archive_bytes':raw_bytes,
        'early_stop':stopped,'failure_distribution':dict(failures),'completed_configurations':len(done),
        'max_output_delta':max(r['max_output_delta'] for r in rows),
        'max_water_residual_kg_m2':max(r['water_residual'] for r in rows),
        'max_energy_residual_j_m2':max(r['energy_residual'] for r in rows),
        'completed_node_executions':{'selective':sum(r['selective_executions'] for r in done),'full_safe':sum(r['full_executions'] for r in done)},
        'completed_physical_port_calls_each_mode':sum(r['port_calls_each'] for r in done),
        'median_selective_to_full_time_ratio':statistics.median(ratios),
        'min_max_time_ratio':[min(ratios),max(ratios)],'selective_slower_configurations':sum(x>1 for x in ratios),
        'timing_uncertainty':'three alternating-order repetitions; min/max across configs; no portable speed claim or statistical CI',
        'all_targets_counterexample':{'selective_nodes':all_a['total_node_executions'],'full_nodes':all_b['total_node_executions'],
            'output_equal':all_a['output']==all_b['output'],'selective_seconds':all_a['seconds'],'full_seconds':all_b['seconds']},
        'rows':rows,'evidence':'SYNTHETIC_PHYSICAL_SANDBOX','scientific_admission':'PENDING'}
    results['runs_sha256']=hashlib.sha256((out/'runs.jsonl').read_bytes()).hexdigest()
    (out/'summary.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return results
