# Climate Scorecard：政策证据层审计

本轮核查 [首页](https://www.climatescorecard.org/)（一次超时）、[scorecard](https://www.climatescorecard.org/scorecard/)、[reports](https://www.climatescorecard.org/reports/)、公开承诺跟踪页、澳大利亚/中国分类页，以及两个有界报道样本。未访问私人草稿、订阅或邮件。

固定快照2026-11-09。原始scorecard HTML字节SHA为 `72dd282073bf130b08379e2b0436599ff6825d00972862e3a4c3f764f6fe0948`；JSON-LD日期：2021-03-29发布、2025-09-25修改。**这不证明25个评分卡都更新到了2025，更不证明2026仍适用。** 个别政策文字明显旧，逐国生效日期UNKNOWN。

页面规则为五项各20分：是否在2023前更新50%减排承诺；2030减排50%承诺；对应计划；2050碳中和承诺；对应计划。分档为0–49、50–79、80–100。页面包含10分刻度的CSS显示标签，但未给出本轮可以独立重算的逐项部分得分规则。因此记录**原站实际发布标签**，不以Yes数量自行重算、不提供新排名。

`extract_metadata.py` 从每张country toggle的CSS class读取数值，再核对同页 `::after content` 定义，不靠猜测英文类名。25个卡包括欧盟；24个为国家卡。导航菜单24个实体与正文25个评分卡不一致（例如正文有Poland）；不把菜单当评分覆盖全集。事实清单：[scorecard-facts](evidence/scorecard-facts.json)。没有深读25国政策，仅对任务选定的12案例做有界映射。

| 证据层 | 本轮机器表示 | 允许解释 | 禁止解释 |
|---|---|---|---|
| COUNTRY_POLICY_SCORE | POLICIES的8个原站标签 + POLICY_ASSESSMENT | 该版本规则下的外部评价 | 物理系数、实测减排、国家温控贡献 |
| POLICY_COMMITMENT | 4个NDC 3.0提交行元数据 | 有官方提交记录可追踪 | 目标已实现、全文已审查或法律合规 |
| COUNTRY_REPORT | `AU_COUNTRY_REPORT`，Jessica Gregory，2026-03-25/05-08 | 公开报道的作者/日期/预测类型 | 将2026预测当完整2026观测 |
| OBSERVED_OUTCOME | `OUTCOME_GAP`，EVIDENCE_INSUFFICIENT | 指向森林报告与独立验证需求 | 将媒体描述当已接纳生态成果 |

报道样本：[澳大利亚预测](https://www.climatescorecard.org/2026/03/australia-2026-emissions-forecast/)列出官方清单与预测报告引用，但本轮没有复核其全部数字，故仅入报道元数据。[Report80](https://www.climatescorecard.org/project/report-80/)是森林专题，国家文章日期为2024-11-25；不是统一方法的卫星观测数据包。评分页个体作者未明确，记录机构发布者，个体作者UNKNOWN。

冲突C1：澳大利亚卡正文把43%的比较基年写为2030。[官方Climate Change Act，Compilation2，s10(1)(a)](https://www.legislation.gov.au/C2022A00037/2025-02-20/2025-02-20/text/original/epub/OEBPS/document_1/document_1.html)固定文本的基年是2005。保留原站50标签，政策条目标MATERIAL_CONTRADICTION，不静默改源或推断分数应调整。C2：Russia卡内70% reduction与30% below1990表述相冲，待官方逐条核验；未裁决其现行承诺。India强度目标与绝对减排的口径必须分开。

Malaysia/Ethiopia/Egypt/Fiji在本次评分正文均NOT_COVERED，不表示该组织从未写过这些国家。以 [UNFCCC NDCregistry](https://unfccc.int/NDCREG) 可见提交元数据补背景；本地获取为防护页，标EVIDENCE_INSUFFICIENT，未下载NDC全文或解析目标。

版权：站点All Rights Reserved；只发布自写说明、事实标签、短定位和链接。原始HTML在git-ignored缓存，不公开原文、图片或整篇报道；没有把“公开可读”写成开放再分发许可。页面修改会生成新版本，不能覆盖旧收据。
