"""V1.6 capability checks against localhost:8877; actual screenshots, no deployment."""
from pathlib import Path
import json, subprocess
from playwright.sync_api import sync_playwright, expect
APP=Path(__file__).resolve().parents[1]
OUT=APP/'qa'/'system'; OUT.mkdir(exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width,height in [(1440,900),(390,844)]:
  ctx=b.new_context(viewport={'width':width,'height':height},accept_downloads=True,reduced_motion='reduce')
  page=ctx.new_page(); errors=[];page.on('pageerror',lambda e: errors.append(str(e)))
  page.goto('http://127.0.0.1:8877/')
  expect(page.locator('#contentCount')).to_have_text('127')
  page.locator('[data-node-id=csp6]').focus();page.keyboard.press('Enter')
  page.get_by_role('button',name='Knowledge & work dossier',exact=True).click()
  page.get_by_role('button',name='CO2e emissions per capita',exact=True).click()
  expect(page.locator('#details')).to_contain_text('29.9')
  expect(page.locator('#details')).to_contain_text('PUBLIC_TEXT_OBSERVED')
  page.locator('#domainReason').fill('QA challenge: current-version and permission gates remain pending')
  page.locator('#contestDomain').click()
  expect(page.locator('#domainMessage')).to_contain_text('Local challenge appended')
  expect(page.locator('#details .detail-badge')).to_contain_text('CONTESTED')
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  assert page.locator('#inspector').evaluate('(e)=>e.scrollWidth<=e.clientWidth')
  page.screenshot(path=str(OUT/f'domain-{width}.png'))
  page.get_by_role('button',name='Trace back to strategy station',exact=True).click()
  expect(page.locator('#details')).to_contain_text('Objective 6.1')
  with page.expect_download() as download:
   page.locator('#toolsMenu>summary').click();page.locator('#exportBtn').click()
  target=Path(f'/tmp/atlas-domain-{width}.json');download.value.save_as(str(target))
  subprocess.run(['node',str(APP/'verify-snapshot.cjs'),str(target)],check=True)
  bundle=json.loads(target.read_text());assert bundle['dataset']['domain']['entities'][0]['state']=='CONTESTED'
  assert not errors,errors
  print(f'PASS: {width}x{height} domain dossier, real accounting record, local immutable challenge, reverse station trace, snapshot download/offline verification and no overflow/errors',flush=True)
  ctx.close()
 b.close()
