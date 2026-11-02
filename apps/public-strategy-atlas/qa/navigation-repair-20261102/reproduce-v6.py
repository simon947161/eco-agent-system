import json,time,datetime,threading,http.server,functools,os
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
APP=Path('/workspace/eco-agent-system/apps/public-strategy-atlas')
OUT=APP/'qa/navigation-repair-20261102';OUT.mkdir(exist_ok=True)
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(APP)))
threading.Thread(target=server.serve_forever,daemon=True).start()
base='http://127.0.0.1:'+str(server.server_port)+'/'
report={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mode':'local canonical v6 code','results':[]}
def save():(OUT/'before.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
with sync_playwright()as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in [1440,390]:
  page=browser.new_page(viewport={'width':width,'height':900 if width==1440 else 844},has_touch=width==390);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(base);expect(page.locator('#contentCount')).to_have_text('127',timeout=30000)
  page.locator('#sourceResearchLink').click();expect(page.locator('#csoiEngineeringTasks [data-task-id]')).to_have_count(80,timeout=30000)
  for label in ['打开 LSPS 地图与正文','只看地图记录','打开 OP 逐页梳理']:
   link=page.get_by_role('link',name=label,exact=True);target=link.get_attribute('href');link.click();expect(page.locator('#csoiEngineeringTasks [data-task-id]')).to_have_count(80,timeout=30000)
   row=page.evaluate('''()=>{let h=document.querySelector('#csoiWorkspace'), list=h.querySelector('.csoi-records'), a=list?.querySelector('a');return {url:location.href,hash:location.hash,heading:h.querySelector('h1')?.textContent,scrollTop:h.scrollTop,viewport:innerHeight,visibleTop:document.elementFromPoint(innerWidth/2,150)?.textContent?.slice(0,240),cards:list?.querySelectorAll('li').length,first:a?.textContent,firstHref:a?.getAttribute('href'),firstY:a?.getBoundingClientRect().top,empty:h.textContent.includes('未找到这项来源记录'),error:h.textContent.includes('Workspace could not be verified')}}''');row.update(viewport=width,clicked=label,target=target,browserErrors=list(errors));report['results'].append(row);save();page.screenshot(path=str(OUT/f'before-{width}-{len(report["results"])}.png'));print(json.dumps(row,ensure_ascii=False),flush=True)
  page.close()
 browser.close()
server.shutdown()
