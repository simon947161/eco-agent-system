"""Source coverage, actual navigation, exports and invalidation at desktop/mobile."""
from pathlib import Path
from urllib.parse import quote
import csv,datetime,json,subprocess,tempfile
from playwright.sync_api import sync_playwright,expect
APP=Path(__file__).resolve().parents[1];OUT=APP/'qa/strategy-completion/browser';OUT.mkdir(parents=True,exist_ok=True)
results=[]
def go(page,path):
 page.evaluate('(path)=>location.hash="#"+path',path)
 expect(page.locator('#csoiWorkspace h1')).to_be_visible()
def research(page,suffix=''):
 go(page,'/research'+suffix);expect(page.locator('#csoiEngineeringTasks [data-task-id]')).to_have_count(80,timeout=30000)
def knowledge(page,id):
 go(page,'/knowledge/'+quote(id,safe=''));expect(page.locator('#csoiSourceReading')).to_be_visible()
def tool(page,id):
 if page.locator('#toolsMenu').get_attribute('open')is None:page.locator('#toolsMenu>summary').click()
 page.locator('#'+id).click()
def download(page,name,path):
 with page.expect_download()as info:page.get_by_role('button',name=name,exact=True).click()
 info.value.save_as(str(path));return path
def export(page,path):
 page.evaluate('location.hash="#/atlas"');expect(page.locator('#routeMap')).to_be_visible()
 with page.expect_download()as info:tool(page,'exportBtn')
 info.value.save_as(str(path));subprocess.run(['node',str(APP/'verify-snapshot.cjs'),str(path)],check=True)
def load(page,path):
 page.evaluate('location.hash="#/atlas"');expect(page.locator('#routeMap')).to_be_visible();tool(page,'importSnapshotBtn');page.locator('#snapshotFile').set_input_files(str(path));expect(page.locator('#snapshotMessage')).to_contain_text('Explicit replacement required',timeout=30000);page.locator('#applySnapshot').click();expect(page.locator('#snapshotMessage')).to_contain_text('explicitly loaded in memory')
with tempfile.TemporaryDirectory(prefix='csoi-strategy-browser-')as tmp,sync_playwright()as p:
 tmp=Path(tmp);browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width,height in [(1440,900),(390,844)]:
  page=browser.new_page(viewport={'width':width,'height':height},reduced_motion='reduce',accept_downloads=True);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:8877/');expect(page.locator('#contentCount')).to_have_text('127');expect(page.locator('#routeMap')).to_be_visible();page.locator('#sourceResearchLink').click();expect(page.locator('#csoiEngineeringTasks [data-task-id]')).to_have_count(80,timeout=30000)
  expect(page.locator('#csoiResearchProgress')).to_contain_text('80 项是工程任务');expect(page.locator('#csoiWorkspace')).to_contain_text('CSP_INDICATOR: 63 / 63');expect(page.locator('#csoiWorkspace')).to_contain_text('LSPS_IMPLEMENTATION_ACTION: 83 / 83');expect(page.locator('#csoiWorkspace')).to_contain_text('WATER_ACTIVITY: 8 / 8');page.screenshot(path=str(OUT/f'research-progress-{width}.png'))
  matrix=json.loads(download(page,'Export source coverage JSON',tmp/f'matrix-{width}.json').read_text());assert len(matrix['rows'])==252;assert all(r['verification']=='SOURCE_CHECKED_BOUNDED' for r in matrix['rows']);assert matrix['officialRelationships']==0
  with download(page,'Export source coverage CSV',tmp/f'matrix-{width}.csv').open(encoding='utf-8-sig',newline='')as f:assert len(list(csv.DictReader(f)))==252
  scopes=json.loads(download(page,'Export page review scope JSON',tmp/f'pages-{width}.json').read_text());assert [d['totalPages']for d in scopes['documents']]==[36,118,142]
  visited={}
  for family,total in [('CSP',127),('LSPS',114),('OP',11)]:
   research(page,'?source='+family);ids=set()
   while True:
    links=page.locator('#csoiWorkspace section').filter(has=page.get_by_role('heading',name='可打开的来源条目',exact=True)).locator('a[href*="/knowledge/"]');ids.update(links.evaluate_all('(els)=>els.map(e=>e.getAttribute("href"))'))
    next_link=page.get_by_role('link',name='下一页',exact=True)
    if not next_link.count():break
    before=page.url;next_link.click();page.wait_for_function('(old)=>location.href!==old',arg=before);expect(page.locator('#csoiEngineeringTasks [data-task-id]')).to_have_count(80,timeout=30000)
   assert len(ids)==total,(family,len(ids));visited[family]=len(ids)
  research(page,'?source=CSP');page.get_by_role('textbox',name='Search source research').fill('7519');page.get_by_role('button',name='查询来源内容',exact=True).click();expect(page.locator('#csoiWorkspace')).to_contain_text('当前查询：1 项');qmatrix=json.loads(download(page,'Export source coverage JSON',tmp/f'query-{width}.json').read_text());assert len(qmatrix['rows'])==1;page.locator('#csoiWorkspace section').filter(has=page.get_by_role('heading',name='可打开的来源条目',exact=True)).locator('a').click();expect(page.locator('#csoiSourceReading')).to_contain_text('7519');expect(page.locator('#csoiSourceReading')).to_contain_text('UNKNOWN');page.screenshot(path=str(OUT/f'water-unit-unknown-{width}.png'))
  knowledge(page,'csoi:knowledge:csp2035:strategy:6.1');expect(page.locator('#csoiSourceReading')).to_contain_text('原文角色');expect(page.locator('#csoiSourceReading')).to_contain_text('原文伙伴')
  knowledge(page,'csoi:knowledge:lsps2020:action:3.2');expect(page.locator('#csoiSourceReading')).to_contain_text('Historical');expect(page.locator('#csoiSourceReading').get_by_role('link',name='Open conflicting source occurrence')).not_to_have_count(0)
  page.locator('#csoiSourceReading').get_by_role('link',name='Open conflicting source occurrence').first.click();expect(page.locator('#csoiSourceReading')).to_be_visible();page.screenshot(path=str(OUT/f'lsps-conflict-{width}.png'))
  knowledge(page,'csoi:knowledge:op2026:water:activity:service-requests');expect(page.locator('#csoiWorkspace')).to_contain_text('EXPLICIT_DOCUMENT_REFERENCE');page.screenshot(path=str(OUT/f'op-references-{width}.png'));page.locator('a[href*="csp2035%3Astrategy%3A8.2"]').first.click();expect(page.locator('#csoiWorkspace')).to_contain_text('Published OP references back to this strategy');assert page.locator('a[href*="service-requests"]').count()>0
  snapshot=tmp/f'snapshot-{width}.json';export(page,snapshot);data=json.loads(snapshot.read_text())['dataset'];assert len(data['domain']['entities'])==389
  code="""const fs=require('fs'),M=require('./atlas-model.js'),I=require('./atlas-intake.js'),G=require('./csoi-governance.js'),B=require('./qa/strategy-completion/baseline-prefix.json');(async()=>{const d=JSON.parse(fs.readFileSync(process.argv[1])).dataset,x=structuredClone(d);x.domain.sourceCatalogue=await I.correctStage(x.domain.sourceCatalogue,'csoi:smrc-csp-full-2025:20261030','SOURCE_RETRIEVED',{actor:'QA',at:new Date().toISOString(),reason:'Browser isolated source withdrawal'});fs.writeFileSync(process.argv[2],JSON.stringify(await M.exportSnapshot(x)));const parent=M.domainIndex(d).get('csoi:knowledge:csp2035:objective:6'),r=await G.makeRecord({...parent.data.csoiRecord,state:'WITHDRAWN',observedAt:new Date().toISOString()}),y=await M.reviseResearchRecord(d,{id:parent.id,expectedRevisionId:parent.revisionId,record:r,reason:'Browser parent withdrawal'});fs.writeFileSync(process.argv[3],JSON.stringify(await M.exportSnapshot(y)));const old=structuredClone(d);old.domain.revisions=old.domain.revisions.slice(0,B.domainRevisions);old.domain.events=old.domain.events.slice(0,B.domainEvents);const by=new Map(old.domain.revisions.map(r=>[r.logicalId,{...r.record,revisionId:r.id}]));old.domain.entities=B.entityIds.map(id=>by.get(id));old.domain.assertions=B.assertionIds.map(id=>by.get(id));if(await M.objectDigest(old)!==B.datasetDigest)throw Error('OLD_SNAPSHOT_CHANGED');fs.writeFileSync(process.argv[4],JSON.stringify(await M.exportSnapshot(old)));})().catch(e=>{console.error(e);process.exitCode=1});"""
  withdrawn=tmp/f'withdrawn-{width}.json';parent=tmp/f'parent-{width}.json';old=tmp/f'old-{width}.json';subprocess.run(['node','-e',code,str(snapshot),str(withdrawn),str(parent),str(old)],cwd=APP,check=True)
  load(page,parent);knowledge(page,'csoi:knowledge:csp2035:strategy:6.1');expect(page.locator('#csoiSourceReading')).to_contain_text('已经失效');research(page);m=json.loads(download(page,'Export source coverage JSON',tmp/f'parent-matrix-{width}.json').read_text());assert next(r for r in m['rows']if r['id'].endswith('strategy:6.1'))['verification']=='INVALIDATED'
  load(page,withdrawn);research(page);m=json.loads(download(page,'Export source coverage JSON',tmp/f'withdrawn-matrix-{width}.json').read_text());assert all(r['verification']=='INVALIDATED'for r in m['rows']if r['family']=='CSP' or r['category']=='WATER_ACTIVITY');assert all(r['verification']=='SOURCE_CHECKED_BOUNDED'for r in m['rows']if r['family']=='LSPS');page.screenshot(path=str(OUT/f'source-withdrawn-{width}.png'))
  load(page,old);research(page);m=json.loads(download(page,'Export source coverage JSON',tmp/f'old-matrix-{width}.json').read_text());assert all(r['verification']=='NOT_IMPLEMENTED'for r in m['rows']);expect(page.locator('#csoiWorkspace')).to_contain_text('CSP_INDICATOR: 0 / 63');page.screenshot(path=str(OUT/f'old-snapshot-missing-{width}.png'));page.get_by_role('link',name='下一页',exact=True).click();expect(page.locator('#csoiResearchMatrix > details')).to_have_count(25)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');assert not errors,errors
  results.append({'viewport':[width,height],'status':'PASS_TESTED_HERE','allSourceItemsVisited':visited,'matrixRows':252,'engineeringTasksShown':80,'exportAndImport':'PASS','sourceAndParentWithdrawal':'PASS','historicalSnapshotMissing':'PASS','browserErrors':errors});page.close()
 browser.close()
(OUT/'results.json').write_text(json.dumps({'generatedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':results},indent=2)+'\n')
print('PASS: desktop/mobile252source items and80engineering task states, source scope exports, ambiguous units, conflicting actions, OP references, parent/source withdrawal and old snapshot missing evidence')
