import sys,termios,json,os,time,urllib.parse
from playwright.sync_api import sync_playwright,expect
from pathlib import Path
s=termios.tcgetattr(sys.stdin.fileno());s[3]&=~termios.ECHO;termios.tcsetattr(sys.stdin.fileno(),termios.TCSANOW,s);print('Ready for supported service credential JSON.',flush=True);c=json.loads(sys.stdin.readline());base=c['url'].rstrip('/')+'/';assert base=='https://council-strategy-intelligence.minshu.chatgpt.site/'
report={'mode':'Direct Chromium through configured proxy, scoped supported service header; TLS verification enabled','requests':[],'errors':[]}
proxy=os.environ.get('HTTPS_PROXY')or os.environ.get('https_proxy');assert proxy,'Configured proxy missing'
with sync_playwright()as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'],proxy={'server':proxy});page=b.new_page(viewport={'width':1440,'height':900});page.on('pageerror',lambda e:report['errors'].append(str(e).replace(c['token'],'[redacted]')))
 def auth(route):
  req=route.request;assert req.url.startswith(base);headers=dict(req.headers);headers['OAI-Sites-Authorization']='Bearer '+c['token'];route.continue_(headers=headers)
 page.route(base+'**',auth);page.on('response',lambda r:report['requests'].append({'origin':urllib.parse.urlsplit(r.url).netloc,'path':urllib.parse.urlsplit(r.url).path,'status':r.status}))
 start=time.monotonic()
 try:
  page.goto(base,timeout=30000);expect(page.locator('#contentCount')).to_have_text('127',timeout=30000);page.locator('#sourceResearchLink').click();expect(page.locator('#csoiEngineeringTasks [data-task-id]')).to_have_count(80,timeout=30000);page.get_by_role('link',name='只看地图记录',exact=True).click();expect(page.locator('#csoiResearchResults .csoi-records a').first).to_be_in_viewport();report['status']='PASS';report['content']=page.locator('#csoiResearchResults').inner_text()[:300]
 except Exception as e:
  report['status']='FAILED';report['failure']=str(e)[:1500]
  try:report['state']=page.context.new_cdp_session(page).send('Runtime.evaluate',{'expression':"JSON.stringify({ready:document.readyState,notice:document.getElementById('startupMessage')?.textContent,count:document.getElementById('contentCount')?.textContent,url:location.href})",'returnByValue':True,'timeout':2000})
  except Exception as x:report['diagnosticFailure']=str(x)[:500]
 report['seconds']=round(time.monotonic()-start,3);b.close()
(Path(__file__).resolve().parent/'navigation-repair-20261102/direct-browser-probe.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='requests'},ensure_ascii=False),flush=True)
