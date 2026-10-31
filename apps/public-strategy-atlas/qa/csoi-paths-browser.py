"""Real source/strategy multibranch path proofs, independent verification and limits."""
from pathlib import Path
import json,datetime,tempfile,subprocess
from playwright.sync_api import sync_playwright,expect
APP=Path(__file__).resolve().parents[1];OUT=APP/'qa/csoi';results=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width,height in [(1440,900),(390,844)]:
  page=b.new_page(viewport={'width':width,'height':height},reduced_motion='reduce',accept_downloads=True);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:8877/#/compare/paths');expect(page.locator('#csoiWorkspace h1')).to_have_text('Typed path-set comparison',timeout=30000)
  page.get_by_role('button',name='Inspect pinned path sets',exact=True).click()
  expect(page.locator('#csoiWorkspace')).to_contain_text('REJECTED_UNKNOWN_ADMISSION',timeout=30000)
  expect(page.locator('#csoiWorkspace')).to_contain_text('Pinned nodes: 9')
  expect(page.locator('#csoiWorkspace')).to_contain_text('Arithmetic: NOT_PERFORMED')
  expect(page.locator('#csoiWorkspace')).to_contain_text('Official relationship: UNKNOWN')
  expect(page.locator('#csoiWorkspace')).to_contain_text('GOVERNED_INPUT_LINEAGE')
  expect(page.locator('#csoiWorkspace')).to_contain_text('RESEARCH_CANDIDATE')
  page.screenshot(path=str(OUT/f'path-sets-{width}.png'))
  with page.expect_download() as download:page.get_by_role('button',name='Export pinned path comparison proof',exact=True).click()
  proof=Path(tempfile.gettempdir())/f'csoi-path-proof-{width}.json';download.value.save_as(str(proof))
  data=json.loads(proof.read_text());assert data['core']['arithmetic']=='NOT_PERFORMED';assert all(e['revisionId'].startswith('sha256:') for pth in data['core']['right'] for e in pth['core']['relationships'])
  page.evaluate('location.hash="#/atlas"');expect(page.locator('#routeMap')).to_be_visible();page.locator('#toolsMenu>summary').click()
  with page.expect_download() as download:page.locator('#exportBtn').click()
  snapshot=Path(tempfile.gettempdir())/f'csoi-path-snapshot-{width}.json';download.value.save_as(str(snapshot));subprocess.run(['node',str(APP/'verify-paths.cjs'),str(snapshot),str(proof)],check=True)
  assert not errors,errors;results.append({'viewport':[width,height],'status':'PASS_TESTED_HERE','DcpNodes':9,'independentPathComparison':'PASS','officialUse':'REJECTED_UNKNOWN_ADMISSION','arithmetic':'NOT_PERFORMED'});page.close()
 b.close()
(OUT/'browser-paths.json').write_text(json.dumps({'generatedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':results},indent=2)+'\n')
print('PASS: desktop/mobile independently pinned OP/CSP and nine-node DCP path sets, retained candidate/counterevidence gates and standalone proof verification')
