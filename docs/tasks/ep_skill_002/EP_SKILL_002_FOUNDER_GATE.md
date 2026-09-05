# EP-SKILL-002 Founder Gate — Cooma Current Evidence Refresh & Convergence v0.1

Date: 2026-09-04  
State: `FOUNDER_AUTHORISED_OPTION_B / DESIGN_GATE_COMPLETE / IMPLEMENTATION_NOT_STARTED`
Authoritative baseline: `598eed3d65c9d7d9521166908df50475d20951ca`

## Founder decision — 2026-09-05

`AUTHORISE_OPTION_B`

Founder authorises the bounded offline EP-SKILL-002 implementation described in Option B, subject to the orthogonal-state correction below. This is not network authority: no external API call, new environmental-data retrieval, WaterNSW authentication, public release, A2+ action or current-condition conclusion is authorised. Any future Option A execution requires a separate exact Founder network token.

## 1. Current accepted baseline

EP-SKILL-001 is in `main`. It accepts an immutable SiteReadingRequest, resolves admitted sources without array-order dependence, reuses the Environmental Evidence Passport and Time-Bounded Environmental Answer, binds accepted QGIS context, emits PC-01/02/03/04/13 plus an A0 Action Passport, and writes revision-safe artifacts and a Run Receipt.

The accepted fixture `SRQ-COOMA-001-R1-20260904` has cutoff `2026-07-27`, valid-until `2026-12-04T23:59:59Z`, maturity `S0`, conclusion ceiling `L2`, and intervention ceiling `A0`. Hydrology remains locked:

```text
ADMISSION_BLOCKED_MISSING_RAW_RESPONSE
NOT_COMPARABLE_YET
TREND_DEFERRED
current_flow = null
```

The existing two-axis system remains authoritative: `S0–S7` describes evidence maturity; `L0–L4` describes supportable conclusion type and authority. Promotion requires new evidence or completed review, never elapsed time. Evidence stage never grants legal authority. The existing Time-Bounded Environmental Answer is revised, not replaced.

PR #115 is `PARALLEL HUMAN REVIEW / NOT MAINLINE BLOCKER`. PR #116 is `DESIGN PROVENANCE / LATER EXTRACTION OR SUPERSESSION`. Neither is changed by this Gate.

## 2. Product question and source states

> As of a declared evidence cutoff, which Cooma evidence streams are current, stale, conflicting, blocked or missing; what pattern, if any, is supportable; when must the answer be refreshed; and what A0/A1 action is proportionate?

The states are orthogonal and may coexist. They must not be implemented as one mutually exclusive freshness enum:

```yaml
availability_state: AVAILABLE | NOT_AVAILABLE | ACCESS_BLOCKED | UNKNOWN
admission_state: NOT_RETRIEVED | RETRIEVED_PENDING_VALIDATION | ADMITTED | REJECTED | ADMISSION_BLOCKED
temporal_state: NOT_EVALUATED | CURRENT_FOR_DECLARED_USE | STALE | EXPIRED | NOT_APPLICABLE_HISTORICAL_BASELINE
evidence_relation: SUPPORTING | CONFLICTING | CONTEXT_ONLY | MISSING_FOR_QUESTION | NOT_FIT_FOR_USE | UNKNOWN
evidence_role: CURRENT_OBSERVATION | HISTORICAL_BASELINE | LARGE_SCALE_CONTEXT | SPATIAL_CONTEXT | METADATA | REVIEW_GATE | MISSING_REQUIRED_LINE
```

Availability is not retrieval. Retrieval is not admission. Admission is not currency. Conflict is claim-relative, not temporal. A historical baseline can remain valid for its declared role while being inapplicable to current-condition freshness. Official status alone grants no temporal or local fitness, and a source cannot promote itself.

## 3. Evidence-source and freshness matrix

No source was contacted for this Gate. Rules below are proposed contracts, not current-condition claims.

| Stream | Provider/product and frequency | Spatial/temporal relevance and access | Repository state, freshness/expiry | S-stage and disposition |
|---|---|---|---|---|
| Cooma daily observations | BoM DWO `IDCJDW2033`, stations `070278/070217`; daily; prior HTTPS CSV, zero observed cost | Local weather context, not catchment state; product terms/retention remain binding; independent of WaterNSW but shared BoM lineage matters | `COOMA-BOM-DWO-2026-07` admitted through `2026-07-27`; current only for declared completed days; stale when a required day is absent; expire after question-specific `fresh_until`; source/station drift demotes | S0; S1 only after a valid deviation test. `REUSE`; refresh needs separate token |
| ENSO archive | BoM Southern Hemisphere archive `BOM-ENSO-MONITORING-2026-07-14`; dated outlook | Large-scale background only; no local Cooma inference; prior HTTPS receipt, zero observed cost | Admitted outlook dated `2026-07-14`, local-impact claim null; fresh to stated horizon or superseding outlook; expire when assessment window closes | S0 context only; cannot promote local pattern. `REUSE_BOUNDED_CONTEXT` |
| Mittagang historical L2 | BoM HRS station `410033`; record `1964-03-01/2024-02-29`; static baseline | Station-bounded historical comparator; exact product, digest `12740d…1534`, receipt and passport exist | `S0/L2`; valid until source digest/version, station identity, quality definitions or method change; never current by age | `REUSE`; equivalent units, timestamps, aggregation and quality treatment required |
| WaterNSW near-current | WaterNSW object `WATERNSW-410033-NEAR-CURRENT-ADMISSION-V0.1`; candidate FlowRate | Authenticated API; subscription key and exact response absent; temporal/quality semantics unresolved; possible institutional independence, measurement lineage still unproved | `ADMISSION_BLOCKED_MISSING_RAW_RESPONSE`; no digest, comparison or freshness status; any future evidence needs an observation-age rule distinct from retrieval time | L1 maximum on admission; no S1/current-flow claim before comparability and review. `DEFER_NETWORK / PRESERVE_BLOCK` |
| Registered weather metadata | BoM station directory/CDO `QGIS-SRC-006`; periodic metadata | Identity/location context; representativeness not established; terms require confirmation | `PROPOSED_METADATA_ONLY_NOT_RETRIEVED`; no freshness before retrieval/admission; expires on station metadata/site-history revision | S0 identity only. `DEFER` |
| QGIS spatial context | NSW Spatial Services locality/roads; GA SRTM DEM-S; BoM Geofabric V3.3 | Locality +10 km orientation; gauge remains station-bounded; accepted CC BY registries; committed references reusable offline | IDs `COOMA-LOCALITY`, `COOMA-TERRAIN-DEM`, `COOMA-WATERCOURSES`, `COOMA-CATCHMENTS`, `COOMA-ROADS-SETTLEMENT`; freshness tied to source version, identity, CRS, extent and transformation digest | S0 spatial fitness only. `REUSE`; presence is not flow, storage, quality or condition |
| Aerial imagery | NSW Spatial Services `NSWWebImagery`; viewport tiles | Visual orientation only; capture date unknown; online cached tiles, no bulk retention | Never current environmental evidence without dated provenance/admission | No stage promotion. `EXCLUDE_FROM_SLICE` |
| Land cover/ecology/exposure | DEA Land Cover v2.0.0 `QGIS-SRC-007`; annual candidate | 30 m land-cover class is not condition, habitat, fuel or risk; CC BY; network required | `PROPOSED_LATER_METADATA_ONLY_NOT_RETRIEVED`; no admitted ecological/exposure observations | At most S0 after admission. `DEFER` |

Rainfall, temperature, snow, flow, land cover and geometry are not interchangeable. Independence must consider publisher, measurement and processing lineage, not object count.

## 4. USE BEFORE BUILD reuse map

| Need | Reuse | EP-SKILL-002 boundary |
|---|---|---|
| Request and immutable revision | `climateos.site_reading_request.v0.1`, CLI overwrite refusal | Add refresh intent/prior reference compatibly; preserve R1 |
| Resolution/admission | EP-SKILL-001 identity checks, official receipts, WaterNSW control, QGIS registries | Freshness follows admission; retrieval is not admission |
| S/L classification | Existing S0–S7 and L0–L4 | Calculate ceilings; create no new scale |
| Answer | `climateos.time_bounded_environmental_answer.v0.1` | New immutable revision, cutoff, validity and triggers |
| Provenance | Environmental Evidence Passport and Run Receipt | Add freshness/convergence references and digests |
| Actions | PC-01/02/03/04/13 and A0 Passport | Reuse envelope; A1 requires named approval |
| Space | Accepted QGIS IDs/registries | Reassess fitness; never infer condition from presence |
| Lifecycle | Existing update, expiry, demotion and stop semantics | Make evaluation machine-readable/source-specific |

## 5. Minimum vertical slice

```text
Load EP-SKILL-001 request, prior revision and committed receipts
→ validate immutable identities and digests
→ emit one Evidence Freshness Record per source
→ classify refresh-required, blocked, missing and unusable sources
→ build a Convergence Matrix from admitted question-fit lines only
→ preserve conflicts, dependence and alternatives
→ assign S-stage and L-level ceilings without automatic promotion
→ revise the existing Time-Bounded Environmental Answer
→ emit A0 actions and separately labelled A1 candidates
→ write Passport, Receipt, review state and Founder Watch revision
```

Offline work may validate committed artifacts, test expiry with fixed clocks, issue a new fixture revision and verify determinism. It must not claim a refresh occurred. Network work requires a separate Founder token naming literal URLs/products, request count, time window, retention, licence, cost ceiling and stops. Credentials stay outside Git. Failure produces a blocked receipt and leaves the last admitted answer immutable.

## 6. Minimum object contracts

### Evidence Freshness Record

```yaml
source_object_id:
observed_at:
retrieved_at:
admitted_at:
evidence_cutoff:
evidence_role: CURRENT_OBSERVATION | HISTORICAL_BASELINE | LARGE_SCALE_CONTEXT | SPATIAL_CONTEXT | METADATA | REVIEW_GATE | MISSING_REQUIRED_LINE
availability_state: AVAILABLE | NOT_AVAILABLE | ACCESS_BLOCKED | UNKNOWN
admission_state: NOT_RETRIEVED | RETRIEVED_PENDING_VALIDATION | ADMITTED | REJECTED | ADMISSION_BLOCKED
temporal_state: NOT_EVALUATED | CURRENT_FOR_DECLARED_USE | STALE | EXPIRED | NOT_APPLICABLE_HISTORICAL_BASELINE
evidence_relation: SUPPORTING | CONFLICTING | CONTEXT_ONLY | MISSING_FOR_QUESTION | NOT_FIT_FOR_USE | UNKNOWN
fresh_until:
expiry_reason:
update_trigger:
spatial_fitness:
temporal_fitness:
review_state:
```

The three timestamps are distinct and nullable with reason. `fresh_until` is machine-readable when time-based, otherwise paired with a deterministic event rule. The five state dimensions are independently evaluated and can coexist; a record cannot promote its own source.

### Evidence Convergence Matrix

```yaml
question:
signal_or_state:
supporting_lines: []
conflicting_lines: []
blocked_lines: []
source_independence:
spatial_alignment:
temporal_alignment:
alternative_explanations: []
promotion_ceiling:
```

Empty support cannot become convergence. S2 needs persistence/repetition or independent support; S3 needs multiple partly independent lines and explicit counterevidence review.

### Refresh Plan

```yaml
source:
refresh_needed:
access_method:
network_cost_boundary:
admission_test:
failure_state:
fallback_source:
next_review_time:
```

Fallback is an alternative evidence request, never silent substitution or a changed question.

### Revised Time-Bounded Answer

Reuse `climateos.time_bounded_environmental_answer.v0.1`. A new answer has a new stable identity and explicit parent/supersedes relationship. Prior answers remain immutable.

## 7. Authority and data-access boundary

**A0 permitted in an authorised implementation:** inspect freshness; prepare evidence requests; retrieve only under separate source/network authority; validate/admit; preserve records; produce an internal watch note; request professional review.

**A1 candidate only after named human approval:** schedule a low-regret inspection; increase monitoring frequency; preserve options; communicate uncertainty internally. Each remains `NOT_AUTHORISED` until owner, scope, duration, reversibility, cost and stop are approved.

**Always prohibited:** public warning; drinking-water conclusion; drought declaration; current-flow claim without admitted evidence; engineering/regulatory direction; procurement; autonomous operations; private Council data; silent fallback; committed credentials; licence-breaking retention. Evidence stage never grants authority.

## 8. Test plan

1. Keep EP-SKILL-001 `--verify-fixture` passing.
2. Validate every freshness state and reject `AVAILABLE → CURRENT` shortcuts.
3. Test observed/retrieved/admitted separation, timezone, future/missing timestamps and event expiry.
4. Prevent stale/expired answers from being called current.
5. Fail closed on identity, digest, licence, spatial or temporal defects.
6. Test order independence, duplicates and shared-lineage scoring.
7. Prohibit promotion from one line, elapsed time, official status, QGIS presence or ENSO alone.
8. Preserve conflicts and alternatives in machine/human outputs.
9. Test S/L ceilings, A0 and unapproved A1; prohibit A2+ and public actions.
10. Test immutable lineage, deterministic fixed-clock reruns, POSIX paths and overwrite refusal.
11. Deny network/client use in offline mode.
12. For separately authorised network mode, test exact allowlist, HTTPS, redirect refusal, request/byte/cost ceilings, credential redaction, retention, timeout and blocked receipts.
13. Run targeted EP-SKILL tests and full `python -m unittest discover`; require a clean worktree.

## 9. Explicit exclusions

No implementation, data fetch, API call, scheduling, current-flow/trend conclusion, hydrology approval, QGIS modification, EP-SKILL-001 replacement, new S/L system, private Council data, PR #115/#116 change, public release or operational action is authorised here.

## 10. Founder decision options

### Option A — Bounded implementation plus small official refresh

Authorise the offline slice and a separate zero-cost, read-only token limited to:

- BoM DWO `IDCJDW2033`, stations `070278/070217`: one GET of a literal Founder-approved monthly CSV URL;
- BoM Southern Hemisphere ENSO archive: one GET of a literal Founder-approved dated archive URL;
- optional BoM HRS `410033_daily_ts.csv`: one conditional GET only when explicitly named for version checking.

The token must bind literal URLs, dates and product identities. Same-host/path redirect policy only; git-ignored raw storage; publish receipts/digests/admitted metadata only; `AUD 0`; maximum three requests; no WaterNSW, credentials, imagery or public release. Stop on identity drift, disallowed redirect, non-200, oversized/malformed content, licence ambiguity, auth/cost, provenance failure, or premature current-condition inference.

Benefit: exercises the end-to-end refresh. Risk: combines new mechanics with live-source variability.

### Option B — Offline framework only

Implement freshness, convergence, expiry and immutable revision mechanics using committed evidence/fixtures only. Network and new retrieval stay disabled. Produce Refresh Plans and blocked receipts without claiming a refresh.

Benefit: proves semantics, compatibility and fail-closed behaviour before a separate small refresh Gate.

### Option C — Hold

Retain EP-SKILL-001 and defer EP-SKILL-002. Existing expiry and hydrology blockers remain human-managed.

Benefit: no implementation risk. Cost: no reusable freshness/convergence/watch mechanics.

## 11. Recommended decision

**Option B.** It is the smallest executable batch that advances ClimateOS from a static reading to an auditable refresh-ready Watch without mixing contract work and live-source variability. It preserves the WaterNSW block, proves that BoM/ENSO/QGIS context cannot self-promote, and prepares a stable admission surface for a later separately authorised Option A trial.

## 12. Next executable work unit

Founder selected `AUTHORISE_OPTION_B`. After this Gate is merged: branch from the new `main`; add versioned Freshness/Convergence/Refresh objects by reusing EP-SKILL-001 envelopes; add a fixed-clock offline R2 fixture parented to `SRQ-COOMA-001-R1-20260904`; issue revised Answer/Passport/Receipt/Founder Watch without unsupported promotion; run targeted/full tests; open a separate Draft PR; stop before network access.

## 13. CRP harvest block

- 核心知识点：`available / retrieved / admitted / current` 不等价；官方来源也需通过问题特定的时空和新鲜度门。
- 想法点：以 Freshness Record 包围现有对象，以 Convergence Matrix 约束推理，不重建证据系统。
- 愿望点：让 Site Reading 在保留冲突、阻断和历史版本时形成可审计 Watch 修订。
- 推理点：先离线验证状态机，可分离网络不确定性与科学语义错误。
- 关键决策：推荐 B；WaterNSW 不是唯一进展路径但阻断必须保留；BoM、ENSO、QGIS 不能单独支持当前水文结论。
- 未解决问题：最终 freshness 时窗、独立性评分、WaterNSW 参数/时区/质量语义、A1 命名责任人。
- 下一步行动：Founder 选择 A/B/C；未授权前不实现、不联网、不抓取数据。
- 项目关键词：`EP-SKILL-002`, `Freshness`, `Convergence`, `Expiry`, `S0-S7`, `L0-L4`, `WaterNSW Block`, `QGIS Context`.
