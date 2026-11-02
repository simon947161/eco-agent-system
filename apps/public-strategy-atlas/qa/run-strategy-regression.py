"""Run all current browser leaf suites and retain their output in this batch."""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
import datetime,json,subprocess,sys,threading
APP=Path(__file__).resolve().parents[1];OUT=APP/'qa/strategy-completion/regression';OUT.mkdir(parents=True,exist_ok=True)
SCRIPTS=['e0-browser.py','system-browser.py','deep-browser.py','merge-browser.py','discovery-browser.py','integration-browser.py','intake-access-browser.py','csoi-browser.py','csoi-source-browser.py','csoi-corpus-browser.py','csoi-layer-browser.py','csoi-compare-browser.py','csoi-wcos-browser.py','csoi-phe-browser.py','csoi-work-browser.py','csoi-calendar-browser.py','csoi-clauses-browser.py','csoi-snowy-browser.py','csoi-paths-browser.py','csoi-review-work-browser.py','csoi-cooma-browser.py','csoi-phe-context-browser.py','csoi-bombala-browser.py','csoi-bombala-phe-browser.py']
selected=sys.argv[1:]or SCRIPTS
assert all(s in SCRIPTS for s in selected)
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',8877),partial(Quiet,directory=str(APP)));threading.Thread(target=server.serve_forever,daemon=True).start()
results=[]
try:
 for script in selected:
  start=datetime.datetime.now(datetime.timezone.utc).isoformat();r=subprocess.run([sys.executable,str(APP/'qa'/script)],capture_output=True,text=True);(OUT/(script+'.log')).write_text(r.stdout+r.stderr)
  row={'script':script,'startedAt':start,'finishedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exitCode':r.returncode,'status':'PASS_TESTED_HERE'if r.returncode==0 and 'PASS:'in r.stdout else'FAIL','log':script+'.log'};results.append(row);(OUT/'browser-run.json').write_text(json.dumps({'results':results},indent=2)+'\n');print(row['status'],script,flush=True)
finally:server.shutdown();server.server_close()
if any(r['status']=='FAIL'for r in results):sys.exit(1)
