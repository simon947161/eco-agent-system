# P4 执行授权归档

评估日期：2026-11-24（Australia/Sydney）｜`READ_ONLY`｜`NO_RAW_DATA_DOWNLOADED`

唯一权威：[Issue #164](https://github.com/simon947161/eco-agent-system/issues/164)。以下为本轮读取的任务书正文，非扩权文件；GitHub 后续变更须再次读取。P0–P3 冻结，所有工作仅在本 p4 子目录增量交付。

# CLIMATEOS–AWT–001 / P4 — 真实数据候选包与许可只读尽调（Founder Approved）
**批准日期：2026-11-24（Australia/Sydney）**
**Owner：Codex（调查/整理）；Reviewer：ChatGPT（独立复核）；Authority：Founder**
**Parent Issue：#162｜Parent Draft PR：#163｜固定审阅基线 HEAD：`9aea387a4261b913163b3be3197597089d9e9414`**
**本任务许可范围：READ-ONLY DISCOVERY / LICENCE DUE DILIGENCE / METADATA REVIEW ONLY。**
**初始状态：APPROVED_FOR_P4_DISCOVERY；真实数据准入 DATA_NOT_READY；科学 PENDING；信用 NOT_DETERMINED。**

## 0. 不可逾越的限制
1. 不合并 PR #163，不改 main，不部署、不申报ACCUs、不提交官方咨询意见；不启动真实数据在CarbonOS、PR144/145、AWT引擎或EcoEngine中的正式接入、不运行真实排放估算。合成P0–P3代码及测试逻辑保留冻结。
2. 不接触Council/私人/受保护/付费/个人数据，不要求密钥或账户，不绕过403/429/登录/CAPTCHA/robots/访问控制；不可用镜像或第三方复制规避来源限制。发现访问/授权不明时STOP并登记。
3. 此阶段**原则上不下载真实原始数据包**。允许访问公开页面、元数据、许可文本、公开目录/API文档、示例字段介绍并记录证据；即使发现可合法下载的候选包，也**仅登记原始URL、预期文件、大小、许可、版本、访问条件和下载前核验方案**。数据包的获取、保存、哈希计算及解析须后续单独授权。可存自己编制的文字元数据与小型JSON索引，不复制第三方受限文本。
4. 不扩增384次合成计算、不创建新数据库、平台、Agent或长期监控任务；不做科学保证或法律正式意见。不自动标记 PASSED/ELIGIBLE。

## 1. 研究问题及最小足够证据
目标不是“找到一份甲烷CSV”而是明确：是否存在**一条有合法许可、可追溯来源、可表达同一物料/设施/时间支持**的真实数据链，能够在未来被独立检验基线与项目及残渣的排放。调查仅评估可行性，不推算减排。
- 设施/废物流：物料湿质量、组成或DOC、批次归属、设施工艺、区域、测量期；
- 甲烷：产生量与捕集量/设施气量、组分、燃烧或提纯销毁、管漏/逸散、覆盖氧化；区分**实测**、模型/库存估算和厂商声明，严禁把浓度当排放质量流量；
- AD及残渣：投入/产气、消化残渣湿重及碳、去向、后续CH4/N2O；
- 能量和附带排放：进口电、燃料、运输、发电外供、各自边界与双重计算风险；
- 反事实：无项目时实际废物流向/法规约束、项目注册与crediting period，证据质量是否足以支持可比性；
- 时间：原始时间戳、时区/夏令时、间隔、时钟同步、缺失值、QC与校准、监测边界；严禁将单日浓度强推为100年积分；
- 法规/方法：ARRC2026为咨询而非生效法；AWT2015已到期仅限其新注册路径；NSW FOGO是有适用对象/豁免的收集义务，不等于AD工艺义务或额外性证明；GWP研究因子不等于法定因子。

## 2. Codex 工作步骤（有界）
**P4.0 冻结基线：**读取#162、PR#163准确HEAD、科学评审 review #6029057378、P0–P3的 `REVIEW_REQUEST.md`、`sources.json`、`EXISTING_ASSETS_AND_GAPS.md`、`NEXT_SESSION.md`及PR144/145复用位置；登记现有科学闸门，禁止改它们。

**P4.1 候选发现（总量最多6、深入最多3）：**优先官方/原始发布者目录，允许地域优先 Australia/NSW，其次可信的开放国际基准。探查公开监管环境数据、废物设施监测数据、公开科研数据仓库（如政府官方目录及论文附件公开仓库）。逐候选注明是否同设施同时间同批次；跨设施拼接的数据只可作方法验证，不能冒充真实反事实。每个候选登记来源、持有方、最后更新日、数据粒度、格式、可用字段、预计许可证和缺口。**不要求必须找到满足全链的数据。**

**P4.2 权利及访问审计：**逐候选查明确许可原文链接/授权方、再分发与衍生用途、署名、非商业限制、API ToS、隐私/商业敏感性、地理敏感性与数据保留条件；仅“publicly viewable”不等于“open licensed”。许可不明标记 `LICENCE_UNVERIFIED`，不进入准入候选。

**P4.3 可比较性审计：**以PR#163的1000t cohort及9类passport为参考定义字段映射（**只做字段映射，不导入数据**）。每项标记 `DIRECT_MEASURED / CALCULATED / REPORTED / MISSING / UNKNOWN`、单位与时间支持、设备/QC及出现场址关联。特别列出残渣路径、基线合法性、对应年份GWP/电网因子和重复信用权益风险；不可用假设0弥补空缺。

**P4.4 排序与停止：**每候选通过独立闸门：G1合法许可；G2可真实获取而无需越权；G3来源/版本/时间/单位可追溯；G4同设施/时期物料链的可比性；G5残渣和能量边界；G6校准/QC；G7方法和基线可能性。给出 `CANDIDATE_FOR_FOUNDER_APPROVAL`、`PARTIAL_METHOD_ONLY`、`BLOCKED` 或 `NO_SUITABLE_DATASET`，绝不输出 `SCIENTIFICALLY_ADMITTED`。若所有候选都缺许可或缺关键时间/残渣，坦诚STOP，交缺口报告，不得无限搜寻。

## 3. 交付物（文档为主；勿新增运行基础设施）
请在基于PR#163固定HEAD新建隔离工作分支 `codex/climateos-awt-001-p4-discovery-20261124`；不得直接推送main或修改既有PR#163审阅对象；用**独立Draft PR**交付，与#163关联，禁止自动合并。
在 `docs/tasks/climateos_awt_001/p4/` 生成：
1. `P4_READONLY_TASKBOOK.md` — 本批准边界及不可执行项（可引用本Issue作为权威任务书）。
2. `CANDIDATE_DATASET_REGISTER.md` + `candidate_register.json` — 最多6个发现、深入3个，source URLs、owner、版本、发布日期、时间/格式/字段、许可证据、访问状态、风险和适用等级。
3. `LICENCE_AND_PROVENANCE_AUDIT.md` — 每候选许可文字准确链接、允许/禁止/未知、是否可以下载及再分发（只是审计，非实际下载）。
4. `FIELD_TIME_QC_MAPPING.md` — 9类护照与物料/CH4/残渣/能耗/气象时序等字段证据等级，missingness、时区、间隔、QC、校准，分清排放量与浓度。
5. `BASELINE_LEGAL_RIGHTS_GAPS.md` — AWT、FOGO、历史/新方法、反事实与权益交叉的**需核查事项**，非法律结论。
6. `FOUNDER_P4_DECISION_CN.md` — 中文≤12页等价结构：最好候选为何优先、为何仍不能正式准入、红旗、下一步需Founder单独批准哪些具体数据URL和下载/核验范围。
7. `CRP_HANDOFF.md` + `NEXT_SESSION.md` — 核心知识/想法/愿望/推理/决策/问题/下一步/项目索引。

每份报告必须注明准确评估日期、独立可点击原始链接、`READ_ONLY`、`NO_RAW_DATA_DOWNLOADED`，缺证据要保留 `null/UNKNOWN`。如确实进行了浏览器查看，仅声明浏览器查看，不冒充已核验原始文件字节。

## 4. 验收与回执
- 检查候选数量上限、每个主张有来源、许可证可回溯、格式JSON语法和相互链接；不要求无谓的大量测试，但凡新增检查必须有真实运行记录。
- 不可将“找到公开页面”写成“获得合法可下载数据包”，不得把候选元数据当现场数据；不允许任何真实减排计算结果、信用量或科学准入升级。
- Draft PR描述、Commit SHA、变更文件清单、证据链接、许可疑点、停止原因和Founder待审批项逐项回报；须证明未触发部署、未改既有科学状态。
- 若无合格候选，输出 `NO_SUITABLE_DATASET` 并结束，而不是扩大范围。
- 这次Founder审批**仅覆盖P4发现和尽调**；后续下载、保存、哈希核验、解析、模型接入、专业第三方评审、部署、合并、正式申报或对外代表Founder发文均须新的明确审批。

## 5. Founder handoff / CRP
知识点：可计算不等于可核证；许可、时间支持、实测/推算分层决定证据可信度。
想法：用已有PR145证据接口做未来准入计划，而非新平台。
愿望：逐步达到可核查减排证据链。
推理：许可→来源→时间/物料可比→QC→独立评审→可能的科学准入。
决策：只读候选调查已批准；后续所有写入/接入/申报未批。
未解决：是否有同边界真实数据链；残渣/反事实和权益证据。
下一步：Codex交隔离Draft PR和候选审计；ChatGPT评审；Founder选择一个明确候选及单独许可行动。
索引：ClimateOS / AWT / Methane / CarbonOS / EcoChain / PR144 / PR145 / PR163 / D3.
