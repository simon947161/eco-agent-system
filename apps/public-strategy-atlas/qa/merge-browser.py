"""Actual divergent-workspace reconciliation + domain snapshot import acceptance."""
from pathlib import Path
import json, subprocess
from playwright.sync_api import sync_playwright, expect
APP=Path(__file__).resolve().parents[1];OUT=APP/'qa'/'system'
fixture=Path('/tmp/atlas-incoming-workspace.json')
subprocess.run(['node','-e',"const W=require('./atlas-workspace.js'),D=require('./atlas-data.js'),fs=require('fs');(async()=>{const b=await W.create(D),i=await W.commit(b,D,{targetId:'water:content',content:{title:'Imported branch title',text:'<img src=x onerror=window.__atlasInjected=1> Synthetic imported annotation.'},reason:'Synthetic divergent import fixture'});fs.writeFileSync('/tmp/atlas-incoming-workspace.json',JSON.stringify(i));})();"],cwd=APP,check=True)
def tool(page,id):
 if page.locator('#toolsMenu').get_attribute('open') is None:page.locator('#toolsMenu>summary').click()
 page.locator('#'+id).click()
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width,height in [(1440,900),(390,844)]:
  context=b.new_context(viewport={'width':width,'height':height},reduced_motion='reduce',accept_downloads=True)
  page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:8877/');expect(page.locator('#contentCount')).to_have_text('127')
  page.locator('[data-node-id=water]').focus();page.keyboard.press('Enter')
  page.get_by_role('button',name='Explore inside',exact=True).click();page.locator('#editLocalContent').click()
  page.locator('#editTitle').fill('Local branch title');page.locator('#editText').fill('Local synthetic annotation');page.locator('#editReason').fill('Local divergent branch');page.locator('#commitRevision').click()
  expect(page.locator('#workspaceMessage')).to_contain_text('Revision appended')
  tool(page,'workspaceBtn');page.locator('#workspaceImport').set_input_files(str(fixture))
  expect(page.locator('#details h3').first).to_have_text('Three-way import reconciliation')
  page.locator('#resolveWorkspaceMerge').click();expect(page.locator('#mergeMessage')).to_contain_text('MERGE_REASON_REQUIRED')
  page.locator('[data-merge-field=title]').select_option('LOCAL');page.locator('[data-merge-field=text]').select_option('IMPORT');page.locator('#mergeReason').fill('Retain local title and explicitly select imported text')
  page.screenshot(path=str(OUT/f'merge-preview-{width}.png'))
  page.locator('#resolveWorkspaceMerge').click();expect(page.locator('#workspaceMessage')).to_contain_text('Resolved in memory')
  expect(page.locator('#details')).to_contain_text('RESOLVE')
  page.locator('#saveWorkspace').click();expect(page.locator('#workspaceMessage')).to_contain_text('Saved locally')
  with page.expect_download() as download:page.locator('#exportWorkspace').click()
  exported=Path(f'/tmp/atlas-merged-{width}.json');download.value.save_as(str(exported))
  subprocess.run(['node',str(APP/'verify-workspace.cjs'),str(exported)],check=True)
  data=json.loads(exported.read_text());assert data['revisions'][-1]['content']['title']=='Local branch title';assert data['mergeRecords'][0]['importedWorkspace']==json.loads(fixture.read_text())
  page.locator('[data-edit-target="water:content"]').first.click();expect(page.locator('#editText')).to_have_value('<img src=x onerror=window.__atlasInjected=1> Synthetic imported annotation.')
  assert page.evaluate('window.__atlasInjected===undefined')
  with page.expect_download() as download:tool(page,'exportBtn')
  snapshot=Path(f'/tmp/atlas-snapshot-import-{width}.json');download.value.save_as(str(snapshot))
  corrupted=json.loads(snapshot.read_text());corrupted['dataset']['domain']['entities'][0]['label']='Forged after export'
  bad=Path(f'/tmp/atlas-bad-snapshot-{width}.json');bad.write_text(json.dumps(corrupted))
  tool(page,'importSnapshotBtn');page.locator('#snapshotFile').set_input_files(str(bad));expect(page.locator('#snapshotMessage')).to_contain_text('REJECTED: SNAPSHOT_INVALID');expect(page.locator('#applySnapshot')).to_be_disabled()
  page.locator('#snapshotFile').set_input_files(str(snapshot));expect(page.locator('#snapshotMessage')).to_contain_text('Explicit replacement required');page.locator('#applySnapshot').click();expect(page.locator('#snapshotMessage')).to_contain_text('explicitly loaded in memory')
  page.screenshot(path=str(OUT/f'snapshot-import-{width}.png'))
  old=Path(f'/tmp/atlas-older-domain-{width}.json')
  subprocess.run(['node','-e',"const fs=require('fs'),m=require('./atlas-model.js');(async()=>{const s=JSON.parse(fs.readFileSync(process.argv[1]));delete s.dataset.domain.sourceCatalogue;fs.writeFileSync(process.argv[2],JSON.stringify(await m.exportSnapshot(s.dataset)));})();",str(snapshot),str(old)],cwd=APP,check=True)
  tool(page,'importSnapshotBtn');page.locator('#snapshotFile').set_input_files(str(old));expect(page.locator('#snapshotMessage')).to_contain_text('Explicit replacement required');page.locator('#applySnapshot').click()
  tool(page,'coverageBtn');expect(page.locator('#details')).to_contain_text('Source register not included in this snapshot')
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');assert not errors,errors
  print(f'PASS: {width}x{height} real local edit/divergent file import/explicit resolution/archive/save/offline verification, injection escaped and corrupted/valid snapshot import',flush=True)
  context.close()
 b.close()
