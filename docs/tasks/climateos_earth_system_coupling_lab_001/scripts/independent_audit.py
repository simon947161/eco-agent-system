"""Read saved numbers only; independent whole-domain inventory reconstruction."""
from pathlib import Path
import collections,hashlib,json,statistics
TASK=Path(__file__).resolve().parents[1]
def audit():
    read=lambda p:json.loads(p.read_text(encoding='utf-8'))
    summary=read(TASK/'EXPERIMENT_RESULTS.json');raw=(TASK/'evidence/main/runs.jsonl').read_bytes()
    assert hashlib.sha256(raw).hexdigest()==summary['runs_sha256']
    rows=[json.loads(line) for line in raw.splitlines()];assert len(rows)==summary['completed_runs']==10008
    assert len({r['config_hash'] for r in rows})==10008
    counts=collections.Counter(r['failure']['code'] if r['failure'] else 'COMPLETED' for r in rows)
    assert dict(counts)==summary['failure_distribution'];assert all(r['scientific_admission']=='PENDING' for r in rows)
    for i in range(0,len(rows),3):
        triple=rows[i:i+3];assert len({json.dumps(r['config'],sort_keys=True) for r in triple})==1
        assert {r['strategy'] for r in triple}=={'independent','one_way','two_way'}
    # Check each family's grid/step coverage rather than assuming randomization.
    designs={k:{(r['config']['grid_n'],r['config']['dt_s']) for r in rows if r['family']==k} for k in summary['family_counts']}
    assert all(len(v)==6 for v in designs.values())
    diag=read(TASK/'evidence/diagnostics.json');r=diag['runs']['two_way'];c=r['config'];mean=statistics.mean
    mass=c['pressure_pa']/(287.05*c['ta_k'])*c['mixing_height_m'];capacity=1004*mass;wr=[];er=[]
    for before,after in zip(r['trace'],r['trace'][1:]):
        a,b=before['values'],after['values'];ledger=after['ledger'];dt=after['elapsed_s']-before['elapsed_s']
        change=mean(b['water'])-mean(a['water'])+mass*(mean(b['q'])-mean(a['q']))
        external=c['rain_kg_m2_s']*dt-ledger['runoff_kg_m2']-mean(ledger['vented_water_kg_m2']);wr.append(change-external)
        enthalpy=c['surface_heat_capacity']*(mean(b['ts'])-mean(a['ts']))+capacity*(mean(b['ta'])-mean(a['ta']))+2.45e6*mass*(mean(b['q'])-mean(a['q']))
        boundary=c['radiation_w_m2']*dt+mean(ledger['boundary_heat_j_m2'])-2.45e6*mean(ledger['vented_water_kg_m2']);er.append(enthalpy-boundary)
    assert max(map(abs,wr))<1e-8 and max(map(abs,er))<1e-5
    assert diag['mediation']['area_integral_before']==diag['mediation']['area_integral_after']
    assert diag['mediation']['round_trip_hash_equal']
    assert {k:v['hot_dry_exceeded'] for k,v in diag['joint_scenarios'].items()}=={'baseline':False,'heat_only':False,'dry_only':False,'joint_heat_dry':True}
    return {'status':'PASS','main_rows':len(rows),'unique_configs_with_strategy':len({r['config_hash'] for r in rows}),'counts':dict(counts),
            'whole_domain_max_water_residual_kg_m2':max(map(abs,wr)),'whole_domain_max_energy_residual_j_m2':max(map(abs,er)),
            'six_grid_clock_combinations_per_family':True,'method':'independent inventory differences from saved trajectory; no coupling runtime import','science':'PENDING'}
if __name__=='__main__':print(json.dumps(audit(),indent=2))
