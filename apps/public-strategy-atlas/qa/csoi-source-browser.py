"""Actual source-backed pages; raw public originals are never served from this app."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright,expect
APP=Path(__file__).resolve().parents[1];OUT=APP/'qa/csoi';results=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width,height in [(1440,900),(390,844)]:
  page=b.new_page(viewport={'width':width,'height':height},reduced_motion='reduce');errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:8877/#/sources/csoi%3Asmrc-op-2026%3A20261030')
  expect(page.locator('#csoiWorkspace h1')).to_have_text('Source evidence',timeout=20000)
  expect(page.locator('#csoiWorkspace')).to_contain_text('RAW_BYTES_VERIFIED')
  expect(page.locator('#csoiWorkspace')).to_contain_text('UNKNOWN')
  page.locator('a[href="#/knowledge/csoi%3Asource-note%3Asmrc-op-2026%3Afood-program-p27"]').click()
  expect(page.locator('#csoiWorkspace')).to_contain_text('Optimal volume 168, funded volume 84 and target 84')
  expect(page.locator('#csoiWorkspace')).to_contain_text('not actual completed counts')
  expect(page.locator('#csoiWorkspace')).to_contain_text('page 27')
  assert page.locator('#csoiWorkspace a[target="_blank"]').count()>0
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  page.screenshot(path=str(OUT/f'op-planned-source-{width}.png'))
  page.evaluate('location.hash="#/coverage"')
  expect(page.locator('#csoiWorkspace')).to_contain_text('freshByteVerified')
  expect(page.locator('#csoiWorkspace')).to_contain_text('currentLegalVersionConfirmed')
  assert not errors,errors;results.append({'viewport':[width,height],'status':'PASS_TESTED_HERE','basis':'Actual source receipts and attributed research notes; no official admission'})
  page.close()
 b.close()
(OUT/'browser-b.json').write_text(json.dumps({'results':results},indent=2)+'\n')
print('PASS: real OP page27 research note, planned-versus-actual distinction, source/version/hash/review trace and separate corpus coverage on desktop/mobile')
