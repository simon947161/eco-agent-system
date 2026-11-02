#!/usr/bin/env python3
"""Run existing browser assertions unchanged except output directory/local port.
This adapter is audit tooling only; no edits to production or original QA files.
"""
import ast,datetime,hashlib,json,os,re,subprocess,sys,threading,time
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
HERE=Path(__file__).resolve().parent;APP=HERE.parents[2];ROOT=APP.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
allowed={'csoi-compare-browser.py','csoi-paths-browser.py','discovery-browser.py','integration-browser.py'}
scripts=sys.argv[1:] or ['csoi-compare-browser.py','csoi-paths-browser.py','discovery-browser.py','integration-browser.py']
assert set(scripts)<=allowed
run_tag=os.environ.get('CSOI_AUDIT_RUN_TAG','')
assert not run_tag or re.fullmatch(r'[A-Za-z0-9_-]{1,40}',run_tag)
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(APP)))
port=server.server_address[1];base=f'http://127.0.0.1:{port}/'
threading.Thread(target=server.serve_forever,daemon=True).start()
results=[]
paths=sorted([*APP.glob('*.js'),*APP.glob('*.css'),*APP.glob('*.html'),*APP.glob('sources/*.json'),*APP.glob('sources/*.js')])
before={str(p.relative_to(ROOT)):sha(p) for p in paths}
class Adapter(ast.NodeTransformer):
    def __init__(self,out):self.out=out
    def visit_Assign(self,node):
        self.generic_visit(node)
        if any(isinstance(t,ast.Name) and t.id=='OUT' for t in node.targets):node.value=ast.Call(func=ast.Name(id='Path',ctx=ast.Load()),args=[ast.Constant(str(self.out))],keywords=[])
        return node
    def visit_Constant(self,node):
        if isinstance(node.value,str):
            node.value=node.value.replace('http://127.0.0.1:8877/',base)
            if node.value.startswith('/tmp/atlas-discovery-'):node.value=node.value.replace('/tmp/',str(self.out)+'/',1)
        return node
    def visit_Call(self,node):
        self.generic_visit(node)
        if isinstance(node.func,ast.Attribute) and isinstance(node.func.value,ast.Name) and node.func.value.id=='tempfile' and node.func.attr=='gettempdir':return ast.Constant(str(self.out))
        return node
try:
    for name in scripts:
        source=APP/'qa'/name;out=HERE/'browser'/(name.removesuffix('.py')+('-'+run_tag if run_tag else ''));out.mkdir(parents=True,exist_ok=True)
        tree=ast.fix_missing_locations(Adapter(out).visit(ast.parse(source.read_text())))
        transformed=ast.unparse(tree)
        adapted=out/'adapted-test.py'
        adapted.write_text('__file__='+repr(str(source))+'\n'+transformed+'\n')
        started=now();tick=time.monotonic()
        run=subprocess.run([sys.executable,str(adapted)],cwd=ROOT,capture_output=True,text=True,timeout=300)
        (out/'execution.log').write_text(run.stdout+run.stderr)
        row={'script':name,'sourceSHA256':sha(source),'adaptedSHA256':sha(adapted),'onlyAdaptations':['OUT path','loopback ephemeral port','temporary download destination'],'startedAt':started,'finishedAt':now(),'durationSeconds':round(time.monotonic()-tick,3),'status':'PASS_ACTUALLY_TESTED' if run.returncode==0 else 'FAIL','exitCode':run.returncode,'log':str((out/'execution.log').relative_to(HERE))}
        results.append(row);print(name,row['status'],flush=True)
        report={'at':now(),'head':subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,text=True,capture_output=True,check=True).stdout.strip(),'runTag':run_tag,'baseURL':base,'runtimeFileSHA256Before':before,'results':results,'runtimeUnchanged':all(sha(ROOT/p)==h for p,h in before.items()),'sameAgentAsBaselineAuthor':True}
        text=json.dumps(report,ensure_ascii=False,indent=2)+'\n';(HERE/'browser-results.json').write_text(text)
        if run_tag:(HERE/('browser-results-'+run_tag+'.json')).write_text(text)
        if run.returncode:raise SystemExit(run.returncode)
    env=os.environ.copy();env['CSOI_AUDIT_BASE_URL']=base
    run=subprocess.run([sys.executable,str(HERE/'browser-linear-accessibility.py')],cwd=ROOT,capture_output=True,text=True,env=env,timeout=180)
    (HERE/'linear-accessibility.log').write_text(run.stdout+run.stderr);print('linear-accessibility',run.returncode,flush=True)
    if run.returncode:raise SystemExit(run.returncode)
finally:
    server.shutdown();server.server_close()
