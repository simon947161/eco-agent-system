"""Read-only local audit. No existing app tests/append/save/import actions are used."""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from urllib.parse import quote,urlparse
import threading,json,datetime,traceback,csv
from playwright.sync_api import sync_playwright,expect
APP=Path('/tmp/csoi-integrity-audit-20261031/readonly-head/apps/public-strategy-atlas');OUT=Path(__file__).parent;BASE='http://127.0.0.1:8891/'
model=json.loads((OUT/'model-results.json').read_text());result={'head':model['sha'],'startedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'readOnly':True,'sourcePaths':[],'routeSmoke':[],'unsupportedQueries':[],'externalRequests':[],'errors':[]}
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',8891),partial(Quiet,directory=str(APP)));threading.Thread(target=server.serve_forever,daemon=True).start()
def navigate(page,route,heading=None):
 page.goto(BASE+route,wait_until='domcontentloaded');expect(page.locator('#csoiWorkspace h1')).to_have_text(heading or 'Inside the knowledge',timeout=45000)
route_samples=[('atlas','/atlas',None),('knowledge','/knowledge/csp%3Acontent','Inside the knowledge'),('strategy','/strategy','Strategy and plans'),('strategy-detail','/strategy/csp','Strategy dossier'),('wcos','/domains/wcos','WCOS — controlled interface'),('wcos-domain','/domains/wcos/ltw','WCOS professional knowledge'),('phe','/domains/phe','Public health and environment'),('phe-domain','/domains/phe/ossm','Public professional knowledge'),('data','/data','Data layers and evidence'),('data-record','/data/csoi%3Asource-note%3Asmrc-csp-full-2025%3Acarbon-p30','Layer record and lineage'),('operations','/operations','Operations and work'),('operation','/operations/csoi%3Apublished-plan%3Afood-2026%3Aprogramme','Work card'),('calendar','/calendar','Operational year'),('calendar-item','/calendar/calendar%3ACALENDAR%3A2026%3Ayear','Calendar work item'),('metrics','/metrics','Metrics and evidence'),('metric','/metrics/csp2035-carbon-per-capita-baseline','Metric dossier'),('resources','/resources','Resource requirements'),('resource','/resources/synthetic-water-output','Resource dossier'),('sources','/sources','Source register'),('source','/sources/csoi%3Asmrc-csp-full-2025%3A20261030','Source evidence'),('compare','/compare','Compare records across paths'),('path-compare','/compare/paths','Typed path-set comparison'),('discovery','/discovery','Discovery and challenge'),('audit','/audit','History and independent audit'),('coverage','/coverage','Coverage and gaps'),('assistant','/assistant','Michele — draft assistance')]
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  result['browserVersion']=browser.version
  for width,height in [(1440,900),(390,844)]:
   context=browser.new_context(viewport={'width':width,'height':height},reduced_motion='reduce')
   def gate(route):
    u=urlparse(route.request.url)
    if u.hostname in ['127.0.0.1','localhost']:route.continue_()
    else:result['externalRequests'].append({'url':route.request.url,'action':'BLOCKED_READ_ONLY_AUDIT'});route.abort()
   context.route('**/*',gate);page=context.new_page();page.on('pageerror',lambda e:result['errors'].append(str(e)))
   for row in model['rows']:
    record={'testId':row['testId'],'viewport':[width,height],'sourceRoute':row['sourceRoute'],'recordRoute':row['webRoute'],'recordId':row['id'],'classification':'RESEARCH_METADATA_NOT_ADMITTED_CHAIN'}
    try:
     navigate(page,row['sourceRoute'],'Source evidence');expect(page.locator('#csoiWorkspace')).to_contain_text(row['sourceTitle']);
     # Actually follow source→chapter→clause→record links where governed containment exists.
     hops=list(reversed(row['lineageNodeIds']))[1:] if row['lineageNodeIds'] else [row['id']]
     for hop in hops:
      page.locator('a[href="#/knowledge/'+quote(hop,safe='')+'"]').first.click();expect(page.locator('#csoiWorkspace h1')).to_have_text('Inside the knowledge',timeout=45000)
     expect(page.locator('#csoiWorkspace')).to_contain_text('PENDING');expect(page.locator('#csoiWorkspace')).to_contain_text('official linkage UNKNOWN');record['sourceToUiLinkTraversal']='PASS';record['linkHops']=len(hops)
     record['locatorDisplayed']=row['locator'] in page.locator('#csoiWorkspace').inner_text();record['officialUnknownDisplayed']='UNKNOWN' in page.locator('#csoiWorkspace').inner_text()
     back=page.get_by_role('link',name='Original source receipt and review gates',exact=True)
     if back.count():back.click();expect(page.locator('#csoiWorkspace h1')).to_have_text('Source evidence');record['reverseInternalReceiptLink']='PASS'
     else:record['reverseInternalReceiptLink']='MISSING_GENERIC_NOTE_OR_PLAN_LINK_PROVENANCE_TEXT_ONLY'
     if row['testId'] in ['T01','T05','T07','T10']:
      navigate(page,row['webRoute']);page.screenshot(path=str(OUT/(row['testId']+'-'+str(width)+'.png')))
     page.goto(BASE+'#/atlas');expect(page.locator('#routeMap')).to_be_visible(timeout=45000);page.locator('#toolsMenu>summary').click();page.locator('#searchToolsBtn').click();page.locator('#recordQuery').fill(row['id']);page.locator('#searchRecords').click();expect(page.locator('#recordResults')).to_contain_text('1 matches.',timeout=20000);record['exactUserQuery']='PASS';record['searchResultCount']=1;record['status']='PASS_UI_TRACE_ONLY'
    except Exception as error:
     record['status']='FAIL';record['error']=str(error);page.screenshot(path=str(OUT/('FAIL-'+row['testId']+'-'+str(width)+'.png')))
    result['sourcePaths'].append(record)
   # Negative free-text queries use the actual query control and retain zero as zero.
   for q in ['QA_NO_SUCH_OFFICIAL_RELATION_20261031','Council water operations emissions savings 2026 verified actual','7519']:
    page.goto(BASE+'#/atlas');expect(page.locator('#routeMap')).to_be_visible();page.locator('#toolsMenu>summary').click();page.locator('#searchToolsBtn').click();page.locator('#recordQuery').fill(q);page.locator('#searchRecords').click();text=page.locator('#recordResults').inner_text();result['unsupportedQueries'].append({'viewport':[width,height],'query':q,'actualResult':text,'expected':'0 matches; no invented result','status':'PASS_ZERO' if text.startswith('0 matches.') else 'INVESTIGATE'})
    if q=='7519':page.screenshot(path=str(OUT/('published-water-7519-query-gap-'+str(width)+'.png')))
   # Route pattern smoke coverage measures presentation only, not empty-context completeness.
   for name,route,heading in route_samples:
    item={'routePatternName':name,'sampleUrl':'#'+route,'viewport':[width,height]}
    try:
     page.goto(BASE+'#'+route,wait_until='domcontentloaded')
     if name=='atlas':expect(page.locator('#routeMap')).to_be_visible(timeout=45000)
     else:expect(page.locator('#csoiWorkspace h1')).to_have_text(heading,timeout=45000)
     body=page.locator('#csoiWorkspace').inner_text() if name!='atlas' else ''
     item['sampleHasMissingObjectWarning']=any(s in body for s in ['not found','No record with','No object with','No layer record'])
     item['horizontalOverflow']=page.evaluate('document.documentElement.scrollWidth>innerWidth');item['status']='PASS_RENDER_ONLY'
    except Exception as error:item['status']='FAIL';item['error']=str(error)
    result['routeSmoke'].append(item)
   context.close()
  browser.close()
except Exception as error:result['fatal']=str(error);result['traceback']=traceback.format_exc()
finally:
 server.shutdown();server.server_close();result['finishedAt']=datetime.datetime.now(datetime.timezone.utc).isoformat();(OUT/'browser-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'sourceTests':len(result['sourcePaths']),'sourceFailures':[r['testId'] for r in result['sourcePaths'] if r['status']=='FAIL'],'routeSmokeCount':len(result['routeSmoke']),'routeFailures':[r['routePatternName'] for r in result['routeSmoke'] if r['status']=='FAIL'],'scriptErrors':result['errors'],'fatal':result.get('fatal')},ensure_ascii=False))
