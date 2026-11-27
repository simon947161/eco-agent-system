#!/usr/bin/env python3
"""Very short final module-pinned readback; run only after parent stabilises code."""
import datetime,hashlib,json,os,subprocess,time
from pathlib import Path
HERE=Path(__file__).resolve().parent;APP=HERE.parents[2];ROOT=APP.parents[1]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
cases=[('governance',APP/'csoi-governance.test.cjs'),('layers',APP/'csoi-layers.test.cjs'),('digest-screening',APP/'csoi-digest-screening.test.cjs'),('targeted-contract',HERE/'targeted-contract-readback.cjs')]
results=[]
for name,test in cases:
    env=os.environ.copy();receipt=HERE/(name+'-final-loaded-modules.json');env['CSOI_READBACK_MODULE_RECEIPT']=str(receipt)
    command=['node','--require',str(HERE/'capture-module-hashes.cjs'),str(test)];started=now();tick=time.monotonic()
    run=subprocess.run(command,cwd=ROOT,env=env,text=True,capture_output=True,timeout=120)
    log=name+'-final.log';(HERE/log).write_text(run.stdout+run.stderr)
    results.append({'command':command,'startedAt':started,'finishedAt':now(),'seconds':round(time.monotonic()-tick,3),'exitCode':run.returncode,'testSHA256':sha(test),'modules':json.loads(receipt.read_text()),'log':log})
    print(name,'PASS' if run.returncode==0 else 'FAIL',flush=True)
    if run.returncode:break
report={'format':'csoi-final-module-pinned-native-readback-1','head':subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,text=True,capture_output=True,check=True).stdout.strip(),'status':'PASS_ACTUALLY_TESTED' if len(results)==4 and all(r['exitCode']==0 for r in results) else 'FAIL','sameAgentAsBaselineAuthor':True,'results':results,'loadedFilesStableAndCurrent':all(m['stableDuringLoad'] and sha(Path(m['file']))==m['sha256AtLoad'] for r in results for m in r['modules']['modules'])}
(HERE/'final-core-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
raise SystemExit(0 if report['status']=='PASS_ACTUALLY_TESTED' and report['loadedFilesStableAndCurrent'] else 1)
