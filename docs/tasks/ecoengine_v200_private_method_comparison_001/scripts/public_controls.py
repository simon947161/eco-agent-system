"""PUBLIC PR152 controls only. No legacy loader, private paths or data."""
from pathlib import Path
import argparse,hashlib,json,statistics,sys,time
TASK=Path(__file__).resolve().parents[1];ROOT=TASK.parents[2];sys.path.insert(0,str(ROOT))
from cczps_lite.integration.earth_system_coupling import models as m
from cczps_lite.integration.earth_system_coupling.state import canonical
BASELINE='cf91e4a061341bc33d16400bcf4c6a2c2817aa65'

def cases():
    base=m.default_config()
    return [
      ('C01','Published nominal water/heat example',{},'REPRODUCTION'),
      ('C02','Zero wind exchange limit',{'wind_m_s':0.},'ANALYTIC_LIMIT'),
      ('C03','Dry external boundary with radiation off',{'rain_kg_m2_s':0.,'radiation_w_m2':0.,'diffusivity_m2_s':0.},'BOUNDARY_ACCOUNTING'),
      ('C04','Missing humidity',{'fault':'missing_q'},'SPARSE_DEPENDENCY'),
      ('C05','Wrong forcing interval',{'fault':'time'},'TEMPORAL_SUPPORT'),
      ('C06','Global radiation used as local forcing',{'fault':'global_to_local'},'SPATIAL_SUPPORT'),
      ('C07','Strong rain at nearly full storage',{'water_kg_m2':149.,'rain_kg_m2_s':.003},'EXTREME_BOUNDARY'),
      ('C08','One-iteration solver budget',{'max_iterations':1},'NONCONVERGENCE')]

def protocol():return {'baseline_sha':BASELINE,'science':'PENDING','evidence':'PUBLIC_SYNTHETIC_CONTROLS',
    'purpose':'fixed public side of prospective comparison; does not establish legacy equivalence',
    'case_count':8,'cases':[{'id':i,'question':q,'config':dict(m.default_config(),**change),'role':role} for i,q,change,role in cases()],
    'legacy_inputs':None,'legacy_execution':False,'common_tasks':'UNDETERMINED_UNTIL_LEGACY_IDENTITY_AND_OUTPUT_SUPPORT_VERIFIED',
    'selection_rule':'preselected public controls, no tuning against private results; retain all failures',
    'truth':'analytic zero-exchange/inventory and numerical residual checks only, no field prediction truth',
    'cost_rule':'per-side costs descriptive only; no speed winner without equivalent work; no large sweep'}

def run():
    design=json.loads((TASK/'PUBLIC_CASE_PROTOCOL.json').read_text(encoding='utf-8'));assert design==protocol()
    frozen=json.loads((ROOT/'docs/tasks/climateos_earth_system_coupling_lab_001/EXPERIMENT_RESULTS.json').read_text(encoding='utf-8'))
    for name,h in frozen['source_hashes'].items():assert hashlib.sha256((ROOT/name).read_bytes().replace(b'\r\n',b'\n')).hexdigest()==h
    started=time.perf_counter();rows=[]
    for c in design['cases']:
        outputs={};cost={}
        for strategy in m.STRATEGIES:
            t=time.perf_counter();a=m.simulate(c['config'],strategy,capture=False);elapsed=time.perf_counter()-t
            b=m.simulate(c['config'],strategy,capture=False);assert a==b
            if a['status']=='COMPLETED':assert a['max_water_residual_kg_m2']<1e-8 and a['max_energy_residual_j_m2']<1e-5
            outputs[strategy]=a;cost[strategy]=elapsed
        rows.append({'id':c['id'],'role':c['role'],'new':outputs,'new_seconds_first_execution':cost,
                     'same_seed_repeat_exact':True,'legacy':None,'paired_comparison':'NOT_EXECUTED','winner':'UNKNOWN'})
    return {'baseline_sha':BASELINE,'case_count':len(rows),'public_execution_count':48,'legacy_execution_count':0,
      'rows':rows,'total_seconds':time.perf_counter()-started,'science':'PENDING','deployed':False,
      'scope':'public new-model controls; NOT eight completed old-versus-new experiments',
      'results_only_sha256':hashlib.sha256(canonical([{k:v for k,v in r.items() if k!='new_seconds_first_execution'} for r in rows]).encode()).hexdigest()}

def main():
    p=argparse.ArgumentParser();p.add_argument('--prepare',action='store_true');p.add_argument('--output',type=Path);a=p.parse_args()
    if a.prepare:
        (TASK/'PUBLIC_CASE_PROTOCOL.json').write_text(json.dumps(protocol(),indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n');print('PUBLIC_PROTOCOL_FIXED');return
    r=run();target=a.output or ROOT/'runtime_data/issue151_public_controls.json';target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'cases':r['case_count'],'public_executions':r['public_execution_count'],'legacy_executions':0,'elapsed_seconds':r['total_seconds'],'result_hash':r['results_only_sha256']}))
if __name__=='__main__':main()
