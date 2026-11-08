# 下一轮交接

本轮工作分支 `research/climateos-spatial-ghg-hypothesis-validation-001`，唯一入口[README](README.md)。远程Draft PR提交及评审状态在PR会话/后续回执记录；不要把本文件的研究完成当评审已通过。

## 保留的事实与边界

- 基线PR140 HEAD `16f0b59dab966f0b66d91b7c28135e8fce9e4cc1`，旧任务/旧PR不改。
- 已取得CC0 NOAA AirCore ZIP；外部本地缓存 `D:\Codex\ClimateOS\.local\spatial-ghg-hypothesis-validation-001`。完整ZIP未进Git；单个L2+INI+L1met原字节及README/回执在本任务evidence。离线复算不需要再下载。
- ATom两个入口403已停止；AirCore第二候选；WDCGG Jungfraujoch第三候选元数据后停止。不得换镜像或新增第4个候选。
- Stage1 WITH_LIMITS，Stage2 BLOCKED/NO_VALID_VERTICAL_PROFILE，Stage3 WITH_LIMITS/METHOD_READY_NOT_VALIDATED。科学准入PENDING，D3 DATA_NOT_READY、P1-A PENDING、PR140 NO_VALID_PAIR不变。
- 5项防错测试、8项P1参考测试及离线结构QC通过；不代表真实比较通过。没有观测P1、层差、反演或模型模拟。

## 下一步顺序

1. 阅读ChatGPT针对精确研究HEAD的只读评审，归档回执并区分“已读/独立复跑/作者报告”。只纠正本任务报告中的事实/公式/代码错误；不借评审自动开新实验。
2. Founder决定是否接受本轮研究结果；如要推进定量工作，先决定是否仅补现有候选的公共版本/传感器/湿度/高度证据，再重新冻结协议。
3. 若未来批准模型路线，先核具体模型许可、全输入、守恒测试、时域、可接受等效界限和资源；未经单独批准不跑。
4. 缺元数据继续UNKNOWN/BLOCKED，不重新计算固定2ppm、不隐含替换CO2/CH4、不用Cooma名字套AirCore数据。

无需任何新权限即可阅读当前归档；需外部联系、访问受限源、付费或扩大模型运行范围时停止并报告。无部署/合并授权。

## Conversation Radar

| 类别 | 记录 |
|---|---|
| Knowledge | 干摩尔分数/环境质量浓度不同；气体质量效应与航空综合效应不同；AirCore采样/分析时钟不同 |
| Ideas | 小型问题—模型—输入—误差—准入契约；复用P1而不新造海拔因子 |
| Decisions | 三候选封顶；一个预选剖面；全局缺口停止定量；反事实只设计 |
| Risks | RH升降段混用、尺度转换链不明、数据层级误称原始电信号、独立样本夸大、NOx结果误归CH4 |
| Open questions | P/T/RH精度与datum公开证据在哪里？是否存在完整开放直接CH4/CO2高度脉冲复现包？ε如何独立确定？ |
| Next actions | 只读评审、最小修正、Founder决策；不自动启动下一阶段 |
| Keywords | ClimateOS, CarbonOS, EcoEngine, CCZPS, ATom, AirCore, OH, CO2, CH4, uncertainty, counterfactual, evidence admission |
