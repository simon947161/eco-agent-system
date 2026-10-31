"""Actual typed work/quantity/accounting pages and portable calculation receipts."""
from pathlib import Path
import json,subprocess,tempfile
from playwright.sync_api import sync_playwright,expect
APP=Path(__file__).resolve().parents[1];OUT=APP/'qa/csoi';results=[]
with tempfile.TemporaryDirectory() as tmp,sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for w,h in [(1440,900),(390,844)]:
  context=b.new_context(viewport={'width':w,'height':h},accept_downloads=True);page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:8877/#/metrics');expect(page.get_by_role('button',name='Calculate and append research receipt')).to_be_visible(timeout=20000)
  expect(page.locator('#csoiWorkspace')).to_contain_text('UNIQUE_SERVICE_ENTITY_TYPE_ENTITY_ID');expect(page.locator('#csoiWorkspace')).to_contain_text('completeInventoryCoverage')
  page.get_by_role('button',name='Calculate and append research receipt').click();expect(page.locator('#csoiCalculationResult')).to_contain_text('2000')
  expect(page.locator('#csoiCalculationResult')).to_contain_text('AUD/ML')
  page.locator('select[name=workFormula]').select_option('PER_CAPITA_TOTAL');page.locator('input[name=workInputs]').fill('csp2035-carbon-per-capita-baseline,synthetic-water-output');page.get_by_role('button',name='Calculate and append research receipt').click();expect(page.locator('#csoiCalculationResult')).to_contain_text('UNADMITTED_INPUTS')
  page.screenshot(path=str(OUT/f'work-guards-{w}.png'))
  page.evaluate('location.hash="#/resources"');expect(page.locator('#csoiWorkspace')).to_contain_text('plannedFteEquivalent');expect(page.locator('#csoiWorkspace')).to_contain_text('personnelHeadcount')
  page.evaluate('location.hash="#/metrics/csp2035-carbon-per-capita-baseline"');expect(page.locator('#csoiWorkspace')).to_contain_text('29.9');expect(page.locator('#csoiWorkspace')).to_contain_text('t_CO2e/person');expect(page.locator('#csoiWorkspace')).to_contain_text('officialMapping')
  page.locator('#toolsMenu>summary').click()
  with page.expect_download() as pending:page.locator('#exportBtn').click()
  target=Path(tmp)/f'work-{w}.json';pending.value.save_as(str(target));subprocess.run(['node',str(APP/'verify-snapshot.cjs'),str(target)],check=True)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');assert not errors,errors
  results.append({'viewport':[w,h],'status':'PASS_TESTED_HERE','sourceRelations':'RESEARCH_CANDIDATE_ONLY','actualCouncilSpend':'UNKNOWN','environmentalOutcome':'UNKNOWN'});context.close()
 b.close()
(OUT/'browser-f.json').write_text(json.dumps({'results':results},indent=2)+'\n');print('PASS: desktop/mobile unique regulatory denominators, typed cost receipt, unadmitted carbon rejection, resource assumptions, reverse trace and independent export')
