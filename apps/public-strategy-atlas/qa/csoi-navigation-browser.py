"""Founder-reported navigation: actual DOM clicks and visible destination content.

Direct goto is used only for explicit initial/deep-link/reload cases, never as a
substitute for the three reported links. Optional live adapter supplies supported
service access; it must not claim an owner-login session.
"""
from pathlib import Path
import datetime,functools,http.server,json,os,threading,tempfile,subprocess,time
from playwright.sync_api import sync_playwright,expect
APP=Path(__file__).resolve().parents[1]
OUT=Path(os.environ.get('ATLAS_NAV_OUTPUT',str(APP/'qa/navigation-repair-20261102/local')));OUT.mkdir(parents=True,exist_ok=True)
BASE=os.environ.get('ATLAS_TEST_URL');server=None
if not BASE:
 class Quiet(http.server.SimpleHTTPRequestHandler):
  def log_message(self,*args):pass
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(APP)))
 threading.Thread(target=server.serve_forever,daemon=True).start();BASE='http://127.0.0.1:'+str(server.server_port)+'/'
report={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mode':os.environ.get('ATLAS_NAV_MODE','local real Chromium'),'ownerInteractiveLogin':'NOT_TESTED','results':[]}
def save():(OUT/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
def ready(page):
 expect(page.locator('#contentCount')).to_have_text('127',timeout=30000);expect(page.locator('#startupNotice')).to_be_hidden();expect(page.locator('.app')).not_to_have_attribute('inert','')
def settled(page):expect(page.locator('#csoiWorkspace')).not_to_have_attribute('aria-busy','true',timeout=30000)
def result(page,title):
 expect(page.locator('#csoiResearchResults h2')).to_have_text(title,timeout=30000);settled(page)
 first=page.locator('#csoiResearchResults .csoi-records a').first;expect(first).to_be_in_viewport()
 expect(page.locator('#csoiResearchResults h2')).to_be_focused()
 assert first.inner_text().strip();assert page.locator('#routeMap').is_hidden()
 return {'title':title,'firstText':first.inner_text(),'firstHref':first.get_attribute('href'),'firstY':first.bounding_box()['y'],'hash':page.evaluate('location.hash'),'focus':page.locator(':focus').inner_text()}
def research(page):
 page.locator('#csoiNavigation > summary').click();page.get_by_role('navigation',name='CSOI workspaces').get_by_role('link',name='Research progress / 研究进展',exact=True).click()
 expect(page.locator('#csoiEngineeringTasks [data-task-id]')).to_have_count(80,timeout=30000);settled(page)
def tool(page,id):
 if page.locator('#toolsMenu').get_attribute('open')is None:page.locator('#toolsMenu > summary').click()
 page.locator('#'+id).click()
try:
 with sync_playwright()as p,tempfile.TemporaryDirectory(prefix='csoi-navigation-')as tmp:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  for width,height in [(1440,900),(390,844)]:
   context=browser.new_context(viewport={'width':width,'height':height},has_touch=width==390,accept_downloads=True,reduced_motion='reduce');page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
   page.goto(BASE);ready(page);case={'viewport':[width,height],'checks':[]}
   page.evaluate("localStorage.setItem('csoi-navigation-existing-draft','preserve-me');sessionStorage.setItem('csoi-navigation-session','preserve-me')")
   for node in ['csp','lsps']:
    page.locator('#atlasGraph [data-node-id="'+node+'"] .station-hit').click();expect(page.locator('#inspector')).to_be_visible();assert page.locator('#details').inner_text().strip();page.locator('#closeDetails').click()
   expect(page.locator('#sourceResearchLink')).to_be_visible();case['checks'].append('Actual pointer clicks on original CSP and LSPS map stations open populated inspector; research entry remains reachable after map pan')
   page.locator('#sourceResearchLink').click();expect(page.locator('#csoiEngineeringTasks [data-task-id]')).to_have_count(80,timeout=30000);settled(page)
   for label,title,needle in [('打开 LSPS 地图与正文','LSPS 地图、正文与行动','lsps2020'),('只看地图记录','LSPS 地图记录','context%3Amap'),('打开 OP 逐页梳理','OP 逐页梳理','op2026%3Areview%3Apage')]:
    page.get_by_role('link',name=label,exact=True).click();observed=result(page,title);assert needle in observed['firstHref'];observed['clicked']=label
    page.screenshot(path=str(OUT/f'{width}-{needle.split("%")[0]}.png'))
    # Same-hash navigation must still return from the long progress area to results.
    page.get_by_role('link',name=label,exact=True).click();result(page,title)
    page.locator('#csoiResearchResults .csoi-records a').first.click();expect(page.locator('#csoiSourceReading')).to_be_visible(timeout=30000);settled(page)
    if title=='LSPS 地图记录':
     reading=page.locator('#csoiLspsContextReading');expect(reading).to_contain_text('地图实际像素与图例核对');reading.locator('summary').filter(has_text='项图例').click();assert reading.locator('details[open]').inner_text().strip()
    if title=='OP 逐页梳理':
     unit=page.locator('#csoiOpSourceReading [data-op-unit]').first;unit.locator(':scope > summary').click();expect(unit.locator('p').first).to_be_visible();assert unit.locator('p').first.inner_text().strip()
    detail_url=page.url;page.go_back();result(page,title);page.go_forward();expect(page.locator('#csoiSourceReading')).to_be_visible(timeout=30000);settled(page);assert page.url==detail_url
    page.reload();ready(page);expect(page.locator('#csoiSourceReading')).to_be_visible(timeout=30000);settled(page)
    assert page.evaluate("localStorage.getItem('csoi-navigation-existing-draft')")=='preserve-me'
    assert page.evaluate("sessionStorage.getItem('csoi-navigation-session')")=='preserve-me'
    page.go_back();result(page,title);case['checks'].append(observed);save()
   # Explicit deep-link cold entries and refresh must land on visible results too.
   for fragment,title in [('#/research?source=LSPS','LSPS 地图、正文与行动'),('#/research?domain=LSPS_MAP&source=LSPS','LSPS 地图记录'),('#/research?source=OP&domain=OP_PAGE','OP 逐页梳理')]:
    page.goto(BASE+fragment);ready(page);result(page,title);page.reload();ready(page);result(page,title)
   case['checks'].append('Cold deep links, browser back/forward and reload show target content; existing local/session values preserved')
   # Real query form and pagination, including a truthful empty result.
   page.get_by_role('navigation',name='Source research pages').get_by_role('link',name='下一页',exact=True).click();result(page,'OP 逐页梳理');expect(page.locator('#csoiResearchResults')).to_contain_text('OP PDF 26')
   page.get_by_role('textbox',name='Search source research').fill('no-match-navigation-fixture');page.get_by_role('button',name='查询来源内容',exact=True).click();expect(page.locator('#csoiResearchResults')).to_contain_text('当前快照没有匹配');settled(page);expect(page.locator('#csoiResearchResults h2')).to_be_in_viewport()
   case['checks'].append('Actual pagination and form submit; empty results visible with explicit recovery explanation')
   assert not errors,errors;case['status']='PASS';case['browserErrors']=errors;report['results'].append(case);save();context.close();print('PASS navigation actual-click/visibility/history/deep-link/storage at '+str(width),flush=True)
  browser.close()
 report['status']='PASS';save()
except BaseException as error:
 report['status']='FAILED';report['failure']={'type':type(error).__name__,'message':str(error)[:3000]};save();raise
finally:
 if server:server.shutdown()
