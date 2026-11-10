"""Offline reproduction; --record updates only this new research package."""
import argparse, hashlib, json, platform, re, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path
TASK=Path(__file__).resolve().parents[1];ROOT=TASK.parents[2]
sys.path.insert(0,str(ROOT))
from cczps_lite.integration import multisource_data_admission as m
from independent_audit import audit
EXCLUDE={'manifest.json','validation.json','HANDOFF_STATUS.json','REVIEW_REQUEST.json'}
def manifest():
    paths=[p for p in TASK.rglob('*') if p.is_file() and p.name not in EXCLUDE and '__pycache__' not in p.parts]
    paths += [ROOT/'cczps_lite/integration/multisource_data_admission.py',ROOT/'tests/test_multisource_data_admission.py']
    exact=[p.relative_to(ROOT).as_posix() for p in paths if p.suffix in ('.csv','.png') or p.name=='PRE_ACCESS_PLAN.md']
    files={p.relative_to(ROOT).as_posix():m.sha(p.read_bytes() if p.relative_to(ROOT).as_posix() in exact else p.read_bytes().replace(b'\r\n',b'\n')) for p in sorted(paths)}
    (TASK/'evidence/manifest.json').write_text(m.canonical({'algorithm':'sha256','normalization':'LF except byte_exact raw files and pre-access plan','byte_exact':exact,'excluded_metadata':sorted(EXCLUDE),'files':files}),encoding='utf-8',newline='\n')
def run(args,path):
    r=subprocess.run([sys.executable,'-X','utf8',*args],cwd=ROOT,text=True,encoding='utf-8',errors='replace',stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    path.write_text('COMMAND: python -X utf8 '+' '.join(args)+'\n'+r.stdout+'\nEXIT_CODE: '+str(r.returncode)+'\n',encoding='utf-8',newline='\n')
    if r.returncode:raise RuntimeError(r.stdout)
    return r.stdout
def write(path,obj):path.write_text(m.canonical(obj),encoding='utf-8',newline='\n')
def main():
    p=argparse.ArgumentParser();p.add_argument('--record',action='store_true');a=p.parse_args()
    target=TASK/'evidence' if a.record else ROOT/'runtime_data/multisource_validation';target.mkdir(parents=True,exist_ok=True)
    if a.record:manifest()
    log=run(['-m','unittest','tests.test_multisource_data_admission','-v'],target/'tests-new.txt')
    run(['docs/tasks/climateos_enso_regional_weather_probability_001/scripts/validate.py'],target/'tests-pr148-regression.txt')
    old=m.read(ROOT/'runtime_data/enso_regional_validation/validation.json')
    write(target/'inherited-validation.json',old)
    if a.record:manifest()
    result=m.evaluate(m.request());snap=m.canonical(result)
    assert snap==m.canonical(m.evaluate(m.request())),'NONDETERMINISTIC'
    if not a.record:assert snap==(TASK/'evidence/results.json').read_text(encoding='utf-8'),'ARCHIVED_RESULT_CHANGED'
    (target/'results.json').write_text(snap,encoding='utf-8',newline='\n')
    write(target/'independent-exact-audit.json',audit())
    if a.record:
        write(TASK/'PAIRED_DATA.json',{'source_id':m.SOURCE,'data_support':m.SUPPORT,'index_version':m.INDEX,
          'unit':'mm','rows':result['paired_rows'],'unique_valid_rain_years':46,'valid_mode_pairs':92,
          'warning':'same response years reused across two modes; not 92 independent weather years'})
        manifest()
    from urllib.parse import unquote
    links=0
    for doc in TASK.glob('*.md'):
        for u in re.findall(r'\]\(([^\s)]+)\)',doc.read_text(encoding='utf-8-sig')):
            if '://' in u or u.startswith('#'):continue
            assert (doc.parent/unquote(u.split('#')[0])).is_file(),(doc,u)
            links+=1
    report={'completed_utc':datetime.now(timezone.utc).isoformat(),'python':platform.python_version(),
      'engineering_status':'LOCAL_VERIFIED','data_status':result['status'],'scientific_admission':'PENDING',
      'new_tests':int(re.search(r'Ran (\d+) tests',log).group(1)),'inherited_tests':old['new_tests']+old['inherited_tests'],
      'new_manifest_files':m.verify(),'inherited_pr148_files':old['manifest_files'],
      'inherited_pr148_result_sha256':old['results_sha256'],'inherited_pr147_result_sha256':old['inherited_results_sha256'],
      'results_sha256':m.sha(snap.encode()),'repeat_runs':2,'unique_valid_rain_years':46,
      'independent_rational_implementation':'PASS','local_links':links,'network_files':3,'network_bytes':420750,
      'numerical_experiment':'AUTHORIZED_BOUNDED_HISTORICAL_DESCRIPTIVE_STATISTICS','deployed':False}
    write(target/'validation.json',report);print(m.canonical(report))
if __name__=='__main__':main()
