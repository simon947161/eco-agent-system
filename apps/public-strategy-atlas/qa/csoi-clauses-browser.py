"""Real DCP outline → eight-level evidence facet → historical quantity and snapshot."""
from pathlib import Path
import json,datetime,subprocess,tempfile
from urllib.parse import quote
from playwright.sync_api import sync_playwright,expect
APP=Path(__file__).resolve().parents[1];OUT=APP/'qa/csoi';results=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width,height in [(1440,900),(390,844)]:
  page=b.new_page(viewport={'width':width,'height':height},reduced_motion='reduce',accept_downloads=True);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:8877/#/sources/csoi%3Asmrc-dcp-snowy-2013-amend3%3A20261030')
  expect(page.locator('#csoiWorkspace h1')).to_have_text('Source evidence',timeout=30000)
  expect(page.locator('#csoiWorkspace')).to_contain_text('Recursive research outline')
  prefix='csoi:dcp:snowy2013:'
  for suffix in ['document','C','C9','C9:3','C9:3:2','C9:3:1','C9:3:1:b','C9:3:1:b:soil']:
   page.locator('a[href="#/knowledge/'+quote(prefix+suffix,safe='')+'"]').first.click()
   expect(page.locator('#csoiWorkspace')).to_contain_text('SOURCE_PINNED_RESEARCH_PENDING_REVIEW',timeout=15000)
   expect(page.locator('#csoiWorkspace')).to_contain_text('not an admitted legal duty')
  expect(page.locator('#csoiWorkspace')).to_contain_text('No soil sample')
  expect(page.locator('nav[aria-label="Research clause ancestry"] a')).to_have_count(7)
  expect(page.locator('#csoiWorkspace')).to_contain_text('actualPhysicalQuantities')
  page.screenshot(path=str(OUT/f'clause-depth-eight-{width}.png'))
  page.locator('nav[aria-label="Research clause ancestry"] a').first.click()
  expect(page.locator('#csoiWorkspace')).to_contain_text('research outline')
  page.evaluate('(path)=>location.hash="#/knowledge/"+encodeURIComponent(path)',prefix+'C9:2:potable:b')
  expect(page.locator('#csoiWorkspace')).to_contain_text('Historical quantitative references')
  page.locator('a[href="#/knowledge/csoi%3Adcp-reference%3Asnowy%3Apotable-accommodation"]').click()
  expect(page.locator('#csoiWorkspace')).to_contain_text('Historical document reference — current applicability UNKNOWN')
  expect(page.locator('#csoiWorkspace')).to_contain_text('L/person/day')
  expect(page.locator('#csoiWorkspace')).to_contain_text('110')
  expect(page.locator('#csoiWorkspace')).to_contain_text('HISTORICAL_DESIGN_REFERENCE_NOT_ACTUAL')
  page.screenshot(path=str(OUT/f'dcp-reference-rate-{width}.png'))
  page.evaluate('location.hash="#/atlas"');expect(page.locator('#routeMap')).to_be_visible()
  page.locator('#toolsMenu>summary').click()
  with page.expect_download() as download:page.locator('#exportBtn').click()
  snapshot=Path(tempfile.gettempdir())/f'csoi-clause-snapshot-{width}.json';download.value.save_as(str(snapshot));subprocess.run(['node',str(APP/'verify-snapshot.cjs'),str(snapshot)],check=True)
  assert page.locator('#contentCount').inner_text()=='127';assert not errors,errors
  results.append({'viewport':[width,height],'status':'PASS_TESTED_HERE','sourceDepth':8,'historicRate':110,'unit':'L/person/day','actualDemand':'UNKNOWN','legalApplicability':'UNKNOWN','independentSnapshot':'PASS'})
  page.close()
 b.close()
(OUT/'browser-clauses.json').write_text(json.dumps({'generatedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':results},indent=2)+'\n')
print('PASS: desktop/mobile real eight-level DCP outline, parent return, historical design rate, source gates and independently verified expanded snapshot')
