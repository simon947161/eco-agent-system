"""PHE → historical page evidence → independent review → calendar; withdrawal/import."""
from pathlib import Path
import json,datetime,tempfile,subprocess
from playwright.sync_api import sync_playwright,expect
APP=Path(__file__).resolve().parents[1];OUT=APP/'qa/csoi';results=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width,height in [(1440,900),(390,844)]:
  page=b.new_page(viewport={'width':width,'height':height},reduced_motion='reduce',accept_downloads=True);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:8877/#/domains/phe/ossm');host=page.locator('#csoiPheHistorical');expect(host.locator('[data-clause-id]')).to_have_count(6,timeout=30000)
  expect(host).to_contain_text('operational linkage remain UNKNOWN');host.scroll_into_view_if_needed();page.screenshot(path=str(OUT/f'phe-historical-{width}.png'))
  for clause in ['csoi:dcp:snowy2013:C9:3:1:b:soil','csoi:dcp:cooma2014:7:4:2:2:soil']:
   card=host.locator('[data-clause-id="'+clause+'"]');card.locator('summary').click();expect(card).to_contain_text('normalizedPageDigest');expect(card).to_contain_text('sha256:');expect(card).to_contain_text('PENDING')
   card.get_by_role('link',name='Read historical clause',exact=True).click();expect(page.locator('#csoiWorkspace')).to_contain_text('SOURCE_PINNED_RESEARCH_PENDING_REVIEW');page.get_by_role('link',name='Return to on-site sewage evidence',exact=True).click()
   card.get_by_role('link',name='Choose own review date',exact=True).click();page.locator('input[name=sourceReviewDate]').fill('2026-11-03');page.locator('input[name=sourceReviewHours]').fill('1.25');page.get_by_role('button',name='Append independent review plan',exact=True).click()
   expect(page.locator('#csoiWorkspace h1')).to_have_text('Calendar work item',timeout=30000);expect(page.locator('#csoiWorkspace')).to_contain_text('ASSUMED');expect(page.locator('#csoiWorkspace')).to_contain_text('NOT_CREATED')
   page.get_by_role('link',name='Open work dossier',exact=True).click();expect(page.locator('#csoiWorkspace')).to_contain_text('actualSpend');page.get_by_role('link',name='Return to on-site sewage evidence',exact=True).click();expect(card.get_by_role('link',name='Annual calendar · 2026-11-03',exact=True)).to_be_visible()
  page.get_by_role('link',name='Compare Snowy and Cooma evidence paths',exact=True).click();page.get_by_role('button',name='Inspect pinned path sets',exact=True).click();expect(page.locator('#csoiWorkspace')).to_contain_text('Metadata compatibility: CONFLICT',timeout=30000)
  with page.expect_download() as download:page.get_by_role('button',name='Export pinned path comparison proof',exact=True).click()
  proof=Path(tempfile.gettempdir())/f'phe-context-proof-{width}.json';download.value.save_as(str(proof))
  page.evaluate('location.hash="#/atlas"');expect(page.locator('#routeMap')).to_be_visible();page.locator('#toolsMenu>summary').click()
  with page.expect_download() as download:page.locator('#exportBtn').click()
  snapshot=Path(tempfile.gettempdir())/f'phe-context-snapshot-{width}.json';download.value.save_as(str(snapshot))
  subprocess.run(['node',str(APP/'verify-snapshot.cjs'),str(snapshot)],check=True);subprocess.run(['node',str(APP/'verify-paths.cjs'),str(snapshot),str(proof)],check=True)
  withdrawn=Path(tempfile.gettempdir())/f'phe-context-withdrawn-{width}.json'
  script="""const fs=require('fs'),M=require('./atlas-model.js'),I=require('./atlas-intake.js');(async()=>{const d=JSON.parse(fs.readFileSync(process.argv[1])).dataset;d.domain.sourceCatalogue=await I.correctStage(d.domain.sourceCatalogue,'csoi:smrc-dcp-cooma-2014-amend4:20261030','SOURCE_RETRIEVED',{actor:'QA',at:new Date().toISOString(),reason:'Withdraw Cooma byte verification for browser negative'});fs.writeFileSync(process.argv[2],JSON.stringify(await M.exportSnapshot(d)));})().catch(e=>{console.error(e);process.exitCode=1});"""
  subprocess.run(['node','-e',script,str(snapshot),str(withdrawn)],cwd=APP,check=True);subprocess.run(['node',str(APP/'verify-snapshot.cjs'),str(withdrawn)],check=True)
  page.locator('#importSnapshotBtn').click();page.locator('#snapshotFile').set_input_files(str(withdrawn));expect(page.locator('#snapshotMessage')).to_contain_text('Explicit replacement required',timeout=30000);page.locator('#applySnapshot').click()
  page.evaluate('location.hash="#/domains/phe/ossm"');expect(host.locator('[data-clause-id]')).to_have_count(6,timeout=30000)
  for card in host.locator('[data-clause-id*="cooma2014"]').all():expect(card.get_by_role('link',name='Choose own review date',exact=True)).to_have_count(0);expect(card).to_contain_text('invalidated')
  expect(host.locator('[data-clause-id*="snowy2013"]').get_by_role('link',name='Choose own review date',exact=True)).to_have_count(3)
  cooma=host.locator('[data-clause-id="csoi:dcp:cooma2014:7:4:2:2:soil"]');cooma.scroll_into_view_if_needed();page.screenshot(path=str(OUT/f'phe-withdrawn-{width}.png'));cooma.get_by_role('link',name='Review work card · 2026-11-03',exact=True).click();expect(page.locator('#csoiWorkspace')).to_contain_text('inputPinsCurrent');expect(page.locator('#csoiWorkspace')).to_contain_text('false');expect(page.locator('#csoiWorkspace')).to_contain_text('UNKNOWN')
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');assert not errors,errors
  results.append({'viewport':[width,height],'status':'PASS_TESTED_HERE','curatedCards':6,'independentPlans':2,'exportAndProofRevalidation':'PASS','withdrawalImport':'PASS','crossSourceIsolation':'PASS','CouncilAssignment':'NOT_CREATED'});page.close()
 b.close()
(OUT/'browser-phe-context.json').write_text(json.dumps({'generatedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':results},indent=2)+'\n')
print('PASS: PHE/source/work/calendar navigation, exact pins, independent exports, explicit withdrawn-snapshot import and source-isolated review blocking at desktop/390px')
