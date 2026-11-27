#!/usr/bin/env python3
"""Sequential focused native checks; leaves production and original audit intact."""
import datetime,hashlib,json,subprocess,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
APP=HERE.parents[2]
ROOT=APP.parents[1]
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
runtime=sorted([*APP.glob('*.js'),*APP.glob('*.css'),*APP.glob('*.html'),*APP.glob('sources/*.json')])
code_hashes={str(p.relative_to(ROOT)):sha(p) for p in runtime}
code_digest=hashlib.sha256(json.dumps(code_hashes,sort_keys=True,separators=(',',':')).encode()).hexdigest()
head=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,capture_output=True,text=True,check=True).stdout.strip()
tests=['csoi-governance.test.cjs','csoi-layers.test.cjs','csoi-wcos.test.cjs','csoi-router.test.cjs','integration.test.cjs','comparison.test.cjs','csoi-paths.test.cjs','discovery.test.cjs']
commands=[['node',str(APP/t)] for t in tests]+[['node',str(HERE/'targeted-contract-readback.cjs')]]
results=[]
for command in commands:
    name=Path(command[-1]).name;start=stamp();tick=time.monotonic()
    try:
        result=subprocess.run(command,cwd=ROOT,text=True,capture_output=True,timeout=120)
        status='PASS_ACTUALLY_TESTED' if result.returncode==0 else 'FAIL'
        stdout,stderr,exit_code=result.stdout,result.stderr,result.returncode
    except subprocess.TimeoutExpired as error:
        status='TIMEOUT';stdout=str(error.stdout or '');stderr=str(error.stderr or '');exit_code=None
    (HERE/(name+'.log')).write_text(stdout+stderr)
    row={'command':command,'cwd':str(ROOT),'startedAt':start,'finishedAt':stamp(),'durationSeconds':round(time.monotonic()-tick,3),'status':status,'exitCode':exit_code,'testSHA256':sha(Path(command[-1])),'log':name+'.log'}
    results.append(row);print(name,status,flush=True)
    report={'format':'csoi-023-074-targeted-native-readback-1','head':head,'runtimeFileSHA256':code_hashes,'runtimeManifestSHA256':code_digest,'executedSequentially':True,'perProcessLimitSeconds':120,'sameAgentAsBaselineAuthor':True,'status':'PASS_ACTUALLY_TESTED' if all(r['status']=='PASS_ACTUALLY_TESTED' for r in results) else 'FAIL','complete':len(results)==len(commands),'results':results,'runtimeUnchangedAfterChecks':all(sha(ROOT/p)==h for p,h in code_hashes.items())}
    (HERE/'native-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    if status!='PASS_ACTUALLY_TESTED':raise SystemExit(1)
