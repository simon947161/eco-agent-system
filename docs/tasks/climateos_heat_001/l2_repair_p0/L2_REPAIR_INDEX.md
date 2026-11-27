
# HEAT–001 L2 repair P0 research index

## State and provenance

- Sole authorization: [Issue #185](https://github.com/simon947161/eco-agent-system/issues/185), Founder REQUEST REPAIR / EVIDENCE.
- Frozen implementation: [Draft PR #184](https://github.com/simon947161/eco-agent-system/pull/184), HEAD 8d70dbe349c9d8667eb09b1f041136f7775a7eaf.
- Gate: a351247e92a673dc39a2136822ed8fe3e5a65231; contract SHA-256 60861f0fc5c34e14f7c66feff10b70b7680e61809cbf27e3df9225c4232a9c7b.
- Current main at branch creation: 9eb7577e145e76161f9f1cd8509348b19c2904cc.
- Isolated branch: codex/heat-001-l2-repair-evidence-20261127.
- Status remains INCONCLUSIVE / MODEL_NOT_READY_FOR_RANKING.
- New model runs: **0**. No solver, model or test was modified or executed. P1, frozen contract and #184 artifacts untouched.

## Research package

- [Full matrix and resource calculation](L2_REPAIR_WORKLOAD_AUDIT.md)
- [Exact-zero periodic state audit](L2_REPAIR_PERIODIC_STATE_AUDIT.md)
- [Deterministic optimization and equivalence protocol](L2_REPAIR_OPTIMIZATION_OPTIONS.md)
- [A/B/C resource-budget proposal and future gate](L2_REPAIR_RESOURCE_AND_BUDGET_PROPOSAL.md)
- [中文 Founder Slides 式报告](L2_REPAIR_FOUNDER_REVIEW_CN.md)

## CRP / evidence map

| Source | Evidence link |
|---|---|
| Task | [Issue #185](https://github.com/simon947161/eco-agent-system/issues/185) |
| Frozen L2 | [Draft #184](https://github.com/simon947161/eco-agent-system/pull/184), exact HEAD above |
| Design | [Draft #182](https://github.com/simon947161/eco-agent-system/pull/182), 8b08152670406ec57de443facd5d589060a675b0 |
| Accepted frozen P1 | [Draft #179](https://github.com/simon947161/eco-agent-system/pull/179), 5a2039a2753142b2eb17665da2dba6c4a8648b14 |
| P0 / P0-A / ARCH-P0 | [#174](https://github.com/simon947161/eco-agent-system/pull/174), [#177](https://github.com/simon947161/eco-agent-system/pull/177), [#180](https://github.com/simon947161/eco-agent-system/pull/180) |
| Receipt/resource code | l2_impl/L2_RUN_RECEIPT.json, l2_impl/profile_resources.py at #184 HEAD |
| Audited paths | l2_impl/run_l2.py:27–48,129–146; l2_impl/l2_model.py:166–189,195–226 |
| Host/resource note | l2_impl/docs/L2_CONSERVATION_CONVERGENCE.md at #184 HEAD |

## CRP — handling and actions

HOME-GPU-01 project directory is projectless and contains only outputs/ and work/; no Git checkout exists there, and no local files were altered. GitHub docs were prepared on an isolated branch created from current main. Inspected code, receipt, contract, resource report and both readable annual JSON outputs at fixed commits, plus current Issue/PR metadata. Binary compressed hourly tables were not decompressed; receipt hashes/sizes were checked, while their row contents remain NOT_VERIFIED. No real site, Council, GIS, field or other non-synthetic data accessed.

No solver, partial/annual/convergence case, benchmark, test, install, CFD, P2, deployment, merge, purchase or remote compute action occurred. GitHub writes are limited to this new docs-only branch/commit/Draft PR. Existing PRs were not changed. Workload arithmetic uses frozen geometry/counters and previously recorded timings; every projection is labeled estimate.

## Review decision

Choose A (full unchanged matrix with a newly approved resource ceiling/verified runner), B (separate temporal-only non-ranking screen with resource approval), or C HOLD. Until a Founder decision and new pre-run gate pass, no further computation is authorized.
