# CLIMATEOS-AU-LANDFILL-METHANE-METHODS-001
## 唯一总任务书｜澳大利亚填埋场甲烷官方方法精读、可追溯知识库、生成—收集—氧化—实际排放物料账
日期：2026-11-09 Australia/Sydney
Founder目的：科学、气候治理和长期个人学习；不以商业门户、营销或通用Client AI为本轮主线。
仓库：simon947161/eco-agent-system
工作分支：research/climateos-au-landfill-methane-methods-001
冻结父提交：PR #143 HEAD 746825e65b8ddbd0f518709c94d9476df107208b
本任务为 FOUNDER_AUTHORISED_BOUNDED_RESEARCH_AND_METHOD_KNOWLEDGE_BUILD；允许有界的官方文献检索、合法下载/校验、方法提取、离线公式/质量账解析验证和知识库整理；不批准真实设施排放推断、法定报告、碳信用申报、私有Council数据、外部联系、付费、部署、合并、改动旧PR科学状态或大型数值模拟。
任务文件是本轮唯一授权。先核对远程 HEAD、旧 PR #138–143 的状态与相关代码；有漂移先记录，不覆盖。

## 0. 首先回答的问题
澳大利亚填埋场的甲烷究竟怎样产生、在垃圾/气孔/覆盖层中怎样储存和迁移、怎样被收集/燃烧/利用、怎样被氧化/泄漏，最后多少真正进入大气？澳大利亚国家温室气体报告、碳减排方法和 NSW 环境工程指导分别要求如何测量和核算？这些既有公式与 PR143 的 P1–P4 和 E01–E14 如何正确连接？哪些是通用物理规律、哪些是澳大利亚特定监管计算规则、哪些是场址参数、哪些尚不能计算？
所有结论区分“官方文件原文”“研究者推导”“软件验证”“现场验证”“法定适用”；不能把法规核算值等同于实际瞬时排放，也不能把项目信用基线当作物理实测真值。

## 1. 权威来源：逐份读取和冻结版本
优先研究以下候选官方原始资料（URL是待核验的线索，不预设当前有效性）：
A. 澳大利亚清洁能源监管机构 CER：Estimating emissions and energy from solid waste and landfill biogas management guideline
https://cer.gov.au/document_page/estimating-emissions-and-energy-solid-waste-and-landfill-biogas-management-guideline
B. CER：Reducing methane emissions from landfill gas 2025 method，及正式法定method determination、explanatory statement、tools/calculators、reporting/monitoring requirements
https://cer.gov.au/schemes/australian-carbon-credit-unit-scheme/accu-scheme-methods/reducing-methane-emissions-landfill-gas-2025-method
C. Federal Register of Legislation：National Greenhouse and Energy Reporting (Measurement) Determination 2008 的现行汇编和2026相关修订、说明书
https://www.legislation.gov.au/F2008L02309/latest/details
D. NSW EPA：Environmental Guidelines: Solid Waste Landfills（2016版候选，检查后续更新/法律适用）
https://www.epa.nsw.gov.au/sites/default/files/solid-waste-landfill-guidelines-160259.pdf
E. NSW EPA：Food organics and garden organics / Emissions impacts of food waste recovery technologies
https://www.epa.nsw.gov.au/Your-environment/Recycling-and-reuse/business-government-recycling/Food-organics-and-garden-organics/Emissions-impacts-of-food-waste-recovery-technologies
F. NSW EPA：适用有机物处理/堆肥环境指南与地表甲烷调查指导；以官方站内检索确定精确URL/年份，不凭先前聊天推断。
G. IPCC 2006 Guidelines Vol5 Ch3 Solid Waste Disposal + 2019 Refinement 相应章节，用于与澳大利亚法定方法比较（不混用年份默认值）。
H. 相关澳大利亚农业/污水/厌氧消化官方方法仅建 FUTURE_SCOPE 索引，不进行本轮完整计算开发。
对每份核实：官方出版者、正式文件标题、编号、版本/生效日、修订/替代关系、适用活动、具体条款、是否现行、法规/指南/研究报告的法律层级。尤其核实2026 NGER现场测量条款、适用对象、方法与门槛，2025 ACCU装置破坏效率及监测频率；先前对话中“98%”“逐分钟”“25m/5cm/500ppmv”“堆肥减排96%”均仅为待核查线索，不得在核对精确条款前当事实写入。
可公开合法下载的完整原件，按版权和许可决定：许可允许仓库存放才提交原文件；否则只提交链接、SHA/大小/获取日/版本/章节定位、自己的释义和极短必要引文，不将整份版权PDF推送Git。大文件使用本地不入库缓存并记录可复现获取说明。不可获取的来源标 BLOCKED，不绕过403或付费墙。
逐份生成 SOURCE_RECEIPT、SECTION_MAP、EQUATION_EXTRACT、METHOD_LIMITATIONS；具体页码、条款、原文变量名和单位、公式编号及表格版本。保留来源的定义和边界，不用AI自己的猜测替换原文。

## 2. 方法比较：监管、工程与物理三条不同路线
建立 NGER / ACCU 2025 / NSW EPA / IPCC 的逐项对照：
- 目的：全国温室气体报告、减排项目核证、现场环境管理、国际库存估算；
- 适用对象/阈值/设施/报告年、默认因子与允许替代、版本生效/过渡；
- 方法：废物历史与可降解有机碳（DOC/DDOC）、一阶降解FOD、甲烷生成、回收/火炬/发电、破坏效率、覆盖层氧化、逸散/气体迁移、库存变化、现场监测、模型校准、缺测处理；
- 监测：填埋气流量及其状态基准、CH4体积分数（干/湿）、压力、温度、水汽、气井、管网、火炬/发动机状态、表面扫描、通量箱、代表性分区、频率、QA/QC、仪器校准、独立审计；
- 单位：tCO2-e vs kgCH4, Nm3 vs m3, dry/wet, mg/m3 vs ppm, mass flux vs concentration, oxidation vs destruction, biogenic CO2 vs fossil emissions；
- 计算产物与不确定性、可比性、法律适用边界。
必须核实“排放量”在各方法中的定义：gross generation、collected、destroyed、vented、oxidized、net emitted、credited abatement，不得把它们相互替代。
列出至少三个可直接追踪到原文条款的完整 worked example；如果原文没有实例，明确标记 AUTHOR_DERIVED_SYNTHETIC_EXAMPLE，不能冒充监管实例。

## 3. 建立真实物理过程与闭合质量账（重点）
从系统边界而不是单一排放公式出发：
- 废物中可降解碳库→甲烷生成（按碳/CH4质量、时间）；
- 气相/溶解态/孔隙储存、进出边界、气体组成、捕集、火炬/能源利用、未燃烧/旁路/设备泄漏、覆盖层氧化、表面逸散、横向迁移；
- 可选不同边界：整个填埋体、集气管网、燃烧设备、地表覆盖层。边界间流量必须匹配，避免捕集/破坏/氧化重复扣减；
- 总量守恒：期初库存+期间生成+流入=期末库存+向大气排放+燃烧/氧化反应消耗+流出+其他经证实去向。若跨CH4→CO2反应，分别核算甲烷质量与碳元素守恒；不要要求甲烷分子燃烧后仍为甲烷。
- 逐项区分源率、观测浓度、测量通量、模型估计值、核证信用值。
- 审查 PR143 E06/E07 的原文边界：年度FOD索引、可降解碳定义、16/12碳→CH4换算、R/氧化/OX、燃烧DRE与设备漏排的关系；核查E07扩展公式是否重复计数或不适用于特定监管法。
- P1用于实测流量/甲烷比例/压力/温度/水汽的**有条件质量换算**，不从环境浓度直接推源强；P2纯CH4容器不能无组成/体积/时间桥接到稀薄混合气；P3/P4只可在已审查假设与场址参数内复用。
- 最少设计三种明确边界的合成场景：未捕集、捕集+火炬、覆盖层氧化/泄漏；对每个场景做双重守恒/单位/时间测试，区分设备破坏率与全场收集率。
优先先做方法契约、解析核验和小型离线合成质量账；不得新建大型模拟器或真实排放模型。若缺证据不能闭合，保留 BLOCKED 并给出最小缺口，不能硬接。

## 4. 现场测量如何约束模型
单独研究 surface screening vs flux chamber vs gas collection flow meter vs tracer/remote sensing（若官方方法提及）；分别能测什么、不能测什么、代表什么空间时间尺度。地表500ppmv热点浓度不能直接等于kg/h排放。
为未来真实公开场址设计最小输入清单：废物分年度量与组成、场址边界与覆盖类型、填埋龄、甲烷比例、气体流量/状态基准、捕集设备、氧化参数、地表通量、监测时段、仪器校准和许可。
建立现场观测→参数估计→模型预测→独立验证/残差→情景比较的流程；清楚区分校准样本与留出验证样本。先调查最多两个合法开放案例，不得用Council私人数据、不得推断实际场址排放；找不到则 DATA_NOT_READY，不无限搜索。

## 5. 长期知识库：Enotebook / ClimateOS Method Library
这是必须完成的正式交付，不是报告附件。优先复用仓库已有知识库、CSP/Enotebook/知识蒸馏结构；先审计目录与schema，禁止平行再造一个竞争系统。
每份来源建立：
SOURCE_MASTER（完整原件链接/许可/版本/哈希/章节目录/原文保存位置）
KNOWLEDGE_CORE（关键定义、物理机制、公式、变量表、方法前提、重要表格、图解、限制）
SKILL_PROCEDURE（如何计算、如何测量、怎样查错、逐步实例）
CASE_EVIDENCE（官方实例、数据和现场案例、证据等级）
CONNECTIONS（与P1–P4/E01–E14/CCZPS、气象、QGIS、未来堆肥/农业/污水的映射）
LEARNING_PATH_ZH（Founder逐章学习顺序、每章核心问题、3–5个练习及参考答案、复习书签）
UPDATE_LEDGER（版本变化、个人新理解、未来案例/实践补充的可追加记录）。
保留完整上下文和来源定位；不能只做摘要。版权不允许存储原件时，使用可追溯外部源与自有结构化学习笔记；不得把版权文件大段复制进Git。记录权利及版本，不擅自宣布全文已阅读。
要求输出一本「澳大利亚填埋场甲烷工程与核算」中文可连续学习的索引册，适合Founder逐章理解和后续AI检索；与ClimateOS项目索引互相链接。不得覆盖用户已有Enotebook条目或学习进度。

## 6. 工程范围、检验和成本约束
在 PR143 后新增一个有界任务目录和必要的小型解析/守恒代码与测试；旧科学核心和PR138–143保持不变。重点是“官方原文→可执行公式→质量账→人类可读解释”可追溯，**不是**开发门户、全自动LLM代理或大规模模型。
所有合成数值标 SYNTHETIC_METHOD_TEST，不给真实填埋场排放量、法定NGER报告或ACCU信用数量。对公式给出独立手算与至少一种边界/反例测试。测试：年度/小时错位、tC→tCH4、m3/Nm3、干湿体积、捕集/燃烧/氧化双扣、燃烧后CH4与CO2守恒区别、负/缺失/不确定参数、漏排、监测覆盖、监管版本错用、无来源/许可/校准、图谱断链、错误气体/相态。失败拒绝，不补默认0。
最多重点精读8个官方主来源主题、最多两个公开案例候选；若某法定文件有多个必须配套附件可以增加登记但必须说明，不无限扩展。
真实执行的测试、原件字节SHA、引用定位、源码差异和远程CI逐项归档；如无真实数据不得升级科学准入。保持D3 DATA_NOT_READY、P1-A PENDING、PR140 NO_VALID_PAIR、PR141 NO_VALID_VERTICAL_PROFILE、PR143 ChainB BLOCKED及Stage3 METHOD_READY_NOT_VALIDATED。报告要把“真实研究完成”和“未来实施建议”分开。

## 7. GitHub交接与验收
沿用 PR142/143 R研究内容、D交接元数据、精确HEAD最终评论。新建独立 Draft PR，父基线PR143 HEAD，提交前后核对本地/远程/PR HEAD一致。ChatGPT仅在Founder发出短句后通过GitHub只读评审，不声称自动收到；评审完成后再由Codex按Founder授权归档回执。
ChatGPT评审重点：官方文件版本与条款真实、NGER/ACCU/NSW EPA/IPCC区别、公式与单位、甲烷/碳守恒、测量与源强、来源许可、知识库是否真可持续学习、合成代码和测试、未批准结论是否被阻止。
不合并、不部署、不联系第三方、不读取任何Council非公开文件、客户信息或采购资料。

## 8. 必交成果
目录 docs/tasks/climateos_au_landfill_methane_methods_001/：
README.md；FOUNDER_REPORT_ZH.md；SOURCE_REGISTER.md；REGULATORY_VERSION_MATRIX.md；SECTION_AND_EQUATION_CROSSWALK.md；AU_LANDFILL_METHOD_COMPARISON.md；LANDFILL_PHYSICS_AND_MASS_BALANCE.md；MEASUREMENT_AND_MODEL_CALIBRATION.md；PR143_E06_E07_BRIDGE_AUDIT.md；SYNTHETIC_MASS_BALANCE_RESULTS.md；OPEN_DATA_FEASIBILITY.md；METHOD_KNOWLEDGE_INDEX.md；LEARNING_PATH_ZH.md；FUTURE_MODULES_INDEX.md；QA_AND_VALIDATION.md；NEXT_SESSION.md；CRP_HANDOFF.md；REVIEW_REQUEST.json；HANDOFF_STATUS.json；source_receipts/、knowledge/（每份官方来源的结构化知识包）、evidence/（合法文件收据、合成输入/输出、日志、SHA、测试）。
如已有知识库目录可正式接纳这些知识包，则在该目录增加链接/索引并提供真实可用的检索入口；如果当前知识库不可写或不明确，则保留独立包和明确待接入状态，不谎称已入正式知识库。
Founder中文报告必须直白回答：澳大利亚工程师怎么干？哪些数字怎样测？哪个公式算什么？我们现在真正能算什么？还缺什么？下一步该研究哪个环节？先讲因果和工程流程，再把技术细节放附录。
成功标准：每条关键行业计算有官方章节和公式定位；有一个统一物料账的可复核合成示例；能解释测量如何校准生成模型；知识库可查、可学、可追加；未验证部分保持明确阻塞。
