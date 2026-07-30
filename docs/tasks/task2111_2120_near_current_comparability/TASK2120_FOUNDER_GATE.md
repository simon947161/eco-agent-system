# Task2120 Founder Gate

Date: 2026-07-31  
State: `COMPARABILITY GATE IMPLEMENTED / NOT COMPARABLE YET`

## Finding

The existing WaterNSW near-current sample cannot yet be compared with the
accepted BoM HRS daily historical baseline.

| Dimension | Status | Reason |
|---|---|---|
| Station `410033` | PASS | Same gauge identifier |
| Unit `ML/day` | PASS | Canonical unit matches |
| Measurement meaning | BLOCKED | `FlowRate` is not proven equivalent to a daily discharge total |
| Aggregation | BLOCKED | Near-current interval is undocumented in admitted evidence |
| Day boundary | BLOCKED | Historical product closes at 09:00 local time |
| Timezone | BLOCKED | Source-local timezone and DST treatment are unresolved |
| Quality | BLOCKED | Numeric code `125` is not mapped to A/B/C/E/G |
| Provenance | BLOCKED | Exact response bytes and SHA-256 receipt are absent |

## What was deliberately not calculated

- historical percentile of `194.296 ML/day`;
- “above/below normal” label;
- 2026 current-condition statement;
- formal trend, change point or causal attribution;
- water-supply, drinking-water, engineering or public-safety conclusion.

## Recommended next gate

```text
AUTHORISE_TASK2121_2130_WATERNSW_NEAR_CURRENT_EVIDENCE_ADMISSION
MAINTAIN_TREND_DEFERRAL_PENDING_HYDROLOGY_REVIEW
```

The admission task should retain exact authorised response bytes locally,
publish a redacted SHA-256 receipt, resolve the parameter aggregation and
timezone contracts, and document quality code `125`. It must return to this
comparability gate before any percentile calculation.

## Alternative

```text
PAUSE_NEAR_CURRENT_AND_PREPARE_HYDROLOGY_REVIEW_PACKAGE
```

## CRP

- 核心知识点：同站点、同单位不等于同测量方法。
- 想法点：把可比性做成全维度通过的硬门，避免数字一到手就被误读。
- 愿望点：形成可重复、可回顾的近当前环境证据路径。
- 推理点：日累计与时点/区间流量、不同质量体系不能静默混用。
- 关键决策：本轮状态为 `NOT_COMPARABLE_YET`，不计算百分位。
- 未解决问题：FlowRate聚合定义、09:00边界、时区、代码125、响应摘要。
- 下一步行动：受控接纳WaterNSW近当前证据，或先做水文复核包。
- 项目关联关键词：`ClimateOS v2`, `410033`, `WaterNSW`, `Comparability Gate`,
  `S0/L1`, `Quality Code 125`, `Hydrology Review`.
