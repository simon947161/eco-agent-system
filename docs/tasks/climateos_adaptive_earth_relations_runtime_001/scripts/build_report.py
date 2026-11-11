"""Render static research documents and offline slides from archived real run receipts."""
from pathlib import Path
import json,html
TASK=Path(__file__).resolve().parents[1]
r=json.loads((TASK/'evidence/benchmark_final/summary.json').read_text(encoding='utf-8'))
s=json.loads((TASK/'evidence/scenarios.json').read_text(encoding='utf-8'))
t=json.loads((TASK/'evidence/trace.json').read_text(encoding='utf-8'))
base='cf91e4a061341bc33d16400bcf4c6a2c2817aa65'
def write(name,text): (TASK/name).write_text(text.strip()+'\n',encoding='utf-8')
def mean(run,key):return sum(run['final_values'][key])/len(run['final_values'][key])
rows='\n'.join(f"|{k}|{mean(v,'ta'):.6f}|{mean(v,'ts'):.6f}|{mean(v,'water'):.6f}|{mean(v,'q'):.8f}|{v['output']['question']['answer']}|" for k,v in s['runs'].items())
saving=1-r['completed_node_executions']['selective']/r['completed_node_executions']['full_safe']
write('RESULTS.json',json.dumps(r,ensure_ascii=False,indent=2))
write('README.md','''# Typed Earth Relations Runtime · Issue154

状态：IMPLEMENTED_LOCAL_VERIFIED / SYNTHETIC_PHYSICAL_SANDBOX / SCIENCE_PENDING。

- [中文Founder报告](FOUNDER_REPORT_ZH.md) · [离线10页展示](slides.html)
- [唯一任务书](TASKBOOK_ZH.md) · [冻结协议](EXPERIMENT_PROTOCOL.json)
- [源码复用](SOURCE_REUSE.md) · [图契约](GRAPH_SCHEMA.md) · [实际对照](RUNTIME_EXPERIMENTS.md)
- [反例](COUNTEREXAMPLES.md) · [科学边界](PHYSICAL_SCIENCE_LIMITS.md) · [QA](QA.md)
- [下一轮](NEXT_SESSION.md) · [科学评审](CRP_HANDOFF.md)

仓库根目录直接运行，无新增Python依赖：
```shell
python -m cczps_lite.integration.earth_relations run-graph
python -m cczps_lite.integration.earth_relations compare-scenarios
python -m cczps_lite.integration.earth_relations inspect-relations
python -m cczps_lite.integration.earth_relations plan-subgraph --targets question
python -m cczps_lite.integration.earth_relations trace-influences --diamonds 30 --targets diamond_29_a
python -m cczps_lite.integration.earth_relations audit-failures
python -m unittest tests.test_earth_relations
python -m cczps_lite.integration.earth_relations benchmark --output runtime_data/earth_relations/replay
```

浏览器直接打开slides.html，无服务器、网络请求或生产部署。图内数字是已执行CLI结果的回放，不是在浏览器中新算的预测。
''')
write('SOURCE_REUSE.md',f'''# 来源与复用

父PR152固定HEAD `{base}`；工作任务书提交`274f4d20f2049413cb87be7c31e6477aa08a1ebf`。

|来源|实际复用|边界|
|---|---|---|
|`earth_system_coupling/state.py`|原Field、State、Grid、TimeSupport、单位/缺测/时空门、checkpoint|未另建环境状态存储|
|`models.py`|原Atmosphere、Surface、fluxes、advance固定点、双边水焓账、context_state|仅advance增加可选mapper参数和调用点；默认映射与所有公式不变|
|`ports.py`|实际ModelPort.step提案驱动；每次迭代恢复旧clock|只有耦合器在收敛后提交库存|
|`diagnostics.py`|原联合阈值含义、Ce×U不可辨识反例|不提升为自然因果|
|PR147 / PR149已存公共结果|全球ERF与季节ENSO独立端口，保留原空间/时间支撑|不抓取新数据，不转成局地强迫|
|`docs/00_MASTER_ARCHITECTURE/SYSTEM_RELATIONSHIP_MAP.md`|运行、解释与人类治理职责分离|不新建治理/认证基础设施|

原父分支及所有旧研究工件保持原样。当前分支的`models.py`增量不是宣称父工件hash未变；原始hash见父PR152固定结果，当前实现hash见RESULTS.json。26项新增测试中，原advance默认路径和真实端口映射在相同输入下逐字段完全一致。没有读取PR153之外的私人资产，也没有借用私人实现。

公开技术资料（2026-11-11查阅；仅用于机制设计，不宣称实现标准认证）：
- [CSDMS BMI](https://csdms.colorado.edu/wiki/BMI)：明确组件时间、变量与单位接口。
- [preCICE隐式耦合](https://precice.org/couple-your-code-implicit-coupling.html)：同一时间窗的checkpoint、迭代与回滚。
- [preCICE加速配置](https://precice.org/configuration-acceleration)：收敛仍需各参与者内部求解成立；本实现未集成preCICE。

研究选择：外围依赖DAG＋不可拆开的已注册反馈因子。物理反馈交给原数值求解；图只组织计算与证据，不产生新物理定律。
''')
write('GRAPH_SCHEMA.md','''# 图契约与调度

`graph.py`定义冻结Node/Edge数据类，节点和边表为只读MappingProxy；改边须调用with_edge返回新图，避免边表与邻接表失配。SHA绑定完整声明。最多256节点、1024边。

节点包括强迫、模型场、物理过程、统计上下文、诊断、决策问题。OBSERVATION为保留类型，本轮未提供新的观测加载执行操作；不能伪称已实现任意观测插件。操作白名单与节点种类必须匹配。

边记录：source/target、source_field/target_field、源/目标单位与范围、clock、lag_steps、conversion、evidence、source_ref、applicability、numeric、enabled、revoked、required、ledger。字段端点须命中操作契约。当前只支持identity转换；不同单位即使可换算也拒绝，须另经显式适配扩展。required标记用于说明，实际最低依赖由操作注册表强制约束，不能通过改为false删掉必需条件。

五类边：PHYSICAL_FLUX、DECLARED_PROCESS_DEPENDENCY、STATISTICAL_ASSOCIATION、HYPOTHESIS_CANDIDATE、DIAGNOSTIC_DERIVATION。统计/候选边可作为CONTEXT_ONLY存在，不能向数值模型传力。即使把统计节点边改成普通依赖，也会被CONTEXT_CANNOT_FORCE拒绝。执行准入只意味合成沙盒契约满足；正式科学准入始终PENDING。

`coupled`是包含空气与地表的原子因子。内部蒸发/潜热和显热边绑定固定双边账本；任一交换被撤销时整个因子拒绝。q反馈按声明lag调用原模型；初始不足历史时使用明确登记的初态延拓。它不是可随意添加的普通自环。所有其余未注册环拒绝。

选择性计划：从目标迭代计算上游闭包，每个共享节点每时钟最多执行一次；拓扑排序不枚举路径，O(V+E)。反馈求解成本另为O(时间步×固定点迭代×网格数)，不能算进“图线性”保证。计划每次重新计算，不做跨运行缓存或未声明的自适应物理步长。

同一land interval内原空气组件有两次dt/2子步。季节/年度节点各按原时段独立计算一次。lag_water输出前一个已完成水库存，不插值成未知历史。每步回执记录执行节点、条件关闭、实际边、ledger、时间、rollback。

反向追踪返回去重节点/边、深度、来源、拒绝候选；路径计数封顶1,000,000且不展开路径。它是计算依赖追踪，不是由结果唯一反演自然原因。联合情景差是同模型下的数值差，不自动赋予因果含义。
''')
write('RUNTIME_EXPERIMENTS.md',f'''# 实际执行结果

协议EXPERIMENT_PROTOCOL.json在主批运行前固定。最终源码锁定于RESULTS.json；seed={r['seed']}。120配置×2模式×3重复={r['actual_runtime_invocations']}次调用。三次轮换执行顺序，逐模式确定性hash相同。前期可变图实现的首批保留在evidence/benchmark；修复邻接表一致性风险后重跑在evidence/benchmark_final。三批不拼为更多独立样本；第二批保留在evidence/benchmark_before_endpoint_hardening。最终还检查了物理账本必须绑定当前因子、慢域节点不能被改标签为局地。

有效配置50，故意破坏的配置70；对应最终批300次完成、420次拒绝。失败不是预测误差，通过比例不是科学准确率。

|拒绝类别|配置数|
|---|---|
'''+ '\n'.join(f'|{k}|{v}|' for k,v in r['failure_distribution'].items())+f'''

相同条件下输出/最终物理场/拒绝完全一致，最大差0。每模式每个有效配置取一次的执行数：选择性2165、完整安全5044，减少{saving:.1%}；物理ModelPort调用各11662，未节省守恒所需计算。计入三次重复时这些计数乘3，不能混淆。

选择性/完整耗时比中位{r['median_selective_to_full_time_ratio']:.6f}，范围{r['min_max_time_ratio']}；{r['selective_slower_configurations']}/50有效配置选择性更慢。此为本机小任务实测，三次重复不足以证明稳定跨机器加速。请求全部结果时双方122次节点执行，无剪枝收益。

最大水残差{r['max_water_residual_kg_m2']:.8g} kg/m²；能量{r['max_energy_residual_j_m2']:.8g} J/m²。另有逐单元库存与全域焓的独立测试，未只断言回执自称守恒。

最终批{r['elapsed_seconds']:.3f}秒，原始记录{r['archive_bytes']}字节；未触发20分钟/200MB门。三批各自低于门槛；旧10008批未作为本研究重跑，完整仓库回归仍会执行其已有测试。

## 三个实际纵向情景

|情景|空气K|地表K|水库存kg/m²|比湿kg/kg|合成诊断|
|---|---|---|---|---|---|
{rows}

两单元初始地表温度不同；雨脉冲前两个时段分别按1.0、1.2倍降雨输入，之后为0。所有驱动为合成。heat/dry和rain/heat为至少两个联合扰动；差分见evidence/scenarios.json。
''')
write('COUNTEREXAMPLES.md','''# 反例和未通过条件

1. 全部结果都被请求：选择性与完整图各执行122节点；图机制无剪枝收益，实测也可能更慢。
2. 最终50有效配置中13个选择性更慢。大量时间在不可拆分的物理求解内；诊断节点减少不等于同比加速。
3. 30层共享菱形网络：路径数量超过计数上限，但只追踪少量独立节点。按家谱位置枚举路径会重复祖先，按路径累加贡献会重复计算；本实现不将路径数解释成因果贡献。
4. max_iterations=1：NON_CONVERGENCE，失败步状态/端口时钟回滚；已完成步保留。
5. 撤销蒸发交换：PHYSICAL_CLOSURE_REQUIRED，不能只算空气或地表一端。
6. 年度全球ERF/季节ENSO到局地小时字段：UNSUPPORTED_NUMERIC_LINK；改写为普通依赖仍CONTEXT_CANNOT_FORCE。
7. 缺q、错误单位/时间/空间、非有限参数：分别拒绝；不补零或静默重采样。
8. 两倍风速与一半交换系数有相同轨迹：参数不可独立辨识。输出相同不能证实真实机制。
9. 另一个物理因子不能借用现有交换账；全球/季节节点不能仅改标签为局地，新增两个回归测试。
10. 图数据必须不可变。初版存在“更新边表但邻接表保留旧边”的风险；已用不可变映射与with_edge修复，并加入撤销普通依赖的测试。初版与修复批分别归档。

本批没有建立现实因果真值、自动发现正确边、一般空间传输模型或任意第三方过程插件。拒绝这些扩展不等于工程失败；本轮通过的是已声明操作集合。
''')
write('PHYSICAL_SCIENCE_LIMITS.md','''# 物理与科学边界

SYNTHETIC_PHYSICAL_SANDBOX；SCIENTIFIC_ADMISSION=PENDING。没有真实区域预测、甲烷设施排放、因果效应或准确率结论。没有读取私人v200。

原PR152假设全部继承：理想化混合层/地表库存；规定风/气压/净辐射；不求解动量、降水形成、凝结、云微物理；雨和径流显热采用简化参考焓。Ce、容量、扩散、热容量等不是现场校准值。局地水热预算闭合不能证明这些闭合项足以描述真实环境。

热旱/饱和阈值只作为合成条件。边执行准入与科学准入分别记录。单位和时空匹配只排除部分错误，不能自动证明因果。慢尺度公共证据继承PR147/149状态、许可及hash，本轮不提升。

不确定性分为数值误差、参数不可辨识、结构遗漏、来源/适用范围与计时噪声。实验只测有限数值门和运行性能；未声称有预测区间或气候影响的不确定度分布。

反向追踪解释程序实际用过哪些输入，不唯一解释自然原因。情景差分不等于观测识别的干预效应。任何现实行动仍需独立科学评审和Founder批准。
''')
write('FOUNDER_REPORT_ZH.md',f'''# Founder报告：可以计算的关系网络，及其没有做到的事

已亲自实现、运行并复核一个小型Typed Earth Relations Graph：共同上游只执行一次；多个过程分叉后汇入诊断；物理反馈通过真实PR152 ModelPort与原固定点/守恒账推进；错误边拒绝并保留原因。

真正结果：最终120种配置、720次运行；50种有效、70种故意破坏契约。两种调度的请求结果与最终物理场完全一致。节点执行减少{saving:.1%}，耗时中位减少约{(1-r['median_selective_to_full_time_ratio']):.1%}，但13/50反而更慢。所有目标都需要时没有剪枝收益。因此不主张“图一定更快”。

|情景|空气K|地表K|水库存kg/m²|比湿kg/kg|阈值结果|
|---|---|---|---|---|---|
{rows}

这些是实际程序输出的合成实验，不是天气观测或真实设施预测。旧全球甲烷ERF与季节ENSO保留独立节点，禁止变成无依据的本地小时强迫。来源追踪不是因果归因。

工程判断：适合保留“外围依赖闭包＋原子反馈因子”的实现继续评审。它复用已有状态和物理，不要求所有变量两两相连；它在查询少量结果、无关诊断较多时能减少工作。若物理求解占主导、所有结果都需要，收益很小或为负。

实际交付：6个CLI工作流及benchmark、26项新增测试、完整原始结果与失败分布、10页离线桌面/手机展示、科学边界和交接。远程HEAD/CI只以PR精确提交回执为准，不在生成文档时预填成功。

需Founder决定的最少事项：先请ChatGPT审查边准入、原子求解与账本、时滞和计数；是否进入新的模型/观测扩展应另行决定。本轮不合并、不部署、不改旧PR、不升级科学状态。
''')
write('QA.md','''# 验证证据

- 26项新增行为/数值测试覆盖任务书A–J：共享祖先、真实端口与原路径逐值相等、独立水焓库存、零通量解析极限、普通异常及不收敛回滚、整组物理边撤销、真实前态延迟、单位/时空/语义门、统计边不能伪装、非有限/缺测、参数不可辨识、完整/选择性一致、无收益反例、30层菱形及非法环、条件阈值。
- 本机完整回归765项，764通过、1项Windows symlink权限跳过（最终运行时间见evidence/test-results.json）。首次旧localhost测试8项因WinError10013失败；允许回环后通过。不是新图算法失败；没有把初次失败抹掉。
- 原始结果在evidence/benchmark_final，初版在evidence/benchmark，中间版在evidence/benchmark_before_endpoint_hardening；三批seed相同，但不同源码版本，不能合并为独立科学样本；前两批为历史记录，当前HEAD直接复现最终批。
- RESULT文件与代码hash可按evidence/benchmark_final/summary.json复核。计时不能逐字节复现；每模式数值/审计记录去除seconds后重复hash相同。
- 展示验收见evidence/ui/qa.json；浏览器证据完成前该项不视为通过。
- 原PR152仅本分支models.advance新增可选mapper，不改变默认公式；父分支、旧报告和科学状态保持。没有访问私人旧资产。
- GitHub CI与精确远程HEAD见最终PR回执；本地通过不代替远程通过。
''')
write('NEXT_SESSION.md','''# 下一轮交接

本轮主线已实现并完成120配置×2模式×3重复，保留两轮修复前证据。不要重新把任务变成家谱动图，也不要重跑旧10008批作为新研究。

先读取PR精确HEAD评审、RESULTS、COUNTEREXAMPLES、SOURCE_REUSE和测试。公开数据和物理边界均PENDING，不访问私人v200。若评审发现问题，优先复现实验ID及反例，再最小修正。

下一轮可提出但未自动授权：以真实观测校验某个已声明过程；显式单位适配器；可证明安全的跨网格聚合；多源误差传播。当前不自动进入这些新实验，不合并、不部署。

Conversation Radar：知识=共享依赖可去重而物理账不能拆；想法=查询驱动的有限因子组织；决定=固定父PR152、保留全部失败；风险=速度提升微弱/模型适用性未知；开放问题=现实验证与扩域门；下一步=ChatGPT审查；关键词=ClimateOS/CCZPS/typed graph/ModelPort/conservation/provenance。
''')
write('CRP_HANDOFF.md','''# Codex → ChatGPT → Founder 科学评审包

请按PR最终精确HEAD读取本包；本文件不是科学接受证明。

重点复核：
1. 是否真的用ModelPort驱动原空气与地表核，并在固定旧库存上迭代？mapper默认路径是否保持PR152行为？是否可能让新增物理因子借用别的因子账本？
2. 被撤销/缺少的物理账是否阻断整组？异常时状态及clock是否真正恢复？
3. 图边源/目标语义、单位、时空、lag、证据是否全部检查？统计节点能否伪装成物理强迫？
4. 共享驱动/菱形汇合是否发生重复贡献？trace是否夸大因果或枚举指数路径？
5. 120配置、720调用、50有效/70故障及三批历史是否清楚？选择性更慢的13例是否完整保留？
6. 水热公式边界、单元差异、慢域证据和合成阈值是否仍正确标识？
7. 桌面/手机展示是否忠实回放JSON，是否误说浏览器中正在实时求解？

请给出ACCEPT_WITH_CONDITIONS / CHANGES_REQUESTED / REJECT，绑定HEAD、路径、实验ID与最低修正。公共代码和数据可复算；全部结果限合成沙盒，不含私人代码或现场排放实验。科学PENDING；不合并不部署。
''')
print('REPORT_DOCUMENTS_GENERATED')
# Deterministic offline HTML uses only the archived public run receipts.
data={'results':r,'scenarios':s,'trace':t}
template=(TASK/'scripts/slides.template.html').read_text(encoding='utf-8-sig')
(TASK/'slides.html').write_text(template.replace('__DATA__',json.dumps(data,ensure_ascii=False).replace('</','<\\/')),encoding='utf-8')
