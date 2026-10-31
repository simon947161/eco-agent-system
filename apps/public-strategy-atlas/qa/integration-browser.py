"""Route-first layout, typed search, scenario invalidation, history and table acceptance."""
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
APP=Path(__file__).resolve().parents[1];OUT=APP/'qa'/'system'
def tool(page,id):
 if page.locator('#toolsMenu').get_attribute('open') is None:page.locator('#toolsMenu>summary').click()
 page.locator('#'+id).click()
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width,height in [(1440,900),(390,844),(1920,1080),(2560,1080),(3840,1080)]:
  ctx=b.new_context(viewport={'width':width,'height':height},reduced_motion='reduce',accept_downloads=True)
  page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:8877/');expect(page.locator('#contentCount')).to_have_text('127')
  expect(page.locator('#inspector')).to_be_hidden()
  assert page.locator('#mapShell').evaluate('(e)=>e.clientWidth*e.clientHeight/(innerWidth*innerHeight)')>.65
  assert page.evaluate('matchMedia("(prefers-reduced-motion: reduce)").matches')
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  page.screenshot(path=str(OUT/f'integrated-map-{width}.jpg'),quality=75)
  page.locator('.mini-map>summary').click();expect(page.locator('#miniProjection')).to_be_visible()
  old=page.locator('#miniViewport').get_attribute('x');page.locator('[data-pan=end]').click();page.wait_for_function('document.querySelector("#miniViewport").getAttribute("x")!=='+repr(old)) if width==390 else None
  page.locator('[data-pan=start]').click();page.locator('.mini-map>summary').click()
  if page.locator('#toolsMenu').get_attribute('open') is None:page.locator('#toolsMenu>summary').click()
  page.locator('[data-mode=coverage]').click();expect(page.locator('#modeExplanation')).to_contain_text('SYNTHETIC DEMO');assert page.locator('.atlas-edge.colour').count()>0
  page.locator('[data-mode=kpi]').click();expect(page.locator('#modeExplanation')).to_contain_text('UNKNOWN');assert page.locator('.atlas-edge.colour').count()==0
  page.locator('[data-mode=routes]').click();page.locator('#toolsMenu>summary').click()
  page.locator('#search').fill('29.9 t CO2e/person');page.locator('#searchResults button').first.click();expect(page.locator('#details')).to_contain_text('PUBLIC_TEXT_OBSERVED')
  assert page.locator('#reviseScenarioValue').count()==0
  tool(page,'searchToolsBtn');page.locator('#recordKind').fill('WorkPackage');page.locator('#searchRecords').click()
  page.locator('#recordResults button').filter(has_text='Illustrative inspection').first.click()
  expect(page.locator('#details')).to_contain_text('WorkPackage')
  tool(page,'searchToolsBtn');page.locator('#recordQuery').fill('synthetic-water-spend');page.locator('#searchRecords').click();page.locator('#recordResults button').first.click()
  page.locator('#domainReason').fill('Synthetic current-input edit for invalidation test');page.locator('#scenarioValue').fill('18000');page.locator('#reviseScenarioValue').click();expect(page.locator('#domainMessage')).to_contain_text('revision appended')
  page.get_by_role('button',name='Back to dossier',exact=True).click();page.get_by_role('button',name='Three-ledger calculations',exact=True).click();page.locator('#runCalculation').click();expect(page.locator('#calculationMessage')).to_contain_text('1500 AUD/ML')
  tool(page,'auditBtn');expect(page.locator('#details')).to_contain_text('Event chain: PASS');expect(page.locator('#details')).to_contain_text('DOMAIN_RESEARCH');page.get_by_role('button',name='Older events',exact=True).click();expect(page.locator('#details')).to_contain_text('Event chain: PASS')
  page.screenshot(path=str(OUT/f'integrated-history-{width}.jpg'),quality=75)
  if width==390:(OUT/'accessibility-tree-390.txt').write_text(page.locator('body').aria_snapshot())
  page.goto('http://127.0.0.1:8877/?fixture=1000&table=1');expect(page.locator('#contentCount')).to_have_text('1127')
  page.locator('[data-node-id="density:0"]').focus();page.keyboard.press('Enter');expect(page.locator('.content-table')).to_contain_text('SYNTHETIC_FY2026-27');assert page.locator('tbody tr').count()==20
  page.get_by_role('button',name='Next table rows',exact=True).click();expect(page.locator('tbody')).to_contain_text('Synthetic row 20');assert page.locator('tbody tr').count()==20
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');assert not errors,errors
  if width in [390,1440]:page.screenshot(path=str(OUT/f'table-{width}.jpg'),quality=75)
  print(f'PASS: {width}x{height} route dominance, reduced motion, minimap, typed numeric/source/work search, scenario edit/recalculation, full-layer audit pagination, paginated units/fiscal/footnote table and no script errors/overflow',flush=True)
  ctx.close()
 b.close()
