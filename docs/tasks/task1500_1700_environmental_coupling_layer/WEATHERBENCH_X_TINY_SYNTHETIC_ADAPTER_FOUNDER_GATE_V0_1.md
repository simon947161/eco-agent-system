# WeatherBench-X Tiny Synthetic Adapter Founder Gate v0.1

Date: 2026-07-16

Status: IMPLEMENTATION_COMPLETE / READY_FOR_FOUNDER_REVIEW / NOT_MERGED

Branch: `agent/weatherbench-tiny-synthetic-adapter-v0-1`

Base main HEAD: `b2f8ada01e0306937805571d496e2ba2962414f0`

## 1. Gate result

`BOUNDED_SYNTHETIC_ADAPTER_PASS / UPSTREAM_AND_REAL_DATA_NOT_EXECUTED / MODEL_ADMISSION_BLOCKED`

The approved tiny synthetic lane is complete. It demonstrates that ClimateOS
can enforce a fixed evaluation boundary and calculate three transparent
latitude-weighted metrics without importing WeatherBench or accessing external
data.

It does not demonstrate WeatherBench compatibility, model skill, physical
consistency, regional fitness or decision value.

## 2. Verification matrix

| Control | Result |
|---|---|
| Repository-authored micro fixture only | PASS |
| Fixed interface | PASS |
| Unknown fields and URL field rejected | PASS |
| Real-data classification rejected | PASS |
| External origin rejected | PASS |
| Time/lead consistency enforced | PASS |
| Variable/unit mapping enforced | PASS |
| Grid shape enforced | PASS |
| Weighted RMSE/MAE/bias arithmetic | PASS |
| Official WeatherBench score claimed | NO |
| Upstream code installed or run | NO |
| Dataset downloaded | NO |
| Network/cloud/API/account | NO |
| Cost | AUD 0 |
| Full repository regression | 219 PASS |
| Task1641–1650 activated | NO |

## 3. Founder decisions now available

### Gate A — Merge prototype

Authorize controlled merge only after verifying the resulting Draft PR remains
limited to the adapter, fixture, tests and three governance/reference records.

### Gate B — Continue Task1641–1650

Requires separate explicit authorization. The present prototype must not be
used to imply that the Bondo Passport Validation and Change Detection batch has
started.

### Gate C — Any real or upstream evaluation

Requires a new cost/data/execution gate covering exact code version, dependency
lock, source integrity, dataset identity and licence, object sizes, storage,
transfer, compute, variables, grid, time conventions, leakage and reproducible
audit outputs.

Until a further decision, the correct state is:

`WAIT_FOR_FOUNDER_MERGE_DECISION / NO_REAL_DATA / NO_UPSTREAM_RUN / TASK1641_NOT_STARTED`
