"""Offline scoped validation. --record archives this new task only."""
import argparse
from datetime import datetime, timezone
import hashlib, json, platform, re, subprocess, sys
from pathlib import Path
from urllib.parse import unquote
TASK=Path(__file__).resolve().parents[1];ROOT=TASK.parents[2]
sys.path.insert(0,str(ROOT))
from cczps_lite.integration import enso_regional_weather as e

EXCLUDE={'manifest.json','validation.json','HANDOFF_STATUS.json','REVIEW_REQUEST.json'}
def manifest():
    paths=[p for p in TASK.rglob('*') if p.is_file() and p.name not in EXCLUDE and '__pycache__' not in p.parts]
    paths += [ROOT/'cczps_lite/integration/enso_regional_weather.py',ROOT/'tests/test_enso_regional_weather.py']
    files={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest() for p in sorted(paths)}
    (TASK/'evidence/manifest.json').write_text(e.canonical({'algorithm':'sha256','normalization':'CRLF_to_LF_for_text; acquisition receipts separately preserve raw SHA',
        'excluded_metadata':sorted(EXCLUDE),'files':files}),encoding='utf-8',newline='\n')
def run(command,log):
    r=subprocess.run([sys.executable,'-X','utf8',*command],cwd=ROOT,text=True,encoding='utf-8',errors='replace',stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    log.write_text('COMMAND: python -X utf8 '+' '.join(command)+'\n'+r.stdout+'\nEXIT_CODE: '+str(r.returncode)+'\n',encoding='utf-8',newline='\n')
    if r.returncode: raise SystemExit(r.returncode)
    return r.stdout
def links():
    count=0
    for p in TASK.glob('*.md'):
        for url in re.findall(r'\]\(([^\s)]+)\)',p.read_text(encoding='utf-8-sig')):
            if '://' in url or url.startswith('#'):continue
            target=(p.parent/unquote(url.split('#')[0])).resolve()
            if not target.is_file():raise ValueError('BROKEN_LOCAL_LINK '+str(p)+': '+url)
            count+=1
    return count
def main():
    p=argparse.ArgumentParser();p.add_argument('--record',action='store_true');a=p.parse_args()
    target=TASK/'evidence' if a.record else ROOT/'runtime_data/enso_regional_validation'
    target.mkdir(parents=True,exist_ok=True)
    if a.record:manifest()
    newlog=run(['-m','unittest','tests.test_enso_regional_weather','-v'],target/'tests-new.txt')
    inherited=run(['docs/tasks/climateos_physical_process_trajectory_001/run_validation.py'],target/'tests-inherited-run.txt')
    old=ROOT/'runtime_data/physical_trajectory_validation'
    (target/'tests-inherited.txt').write_text((old/'tests.txt').read_text(encoding='utf-8'),encoding='utf-8',newline='\n')
    oldresult=e.read(old/'validation.json')
    if a.record:manifest()
    v=e.evaluate(e.request()); snap=e.canonical(v)
    assert snap==e.canonical(e.evaluate(e.request())),'NONDETERMINISTIC'
    if not a.record:assert snap==(TASK/'evidence/end-to-end.json').read_text(encoding='utf-8'),'ARCHIVED_RESULT_CHANGED'
    (target/'end-to-end.json').write_text(snap,encoding='utf-8',newline='\n')
    if a.record:manifest()
    count=e.verify()
    report={'completed_utc':datetime.now(timezone.utc).isoformat(),'python':platform.python_version(),
      'engineering_status':'LOCAL_VERIFIED','science_result':'DATA_NOT_READY','scientific_admission':'PENDING',
      'new_tests':int(re.search(r'Ran (\d+) tests',newlog).group(1)), 'inherited_tests':120,
      'manifest_files':count,'inherited_trajectory_files':oldresult['manifest_checked'],
      'inherited_atlas_files':oldresult['frozen_atlas_files_checked'],'local_links':None,
      'inherited_results_sha256':oldresult['results_sha256'],
      'results_sha256':hashlib.sha256(snap.encode()).hexdigest(),'repeat_runs':2,
      'real_rain_pairs':0,'statistical_experiment_executed':False,'deployed':False}
    (target/'validation.json').write_text(e.canonical(report),encoding='utf-8',newline='\n')
    report['local_links']=links()
    (target/'validation.json').write_text(e.canonical(report),encoding='utf-8',newline='\n');print(e.canonical(report))
if __name__=='__main__': main()
