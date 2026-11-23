# Founder P4 决策报告 · 8页等价版

评估日期：2026-11-24（Australia/Sydney）｜`READ_ONLY`｜`NO_RAW_DATA_DOWNLOADED`

唯一授权：[Issue #164](https://github.com/simon947161/eco-agent-system/issues/164)。父基线：[PR163冻结提交](https://github.com/simon947161/eco-agent-system/commit/9aea387a4261b913163b3be3197597089d9e9414)。

## 第1页｜结论

**P4.0–P4.4 已完成有界调查，结果 NO_SUITABLE_DATASET。** 已审4项候选、详细评估3项。没有取得任何原始数据包，没有做真实排放计算。没有候选同时连通“同一物料—设施—时间—残渣—能源—校准—权利”。按任务书停止搜索。

这不是“没找到甲烷数据”，而是“找到片段，但不能把片段拼成已证明减排”。SCIENCE=PENDING；DATA_NOT_READY；CREDIT_NOT_DETERMINED。

## 第2页｜实际复用了什么

读取完整Issue164、Issue162、父PR及绑定HEAD的[科学评审](https://github.com/simon947161/eco-agent-system/pull/163#pullrequestreview-6029057378)，核对P0–P3来源、交接、1000t边界及九类护照。复用PR144的物料账语义和PR145的证据/权利分层；只做映射，没有调用模型或修改schema。

旧384角点、570项CI等均是继承记录，本轮不重跑、不冒充新验证。D3旧下载阻塞没有重试。没有访问私人旧系统或Council数据。

## 第3页｜澳大利亚候选

C01联邦CER表是可追溯的监管年报入口 [S02](https://cer.gov.au/markets/reports-and-data/safeguard-data/2024-25-baselines-and-emissions-data)，但不是批次物料账，许可未确认；年度监管baseline不等于无项目填埋量。

C02 NSW交通部门St Peters目录 [S04](https://www.transport.nsw.gov.au/operations/roads-and-waterways/environment-and-heritage/environmental-compliance/environment) 返回403，立即停止。索引中的监测PDF [S05](https://www.transport.nsw.gov.au/system/files/media/documents/2025/SPI-Landfill-Gas-Monitoring-March-2025.pdf) 没有打开，不通过文件直链绕过目录，不把公示等同开放再利用。

## 第4页｜国际候选

C03欧洲AD整场研究 [S06](https://zenodo.org/records/14165793) [S07](https://zenodo.org/records/14197882) 提供工况/因子研究线索；新旧记录必须分开，许可尚未可读，不能因为在Zenodo就假定开放许可。跨厂数据不能冒充同批次反事实。

C04加州奶牛场资料 [S09](https://datadryad.org/dataset/doi:10.5061/dryad.ht76hdrtc) 有安装前后设计、气象与甲烷字段说明，是**方法片段首选**。Dryad政策 [S10](https://datadryad.org/terms) 给出CC0依据，但它不是澳大利亚项目，也不是有机固废1000t链。

## 第5页｜首选仍然卡在哪里

C04设施身份与坐标已被作者删除，应保留匿名。时区、DST、平均窗口长度、同步和校准证书没有核实；个别气象来自机场，不能假装全部共址。浓度来自测量，质量排放来自扩散反演，两者不是独立的真值对照。变量单位说明也有疑点待核。

所有候选都没有建立完整残渣碳、后续CH4/N2O、能源和权利链。不能用合成参数或0填缺；不能将外国研究减排比例直接当作本地项目效果。详见[字段表](FIELD_TIME_QC_MAPPING.md)。

## 第6页｜证据与测试到底证明什么

本轮真正读取的是公开元数据、内嵌README、许可及官方指引。文件大小是页面标签，原始文件URL部分未解析，原始哈希均null。403与工具不可访问分开记录，未编造HTTP状态。

[验证回执](validation_results.json)检查登记JSON、4/3数量、七闸门、链接、敏感输出及冻结文件版本；不验证原始观测真伪，不证明依法可下载，不验证任何真实减排。旧manifest的递归范围会覆盖新增p4，故不运行旧数值复放器，也不修改其冻结封条；详见[验证说明](VALIDATION.md)。

## 第7页｜下一步真正需要批准什么

目前建议Founder先审查本结论，而非直接启动数据接入。若仍希望做**方法片段的文件核验**，可另行批准以下严格分步范围：

1. 只围绕 [C04固定记录](https://datadryad.org/dataset/doi:10.5061/dryad.ht76hdrtc) 的2026-02-19版，补充公开文件URL/许可例外的元数据核实；不要扩大候选集、识别匿名场址或联系作者。当前具体文件下载URL为UNKNOWN，不能编造一个让Founder批准。
2. URL核实并提交后，Founder再单独选择是否批准下载 `All_Receptor_Meteorology_and_CH4_Mole_Fraction_Data.csv`（目录37.97 KB）与 `README.md`（12.75 KB），建议合计上限100 KB、只允许这两项原始URL、无登录/无付费、遇限制即停。该提议尚未获批；不得趁解析链接同时下载。
3. 若第二步获批，只保存、SHA-256、字段/单位/时间/QC/缺失检查；不下载全包或模型结果工作簿，不回归、不排放复算、不转接AWT运行器。任何模型实验再单独批准。

C01/C03许可未知不推荐取件；C02维持STOP。完整AWT证据链仍需不同的专项授权，不自动把C04晋级。

## 第8页｜交接与决策边界

已提交内容定位于[本目录索引](README.md)；精确新HEAD、Draft PR与实际CI状态由GitHub回执绑定，未生成虚构发布地址。请求ChatGPT审查：许可支持是否被夸大、三种时间尺度是否被混同、方法片段排序是否合理、NO_SUITABLE_DATASET是否得到证据支持。

Founder最少决策：接受本次STOP；或另批第7页的第一步元数据补查。除此之外，下载/保存/哈希/解析、真实接入、专业鉴证、合并、部署及正式主张均未获准。
