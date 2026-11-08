# 甲烷影响因素：唯一导航入口

CLIMATEOS-METHANE-FACTOR-ORDER-001 · 2026-11-08 · **NO_VALID_PAIR**

交付：[Draft PR #140](https://github.com/simon947161/eco-agent-system/pull/140)。研究HEAD `f3d4ba0`已收到ChatGPT **ACCEPT_WITH_CONDITIONS**，详见[评审回执](SCIENTIFIC_REVIEW_RECEIPT.md)；下文PENDING为提交时状态，不改变D3/P1-A门槛。

先读[通俗中文报告](FOUNDER_REPORT_ZH.md)，再读[停止依据](NO_VALID_PAIR_REPORT.md)。本目录执行冻结[TASKBOOK_ZH](TASKBOOK_ZH.md)，不替代旧任务的状态或授权。

|材料|用途|
|---|---|
|[机制矩阵](FACTOR_MECHANISM_MATRIX.md)|A–E科学问题、因果方向、混杂、时滞、可控性|
|[三个数据适配卡](DATA_FIT_CARDS.md)|官方来源、版本、许可、字段及缺口|
|[不确定性与归因](UNCERTAINTY_AND_ATTRIBUTION.md)|P1公式、顺序无关分解、误差、匹配和状态定义|
|[地点条件决策矩阵](LOCAL_CONTROL_DECISION_MATRIX.md)|填埋场、污水和背景站的证据需求|
|[机器审计](evidence/quality_audit.json)|真实行数、缺失、排除瀑布、原值示例、SHA|
|[来源指纹](evidence/source_manifest.json)、[HTTP获取记录](evidence/acquisition.json)|证据可追溯性；HTML仅作为来源快照，不执行脚本|
|[验证记录](VALIDATION.md)|测试、复算范围与安全审查|
|[ChatGPT评审包](CRP_HANDOFF.md)、[下一轮交接](NEXT_SESSION.md)|只读审查、剩余缺口及停止边界|

## 离线复核（仓库根目录，Python标准库）

```powershell
python docs/tasks/climateos_methane_factor_order_001/audit_observations.py
python -m unittest discover -s docs/tasks/climateos_methane_factor_order_001 -p test_audit.py -v
python -m unittest tests.test_physics_validation.GasTests -v
```

第一条仅核验归档输入指纹并重新生成结构QC JSON，不做P1观测比较。原ZIP存本地工作区外置缓存；若独立取得与记录SHA一致的原ZIP、发布者sha256及气象文件，可加`--source-dir <目录>`重建2024子集。工具没有网络功能、不会自动下载或重试。

NOAA数据引用：Pétron等(2026)，NOAA GML，CH4 in-situ surface，版本2026-08-11，DOI10.15138/ve0c-be70；BRW hourly meteorology 2024，NOAA GML，数据页更新2026-01-09，CC0。CH4子集是从原ZIP小时成员选取注释/表头/2024记录，保持原行值、仅LF规范化；气象为原字节。HTML元数据快照不代表其所述数值产品已经下载。

基线：PR138 `f9016aa4cdc728728a1a5dece0b947b1c2e5e7bc`；PR139 `fc450196d01c9add5edf51f599072b18e6658196`；任务书提交`e5b731531a7f0f694f3ea7cfc0f67c05a668a12a`。PR138 P1代码未改；PR139水相数据未混为大气数据。旧PR均保持原状。

状态：文件/QC **LOCAL_VERIFIED**；观测对照 **NOT_COMPARABLE**；D3 **DATA_NOT_READY**；P1-A **PENDING**；科学评审 **PENDING**；非部署、非科学准入、非真实设施减排结论。
