"""Final compatibility delta: old document/new scripts and versioned current assets."""
from pathlib import Path
import functools,http.server,threading,subprocess,json,datetime
from playwright.sync_api import sync_playwright,expect
APP=Path(__file__).resolve().parents[1];OUT=APP/'qa/navigation-repair-20261102/compat';OUT.mkdir(exist_ok=True)
old=subprocess.check_output(['git','show','ad79ec234a4c3d7017183b427a63f2e1951bfdb8:apps/public-strategy-atlas/index.html'],cwd=APP)
class Handler(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
 def do_GET(self):
  if self.path=='/?legacy=1':self.send_response(200);self.send_header('Content-Type','text/html');self.end_headers();self.wfile.write(old)
  else:super().do_GET()
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(APP)));threading.Thread(target=server.serve_forever,daemon=True).start();base='http://127.0.0.1:'+str(server.server_port)+'/'
result={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cases':[]}
try:
 with sync_playwright()as p:
  b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  for width,legacy in [(1440,False),(390,False),(1440,True)]:
   page=b.new_page(viewport={'width':width,'height':844},has_touch=width==390);errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.goto(base+('?legacy=1'if legacy else''));expect(page.locator('#contentCount')).to_have_text('127',timeout=30000)
   if not legacy:expect(page.locator('#startupNotice')).to_be_hidden();assert '?v=navigation-20261102-2'in page.locator('script[src*="/atlas.js"]').get_attribute('src')
   page.locator('#sourceResearchLink').click();expect(page.locator('#csoiEngineeringTasks [data-task-id]')).to_have_count(80,timeout=30000)
   for label,title in [('打开 LSPS 地图与正文','LSPS 地图、正文与行动'),('只看地图记录','LSPS 地图记录'),('打开 OP 逐页梳理','OP 逐页梳理')]:
    page.get_by_role('link',name=label,exact=True).click();expect(page.locator('#csoiResearchResults h2')).to_have_text(title,timeout=30000);expect(page.locator('#csoiWorkspace')).not_to_have_attribute('aria-busy','true',timeout=30000);expect(page.locator('#csoiResearchResults h2')).to_be_focused();expect(page.locator('#csoiResearchResults .csoi-records a').first).to_be_in_viewport()
   assert not errors;result['cases'].append({'width':width,'legacyDocumentWithCurrentScripts':legacy,'actualClicks':3,'status':'PASS','errors':errors});page.close()
  b.close()
 result['status']='PASS'
finally:
 (OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n');server.shutdown()
