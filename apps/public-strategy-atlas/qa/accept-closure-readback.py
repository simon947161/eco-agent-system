"""Root readback of original023/074/076 conditions and current executable evidence."""
from pathlib import Path
import datetime,hashlib,json
APP=Path(__file__).resolve().parents[1];REPO=APP.parents[1];OUT=APP/'qa/audit-closure-20261102';D=OUT/'independent';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
readback=json.loads((D/'readback.json').read_text());browser=json.loads((D/'browser-results.json').read_text());core=json.loads((D/'final-core-results.json').read_text());linear=json.loads((D/'browser/linear-accessibility/results.json').read_text());units=json.loads((D/'source-unit-filter-readback.json').read_text())
assert readback['finalBrowserPassed']and browser['runtimeUnchanged'];assert len(browser['results'])==4
for r in browser['results']:assert r['status']=='PASS_ACTUALLY_TESTED'
for file,h in browser['runtimeFileSHA256Before'].items():assert sha(REPO/file)==h,file
for r in core['results']:
 assert r['exitCode']==0
 for m in r['modules']['modules']:assert m['stableDuringLoad']and sha(Path(m['file']))==m['sha256AtLoad'],m['file']
assert len(linear['results'])==5 and all(r['actualScreenReader']=='NOT_TESTED'for r in linear['results'])
assert units['knownUnitSourceObservationCount']==38 and not units['incorrectlyExcluded']
record={'format':'original-80-task-root-closure-readback-1','at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'BOUNDED_CLOSURE_ACCEPTED','reviewer':'Root agent separate from baseline author and follow-up test reader; code, exact original conditions, evidence and current module hashes read back. No official/professional human admission.','evidenceSHA256':{str(p.relative_to(APP)):sha(p)for p in [D/'readback.json',D/'browser-results.json',D/'final-core-results.json',D/'source-unit-filter-readback.json',D/'path-validation-callgraph.json']},'decisions':[
 {'id':'COI-023','before':'PARTIAL','after':'VERIFIED','scope':'L2 research classification and evidence/counterevidence/UNKNOWN preservation. Original source evidence stays pinned; five research judgments stay distinct; formal decisions are explicitly blocked/separated. No official decision service or complete law corpus added as a software prerequisite.','evidence':'Module-pinned layers/governance and targeted-contract-readback positive/negative assertions.'},
 {'id':'COI-074','before':'PARTIAL','after':'VERIFIED','scope':'Existing unified search; q/year/region/law/source/work/unit filters; typed path and record comparisons; questions/candidates and linear route alternative. Recorded references and research candidates only.','evidence':'4 final browser suites, five-viewports linear/AX supplement,38 actual-source unit filter records and root final path transaction native tests. Original mobile timeout retained; unchanged-limit retry passes after eliminating repeated full validation.'},
 {'id':'COI-076','before':'PARTIAL','after':'PARTIAL','scope':'Current five-viewports, keyboard/emulated touch, reduced motion, focus, pagination and AX-name evidence accepted.','remaining':'Actual basic screen-reader listening/interaction not tested; no available screen-reader in this environment. No professional certification or physical wide-screen purchase requirement invented.','actionStatus':'PENDING_TOOL_OR_HUMAN_ACCEPTANCE_NOT_DENIED'}
 ],'sourceResearchStatus':'PARTIAL','officialAdmission':'PENDING','actualCouncilDelivery':'UNKNOWN','stateOnlyUpdateAfterBrowser':'Only registry status/evidence metadata may now change; no runtime implementation/source bundle change is authorised by this receipt.'}
(OUT/'root-readback.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
registry=APP/'COI_TASK_REGISTRY_V1_7.json';r=json.loads(registry.read_text())
for decision in record['decisions']:
 t=next(t for t in r['tasks']if t['id']==decision['id']);assert t['status']==decision['before'];t['status']=decision['after'];t['evidence_links']=list(dict.fromkeys(t['evidence_links']+['qa/audit-closure-20261102/root-readback.json','qa/audit-closure-20261102/independent/REPORT_ZH.md']))
 t['closureUpdate']={'batch':'OP-FULL-REVIEW-20261102','completedNow':decision['scope'],'remainingGap':decision.get('remaining','原软件范围本轮验收通过；完整研究语料、法律适用与正式准入由相应独立任务继续。'),'nextPublicAction': '保留既有行为的回归；按其他来源任务补公开研究，不将其重新作为本软件项前提。'if decision['after']=='VERIFIED'else'在可用辅助技术或人工环境补实际读屏听读和控件反馈；当前AX树结果只证明对应程序化检查。','runtimeAcceptance':'PASS_BOUNDED_SOFTWARE'if decision['after']=='VERIFIED'else'PARTIAL_BASIC_SCREEN_READER_PENDING','evidence':['qa/audit-closure-20261102/root-readback.json']}
 t['blocker']='NONE_WITHIN_ORIGINAL_SOFTWARE_SCOPE'if decision['after']=='VERIFIED'else t['closureUpdate']['remainingGap'];t['next_action']=t['closureUpdate']['nextPublicAction']
r['updated_at']=record['at'];registry.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print('Root accepted023/074;076 remainsPARTIAL. Original task titles unchanged;51VERIFIED/26PARTIAL/3BLOCKED.')
