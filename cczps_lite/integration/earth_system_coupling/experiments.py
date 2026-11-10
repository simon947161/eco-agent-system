"""Finite, seeded paired-strategy experiments with real resource receipts."""
import csv,hashlib,json,math,random,statistics,time
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path
from . import VERSION
from .state import canonical,digest,need
from .models import TASK,ROOT,STRATEGIES,default_config,simulate

FAMILIES=('nominal','heat_dry','rain_pulse','zero_wind','lagged','stiff','missing_q','unit','time','iteration_limit','synthetic_as_observed','global_to_local')
def scenario(index,rng,correlation=-.6):
    c=default_config();z=rng.gauss(0,1);z2=correlation*z+math.sqrt(1-correlation**2)*rng.gauss(0,1)
    # Balance grid and clock within each family; do not confound them with family ID.
    block=index//len(FAMILIES)
    c.update(grid_n=2 if block%2==0 else 4,dt_s=(450.,900.,1800.)[block%3],ta_k=min(314.,max(286.,300+5*z)),
        q_kgkg=min(.018,max(.002,.010+.003*z2)),wind_m_s=rng.uniform(.2,10),water_kg_m2=rng.uniform(15,120),
        radiation_w_m2=rng.uniform(50,400),rain_kg_m2_s=rng.uniform(0,5e-5),surface_heat_capacity=rng.uniform(1e6,3e6),
        mixing_height_m=rng.uniform(60,180),transfer_coefficient=rng.uniform(.0005,.004),diffusivity_m2_s=rng.uniform(0,2))
    c['steps']=int(21600/c['dt_s']);family=FAMILIES[index%len(FAMILIES)]
    if family=='heat_dry':c.update(ta_k=rng.uniform(303,314),water_kg_m2=rng.uniform(5,30),q_kgkg=.003)
    elif family=='rain_pulse':c.update(rain_kg_m2_s=rng.uniform(.001,.004),water_kg_m2=rng.uniform(120,149))
    elif family=='zero_wind':c['wind_m_s']=0.
    elif family=='lagged':c['lag_steps']=1+index%4
    elif family=='stiff':c.update(diffusivity_m2_s=1000.)
    elif family=='iteration_limit':c.update(max_iterations=1)
    elif family in ('missing_q','unit','time','synthetic_as_observed','global_to_local'):c['fault']=family
    return family,c

def code_hashes():
    paths=sorted(Path(__file__).parent.glob('*.py'))
    return {p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest() for p in paths}
def sweep(count=300,seed=20261110,output=None,seconds=1200.,max_bytes=200_000_000,correlation=-.6):
    need(type(count) is int and 1<=count<=100000,'RUN_COUNT_BUDGET');need(0<seconds<=1200 and 0<max_bytes<=200_000_000,'RESOURCE_BUDGET')
    need(-1<correlation<1,'COVARIANCE_NOT_PSD')
    if output is None:output=ROOT/'runtime_data/earth_coupling'/f'seed-{seed}'
    output=Path(output).resolve();need(output.is_relative_to(ROOT),'OUTPUT_OUTSIDE_WORKSPACE');output.mkdir(parents=True,exist_ok=True)
    rng=random.Random(seed);started=time.monotonic();start_utc=datetime.now(timezone.utc).isoformat();hashes=code_hashes();plan_hash=hashlib.sha256((TASK/'PRE_RUN_PROTOCOL.md').read_bytes()).hexdigest()
    fingerprint=hashlib.sha256();counts=Counter();groups={s:Counter() for s in STRATEGIES};ids=set();family_counts=Counter();nbytes=0;completed=0;stopped=None;paired=[];parameters=[];max_water=max_energy=0.;paircache={};rawfile=output/'runs.jsonl'
    with rawfile.open('wb') as f:
        for i in range(count):
            if time.monotonic()-started>=seconds:stopped='WALL_TIME_BUDGET';break
            if i%3==0:family,c=scenario(i//3,rng,correlation);parameters.append((c['ta_k'],c['q_kgkg']));paircache={}
            strategy=STRATEGIES[i%3];r=simulate(c,strategy,capture=False)
            row={k:v for k,v in r.items() if k not in ('trace','final_shared_state','components')}
            row.update(run_id=i,scenario_id=i//3,family=family,seed=seed)
            payload=(canonical(row)+'\n').encode()
            if nbytes+len(payload)>max_bytes:stopped='OUTPUT_BYTE_BUDGET';break
            f.write(payload);fingerprint.update(payload);nbytes+=len(payload);completed+=1;ids.add(r['config_hash']);family_counts[family]+=1
            status=r['failure']['code'] if r['failure'] else 'COMPLETED';counts[status]+=1;groups[strategy][status]+=1;paircache[strategy]=r
            max_water=max(max_water,r['max_water_residual_kg_m2']);max_energy=max(max_energy,r['max_energy_residual_j_m2'])
            if r['status']=='COMPLETED':groups[strategy]['threshold_exceeded']+=int(bool(r['hot_dry_exceeded']))
            if i%3==2:
                p={'scenario_id':i//3,'family':family,'statuses':{k:v['status'] for k,v in paircache.items()}}
                if all(v['status']=='COMPLETED' for v in paircache.values()):
                    p['two_minus_one_evap_kg_m2']=paircache['two_way']['evaporation_kg_m2']-paircache['one_way']['evaporation_kg_m2']
                    p['two_minus_independent_ts_K']=statistics.mean(paircache['two_way']['final_values']['ts'])-statistics.mean(paircache['independent']['final_values']['ts'])
                paired.append(p)
    elapsed=time.monotonic()-started
    corr=None
    if len(parameters)>1:
        a,b=zip(*parameters);am,bm=statistics.mean(a),statistics.mean(b);den=math.sqrt(sum((x-am)**2 for x in a)*sum((x-bm)**2 for x in b));corr=sum((x-am)*(y-bm) for x,y in parameters)/den if den else None
    summary={'model_version':VERSION,'seed':seed,'requested':count,'completed_runs':completed,'unique_config_strategy_hashes':len(ids),'scenario_count':len(parameters),
        'strategy_counts':{k:dict(v) for k,v in groups.items()},'failure_distribution':dict(counts),'family_counts':dict(family_counts),
        'started_utc':start_utc,'elapsed_seconds':elapsed,'seconds_per_run':elapsed/completed if completed else None,'output_bytes':nbytes,
        'budget':{'seconds':seconds,'bytes':max_bytes,'max_steps':96,'max_iterations':80},'early_stop':stopped,
        'runs_sha256':fingerprint.hexdigest(),'source_hashes':hashes,'pre_run_protocol_sha256':plan_hash,
        'max_water_residual_kg_m2':max_water,'max_energy_residual_j_m2':max_energy,
        'requested_input_correlation':correlation,'actual_all_family_T_q_correlation':corr,
        'correlation_note':'nominal Gaussian draws correlated; clipping and designed edge families alter whole-matrix correlation',
        'pairs':paired,'evidence_class':'SYNTHETIC_MODEL_EXPERIMENT','scientific_admission':'PENDING',
        'interpretation':'algorithm frequency over declared design, not 10000 independent field experiments or real hazard probability'}
    (output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8',newline='\n')
    with (output/'summary.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.writer(f);writer.writerow(['strategy','outcome','count'])
        for s,v in groups.items():
            for k,n in sorted(v.items()):writer.writerow([s,k,n])
    return summary
