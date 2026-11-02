#!/usr/bin/env python3
"""Read-only 80-task closure audit. Writes only its own author directory."""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parents[2]
ROOT = APP.parents[1]
BASE = '1bd44ea96bf742e63072d866502479ca34d34061'
P = 'PUBLIC_SOURCE_RESEARCH'
R = 'RUNTIME_INTEGRATION'
F = 'FOUNDER_DECISION'
A = 'AUTHORISED_PRIVATE_ACCESS'
H = 'HUMAN_OR_HARDWARE_ACCEPTANCE'
registry_path = APP / 'COI_TASK_REGISTRY_V1_7.json'
registry = json.loads(registry_path.read_text())
native_path = APP / 'qa/lsps-completion/native-reconciled.json'
native = json.loads(native_path.read_text())
native_by_test = {x['test']: x for x in native['results']}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def ref(path, needle=None, line=None, note=None):
    p = APP / path
    if path.startswith('ROOT:'):
        p = ROOT / path[5:]
    lines = p.read_text().splitlines()
    if line is None:
        line = next((i for i, text in enumerate(lines, 1) if needle in text), None) if needle else 1
    assert line and line <= len(lines), (path, needle, line)
    return {'path': str(p.relative_to(ROOT)), 'line': line, 'sha256': digest(p), 'locator': needle or 'line '+str(line), 'note': note or ''}

def ev(path, needle=None, line=None):
    return (path, needle, line)

# The authored findings below are deliberately task-specific. Requirements are copied
# exactly from the original registry, not shortened or reinterpreted in this table.
findings = {}
def add(n, actual, gap, types, next_action, criterion, evidence, tests, founder='NONE', stale=''):
    findings[n] = dict(actual=actual, gap=gap, types=types, next=next_action, criterion=criterion, evidence=evidence, tests=tests, founder=founder, stale=stale)

add(1,'既有基线矩阵、原始回归矩阵和当前 NEXT_SESSION 均存在；本审计重新固定 HEAD，并按原 80 项编号复查。','本项基线能力已有；历史报告只适用于各自源码，不能代替本轮全工程完成结论。',[], '后续变更以本基线逐项追加差异，不另建应用。','基线注明源码、原任务编号、证据日期、剩余边界；旧历史保留。',[ev('qa/CSOI_BASELINE_MATRIX.md'),ev('NEXT_SESSION.md')],['csoi-model.test.cjs'])
add(2,'边界文档明确未访问原 WCOS；目前只有独立编写的概念链，不能证明原系统接口存在或兼容。','缺获授权的原 WCOS 模块目录、抽象接口契约和准许检查的环境；不是公开资料下载问题。',[A,F], '现在可准备不含客户数据的接口清单模板，列模块、读写能力、标识符、版本、日历语义；维持原系统不接入。','获授权范围内逐一核对七类原模块及接口；给出许可范围、版本与原件证据，未取得前保持 BLOCKED。',[ev('docs/CSOI_WCOS_BOUNDARY.md','COI-002'),ev('csoi-wcos.js','function adapt')],['csoi-wcos.test.cjs'],'CONDITIONAL_PRIVATE_SCOPE','保留真实访问阻塞；不要把未接入 WCOS 当作整个公开系统停止条件。')
add(3,'模块命名空间及依赖方向由 MODULES、logicalId、dependencies 校验。','未发现本项有限模块契约的新缺口；实际私有 WCOS 兼容性另属 002/031/040。',[],'新增来源模块时使用现有命名空间与依赖校验。','合法 ID/依赖通过，跨模块越权依赖和非法 ID 被拒绝。',[ev('csoi-governance.js','const MODULES'),ev('csoi-governance.js','function dependencies')],['csoi-governance.test.cjs'])
add(4,'四类安全分类存在；assessPublic 对私有、受保护、未知和伪造获准发布拒绝。','本项拒绝策略可用；没有获授权发布角色验证器并不意味着可以跳过它。',[],'保持新增入口全部经过相同权限校验。','四类与未知状态在存储、显示、导入导出通道均按边界处理，伪造批准不能放行。',[ev('csoi-governance.js','const SECURITY'),ev('csoi-governance.js','function assessPublic')],['csoi-governance.test.cjs'])
add(5,'authority() 明示 Council 权威记录系统，独立研究不得发出正式决定。','本项权威边界已实现；不把正式决定被禁止误报为应立即解除的功能缺陷。',[],'在新来源和页面继续明确研究与业务权威的区别。','任意研究记录不能发出、批准、发送或覆盖 Council 业务记录。',[ev('csoi-governance.js','function authority'),ev('docs/CSOI_WCOS_BOUNDARY.md','The bridge')],['csoi-governance.test.cjs'])
add(6,'嵌套敏感字段、版权模式、保密和小样本检查存在，导入导出使用同一治理门槛。','程序检测不能代替真实数据披露风险的人类判断；当前没有真实私有数据。',[],'维持公开/合成输入；任何新增真实聚合须单独授权与披露审核。','恶意嵌套 PII、机密、小样本与自报批准负例被拒绝，公开作者摘要保持可用。',[ev('csoi-governance.js','function inspectPayload'),ev('csoi-governance.js','SMALL_CELL_OR_DISCLOSURE_RISK')],['csoi-governance.test.cjs'])
add(7,'原 Atlas 类型集合、不可变 revision 和迁移接口继续被 CSOI 复用。','未发现已限定的类型迁移要求的新缺口；类型存在不证明真实来源内容完整。',[],'未来来源记录继续通过同一类型/时空/权限契约。','旧 127 项与快照兼容，非法类型、旧 revision 写入和权限升级拒绝。',[ev('atlas-domain.js','const TYPES'),ev('atlas-domain.js','async function migrateDataset')],['csoi-model.test.cjs','domain.test.cjs'])
add(8,'路由清单和实际页面渲染存在，保留 route-first Atlas 入口及旧内容。','页面可运行不等于每页全部公共知识已梳理；内容缺口见 B/E。',[],'复用原路由扩充已授权内容并做受影响页面回归。','主要页面可打开、深链接及返回有效，原路线/127项未丢失。',[ev('csoi-router.js','const ROUTES'),ev('csoi-pages.js','async function render'),ev('atlas.js','function render')],['csoi-router.test.cjs','route-main.test.cjs'])
add(9,'测试矩阵与最新 acceptance 将软件、资料、准入分开记录。','三重状态需要持续更新，不能因 native PASS 把资料和人类准入变为 PASS。',[],'以本逐项基线更新后续验收口径，保留失败后修复的过程证据。','每批报告分别列实际测试、资料范围与准入边界。',[ev('qa/CSOI_TEST_MATRIX.json'),ev('qa/lsps-completion/acceptance.json','overallProject')],['csoi-governance.test.cjs'])
add(10,'原测试 runner、真实浏览器运行器和历史分包回执存在；后续 B–H 已实际推进。','这是历史 Pack A 交付里程碑，不是每次重做 A 或再次等待 Pack B 的理由。',[],'直接继续本基线列出的未完成工作。','测试命令与真实回执、推送/续接记录可追溯；不把历史回执冒充新跑结果。',[ev('run-tests.cjs'),ev('qa/run-local-browser.py'),ev('NEXT_SESSION.md')],['csoi-router.test.cjs'])
add(11,'CSP 核心表已形成 14目标/44策略/63指标；LSPS 本轮已补叙述和地图；OP 仍只有指定活动片段，目录观察不等于全文件研究。','DP、资源/财务/资产计划、年度报告的完整具体版本/采用日期及受控当前性未全部核验；OP 全 142 页尚待逐项研究。',[P,R], '完成已登记 OP 142 页原件清点；随后按目录核对 DP/资源/财务/资产/年报的版本表和确切定位，记录冲突。','逐份要求有版本、日期、目录→原件链、字节、页级范围和冲突结论；不明当前性明确 UNKNOWN。',[ev('csoi-intake.js','async function extendCatalogue'),ev('qa/strategy-completion/REPORT_ZH.md','OP 2026'),ev('qa/csp-metric-review/acceptance.json','sourceReview'),ev('qa/lsps-completion/acceptance.json','semanticUnits')],['csoi-intake.test.cjs','csoi-strategy-research.test.cjs'],'NONE','LSPS 非编号叙述/地图不再是未开始任务；不能从旧剩余范围继续复制。')
add(12,'LSPS 118页有逐页处置、512语义单元和27地图出现位置；历史三地 DCP 记录与时空拒绝规则存在。','LSPS 地图目视研究不是地块 GIS；现行 LEP/DCP/SEPP 整体修订、法定图层及地块适用证据不完整。',[P,R], '整理 LEP/DCP/SEPP 文档—修订—地图索引，逐一比较采用/生效/地域；有授权公开原件时补精确来源。','每个规划来源标明版本与空间/时间范围；错地域、过期、草稿与缺地块数据不得给出适用结论。',[ev('csoi-lsps-context.js','function scope'),ev('qa/lsps-completion/acceptance.json','mapOccurrences'),ev('applicability.test.cjs')],['csoi-lsps-context.test.cjs','applicability.test.cjs'],'NONE','“继续 LSPS 地图/叙述”已被 v4 有限交付取代；现行法定空间适用缺口仍真实。')
add(13,'来源登记、元数据阶段、精确摘要输入和 sources 搜索页面已实现。','登记量不是整个要求语料分母；字段 UNKNOWN 必须保留。',[],'将后续 OP 等来源纳入既有登记并显示缺字段。','来源可查 URL、版本/日期、哈希和定位，无法证明字段不编造。',[ev('csoi-intake.js','async function extendCatalogue'),ev('csoi-pages.js','function sourcesPage')],['csoi-intake.test.cjs','intake.test.cjs'])
add(14,'阶段 intake、独立原件核验和公开研究资料包已运行；不自动授予官方准入。','完整要求语料还未逐份到达提取/精确定位/版本核验阶段；阶段机制已存在，人工准入不可由代码自行补。',[P,R], '逐份补 OP/DP/资源与法规阶段矩阵：已取字节、提取范围、锚点、当前性、待人工项分别填。','每个纳入来源都有可复查阶段回执和负例；缺失阶段显示明确缺口，不用一个 corpus PARTIAL 覆盖全部。',[ev('csoi-intake.js','async function registerSummaries'),ev('atlas-intake.js'),ev('qa/lsps-completion/independent-position/verification.json')],['intake.test.cjs','csoi-receipts.test.cjs'],'NONE','软件 intake 不是未实现；下一步为未覆盖来源逐项补全，不是重复通用框架。')
add(15,'已有 OP 指定8活动及9个不同印刷 CSP 引用研究关系；CSP 策略/目标有来源层级。','完整 DP 中介、全部 OP 活动、资金条目与明确战略关系尚未清点；来源印刷引用不是实际履约或因果。',[P,R], '逐行提取全 OP 印刷引用，再检 DP/预算的明确交叉引用；把无引用目标列为未关联，不靠同名补边。','所有新增关系有来源版本/页/行和明确关系种类；有分母并列缺链，撤回源后关系失效。',[ev('qa/strategy-completion/relationship-coverage.json'),ev('csoi-intake.js','async function registerPlanningFacts'),ev('csoi-knowledge.js')],['csoi-strategy-research.test.cjs','csoi-planning.test.cjs'],'NONE','已有有限关系应保留，但不等于全 CSP→DP→OP 完成。')
add(16,'LSPS 的12优先事项、83实施行动和18冲突观察保持独立；历史空间说明和 DCP 路径可比较。','旧 LEP/DCP 的具体修订及当下适用关系仍 UNKNOWN；来源计划表中的勾选不证明正式现行法定链。',[P,R], '从 LSPS 明确提及的 LEP/DCP 文本与图层索引建立引用观察；按真实日期/地域校验，保留18冲突。','只有来源明确支持的路径进入研究模型；战略一致性不自动生成义务，缺日期/地域不连成已适用链。',[ev('sources/lsps-public-knowledge.json'),ev('csoi-lsps-context.js','function project'),ev('csoi-paths.js')],['csoi-lsps-context.test.cjs','csoi-paths.test.cjs'],'NONE','已有 LSPS 全页有界阅读与历史路径，不应重复声称完全未梳理。')
add(17,'八类公开 PHE/WCOS 来源页面已登记，存在原件回执与4项法规访问失败记录。','部分权威法规/指引尚未取得可核正文或确切当前版；Food/Health 与地方页面存在版本差异。',[P], '先用已合法可读的官方目录/原件补每类来源版本矩阵；对被拒 URL 仅在有新相关证据且确认未执行时考虑受约束重试。','每类要求有权威来源、版本及获取/缺失状态；访问失败精确归属来源，不能伪造取得或当前性。',[ev('csoi-phe.js','const SPECS'),ev('sources/csoi-legislation-access.json'),ev('sources/csoi-source-observations.json','"coverage"')],['csoi-phe.test.cjs','csoi-intake.test.cjs'],'NONE','403/503 是历史逐 URL 证据，不是本次网络重测，也不是阻止所有公开研究的通用理由。')
add(18,'PHE 有条件入口和通用多阶段研究步骤，DCP 有详细历史段落；L2 可保存条件/反证/裁量。','每一法/指引的义务、例外与程序条件未全面拆解；通用 steps 和源摘要不能代替逐条义务表。',[P,R], '优先对已取得 LTW 指引建立章节/条款条件矩阵，再对八类来源形成对象—触发—例外—证据表。','范围内每条规则有确切来源与条件/例外；缺条款或法律适用性明确 UNKNOWN，研究计划不冒充 Council SOP。',[ev('csoi-phe.js','const domains='),ev('csoi-phe.js','function workflow'),ev('csoi-layers.js','async function statement')],['csoi-phe.test.cjs','csoi-layers.test.cjs'],'NONE','原 next_action 中比较/日历已有实现，剩余是逐条规则研究与模型接入。')
add(19,'coverage() 分别报告登记记录、请求、字节回执、研究摘要和零准入，而非单一完成率。','全要求语料总体分母仍 UNKNOWN；已有“覆盖率可测”不表示内容全覆盖。',[],'以全 OP 及后续来源逐项分母更新覆盖视图，保留明确未知。','登记/字节/提取/权利/准入指标不可互换，缺口队列可定位具体来源。',[ev('csoi-intake.js','function coverage'),ev('sources/csoi-source-observations.json','"coverage"')],['csoi-intake.test.cjs','intake.test.cjs'])
add(20,'来源研究页面可打开原件定位、保留版本与负例；后续开发已跨过 B 包。','本项有限软件交付已在；不能把它写成全部法规研究完成。',[],'继续非受阻来源研究并维持版本/撤回负例。','有真实可点来源和具体定位；缺失、变更、撤回不继续显示通过。',[ev('csoi-pages.js','async function knowledgeEvidence'),ev('csoi-pages.js','async function researchPage')],['csoi-knowledge.test.cjs','csoi-source-integrity.test.cjs'])
add(21,'L0 source() 建独立身份/版本/事件；公共治理只容许摘要/合成或明确元数据，敏感原件不搬入。','未发现有限 L0 身份契约新缺口；原私有件尚未授权访问。',[],'新原件继续临时读取、仅保留合法摘要与回执。','身份/原始散列可追溯，受保护正文不进入公共仓库或导出。',[ev('csoi-layers.js','async function source'),ev('csoi-governance.js','function assessPublic')],['csoi-layers.test.cjs','csoi-receipts.test.cjs'])
add(22,'normalizeIdentity 按物业、场所、活动、连接、设备、事件分型并保留有效期；重复与非法键拒绝。','有限身份能力已有；未验证真实 WCOS 身份映射。',[],'后续公开/合成对象继续使用类型和时间区间，不按地址强制合并。','不同监管对象分母保持独立；重复冲突和历史时段非法输入拒绝。',[ev('csoi-layers.js','function normalizeIdentity'),ev('csoi-layers.js','async function normalize')],['csoi-layers.test.cjs'])
add(23,'L2 statement() 可区分规则/观察/推论/裁量/UNKNOWN，并要求反证与未知列表；正式决定由治理拒绝。','现有 PARTIAL 混合了软件分类与正式业务决定准入；需要逐要求验收说明，而不是解除正式决定禁止。',[R,H], '补一份 L2 验收逐类矩阵：五种研究陈述及 FORMAL_DECISION 拒绝、counterevidence/UNKNOWN 保留；由父任务判断窄软件范围能否闭合。','明确本项是类型/证据边界还是需真实获授权决定；前者可独立验收，后者保持未授权，不用人类同意制造权限。',[ev('csoi-layers.js','async function statement'),ev('csoi-governance.js',"FORMAL_DECISION_NOT_AUTHORISED")],['csoi-layers.test.cjs','csoi-governance.test.cjs'],'NONE','比较/复核日历不是本项缺口；建议拆软件验收与业务准入后再决定状态，不直接升 VERIFIED。')
add(24,'L3 校验公式、单位、时间/区域、分子分母与输入 revision；独立重算检测自洽伪造。CSP63指标复核仍阻止未具依据计算。','有限核算基础已交付；63指标缺真实方法/输入，不能据此计算实际进展。',[],'只对可准入且口径明确的输入开放对应计算；其余保留 NOT_COMPUTABLE。','源变更失效、历史可验证；错误单位/分母与伪造重算被拒绝。',[ev('csoi-layers.js','function calculate'),ev('csoi-layers.js','async function quantify'),ev('csoi-metric-review.js','function project')],['csoi-recompute.test.cjs','csoi-metric-review.test.cjs'])
add(25,'aggregate 要求不重叠的合格对象分母、完整回执与最低5样本；工作覆盖不等于合规。','公开/合成机制已在；真实披露风险仍需实际授权数据环境审核。',[],'继续保留完整分母和 UNKNOWN，不用未检查对象充当合规。','重复分母/小样本/未知资格拒绝或明确未知，风险消除与合规不被自动生成。',[ev('csoi-layers.js','async function aggregate')],['csoi-layers.test.cjs','csoi-work.test.cjs'])
add(26,'prepareRelease 只生成 REVIEW_PENDING 研究草稿，officialReport=false，不升级安全等级。','正式 Council 报告审批并未接入，属于边界而非已完成真实发布。',[],'保留草稿、分享审查及正式报告的区别。','L5 输出不能被自报批准变成正式或获准发布。',[ev('csoi-layers.js','async function prepareRelease')],['csoi-layers.test.cjs','csoi-governance.test.cjs'])
add(27,'跨层转换强制顺序、责任角色、质量报告和相同安全分类；撤回/重算保留历史。','有限治理转换能力已在；外部见证/真实业务授权仍未知。',[],'新转换遵循原序列与来源输入 pins。','缺责任、越层、分类混用、失效来源和错误回执拒绝。',[ev('csoi-layers.js','async function transform'),ev('csoi-layers.js','async function verifyDerivation')],['csoi-layers.test.cjs','csoi-recompute.test.cjs'])
add(28,'quality() 对重复、来源冲突/丢失、时空不符、非采用法律、过期、单位和身份冲突给出明确原因。','规则拒绝测试已在；拒绝不证明真实语料本身完整无误。',[],'按新来源发现增加有依据的负例，不扩大未知为有效。','逐类错误返回相应原因，不能将 UNKNOWN 静默转零。',[ev('csoi-layers.js','function quality')],['csoi-layers.test.cjs','csoi-recompute.test.cjs'])
add(29,'研究记录注册在原 Atlas registry，沿用不可变 revisions、snapshots 和原127内容。','没有另建图；后续扩展仍需检查历史和导出兼容。',[],'新增 OP 内容继续通过现有注册接口与 boot 等价检查。','旧快照可验证、旧历史保留、当前缓存与完整注册相等。',[ev('atlas-domain.js','async function registerResearchRecord'),ev('csoi-lsps-context.js','async function apply')],['csoi-model.test.cjs','csoi-boot.test.cjs'])
add(30,'L0–L5 权限、来源撤回、历史重放与独立计算回执负例存在并有最新记录结果。','本项测试范围不包括未接入私有系统或真实正式授权。',[],'新增分支复用对应权限/撤回/历史负例。','坏输入被拒绝且未污染保留历史，历史导出和当前适用状态分开。',[ev('csoi-layers.test.cjs'),ev('csoi-recompute.test.cjs')],['csoi-layers.test.cjs','csoi-recompute.test.cjs'])
add(31,'adapt() 的12类概念链只验证仓库作者编写的 syntheticFixture；返回 privateCompatibility BLOCKED。','未提供获授权原 WCOS 技术契约，不能把同名年度链当作真实系统映射。',[A,F], '现在可产出抽象字段映射草案和无敏感数据的契约测试清单；待合法原契约可用再核对。','真实授权契约逐阶段对应、版本和差异可复查，兼容测试有准许环境；未满足保持 BLOCKED。',[ev('csoi-wcos.js','function adapt'),ev('docs/CSOI_WCOS_BOUNDARY.md','COI-002')],['csoi-wcos.test.cjs'],'CONDITIONAL_PRIVATE_SCOPE','真实契约缺失继续有效；不要求为完成公开来源研究先提供私有资料。')
add(32,'适配器 READ_ONLY、拒绝写操作/敏感字段/伪造合成标志，公开元数据须受信来源回调。','目前是受限研究适配层，不是已连原 WCOS。',[],'保持不连真实系统；可扩展获准公开元数据的严格校验。','真实私有与任意 self-labelled synthetic 输入不得进入，网络/同步写入不发生。',[ev('csoi-wcos.js','function adapt')],['csoi-wcos.test.cjs'])
add(33,'ltwWorkflow 接受 A/B/C/S 作为研究标签并返回 categoryVerification UNKNOWN；10阶段模板存在。','缺 NSW LTW2021 分类章节的完整触发、排放/设施、approval/concurrence 精确条件矩阵；标签不能算分类引擎。',[P,R], '用已登记官方指引逐章清点 A/B/C/S 条件和例外，给出每项页锚；只把证据充分的条件接入研究判别。','所有类别有来源定义、必要输入、例外、需人工点；缺参数/交叉条件/不适用负例通过，不签发许可。',[ev('csoi-wcos.js','function ltwWorkflow'),ev('csoi-phe.js',"['ltw'")],['csoi-wcos.test.cjs','csoi-phe.test.cjs'],'NONE','模板阶段已存在；真正缺的是精确条款条件，不能再以继续日历替代。')
add(34,'LTW 十阶段含分类、approval/concurrence、pretreatment、monitoring、整改、复检和报告；全部 proposed/UNKNOWN。','这是研究工作流能力，不是正式 Council SOP 或批准结果。',[],'用033精确来源充实模板，维持未授权决定禁止。','十阶段能显示证据缺失/负责角色未知，不因阶段存在生成已完成或正式许可。',[ev('csoi-wcos.js','function ltwWorkflow')],['csoi-wcos.test.cjs'])
add(35,'Backflow 条件识别连接/可测试设备，公共摘要保留年检线索；backflowDue 的适用/版本/锚点门槛生效。','水连接风险等级、设备缺陷/维修/通知/关闭条件没有完整公共条款支撑；public rule 的 anchorVerified/currentVersionChecked 均 false。',[P,R], '核对已取得地方 Backflow 来源的设备、风险、测试、缺陷与通知表述，补当前版/页锚；形成独立条件表。','每个缺陷/到期/关闭判断均有适用证据；缺 current 或 anchor 仍 UNKNOWN；不得将物业等同设备。',[ev('csoi-phe.js','function backflowRule'),ev('csoi-wcos.js','function backflowDue')],['csoi-wcos.test.cjs','csoi-phe.test.cjs'],'NONE','代码门槛不是未实现；资料和状态转换证据才是剩余项。')
add(36,'设备限定的日期计算已处理闰年和错误日期；已核公共规则缺失时返回 UNKNOWN。','真实适用频次和当前有效区间未准入；设备全生命周期提醒尚缺完整源条件，不能给所有物业年检。',[P,R], '随035建立 interval/生效期/设备类别表，给 synthetic 场景补不同频次/更换/停用负例。','只为证据充分的设备生成研究日期；未知/不适用无日期，日期标签不能当法定通知。',[ev('csoi-wcos.js','function backflowDue'),ev('csoi-calendar.js','function recurrence')],['csoi-wcos.test.cjs','csoi-calendar.test.cjs'],'NONE','日历基本运算已完成；不能用年检演示证明全部法定频次。')
add(37,'RULE/EVIDENCE_INFERENCE/DISCRETION/FORMAL_DECISION 四类可区分，formal 被阻断并要求人类审查。','原 WCOS DecisionNavigator 的真实接口、字段和授权角色未核验；研究分类和私有系统兼容是两件事。',[R,A,F], '现在独立完善四类输出的说明和拒绝矩阵；原系统映射单列等待获授权抽象契约。','研究分类负例完整；如验收原 WCOS 复用，则需合法契约逐字段和角色映射，不能只看同名。',[ev('csoi-wcos.js','function judgment'),ev('docs/CSOI_WCOS_BOUNDARY.md','judgment()')],['csoi-wcos.test.cjs'],'CONDITIONAL_PRIVATE_SCOPE','公共分类可继续；原私有兼容保持未验证，不要求现在导出真实决定。')
add(38,'conditionalServices() 按食物活动、排放/下水连接、可测试防回流设备独立判断三条研究路径。','有限交叉条件能力已在；不构成三个真实许可。',[],'继续逐源条件化，保持同一物业多对象和未知事实。','无排放/无连接/无设备或未知时不得自动生成三重义务。',[ev('csoi-wcos.js','function conditionalServices')],['csoi-wcos.test.cjs'])
add(39,'summary()/coverage() 可对合成对象生成清楚分母的到期、完成、风险与工时研究汇总；真实记录直接拒绝。','真实业务聚合和披露检查未接入；现有合成汇总不等于原 WCOS 安全统计输出。',[R,A,F,H], '现在补公开/合成汇总的字段契约、分母和小样本审查清单；禁止为“完成”而放开真实输入。','有限合成汇总可独立验收；真实汇总另需获授权数据契约、合格披露审核和权限边界测试。',[ev('csoi-wcos.js','function summary'),ev('csoi-work.js','function coverage'),ev('csoi-governance.js','SMALL_CELL_OR_DISCLOSURE_RISK')],['csoi-wcos.test.cjs','csoi-work.test.cjs'],'CONDITIONAL_PRIVATE_SCOPE','不能将“真实输入被拒绝”同时宣称真实聚合完成；也不应因此停止公开演示研究。')
add(40,'Outlook adapter 所有网络能力关闭；原 WCOS 兼容性明确 BLOCKED，没有原文件/计划被改写。','缺准许的原 WCOS/Outlook 测试环境和抽象契约，未进行原环境无损兼容演练。',[A,F,H], '准备无敏感资料的预检/回退/只读模拟方案；当前不连接账户、不改日历。','获授权后在指定环境证明原版本/计划/记录前后不变；未获环境前保持 BLOCKED，合成测试不能替代。',[ev('csoi-assistant.js','function outlookAdapter'),ev('docs/CSOI_WCOS_BOUNDARY.md','COI-002')],['csoi-assistant.test.cjs','csoi-wcos.test.cjs'],'CONDITIONAL_PRIVATE_SCOPE','保持真实阻塞和已延期决定；不是要求 Founder 现在开放账户。')
add(41,'八类 PHE 来源与 authority() 保留 statutoryPowers、localInternalAllocation UNKNOWN。','法定机关、Council 公共政策职责及内部实际分工尚未按来源逐项分开；没有官方岗位授权。',[P,R], '建立公开职责/法定机关矩阵，逐项链接法律或公开政策；内部岗位一栏独立 UNKNOWN。','每一角色声明带来源/版本/范围；不能从公开职责推断具体员工或内部分工。',[ev('csoi-phe.js','authority:{'),ev('csoi-phe.js','const domains=')],['csoi-phe.test.cjs'],'NONE','内部角色 UNKNOWN 不阻止公开机关职责研究；历史403不能概括所有页面。')
add(42,'Food 条件入口与研究步骤存在，已有 Council/NSW 来源摘要。','Food Act/Reg、Partnership、风险/频次、投诉/复查/培训/处罚条件未形成完整源条款与当前版矩阵。',[P,R], '先从已可读公开资料提取注册、风险、检查、投诉和复查条件；缺法律正文逐条标注，处罚不推断。','每个流程节点有精确依据和例外，当前法规不明时不输出强制义务或处罚结论。',[ev('csoi-phe.js',"['food'"),ev('csoi-phe.js','function workflow'),ev('sources/csoi-legislation-access.json')],['csoi-phe.test.cjs'],'NONE','有目录/摘要与6步模板，不等于完整 Food 程序；公开补研究无需 Founder 操作。')
add(43,'OSSM 保留安装/运行审批区别；Snowy/Cooma/Bombala 的11个历史阅读选择已可连复核卡和日历。','现行 OSSM 法规、检查策略、风险频次、维护和失败处理依据未完整；历史 DCP 非当前地块决定。',[P,R], '把已有历史段落与现行公开 OSSM 策略/许可说明分栏核对；整理系统类型、风险、维护、失败/水土影响条件。','现行与历史来源不混同；每条条件有源页/版本，未知检查频次与岗位保持 UNKNOWN，撤回源阻断卡片。',[ev('csoi-phe.js','const OSSM_READING'),ev('csoi-phe.js','function historicalContexts'),ev('csoi-review-work.js','async function status')],['csoi-bombala-phe.test.cjs','csoi-phe-context.test.cjs'],'NONE','历史复核卡/日历已经实现，缺的是当前规则/inspection strategy，不是再做同一批卡。')
add(44,'Public pool/spa 路径区分公共设施事实，源摘要明确 Regulation 版本冲突。','通知、消毒/水质阈值、留档、缺陷复查的完整当前规则尚缺，不能从摘要推精确限值。',[P,R], '核对地方与 NSW Health 引用的 Regulation editions，逐项列水质/消毒/记录/复查依据与冲突。','版本冲突保留；精确阈值/频次须有源锚和单位，缺原文不计算合规。',[ev('csoi-phe.js',"['pools'"),ev('csoi-phe.test.cjs','Regulation')],['csoi-phe.test.cjs'],'NONE','旧页面版本差异是具体资料问题，不是整类系统不能研究。')
add(45,'Cooling/warm-water 路径包含系统类型、风险、维护和独立审核者线索，local role UNKNOWN。','登记、风险管理、维护、独立审核和通知的完整当前条件未拆；不能认定本地负责岗位。',[P,R], '逐条结构化已取得 NSW Health 正文中的系统、风险、维护、通知/审计条件，分开机构职责与岗位未知。','每项条件有出处及适用对象；不同系统/审核角色不混同，未知责任不被自动分派。',[ev('csoi-phe.js',"['cooling'"),ev('csoi-phe.js','function workflow')],['csoi-phe.test.cjs'],'NONE','保留公开研究可独立进行；内部职责需另行合法证据。')
add(46,'Skin penetration 判断显式保留 laser-only 和 registered practitioner in health service 排除条件。','卫生、通知、整改、复检与年度报告依据未全面逐条锚定；行业名称不能替代程序事实。',[P,R], '补程序/健康服务场景/排除条件，以及公开通知卫生与年度报表依据的逐条矩阵。','触发与排除都带精确出处；无程序事实为 UNKNOWN，不以美容行业整体生成义务。',[ev('csoi-phe.js',"if(domain==='skin')"),ev('csoi-phe.js',"['skin'")],['csoi-phe.test.cjs'],'NONE','现有排除测试是有限能力；不等于全部卫生/报告条款完结。')
add(47,'环境投诉路径将 complaint 与 breach 分开，列 Council/EPA/其他机关核对步骤。','噪音/污染具体事项管辖、证据和转介规则未全部来源化；投诉不证明违法。',[P,R], '从公开投诉/噪音/污染原文形成事项—管辖—例外—转介表，区分报告事实与判断。','每种可见研究路径能展示依据与替代管辖；无适用证据不得指定处罚或认定违规。',[ev('csoi-phe.js',"['environment'"),ev('csoi-phe.js','authority:{')],['csoi-phe.test.cjs'],'NONE','并非全部依赖法规站点403；先整理已有公开指引可继续。')
add(48,'共用类型可表达活动/设施/风险/条款/检查步骤，source-linked workflow 和合成对象分母存在。','跨8领域具体设施/检查/整改/复检/结果状态还多为通用 PROPOSED/UNKNOWN；不是完整类型化流程实例。',[P,R], '以已核公共条件创建各领域无客户数据的实例/反例；复用原模型，补证据关闭与缺失状态转换。','每类实例各自保留对象ID、来源、检查/整改证据及结果未知；不能用模板步数充当已执行记录。',[ev('csoi-phe.js','function workflow'),ev('csoi-work.js','function coverage'),ev('atlas-domain.js','const TYPES')],['csoi-phe.test.cjs','csoi-work.test.cjs'],'NONE','通用对象模型不是没有，但领域条件和完整状态实例未覆盖。')
add(49,'八条条件研究路由和反例已存在，至少五条路由可运行；历史 OSSM 另有精确来源卡。','“≥5”数量已满足但每条法定/有效期/地域/例外源证据深度不齐；不能靠模板数量结束验收。',[P,R], '选 Food/OSSM/pools/skin/LTW 五条完整公开研究链，逐节点核验来源、条件与反例，缺来源显示断点。','每条有来源→条件→对象→工作提案→证据/人类裁量，源撤回/缺失/不适用均正确阻断，不授予实际义务。',[ev('csoi-phe.js','const examples='),ev('csoi-phe.js','function workflow'),ev('csoi-phe.test.cjs')],['csoi-phe.test.cjs','csoi-phe-context.test.cjs'],'NONE','模板8条不是全面条款研究完成；缺口要按链而非用统一403说明。')
add(50,'PHE catalog/domain 页面有来源、步骤、示例和缺口，8领域可用。','本项页面功能完成不代表041–049的全部条款研究。',[],'随来源完善更新页面，不另建领域应用。','领域→来源→研究工作流→未知/反例可点击，页面不把研究命名为正式程序。',[ev('csoi-router.js',"['wcos'"),ev('csoi-phe.js','const domains='),ev('csoi-pages.js','async function render')],['csoi-phe.test.cjs','csoi-router.test.cjs'])
add(51,'coverage() 区分注册、需审批、已知合格、计划、完成、过期、设备、事件和问题，按service/type/id去重。','有限合成分母能力已在；未知总体不能被称为完整实际库存。',[],'以同一对象定义扩展合成例子和公开统计，不合并物业与设备分母。','重复和冲突检测有效；unknown资格/次数/到期不被算零或合规。',[ev('csoi-work.js','function coverage'),ev('csoi-work.js','function denominatorKey')],['csoi-work.test.cjs'])
add(52,'coverage 消费输入 requiredVisits，算计划/完成/overdue/UNKNOWN；recurrence 只对合成已知适用规则产生日期。','没有覆盖各领域的来源支持频次推导器；风险标签本身不创建应检次数，公共法定频次缺独立准入。',[P,R], '提取已取得公开规则中的触发、风险等级、频次、有效期/例外；构建合成规则决策表并接到现有 counts。','每项应检次数能追到精确适用规则和输入；无规则/未知风险/更换版本不生成虚假应检量。',[ev('csoi-work.js','const required='),ev('csoi-work.js','Risk labels'),ev('csoi-calendar.js','function recurrence')],['csoi-work.test.cjs','csoi-calendar.test.cjs'],'NONE','分母计算已做；缺源频次规则和推导，不应写成工作日历还没开始。')
add(53,'六阶段工时分开 ESTIMATED/MEASURED/ASSUMED，缺项计 UNKNOWN；不换算支出。','有限工时核算可用；没有真实作业测量数据。',[],'保持每阶段基准来源，真实工时不能从提案推断。','阶段缺项/负值/重复任务拒绝或未知，估算和测量分开。',[ev('csoi-work.js','const PHASES'),ev('csoi-work.js','function workload')],['csoi-work.test.cjs'])
add(54,'resources() 计算技能与车辆/培训/设施小时，仅在明确年产能下给FTE等效情景。','没有实际编制/排班/薪资证据，结果明确不是这些事实。',[],'继续使用显式假设，公开资源数字不私自分摊员工。','产能未知则FTE未知；估计工作量不产生实际支出、岗位或人员安排。',[ev('csoi-work.js','function resources')],['csoi-work.test.cjs'])
add(55,'三账分类和财务 typed formulas 存在；approved/revised/committed/actual 可区分，默认仅合成金额。','完整公开预算、修订、收费、资本/运营及年度实支项目尚未逐条入库/对齐，actualCouncilSpend仍UNKNOWN。',[P,R], '全 OP 研究后对公开预算/收费/年度报告财务表逐表提取，保留财政年/币种/计划vs实际/重复分配。','每项财务事实有原表页、单位/年度/角色；同项不重复分摊，预算不能充实支，缺披露的交易不补造。',[ev('atlas-domain.js','DOMAIN_FINANCIAL'),ev('csoi-work.js','function ledgerSummary'),ev('ledger.test.cjs')],['ledger.test.cjs','csoi-work.test.cjs'],'NONE','无需客户/员工或内部流水才能梳理公开财务表；公开资料研究可立即推进。')
add(56,'既有 metric/observation/resource/asset/spatial 类型与单位引擎可表达物理量，保留流量/存量及边界。','有限量纲核算能力已在；完整地域实测库存和GIS不是已交付。',[],'新增公开量必须具备单位、时间、范围和测量口径；缺单位不补吨/ML。','物理与财务不可混算，错单位/时空/边界拒绝。',[ev('csoi-work.js','function ledgerSummary'),ev('atlas-domain.js','const TYPES'),ev('atlas-execution.js','async function derive')],['accounting.test.cjs','ledger.test.cjs'])
add(57,'结果类型分开 Output/Outcome/Contribution；coverage 和 ledger 明确不证明风险消除/环境改善。','实际结果与因果仍未知，属于不能凭软件生成的事实。',[],'新增结果须独立证据与因果限制；只报告已证实的工作/问题状态。','检查完成和问题关闭不自动改成合规、风险消除或环境成果。',[ev('csoi-work.js','function ledgerSummary'),ev('csoi-work.js','environmentalOutcome')],['csoi-work.test.cjs','ledger.test.cjs'])
add(58,'有限 OP→CSP 印刷引用已保留，路径追溯能显示证据及断点；历史 LSPS/DCP 独立。','完整监管工作→OP/DP/CSP/资源明确链不全；官方实施/预算/因果关系未获证明。',[P,R], '以全 OP 印刷引用为起点逐项查 DP/CSP/资源表；只有明确空间事项才关联 LSPS/LEP/DCP。','每条边有源版本/页锚和关系类型，未知/未关联目标可见；不能靠站点归属和文本相似推正式关系。',[ev('qa/strategy-completion/relationship-coverage.json'),ev('csoi-work.js','function reverseTrace'),ev('csoi-paths.js')],['csoi-strategy-research.test.cjs','csoi-paths.test.cjs'],'NONE','已有研究关系不应重复报未实现，但全链仍未完成。')
add(59,'reverseTrace 返回来源、输入回执、公式和反向路径；站点情景不是官方策略关系。','有限反向追踪能力已在；无法追到的真实映射必须显示断点。',[],'将新增公开条目纳入既有输入pins与断点显示。','金额/量/工时均能回到输入及公式；缺官方边明确UNKNOWN而非补边。',[ev('csoi-work.js','function reverseTrace'),ev('atlas-execution.js','function shortestPath')],['csoi-work.test.cjs','ledger.test.cjs'])
add(60,'碳29.9保持历史人均排放；合成水/土地运算和重复/分母/类型负例在原测试中。','真实碳价、总排放、改善结果不在这些合成验收范围。',[],'保持历史指标角色与真实可算性门槛。','29.9不得作价格/总量，未知输入和重复分母不得计算虚假成果。',[ev('csoi-work.test.cjs','PER_CAPITA_TOTAL'),ev('accounting.test.cjs')],['accounting.test.cjs','csoi-work.test.cjs','csoi-metric-review.test.cjs'])
add(61,'Annual Edition 投影 Mission→年/季/月/周/日→Task/Work/Brief/Execution/Evidence/Followup/Report，复用原注册。','有限研究树可用；不是实际 Council 任务排班。',[],'把新公开来源复核任务放在相同年度投影中。','闰年/财政年/ISO周和双向父子导航正确，原模型身份不复制。',[ev('csoi-calendar.js','function annualEdition'),ev('csoi-review-work.js','function project')],['csoi-calendar.test.cjs','csoi-review-work.test.cjs'])
add(62,'AnnualEdition 研究概念、财政年、日期导航与卡片功能已实现，不覆盖 Excel/Outlook。','原 WCOS AnnualEdition 原契约未取得；现在是独立研究实现，不能验证“复用原 WCOS”一致性。',[A,F,R], '现有研究日历继续使用；准备年度/财政年/跨年周/标识符的抽象对照表，原契约可用后只核对。','概念实现与原契约兼容分开验收；后者需合法接口证据且原文件/排班不改。',[ev('csoi-calendar.js','function annualEdition'),ev('docs/CSOI_WCOS_BOUNDARY.md','Annual')],['csoi-calendar.test.cjs','csoi-wcos.test.cjs'],'CONDITIONAL_PRIVATE_SCOPE','Annual Calendar 软件不是尚未开始；剩余原 WCOS 兼容不应阻止研究卡使用。')
add(63,'任务来源分类、sourceBasis、审批状态与责任角色字段受校验，禁止伪造法定授权。','公开研究任务不代表已获 Council/Michele 分派。',[],'保持真实来源与未知角色，提案不变成授权指令。','伪造批准、无证据实绩和不合法来源类型被拒绝。',[ev('csoi-calendar.js','function validateTask')],['csoi-calendar.test.cjs','csoi-capsule.test.cjs'])
add(64,'重复日程有日期/适用/区间/次数上限，依赖循环与先后冲突检测存在。','公共法定义务复发频次仍需052来源；本项基础调度不是准入。',[],'用新增明确研究周期补测试，保持未知规则不生成法定日期。','月末/闰年/异常日期/循环/缺依赖有正确结果或拒绝。',[ev('csoi-calendar.js','function recurrence'),ev('csoi-calendar.js','function conflicts')],['csoi-calendar.test.cjs'])
add(65,'任务卡显示依据、适用、风险、工时、附件、下一步、裁量和历史；实际小时需要记录及证据。','有限任务卡能力已在，卡片内容若缺来源保持明确空缺。',[],'为公开来源复核卡填真实版本pins，保持实际结果未知。','缺证据实际小时不准通过；source/approval/next/discretion保留且可追踪。',[ev('csoi-calendar.js','function validateTask'),ev('csoi-calendar.js','function taskCard'),ev('csoi-review-work.js','async function register')],['csoi-calendar.test.cjs','csoi-review-work.test.cjs'])
add(66,'calendar parents/children/query 与 taskCard 区分计划、记录和成果；复核卡可回到日历。','没有实际 Council 执行数据，日期过去不是违规或完成。',[],'保持时间导航和来源卡回跳，实际仍按证据。','年/月/周/日/卡双向可达；planned与recorded/unknown不混用。',[ev('csoi-calendar.js','function children'),ev('csoi-calendar.js','function parents'),ev('csoi-pages.js','async function calendarPage')],['csoi-calendar.test.cjs','csoi-review-work.test.cjs'])
add(67,'compileWeek 汇总风险、待审、缺附件、过期提案和容量情景；Michele只在草稿标签中，ownerRole UNKNOWN。','未读真实经理日程或 Council 风险；草稿不是发送或正式决定。',[],'在公开/合成范围让周报保持来源与假设清楚。','已知工时与未知容量分开；不存在自动职员分派、发信或提醒。',[ev('csoi-assistant.js','function compileWeek')],['csoi-assistant.test.cjs'])
add(68,'meetingDraft 生成议程、证据问题、待确认决定与未知责任/日期的跟进。','草稿未证明会议发生或经理同意。',[],'保持未确认决定 UNKNOWN，所有跟进只作研究准备。','没有由草稿生成“已同意/已决定”或自动发信。',[ev('csoi-assistant.js','function meetingDraft')],['csoi-assistant.test.cjs'])
add(69,'outlookAdapter 明确 SIMULATION_DISABLED，read/write/send/remind均拒绝，simulate网络调用0。','本项受限模拟按要求成立；真实账户功能与040另需授权。',[],'继续只使用不连账号的模拟；不为展示接入真实 Outlook。','所有实际账号/邮件/提醒调用被拒绝，模拟不产生副作用。',[ev('csoi-assistant.js','function outlookAdapter')],['csoi-assistant.test.cjs'])
add(70,'实际 browser suites 和原日历测试覆盖年/月/卡/来源导航；新PHE复核卡也能进日历。','E2E是在公开/合成研究范围；不证明真实 Council 执行。',[],'每次日历/来源改动复测390与桌面，以及相应来源失效。','端到端入口/回跳/卡片定位通过，缺证据策略关系仍UNKNOWN。',[ev('csoi-pages.js','async function calendarPage'),ev('qa/lsps-completion/browser-final.json'),ev('qa/csoi-browser.py','for width,height')],['csoi-calendar.test.cjs','csoi-review-work.test.cjs'])
add(71,'原 route-first 地图、分支/候选与文本路线入口保留，生产投影测试存在。','有限导航体验已在；不意味着未来动态架构任务已开始。',[],'保持原路线模型和稳定焦点，新增来源复用现有网络。','候选不是正式边；展开/回退/焦点可预期且原内容不变。',[ev('atlas.js','function render'),ev('atlas.js',"textRoutesBtn"),ev('route-main.test.cjs')],['route-main.test.cjs','route-map.test.cjs'])
add(72,'CSP/LSPS/DP/OP等知识、WCOS/PHE、calendar、metrics、sources/audit 等入口真实存在；v4含新LSPS页。','入口完整不等于每个领域全部资料完整，具体缺口在011–018等。',[],'在现有知识页接入全OP，避免第二套网站或图。','每个路由打开真实数据/明确缺口，不以静态假交互替代。',[ev('csoi-router.js','const ROUTES'),ev('csoi-pages.js','async function render'),ev('qa/lsps-completion/acceptance.json','semanticUnits')],['csoi-router.test.cjs','csoi-lsps-context.test.cjs'])
add(73,'内容遍历/分页有5000层及10000宽测试，DCP源树有真实更深层级；不是固定六层截断。','软件有界分页保证可遍历，不是已填无限资料。',[],'按真实章节结构注册新内容，保留迭代遍历与循环拒绝。','深层/宽节点可分页追溯，缺父/循环/假来源拒绝，旧内容兼容。',[ev('deep-content.test.cjs'),ev('csoi-clauses.test.cjs')],['deep-content.test.cjs','csoi-clauses.test.cjs'])
add(74,'搜索允许year/region/law/work/unit等；两记录版本比较和 typed path-set 比较已实现，原文本路线与问题候选存在。','完整法律义务/全 OP/DP 来源索引仍未覆盖；记录文本匹配不是当前适用搜索，未知字段匹配不能假装相等。',[P,R], '全 OP/DP 等纳入后补源支持检索案例；列每个过滤维度的未知排除与跨路径冲突，不重复重建比较器。','用户能在已覆盖语料按维度检索和对比确切源路径；缺语料/未知适用明确可见，缺pin拒绝。',[ev('csoi-router.js','const QUERY'),ev('csoi-pages.js','async function pathComparePage'),ev('atlas-execution.js','async function compareRecords'),ev('atlas.js',"textRoutesBtn")],['comparison.test.cjs','csoi-paths.test.cjs','integration.test.cjs'],'NONE','full path-set comparison 已经交付；不可再等待旧Phase2临时文件才推进公开来源检索。')
add(75,'companionUrl 支持独立同源深链接，browser脚本实际打开弹窗并检查独立导航；单屏/移动布局可用。','模拟浏览器并非真实多显示器硬件认证；硬件体验归076。',[],'继续保持同源参数和移动等价路径。','弹窗不共享错误焦点/导航状态，恶意外域URL拒绝，单屏也可完成任务。',[ev('csoi-router.js','function companionUrl'),ev('qa/csoi-browser.py','companion=popup.value')],['csoi-router.test.cjs'])
add(76,'历史 Chromium 测了390、1440、1600、2560、3840视口、触摸模拟、reduced motion和焦点；最新批次测1440/390。','没有真实屏幕阅读器、物理触屏或真实21:9/32:9/多屏使用验收；宽视口模拟不是硬件，也不是完整可访问性认证。',[R,H], '现在可补程序化可访问名称/键盘顺序/缩放与溢出审计；另准备真实设备+屏幕阅读器脚本和记录表。','在指定真实设备/辅助技术逐流程验收焦点、朗读、触控、缩放/重排与减动；失败修复并有实际证据。',[ev('qa/csoi-browser.py','for width,height'),ev('qa/csoi-browser.py','reduced_motion'),ev('qa/lsps-completion/browser-final.json')],['csoi-router.test.cjs'],'EVENTUAL_HUMAN_HARDWARE','next_action 指向 DCP/比较与本项硬件/可访问性缺口不相干。无需Founder先找代码文件夹。')
add(77,'coverage/acceptance 明确软件、资料、关系、准入与实际KPI互不替代。','本项信息分离能力已在；“49 VERIFIED”仍不得被解释为49实际Council项目完成。',[],'用逐项证据/资料分母更新进度，避免单一总完成率。','工程/研究/关系/质量/实际业绩分别标示，UNKNOWN不被计成果。',[ev('csoi-intake.js','function coverage'),ev('csoi-work.js','governmentKpi'),ev('qa/lsps-completion/acceptance.json','overallProject')],['csoi-intake.test.cjs','csoi-work.test.cjs'])
add(78,'治理、来源导入、不可变知识校验和恶意脚本/HTML/权限升级负例已记录；源文本作为数据处理。','程序负例不等同全面外部安全认证；没有新增真实敏感数据入口。',[],'新增来源与页面复用textContent及同一公共权限门槛。','恶意来源、伪造准入、嵌套秘密和篡改bundle全部拒绝，不执行源指令。',[ev('csoi-governance.js','function inspectPayload'),ev('csoi-pages.js','textContent'),ev('csoi-knowledge.test.cjs')],['csoi-governance.test.cjs','csoi-knowledge.test.cjs','workspace.test.cjs'])
add(79,'最近45原生文件经完整44PASS/1fixture失败后修正重跑记录为PASS；6真实Chromium套件通过，深宽递归/导出/并发仍有回归。','本审计未重跑这些测试；旧回执的测试SHA与当前文件逐个核对，源码更新后的验收仍由父任务执行。',[],'完成全OP新批后运行适用完整原生与真实浏览器验收并保留任何初次失败。','最终实际代码对应真实测试回执，源撤回/缺失/导出与10000宽/深层负例不弱化。',[ev('qa/lsps-completion/native-reconciled.json'),ev('qa/lsps-completion/browser-final.json'),ev('deep-content.test.cjs')],['deep-content.test.cjs','workspace-merge.test.cjs','csoi-boot.test.cjs'])
add(80,'已有Founder中文报告、来源矩阵、下一步与同一Draft PR；v4已在明确后续授权下更新原owner-only站。','原要求“不得部署”已被后续仅Council私人站授权具体覆盖；未合并。owner本人交互登录未由代理验证，服务认证不是本人登录。',[],'本次先交80项闭合基线，再按全OP研究和真实剩余缺口推进；继续报告已做/未做/原因/下一步。','Founder可看到可检查报告与当前网站；不把私有试用版或软件49项当全工程完成，未合并/水文站未改。',[ev('qa/lsps-completion/REPORT_ZH.md'),ev('qa/lsps-completion/deployment.json','ownerSignedInBrowser'),ev('NEXT_SESSION.md')],['csoi-strategy-research.test.cjs'],'NONE','“发布私人网站”已完成到v4；只有下一批内容通过测试后更新原站，不能重建/重复站点。')

# Scope calibration against the original Master Plan, not broadened acceptance.
# A complete legal corpus and professional accessibility certification were NOT
# prerequisites of the bounded software requirements 023 / 074 / 076.
findings[23].update(
    gap='五种研究陈述与正式决定拒绝已有代码和测试。本审计尚未形成原要求逐子项验收的独立闭合判断；不得把正式决定授权接入新增为023的软件前提。',
    types=[R],
    next='按原023逐类列证据：规则、观察、推论、裁量、正式决定边界、反证、UNKNOWN；父任务完成独立读回后判断窄软件范围状态。',
    criterion='六类含义及反证/UNKNOWN有可检查行为，正式决定始终与研究输出分离；无需真实正式决定或官方准入才能验收分类软件。',
    stale='现有分类软件有证据。正式业务权限与完整法规语料是另一个维度，不能继续作为023通用软件阻塞；状态仍由父任务独立验收后决定。')
findings[74].update(
    gap='原074要求的软件入口均可找到：搜索/7类过滤、两记录及路径集比较、问题/候选与文本路线。尚需把这些实际验收证据逐子项汇总读回；完整法规或OP语料不是074的软件新增前提。',
    types=[R],
    next='汇总已存搜索、比较、路径、问题候选、线性替代的实际断言/浏览器证据；父任务只复测证据不足子项，独立判断软件闭合。公开语料覆盖另归011–018。',
    criterion='按原要求每个入口/过滤/比较/问题候选/文字替代都有实际行为与相应否定例证据；允许如实显示缺语料/UNKNOWN，不要求全法律语料才验收软件。',
    stale='full path-set comparison已交付。旧next_action与完整资料/旧Phase2恢复混用，不能据此维持软件PARTIAL；需独立逐子项验收再由父任务决定，作者未升状态。')
findings[76].update(
    gap='五种视口、键盘、触摸模拟、低动效、焦点和分页已有不同批次证据；基本读屏实际体验的可检查回执未找到。原要求不等于完整WCAG认证或强制购买真实多屏硬件。',
    types=[R,H],
    next='先映射原076各子项已存浏览器证据，补基本读屏的可访问名称/阅读顺序/控件状态实际检查；使用可用辅助技术记录结果，只有必须人工操作的环节才安排人工验收。',
    criterion='390px与16:9/21:9/32:9、键盘/触屏、低动效、焦点上下文、长表分页及基本读屏逐项有实测证据；明确模拟环境限制，不额外要求专业认证。',
    founder='EVENTUAL_BASIC_ASSISTIVE_TECH_ACCEPTANCE',
    stale='旧next_action的DCP/比较与076不相干。应补原范围的基本读屏等验收证据，不能把专业硬件认证或必需Founder设备操作写成原要求。')
findings[74]['evidence'] += [ev('atlas.js','const showLegacyCrossings'),ev('qa/csoi/browser-paths.json'),ev('qa/csoi/browser-comparison.json')]
findings[74]['tests'] += ['discovery.test.cjs','csoi-router.test.cjs']
findings[76]['evidence'] += [ev('qa/csoi/browser-h.json'),ev('csoi-pages.js',"Next calendar items")]

assert set(findings) == set(range(1,81))
master = 'ROOT:docs/research/public-strategy-atlas/CSOI_V1_7_80_Task_Master_Plan.md'
rows=[]
for t in registry['tasks']:
    n=int(t['id'].split('-')[1]); f=findings[n]
    tests=[]
    for name in f['tests']:
        result=native_by_test[name]
        tests.append({'testFile':ref(name), 'recordedResult':ref('qa/lsps-completion/native-reconciled.json', '"test": "'+name+'"'), 'recordedStatus':result['status'], 'recordedAt':native['at'], 'currentTestFileMatchesRecordedSHA256':digest(APP/name)==result['testSHA256'], 'recordedSummary':result['stdout'].strip(), 'runInThisAudit':False})
    stale=f['stale'] or ('这是历史顺序提示；B–H及后续来源/页面批次已推进，保留现能力即可，不应重复从Pack B开工。' if n<=10 else '按本行 actual/remaining/criterion 判定；原通用 next_action 不作为未完成证据。')
    rows.append({'id':t['id'],'pack':t['pack'],'exactOriginalRequirement':t['title_and_scope'],'requirementReference':ref(master,'**'+t['id']+'**'), 'registryReference':ref('COI_TASK_REGISTRY_V1_7.json','"id": "'+t['id']+'"'),'registryStatus':t['status'],'recommendedStatus':'KEEP_'+t['status'],'statusDecisionOwner':'PARENT_AFTER_INDEPENDENT_REVIEW','actualBoundedImplementation':f['actual'],'implementationEvidence':[ref(*e) for e in f['evidence']],'testEvidence':tests,'remainingGap':f['gap'],'gapTypes':f['types'],'independentlyExecutableNextAction':f['next'],'completionCriterion':f['criterion'],'founderActionNeededNow':False,'eventualDependency':f['founder'],'whatDoesNotRequireFounderAction':'公开官方资料梳理、作者摘要、现有模型内开发与测试、证据报告和同一Draft PR续接已获授权；不需Founder找目录或转发任务书。'+(' 本行可先准备无敏感信息的契约/验收材料；原私有接入仍维持延期，未要求现在开放。' if f['founder']=='CONDITIONAL_PRIVATE_SCOPE' else ''),'originalBlocker':t['blocker'],'originalNextAction':t['next_action'],'staleOrOverbroadPlanAssessment':stale,'officialAdmission':'PENDING_NOT_GRANTED','actualCouncilDelivery':'UNKNOWN','auditMethod':'Read current implementation and assertion sources plus recorded results; no new app test execution, no network or private access.'})

subcriteria = {
  23: [
    ('研究陈述种类','IMPLEMENTED_BOUNDED', 'csoi-layers.js statement()接受 RULE/OBSERVATION/EVIDENCE_INFERENCE/DISCRETION/UNKNOWN。'),
    ('正式决定的区别','IMPLEMENTED_DENIAL_BOUNDARY', 'FORMAL_DECISION 在治理层被拒绝；不需要制造真实正式决定来证明已区分。'),
    ('反证和未知','IMPLEMENTED_BOUNDED', 'counterevidence/unknowns为显式数组，规则必须带source revision/locator/role/applicability。'),
    ('独立闭合判定','PARENT_READBACK_PENDING', '作者仅指出原通用阻塞过宽；状态调整由父任务逐子项证据读回后决定。')],
  74: [
    ('统一搜索/年度地区法规来源工作单位过滤','IMPLEMENTED_BOUNDED', 'csoi-router QUERY、csoi-pages filter form、AtlasExecution search；integration/router tests和历史comparison浏览器证据。'),
    ('跨路径比较','IMPLEMENTED_BOUNDED', 'compareRecords与comparePathSets、原生comparison/paths及历史桌面移动浏览器证据。'),
    ('问题导航/解释性候选暗线','IMPLEMENTED_BOUNDED', 'Atlas discovery与cross-path questions/explanations/falsifiers/counterevidence，discovery测试；不是新自然语言智能代理。'),
    ('线性文字替代','IMPLEMENTED_BOUNDED', 'atlas.js Text route guide沿实际可见边显示始末可点击入口。'),
    ('独立逐子项验收','PARENT_READBACK_PENDING', '旧总体PARTIAL不能用完整法律语料缺失代替软件差距判断；父任务补不足验收证据后决定。')],
  76: [
    ('390px和三种桌面比例','RECORDED_BROWSER_VIEWPORT_CHECKS', '历史390/1440/1600/2560/3840视口；本批最新1440/390。声明日期与模拟限制。'),
    ('键盘/触屏/低动效/焦点','RECORDED_BOUNDED_CHECKS', 'csoi-browser.py以has_touch模拟移动输入、reduced_motion、键盘Enter和focused heading检查。'),
    ('长表分页','IMPLEMENTED_BOUNDED', 'records及calendar分页、audit分页；深宽内容测试。有界分页不等于全部屏幕阅读体验。'),
    ('基本读屏','EVIDENCE_GAP', '未找到实际基本朗读/可访问树+阅读顺序/控件状态的逐流程验收回执；不新增专业认证要求。')]
}
for row in rows:
    n=int(row['id'].split('-')[1])
    row['softwareCapabilityAssessment']={
        'state': 'EXISTING_BOUNDED_ACCEPTANCE' if row['registryStatus']=='VERIFIED' else ('IMPLEMENTED_SUBCRITERIA_CLOSURE_READBACK_PENDING' if n in [23,74,76] else ('ORIGINAL_PRIVATE_CONTRACT_UNVERIFIED' if n in [2,31,40] else 'PARTIAL_WITH_IMPLEMENTED_SUBCRITERIA')),
        'meaning':row['actualBoundedImplementation']}
    row['publicEvidenceAssessment']={
        'state':'BOUNDED_PUBLIC_RESEARCH_INCOMPLETE' if P in row['gapTypes'] else 'NOT_A_COMPLETE_CORPUS_CLAIM',
        'isFullCorpusCompletionAClosurePrerequisite':False if n in [23,74,76] else None,
        'meaning':'本行已引用的公开/合成证据仅证明其明确范围；全文/规则研究不足另列来源任务，不自动作为每个软件任务的阻塞。'}
    row['humanAdmissionAssessment']={
        'state':'OFFICIAL_ADMISSION_NOT_GRANTED',
        'isOfficialAdmissionASoftwareClosurePrerequisite':False,
        'meaning':'正式业务决定/法定适用/真实披露仍由相应合法权限与专业判断约束；不从工程PASS推正式准入，也不将正式准入新增为研究软件通用完成前提。'}
    row['subcriteria']=[{'requirementPart':a,'state':b,'evidenceMeaning':c} for a,b,c in subcriteria.get(n,[('原要求有限能力','BOUNDED_EVIDENCE_RECORDED',row['actualBoundedImplementation']),('剩余条件','NONE_NEW_FOR_BOUNDED_SCOPE' if row['registryStatus']=='VERIFIED' else 'OPEN',row['remainingGap'])])]

counts=Counter(t['status'] for t in registry['tasks'])
types={k:[r['id'] for r in rows if k in r['gapTypes']] for k in [P,R,F,A,H]}
data={'format':'csoi-original-80-closure-baseline-1','createdAt':'2026-11-02','baselineCommit':BASE,'scope':'80 original ENGINEERING tasks, not 80 Council projects; read-only author audit, no status promotion','registrySHA256':digest(registry_path),'registryStatusCounts':dict(counts),'taskCount':len(rows),'newApplicationTestsExecuted':False,'recordedTestEvidence':'Latest native-reconciled + browser-final at LSPS v4 batch; per-test SHA checked against current file. A recorded PASS is not a new run or full-source completion.','statusChangesApplied':0,'dependenciesAreNotAllFounderActions':True,'gapTypeTaskIds':types,'publicOrRuntimeWorkCanProceedWithoutFounder':[r['id'] for r in rows if P in r['gapTypes'] or R in r['gapTypes']],'privateTasksRemainDeferred':['COI-002','COI-031','COI-040'],'originalPhase2':'Original uncommitted Phase2 temporary files remain inaccessible from this environment; neither declared lost nor recovered. Later public-source reconstruction is new work.','sourceScope':{'CSP':'CSP：核心5主题、14目标、44策略和63指标已按来源结构化，63指标已独立语义读回；36页全部背景叙述/图表/上下文尚未逐句结构化。63指标仍为NOT_COMPUTABLE，缺底层方法/真实观察不能计算实际成绩。','LSPS':'LSPS：118页各有明确处置；76个页面节点含512个作者语义单元，27处地图；原83条实施行动及18条冲突观察保留。已交付有界历史来源解释，不是GIS地块核准、现行法律适用或官方准入。','OP':'OP：在本固定基线，仅PDF73–74的8项指定活动、11条核心记录、9个不同活动→CSP印刷引用及另行核对的既有Food/LTW引用。全142页活动分母尚待清点，父任务随后开展的完整研究另算新交付。','DP_resources_finance_annualReports':'DP、资源、财务、年度报告：完整版本/覆盖/明确关系与公开财务表研究尚未完成。'},'deploymentEvidence':ref('qa/lsps-completion/deployment.json'),'deploymentLimits':'Existing Council owner-only trial v4; canonical app4abe263be3d383ecf3ac1367ffb462d8fe683035 differs from later documentation HEAD. Recorded48live assets match,5live suites,3anonymous403; no owner signed-in browser session. No deployment performed by this audit.','tasks':rows}
(HERE/'closure-baseline.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
fields=['id','pack','registryStatus','recommendedStatus','exactOriginalRequirement','actualBoundedImplementation','remainingGap','gapTypes','independentlyExecutableNextAction','completionCriterion','founderActionNeededNow','eventualDependency','whatDoesNotRequireFounderAction','staleOrOverbroadPlanAssessment','softwareCapabilityAssessment','publicEvidenceAssessment','humanAdmissionAssessment','subcriteria','originalBlocker','originalNextAction','requirementReference','implementationEvidence','testEvidence']
with (HERE/'closure-baseline.csv').open('w',newline='',encoding='utf-8-sig') as stream:
    writer=csv.DictWriter(stream,fieldnames=fields);writer.writeheader()
    for row in rows:
        writer.writerow({k:json.dumps(row[k],ensure_ascii=False,separators=(',',':')) if isinstance(row[k],(dict,list)) else row[k] for k in fields})

refs={}
for row in rows:
    for r in [row['requirementReference'],row['registryReference'],*row['implementationEvidence'],*[x['testFile'] for x in row['testEvidence']],*[x['recordedResult'] for x in row['testEvidence']]]:
        refs[(r['path'],r['line'])]=r
manifest={'format':'csoi-closure-evidence-index-1','baselineCommit':BASE,'references':list(refs.values()),'referenceCount':len(refs),'files':len({x['path'] for x in refs.values()}),'currentTestSHAAllMatch':all(t['currentTestFileMatchesRecordedSHA256'] for row in rows for t in row['testEvidence']),'newTestsExecuted':False}
(HERE/'evidence-index.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')

unfinished=[r for r in rows if r['registryStatus']!='VERIFIED']
report=['# 原80项工程任务闭合基线（作者审查）','',f'固定源码 `{BASE}`。本批已经逐项形成80行JSON/CSV，保留登记表的49 VERIFIED、28 PARTIAL、3 BLOCKED；没有改登记状态、运行时、源码资料包或网站。80项是工程任务，不是80个Council项目。','',
'- [80项逐行JSON](closure-baseline.json)：完整原要求、现有代码/测试行号和文件散列、具体缺口、下一步、完成条件。',
'- [80项CSV](closure-baseline.csv)：便于筛选和阅读。',
'- [证据索引](evidence-index.json)：固定本次审阅文件与定位。','',
'## 哪些工作现在就能继续','',
'公开资料梳理和原模型内开发无需Founder再找文件夹、生成任务书或开放私有资料。优先把全142页OP逐项清点，再补DP/资源/预算/年度报告的真实引用和财务条目；同时可深化已取得LTW、Backflow和PHE公开条件。原私有WCOS三项仍延期，不阻断这些工作。','',
'| 缺口类型 | 涉及未完成任务数（可重叠） | 说明 |','| --- | ---: | --- |']
labels={P:'公开来源具体内容/版本/条件研究',R:'在原模型中补规则、状态或逐要求验收',F:'仅未来解除私有范围延期时需范围决定，不是现在反复请示',A:'原WCOS契约/准许环境等合法访问条件',H:'实际硬件/辅助技术或真实业务披露/正式准入审查'}
for typ in [P,R,F,A,H]: report.append(f'| {typ} | {len(types[typ])} | {labels[typ]} |')
report+=['','没有任何一行要求Founder现在先行动才可做本批公开工作。002/031/040是真实私有契约阻塞；037/039/062只有原私有兼容或真实聚合部分依赖该契约。076应补原范围的基本读屏等验收证据，程序化检查和可用辅助技术可以先做；不能额外要求专业认证或强制购买硬件。正式Council决定不能靠Founder一般同意或软件测试自动授予。','',
'## 现有实现究竟差在哪里','',
'代码已能做研究工作流、分类、计划、日历、分母/工时、版本对比和源路径追溯；下一批不该再重复搭这些框架。仍需补足的具体证据包括：LTW A/B/C/S目前只是待核标签；Backflow公共规则的锚点/当前版门槛仍未满足；应检次数目前由输入提供而非完整源规则推导；账本能分类/核算，却没有全部公开预算和年度实支条目。PHE多为条件入口和通用拟议步骤，不能把8条模板当8类法律程序全面完成。','',
'| 未完成任务 | 具体剩余缺口 | 可独立推进的下一步 |','| --- | --- | --- |']
for r in unfinished:
    report.append('| '+r['id']+' '+r['registryStatus']+' | '+r['remainingGap'].replace('|','／')+' | '+r['independentlyExecutableNextAction'].replace('|','／')+' |')
report+=['','## 必须修正的旧“下一步”说法','',
'- LSPS非编号叙述/地图已在v4完成有界研究，旧报告中的“仍未做”只代表当时。现有27张地图目视解释不等于GIS地块核准；当前法规适用性仍未知。',
'- 记录比较、typed path-set comparison、历史DCP复核卡和Annual Calendar均已实现。COI018/023/029/059/073/078/079等不应再用这些通用后续项解释本项缺口。COI074应逐子项汇总搜索、比较、问题导航/候选与文字替代验收，不能把完整法规语料作为软件验收新前提。',
'- COI076的旧next_action谈DCP/比较，不能回答基本读屏等原范围验收证据缺口；宽视口模拟限制须说明，不扩大为专业硬件认证。',
'- 原私人网站已部署v4；COI080“再发布私人站”不是尚未开始事项。下一批经过测试后更新现有站，不能创建另一套应用。原任务“不部署”已被后续明确仅Council私人站授权具体覆盖；仍不得合并或改水文站。',
'- 法规403与FoodAuthority503属于历史逐URL访问证据，本审计没有网络重测，不能把旧拒绝说成今天重新失败，也不能据此阻断所有可读公开资料。',
'- 原未提交Phase2临时文件当前环境仍不可取得，不能宣称丢失或已恢复；不应把等旧文件作为继续新公开研究的先决条件。','',
'## CSP、LSPS和OP的边界','',
data['sourceScope']['CSP'],'',data['sourceScope']['LSPS'],'',data['sourceScope']['OP'],'',
'CSP旧报告中的LSPS未完成范围已被新批次覆盖；旧审计和新来源研究必须按日期/源码理解。DP/资源/财务/年度报告及完整明确关系仍是公开研究待办。各来源的现行法律适用、官方准入、真实业务执行、实绩与因果仍不能由作者摘要或散列验证代替。','',
'## 本次证据与状态建议','',
'本次实际检查了代码、测试断言和保存的最终回执；没有重跑应用测试。最新原生回执是完整运行44PASS/1测试夹具失败后修复并单独重跑，汇总45个文件通过，不能写成首轮45个全部通过。逐行记录测试文件SHA与当前文件一致性。最新批次6个Chromium套件、桌面1440/移动390；五视口/多屏模拟是历史覆盖，不冒充本次全部重跑，更不冒充真实硬件/屏幕阅读器验收。','',
'本作者建议暂不升任何任务状态。COI023/074应由父任务按原要求逐子项独立读回后判断软件闭合；不得把正式业务权限或完整法律语料新增为软件前提。COI076只要求原范围基本读屏等实测，不扩大为专业认证。其他PARTIAL应按上表补具体证据，不为提高数字降低原要求。','',
'已发布Council v4的资产/服务认证浏览器/匿名拒绝证据保存在 `qa/lsps-completion/deployment.json`；Founder本人登录浏览器仍未代测。本作者未部署或修改任何站点。未来动态架构任务仅保存，未开始实现。','',
'本批80项闭合基线已完成；整个Council项目尚未宣称全部完成。']
(HERE/'REPORT_ZH.md').write_text('\n'.join(report)+'\n')
print(json.dumps({'rows':len(rows),'statusCounts':dict(counts),'gapTypeCounts':{k:len(v) for k,v in types.items()},'evidenceFiles':manifest['files'],'testHashesAllMatch':manifest['currentTestSHAAllMatch']},ensure_ascii=False))
