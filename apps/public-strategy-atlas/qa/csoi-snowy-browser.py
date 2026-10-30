"""New real original-byte receipt, historical scope and independent admission gates."""
from pathlib import Path
import json,datetime
from playwright.sync_api import sync_playwright,expect
APP=Path(__file__).resolve().parents[1];OUT=APP/'qa/csoi';results=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width,height in [(1440,900),(390,844)]:
  page=b.new_page(viewport={'width':width,'height':height},reduced_motion='reduce');errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:8877/#/sources/csoi%3Asmrc-dcp-snowy-page%3A20261030')
  expect(page.locator('#csoiWorkspace h1')).to_have_text('Source evidence',timeout=20000)
  page.locator('a[href="#/sources/csoi%3Asmrc-dcp-snowy-2013-amend3%3A20261030"]').click()
  expect(page.locator('#csoiWorkspace')).to_contain_text('RAW_BYTES_VERIFIED')
  expect(page.locator('#csoiWorkspace')).to_contain_text('Amendment3 (Issue4)')
  expect(page.locator('#csoiWorkspace')).to_contain_text('58/23')
  expect(page.locator('#csoiWorkspace')).to_contain_text('f17fca90befb888b50dbc20f80e38c8e0458ee09b693e1f38f9241b5e18efe9d')
  expect(page.locator('#csoiWorkspace')).to_contain_text('Tyrolean')
  expect(page.locator('#csoiWorkspace')).to_contain_text('UNKNOWN')
  page.get_by_role('heading',name='Observed revision and conflicts — independent review pending').scroll_into_view_if_needed()
  page.screenshot(path=str(OUT/f'snowy-receipt-{width}.png'))
  page.locator('a[href="#/knowledge/csoi%3Asource-note%3Asmrc-dcp-snowy-2013-amend3%3Aamendment-and-historical-scope"]').click()
  expect(page.locator('#csoiWorkspace')).to_contain_text('not a current all-LGA or parcel legal finding')
  expect(page.locator('#csoiWorkspace')).to_contain_text('Official applicability: PENDING')
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');assert not errors,errors
  results.append({'viewport':[width,height],'status':'PASS_TESTED_HERE','originalByteReceipt':'PASS','legalApplicability':'UNKNOWN','officialAdmission':'PENDING'})
  page.close()
 b.close()
(OUT/'browser-snowy-source.json').write_text(json.dumps({'generatedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':results},indent=2)+'\n')
print('PASS: desktop/mobile Snowy River directory→exact original receipt→research note, historical scope/exception and pending review gates')
