"""Synthetic read-only WCOS boundary; never connects to private production."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright,expect
OUT=Path(__file__).resolve().parent/'csoi';results=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for w,h in [(1440,900),(390,844)]:
  page=b.new_page(viewport={'width':w,'height':h});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:8877/#/domains/wcos/ltw');expect(page.locator('#csoiConditionalResult')).to_be_visible(timeout=20000)
  expect(page.locator('#csoiWorkspace')).to_contain_text('BLOCKED_AUTHORISED_TECHNICAL_CONTRACT_NOT_SUPPLIED')
  for key,val in [('handlesFood','true'),('dischargesLiquidTradeWaste','false'),('sewerConnection','true'),('waterConnection','true'),('testableBackflowDevice','false')]:page.locator('select[name='+key+']').select_option(val)
  page.get_by_role('button',name='Check synthetic activity conditions').click()
  expect(page.locator('#csoiConditionalResult')).to_contain_text('APPLICABLE_FOR_RESEARCH')
  expect(page.locator('#csoiConditionalResult')).to_contain_text('NOT_APPLICABLE')
  expect(page.locator('#csoiConditionalResult')).to_contain_text('No AI approval')
  page.screenshot(path=str(OUT/f'wcos-conditional-{w}.png'))
  page.evaluate('location.hash="#/domains/wcos/backflow"');expect(page.locator('#csoiWorkspace')).to_contain_text('2025-02-28')
  expect(page.locator('#csoiWorkspace')).to_contain_text('Device-specific scheduling boundary')
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');assert not errors,errors
  results.append({'viewport':[w,h],'status':'PASS_TESTED_HERE','scope':'ABSTRACT_SYNTHETIC_READ_ONLY','privateCompatibility':'BLOCKED'});page.close()
 b.close()
(OUT/'browser-d.json').write_text(json.dumps({'results':results},indent=2)+'\n');print('PASS: desktop/mobile conditional Food/LTW/Backflow negative case, read-only/private boundaries, LTW stages and device-specific synthetic schedule')
