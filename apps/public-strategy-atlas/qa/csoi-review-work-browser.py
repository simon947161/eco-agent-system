"""Clause→independent work plan→Annual Edition→source and verified portable snapshot."""
from pathlib import Path
import json,datetime,tempfile,subprocess
from playwright.sync_api import sync_playwright,expect
APP=Path(__file__).resolve().parents[1];OUT=APP/'qa/csoi';results=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width,height in [(1440,900),(390,844)]:
  page=b.new_page(viewport={'width':width,'height':height},reduced_motion='reduce',accept_downloads=True);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:8877/#/knowledge/csoi%3Adcp%3Asnowy2013%3AC9%3A3%3A1%3Ab%3Asoil');expect(page.locator('#csoiWorkspace h1')).to_have_text('Inside the knowledge',timeout=30000)
  page.get_by_role('link',name='Plan an independent source review',exact=True).click();expect(page.locator('#csoiWorkspace h1')).to_have_text('Operational year')
  page.locator('input[name=sourceReviewDate]').fill('2026-11-02');page.locator('input[name=sourceReviewHours]').fill('1.5');page.get_by_role('button',name='Append independent review plan',exact=True).click()
  expect(page.locator('#csoiWorkspace h1')).to_have_text('Calendar work item',timeout=20000);expect(page.locator('#csoiWorkspace')).to_contain_text('Independent review work card');expect(page.locator('#csoiWorkspace')).to_contain_text('ASSUMED');expect(page.locator('#csoiWorkspace')).to_contain_text('NOT_CREATED');expect(page.locator('#csoiWorkspace')).to_contain_text('PERSONAL_LEARNING')
  page.screenshot(path=str(OUT/f'source-review-calendar-{width}.png'))
  page.get_by_role('link',name='Open work dossier',exact=True).click();expect(page.locator('#csoiWorkspace')).to_contain_text('Independent source-review work card — no Council assignment');expect(page.locator('#csoiWorkspace')).to_contain_text('actualSpend');expect(page.locator('#csoiWorkspace')).to_contain_text('UNKNOWN');page.get_by_role('link',name='Calendar review plan',exact=True).click()
  for _ in range(5):page.locator('nav[aria-label="Calendar parents"] a').first.click()
  expect(page.locator('#csoiWorkspace')).to_contain_text('OPERATING_YEAR')
  expect(page.locator('#csoiWorkspace')).to_contain_text('assumedPlannedHours');expect(page.locator('#csoiWorkspace')).to_contain_text('1.5')
  page.evaluate('location.hash="#/assistant"');expect(page.locator('#csoiWorkspace')).to_contain_text('Independent source-review preparation — not Council assignments')
  page.evaluate('location.hash="#/atlas"');expect(page.locator('#routeMap')).to_be_visible();page.locator('#toolsMenu>summary').click()
  with page.expect_download() as download:page.locator('#exportBtn').click()
  snapshot=Path(tempfile.gettempdir())/f'csoi-review-work-{width}.json';download.value.save_as(str(snapshot));subprocess.run(['node',str(APP/'verify-snapshot.cjs'),str(snapshot)],check=True)
  data=json.loads(snapshot.read_text())['dataset'];plans=[e for e in data['domain']['entities'] if e.get('data',{}).get('csoiRecord',{}).get('data',{}).get('reviewPlan')];assert len(plans)==1;assert plans[0]['classification']=='LOCAL_RESEARCH';assert plans[0]['data']['csoiRecord']['data']['reviewPlan']['actualSpend']=='UNKNOWN';assert page.locator('#contentCount').inner_text()=='127';assert not errors,errors
  results.append({'viewport':[width,height],'status':'PASS_TESTED_HERE','ownAssumedHours':1.5,'actualHours':'UNKNOWN','CouncilAssignment':'NOT_CREATED','sourceWorkCalendarNavigation':'PASS','independentSnapshot':'PASS'});page.close()
 b.close()
(OUT/'browser-review-work.json').write_text(json.dumps({'generatedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':results},indent=2)+'\n')
print('PASS: desktop/mobile clause→independent public work plan→day/week/month/quarter/year→draft preparation, assumed-hours boundary and independent snapshot')
