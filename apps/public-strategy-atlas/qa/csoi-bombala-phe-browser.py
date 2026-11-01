"""Real desktop/mobile Bombala PHE flow on the remediated canonical app; no deployment."""
from pathlib import Path
from urllib.parse import quote
import json,datetime,tempfile,subprocess
from playwright.sync_api import sync_playwright,expect
APP=Path(__file__).resolve().parents[1];OUT=APP/'qa/bombala-phe';OUT.mkdir(exist_ok=True);results=[]
SOIL='csoi:dcp:bombala2012:3:1:5:A9:soil';RURAL='csoi:dcp:bombala2012:4:5:4:A2';SOURCE='csoi:smrc-dcp-bombala-2014:20261030'
def tool(page,id):
 if page.locator('#toolsMenu').get_attribute('open')is None:page.locator('#toolsMenu>summary').click()
 page.locator('#'+id).click()
def export(page,path):
 page.evaluate('location.hash="#/atlas"');expect(page.locator('#routeMap')).to_be_visible()
 with page.expect_download()as download:tool(page,'exportBtn')
 download.value.save_as(str(path));subprocess.run(['node',str(APP/'verify-snapshot.cjs'),str(path)],check=True)
def import_snapshot(page,path):
 page.evaluate('location.hash="#/atlas"');expect(page.locator('#routeMap')).to_be_visible();tool(page,'importSnapshotBtn');page.locator('#snapshotFile').set_input_files(str(path));expect(page.locator('#snapshotMessage')).to_contain_text('Explicit replacement required',timeout=30000);page.locator('#applySnapshot').click();expect(page.locator('#snapshotMessage')).to_contain_text('explicitly loaded in memory')
def phe(page):page.evaluate('location.hash="#/domains/phe/ossm"');expect(page.locator('#csoiPheHistorical [data-clause-id]')).to_have_count(11,timeout=30000)
with tempfile.TemporaryDirectory(prefix='bombala-phe-browser-')as tmp,sync_playwright()as p:
 tmp=Path(tmp);browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width,height in [(1440,900),(390,844)]:
  page=browser.new_page(viewport={'width':width,'height':height},reduced_motion='reduce',accept_downloads=True);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:8877/');expect(page.locator('#contentCount')).to_have_text('127');expect(page.locator('#routeMap')).to_be_visible();phe(page)
  host=page.locator('#csoiPheHistorical');gaps=page.locator('#csoiPheEvidenceGaps');expect(gaps.locator('[data-evidence-gap]')).to_have_count(2);expect(gaps).to_contain_text('not a Council inspection deadline');expect(gaps.locator('[data-evidence-gap=current-rule] dt').filter(has_text='currentSourceId').locator('xpath=following-sibling::dd[1]')).to_have_text('null');gaps.scroll_into_view_if_needed();page.screenshot(path=str(OUT/f'evidence-gaps-{width}.png'))
  expect(host.locator('[data-clause-id*="bombala2012"]')).to_have_count(5)
  for clause,condition,locator in [(SOIL,'Reticulated sewerage is unavailable.','PDF page 55, printed page 34'),(RURAL,'rural-development','PDF page 85, printed page 64')]:
   card=host.locator('[data-clause-id="'+clause+'"]');expect(card).to_contain_text(condition);expect(card).to_contain_text(locator);card.scroll_into_view_if_needed();page.screenshot(path=str(OUT/f'bombala-{"soil"if clause==SOIL else"rural"}-{width}.png'))
   card.locator('summary').click();expect(card).to_contain_text('normalizedPageDigest');expect(card).to_contain_text('parentContext');expect(card).to_contain_text('revisionId')
   card.get_by_role('link',name='Read historical clause',exact=True).click();expect(page.locator('#csoiWorkspace')).to_contain_text('SOURCE_PINNED_RESEARCH_PENDING_REVIEW');page.get_by_role('link',name='Return to on-site sewage evidence',exact=True).click()
   card.get_by_role('link',name='Choose own review date',exact=True).click();page.locator('input[name=sourceReviewDate]').fill('2026-11-06');page.locator('input[name=sourceReviewHours]').fill('1.25');page.get_by_role('button',name='Append independent review plan',exact=True).click()
   expect(page.locator('#csoiWorkspace h1')).to_have_text('Calendar work item',timeout=30000);expect(page.locator('#csoiWorkspace')).to_contain_text('NOT_CREATED');expect(page.locator('#csoiWorkspace')).to_contain_text('does not resolve missing current-rule');page.screenshot(path=str(OUT/f'bombala-calendar-{width}.png'))
   page.get_by_role('link',name='Open work dossier',exact=True).click();expect(page.locator('#csoiWorkspace')).to_contain_text('ASSUMED');expect(page.locator('#csoiWorkspace')).to_contain_text('actualSpend');page.get_by_role('link',name='Return to on-site sewage evidence',exact=True).click();expect(card.get_by_role('link',name='Annual calendar · 2026-11-06',exact=True)).to_be_visible();expect(gaps.locator('[data-evidence-gap]')).to_have_count(2);expect(gaps.locator('[data-evidence-gap=current-rule] dt').filter(has_text='resolved').locator('xpath=following-sibling::dd[1]')).to_have_text('false')
  page.get_by_role('link',name='Compare Bombala and Cooma evidence paths',exact=True).click();page.get_by_role('button',name='Inspect pinned path sets',exact=True).click();expect(page.locator('#csoiWorkspace')).to_contain_text('Metadata compatibility: CONFLICT',timeout=30000)
  with page.expect_download()as download:page.get_by_role('button',name='Export pinned path comparison proof',exact=True).click()
  proof=tmp/f'proof-{width}.json';download.value.save_as(str(proof));snapshot=tmp/f'snapshot-{width}.json';export(page,snapshot);subprocess.run(['node',str(APP/'verify-paths.cjs'),str(snapshot),str(proof)],check=True)
  data=json.loads(snapshot.read_text())['dataset'];index={e['id']:e for e in data['domain']['entities']};assert len(index)==139;assert len(data['domain']['assertions'])==48;assert len(data['contentItems'])==127;assert index['csoi:dcp:snowy2013:A2:4:1:drainage']['data']['csoiRecord']['state']=='WITHDRAWN'
  plans=[e for e in index.values()if e.get('data',{}).get('csoiRecord',{}).get('data',{}).get('reviewPlan')];assert len(plans)==2
  for task in plans:
   plan=task['data']['csoiRecord']['data']['reviewPlan'];assert plan['clauseRevisionId']==index[plan['clauseId']]['revisionId'];assert task['provenance']['locator']==index[plan['clauseId']]['provenance']['locator'];assert plan['actualHours']=='UNKNOWN'
  parent=tmp/f'parent-{width}.json';withdrawn=tmp/f'source-{width}.json'
  code="""const fs=require('fs'),M=require('./atlas-model.js'),G=require('./csoi-governance.js'),I=require('./atlas-intake.js');(async()=>{const d=JSON.parse(fs.readFileSync(process.argv[1])).dataset,p=M.domainIndex(d).get('csoi:dcp:bombala2012:3:1:5:A9'),record=await G.makeRecord({...p.data.csoiRecord,state:'WITHDRAWN',observedAt:new Date().toISOString()}),parent=await M.reviseResearchRecord(d,{id:p.id,expectedRevisionId:p.revisionId,record,reason:'Synthetic browser parent withdrawal'});fs.writeFileSync(process.argv[2],JSON.stringify(await M.exportSnapshot(parent)));d.domain.sourceCatalogue=await I.correctStage(d.domain.sourceCatalogue,'csoi:smrc-dcp-bombala-2014:20261030','SOURCE_RETRIEVED',{actor:'QA',at:new Date().toISOString(),reason:'Synthetic browser source withdrawal'});fs.writeFileSync(process.argv[3],JSON.stringify(await M.exportSnapshot(d)));})().catch(e=>{console.error(e);process.exitCode=1});"""
  subprocess.run(['node','-e',code,str(snapshot),str(parent),str(withdrawn)],cwd=APP,check=True)
  import_snapshot(page,parent);phe(page);soil=host.locator('[data-clause-id="'+SOIL+'"]');rural=host.locator('[data-clause-id="'+RURAL+'"]');expect(soil.get_by_role('link',name='Choose own review date',exact=True)).to_have_count(0);expect(rural.get_by_role('link',name='Choose own review date',exact=True)).to_have_count(1);expect(soil.get_by_role('link',name='Review work card · 2026-11-06',exact=True)).to_have_count(1)
  import_snapshot(page,withdrawn);phe(page)
  for card in host.locator('[data-clause-id*="bombala2012"]').all():expect(card.get_by_role('link',name='Choose own review date',exact=True)).to_have_count(0);expect(card).to_contain_text('invalidated')
  expect(host.locator('[data-clause-id*="snowy2013"]').get_by_role('link',name='Choose own review date',exact=True)).to_have_count(3);expect(host.locator('[data-clause-id*="cooma2014"]').get_by_role('link',name='Choose own review date',exact=True)).to_have_count(3);expect(host.get_by_role('link',name='Compare Bombala and Cooma evidence paths',exact=True)).to_have_count(0);expect(gaps.locator('[data-evidence-gap=current-rule] dt').filter(has_text='resolved').locator('xpath=following-sibling::dd[1]')).to_have_text('false')
  soil.scroll_into_view_if_needed();page.screenshot(path=str(OUT/f'bombala-withdrawn-{width}.png'));soil.get_by_role('link',name='Review work card · 2026-11-06',exact=True).click();expect(page.locator('#csoiWorkspace dt').filter(has_text='inputPinsCurrent').locator('xpath=following-sibling::dd[1]')).to_have_text('false');expect(page.locator('#csoiWorkspace')).to_contain_text('UNKNOWN');assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');assert not errors,errors
  results.append({'viewport':[width,height],'status':'PASS_TESTED_HERE','selectedCards':11,'BombalaCards':5,'unresolvedEvidenceGaps':2,'independentPlans':2,'retainedRemediation':'PASS','exportProofAndSnapshot':'PASS','parentWithdrawalIsolation':'PASS','sourceWithdrawalIsolation':'PASS','CouncilAssignment':'NOT_CREATED','browserErrors':errors});page.close()
 browser.close()
(OUT/'browser-results.json').write_text(json.dumps({'generatedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':results},indent=2)+'\n')
print('PASS: desktop/mobile Bombala subdivision/rural PHE context, persistent evidence gaps, pinned work/calendar, independent exports, parent/source withdrawal and preserved P0/P1 corrections')
