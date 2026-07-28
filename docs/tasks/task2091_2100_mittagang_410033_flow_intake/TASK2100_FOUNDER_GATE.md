# Task2100 Founder Gate — Mittagang 410033 Flow Intake

Status: REAL_RUN_COMPLETE / L1 RECEIPT COMPLETE / CURRENT-DATA GAP OPEN

## Gate state

```text
PR107_MERGED_MAIN_7B7F4289
/ INDEPENDENT_FROM_MAIN_7B7F4289
/ FIXED_BOM_HRS_HTTPS_ENDPOINT
/ HTTP_200_REAL_DOWNLOAD
/ STATION_410033_IDENTITY_VALIDATED
/ UNIT_ML_PER_DAY_VALIDATED
/ COVERAGE_1964_03_01_TO_2024_02_29
/ ROWS_21915
/ MISSING_DATES_0
/ BLANK_VALUES_0
/ DUPLICATES_0
/ QUALITY_CODES_RETAINED
/ SHA256_RECORDED
/ SOURCE_LOCAL_TIME_BOUNDARY_RETAINED
/ IANA_TIMEZONE_NOT_DECLARED
/ RAW_FILE_GITIGNORED
/ COUNCIL_NON_PUBLIC_DATA_NOT_ACCESSED
/ QGIS_V0_4_UNCHANGED
/ MAXIMUM_L1
/ NO_ENVIRONMENTAL_OR_SUPPLY_CONCLUSION
```

## Founder Gate finding

The controlled intake is suitable as a reproducible historical L1 evidence
source. The file is official, fixed, licensed, content-addressed and machine
validated. Its complete date sequence includes source-declared model gap
filling and quality classes; completeness must not be confused with uniformly
high observational quality.

This product ends on 29 February 2024. It cannot replace a current/provisional
2026 flow feed. The old WaterNSW CGI returned HTTP 403 to bounded automated
requests in this environment, so current operational ingestion remains a
separate endpoint-access gate.

## Recommended next action

1. Preserve PR #107 merge and `main@7b7f4289f8c4af609495e675fc9f2150fe8d7cd1`
   as the independent review base.
2. Decide whether to pursue a registered WaterNSW API/WaterInsights export for
   current flow, or first use the admitted historical series for a strictly
   quality-aware climatology method design.
3. Keep current flow, town extraction, treated storage and demand as separate
   evidence terms.

## CRP Harvest Block

- 核心知识点：BoM HRS 提供 410033 的固定官方历史日流量产品，连续覆盖 1964–2024。
- 想法点：历史验证序列与当前运营序列应成为两个独立 Evidence Objects。
- 愿望点：最终形成降雨、流量、取水、储存和需求可持续更新的水量账本。
- 推理点：零缺日不等于全部直接观测；质量代码与模型补缺必须参与后续方法门。
- 关键决策：当前只升至 L1；不把 2024 年截止的历史文件说成 2026 当前状态。
- 未解决问题：WaterNSW 当前流量接口、明确 IANA 时区、取水量、储水量和需求。
- 下一步行动：完成 PR #108 独立 Founder review，并在注册门后准入 WaterNSW 当前流量 API。
- 项目关键词：`410033`, `Mittagang Crossing`, `BoM HRS`, `Streamflow`, `Quality Code`, `L1 Receipt`, `Water Balance`.
