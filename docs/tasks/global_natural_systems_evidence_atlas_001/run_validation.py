"""Offline tests and deterministic query/interface replay; normal runs do not alter archive."""
import argparse
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
T=Path(__file__).resolve().parent
ROOT=T.parents[2]
sys.path.insert(0,str(ROOT))
from cczps_lite.integration import global_natural_systems_atlas as atlas

def snapshot(data):
    return {'validation':atlas.validate(data),'queries':{
      'nile_ethiopia':atlas.query(data,country='ETH',process='nile_flow'),
      'enso_australia':atlas.query(data,country='AU',process='enso'),
      'china_policy':atlas.query(data,country='CHN',evidence_type='POLICY_ASSESSMENT'),
      'malaysia_gap':atlas.query(data,country='MYS',evidence_type='POLICY_COMMITMENT'),
      'brw_2024':atlas.query(data,country='USA',system='ATM_BOUNDARY',at='2024-06-01T00:00:00Z',evidence_type='PHYSICAL_OBSERVATION'),
      'out_of_time':atlas.query(data,at='2025-01-01T00:00:00Z'),
      'methane_trace':atlas.trace(data,'CH4_SOURCE','CLIMATE_RESPONSE')},'e2e':atlas.end_to_end(data)}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--record',action='store_true');args=parser.parse_args()
    target=T/'evidence' if args.record else ROOT/'runtime_data/global_atlas_validation'
    target.mkdir(parents=True,exist_ok=True)
    data=atlas.load_atlas()
    logs=[datetime.now(timezone.utc).isoformat(),'Python '+platform.python_version()]
    commands=[['-m','unittest','tests.test_global_natural_systems_atlas','tests.test_scenario_comparison','-v'],
      ['-m','unittest','discover','-s','docs/tasks/climateos_global_method_evidence_ecochain_001/tests','-v'],
      ['-m','unittest','discover','-s','docs/tasks/climateos_au_landfill_methane_methods_001','-p','test_mass_balance.py','-v'],
      ['-m','unittest','tests.test_methane_knowledge_engine','-v']]
    for command in commands:
        result=subprocess.run([sys.executable,*command],cwd=ROOT,text=True,encoding='utf-8',errors='replace',stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        logs+=['COMMAND: python '+' '.join(command),result.stdout,'EXIT_CODE: '+str(result.returncode)]
        (target/'tests.txt').write_text('\n'.join(logs),encoding='utf-8',newline='\n')
        if result.returncode: raise SystemExit(result.returncode)
    def canonical(value): return json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+'\n'
    first=canonical(snapshot(data)); second=canonical(snapshot(data))
    assert first==second,'NONDETERMINISTIC_RESULT'
    if not args.record: assert first==(T/'evidence/query-results.json').read_text(encoding='utf-8'),'FROZEN_RESULTS_CHANGED'
    (target/'query-results.json').write_text(first,encoding='utf-8',newline='\n')
    report={'completed_at_utc':datetime.now(timezone.utc).isoformat(),'status':'LOCAL_VERIFIED','repeat_runs':2,
      'results_sha256':hashlib.sha256(first.encode()).hexdigest(),'manifest_files_checked':atlas.verify_manifest(),
      'scientific_admission':'PENDING','scope':'Metadata validation + existing internal synthetic fixtures only'}
    (target/'validation.json').write_text(canonical(report),encoding='utf-8',newline='\n')
    print(json.dumps(report))

if __name__=='__main__': main()
