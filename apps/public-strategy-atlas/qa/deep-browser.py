"""Real browser capacity checks; synthetic records do not count as public corpus."""
from pathlib import Path
import subprocess
from playwright.sync_api import sync_playwright, expect
APP=Path(__file__).resolve().parents[1];OUT=APP/'qa'/'system'
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width,height in [(1440,900),(390,844)]:
  context=b.new_context(viewport={'width':width,'height':height},reduced_motion='reduce',accept_downloads=True)
  page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  for count in [60,200]:
   page.goto(f'http://127.0.0.1:8877/?fixture={count}')
   expect(page.locator('#contentCount')).to_have_text(str(count+127))
   assert page.locator('[data-node-id]').count()<=4
   page.locator('[data-node-id="density:0"]').focus();page.keyboard.press('Enter')
   page.locator('#toolsMenu>summary').click();page.locator('#collapseNode').click()
   assert page.locator('[data-node-id]').count()==1
   page.locator('#expandNode').click();assert page.locator('[data-node-id]').count()==4
   page.locator('#toolsMenu>summary').click()
   page.locator('#search').fill(f'Demo item {count-1}');page.locator('#searchResults button').first.click()
   expect(page.locator('#details h3').first).to_have_text(f'Demo item {count-1}')
   assert page.locator('[data-node-id]').count()<=200
  print(f'PASS: {width}x{height} 60/200 progressive fixtures and last-item search',flush=True)
  page.goto('http://127.0.0.1:8877/?fixture=1000&shape=chain')
  expect(page.locator('#contentCount')).to_have_text('1127')
  assert page.locator('[data-node-id]').count()<=200
  page.locator('#search').fill('Demo item 999')
  page.locator('#searchResults button').first.click()
  expect(page.locator('#details h3').first).to_have_text('Demo item 999')
  expect(page.locator('#breadcrumbs')).to_contain_text('earlier ancestors')
  assert page.locator('[data-node-id]').count()<=5
  page.get_by_role('button',name='↑ Parent content',exact=True).click()
  expect(page.locator('#details h3').first).to_have_text('Demo item 998')
  page.locator('#subtreeQuery').fill('Demo item 999')
  expect(page.locator('#subtreeResults')).to_contain_text('1 matches')
  page.locator('#subtreeResults button').click()
  expect(page.locator('#details h3').first).to_have_text('Demo item 999')
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  page.screenshot(path=str(OUT/f'deep-{width}.png'))
  with page.expect_download() as download:
   page.locator('#toolsMenu>summary').click();page.locator('#exportBtn').click()
  file=Path(f'/tmp/atlas-deep-{width}.json');download.value.save_as(str(file))
  subprocess.run(['node',str(APP/'verify-snapshot.cjs'),str(file)],check=True)
  assert not errors,errors
  print(f'PASS: {width}x{height} 1000-level search/parent/subtree/bounded route and deep snapshot verification',flush=True)
  page.goto('http://127.0.0.1:8877/?fixture=10000')
  expect(page.locator('#contentCount')).to_have_text('10127')
  page.locator('#search').fill('Demo item 9999');page.locator('#searchResults button').first.click()
  expect(page.locator('#details h3').first).to_have_text('Demo item 9999')
  assert page.locator('[data-node-id]').count()<=200
  assert not errors,errors
  print(f'PASS: {width}x{height} 10000-item progressive fixture and late-item navigation',flush=True)
  context.close()
 b.close()
