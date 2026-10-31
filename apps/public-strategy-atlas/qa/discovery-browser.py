"""Actual candidate falsification/local-review/path evidence, not semantic truth proof."""
from pathlib import Path
import json,subprocess
from playwright.sync_api import sync_playwright,expect
APP=Path(__file__).resolve().parents[1];OUT=APP/'qa'/'system'
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width,height in [(1440,900),(390,844)]:
  ctx=b.new_context(viewport={'width':width,'height':height},reduced_motion='reduce',accept_downloads=True)
  page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:8877/');expect(page.locator('#contentCount')).to_have_text('127')
  page.locator('#toolsMenu>summary').click();page.locator('#discoveryEngineBtn').click()
  page.locator('#runEvidencePath').click();expect(page.locator('#queryResults')).to_contain_text('UNKNOWN')
  page.locator('#runCandidateSearch').click()
  page.get_by_role('button',name='legal-fixture:wrong-region',exact=True).click()
  expect(page.locator('#details .detail-badge')).to_contain_text('REJECTED_CANDIDATE')
  expect(page.locator('#details')).to_contain_text('REJECTED_REGION')
  assert page.locator('#researchDecision option[value="APPROVED_FOR_RESEARCH"]').count()==0
  page.locator('#researchReason').fill('Wrong synthetic jurisdiction; shared land wording cannot prove legal applicability.')
  page.locator('#saveResearchReview').click();expect(page.locator('#researchMessage')).to_contain_text('review appended')
  page.screenshot(path=str(OUT/f'discovery-{width}.png'))
  page.get_by_role('button',name='Back to discovery',exact=True).click()
  page.locator('#queryFrom').fill('synthetic-water-output');page.locator('#queryTo').fill('water');page.locator('#queryDirection').select_option('reverse');page.locator('#queryMode').select_option('DISCOVERY_CANDIDATE');page.locator('#runEvidencePath').click()
  expect(page.locator('#queryResults')).to_contain_text('DISCOVERY_CANDIDATE')
  with page.expect_download() as download:
   page.locator('#toolsMenu>summary').click();page.locator('#exportBtn').click()
  file=Path(f'/tmp/atlas-discovery-{width}.json');download.value.save_as(str(file));subprocess.run(['node',str(APP/'verify-snapshot.cjs'),str(file)],check=True)
  data=json.loads(file.read_text());assert any(e['kind']=='ReviewDecision' for e in data['dataset']['domain']['entities'])
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');assert not errors,errors
  print(f'PASS: {width}x{height} known-link UNKNOWN, rejected same-word wrong-region candidate, counterevidence/research review, reverse path and verifiable snapshot',flush=True)
  ctx.close()
 b.close()
