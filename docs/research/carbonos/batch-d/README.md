# Batch D — A/B/C方法比较：ChatGPT科学与战略评审包
2026-11-04 · Issue #131 · Draft PR #132 · **RESEARCH_DESIGN_ONLY / 科学准入 PENDING**

本包响应[Founder任务书6627476759](https://github.com/simon947161/eco-agent-system/pull/132#issuecomment-6627476759)，并落实[C2评审6627278919](https://github.com/simon947161/eco-agent-system/pull/132#issuecomment-6627278919)。基线SHA：61cf333ed980d77267f739b3c36b5aff48b4d1e4。最终交付SHA以包含本包的Git提交和PR评审请求为准，不制造自引用哈希。

## 可直接交给ChatGPT的结论
1. **可支持的事实**：历史AWT是反事实信用规则；IPCC FOD已经包含跨年库存/衰减和气候分类参数。CALMIM、CLEEN已有气候响应研究。ClimateOS不主张首创，也未证明更准确。
2. **本轮设计选择**：同一类填埋CH₄、同一活动历史、同一footprint/时间支持与独立观测目标。Alegal对实际场址通量为NOT_COMPARABLE；另设匹配因子法A-factor，但因子尚未选定。
3. **候选假设**：C在同一FOD库存结构上逐步加入实测过程温湿/氧化/输运；实际体温不等于空气温度。只看到净排放不能同时识别生成、氧化、收集和储存。
4. **数据事实**：发现三个真实公开观测资料入口；没有取得原始序列。NJ资料许可CC0，但文件工具返回403；NY未下载；Zenodo许可值未核实。原件SHA为null。四个澳洲候选不升级。
5. **推断限制**：塔基“排放”含扩散反演；天气可能同时影响标签和模型。已有文献局地拟合不构成独立迁移验证。全ABC当前DATA_NOT_READY，C优势为INSUFFICIENT_EVIDENCE。

## 评审入口
| 交付 | 内容 |
|---|---|
| [D0合同](D0_COMPARISON_CONTRACT.md) | 目标、单位、部门/物理边界、时间尺度、公平输入 |
| [D1原式](D1_BASELINE_METHODS.md) | AWT原式定位；IPCC2006/2019版本；已有动态方法 |
| [D2候选族](D2_RESPONSE_MODEL_FAMILIES.md) | 数学结构、守恒、机制图、参数可辨识性 |
| [原文疑点补充](LITERATURE_AUDIT_NOTES.md) | Kim2026方程与数据可得性须复核；不盲目复用 |
| [D3真实数据](D3_VALIDATION_DATA_DISCOVERY.md) | 优先级、许可、独立性、访问失败 |
| [D4否证协议](D4_FALSIFICATION_PROTOCOL.md) | 时间块留出、泄漏、指标、负对照、停止条件 |
| [方法JSON](METHOD_COMPARISON.json) / [数据JSON](DATA_READINESS.json) | 机器可读；未知参数与原件摘要保留null |
| [来源](SOURCES.json) / [证据矩阵](EVIDENCE_MATRIX.md) | 版本、阅读深度、命题限制 |
| [12页离线Slides](index.html) | 支持键盘、手机、按页证据展开 |
| [交接与CRP](NEXT_SESSION.md) | 下一步决策与边界 |

## 请ChatGPT重点审查
- D0的大气边界与IPCC部门边界桥接是否足够？A-factor在缺合格因子时继续保留为未就绪是否恰当？
- C0/C1的嵌套设计能否使新增过程贡献可辨识？哪些过程必须固定或独立测量？
- 塔基反演的共同气象误差如何影响“独立真值”资格？是否需要独立平台/不同反演作为门槛？
- 以一年训练/一年留出为条件性提案是否有足够统计功效？何种采样才支持年积分与事件峰？
- 原文Kim Eq2/3的不清楚之处是否阻止它成为可执行基线？不得静默修正。
- 哪个最小后续动作值得Founder单独授权？当前建议先合法数据副本的来源/结构/QC审计；完整ABC实验暂不启动。

## 决策建议
建议评审**设计材料**，不批准模型有效性。缺口关闭且另获批准后，才考虑单场址月度B–C1探索；A不匹配时如实标为两方法，不能包装成三方法胜负。研究没有给出准确率排名、排放结果、ACCU或全国总量。

本地验收限定文档结构/离线交互；见evidence/validation.json及browser_qa.json。它不等于原始数据QC、外部CI或科学验证。未执行数值实验、阈值判定、排放计算、外部联络、权限改变、合并、部署；未使用非公开Council数据。
