"""Source-backed PHE learning routes; all activity cases are synthetic research."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright,expect
OUT=Path(__file__).resolve().parent/'csoi';results=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for w,h in [(1440,900),(390,844)]:
  page=b.new_page(viewport={'width':w,'height':h});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  for domain in ['food','ossm','pools','cooling','skin','environment','ltw','backflow']:
   group='wcos' if domain in ['ltw','backflow'] else 'phe'
   page.goto('http://127.0.0.1:8877/#/domains/'+group+'/'+domain)
   expect(page.locator('#csoiPheWorkflow')).to_be_visible(timeout=20000)
   expect(page.locator('#csoiWorkspace')).to_contain_text('PENDING')
   assert page.get_by_role('link',name='Trace exact source note',exact=True).count()>0
   page.get_by_role('button',name='Synthetic applicable case',exact=True).click()
   expect(page.locator('#csoiPheWorkflow')).to_contain_text('APPLICABLE_FOR_RESEARCH')
   expect(page.locator('#csoiPheWorkflow')).to_contain_text('BLOCKED')
   page.get_by_role('button',name='Missing-facts counterexample',exact=True).click()
   expect(page.locator('#csoiPheWorkflow')).to_contain_text('UNKNOWN')
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
   if domain in ['food','pools']:page.screenshot(path=str(OUT/f'phe-{domain}-{w}.png'))
  assert not errors,errors;results.append({'viewport':[w,h],'domains':8,'status':'PASS_TESTED_HERE','currentLegalVersion':'UNKNOWN','formalDecision':'BLOCKED'});page.close()
 b.close()
(OUT/'browser-e.json').write_text(json.dumps({'results':results},indent=2)+'\n');print('PASS: eight source-backed public domains, exact source-note/receipt links, conditional research chains and missing-fact cases on desktop/mobile')
