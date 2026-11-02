from pathlib import Path
import functools,http.server,threading,json,datetime,sys
APP=Path('/workspace/eco-agent-system/apps/public-strategy-atlas');OUT=APP/'qa/navigation-repair-20261102/regression';OUT.mkdir(exist_ok=True)
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(APP)));threading.Thread(target=server.serve_forever,daemon=True).start();base='http://127.0.0.1:'+str(server.server_port)+'/'
report={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'suites':[]}
try:
 for name in ['csoi-phe-context-browser.py','live-workspace-browser.py']:
  file=APP/'qa'/name;source=file.read_text().replace('http://127.0.0.1:8877/',base)
  if name.startswith('csoi'):
   folder=OUT/'phe';folder.mkdir(exist_ok=True);source=source.replace("OUT=APP/'qa/csoi'",'OUT=Path('+repr(str(folder))+')')
  else:
   folder=OUT/'workspace';source=source.replace("OUT = Path(__file__).resolve().parent / 'live-workspace'",'OUT = Path('+repr(str(folder))+')').replace("Path('/tmp/atlas-live-workspace')","Path('/tmp/atlas-nav-workspace')")
  exec(compile(source,str(file),'exec'),{'__file__':str(file),'__name__':'__main__'});report['suites'].append({'name':name,'status':'PASS'});(OUT/'results.json').write_text(json.dumps(report,indent=2)+'\n')
 report['status']='PASS';(OUT/'results.json').write_text(json.dumps(report,indent=2)+'\n')
finally:server.shutdown()
