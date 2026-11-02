"""Real OP page/unit interactions and import negatives at desktop and mobile."""
from pathlib import Path
from urllib.parse import quote
import datetime,json,os,subprocess,tempfile
from playwright.sync_api import sync_playwright,expect
APP=Path(__file__).resolve().parents[1];OUT=APP/os.environ.get('ATLAS_OP_BROWSER_OUTPUT','qa/op-completion-20261102/browser');OUT.mkdir(parents=True,exist_ok=True)
BASE=os.environ.get('ATLAS_TEST_URL','http://127.0.0.1:8877/');plan=json.loads((APP/'sources/op-completion-review.json').read_text());results=[]
def go(page,path):page.evaluate('(path)=>location.hash="#"+path',path)
def research(page):
 go(page,'/research?source=OP');expect(page.locator('#csoiEngineeringTasks [data-task-id]')).to_have_count(80,timeout=30000)
def knowledge(page,id,query=''):
 go(page,'/knowledge/'+quote(id,safe='')+query);expect(page.locator('#csoiSourceReading')).to_contain_text('OP-PAGE-'+id.rsplit(':',1)[-1])
def tool(page,id):
 if page.locator('#toolsMenu').get_attribute('open') is None:page.locator('#toolsMenu>summary').click()
 page.locator('#'+id).click()
def download(page,name,path):
 with page.expect_download() as info:page.get_by_role('button',name=name,exact=True).click()
 info.value.save_as(str(path));return path
def export(page,path):
 go(page,'/atlas');expect(page.locator('#routeMap')).to_be_visible()
 with page.expect_download() as info:tool(page,'exportBtn')
 info.value.save_as(str(path));subprocess.run(['node',str(APP/'verify-snapshot.cjs'),str(path)],check=True)
def load(page,path):
 go(page,'/atlas');expect(page.locator('#routeMap')).to_be_visible();tool(page,'importSnapshotBtn');page.locator('#snapshotFile').set_input_files(str(path));expect(page.locator('#snapshotMessage')).to_contain_text('Explicit replacement required',timeout=30000);page.locator('#applySnapshot').click();expect(page.locator('#snapshotMessage')).to_contain_text('explicitly loaded in memory')
with tempfile.TemporaryDirectory(prefix='csoi-op-browser-')as tmp,sync_playwright()as p:
 tmp=Path(tmp);browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width,height in [(1440,900),(390,844)]:
  page=browser.new_page(viewport={'width':width,'height':height},reduced_motion='reduce',accept_downloads=True,has_touch=width==390);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(BASE);expect(page.locator('#contentCount')).to_have_text('127');research(page);expect(page.locator('#csoiOpReviewProgress')).to_contain_text('143 / 143');page.locator('#csoiOpReviewProgress').scroll_into_view_if_needed();page.screenshot(path=str(OUT/f'op-progress-{width}.png'))
  matrix=json.loads(download(page,'Export OP unit coverage JSON',tmp/f'units-{width}.json').read_text());assert len(matrix['rows'])==911 and all(r['verification']=='SOURCE_CHECKED_BOUNDED'for r in matrix['rows']);assert matrix['officialRelationships']==0
  opened=[];unit_ids=[]
  for node in plan['records']:
   if node['category']!='OP_PAGE':continue
   units=node['facts']['units'];groups=max(1,(len(units)+14)//15)
   for group in range(groups):
    knowledge(page,node['id'],'?page='+str(group+1));reading=page.locator('#csoiOpSourceReading');expect(reading).to_contain_text('本条与本轮逐页原件复核一致');current=units[group*15:(group+1)*15]
    expect(reading.locator('[data-op-unit]')).to_have_count(len(current))
    for unit in current:
     item=reading.locator('[data-op-unit="'+unit['id']+'"]');item.evaluate('(e)=>e.open=true');item.locator('details').evaluate_all('(els)=>els.forEach(e=>e.open=true)');body=item.inner_text();assert unit['summary']in body,unit['id']
     for condition in unit['conditions']+unit['qualifiers']:
      if isinstance(condition,str):assert condition in body,unit['id']
     item.locator('details').evaluate_all('(els)=>els.forEach(e=>e.open=false)');unit_ids.append(unit['id'])
    assert reading.get_by_role('link',name='打开官方 OP PDF 第 '+str(node['anchor']['pdfPage'])+' 页').get_attribute('href').endswith('#page='+str(node['anchor']['pdfPage']))
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    if group==0 and node['anchor']['pdfPage']in [28,73,116,121,132]:reading.get_by_role('heading',name='OP 全文有界梳理 / 计划、条件和预算',exact=True).scroll_into_view_if_needed();page.screenshot(path=str(OUT/f'op-page-{node["anchor"]["pdfPage"]}-{width}.png'))
   opened.append(node['id'])
  assert len(opened)==142 and len(unit_ids)==911 and len(set(unit_ids))==911
  # Real controls: per-page query, pagination and the original retained water activity.
  knowledge(page,'csoi:knowledge:op2026:review:page:073');reading=page.locator('#csoiOpSourceReading');reading.get_by_role('textbox',name='Search OP page units').fill('service');reading.get_by_role('button',name='查询本页',exact=True).click();expect(page).to_have_url(__import__('re').compile('q=service'))
  knowledge(page,'csoi:knowledge:op2026:review:page:112');page.get_by_role('link',name='本页单元下一组',exact=True).click();expect(page).to_have_url(__import__('re').compile('page=2'));assert page.locator('[data-op-unit]').count()<=15
  research(page);task=page.locator('[data-task-id="COI-011"]');task.evaluate('(e)=>e.open=true');expect(task).to_contain_text('验收条件：');expect(task).to_contain_text('具体缺口：')
  snapshot=tmp/f'current-{width}.json';export(page,snapshot)
  if width==1440:
   over=tmp/'oversize.json'
   with over.open('wb')as stream:stream.truncate(32*1024*1024+1)
   tool(page,'importSnapshotBtn');page.locator('#snapshotFile').set_input_files(str(over));expect(page.locator('#snapshotMessage')).to_contain_text('SNAPSHOT_TOO_LARGE');expect(page.locator('#applySnapshot')).to_be_disabled()
  code="""const fs=require('fs'),M=require('./atlas-model.js'),I=require('./atlas-intake.js'),G=require('./csoi-governance.js'),B=require('./qa/op-completion-20261102/baseline-prefix.json');(async()=>{const d=JSON.parse(fs.readFileSync(process.argv[1])).dataset,x=structuredClone(d);x.domain.sourceCatalogue=await I.correctStage(x.domain.sourceCatalogue,'csoi:smrc-op-2026:20261030','SOURCE_RETRIEVED',{actor:'QA',at:'2026-11-02T03:30:00.000Z',reason:'Browser OP source withdrawal'});fs.writeFileSync(process.argv[2],JSON.stringify(await M.exportSnapshot(x)));const e=M.domainIndex(d).get('csoi:knowledge:op2026:review:page:028'),r=structuredClone(e.data.csoiRecord);r.data.publicKnowledge.facts.units.find(u=>u.conditions.length).conditions=[];const y=await M.reviseResearchRecord(d,{id:e.id,expectedRevisionId:e.revisionId,record:await G.makeRecord(r),reason:'Missing OP action condition after source review'});fs.writeFileSync(process.argv[3],JSON.stringify(await M.exportSnapshot(y)));const old=structuredClone(d);old.domain.revisions=old.domain.revisions.slice(0,B.domainRevisions);old.domain.events=old.domain.events.slice(0,B.domainEvents);const by=new Map(old.domain.revisions.map(r=>[r.logicalId,{...r.record,revisionId:r.id}]));old.domain.entities=B.entityIds.map(id=>by.get(id));old.domain.assertions=B.assertionIds.map(id=>by.get(id));if(await M.objectDigest(old)!==B.datasetDigest)throw Error('V4_PREFIX_CHANGED');fs.writeFileSync(process.argv[4],JSON.stringify(await M.exportSnapshot(old)));})().catch(e=>{console.error(e);process.exitCode=1});"""
  withdrawn=tmp/f'withdrawn-{width}.json';edited=tmp/f'edited-{width}.json';old=tmp/f'old-{width}.json';subprocess.run(['node','-e',code,str(snapshot),str(withdrawn),str(edited),str(old)],cwd=APP,check=True)
  load(page,edited);knowledge(page,'csoi:knowledge:op2026:review:page:028');expect(page.locator('#csoiOpSourceReading')).to_contain_text('当前内容、来源或关联版本已变化');research(page);expect(page.locator('#csoiOpReviewProgress')).to_contain_text('142 / 143')
  load(page,withdrawn);research(page);expect(page.locator('#csoiOpReviewProgress')).to_contain_text('0 / 143');page.locator('#csoiOpReviewProgress').scroll_into_view_if_needed();page.screenshot(path=str(OUT/f'op-withdrawn-{width}.png'))
  load(page,old);research(page);expect(page.locator('#csoiOpReviewProgress')).to_contain_text('0 / 143');expect(page.locator('#csoiMetricReviewProgress')).to_contain_text('63 / 63');expect(page.locator('#csoiLspsReviewProgress')).to_contain_text('103 / 103')
  assert not errors,errors;results.append({'viewport':[width,height],'touchEnabled':width==390,'status':'PASS_TESTED_HERE','pageDetailsOpened':opened,'unitsExpandedAndRead':unit_ids,'sourceWithdrawal':'PASS','missingConditionLosesReview':'PASS','oldV4MissingOP':'PASS','exportIndependentRevalidation':'PASS','browserErrors':errors});page.close()
 browser.close()
(OUT/'results.json').write_text(json.dumps({'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':results},indent=2)+'\n')
print('PASS:142 OP pages and911 units expanded/read on desktop/mobile, actual query/pagination, source withdrawal, condition loss, v4 import and independent export verification')
