# ENSO 与澳大利亚区域历史天气概率 — 有界研究交付

**结果：DATA_NOT_READY；最低科学成功门未达到。** 三个固定地区、九站元数据已经选择，降雨归档 HTTP 404，真实天气配对为0。工程检查不代表天气统计完成。

基线 PR147 D `48d0f576e651cd5072e6319ea1539ffa5ba02936`；唯一任务书提交 `9522af5e1b42a343692e470907b6d60b73e8696a`。研究/交付精确提交在 [HANDOFF_STATUS.json](HANDOFF_STATUS.json) 及 PR 交接评论。科学准入始终 PENDING。

## 阅读与评审索引

1. [Founder 中文报告](FOUNDER_REPORT_ZH.md)
2. [唯一任务书](TASKBOOK_ZH.md) · [数值前预登记](PRE_REGISTERED_ANALYSIS_PLAN.md) · [机器参数](PLAN.json)
3. [地区/时间/站点](REGION_AND_TIME_DEFINITION.md) · [选择元数据](REGIONS.json)
4. [来源、许可及获取失败](SOURCE_AND_LICENSE_REGISTER.md) · [获取审计](evidence/ACQUISITION_AUDIT.md)
5. [真实配对文件（空）](PAIRED_ENSO_WEATHER_DATA.json) · [概率状态与公式](CONDITIONAL_PROBABILITY_RESULTS.md)
6. [不确定性与敏感性方案](UNCERTAINTY_AND_SENSITIVITY.md) · [反例及适用边界](COUNTEREXAMPLES.md)
7. [物理机制与混杂](PHYSICAL_MECHANISM_AND_CONFOUNDERS.md) · [CCZPS/ECOChain交接](CCZPS_ECOCHAIN_HANDOFF.md)
8. [QA/复现](QA_AND_VALIDATION.md) · [评审问题](REVIEW_REQUEST.json) · [下一会话](NEXT_SESSION.md) · [Conversation Radar](CRP_HANDOFF.md)

## 离线运行

在仓库根目录执行：

```text
python -m cczps_lite.integration.enso_regional_weather
python docs/tasks/climateos_enso_regional_weather_probability_001/scripts/validate.py
```

默认不联网，不改归档，输出到忽略的 `runtime_data/enso_regional_validation`。入口只返回冻结的失败状态。新 QC 辅助函数只在明确的合成测试里验证；完整概率/块自助/留出估计尚未实现和运行，不能称为真实数据统计引擎。

大库存保存在本地忽略目录；Git 只包含九站元数据摘录、SHA收据、研究文件和测试。下载脚本不是下一轮自动采集器，收据存在即拒绝重试。
