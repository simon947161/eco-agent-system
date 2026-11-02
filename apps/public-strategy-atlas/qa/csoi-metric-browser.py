"""Actual desktop/mobile reading of all63 reviewed indicators and stale review negatives."""
from pathlib import Path
from urllib.parse import quote
import csv,datetime,json,subprocess,tempfile
from playwright.sync_api import sync_playwright,expect
APP=Path(__file__).resolve().parents[1];OUT=APP/'qa/csp-metric-review/browser';OUT.mkdir(parents=True,exist_ok=True)
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
with tempfile.TemporaryDirectory(prefix='csoi-metric-browser-')as tmp,sync_playwright()as p:
 tmp=Path(tmp);browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);plan=json.loads((APP/'sources/csp-indicator-review.json').read_text())
 for width,height in [(1440,900),(390,844)]:
  page=browser.new_page(viewport={'width':width,'height':height},reduced_motion='reduce',accept_downloads=True);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:8877/');expect(page.locator('#contentCount')).to_have_text('127');research(page,'?source=CSP&domain=CSP_INDICATOR');expect(page.locator('#csoiMetricReviewProgress')).to_contain_text('63 / 63');page.screenshot(path=str(OUT/f'metric-progress-{width}.png'))
  matrix=json.loads(download(page,'Export source coverage JSON',tmp/f'matrix-{width}.json').read_text());assert len(matrix['rows'])==63 and all(r['semanticReview']=='SECOND_SOURCE_REVIEW_CURRENT'for r in matrix['rows'])
  with download(page,'Export source coverage CSV',tmp/f'matrix-{width}.csv').open(encoding='utf-8-sig',newline='')as f:assert len(list(csv.DictReader(f)))==63
  opened=[]
  for row in plan['records']:
   n=row['node'];knowledge(page,n['id']);expect(page.locator('#csoiSourceReading')).to_contain_text(n['code']);review=page.locator('#csoiMetricSemanticReview');expect(review).to_contain_text('本条已逐项对照原页复核');expect(review).to_contain_text(n['facts']['semanticReview']['definition']);expect(review).to_contain_text(n['facts']['semanticReview']['calculation']);assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');opened.append(n['id'])
   if n['code']in ['CSP-KPI-29-community-24','CSP-KPI-30-economy-02','CSP-KPI-31-infrastructure-05']:
    review.scroll_into_view_if_needed();page.screenshot(path=str(OUT/f'{n["code"]}-{width}.png'))
  snapshot=tmp/f'current-{width}.json';export(page,snapshot)
  code="""const fs=require('fs'),M=require('./atlas-model.js'),I=require('./atlas-intake.js'),G=require('./csoi-governance.js'),B=require('./qa/csp-metric-review/baseline-prefix.json');(async()=>{const d=JSON.parse(fs.readFileSync(process.argv[1])).dataset,x=structuredClone(d);x.domain.sourceCatalogue=await I.correctStage(x.domain.sourceCatalogue,'csoi:smrc-csp-full-2025:20261030','SOURCE_RETRIEVED',{actor:'QA',at:new Date().toISOString(),reason:'Browser source withdrawal'});fs.writeFileSync(process.argv[2],JSON.stringify(await M.exportSnapshot(x)));const e=M.domainIndex(d).get('csoi:knowledge:csp2035:indicator:29-community-24'),record=await G.makeRecord({...e.data.csoiRecord,data:{...e.data.csoiRecord.data,summary:'Locally edited after semantic review.'}}),y=await M.reviseResearchRecord(d,{id:e.id,expectedRevisionId:e.revisionId,record,reason:'Local post-review edit'});fs.writeFileSync(process.argv[3],JSON.stringify(await M.exportSnapshot(y)));const old=structuredClone(d);old.domain.revisions=old.domain.revisions.slice(0,B.domainRevisions);old.domain.events=old.domain.events.slice(0,B.domainEvents);const by=new Map(old.domain.revisions.map(r=>[r.logicalId,{...r.record,revisionId:r.id}]));old.domain.entities=B.entityIds.map(id=>by.get(id));old.domain.assertions=B.assertionIds.map(id=>by.get(id));if(await M.objectDigest(old)!==B.datasetDigest)throw Error('OLD_SNAPSHOT_CHANGED');fs.writeFileSync(process.argv[4],JSON.stringify(await M.exportSnapshot(old)));})().catch(e=>{console.error(e);process.exitCode=1});"""
  withdrawn=tmp/f'withdrawn-{width}.json';edited=tmp/f'edited-{width}.json';old=tmp/f'old-{width}.json';subprocess.run(['node','-e',code,str(snapshot),str(withdrawn),str(edited),str(old)],cwd=APP,check=True)
  load(page,edited);knowledge(page,'csoi:knowledge:csp2035:indicator:29-community-24');expect(page.locator('#csoiMetricSemanticReview')).to_contain_text('属于历史版本');research(page);expect(page.locator('#csoiMetricReviewProgress')).to_contain_text('62 / 63')
  load(page,withdrawn);research(page);expect(page.locator('#csoiMetricReviewProgress')).to_contain_text('0 / 63');knowledge(page,plan['records'][0]['id']);expect(page.locator('#csoiMetricSemanticReview')).to_contain_text('属于历史版本');page.screenshot(path=str(OUT/f'review-withdrawn-{width}.png'))
  load(page,old);research(page);expect(page.locator('#csoiMetricReviewProgress')).to_contain_text('0 / 63');knowledge(page,plan['records'][0]['id']);expect(page.locator('#csoiMetricSemanticReview')).to_have_count(0);page.screenshot(path=str(OUT/f'v2-review-missing-{width}.png'))
  assert not errors,errors;results.append({'viewport':[width,height],'status':'PASS_TESTED_HERE','detailsActuallyOpened':opened,'semanticDefinitionAndCalculationDisplayed':63,'matrixExportRows':63,'sourceWithdrawal':'PASS','postReviewLocalEdit':'PASS','oldV2SnapshotNotPromoted':'PASS','exportIndependentRevalidation':'PASS','browserErrors':errors});page.close()
 browser.close()
(OUT/'results.json').write_text(json.dumps({'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':results},indent=2)+'\n')
print('PASS: all63 actual detail views at desktop/mobile, meaning/calculation display, matrix/snapshot exports, source withdrawal, local edits and v2 imports do not retain current semantic-review status')
