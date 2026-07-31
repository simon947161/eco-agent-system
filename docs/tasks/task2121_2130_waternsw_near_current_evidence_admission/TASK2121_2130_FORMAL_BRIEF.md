# Task2121–2130 — WaterNSW Near-Current Evidence Admission

## Authority

```text
AUTHORISE_TASK2121_2130_WATERNSW_NEAR_CURRENT_EVIDENCE_ADMISSION
MAINTAIN_TREND_DEFERRAL_PENDING_HYDROLOGY_REVIEW
```

## Purpose

Create a bounded admission path for exact WaterNSW response bytes and return
the available 2026 evidence to the existing comparability gate without
manufacturing provenance.

## Tasks

| Task | Result |
|---|---|
| 2121 | Reconfirm PR #112 Founder Gate and trend deferral |
| 2122 | Define exact-response admission boundary |
| 2123 | Require station `410033`, parameter `FlowRate`, unit `ML/day` |
| 2124 | Require HTTP 200, HTTPS source and retrieval timestamp |
| 2125 | Compute SHA-256 over exact response bytes |
| 2126 | Compute a separate canonical retrieval-receipt SHA-256 |
| 2127 | Keep raw response local and Git-ignored |
| 2128 | Preserve unresolved semantics, timezone and quality mapping |
| 2129 | Run tests and emit real-run receipt |
| 2130 | Stop at Founder Evidence Gate |

## Real-run finding

The current runtime has neither the exact body returned on 28 July 2026 nor a
configured WaterNSW subscription key. The user-observed fields—station,
parameter, value, unit, timestamp and quality code—are a useful evidence
summary, but they are not the original response bytes.

The adapter therefore emits:

```text
ADMISSION_BLOCKED_MISSING_RAW_RESPONSE
/ S0 EVIDENCE_PREPARATION
/ L1 MAXIMUM
/ NO_COMPARISON
/ NO_CURRENT_CONDITION
/ TREND_DEFERRED
```

The code is ready to admit a future exact response, but no admission is claimed
in this batch.

## Source-policy note

WaterNSW's official developer portal states that Water Data API use requires a
registered account, product subscription and unique subscription key. No key
is embedded in code, committed to Git, or inferred from prior conversation.

## Prohibited interpretations

- A copied JSON object is not substituted for the original response.
- No percentile, high/low/normal label or current-condition statement is made.
- No drinking-water, supply, engineering or public-safety conclusion is made.
- Formal trend remains deferred pending qualified hydrology review.
