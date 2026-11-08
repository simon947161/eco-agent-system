# 提交 ChatGPT 的只读科学评审材料

任务CLIMATEOS-METHANE-FACTOR-ORDER-001，唯一依据TASKBOOK_ZH.md。建议依次审阅FOUNDER_REPORT_ZH、DATA_FIT_CARDS、NO_VALID_PAIR_REPORT、UNCERTAINTY_AND_ATTRIBUTION、LOCAL_CONTROL_DECISION_MATRIX及实际输入/QC。导航README。

## 请求审查（不得自动触发实验）

1. 真实NOAA数据已取得，但3340完整时间行没有足够精度/高度证据：NO_VALID_PAIR是否正确执行第7节？固定2ppm不消除气象缺口的判断是否成立？
2. 9.9/35.05m两进气高度、气象RH水/冰定义未知、站压非海平面压，是否足够明确？还有哪些最小元数据是继续前必须满足？
3. P1对数分解、P/e两顺序平均、协方差误差传播是否正确？是否误将数学贡献表述为因果贡献？
4. NOAA背景QC本身依赖风，`.C.`只是非背景；保守筛选的选择偏差与样本损失是否诚实？
5. A–E问题树是否区分生成、逸散、输送、辐射及治理？条件矩阵是否仍有未经证实的措施暗示？
6. 三候选调查、原件/子集/元数据哈希及CC0/CCBY来源区分是否满足审查？

请针对本次Draft PR精确HEAD给出ACCEPT_WITH_CONDITIONS / REVISE / REJECT及阻塞项。此文和GitHub评审请求只是**提交材料**，不是已收到ChatGPT意见；PR138/139继承成果也不自动等于已科学接受。先前PR138评论仅确认提交评审、PR139可见评论为空，未据此虚构ACCEPT。

状态保持D3 DATA_NOT_READY、P1-A PENDING。不运行观测P1比较、P2–P4真实标定、排放反演、ACCU、部署或合并。审查通过不扩大授权。

## Conversation Radar

- 知识点：同小时可连接不等于可比较；逐行高度比站点标称高度更具体；状态换算不是排放量。
- 想法：未来先完善历史传感器误差/高度与RH定义，再决定同高度分层是否值得做；不先追求排名。
- 决策：三个候选到限；精度门未过，采用NO_VALID_PAIR分支。
- 风险：背景选择与风循环论证；空气/水相混用；用显示位数冒充精度；区域措施过度外推。
- 开放问题：历史气象传感器校准和高度证据是否可公开取得？适用RH参考和共同校准协方差如何界定？
- 下一行动：ChatGPT只读评审；Founder再决定是否授权补证；不自动继续实验。
- 项目关键词：ClimateOS、CarbonOS、EcoEngine、Evidence Passport、P1、NOAA、ICOS、GAW、methane、uncertainty、human-in-the-loop。
