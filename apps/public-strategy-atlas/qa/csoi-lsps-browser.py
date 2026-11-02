"""Actual LSPS page/map reading, expanded semantic units, source conditions and import negatives."""
from pathlib import Path
from urllib.parse import quote
import csv,datetime,json,subprocess,tempfile
from playwright.sync_api import sync_playwright,expect
APP=Path(__file__).resolve().parents[1];OUT=APP/'qa/lsps-completion/browser';OUT.mkdir(parents=True,exist_ok=True)
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
with tempfile.TemporaryDirectory(prefix='csoi-lsps-browser-')as tmp,sync_playwright()as p:
 tmp=Path(tmp);browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);plan=json.loads((APP/'sources/lsps-context-review.json').read_text());total=len(plan['records'])
 for width,height in [(1440,900),(390,844)]:
  page=browser.new_page(viewport={'width':width,'height':height},reduced_motion='reduce',accept_downloads=True);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:8877/');expect(page.locator('#contentCount')).to_have_text('127');research(page,'?source=LSPS');expect(page.locator('#csoiLspsReviewProgress')).to_contain_text(f'{total} / {total}');assert page.get_by_role('navigation',name='LSPS reading views').get_by_role('link').count()==3;assert page.get_by_role('navigation',name='LSPS reading views').get_by_role('link').evaluate_all('(els)=>els.every(e=>e.getBoundingClientRect().height>=44)');page.locator('#csoiLspsReviewProgress').scroll_into_view_if_needed();page.screenshot(path=str(OUT/f'lsps-progress-{width}.png'))
  matrix=json.loads(download(page,'Export source coverage JSON',tmp/f'matrix-{width}.json').read_text());assert len(matrix['rows'])==114+total and all(r['verification']=='SOURCE_CHECKED_BOUNDED'for r in matrix['rows'])
  opened=[];units_read=[];maps_read=[]
  for n in plan['records']:
   knowledge(page,n['id']);expect(page.locator('#csoiSourceReading')).to_contain_text(n['code']);reading=page.locator('#csoiLspsContextReading');expect(reading).to_contain_text('本条与本轮原页复核内容一致');reading.locator('details').evaluate_all('(els)=>els.forEach(e=>e.open=true)')
   if n['category']=='LSPS_NARRATIVE':
    for unit in n['facts']['units']:
     item=reading.locator('[data-lsps-unit="'+unit['id']+'"]');assert item.get_attribute('open')is not None;body=item.inner_text();assert unit['summary']in body
     for condition in unit['conditions']+unit['qualifiers']:assert (condition if isinstance(condition,str)else condition['text'])in body
     units_read.append(unit['id'])
   else:
    m=n['facts']['map'];body=reading.inner_text();assert all(x['label']in body and x['symbol']in body for x in m['legend']);assert all(x in body for x in m['conditions']+m['qualifiers']);maps_read.append(m['id'])
   href=reading.get_by_role('link',name='打开官方 PDF 第 '+str(n['anchor']['pdfPage'])+' 页').get_attribute('href');assert href.endswith('#page='+str(n['anchor']['pdfPage']))
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');opened.append(n['id'])
   if n['code']in ['MAP-027','MAP-114','PAGE-056','PAGE-073']:
    reading.scroll_into_view_if_needed();page.screenshot(path=str(OUT/f'{n["code"]}-{width}.png'))
  assert len(units_read)==plan['counts']['semanticUnits'] and len(maps_read)==27
  knowledge(page,'csoi:knowledge:lsps2020:priority:12');expect(page.get_by_role('heading',name='Related source reading / 相关正文、地图与条件')).to_be_visible();assert page.locator('a[href*="context%3Apage%3A056"]').count()>0
  snapshot=tmp/f'current-{width}.json';export(page,snapshot)
  code="""const fs=require('fs'),M=require('./atlas-model.js'),I=require('./atlas-intake.js'),G=require('./csoi-governance.js'),B=require('./qa/lsps-completion/baseline-prefix.json');(async()=>{const d=JSON.parse(fs.readFileSync(process.argv[1])).dataset,x=structuredClone(d);x.domain.sourceCatalogue=await I.correctStage(x.domain.sourceCatalogue,'csoi:smrc-lsps-2020:20261030','SOURCE_RETRIEVED',{actor:'QA',at:new Date().toISOString(),reason:'Browser LSPS source withdrawal'});fs.writeFileSync(process.argv[2],JSON.stringify(await M.exportSnapshot(x)));const e=M.domainIndex(d).get('csoi:knowledge:lsps2020:context:map:114'),r=structuredClone(e.data.csoiRecord);r.data.publicKnowledge.facts.map.legend.find(x=>x.label.endsWith('Option 5')).label='Heavy Vehicle Investigation Routes: Option 4';const y=await M.reviseResearchRecord(d,{id:e.id,expectedRevisionId:e.revisionId,record:await G.makeRecord(r),reason:'Wrong source legend after review'});fs.writeFileSync(process.argv[3],JSON.stringify(await M.exportSnapshot(y)));const old=structuredClone(d);old.domain.revisions=old.domain.revisions.slice(0,B.domainRevisions);old.domain.events=old.domain.events.slice(0,B.domainEvents);const by=new Map(old.domain.revisions.map(r=>[r.logicalId,{...r.record,revisionId:r.id}]));old.domain.entities=B.entityIds.map(id=>by.get(id));old.domain.assertions=B.assertionIds.map(id=>by.get(id));if(await M.objectDigest(old)!==B.datasetDigest)throw Error('OLD_SNAPSHOT_CHANGED');fs.writeFileSync(process.argv[4],JSON.stringify(await M.exportSnapshot(old)));})().catch(e=>{console.error(e);process.exitCode=1});"""
  withdrawn=tmp/f'withdrawn-{width}.json';edited=tmp/f'edited-{width}.json';old=tmp/f'old-{width}.json';subprocess.run(['node','-e',code,str(snapshot),str(withdrawn),str(edited),str(old)],cwd=APP,check=True)
  load(page,edited);knowledge(page,'csoi:knowledge:lsps2020:context:map:114');expect(page.locator('#csoiLspsContextReading')).to_contain_text('当前记录与本轮复核内容不一致');research(page);expect(page.locator('#csoiLspsReviewProgress')).to_contain_text(f'{total-1} / {total}');page.screenshot(path=str(OUT/f'wrong-legend-{width}.png'))
  load(page,withdrawn);research(page);expect(page.locator('#csoiLspsReviewProgress')).to_contain_text(f'0 / {total}');knowledge(page,plan['records'][0]['id']);expect(page.locator('#csoiLspsContextReading')).to_contain_text('当前记录与本轮复核内容不一致');page.screenshot(path=str(OUT/f'withdrawn-{width}.png'))
  load(page,old);research(page);expect(page.locator('#csoiLspsReviewProgress')).to_contain_text(f'0 / {total}');expect(page.locator('#csoiMetricReviewProgress')).to_contain_text('63 / 63');page.screenshot(path=str(OUT/f'v3-context-missing-{width}.png'))
  assert not errors,errors;results.append({'viewport':[width,height],'status':'PASS_TESTED_HERE','detailsActuallyOpened':opened,'unitsExpandedAndRead':units_read,'mapLegendsExpandedAndRead':maps_read,'matrixRows':114+total,'sourceWithdrawal':'PASS','changedLegendLosesReview':'PASS','oldV3MissingContext':'PASS','exportIndependentRevalidation':'PASS','browserErrors':errors});page.close()
 browser.close()
(OUT/'results.json').write_text(json.dumps({'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':results},indent=2)+'\n')
print('PASS: actual LSPS page/map details and expanded units/legends at desktop/mobile; source withdrawal, wrong legend, old v3 import and independent export verification')
