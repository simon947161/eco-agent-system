"""Bombala historical source → actual clause ancestry → review/calendar → snapshot."""
from pathlib import Path
from urllib.parse import quote
import json,datetime,tempfile,subprocess
from playwright.sync_api import sync_playwright,expect
APP=Path(__file__).resolve().parents[1];OUT=APP/'qa/csoi';results=[]
source='csoi:smrc-dcp-bombala-2014:20261030';prefix='csoi:dcp:bombala2012:'
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width,height in [(1440,900),(390,844)]:
  page=b.new_page(viewport={'width':width,'height':height},reduced_motion='reduce',accept_downloads=True);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:8877/#/sources/'+quote(source,safe=''));expect(page.locator('#csoiWorkspace h1')).to_have_text('Source evidence',timeout=30000)
  for suffix in ['document','3','3:1:5','3:1:5:A9','3:1:5:A9:soil']:
   page.locator('a[href="#/knowledge/'+quote(prefix+suffix,safe='')+'"]').first.click();expect(page.locator('#csoiWorkspace')).to_contain_text('SOURCE_PINNED_RESEARCH_PENDING_REVIEW',timeout=30000)
  expect(page.locator('nav[aria-label="Research clause ancestry"] a')).to_have_count(4);expect(page.locator('#csoiWorkspace')).to_contain_text('PDF page 55, printed page 34');expect(page.locator('#csoiWorkspace')).to_contain_text('No soil sample');assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');page.screenshot(path=str(OUT/f'bombala-soil-{width}.png'))
  page.get_by_role('link',name='Plan an independent source review',exact=True).click();page.locator('input[name=sourceReviewDate]').fill('2026-11-05');page.locator('input[name=sourceReviewHours]').fill('1');page.get_by_role('button',name='Append independent review plan',exact=True).click();expect(page.locator('#csoiWorkspace h1')).to_have_text('Calendar work item',timeout=30000);expect(page.locator('#csoiWorkspace')).to_contain_text('NOT_CREATED');page.get_by_role('link',name='Open work dossier',exact=True).click();expect(page.locator('#csoiWorkspace')).to_contain_text('ASSUMED');page.get_by_role('link',name='Review source clause',exact=True).click();expect(page.locator('#csoiWorkspace')).to_contain_text('Soil and permeability')
  page.evaluate('location.hash="#/atlas"');expect(page.locator('#routeMap')).to_be_visible();page.locator('#toolsMenu>summary').click()
  with page.expect_download() as download:page.locator('#exportBtn').click()
  snapshot=Path(tempfile.gettempdir())/f'bombala-final-{width}.json';download.value.save_as(str(snapshot));subprocess.run(['node',str(APP/'verify-snapshot.cjs'),str(snapshot)],check=True)
  data=json.loads(snapshot.read_text())['dataset'];assert len(data['domain']['entities'])==136;assert len(data['contentItems'])==127;assert len([e for e in data['domain']['entities'] if e.get('data',{}).get('csoiRecord',{}).get('data',{}).get('dcpClause')])==72
  assert not errors,errors;results.append({'viewport':[width,height],'status':'PASS_TESTED_HERE','BombalaDepth':5,'pagePin':'PDF55/printed34','reviewCalendar':'PASS','independentSnapshot':'PASS','legalApplicability':'UNKNOWN'});page.close()
 b.close()
(OUT/'browser-bombala.json').write_text(json.dumps({'generatedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':results},indent=2)+'\n')
print('PASS: desktop/mobile Bombala five-level source/page evidence, independent source-review work/calendar and exported snapshot revalidation')
