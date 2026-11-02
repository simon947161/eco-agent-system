"""Run applicable real Chromium suites; keep this batch's evidence separate from prior runs."""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
import datetime,json,subprocess,sys,threading,os
APP=Path(__file__).resolve().parents[1];OUT=APP/os.environ.get('ATLAS_TEST_OUTPUT','qa/op-completion-20261102/regression');OUT.mkdir(parents=True,exist_ok=True)
SUITES=['csoi-op-browser.py','csoi-lsps-browser.py','csoi-metric-browser.py','csoi-strategy-browser.py','csoi-phe-context-browser.py','e0-browser.py','system-browser.py']
selected=sys.argv[1:]or SUITES
assert all(s in SUITES for s in selected)
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',int(os.environ.get('ATLAS_TEST_PORT','8877'))),partial(Quiet,directory=str(APP)));threading.Thread(target=server.serve_forever,daemon=True).start()
results=[]
try:
 for name in selected:
  script=APP/'qa'/name;source=script.read_text().replace('http://127.0.0.1:8877','http://127.0.0.1:'+os.environ.get('ATLAS_TEST_PORT','8877'));dest=OUT/name.removesuffix('.py');dest.mkdir(parents=True,exist_ok=True)
  for pattern in ["OUT=APP/'qa/lsps-completion/browser'","OUT=APP/'qa/csp-metric-review/browser'","OUT=APP/'qa/strategy-completion/browser'","OUT=APP/'qa/csoi'","OUT=APP/'qa'/'system'","OUT = Path(__file__).resolve().parent / 'e0'"]:
   source=source.replace(pattern,'OUT=Path('+repr(str(dest))+')')
  start=datetime.datetime.now(datetime.timezone.utc).isoformat()
  command='exec(compile('+repr(source)+','+repr(str(script))+',"exec"),{"__file__":'+repr(str(script))+',"__name__":"__main__"})'
  r=subprocess.run([sys.executable,'-c',command],cwd=APP,capture_output=True,text=True);(OUT/(name+'.log')).write_text(r.stdout+r.stderr)
  row={'script':name,'startedAt':start,'finishedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exitCode':r.returncode,'status':'PASS_TESTED_HERE'if r.returncode==0 and 'PASS:'in r.stdout else'FAIL','log':name+'.log'};results.append(row);(OUT/'browser-run.json').write_text(json.dumps({'results':results},indent=2)+'\n');print(row['status'],name,flush=True)
finally:server.shutdown();server.server_close()
if any(r['status']=='FAIL'for r in results):sys.exit(1)
