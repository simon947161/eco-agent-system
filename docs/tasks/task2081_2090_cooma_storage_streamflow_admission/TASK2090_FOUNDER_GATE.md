# Task2090 Founder Gate — Cooma Storage and Streamflow

Status: SOURCE_INVESTIGATION_COMPLETE / L1_ADMISSION_COMPLETE / QUANTITATIVE_STORAGE_GAP_OPEN

## Gate state

```text
PR105_MERGED
/ PR106_MERGED
/ MAIN_31047B6C
/ MITTAGANG_410033_IDENTITY_ADMITTED
/ OFFICIAL_FLOW_UNITS_ML_PER_DAY
/ DATED_OPERATIONAL_FLOW_FACTS_ADMITTED
/ QA_LIMITATION_RETAINED
/ COOMA_SOURCE_WATER_PATHWAY_ADMITTED
/ NAMED_DISTRIBUTION_STORAGES_ADMITTED
/ PUBLIC_STORAGE_TIME_SERIES_NOT_LOCATED
/ COUNCIL_NON_PUBLIC_DATA_NOT_ACCESSED
/ QGIS_V0_4_UNCHANGED
/ MAXIMUM_L1
/ NO_WATER_SUFFICIENCY_OR_SAFETY_CONCLUSION
```

## Independent Founder Gate

The Task2071–2080 real-data intake contract is accepted for continued bounded official-source use.

The Mittagang Crossing gauge is suitable for a next controlled flow-series intake because its identity, owner, units, official relevance and quality caveat are now documented. A future run must still record:

- exact endpoint and retrieval timestamp;
- full available time coverage and selected analysis window;
- units and day boundary/time zone;
- provisional/final or quality-code status;
- missing values and duplicates;
- immutable SHA-256 digest;
- source-specific licence/retention rule;
- L1 Run Receipt before any L2 indicator.

The named Cooma distribution storages are admitted only as facility and process facts. Quantitative storage accounting remains blocked until a lawful public time series is located or the Founder separately authorizes a Council data-request and privacy/authority process.

## Recommended next action

Proceed with one narrow executable slice:

> Retrieve the official public Mittagang Crossing `410033` flow series through a fixed, allowlisted source; retain raw evidence according to licence; validate units, timestamps, quality codes and missingness; publish a redacted L1 Run Receipt; do not calculate supply sufficiency or edit QGIS.

In parallel, prepare a public-information request list for Cooma storage capacity and level/volume time series, but do not contact Council or access non-public systems without a separate Founder authorization.

## CRP Harvest Block

- 核心知识点：Cooma 的公开河流流量证据链可成立；公开储水设施事实存在，但储量时序尚未找到。
- 想法点：先让 `410033` 成为可重复运行的真实流量证据源，再把储水缺口变成明确的数据请求。
- 愿望点：形成降雨—河流流量—取水—处理—储存—用水的持续水量账本。
- 推理点：河流流量与城镇配水储量属于不同水量项，不能互相替代。
- 关键决策：最大结论等级维持 L1；QGIS v0.4 不变；非公开 Council 数据继续隔离。
- 未解决问题：公开流量端点的稳定机器接口、质量代码、储水容量及连续储量、实际取水与需求。
- 下一步行动：受控摄取 `410033` 官方流量时序；另立 Council 数据请求门。
- 项目关键词：`Cooma`, `Mittagang Crossing`, `410033`, `WaterNSW`, `Streamflow`, `Storage`, `Water Balance`, `L1 Evidence`.
