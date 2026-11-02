"""Focused final OP rendering regression; preserve all conflicts behind real disclosure controls."""
from pathlib import Path
from urllib.parse import quote
import datetime,hashlib,json,os
from playwright.sync_api import sync_playwright,expect
APP=Path(__file__).resolve().parents[1];OUT=Path(os.environ.get('ATLAS_READING_BROWSER_OUTPUT',str(APP/'qa/op-completion-20261102/readable-browser')));OUT.mkdir(parents=True,exist_ok=True)
BASE=os.environ.get('ATLAS_TEST_URL','http://127.0.0.1:8879/');results=[]
with sync_playwright()as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width,height in [(1440,900),(390,844)]:
  page=b.new_page(viewport={'width':width,'height':height},has_touch=width==390,reduced_motion='reduce');errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(BASE);expect(page.locator('#contentCount')).to_have_text('127');checked=[]
  for n in [28,73,111,121,132]:
   id='csoi:knowledge:op2026:review:page:'+str(n).zfill(3);page.evaluate('(path)=>location.hash="#"+path','/knowledge/'+quote(id,safe=''));reading=page.locator('#csoiOpSourceReading');expect(reading).to_contain_text('本条与本轮逐页原件复核一致')
   assert all(not dl.is_visible()for dl in page.locator('#csoiSourceReading dl.csoi-fields').all()),'TECHNICAL_JSON_SHOULD_START_COLLAPSED'
   conflict=reading.locator(':scope > details:not([data-op-unit])').first
   if conflict.count():
    assert conflict.get_attribute('open')is None;conflict.locator(':scope > summary').click();expect(conflict.locator(':scope > dl.csoi-fields')).to_be_visible();assert len(conflict.locator(':scope > dl.csoi-fields').inner_text())>20;conflict.locator(':scope > summary').click()
   unit=reading.locator('[data-op-unit]').first;unit.locator(':scope > summary').click();expect(unit.locator('p').first).to_be_visible();assert unit.locator('p').first.inner_text();assert all(not dl.is_visible()for dl in reading.locator('dl.csoi-fields').all())
   assert reading.get_by_role('link',name='打开官方 OP PDF 第 '+str(n)+' 页').get_attribute('href').endswith('#page='+str(n));assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
   reading.get_by_role('heading',name='OP 全文有界梳理 / 计划、条件和预算',exact=True).scroll_into_view_if_needed();page.screenshot(path=str(OUT/f'op-readable-{n}-{width}.png'));checked.append(n)
  page.evaluate('location.hash="#/research?source=OP"');expect(page.locator('#csoiEngineeringTasks')).to_contain_text('VERIFIED：51 项');expect(page.locator('#csoiEngineeringTasks')).to_contain_text('PARTIAL：26 项');expect(page.locator('#csoiEngineeringTasks')).to_contain_text('BLOCKED：3 项');assert not errors
  results.append({'viewport':[width,height],'pages':checked,'technicalJsonDefault':'COLLAPSED','conflictCanBeOpenedAndRead':True,'unitSummaryReadableWithoutTechnicalJson':True,'originalSourceLinks':'PASS','engineeringCounts':[51,26,3],'status':'PASS','errors':errors});page.close()
 b.close()
(OUT/'results.json').write_text(json.dumps({'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','pagesModuleSHA256':hashlib.sha256((APP/'csoi-pages.js').read_bytes()).hexdigest(),'results':results},indent=2)+'\n');print('PASS: OP technical conflicts start collapsed, source evidence remains readable, desktop/mobile no overflow and51/26/3 current task counts')
