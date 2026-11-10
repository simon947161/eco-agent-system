"""Offline archive verification. --record freezes a manifest; no simulations."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,re,sys
TASK=Path(__file__).resolve().parents[1];ROOT=TASK.parents[2];sys.path.insert(0,str(ROOT))
from cczps_lite.integration.earth_system_coupling import experiments as e,models as m
from independent_audit import audit
EXCLUDED={'manifest.json','validation.json','HANDOFF_STATUS.json','REVIEW_REQUEST.json'}
def data(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):
    raw=p.read_bytes();mode='bytes' if p.suffix in ('.jsonl','.png') else 'LF'
    return {'sha256':hashlib.sha256(raw if mode=='bytes' else raw.replace(b'\r\n',b'\n')).hexdigest(),'hash_mode':mode,'bytes':len(raw)}
def paths():
    files=[p for p in TASK.rglob('*') if p.is_file() and p.name not in EXCLUDED and '__pycache__' not in p.parts]
    files+=list((ROOT/'cczps_lite/integration/earth_system_coupling').glob('*.py'))
    files+=[ROOT/'tests/test_earth_system_coupling.py',ROOT/'README.md'];return sorted(files)
def check():
    required='TASKBOOK_ZH.md REUSE_AUDIT.md MECHANISM_RESEARCH.md SHARED_STATE_SCHEMA.json MODEL_INTERFACE.md COUPLER_DESIGN.md NUMERICAL_METHODS_AND_ASSUMPTIONS.md EXPERIMENT_MATRIX.md EXPERIMENT_RESULTS.json summary.csv COUNTEREVIDENCE_AND_FAILURES.md DATA_AND_MODEL_RIGHTS.md PHYSICAL_AND_STATISTICAL_GATES.md FOUNDER_REPORT_ZH.md CCZPS_ECOCHAIN_HANDOFF.md QA_AND_VALIDATION.md NEXT_SESSION.md CRP_HANDOFF.md REVIEW_REQUEST.json HANDOFF_STATUS.json slides.html'.split()
    assert all((TASK/x).exists() for x in required)
    manifest=data(TASK/'manifest.json')
    assert set(manifest)=={p.relative_to(ROOT).as_posix() for p in paths()}
    for name,entry in manifest.items():assert sha(ROOT/name)['sha256']==entry['sha256'],name
    for p in TASK.rglob('*.json'):data(p)
    summary=data(TASK/'EXPERIMENT_RESULTS.json');receipt=data(TASK/'evidence/batch-receipt.json')
    full=data(TASK/'evidence/main/summary.json')
    assert {k:v for k,v in summary.items() if k!='paired_records_path'}=={k:v for k,v in full.items() if k!='pairs'}
    assert summary['source_hashes']==e.code_hashes()==receipt['source_hashes']
    assert summary['pre_run_protocol_sha256']==hashlib.sha256((TASK/'PRE_RUN_PROTOCOL.md').read_bytes()).hexdigest()
    assert receipt['replay_same_sha256'] and receipt['replay_sha256']==summary['runs_sha256']
    older=data(TASK/'evidence/pre_interface_batch_receipt.json');smoke=data(TASK/'evidence/smoke_initial_receipt.json')
    seconds=receipt['total_script_wall_seconds']+older['total_script_wall_seconds']+smoke['elapsed_seconds'];assert seconds<1200
    bytes_total=sum(p.stat().st_size for p in paths());assert bytes_total<200000000
    for x in data(TASK/'evidence/reuse-blobs.json'):assert hashlib.sha256((ROOT/x['path']).read_bytes().replace(b'\r\n',b'\n')).hexdigest()==x['lf_sha256']
    baseline=m.public_baseline();assert abs(baseline['radiation']['ERF_W_m2']-.569344413968403)<1e-14
    links=0
    for p in TASK.glob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
            if target.startswith(('http:','https:','#','mailto:')):continue
            assert (p.parent/target.split('#')[0]).exists(),(p,target);links+=1
    logs=(TASK/'evidence/full-tests.txt').read_text(encoding='utf-8');assert 'Ran 739 tests' in logs and 'OK (skipped=1)' in logs
    ui=data(TASK/'evidence/slides-validation.json');assert len(ui['views'])==24 and not ui['errors'] and not ui['network_requests']
    return {'status':'LOCAL_VERIFIED','scientific_admission':'PENDING','deployed':False,'manifest_files':len(manifest),'local_links':links,
            'total_archive_bytes':bytes_total,'counted_batch_wall_seconds':seconds,'local_tests_total':739,'local_tests_passed':738,'local_tests_skipped':1,
            'new_tests':65,'independent_audit':audit(),'ui':'PASS_24_PAGE_VIEWPORT_CHECKS','source_hashes_match':True,'protected_baseline_verified':True}
def main():
    p=argparse.ArgumentParser();p.add_argument('--record',action='store_true');a=p.parse_args()
    if a.record:(TASK/'manifest.json').write_text(json.dumps({p.relative_to(ROOT).as_posix():sha(p) for p in paths()},indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
    report=check();out=TASK/'evidence/validation.json' if a.record else ROOT/'runtime_data/earth_coupling/validation.json'
    out.parent.mkdir(exist_ok=True,parents=True);out.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n');print(json.dumps(report,ensure_ascii=False))
if __name__=='__main__':main()
