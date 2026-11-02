"""Controlled boot failures and real old/withdrawn snapshot imports; local only."""
from pathlib import Path
import datetime,functools,http.server,json,threading,tempfile,subprocess
from playwright.sync_api import sync_playwright,expect
APP=Path(__file__).resolve().parents[1];OUT=APP/'qa/navigation-repair-20261102/state';OUT.mkdir(parents=True,exist_ok=True)
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(APP)));threading.Thread(target=server.serve_forever,daemon=True).start();BASE='http://127.0.0.1:'+str(server.server_port)+'/'
report={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mode':'local real Chromium; explicitly controlled fault/import fixtures','checks':[]}
def save():(OUT/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
def ready(page):expect(page.locator('#startupNotice')).to_be_hidden(timeout=30000);expect(page.locator('#contentCount')).to_have_text('127')
def menu(page,name):page.locator('#csoiNavigation > summary').click();page.get_by_role('navigation',name='CSOI workspaces').get_by_role('link',name=name,exact=True).click()
def tool(page,id):
 if page.locator('#toolsMenu').get_attribute('open')is None:page.locator('#toolsMenu > summary').click()
 page.locator('#'+id).click()
try:
 with tempfile.TemporaryDirectory(prefix='csoi-navigation-state-')as tmp,sync_playwright()as p:
  tmp=Path(tmp);code="""const fs=require('fs'),M=require('./atlas-model.js'),I=require('./atlas-intake.js'),seed=require('./sources/csoi-default-snapshot.js'),B=require('./qa/op-completion-20261102/baseline-prefix.json');(async()=>{const d=structuredClone(seed.snapshot.dataset),old=structuredClone(d);old.domain.revisions=old.domain.revisions.slice(0,B.domainRevisions);old.domain.events=old.domain.events.slice(0,B.domainEvents);const by=new Map(old.domain.revisions.map(r=>[r.logicalId,{...r.record,revisionId:r.id}]));old.domain.entities=B.entityIds.map(id=>by.get(id));old.domain.assertions=B.assertionIds.map(id=>by.get(id));if(await M.objectDigest(old)!==B.datasetDigest)throw Error('V4_PREFIX_CHANGED');fs.writeFileSync(process.argv[1],JSON.stringify(await M.exportSnapshot(old)));d.domain.sourceCatalogue=await I.correctStage(d.domain.sourceCatalogue,'csoi:smrc-op-2026:20261030','SOURCE_RETRIEVED',{actor:'Navigation QA',at:'2026-11-02T07:45:00.000Z',reason:'Controlled source withdrawal'});fs.writeFileSync(process.argv[2],JSON.stringify(await M.exportSnapshot(d)));})().catch(e=>{console.error(e);process.exitCode=1});"""
  old=tmp/'old-v4.json';withdrawn=tmp/'withdrawn.json';subprocess.run(['node','-e',code,str(old),str(withdrawn)],cwd=APP,check=True)
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  page=browser.new_page(viewport={'width':390,'height':844},has_touch=True)
  page.route('**/csoi-boot.js',lambda route:route.fulfill(status=200,content_type='application/javascript',body=(APP/'csoi-boot.js').read_text()+"\n{const real=AtlasCSOIBoot.load;AtlasCSOIBoot.load=(...args)=>new Promise(resolve=>{window.__releaseBoot=()=>resolve(real(...args))})}"))
  page.goto(BASE,wait_until='domcontentloaded');expect(page.locator('#startupNotice')).to_be_visible();expect(page.locator('.app')).to_have_attribute('inert','');page.evaluate('window.__releaseBoot()');ready(page);page.unroute('**/csoi-boot.js');report['checks'].append('Controlled pending boot shows loading notice and disables controls; release runs original verifier and then enables app')
  # Save a genuine local workspace using the production API, then prove exact persistence.
  saved=page.evaluate('''async()=>{let w=await AtlasWorkspace.create(CsoiDefaultSnapshot.snapshot.dataset);let checkpoint=await AtlasWorkspace.saveLocal(w,CsoiDefaultSnapshot.snapshot.dataset);return {base:w.baseDigest,checkpoint}}''')
  page.evaluate("localStorage.setItem('existing-draft-test','KEEP')")
  for fixture,label in [(old,'oldV4'),(withdrawn,'withdrawnOP')]:
   if not page.locator('#routeMap').is_visible():menu(page,'Route map')
   tool(page,'importSnapshotBtn');page.locator('#snapshotFile').set_input_files(str(fixture));expect(page.locator('#snapshotMessage')).to_contain_text('Explicit replacement required',timeout=30000);page.locator('#applySnapshot').click();expect(page.locator('#snapshotMessage')).to_contain_text('explicitly loaded in memory')
   menu(page,'Research progress / 研究进展');expect(page.locator('#csoiEngineeringTasks')).to_be_visible(timeout=30000);page.get_by_role('link',name='打开 OP 逐页梳理',exact=True).click();expect(page.locator('#csoiResearchResults h2')).to_have_text('OP 逐页梳理',timeout=30000);expect(page.locator('#csoiWorkspace')).not_to_have_attribute('aria-busy','true',timeout=30000)
   if label=='oldV4':expect(page.locator('#csoiResearchResults')).to_contain_text('当前快照没有匹配');expect(page.locator('#csoiResearchResults h2')).to_be_in_viewport();expect(page.locator('#csoiOpReviewProgress')).to_contain_text('0 / 143')
   else:
    page.locator('#csoiResearchResults .csoi-records a').first.click();expect(page.locator('#csoiOpSourceReading')).to_contain_text('当前内容、来源或关联版本已变化',timeout=30000)
   stored=page.evaluate('async base=> (await AtlasWorkspace.loadLocal(base)).checkpoint',saved['base']);assert stored==saved['checkpoint'];assert page.evaluate("localStorage.getItem('existing-draft-test')")=='KEEP';report['checks'].append(label+': actual explicit import/navigation, honest missing or withdrawn state, saved IndexedDB checkpoint and localStorage unchanged');save()
  # A controlled startup rejection must be visible and preserve saved state.
  page.route('**/csoi-boot.js',lambda route:route.fulfill(status=200,content_type='application/javascript',body=(APP/'csoi-boot.js').read_text()+"\nAtlasCSOIBoot.load=async()=>{throw Error('QA_STARTUP_FAILURE')};"))
  page.goto(BASE);expect(page.locator('#startupNotice')).to_have_attribute('role','alert');expect(page.locator('#startupMessage')).to_contain_text('QA_STARTUP_FAILURE');expect(page.locator('.app')).to_have_attribute('inert','');assert page.evaluate("localStorage.getItem('existing-draft-test')")=='KEEP';page.screenshot(path=str(OUT/'controlled-boot-failure-390.png'));page.unroute('**/csoi-boot.js');page.get_by_role('link',name='重新加载页面',exact=True).click();ready(page)
  assert page.evaluate('async base=> (await AtlasWorkspace.loadLocal(base)).checkpoint',saved['base'])==saved['checkpoint'];report['checks'].append('Controlled startup failure visibly blocks dead controls; actual reload link recovers without clearing stored checkpoint');page.close();browser.close()
 report['status']='PASS';save();print('PASS boot readiness/failure/retry and explicit old/withdrawn snapshot navigation with preserved local storage',flush=True)
except BaseException as e:report.update(status='FAILED',failure={'type':type(e).__name__,'message':str(e)[:2500]});save();raise
finally:server.shutdown()
