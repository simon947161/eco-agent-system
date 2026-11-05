# 成熟科学与ClimateOS专业智能体：连接复核

2026-11-05 · CLIMATEOS-DYNAMIC-QUANT-001 · Founder复核修订

## 一、纠正首版的方向

首版说明了软件边界，但回查历史耦合研究不足，并将平台问题缩成数据库迁移。“本轮未运行”不能推出“科学界没有可用方法”；D3缺甲烷数据也不能阻断其他过程的集成研究。

本次有界复核确认：建筑通风、区域气象与地表过程、城市微气候、大气输送各有现成方法。ClimateOS应组织方法选择、资料准备、计算调用、验证和解释。以下是代表性技术，不声称穷尽全部软件或将研究候选视为同等成熟。

## 二、继承已完成的历史工作

下表原文件已重新阅读，均在首版使用的main基线可追溯；路径为仓库相对路径。

|已有工作/文件|实际积累|进入专业智能体的方式|
|---|---|---|
|docs/tasks/task1200_1499_model_assurance_hybrid_weather/TASK1200_1499_MODEL_ASSURANCE_AND_HYBRID_WEATHER_ROADMAP.md|身份、统计误差、物理一致性、极端与区域适用性框架|方法选择和评价清单；路线图不等于所有评价器已实现|
|docs/tasks/task1500_1700_environmental_coupling_layer/TASK1500_1700_UNICM_ENVIRONMENTAL_COUPLING_LAYER_ROADMAP.md|全球气候→区域天气→水文土壤→植被生态→治理|恢复为完整科学路线，不被本轮三日统计缩小|
|docs/tasks/task1541_1550_external_model_observation_foundation/UNICM_NEURALGCM_MULTISCALE_COMPARISON_REPORT.md及同目录研究包|气候模态关系与演化大气场的对照|宏观背景与并行评价；月尺度/全球网格不能直接成为街区边界|
|cczps_lite/integration/environmental_coupling.py及关系schema|已有静态图验证；区分相关、滞后、模型推断、因果假设|复用关系语义，不往合成合同填论文冒充真实输出|
|cczps_lite/integration/mechanism_return_gate.py|基准、扰动、对照、敏感性、版本、边界、计算上限字段|方法复现的设计基础；本轮不修改no-run合同以暗中执行|
|Task1700闭合、Task1701–2099机制/科学智能体研究|专业研究方向、实验与证据缺口|把缺口对应到具体方法/输入/验证，不无限增加泛化治理文件|
|QGIS terrain/hydrology/integrated packs与气象connector|地形、几何、来源、变量接口|准备模型输入；高度、日界、代表性仍须核实|

## 三、成熟方法怎样支持风、热与气体？

|问题|现有技术和原始依据|输入→输出|ClimateOS连接职责|
|---|---|---|---|
|建筑通风与热负荷|EnergyPlus AirflowNetwork [S1]；BASIX/NatHERS [S2]为住宅评价路径|建筑/开口/材料/风压/天气→多区气流、压力及热湿结果|输入核查与报告；不将EnergyPlus等同NatHERS认可软件|
|区域风、温度与土地反馈|WRF地表/城市冠层 [S3]|大气初始/侧边界、地形、土地参数→区域大气/地表场|选择现有配置与网格，不发明新动力学|
|开放街区风与热|PALM 6.0 [S4]及实地验证 [S5]|建筑/植被/地表/土壤、大气边界→局地流动、热和辐射诊断|先复现参考案例与误差，再决定地方应用|
|气体输送与浓度|NOAA HYSPLIT [S6]|三维气象、释放/背景、物质设置→轨迹或浓度|组织现成格式和验证；轨迹不是源强，输送不是增温|
|宏观天气/气候背景|既有UniCM/NeuralGCM研究；NeuralGCM论文 [S7]|模型指定状态/边界→适用尺度场/指标|保留多模型比较，不默认checkpoint支持CH4强迫响应|
|温室气体长期作用|IPCC AR6 WGI第7章 [S8]|情景和合适气候方法→强迫/响应指标|独立于局地输送；本轮没有运行该类模型|

S1明确包含风驱动多区气流。成熟软件并非普遍必须无风；风需要动力学、湍流和边界条件的相应处理，也不能简单认定只会降温。建筑网络、区域气象和局地LES针对不同对象，不能直接替代。

## 四、真实案例说明了什么？

Resler等（2021）在布拉格Dejvice，以现场气象、空气质量、表面温度和墙体热通量评价PALM，局地模拟受中尺度边界驱动。这支持开放城市风与热等过程有现成框架。论文也报告地形离散、复杂立面与玻璃辐射表示的限制。[S5]

这是作者案例验证，不是ClimateOS已复现，也不自动适用NSW或甲烷。下一科学台阶应是选一个此类公开案例，核查版本、输入、许可及独立观测，形成复现配置和误差评价。材料与预算成立后再执行，不能用合成资料替代实地验证。

## 五、连接模型，不重复发明科学

以“植树与铺装改变后，在给定夏季风况下，人行空间热环境怎样改变”为例，应先选内部已经包含所需辐射、地表、水分与流动过程的模型。ClimateOS准备输入、组织计算、检验和解释。

跨尺度先考虑单向驱动：区域场→局地边界→局地结果→评价。检查网格、垂直坐标、风向约定、高度、时窗、旋转坐标、单位和守恒。插值不能把粗网格变成观测到的街区细节。双向耦合需具体模型支持和反馈/稳定性验证，不能承诺任意模型即插即用。

气体走释放/浓度→输送/化学→观测比较；长期气候影响另走强迫/响应。它们可以在一个智能体内协作，不必成为一个未经验证的求解器。生态/水文共享土地、天气与管理情景，指标及验证仍独立。D3关闭的是本轮反演入口，不是其他成熟方法的研究。

## 六、专业训练落实为五种能力

1. 知识记忆：论文、官方方法、历史ClimateOS研究与版本，同时找支持和反证。
2. 方法记忆：问题→尺度→方法规则、输入清单、常见错误和替代办法，不只堆PDF。
3. 执行能力：获准GIS、QA、模型作业、诊断和报告，保留日志、失败与成本。
4. 经验记忆：案例配置、误差、专家修改和失败原因，区分已接受经验与待验证推断。
5. 专业考核：已发表案例、尺度错配题、统计/守恒评价与专家复核，决定允许承担哪些问题。

这是设计建议，未称已上线，也不等于必须先微调基础模型。检索、工作程序、工具和评价可以先形成专业化；参数训练需要另有数据、许可与收益证据。专家反馈应改善能力，不只在最后签字。

## 七、MOI作为智能体平台候选

Founder本轮说明与“探索 Matrix 智能体”聊天确认，关注的是MOI工作空间。本报告不公开其他聊天、账户或上传内容。

官方资料确认AI Studio组织知识、技能、工具和智能体，并有托管/自托管运行环境说明。[P1–P3] 因此应评价它能否承载定制智能体，不能只问三天JSON是否需要数据库。

建议平台负责用户工作区、任务与可用资源管理；ClimateOS保留方法、科学合同、案例和来源；模型在适合资源运行。问题、地图/输入、作业、结果/证据可作为未来工作视图，但属于体验验收目标，不声称现有MOI布局已经满足。

愿意支付平台和中国算力成本是设计前提，不等于已经批准下单。区分大模型推理资源与科学计算CPU/内存/并行资源。运行环境说明不能证明任意中国GPU或集群可直接运行WRF/PALM；地区、架构、MPI/容器、长作业、持久盘、网络、恢复与成本须按具体方案核实。可以评估托管或外部科学worker，连接也需实测。

评价标准应是方法执行、可观测性、经验恢复、权限、导出、科学资源兼容、界面与付费成本。收费本身不是否决项。官方有Credit与实例等不同计费边界 [P4]；本轮没有报价、充值、账号操作或benchmark。

## 八、向前推进的台阶

将下一专业化目标提升为“智能体组织一个已发表的风与热案例”：检索既有研究→解释方法选择→准备输入与预算→调用获准模型→比较独立观测→解释误差。三日描述统计保留为基础，不当作最终目标。

本次完成的是文献与平台连接复核，没有执行这些模型。后续应以可取得的数据、固定版本、计算配置、指标、人员和成本为材料，以案例结果扩展知识与工具；不一次安装所有软件，也不等待所有科学问题解决才开始。

## 来源与核查状态（2026-11-05）

- S1：[EnergyPlus v26.2 AirflowNetwork](https://energyplus.readthedocs.io/en/v26.2.0/guides/input-output-reference/1.27-group-airflow-network.html)，正文已读，风驱动和边界。
- S2：[NSW BASIX Thermal Performance](https://www.planningportal.nsw.gov.au/basix-thermal-performance-section)，2026-10-19页面，住宅路径。
- S3：[WRF官方Physics](https://www2.mmm.ucar.edu/wrf/site/documentation/users_guide/physics.html)，正文已读，执行仍须固定配置版本。
- S4：[Maronga等2020 PALM 6.0](https://doi.org/10.5194/gmd-13-1335-2020)，原始模型论文正文。
- S5：[Resler等2021 Dejvice验证](https://doi.org/10.5194/gmd-14-4797-2021)，原始验证论文正文，案例不是普适保证。
- S6：[NOAA HYSPLIT教程](https://www.ready.noaa.gov/documents/Tutorial/html/index.html)，2023修订/教程5.3.0，正文已读；get/run另页403，未绕过、未下载数据或执行。
- S7：[Kochkov等2024 NeuralGCM](https://doi.org/10.1038/s41586-024-07744-y)，论文摘要和既有研究包；无新增checkpoint或运行准入。
- S8：[IPCC AR6 WGI第7章](https://www.ipcc.ch/report/ar6/wg1/chapter/chapter-7/)，官方检索确认主题，直接请求403；仅方法分类，不抄公式/数值。
- P1：[MOI 5.0 AI Studio](https://docs.matrixorigin.cn/moi/en/5.0/introduction/ai-studio.html)、[Agents](https://docs.matrixorigin.cn/moi/en/5.0/guides/ai-studio/agents/index.html)，正文已读；官方能力声明，非账号实测。
- P2：[托管运行环境](https://docs.matrixorigin.cn/moi/en/5.0/guides/ai-studio/agents/runtime-environments/managed.html)，2026-09-15正文。
- P3：[自托管运行环境](https://docs.matrixorigin.cn/moi/en/5.0/guides/ai-studio/agents/runtime-environments/self-hosted.html)，2026-09-15正文；未执行连接命令。
- P4：[MOI计费](https://docs.matrixorigin.cn/moi/en/5.0/guides/billing/index.html)，官方检索正文，直接打开cache miss；不推断具体价格/额度。

官方能力、已发表验证、仓库实现与仓库验证分开。没有新增数据下载件；网页按URL/DOI/版本/核查日追溯，不虚填文件SHA。
