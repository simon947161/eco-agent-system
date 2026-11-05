# 执行与验证记录

2026-11-05；先行任务书commit `7ce22986fd89e38ef32068d010417b6e28acf236`，在实现前已push并回读GitHub。main基线与受保护PR固定版本见能力审计。本轮没有改旧分支或已有模型、地图、界面，没有常驻服务。

## 真实数据调用

公开NASA和NOAA两个候选各请求一次；请求与哈希见证据登记。只有NOAA原字节作为本轮智能体输入。下载完成后，执行离线回放，结果`OBSERVATION_DESCRIPTIVE_SLICE_PASSED`。不是合成站点成功，也不是LIVE持续采集；准确含义是本轮真实下载成功并端到端回放成功。NASA第二源只做元数据核查，没有假装走过同样的工具链。

实际trace：get_environmental_context → query_observations → run_verified_model（描述算术）→ check_regulatory_context（NOT_ASSESSED）→ generate_evidence_report。保存[实际JSON](evidence/actual-run.json)和[中文报告](evidence/ACTUAL_OBSERVATION_REPORT_ZH.md)。原QA字段TMAX/AWND均为`,,W`，QFLAG为空；没有缺日，未声称没有测量误差。数据日界未知，保持PROVIDER_OBSERVING_DAY。NASA显式UTC，不与之拼接。

|保存的负向路径|实际拒绝|
|---|---|
|missing_data|MISSING_DATA|
|incompatible_unit|UNIT_OR_VARIABLE_MISMATCH|
|wrong_space|SPACE_MISMATCH|
|wrong_time|INVALID_TIME|
|unverified_time_basis|TIME_BASIS_MISMATCH|
|unauthorized_model|MODEL_NOT_AUTHORIZED|
|insufficient_evidence|INSUFFICIENT_EVIDENCE_MIN_3_DAYS|
|methane_not_ready|DATA_NOT_READY_OR_SOURCE_NOT_ADMITTED|
|tampered_bytes|HASH_MISMATCH|

全部无result。详见[negative-runs.json](evidence/negative-runs.json)。这九项是修改请求或移除/改动原件的软件反向验证，不是九次气象/气体科学实验。单元测试另用明确修改的测试行检查缺值、NaN/Inf、负风速、质量标志、重复日和站点错误；修改后的测试收据不是新的政府证据。

## 复现

在仓库根目录，Python标准库，无新依赖、账号、网络和数据库：

```console
python -m cczps_lite.integration.dynamic_quantification
python -m docs.tasks.climateos_dynamic_quant_001.replay_validation
python -m docs.tasks.climateos_dynamic_quant_001.validate_package
python -m unittest discover -s tests -p test_dynamic_quantification.py -v
python -m unittest discover -s tests -v
```

第一个只打印，第二个明确写本任务evidence下三个结果文件。固定原件通过局部.gitattributes保留字节；复放不需要重新下载。主机实际使用Codex bundled Python，Windows运行。原下载件在政策许可范围内署名公开存档，不能推断所有其他NOAA档案可再分发。

validate_package写文档检查结果；初次临时校验把尚未生成的自身结果当成断链，已改为先创建结果文件再检查，并重新通过。没有因此跳过实际缺失链接。

## 本轮测试结果

- 新增5个测试方法通过，覆盖真实回放与多组拒绝子用例。
- 全仓`unittest discover -s tests -v`：**487 tests，OK，skipped=1**，11.771秒；唯一跳过为Windows不允许创建symlink的既有测试。完整日志见[evidence/UNittest_FULL_LOG.txt](evidence/UNittest_FULL_LOG.txt)。
- 全仓测试会重写四个既有展示产物；检查后仅restore这四个生成文件，不将它们混入本PR。
- 文档本地链接、JSON、原件SHA、工具trace与拒绝无result的一致性检查另见[evidence/document-validation.json](evidence/document-validation.json)。Git diff --check结果随提交前验证记录。

这些是软件与文档检查。没有独立仪器验证、模型预测评估、因果分析、MatrixOne基准、QGIS渲染验收或法定审批。不因测试通过将它们升级为科学证据。无UI改动，不伪造浏览器测试。

## 完成边界

有界工程与研究任务完成；科学总愿景仍局部可用。门为PROCEED WITH CONDITIONS；甲烷BLOCKED，完整耦合模型RESEARCH ONLY，MatrixOne NOT_BENCHMARKED。旧NASA默认LST/UTC误标问题已登记，未在本PR扩大修复。下一研究必须重新指定数据/方法/预算，不能由本任务自动续跑。
