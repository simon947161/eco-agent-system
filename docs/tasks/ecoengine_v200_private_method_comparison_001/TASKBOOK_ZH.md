# ECOENGINE-V200-PRIVATE-METHOD-COMPARISON-001
## Codex独立取证与对照复算执行任务书｜2026-11-11
Founder授权立即开始；链接 GitHub Issue #151。父基线 PR #152 HEAD cf91e4a061341bc33d16400bcf4c6a2c2817aa65。
工作分支 research/ecoengine-v200-private-method-comparison-001。
本任务目标：真实理解Founder私有旧版EcoEngine v200的“跳跃”方法，并与PR152新Earth System Coupling Lab在公平、可复算的条件下进行独立比较。不能预设旧方法创新/更好，不能因新系统有万次测试就预判其更好。结论必须敢于明确否定，亦要坦承不可比较之处。

## 0. 执行环境与私人IP硬边界
- Founder许可：能够真正访问其Windows主机D盘的Codex，对已识别的私有EcoEngine v200旧工程仅做最小必要只读审计和安全隔离实验。可能的目录称为EcoEngine与eco_engine_v200；不得全盘扫描或假定这些名称已验证。
- 旧版源代码、独特公式、文件/函数定位、项目结构、私有数据、凭据、知识包与原始复算证据一律保留在Founder本地主机的私有路径，绝不上传到公开GitHub、Issue评论、云端Codex上下文或未经批准的共享位置。
- 旧资产必须零修改、零覆写。未知脚本先静态审计；只有确认无磁盘写入、联网、隐藏副作用，并能在禁网、隔离、受控权限的本机环境运行时才可以执行。如存在额外历史保密/访问限制与本次授权冲突，停止对应目录并标LOCAL_LEGACY_ACCESS_GATE。不得通过云端猜测本机源码。
- 如果执行器只能访问云端、无法读取本机D盘，必须明确HOST_HANDOFF_REQUIRED，指向主机Codex执行；不得编造旧版审计或借公开repo抽象旧版本成品代替。

## 1. 找到真正的旧方法
优先查看原有说明/版本/核心运行路径/作者原始示例。逐条在本地PRIVATE_EVIDENCE记录原术语、核心输入/输出、时空尺度、状态选择、计算规则、跳跃或更新条件、数学/物理假设、误差处理、边界、停止机制、可执行证据。
需分别判断它是：空间非邻近跨点、少数代表点推断、时空差异场、时间跳步、状态空间跃迁、启发式优化，还是其他机制。这些仅是候选，不是预先定义。
标注 ORIGINAL_SOURCE_PROVEN / INDEPENDENT_RECALCULATED / INTERPRETATION / HYPOTHESIS / CONTRADICTED / NOT_FOUND。无法找到不得捏造“跳跃”。

## 2. 现代基线必须原样重跑
冻结PR152源码和固定输入、独立查看state/models/ports/diagnostics/experiments。
实际对照其共享时空Field、单位/空间重映射、时钟、差分与敏感性、Atmosphere-Surface双向水热通量、守恒、独立/单向/双向、收敛/回滚、不可辨识、合成热旱联合阈值。
保留现实科学限制：仅两类组件发生实际局地双向物理交换；ENSO和CH4为独立季节/全球证据，并未做现实局地动力学耦合。不得把10008合成记录当准确率或外部认证。
验证旧PR143–152不改变，未合并、未部署。

## 3. 公平实验：先判断能否比较
事前固定研究问题、共同输入、空间/时间支撑、参数和计算预算。至少三类：
(A) 双方都能处理的共同案例，同样输入和评价指标（有可信真值才报告准确率）；
(B) 若源码证明确实属于旧方法的稀疏点/非局部或跳跃案例，不得凭Founder说法假设其能力；
(C) 新耦合器的守恒、双向反馈、单位/时间/空间门、数值稳定/回滚。
必须包含缺测、错单位、不可识别、错误尺度、极端/不稳定输入的反证案例；同一任务给双方同等修正机会但不得事后挑成功参数。
若一个是探索/近似/检索算法、另一个是动力学求解器，记录 INCOMPARABLE，分任务比较，不能硬给总体赢家。
先10–30个隔离可复算用例，再依据有效差异决定至多约100–1000个参数与反证实验；单批不超过20分钟/200MB、无付费API、无长期常驻或外联。真实旧算法只可在私有主机隔离运行；公开仓库不复制其机制或私有测试夹具。
对照指标：物理守恒/量纲；相同可信基准下误差；多尺度/稀疏数据/时滞/反馈；不确定性和假因果；计算成本；数值稳定性；可辨识；复现性；集成复杂度；隐私与IP风险。每一项判断 OLD_BETTER / NEW_BETTER / EQUAL / INCOMPARABLE / INSUFFICIENT_EVIDENCE，给明确实测或源码支持；没有真值的不能说预测更准确。
输出必须单列：旧方法优点、旧方法缺点、新方法优点、新方法缺点、两者不能比较之处；Founder直觉被支持/被反驳/仍未知。不要奉承，不要预设“独创”或“科学颠覆”。

## 4. 公共与私有交付严格分离
PRIVATE（仅本机受保护目录、不加入Git）：旧项目和函数真实定位、详细推导、运行日志、原始输入输出、指标逐项复算、哈希、完整私有Founder审查说明。禁止外传、上传、通过Issue贴源码或脱敏不足的参数。
PUBLIC（本分支GitHub）：
docs/tasks/ecoengine_v200_private_method_comparison_001/TASKBOOK_ZH.md；
FOUNDER_REPORT_PUBLIC_ZH.md（只给安全、非可逆推出算法的结果）；
COMPARISON_PROTOCOL_PUBLIC.md；
RESULTS_AGGREGATED_PUBLIC.json；
COUNTEREVIDENCE_PUBLIC.md；
PR152_COMPATIBILITY_PUBLIC.md；
QA_AND_VALIDATION_PUBLIC.md；
NEXT_SESSION.md；
CRP_HANDOFF.md；
REVIEW_REQUEST.json；
HANDOFF_STATUS.json。
可添加不含旧机密的通用实验驱动和新耦合器侧测试。Git提交前检查是否泄露旧源码片段、可复刻专有算法的数学规则/系数、完整私有路径、账户密钥、可推断私有方法的fixture；不安全即保留PRIVATE_ONLY并在公开报告写受控证据保留，不以Git公开所有材料为验收前提。
只有经Founder明确允许披露的结果可在GitHub展示；若真实比较的汇总也涉及专有细节，写PRIVATE_EVIDENCE_WITHHELD，Founder在私有本地查看。公开ChatGPT独立评审只能核新耦合器与公共结果，不能声称独立复跑未公开的旧版算法。
创建本分支独立stacked Draft PR，base为PR152分支，核精确HEAD、真正CI/测试、旧PR不变。交接到Issue#151并明确PRIVATE_NOT_EXPORTED，待Founder/ChatGPT审阅。未获额外授权不能移植旧算法到公开代码。
禁止合并、部署、扩大实验或自动收编旧方法。

## 5. 验收重点
不能只有论文和架构图；要有真实旧版只读证据和本地可复算对照，或如实报告访问阻塞/代码不可执行而暂停该维度。必须给出可区分任务条件的明确利弊，指出最有信息增益的下一轮对照；如果旧方法没用或明显不可靠，直接说明依据。如果旧方法有长处，也明确何种范围可以借鉴、何种范围不能物理认证。
本轮不是建立新的单变量任务，不是无限增加测试次数，而是为ClimateOS发展寻找原理正确、可证伪、对真实地球系统有用的计算机制。用户保留全部旧版知识产权及未来是否许可集成的决定权。
