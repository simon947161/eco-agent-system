"""Reconcile the complete native run with explicit affected-test reruns; never erase failures."""
from pathlib import Path
from collections import Counter
import hashlib,json,datetime,subprocess
APP=Path(__file__).resolve().parents[1];OUT=APP/'qa/op-completion-20261102'
def read(p):return json.loads((APP/p).read_text())
def sha(p):return hashlib.sha256((APP/p).read_bytes()).hexdigest()
original=read('qa/op-completion-20261102/native/results.json');retry=read('qa/op-completion-20261102/native-retry/results.json')
assert original['completed']==original['testFiles'],'AGGREGATE_NATIVE_STILL_RUNNING'
latest={r['file']:{**r,'evidenceDirectory':'native'}for r in original['results']}
latest.update({r['file']:{**r,'evidenceDirectory':'native-retry'}for r in retry['results']})
render_native=read('qa/op-completion-20261102/native-rendering/results.json')
latest.update({r['file']:{**r,'evidenceDirectory':'native-rendering'}for r in render_native['results']})
readable=read('qa/op-completion-20261102/readable-browser/results.json');assert readable['status']=='PASS'and len(readable['results'])==2 and readable['pagesModuleSHA256']==sha('csoi-pages.js')
files=sorted(p.name for p in APP.glob('*.test.cjs'));assert sorted(latest)==files
for f,r in latest.items():assert r['status']=='PASS_TESTED_HERE'and r['exitCode']==0 and r['sha256']==sha(f),f
regression=read('qa/op-completion-20261102/regression/browser-run.json');assert len(regression['results'])==6 and all(r['status']=='PASS_TESTED_HERE'for r in regression['results'])
op=read('qa/op-completion-20261102/browser/results.json');assert len(op['results'])==2
for r in op['results']:assert r['status']=='PASS_TESTED_HERE'and len(r['pageDetailsOpened'])==142 and len(set(r['unitsExpandedAndRead']))==911
performance=read('qa/op-completion-20261102/performance-browser/results.json');assert len(performance['results'])==2
for r in performance['results']:
 assert r['status']=='PASS_TESTED_HERE'and r['performance']['snapshotBytes']==22743874 and r['performance']['sampleCount']>=142 and r['performance']['maxSampledJSHeapUsedBytes']>0
small=read('qa/op-completion-20261102/final-actual-readback-samples.json');assert small['status']=='PASS_ALL_911_ACTUAL_UNITS'and small['unitCount']==911
registry_before=(APP/'COI_TASK_REGISTRY_V1_7.json').read_text();registry=read('COI_TASK_REGISTRY_V1_7.json');closure=read('qa/audit-closure-20261102/root-readback.json');assert closure['status']=='BOUNDED_CLOSURE_ACCEPTED'
source=read('sources/op-completion-review.json');assert len(source['records'])==143
for t in registry['tasks']:
 if t.get('closureUpdate',{}).get('runtimeAcceptance')=='PENDING_FINAL_TESTS':
  t['closureUpdate']['runtimeAcceptance']='PASS_BOUNDED_OP_APPLICATION_ACCEPTANCE';t['closureUpdate']['evidence']=list(dict.fromkeys(t['closureUpdate']['evidence']+['qa/op-completion-20261102/acceptance.json']))
registry['latest_op_full_review_batch']['status']='SOURCE_AND_APPLICATION_ACCEPTED'
(APP/'COI_TASK_REGISTRY_V1_7.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n')
if (APP/'COI_TASK_REGISTRY_V1_7.json').read_text()!=registry_before:subprocess.run(['python','tools/build-op-review-workbook.py'],cwd=APP,check=True)
record={
 'format':'op-full-bounded-acceptance-1','at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'status':'PASS_BOUNDED_APPLICATION_ACCEPTANCE','projectCompletion':'PARTIAL',
 'checkpointCommit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=APP,text=True).strip(),
 'native':{'distinctFiles':len(files),'results':list(latest.values()),'initialFailuresPreserved':[r for r in original['results']if r['status']!='PASS_TESTED_HERE'],
 'reconciliation':'Complete initial48-file run plus4affected reruns covers49 distinct final test files. Path transaction was added during the initial run; final paths and transaction tests reran. The full cache build uses unchanged registration/assessDependencies logic, while final browser suites use the final path transaction. Then4 affected native reruns and a desktop/mobile rendering check cover the final OP disclosure correction; this is a complete run plus targeted reconciliation, not a fresh full rerun of unchanged cache registration. No widened timeouts.'},
 'localBrowser':{'suiteCount':7,'regression':regression,'opDetails':{'evidence':'browser/results.json','viewports':[r['viewport']for r in op['results']],'pagesOpenedEach':142,'uniqueUnitsExpandedEach':911,'sourceWithdrawal':True,'missingCondition':True,'oldV4Import':True,'exportIndependentRevalidation':True}},
 'performance':{'evidence':'performance-browser/results.json','results':[{'viewport':r['viewport'],**r['performance']}for r in performance['results']]},'actualFinalUnitReadback':{'index':'final-actual-readback-samples.json','indexSHA256':sha('qa/op-completion-20261102/final-actual-readback-samples.json'),'matrix':'final-actual-unit-readback.csv','independentCheck':'independent/compact-final-readback-check.json'},'workbookSHA256':sha('qa/op-completion-20261102/OP与工程验收矩阵.xlsx'),
 'finalRenderingCorrection':{'evidence':'readable-browser/results.json','observedIssue':'Generic OP sourceAnomalies duplicated an expanded technical block already present in the OP disclosure.','change':'One DOM rendering condition excludes the duplicate; original data and all existing disclosure content remain.','validation':'4 affected native reruns plus1440/390 targeted actual rendering, collapse/open content, source link and51/26/3 checks. Full cache/data-input proofs remain applicable; source/cache bytes unchanged.','initialTestAuthorErrors':'First new selector expected pre instead of existing dl; next used getClientRects on nested closed details. Corrected to actual dl and Playwright visibility, original logs retained.','readback':readable},
 'closureReadback':closure,'registryCounts':dict(Counter(t['status']for t in registry['tasks'])),
 'source':{'sourceBundleSha256':sha('sources/op-completion-review.json'),'pages':142,'units':911,'newRecords':143,'semanticReview':'independent/model-readback-review.json','originalPhase2Recovery':'NOT_RECOVERED_INACCESSIBLE_NOT_DECLARED_LOST'},
 'cache':read('qa/op-completion-20261102/cache-build-receipt.json'),
 'publication':'RECORDED_SEPARATELY_IN_DEPLOYMENT_JSON',
 'limits':['Current controlled source version remains UNKNOWN where original conflict exists.','No actual expenditure/outcome, legal applicability, parcel boundary or official relationship is admitted.','COI076 actual speech-screenreader experience remains pending; AX/touch simulation is bounded evidence.','Private002/031/040 deferred; no private data imported.','Architecture-map plan only; no new main interface implemented.'],
 'runtimeSHA256':{}
}
# A complete asset list is generated by the packaging manifest later; this captures current source inputs.
paths=list(APP.glob('*.js'))+list(APP.glob('*.css'))+[APP/'index.html',APP/'COI_TASK_REGISTRY_V1_7.json']+list((APP/'sources').glob('*.js'))+list((APP/'sources').glob('*.json'))
record['runtimeSHA256']={str(p.relative_to(APP)):hashlib.sha256(p.read_bytes()).hexdigest()for p in sorted(paths)}
(OUT/'acceptance.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':record['status'],'distinctNative':len(files),'localBrowserSuites':7,'registryCounts':record['registryCounts']}))
