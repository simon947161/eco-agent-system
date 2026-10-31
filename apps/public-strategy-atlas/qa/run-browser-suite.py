"""Run actual Atlas browser suites with bounded concurrency and durable outcomes.
Serve the app at 127.0.0.1:8877 first. Requires engineering Playwright + Chromium.
"""
from pathlib import Path
import concurrent.futures, datetime, importlib.metadata, json, subprocess,sys
HERE=Path(__file__).resolve().parent
OUT=HERE/'system';OUT.mkdir(exist_ok=True)
SCRIPTS=['e0-browser.py','system-browser.py','deep-browser.py','merge-browser.py','discovery-browser.py','integration-browser.py']
def run(name):
 result=subprocess.run([sys.executable,str(HERE/name)],text=True,capture_output=True)
 (OUT/('e10-'+name+'.log')).write_text(result.stdout+result.stderr)
 passes=sum(line.startswith('PASS:') for line in result.stdout.splitlines())
 return {'script':name,'status':'PASS_TESTED_HERE' if result.returncode==0 and passes>0 else 'FAIL','exitCode':result.returncode,'functionalCheckGroups':passes,'log':'e10-'+name+'.log'}
selected=sys.argv[1:] or SCRIPTS
if any(name not in SCRIPTS for name in selected):raise ValueError('Unknown browser suite')
current=list(concurrent.futures.ThreadPoolExecutor(max_workers=2).map(run,selected))
prior=json.loads((OUT/'browser-e10.json').read_text()) if (OUT/'browser-e10.json').exists() and selected!=SCRIPTS else {}
by_name={r['script']:r for r in prior.get('results',[])}
for r in current:r['executedAt']=datetime.datetime.now(datetime.timezone.utc).isoformat();by_name[r['script']]=r
results=[by_name[name] for name in SCRIPTS if name in by_name]
for r in results:r.setdefault('executedAt',prior.get('generatedAt'));r['executedThisInvocation']=r['script'] in selected
metadata={'invocationSuites':selected,'allSuitesExecutedThisInvocation':selected==SCRIPTS,'generatedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'browser':subprocess.check_output(['/usr/bin/chromium','--version'],text=True).strip(),'playwright':importlib.metadata.version('playwright'),'python':sys.version.split()[0],'results':results,'limits':'Viewport emulation and Chromium accessibility tree are not physical hardware, cross-browser or professional screen-reader certification.'}
(OUT/'browser-e10.json').write_text(json.dumps(metadata,indent=2)+'\n')
print(json.dumps(metadata,indent=2),flush=True)
if any(r['status']=='FAIL' for r in results):sys.exit(1)
