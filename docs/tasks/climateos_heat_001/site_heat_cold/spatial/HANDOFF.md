# 第二批交接｜空间位置、污水站计量与学术方法交流

本批由 [Issue #189](https://github.com/simon947161/eco-agent-system/issues/189) 的[完整任务书](../FOUNDER_TASK.md)授权。第一批 [PR #190](https://github.com/simon947161/eco-agent-system/pull/190) 已完成独立回读，父提交固定为 `8101d81be403ddaf45f7cbd9fe80081bf63baeb0`。使用上游同一份合成输入和热水交付口径。

1. 选择一组已核实的代表日，给出就地、明示距离及归零/反转边界的可复算比较；标注物理单位、输热温级、损失、泵电、备用燃料、运行碳排及服务等价。明确比较基准（原锅炉，或本地回收），并区分零收益时继续运行与主动停止的结果。计算约束与反例应让第三方复算，保留 #187 的动态模型接口。
2. 给出站内源、换热、储罐、热用户、余热去向的空间图和计量点。用污水站的出水热、消化热、沼气 CHP、火炬与逸散演示跨行业的计量逻辑；热量、燃气去向、甲烷质量以及碳排分别对账。官方技术参照 [IPCC 废水章节](https://www.ipcc-nggip.iges.or.jp/public/2019rf/pdf/5_Volume5/19R_V5_6_Ch06_Wastewater.pdf) 与 [Malabar 公开案例](https://arena.gov.au/knowledge-bank/malabar-biomethane-project-proof-of-concept-life-cycle-assessment/)。[AWT P4](https://github.com/simon947161/eco-agent-system/pull/165) 的实际数据仍有证据缺口。
3. 给出潜在 UNSW 方法交流用的中英双语问题和一份带单位、时间戳、出处/质量的最小字段表。演示 AI 如何给出可反驳的调度建议、记录证据，并保留人的复核、拒绝、覆盖及理由。保持研究身份和离线边界。
4. 在本目录提交结果、验证命令和回执，报告与 #190 互链。实收 ACK、完成后回读固定 HEAD、回告 #189。两批交给 Founder 审阅。