"""Two real DCP source branches, pinned geographic conflicts and source-review calendar."""
from pathlib import Path
from urllib.parse import quote
import json,datetime,tempfile,subprocess
from playwright.sync_api import sync_playwright,expect
APP=Path(__file__).resolve().parents[1];OUT=APP/'qa/csoi';results=[]
source='csoi:smrc-dcp-cooma-2014-amend4:20261030';prefix='csoi:dcp:cooma2014:';leaf=prefix+'7:4:2:2:soil'
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width,height in [(1440,900),(390,844)]:
  page=b.new_page(viewport={'width':width,'height':height},reduced_motion='reduce',accept_downloads=True);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:8877/#/sources/'+quote(source,safe=''));expect(page.locator('#csoiWorkspace h1')).to_have_text('Source evidence',timeout=30000)
  for suffix in ['document','7','7:4','7:4:2:2','7:4:2:2:soil']:
   page.locator('a[href="#/knowledge/'+quote(prefix+suffix,safe='')+'"]').first.click();expect(page.locator('#csoiWorkspace')).to_contain_text('SOURCE_PINNED_RESEARCH_PENDING_REVIEW',timeout=20000)
  expect(page.locator('nav[aria-label="Research clause ancestry"] a')).to_have_count(4);expect(page.locator('#csoiWorkspace')).to_contain_text('no sample');expect(page.locator('#csoiWorkspace')).to_contain_text('Former Cooma-Monaro');page.screenshot(path=str(OUT/f'cooma-ossm-clause-{width}.png'))
  page.evaluate('location.hash="#/compare/paths"');expect(page.locator('#csoiWorkspace h1')).to_have_text('Typed path-set comparison')
  page.locator('textarea[name=leftPaths]').fill(leaf+' | '+source);page.locator('textarea[name=rightPaths]').fill('csoi:dcp:snowy2013:C9:3:1:b:soil | csoi:smrc-dcp-snowy-2013-amend3:20261030');page.get_by_role('button',name='Inspect pinned path sets',exact=True).click()
  expect(page.locator('#csoiWorkspace')).to_contain_text('Metadata compatibility: CONFLICT',timeout=30000);expect(page.locator('#csoiWorkspace')).to_contain_text('Pinned nodes: 6');expect(page.locator('#csoiWorkspace')).to_contain_text('Pinned nodes: 9');expect(page.locator('#csoiWorkspace')).to_contain_text('REJECTED_UNKNOWN_ADMISSION');page.screenshot(path=str(OUT/f'cooma-snowy-path-conflict-{width}.png'))
  with page.expect_download() as download:page.get_by_role('button',name='Export pinned path comparison proof',exact=True).click()
  proof=Path(tempfile.gettempdir())/f'csoi-cooma-proof-{width}.json';download.value.save_as(str(proof))
  page.evaluate('location.hash="#/atlas"');expect(page.locator('#routeMap')).to_be_visible();page.locator('#toolsMenu>summary').click()
  with page.expect_download() as download:page.locator('#exportBtn').click()
  snapshot=Path(tempfile.gettempdir())/f'csoi-cooma-snapshot-{width}.json';download.value.save_as(str(snapshot));subprocess.run(['node',str(APP/'verify-paths.cjs'),str(snapshot),str(proof)],check=True)
  data=json.loads(snapshot.read_text())['dataset'];assert len(data['domain']['entities'])==118;assert len(data['contentItems'])==127;assert len([e for e in data['domain']['entities'] if e.get('data',{}).get('csoiRecord',{}).get('data',{}).get('dcpClause')])==55
  page.evaluate('(id)=>location.hash="#/knowledge/"+encodeURIComponent(id)',leaf);expect(page.locator('#csoiWorkspace h1')).to_have_text('Inside the knowledge');expect(page.locator('#toolsMenu')).not_to_have_attribute('open','');page.get_by_role('link',name='Plan an independent source review',exact=True).click();page.locator('input[name=sourceReviewDate]').fill('2026-11-03');page.locator('input[name=sourceReviewHours]').fill('2.25');page.get_by_role('button',name='Append independent review plan',exact=True).click();expect(page.locator('#csoiWorkspace h1')).to_have_text('Calendar work item',timeout=20000);expect(page.locator('#csoiWorkspace')).to_contain_text('ASSUMED');expect(page.locator('#csoiWorkspace')).to_contain_text('NOT_CREATED');expect(page.locator('#csoiWorkspace')).to_contain_text('2.25');page.get_by_role('link',name='Return to source clause',exact=True).click();expect(page.locator('#csoiWorkspace')).to_contain_text('Soil, terrain and laboratory evidence facets');assert not errors,errors
  results.append({'viewport':[width,height],'status':'PASS_TESTED_HERE','CoomaClauseDepth':5,'pathNodes':[6,9],'geographicCompatibility':'CONFLICT','officialUse':'REJECTED_UNKNOWN_ADMISSION','independentProof':'PASS','sourceReviewCalendar':'PASS'});page.close()
 b.close()
(OUT/'browser-cooma.json').write_text(json.dumps({'generatedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':results},indent=2)+'\n')
print('PASS: desktop/mobile Cooma five-level OSSM outline, six/nine-node independent cross-DCP proof with geographic conflict,118entity snapshot and assumed-hours review/calendar return')
