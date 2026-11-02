"""Actual desktop/mobile acceptance for append-only P0/P1 source corrections.

Own localhost server; no deployment, Council accounts or automatic persistence.
Fixtures/downloads stay temporary; only own prefixed evidence is retained.
"""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from urllib.parse import quote,urlparse
import datetime,json,os,subprocess,tempfile,threading,traceback
from playwright.sync_api import sync_playwright,expect

APP=Path(os.environ.get('CSOI_APP_PATH',str(Path(__file__).resolve().parents[1]))).resolve()
OUT=Path(os.environ.get('CSOI_QA_OUT',str(APP/'qa/remediation'))).resolve();OUT.mkdir(parents=True,exist_ok=True)
BASE='http://127.0.0.1:8892/'
OLD='csoi:dcp:snowy2013:A2:4:1:drainage';NEW='csoi:dcp:snowy2013:A2:4:2:drainage';PARENT='csoi:dcp:snowy2013:A2:4:2'
AMP='csoi:source-note:smrc-water-amp-2025:revision-and-network-scope';MINIMUM='csoi:dcp-reference:snowy:potable-accommodation'
result={'format':'csoi-remediation-browser-1','startedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'appPath':str(APP),'browserChecks':'REAL_CHROMIUM','results':[],'externalRequests':[],'sourceBodiesCommitted':False,'CouncilAccountWrites':False,'automaticPersistence':False}
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
def navigate(page,path,heading='Inside the knowledge'):
 page.evaluate('(path)=>location.hash="#"+path',path)
 expect(page.locator('#csoiWorkspace h1')).to_have_text(heading,timeout=60000)
def knowledge(page,identifier):navigate(page,'/knowledge/'+quote(identifier,safe=''))
def tools(page,button):
 if page.locator('#toolsMenu').get_attribute('open')is None:page.locator('#toolsMenu>summary').click()
 page.locator('#'+button).click()
def export(page,path):
 page.evaluate('location.hash="#/atlas"')
 expect(page.locator('#routeMap')).to_be_visible()
 if page.locator('#toolsMenu').get_attribute('open')is None:page.locator('#toolsMenu>summary').click()
 with page.expect_download()as download:page.locator('#exportBtn').click()
 download.value.save_as(str(path))
def run_node(code,*args):
 r=subprocess.run(['node','-e',code,*map(str,args)],cwd=APP,text=True,capture_output=True)
 if r.returncode:raise AssertionError(r.stdout+r.stderr)
 return r.stdout.strip()

server=ThreadingHTTPServer(('127.0.0.1',8892),partial(Quiet,directory=str(APP)))
threading.Thread(target=server.serve_forever,daemon=True).start()
failure=None
try:
 with tempfile.TemporaryDirectory(prefix='csoi-remediation-browser-')as temporary,sync_playwright()as p:
  temporary=Path(temporary);browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);result['browserVersion']=browser.version
  for width,height in [(1440,900),(390,844)]:
   context=browser.new_context(viewport={'width':width,'height':height},reduced_motion='reduce',accept_downloads=True);page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
   def network_gate(route):
    parsed=urlparse(route.request.url)
    if parsed.hostname in ['127.0.0.1','localhost']:route.continue_()
    else:result['externalRequests'].append(route.request.url);route.abort()
   context.route('**/*',network_gate)
   row={'viewport':[width,height],'status':'IN_PROGRESS'};result['results'].append(row)
   try:
    page.goto(BASE+'#/knowledge/'+quote(OLD,safe=''));host=page.locator('#csoiWorkspace');expect(host.locator('h1')).to_have_text('Inside the knowledge',timeout=60000)
    expect(host).to_contain_text('Retained correction history');expect(host).to_contain_text('STALE');expect(host).to_contain_text('New review planning is unavailable')
    expect(host.get_by_role('link',name='Plan an independent source review',exact=True)).to_have_count(0)
    page.screenshot(path=str(OUT/f'phase1-old-drainage-withdrawn-{width}.png'))
    host.get_by_role('link',name='Open corrected clause and application type',exact=True).click()
    expect(host).to_contain_text('section4.2');expect(host).to_contain_text('type and scale')
    expect(host.locator('nav[aria-label="Research clause ancestry"] a[href="#/knowledge/'+quote(PARENT,safe='')+'"]')).to_have_count(1)
    expect(host.get_by_role('link',name='Plan an independent source review',exact=True)).to_have_count(1)
    page.screenshot(path=str(OUT/f'phase1-corrected-drainage-{width}.png'));row['withdrawnWrongApplicationAndCorrectedParent']='PASS'

    knowledge(page,AMP);expect(host).to_contain_text('PDF pages1,3,13');expect(host).to_contain_text('Table4 Assets by Location');expect(host).to_contain_text('PDF14 is Table5 Assets by Type')
    expect(host.get_by_role('link',name='Original source receipt and review gates',exact=True)).to_have_count(1)
    expect(host.get_by_role('link',name='Trace pinned record to source',exact=True)).to_have_count(1)
    page.screenshot(path=str(OUT/f'phase1-water-amp-locator-{width}.png'));row['waterAmpPdf13Table4']='PASS'

    knowledge(page,MINIMUM);expect(host).to_contain_text('MINIMUM');expect(host).to_contain_text('>=');expect(host).to_contain_text('L/person/day');row['minimumCapacitySemantics']='PASS'
    snapshot=temporary/f'phase1-export-{width}.json';export(page,snapshot)
    independent=subprocess.run(['node',str(APP/'verify-snapshot.cjs'),str(snapshot)],cwd=APP,text=True,capture_output=True,check=True);row['independentSnapshotVerifier']=independent.stdout.strip()
    exported=json.loads(snapshot.read_text());d=exported['dataset'];by={e['id']:e for e in d['domain']['entities']};notes=[e for e in d['domain']['entities']if e['id'].startswith('csoi:source-note:')]
    assert len(d['contentItems'])==127 and len(d['domain']['entities'])>=137 and len(notes)==25
    assert by[OLD]['data']['csoiRecord']['state']=='WITHDRAWN'and by[NEW]['data']['csoiRecord']['data']['dcpClause']['parentId']==PARENT
    assert len([r for r in d['domain']['revisions']if r['logicalId']==OLD])>=2
    assert any(r['logicalId']==OLD and r['record']['data']['csoiRecord']['state']!='WITHDRAWN'for r in d['domain']['revisions'])
    for note in notes:
     inner=note['data']['csoiRecord'];source=next(s for s in d['domain']['sourceCatalogue']['sources']if s['id']==inner['data']['sourceId']);assert {'id':source['id'],'revisionId':source['revisionId']}in inner['inputs'];assert inner['data']['sourceDigest']==source['rawDigest'];assert inner['provenance']['url']==source['officialUrl']
     assert any(r['logicalId']==note['id']and r['record']['data']['csoiRecord']['inputs']==[]for r in d['domain']['revisions'])
    row['currentNoteSourcePins']=len(notes);row['retainedEmptyInputNoteHistory']=len(notes);row['legacyContentItems']=127;row['exportedEntities']=len(d['domain']['entities']);row['datasetDigest']=exported['audit']['datasetDigest']
    history_check="""const fs=require('node:fs'),assert=require('node:assert/strict'),M=require('./atlas-model.js');(async()=>{const d=JSON.parse(fs.readFileSync(process.argv[1])).dataset,b=require('./qa/remediation/corrections-original-verification.json').baseline;d.domain.revisions=d.domain.revisions.slice(0,b.revisionCount);d.domain.events=d.domain.events.slice(0,b.eventCount);d.domain.sourceCatalogue.sources=d.domain.sourceCatalogue.sources.slice(0,b.sourceCount);d.domain.sourceCatalogue.events=d.domain.sourceCatalogue.events.slice(0,b.sourceEventCount);const versions=new Map(d.domain.revisions.map(r=>[r.logicalId,{...structuredClone(r.record),revisionId:r.id}]));d.domain.entities=b.entityIds.map(id=>versions.get(id));d.domain.assertions=b.assertionIds.map(id=>versions.get(id));assert.equal(await M.objectDigest(d),b.datasetDigest);assert(await M.verifySnapshot(await M.exportSnapshot(d)));console.log('PASS exact audit-baseline dataset/history reconstructed from retained prefix');})().catch(e=>{console.error(e);process.exitCode=1});"""
    row['immutableAuditBaselinePrefix']=run_node(history_check,snapshot)

    for note in notes:
     knowledge(page,note['id']);expect(host).to_contain_text(note['label']);expect(host.get_by_role('link',name='Original source receipt and review gates',exact=True)).to_have_count(1);expect(host.get_by_role('link',name='Trace pinned record to source',exact=True)).to_have_count(1)
    row['genericNoteReceiptAndTraceLinks']=25
    knowledge(page,AMP);host.get_by_role('link',name='Trace pinned record to source',exact=True).click();expect(host.locator('h1')).to_have_text('Typed path-set comparison');expect(host).to_contain_text('GOVERNED_INPUT_LINEAGE',timeout=60000);expect(host).to_contain_text('REJECTED_UNKNOWN_ADMISSION')
    with page.expect_download()as download:host.get_by_role('button',name='Export pinned path comparison proof',exact=True).click()
    proof=temporary/f'phase1-note-proof-{width}.json';download.value.save_as(str(proof));independent=subprocess.run(['node',str(APP/'verify-paths.cjs'),str(snapshot),str(proof)],cwd=APP,text=True,capture_output=True,check=True);row['independentNotePathProofVerifier']=independent.stdout.strip()

    withdrawn=temporary/f'phase1-withdrawn-{width}.json'
    withdraw="""const fs=require('node:fs'),M=require('./atlas-model.js'),I=require('./atlas-intake.js');(async()=>{const d=JSON.parse(fs.readFileSync(process.argv[1])).dataset;for(const id of ['csoi:smrc-dcp-snowy-2013-amend3:20261030','csoi:smrc-water-amp-2025:20261030'])d.domain.sourceCatalogue=await I.correctStage(d.domain.sourceCatalogue,id,'SOURCE_RETRIEVED',{actor:'public-synthetic-browser-QA',at:new Date().toISOString(),reason:'Withdraw byte verification in a temporary public browser acceptance fixture'});fs.writeFileSync(process.argv[2],JSON.stringify(await M.exportSnapshot(d)));})().catch(e=>{console.error(e);process.exitCode=1});"""
    run_node(withdraw,snapshot,withdrawn)
    page.evaluate('location.hash="#/atlas"');expect(page.locator('#routeMap')).to_be_visible();tools(page,'importSnapshotBtn');page.locator('#snapshotFile').set_input_files(str(withdrawn));expect(page.locator('#snapshotMessage')).to_contain_text('Explicit replacement required',timeout=60000);page.locator('#applySnapshot').click();expect(page.locator('#snapshotMessage')).to_contain_text('explicitly loaded in memory')
    knowledge(page,NEW);expect(host).to_contain_text('STALE');expect(host.get_by_role('link',name='Plan an independent source review',exact=True)).to_have_count(0);row['withdrawalBlocksNewCorrectedClauseReview']='PASS'
    knowledge(page,AMP);expect(host).to_contain_text('DEPENDENCY_SOURCE_BYTES_NOT_CURRENT');expect(host).to_contain_text('false');page.screenshot(path=str(OUT/f'phase1-source-withdrawal-{width}.png'));row['withdrawalInvalidatesGenericNoteContext']='PASS'
    knowledge(page,'csoi:dcp:cooma2014:7:4:2:2:soil');expect(host).to_contain_text('SOURCE_PINNED_RESEARCH_PENDING_REVIEW');expect(host.get_by_role('link',name='Plan an independent source review',exact=True)).to_have_count(1);row['unaffectedSourceContextRetained']='PASS'
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');assert not errors,errors;assert not result['externalRequests'],result['externalRequests'];row['browserErrors']=errors;row['status']='PASS_TESTED_HERE';context.close()
   except Exception:
    row['status']='FAIL';row['error']=traceback.format_exc();page.screenshot(path=str(OUT/f'phase1-browser-failure-{width}.png'));context.close();raise
  browser.close()
except Exception:
 failure=traceback.format_exc();result['error']=failure
finally:
 server.shutdown();server.server_close();result['finishedAt']=datetime.datetime.now(datetime.timezone.utc).isoformat();result['status']='FAIL'if failure else'PASS_TESTED_HERE';(OUT/'phase1-browser-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
if failure:raise SystemExit(failure)
print('PASS: desktop/mobile append-only corrected application type, AMP page locator,25source-note links/pins/history,110minimum, independent snapshot/path proof, explicit withdrawn-source import and isolated review blocking')
