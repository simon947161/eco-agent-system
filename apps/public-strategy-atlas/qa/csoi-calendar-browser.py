"""Full synthetic Annual Edition drill-through, immutable plans and draft management."""
from pathlib import Path
import json,subprocess,tempfile
from playwright.sync_api import sync_playwright,expect
APP=Path(__file__).resolve().parents[1];OUT=APP/'qa/csoi';results=[]
def jump(page,path):page.evaluate('(path)=>location.hash="#"+path',path)
with tempfile.TemporaryDirectory() as tmp,sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for w,h in [(1440,900),(390,844)]:
  context=b.new_context(viewport={'width':w,'height':h},accept_downloads=True,reduced_motion='reduce');page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:8877/#/calendar');expect(page.locator('#csoiWorkspace h1')).to_have_text('Operational year',timeout=20000)
  from urllib.parse import quote
  chain=['public-research','calendar:CALENDAR:2026:year','calendar:CALENDAR:2026:Q4','calendar:CALENDAR:2026:month:2026-11','calendar:CALENDAR:2026:week:2026-W45','calendar:CALENDAR:2026:day:2026-11-02','csoi:task:2026:ltw']
  for id in chain:page.locator('#csoiWorkspace a[href="#/calendar/'+quote(id,safe='')+'?year=2026&yearBasis=CALENDAR"]').first.click()
  expect(page.locator('#csoiWorkspace')).to_contain_text('actualResult')
  page.get_by_role('button',name='Append task to local research model',exact=True).click();expect(page.locator('#csoiWorkspace')).to_contain_text('Research revision retained')
  page.locator('input[name=taskExpectedHours]').fill('4');page.locator('input[name=taskRevisionReason]').fill('Synthetic preparation estimate reviewed');page.get_by_role('button',name='Append task plan revision').click()
  expect(page.locator('input[name=taskExpectedHours]')).to_have_value('4')
  page.get_by_role('link',name='Learn from public source references',exact=True).click();expect(page.locator('#csoiWorkspace')).to_contain_text('PENDING');page.get_by_role('link',name='Trace exact source note',exact=True).first.click();expect(page.locator('#csoiWorkspace')).to_contain_text('Evidence state:');page.go_back();page.go_back();expect(page.locator('input[name=taskExpectedHours]')).to_have_value('4')
  page.get_by_role('link',name='OP context — task linkage UNKNOWN',exact=True).click();expect(page.locator('#csoiWorkspace h1')).to_have_text('Strategy dossier');page.go_back();page.get_by_role('link',name='CSP context — task linkage UNKNOWN',exact=True).click();expect(page.locator('#csoiWorkspace h1')).to_have_text('Strategy dossier');page.go_back()
  for id in ['csoi:work:ltw','csoi:brief:ltw','csoi:task:2026:ltw:execution','csoi:task:2026:ltw:evidence:0','csoi:followup:ltw','csoi:report:2026']:page.locator('#csoiWorkspace a[href="#/calendar/'+quote(id,safe='')+'?year=2026&yearBasis=CALENDAR"]').first.click()
  expect(page.locator('#csoiWorkspace')).to_contain_text('No actual service delivery')
  page.screenshot(path=str(OUT/f'calendar-report-{w}.png'))
  jump(page,'/calendar?year=2026&yearBasis=AU_FISCAL');expect(page.locator('select[name=yearBasis]')).to_have_value('AU_FISCAL')
  page.locator('input[name=newTaskTitle]').fill('Independent public-source review');page.locator('input[name=newTaskDate]').fill('2026-11-06');page.locator('input[name=newTaskHours]').fill('1');page.get_by_role('button',name='Create synthetic research task',exact=True).click();expect(page.locator('#csoiWorkspace h1')).to_have_text('Calendar work item');expect(page.locator('#csoiWorkspace')).to_contain_text('Synthetic research: Independent public-source review')
  jump(page,'/assistant');expect(page.locator('#csoiAssistantDraft')).to_contain_text('DRAFT');expect(page.locator('#csoiAssistantDraft')).to_contain_text('SIMULATION_DISABLED')
  page.get_by_role('button',name='Append draft to local research model',exact=True).click();expect(page.locator('#csoiAssistantDraft')).to_contain_text('Research revision retained')
  page.screenshot(path=str(OUT/f'weekly-draft-{w}.png'))
  page.locator('#toolsMenu>summary').click()
  with page.expect_download() as pending:page.locator('#exportBtn').click()
  target=Path(tmp)/f'calendar-{w}.json';pending.value.save_as(str(target));subprocess.run(['node',str(APP/'verify-snapshot.cjs'),str(target)],check=True)
  data=json.loads(target.read_text())['dataset'];assert len([r for r in data['domain']['revisions'] if r['logicalId']=='csoi:task:2026:ltw'])==2
  assert not errors,errors;results.append({'viewport':[w,h],'status':'PASS_TESTED_HERE','taskRevisions':2,'actualCouncilWork':'UNKNOWN','outlook':'SIMULATION_DISABLED'});context.close()
 b.close()
(OUT/'browser-g-detail.json').write_text(json.dumps({'results':results},indent=2)+'\n');print('PASS: desktop/mobile mission→year→quarter→month→week→day→task→brief→evidence→report, fiscal projection, immutable task revision, weekly DRAFT and independent snapshot')
