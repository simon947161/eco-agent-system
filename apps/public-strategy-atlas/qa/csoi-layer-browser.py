"""Actual bounded L0–L5 lineage, withdrawal and independent export verification."""
from pathlib import Path
import json,subprocess,tempfile
from playwright.sync_api import sync_playwright,expect
APP=Path(__file__).resolve().parents[1];OUT=APP/'qa/csoi';results=[]
with tempfile.TemporaryDirectory() as tmp,sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width,height in [(1440,900),(390,844)]:
  context=b.new_context(viewport={'width':width,'height':height},accept_downloads=True,reduced_motion='reduce');page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:8877/#/data');expect(page.get_by_role('button',name='Build synthetic L0–L5 evidence chain')).to_be_visible(timeout=20000)
  page.get_by_role('button',name='Build synthetic L0–L5 evidence chain').click()
  expect(page.locator('#csoiWorkspace')).to_contain_text('WORK_COVERAGE_NOT_COMPLIANCE',timeout=20000)
  expect(page.locator('#csoiWorkspace')).to_contain_text('REVIEW_PENDING')
  page.locator('a[href="#/data/csoi%3Ademo%3Awork-coverage"]').click()
  expect(page.locator('#csoiWorkspace')).to_contain_text('CURRENT_SELF_ATTESTED')
  expect(page.locator('#csoiWorkspace')).to_contain_text('Pinned inputs and reverse trace')
  page.screenshot(path=str(OUT/f'layers-current-{width}.png'))
  page.evaluate('location.hash="#/data"');page.get_by_role('button',name='Withdraw synthetic source and invalidate descendants').click()
  expect(page.locator('#csoiWorkspace')).to_contain_text('INVALIDATED',timeout=20000)
  page.screenshot(path=str(OUT/f'layers-withdrawn-{width}.png'))
  page.locator('#toolsMenu>summary').click()
  with page.expect_download() as pending:page.locator('#exportBtn').click()
  target=Path(tmp)/f'layers-{width}.json';pending.value.save_as(str(target));subprocess.run(['node',str(APP/'verify-snapshot.cjs'),str(target)],check=True)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');assert not errors,errors
  results.append({'viewport':[width,height],'status':'PASS_TESTED_HERE','steps':['L0–L5 same-model chain','Explicit denominator 6/10; compliance UNKNOWN','Input withdrawal invalidates descendants','Exported historical snapshot independently verified']});context.close()
 b.close()
(OUT/'browser-c.json').write_text(json.dumps({'results':results},indent=2)+'\n');print('PASS: desktop/mobile L0–L5 workflow, pending release, pinned lineage, withdrawal invalidation and historical snapshot verification')
