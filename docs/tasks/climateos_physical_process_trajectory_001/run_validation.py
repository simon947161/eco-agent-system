"""Offline scoped validation. Default writes ignored output, not the archive."""
import argparse
from datetime import datetime,timezone
import hashlib, json, platform, subprocess, sys
from pathlib import Path
T=Path(__file__).resolve().parent; ROOT=T.parents[2]
sys.path.insert(0,str(ROOT))
from cczps_lite.integration import physical_process_trajectory as t

def canonical(value): return json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+'\n'
def snapshot():
    results={k:t.evaluate(dict(version=t.VERSION,example=k,authority='BOUNDED_RESEARCH_ONLY',scope='FROZEN_EVIDENCE_NO_CAUSAL_EXTRAPOLATION')) for k in ('CH4','ENSO','HYDRO','CROSS','SCORECARD')}
    results['traces']={k:t.trace(k) for k in ('CH4','ENSO','HYDRO')}
    legacy=t.atlas.end_to_end(t.atlas.load_atlas())
    results['CCZPS_ECOChain_reuse']={k:legacy[k] for k in ('scenario_interface','policy_sent_to_model','review_results','ecochain','enotebook','scientific_admission','deployed','not_inferable')}
    return results

def main():
    p=argparse.ArgumentParser(); p.add_argument('--record',action='store_true');args=p.parse_args()
    target=T/'evidence' if args.record else ROOT/'runtime_data/physical_trajectory_validation'; target.mkdir(parents=True,exist_ok=True)
    count=t.verify(); t.load()
    commands=[['-m','unittest','tests.test_physical_process_trajectory','tests.test_global_natural_systems_atlas','tests.test_scenario_comparison','tests.test_methane_knowledge_engine','-v'],
              ['-m','unittest','discover','-s','docs/tasks/climateos_global_method_evidence_ecochain_001/tests','-v'],
              ['-m','unittest','discover','-s','docs/tasks/climateos_au_landfill_methane_methods_001','-p','test_mass_balance.py','-v']]
    logs=[datetime.now(timezone.utc).isoformat(),'Python '+platform.python_version()]
    for command in commands:
        r=subprocess.run([sys.executable,'-X','utf8',*command],cwd=ROOT,text=True,encoding='utf-8',errors='replace',stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        logs += ['COMMAND: python -X utf8 '+' '.join(command),r.stdout,'EXIT_CODE: '+str(r.returncode)]
        (target/'tests.txt').write_text('\n'.join(logs),encoding='utf-8',newline='\n')
        if r.returncode: raise SystemExit(r.returncode)
    first=canonical(snapshot()); second=canonical(snapshot()); assert first==second,'NONDETERMINISTIC'
    if not args.record: assert first==(T/'evidence/end-to-end.json').read_text(encoding='utf-8'),'ARCHIVED_RESULTS_CHANGED'
    (target/'end-to-end.json').write_text(first,encoding='utf-8',newline='\n')
    for name,fn in [('A',t.radiation),('B',t.enso),('C',t.hydro),('S',t.scorecard),('legacy',t.legacy)]:
        assert fn()==t.read(T/'evidence'/('computed-'+name+'.json')), 'RESULT_DRIFT:'+name
    report={'completed_utc':datetime.now(timezone.utc).isoformat(),'python':platform.python_version(),
            'status':'LOCAL_VERIFIED','manifest_checked':count,'frozen_atlas_files_checked':t.atlas.verify_manifest(),
            'repeat_runs':2,'results_sha256':hashlib.sha256(first.encode()).hexdigest(),
            'scientific_admission':'PENDING','deployed':False,'scope':'bounded arithmetic, historical index statistics, QC and rejection paths; no field/causal admission'}
    (target/'validation.json').write_text(canonical(report),encoding='utf-8',newline='\n')
    print(canonical(report))

if __name__=='__main__': main()
