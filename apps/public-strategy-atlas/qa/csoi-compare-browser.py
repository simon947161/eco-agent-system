"""Actual public-source and typed-accounting comparison; no new graph or authority."""
from pathlib import Path
import json,datetime,hashlib
from urllib.parse import urlencode
from playwright.sync_api import sync_playwright,expect
APP=Path(__file__).resolve().parents[1];OUT=APP/'qa/csoi';results=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width,height in [(1440,900),(390,844)]:
  page=b.new_page(viewport={'width':width,'height':height},reduced_motion='reduce');errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
  page.goto('http://127.0.0.1:8877/#/sources/csoi%3Asmrc-dcp-bombala-2014%3A20261030')
  expect(page.locator('#csoiWorkspace h1')).to_have_text('Source evidence',timeout=20000)
  page.get_by_role('link',name='Compare this source revision',exact=True).click()
  expect(page.locator('#csoiWorkspace h1')).to_have_text('Compare records across paths')
  expect(page.locator('#csoiCompareForm input[name=left]')).to_have_value('csoi:smrc-dcp-bombala-2014:20261030')
  page.locator('#csoiCompareForm input[name=right]').fill('csoi:smrc-dcp-cooma-2014-amend4:20261030')
  page.get_by_role('button',name='Compare pinned records',exact=True).click()
  expect(page.locator('#csoiWorkspace')).to_contain_text('Official relationship: UNKNOWN',timeout=20000)
  expect(page.locator('#csoiWorkspace')).to_contain_text('Arithmetic: NOT_PERFORMED')
  expect(page.locator('.csoi-compare-grid')).to_contain_text('Bombala Development Control Plan 2012')
  expect(page.locator('.csoi-compare-grid')).to_contain_text('Cooma-Monaro Shire Development Control Plan 2014')
  assert page.locator('.csoi-compare-grid a[href^="#/sources/"]').count()==2
  pin=page.get_by_role('link',name='Permalink to these exact revisions',exact=True)
  assert 'rightRevision=' in pin.get_attribute('href') and 'leftRevision=' in pin.get_attribute('href')
  pin.click();expect(page.locator('#csoiWorkspace')).to_contain_text('Official relationship: UNKNOWN',timeout=20000)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  assert page.locator('#csoiWorkspace').evaluate('(e)=>e.scrollWidth<=e.clientWidth')
  page.get_by_role('heading',name='Pinned comparison',exact=True).scroll_into_view_if_needed()
  page.screenshot(path=str(OUT/f'comparison-source-{width}.png'))
  with page.expect_popup() as popup:page.locator('[data-csoi-companion]').click()
  other=popup.value;expect(other.locator('#csoiWorkspace')).to_contain_text('Official relationship: UNKNOWN',timeout=20000);assert other.evaluate('window.opener===null');other.close()
  page.locator('#csoiCompareForm input[name=leftRevision]').fill('missing-old-revision')
  page.get_by_role('button',name='Compare pinned records',exact=True).click()
  expect(page.locator('#csoiWorkspace')).to_contain_text('Comparison rejected: COMPARISON_REVISION_NOT_FOUND')
  page.evaluate('location.hash="#/compare?left=water&right=area&leftRevision=bad%40pin"')
  expect(page.locator('#csoiWorkspace h1')).to_have_text('Page not found')
  page.evaluate('(q)=>location.hash="#/compare?"+q',urlencode({'left':'synthetic-water-budget','right':'synthetic-water-spend'}))
  expect(page.locator('#csoiWorkspace')).to_contain_text('Compatibility: CONFLICT',timeout=20000)
  expect(page.locator('#csoiWorkspace')).to_contain_text('APPROVED_BUDGET')
  expect(page.locator('#csoiWorkspace')).to_contain_text('ACTUAL_EXPENDITURE')
  expect(page.locator('#csoiWorkspace')).to_contain_text('Arithmetic: NOT_PERFORMED')
  page.evaluate('(q)=>location.hash="#/compare?"+q',urlencode({'left':'csoi:published-plan:food-2026:target','right':'synthetic-water-output'}))
  expect(page.locator('#csoiWorkspace')).to_contain_text('TARGET_VOLUME',timeout=20000)
  expect(page.locator('#csoiWorkspace')).to_contain_text('PUBLISHED_PLAN_NOT_ACTUAL')
  page.evaluate('location.hash="#/operations?law=food&work=WorkPackage&region=snowy+monaro"')
  expect(page.locator('#csoiWorkspace h1')).to_have_text('Operations and work')
  links=page.locator('#csoiWorkspace .csoi-records a');expect(links).to_have_count(1);expect(links).to_contain_text('Published food inspection programme')
  assert not errors,errors
  results.append({'viewport':[width,height],'status':'PASS_TESTED_HERE','sourceScopeComparison':'EXECUTED','exactRevisionPermalinkAndMissingPin':'EXECUTED','financeAndPlannedVsActual':'EXECUTED','lawWorkFilters':'EXECUTED','officialRelationship':'UNKNOWN'})
  page.close()
 b.close()
(OUT/'browser-comparison.json').write_text(json.dumps({'generatedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'testedFiles':{name:'sha256:'+hashlib.sha256((APP/name).read_bytes()).hexdigest() for name in ['atlas-execution.js','csoi-router.js','csoi-pages.js','csoi-pages.css']},'results':results},indent=2)+'\n')
print('PASS: desktop/mobile exact source revision comparison, immutable permalink, missing-pin rejection, finance roles, real planned quantity boundary, recorded-law/work filters and independent companion')
