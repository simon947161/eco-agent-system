#!/usr/bin/env python3
"""Compose criterion-level evidence without changing registry status."""
import csv,datetime,hashlib,json,shutil,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent;APP=HERE.parents[2];ROOT=APP.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(file,needle=None):
    p=APP/file;lines=p.read_text().splitlines();line=next((i for i,s in enumerate(lines,1) if needle in s),1) if needle else 1
    if needle:assert needle in lines[line-1],(file,needle)
    return {'file':str(p.relative_to(ROOT)),'line':line,'sha256':sha(p),'locator':needle}
registry=json.loads((APP/'COI_TASK_REGISTRY_V1_7.json').read_text());requirements={t['id']:t['title_and_scope'] for t in registry['tasks']}
native=json.loads((HERE/'native-results.json').read_text())
loaded_file=HERE/('final-core-results.json' if (HERE/'final-core-results.json').exists() else 'loaded-native-results.json')
loaded=json.loads(loaded_file.read_text())
browser=json.loads((HERE/'browser-results.json').read_text()) if (HERE/'browser-results.json').exists() else None
linear_file=HERE/'browser/linear-accessibility/results.json'
linear=json.loads(linear_file.read_text()) if linear_file.exists() else None
source_unit_file=HERE/'source-unit-filter-readback.json'
source_units=json.loads(source_unit_file.read_text()) if source_unit_file.exists() else None
expected={'csoi-compare-browser.py','csoi-paths-browser.py','discovery-browser.py','integration-browser.py'}
browser_files_current=bool(browser and all(sha(ROOT/p)==h for p,h in browser['runtimeFileSHA256Before'].items()))
source_units_current=bool(source_units and source_units['pagesModuleSHA256']==sha(APP/'csoi-pages.js') and source_units['sourceCacheSHA256']==sha(APP/'sources/csoi-default-snapshot.js'))
browser_pass=bool(browser and expected=={r['script'] for r in browser['results']} and all(r['status']=='PASS_ACTUALLY_TESTED' for r in browser['results']) and browser['runtimeUnchanged'] and browser_files_current and linear and linear['status']=='PASS_BOUNDED_BROWSER_CHECKS' and source_units_current and source_units['status']=='PASS_ACTUAL_SOURCE_RECORDS')
browser_failed=bool(browser and any(r['status']=='FAIL' for r in browser['results']))
loaded_core_stable=all(sha(Path(m['file']))==m['sha256AtLoad'] and m['stableDuringLoad'] for r in loaded['results'][:2] for m in r['modules']['modules'])
rows=[]
def criterion(task,part,actual,status,evidence,test):
    rows.append({'task':task,'requirementPart':part,'actualObservation':actual,'status':status,'implementationEvidence':evidence,'testEvidence':test})
l2ref=[ref('csoi-layers.js','async function statement'),ref('csoi-governance.js','const JUDGMENTS')]
for kind,meaning in [('RULE','带来源版本/定位/角色/适用字段的规则研究陈述；缺任一字段拒绝。'),('OBSERVATION','独立观察类型；不会因观察存在成为正式判断。'),('EVIDENCE_INFERENCE','证据推论类型保留，不与观察或规则混同。'),('DISCRETION','人类裁量研究类型保留，不变成授权决定。'),('UNKNOWN','未知类型与未知内容列表保留，不转换成确定结论。')]:
    criterion('COI-023',kind,meaning,'PASS_ACTUALLY_TESTED',l2ref,['loaded-native-results.json','targeted-contract-loaded-check.log'])
criterion('COI-023','正式决定与研究分类分离','L2拒绝FORMAL_DECISION；治理正式决定不获授权；WCOS judgment呈BLOCKED且governmentApproval=false。这是原要求的分类边界，不要求接入真实正式决定。','PASS_ACTUALLY_TESTED',[*l2ref,ref('csoi-wcos.js','function judgment'),ref('csoi-governance.js','FORMAL_DECISION_NOT_AUTHORISED')],['loaded-native-results.json','csoi-wcos.test.cjs.log','targeted-contract-loaded-check.log'])
criterion('COI-023','反证、未知与来源版本','五种研究类型均经新增audit-only断言确认counterevidence/unknowns逐字保留、source revision绑定、officialDecision=false；坏规则的5个必要字段分别拒绝。','PASS_ACTUALLY_TESTED',l2ref,['targeted-contract-loaded-check.log'])
criterion('COI-023','证据输入与陈述分栏','L2输入证据以inputs中的id/revisionId保存，陈述保存在data.text/judgment，规则依据在data.rule，反证与未知为独立数组；L1继续保留L0源输入。分栏保留证据链不等于证明陈述为真。','PASS_ACTUALLY_TESTED',[ref('csoi-layers.js','function inputRefs'),ref('csoi-layers.js','async function transform'),ref('csoi-layers.js','async function statement')],['loaded-native-results.json','targeted-contract-loaded-check.log'])
parts=[
 ('统一搜索','数值/单位/源/工作搜索有真实原生断言；既有integration浏览器检验搜索结果进入实际记录。',[ref('atlas-execution.js','function searchRecords'),ref('atlas.js','function advancedSearchPanel')],['integration.test.cjs.log','browser/integration-browser/execution.log']),
 ('年度/地区/法规/来源/工作/单位过滤','七维（含搜索词）分别做正例/反例及组合过滤；未知范围排除。法规过滤只搜索记录引用，不承诺现行法律适用。',[ref('csoi-router.js','const QUERY'),ref('csoi-pages.js','function queryFilter')],['targeted-contract-loaded-check.log','csoi-router.test.cjs.log','browser/csoi-compare-browser/execution.log']),
 ('跨路径比较','保留revision的两记录比较和独立pins路径集比较均有原生断言；实际浏览器含来源记录、冲突、未知、导出验证。',[ref('atlas-execution.js','async function compareRecords'),ref('csoi-paths.js','comparePathSets'),ref('csoi-pages.js','async function pathComparePage')],['comparison.test.cjs.log','csoi-paths.test.cjs.log','browser/csoi-compare-browser/execution.log','browser/csoi-paths-browser/execution.log']),
 ('问题导航和解释性候选暗线','从搜索结果进入记录，发现候选展示原因、替代解释、反证和可证伪条件；错地域候选不能升为已知关系，问题/复核可记录为研究意见。',[ref('atlas.js','function discoveryPanel'),ref('atlas.js','const showLegacyCrossings'),ref('atlas-execution.js','async function candidates')],['discovery.test.cjs.log','browser/discovery-browser/execution.log']),
 ('线性文字替代','Text route guide沿当前可见真实边给出起点和终点按钮；补充浏览器逐视口点击实际起点，检查可访问名称/角色。',[ref('atlas.js',"textRoutesBtn")],['browser/linear-accessibility/results.json','linear-accessibility.log'])]
for part,actual,evidence,test in parts:criterion('COI-074',part,actual,'PASS_ACTUALLY_TESTED' if browser_pass else ('BROWSER_READBACK_FAILED_PENDING_REVIEW' if browser_failed else 'NATIVE_PASS_CURRENT_BROWSER_PENDING'),evidence,test)
if source_units:
    criterion('COI-074','真实来源数量的单位过滤','直接检查635实体actual cache中38条明确单位的非合成QuantifiedObservation，含33条CSP指标；全部按同一单位保留。注册/修订时measurement展平到data，模型同时校验两层一致。','PASS_ACTUAL_SOURCE_RECORDS' if source_units['incorrectlyExcluded']==0 else 'FAIL_REAL_SOURCE_UNIT_FILTER',[ref('atlas-domain.js','const measurement=kind'),ref('atlas-domain.js','DOMAIN_MEASUREMENT_RECEIPT_MISMATCH'),ref('csoi-pages.js','function queryFilter')],['source-unit-filter-readback.json'])
for part,actual in [
 ('390px/16:9/21:9/32:9','既有integration脚本在390、1440、1920、2560、3840视口运行；补充线性/AX脚本在390、1440、1600、2560、3840运行。视口模拟不是物理显示器认证。'),
 ('键盘/触屏/低动效','补充脚本使用真实Chromium键盘Enter、390宽has_touch下tap事件和prefers-reduced-motion；不宣称真实物理触屏。'),
 ('可聚焦上下文','源路由h1获得焦点且在视口内，线性按钮可用键盘/触摸模拟打开对应记录。'),
 ('长表分页','原integration脚本加载1000条合成fixture，20行一页，点击Next table rows并断言下一页与无溢出。'),
 ('基本可访问树/名称','读取真实Chromium Accessibility.getFullAXTree，检查heading/button/textbox的名称和非ignored状态，保存逐视口AX记录。')]:
    criterion('COI-076',part,actual,'PASS_BOUNDED_BROWSER_CHECK' if browser_pass else 'CURRENT_BROWSER_PENDING',[ref('qa/integration-browser.py'),ref('qa/audit-closure-20261102/independent/browser-linear-accessibility.py')],['browser/integration-browser/execution.log','browser/linear-accessibility/results.json'])
criterion('COI-076','基本读屏实际体验','当前Linux环境未发现Orca或speech-dispatcher；AX树不是实际读屏会话，未听读/核对朗读顺序与交互反馈。未安装新工具、未要求购买硬件或专业认证。','PENDING_TOOL_OR_HUMAN_ACCEPTANCE',[],['readback.json#screenReaderTools'])
if not loaded_core_stable:
    for row in rows:
        if row['task']=='COI-023':row['status']='PASS_ON_RECORDED_MODULE_SHA_FINAL_SHA_PENDING'
if loaded_file.name=='final-core-results.json':
    for row in rows:
        row['testEvidence']=[x.replace('loaded-native-results.json','final-core-results.json').replace('targeted-contract-loaded-check.log','targeted-contract-final.log') for x in row['testEvidence']]
if browser:
    latest_logs={'browser/'+r['script'].removesuffix('.py')+'/execution.log':r['log'] for r in browser['results']}
    for row in rows:row['testEvidence']=[latest_logs.get(x,x) for x in row['testEvidence']]
for row in rows:
    if row['task']=='COI-074' and row['requirementPart']=='跨路径比较' and 'compareEndpointSets' in (APP/'csoi-paths.js').read_text():
        row['implementationEvidence'].append(ref('csoi-paths.js','async function compareEndpointSets'))
        row['testEvidence'] += ['path-validation-callgraph.json','browser-results-initial.json','../../op-completion-20261102/native-retry/csoi-path-transaction.test.cjs.log']
        row['actualObservation'] += ' 初次移动端超时被保留；父任务将重复整库验证合并为同一私有完整验证事务，既有proof语义保留，并在原限时下重跑。'
recommendations={
 'COI-023':{'recommended':'VERIFIED' if loaded_core_stable else 'PENDING_FINAL_CODE_RECHECK','basis':'原L2分类、反证、UNKNOWN与正式决定边界已有实际加载散列和正/负断言；'+('当前核心仍匹配。' if loaded_core_stable else '父任务随后修改治理中精确SHA256字符串的电话误检规则，最终代码散列读回待完成；不把旧结果当最终版。'),'notRequiredForSoftwareClosure':['完整法规语料','正式Council决定授权','私有WCOS接入']},
 'COI-074':{'recommended':'VERIFIED' if browser_pass else ('KEEP_PARTIAL_BROWSER_FAILURE' if browser_failed else 'PENDING_FINAL_BROWSER_READBACK'),'basis':'原搜索/过滤/比较/问题候选/线性替代逐项已有实现；'+('本次paths移动端click30秒超时，桌面proof验证通过；保留失败，CPU原因未确认，不扩大限时。' if browser_failed else '最终稳定运行时浏览器通过后可按软件范围闭合。'),'notRequiredForSoftwareClosure':['全OP/DP/法规语料完成','所有研究关系正式准入','新自然语言智能代理架构']},
 'COI-076':{'recommended':'KEEP_PARTIAL','basis':'程序化视口/键盘/触摸模拟/低动效/焦点/分页/AX可检查，但实际基本读屏验收未完成。','notRequiredForSoftwareClosure':['购买物理宽屏','专业WCAG认证','Founder寻找代码目录']}}
tools={name:shutil.which(name) for name in ['orca','speech-dispatcher','espeak','espeak-ng','chromium']}
report={'format':'csoi-023-074-076-criterion-readback-1','at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,capture_output=True,text=True,check=True).stdout.strip(),'sameAgentAsBaselineAuthor':True,'reviewIndependenceLimit':'This is a second source-and-execution readback by the author of the closure baseline; it is not a separate independent agent. Parent decides status after review.','requirements':{k:requirements[k] for k in recommendations},'recommendations':recommendations,'sourceResearchStatusUnchanged':'PARTIAL','officialAdmission':'PENDING_NOT_GRANTED','actualCouncilDelivery':'UNKNOWN','screenReaderTools':tools,'nativeEvidence':{'initial':'native-results.json','initialWholeRuntimeChangedDuringParentOPIntegration':not native['runtimeUnchangedAfterChecks'],'loadedCore':loaded_file.name,'coreModulesStillMatchActuallyLoadedSHA':loaded_core_stable,'initialNativeSuitesPassed':8,'additionalAuditOnlyProbePassed':True,'limits':'Initial app-wide manifest changed during concurrent OP integration; only module-pinned/core and final stable browser evidence support closure, not a fabricated final full suite.'},'browserEvidence':'browser-results.json' if browser else 'PENDING_PARENT_RUNTIME_STABILITY','finalBrowserPassed':browser_pass,'subcriteria':rows,'mutations':{'originalAuthorFiles':False,'runtime':False,'registry':False,'site':False,'privateAccess':False},'commands':['python apps/public-strategy-atlas/qa/audit-closure-20261102/independent/run-targeted.py','python apps/public-strategy-atlas/qa/audit-closure-20261102/independent/run-final-core.py','CSOI_READBACK_MODULE_RECEIPT=<independent/output.json> node --require apps/public-strategy-atlas/qa/audit-closure-20261102/independent/capture-module-hashes.cjs <test.cjs>','python apps/public-strategy-atlas/qa/audit-closure-20261102/independent/run-browser-readback.py','python apps/public-strategy-atlas/qa/audit-closure-20261102/independent/build-readback.py']}
report['finalEvidenceBinding']={'browserFilesStillCurrent':browser_files_current,'sourceUnitProbeStillCurrent':source_units_current,'actualSourceUnitEvidence':'source-unit-filter-readback.json','initialBrowserFailureRetained':'browser-results-initial.json','pathCallgraphBeforeAndAfter':'path-validation-callgraph.json','largeExportArchiveReceipt':'large-export-receipts.json' if (HERE/'large-export-receipts.json').exists() else None}
(HERE/'readback.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
with (HERE/'subcriteria.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader()
    for r in rows:writer.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in r.items()})
lines=['# COI023 / 074 软件闭合读回及076验收边界','',
'本次实际读取原任务子条件并运行精确测试；没有修改运行时、冻结作者基线或登记表。执行者同时是原80项闭合基线作者，因此这是第二次源码与实测读回，不能称为另一位独立代理审查。最终状态由父任务复核。','',
f'- COI023：建议 **{recommendations["COI-023"]["recommended"]}**。五种研究类型、反证和UNKNOWN实际保留；正式决定被清楚分离/拒绝；缺源规则字段逐项拒绝。没有把正式业务权限加入软件验收前提。',
f'- COI074：建议 **{recommendations["COI-074"]["recommended"]}**。按搜索、六类过滤、跨路径比较、问题/候选、线性替代逐项检查；完整法规语料不是其软件新增前提。',
'- COI076：建议 **保留PARTIAL**。基本读屏实际体验仍未验证；Chromium可访问树、键盘和触摸模拟只能证明对应有限行为，不是读屏听读或专业认证。','',
'精确8个既有原生测试和额外audit-only分类/过滤断言实际通过。父任务同步接入OP导致首次整体文件manifest变化，该回执已保留并标明；另做了模块加载时散列固定的governance/layers和补充断言，不冒充最终全量测试。','',
'浏览器：'+('四个既有套件及五视口线性/可访问树补充检查均在稳定运行时通过。' if browser_pass else ('comparison桌面/移动通过；paths桌面导出proof验证通过，但390px点击Inspect pinned path sets在30秒超时。原失败日志保留，原因未确认；等待无重型并行测试窗口按原限时复测，不放宽超时。' if browser_failed else '等待父任务确认新OP运行时稳定后执行，不能把临时未生成文件记为原功能失败。')),'','| 原任务子条件 | 实际观察 | 状态 |','| --- | --- | --- |']
for r in rows:lines.append('| '+r['task']+' '+r['requirementPart']+' | '+r['actualObservation']+' | '+r['status']+' |')
lines+=['','完整原要求、代码行号/散列、每个命令与证据路径见 [readback.json](readback.json)；逐项可筛选表见 [subcriteria.csv](subcriteria.csv)。','',
'屏幕阅读器工具探查：'+json.dumps(tools,ensure_ascii=False)+'。实际基本读屏验收是 pending，不是执行被拒绝；没有尝试安装、变更权限或绕过限制。可先使用已产生的可访问树和交互脚本，待可用工具或合适人工环境再补听读。','',
'研究语料仍PARTIAL、官方准入仍PENDING、真实Council执行仍UNKNOWN；软件子任务闭合不改变这三者。']
if (HERE/'large-export-receipts.json').exists():
    lines += ['','5份共113,733,238字节的可再生公开/合成大快照，在浏览器完成后移至 `/tmp/csoi-closure-exports-20261102`，不提交Git；没有删除证据。[逐文件回执](large-export-receipts.json)保留原路径、字节、SHA256、已实际执行的离线验证结果和新位置。proof、小JSON、日志、截图仍在QA。']
(HERE/'REPORT_ZH.md').write_text('\n'.join(lines)+'\n')
print(json.dumps({'recommendations':recommendations,'browserPassed':browser_pass,'coreStable':loaded_core_stable},ensure_ascii=False))
