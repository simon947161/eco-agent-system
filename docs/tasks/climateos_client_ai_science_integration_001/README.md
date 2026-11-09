# ClimateOS Client AI：公开证据最小交付

任务 CLIMATEOS-CLIENT-AI-SCIENCE-INTEGRATION-001，2026-11-09。唯一授权 [TASKBOOK_ZH.md](TASKBOOK_ZH.md)。本目录是本次研究索引，不修改旧研究入口。

**LOCAL_VERIFIED_PUBLIC_DESCRIPTIVE_SLICE / REVIEW_READY；非生产服务，科学准入未改变。** 一个真实 NOAA 公开站点、三日数据、一个确定性问题入口，已离线运行。无生成式服务、客户数据、Senversa 接口或部署。

## 阅读顺序
1. [中文创始人报告](FOUNDER_REPORT_ZH.md)
2. [冻结科学基线](SCIENTIFIC_BASELINE_AND_GATES.md) → [能力现实矩阵](CAPABILITY_REALITY_MATRIX.md)
3. [Senversa 公开对标](SENVERSA_PUBLIC_BENCHMARK.md) → [接口契约](CLIENT_AI_ARCHITECTURE_AND_CONTRACT.md) → [复用台账](ACTUAL_REUSE_LEDGER.md)
4. [真实案例](PILOT_CASE_AND_RESULTS.md) → [测试证据](QA_AND_VALIDATION.md) → [机器审计](evidence/audit.json) → [空间结果](evidence/station.geojson)
5. [交接协议](HANDOFF_PROTOCOL.md)、[状态](HANDOFF_STATUS.json)、[评审请求](REVIEW_REQUEST.json)、[续航](NEXT_SESSION.md)、[Conversation Radar](CRP_HANDOFF.md)

## 最小复现（仓库根目录，Python 标准库）
```powershell
python docs/tasks/climateos_client_ai_science_integration_001/run_pilot.py
python -m unittest tests.test_client_ai_evidence tests.test_dynamic_quantification -v
```
第一条只覆盖本目录 evidence 的四个派生文件；原始 NOAA 字节在既有 dynamic_quant 目录，保持单份。runtime.json 的测量值随机器改变；audit.json、station.geojson、CLIENT_REPORT_ZH.md 确定性输出。来源与工件见 [manifest.json](evidence/manifest.json)；不重新下载被阻塞来源。

评审版本采用内容提交 R 与交付元数据提交 D 两阶段，见协议。远程状态/CI 以最后 PR 单一评审评论为准；本地通过不等于远程 CI 或科学审查通过。
