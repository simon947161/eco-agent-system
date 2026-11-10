# 多来源数据准入与 Wagga 真实降雨复算

本轮已完成有界数据准入与历史统计：三份真实CSV，Wagga春季46个合格年份；冬季基准仅23年，继续阻塞。**LOCAL_VERIFIED / OPEN_DATA_RECALCULATED / scientific_admission=PENDING / DEPLOYED=false**。

- [中文 Founder 报告](FOUNDER_REPORT_ZH.md) · [12页离线 Slides](slides.html)
- [唯一任务书](TASKBOOK_ZH.md) · [获取前协议](PRE_ACCESS_PLAN.md)
- [来源登记](SOURCE_REGISTRY.json) · [许可与访问](ACCESS_AND_LICENCE_MATRIX.md) · [真实收据](DOWNLOAD_RECEIPTS.json)
- [数据准入](ADMISSION_REPORT.md) · [配对原表](PAIRED_DATA.json) · [概率与公式](PROBABILITY_RESULTS.md)
- [区间、反例与偏差](UNCERTAINTY_AND_COUNTEREXAMPLES.md) · [跨来源可比性](CROSS_SOURCE_COMPARABILITY.md)
- [EcoEngine/CCZPS/ECOChain交接](ECOENGINE_CCZPS_ECOCHAIN_HANDOFF.md) · [测试](QA_AND_VALIDATION.md)
- [完整数值JSON](evidence/results.json) · [独立分数复核](evidence/independent-exact-audit.json) · [源文件清单哈希](evidence/manifest.json)
- [下一会话](NEXT_SESSION.md) · [双向交接](CRP_HANDOFF.md) · [评审请求](REVIEW_REQUEST.json) · [交付状态](HANDOFF_STATUS.json)

离线复现（Python标准库，无新依赖、无联网）：
```sh
python -X utf8 docs/tasks/climateos_multisource_data_admission_001/scripts/validate.py
```
默认写入忽略的runtime_data目录并与归档结果比较。`--record`仅供本任务作者更新本任务归档；不要在评审时覆盖证据。不要再次运行获取脚本；已达成功停止条件。原始文件在本包evidence/raw，原RONI仍复用PR147单一副本。
