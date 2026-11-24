# ClimateOS · WHH 科学准备验收

2026-11-24 · 12屏 · READ_ONLY · 原始数据未下载 · 独立科学审查待进行

## 01｜研究包已交付，传播与健康结论仍未成立

本轮完成AWT状态归档及WHH P0–P1有界调查。最重要的发现是：COO300相对排放口的官方年报描述矛盾；当前不能把它当成已确认的上游或下游对照点。

**SCIENCE=PENDING · REAL_DATA=DATA_NOT_READY · 计算NO-GO。** 我们有一条可审查的研究路径，没有设施责任或人体健康结论。

来源：[拓扑证据与冲突](WHH_P0_TOPOLOGY_CONFLICT.md) · [任务索引](UNIFIED_TASK_INDEX.md)

## 02｜先把真实接收与自动投递分开

任务书已按固定Git字节保存到本机，独立计算SHA-256，并向Issue167发出真实ACK。本轮是Founder直接调用现有Codex主机接收；没有新建或证明存在后台自动队列。

分支从核实的main独立建立。原AWT分支、私人EcoEngine和Council内部资料未改动。

来源：[本机收据](LOCAL_INTAKE_RECEIPT.json) · [Issue ACK](https://github.com/simon947161/eco-agent-system/issues/167#issuecomment-7124894771)

## 03｜AWT已经停止，不重新消耗研究预算

PR165审查明确接受有界调查及NO_SUITABLE_DATASET停止结论，原生review.commit_id与冻结HEAD一致。“没找到完整链”不等于全球没有数据。

保留PENDING / DATA_NOT_READY / NOT_DETERMINED；CI为NOT_TRIGGERED。没有重跑旧合成计算或重开Dryad候选。

来源：[AWT验收指针](AWT_P4_ACCEPTANCE_POINTER.md)

## 04｜14份出版物，证据读到了哪一层就说到哪一层

覆盖PFAS、药物、内分泌活性、抗性基因、微塑料、消毒副产物及水文背景。三篇指定种子已核对身份，但鱼类论文仅取得元数据，体外测定论文只读到出版商索引摘要，不能声称三篇都完成全文审查。

Warwick论文还发现检出比例与显著性文字的内部不一致，已保留问题而未替作者修正。

来源：[文献与主张阶梯](WHH_P0_EVIDENCE_MAP.md) · [阅读深度登记](literature_register.json)

## 05｜检出不等于患病，反证也必须保留

环境检出 → 外部接触 → 内部剂量 → 细胞/生物响应 → 健康结局，每一步都要独立证据。

三个不同证据族提供约束：具体下游化学指标可能低于其参考值；WHO2019对当时饮水微塑料给出有条件低风险判断；NHMRC强调控制消毒副产物不能损害消毒。它们不构成本地无风险保证。

来源：[反证及局限](WHH_P0_EVIDENCE_MAP.md)

## 06｜河流能相连，不代表污染物已到达

2024年报文字支持Cooma Creek → Numeralla → Murrumbidgee的河段连接。The Glen精确出水口、COO300方向和Wagga路径的定量贡献仍未核实。

2022/23方向描述相反；2024/25并未取得足以消除冲突的站点证据。不能把图上的一根箭头当成测量结果。

来源：[有条件关系图](WHH_P0_TOPOLOGY_CONFLICT.md)

## 07｜断流会改变问题本身

2024、2025年报记述Cooma相关溪流后期断流或形成水潭。年度叙述不提供可计算的精确开始/结束日期，但足以否定“永远连续混合”的默认假设。

孤立水潭需要水量、蒸发、地下交换和复连事件证据；浓度上升也可能来自水量减少，不能直接推断污染输入增加。

来源：[2024官方年报p21](https://www.act.waterwatch.org.au/__data/assets/pdf_file/0006/2827986/Reach_report_cards_2024.pdf) · [概念模型](RERM_MODEL_ADMISSION.md)

## 08｜9个门户，5个深入；开放许可有对象边界

The Glen与EPL6368公共名称关联已确认，实际许可详情仍未取得。Waterwatch自有文字许可有图片/第三方例外；BOM许可表列WaterNSW为CC提供者，仍需绑定具体站点文件和提供者代码。

WaterNSW API需要注册/key，本轮在文档阶段停止。网站可读不是原始数据已准入。

来源：[许可登记](WHH_P1_SOURCE_AND_LICENCE_REGISTER.md) · [候选JSON](whh_candidates.json)

## 09｜最危险的错误往往发生在连接数据时

NO3-、NO3-N和TN不能因单位都写mg/L就相等。沉积物干重浓度不能当水浓度；ARG检出不能当活菌；“总PFAS”必须有分析物列表。

没有同时的出水浓度与出水流量，就没有可核验的出水负荷。410081河流站不能充当污水厂流量计。

来源：[时间/QC与语义闸门](WHH_P1_TIME_QC_JOINABILITY.md)

## 10｜三层模型只是待验证概念，不是运行结果

L1连续流守恒、L2平流—弥散—反应、L3断流水潭，已写出符号式、量纲、最小输入、混杂与反驳条件。

三个层级概念准备均为PARTIAL，当前计算全部NO-GO。没有水质模拟、校准、健康风险指数或源归因输出。

来源：[RERM准入表](RERM_MODEL_ADMISSION.md)

## 11｜复用成熟边界，不制造另一套平台

复用PR129来源/CRS契约、CarbonOS D3准入规则和Evidence Passport的主张/缺口分层。甲烷账本与WHH不兼容的数值因子没有移植。

NatureHash仍是概念研究；EcoChain权威主目录/审批接口未在本轮确认。交付为Markdown/JSON及离线检查，不建立新数据库或AI平台。

来源：[复用清单及精确hash](REUSE_AUDIT.md) · [验证记录](VALIDATION.md)

## 12｜请先审查，再决定是否授权下一小步

建议ChatGPT优先审查：方向冲突是否被保留；反证是否充分限定；许可是否绑定正确对象；三层符号式与停止理由是否成立。

Founder下一步最小决策：是否批准一项明确的点位/站史资料核验及其来源范围。任何原始文件下载/存储/解析，必须另列精确URL、许可、大小/字段范围再批；模型执行、现场或健康研究、合并部署及对外主张均未批准。

来源：[CRP交接](CRP_HANDOFF.md) · [下一轮边界](NEXT_SESSION.md)
