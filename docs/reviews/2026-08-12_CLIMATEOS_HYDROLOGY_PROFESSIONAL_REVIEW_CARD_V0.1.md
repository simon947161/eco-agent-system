# ClimateOS Hydrology Professional Review Card v0.1

**Review object:** Mittagang / station `410033` historical–near-current streamflow comparability  
**Date prepared:** 2026-08-12  
**Authority baseline:** `main@4b1ae90fc02db4a32df3296c3a133f1999a9b3e7`  
**Document state:** `REVIEW INSTRUMENT READY / PROFESSIONAL SIGN-OFF PENDING`  
**Maximum present authority:** `S0 / L1`  
**Comparison state:** `NOT_COMPARABLE_YET`  
**Trend state:** `DEFERRED_PENDING_QUALIFIED_HYDROLOGY_REVIEW`

## 1. Purpose

This card converts the existing Task2111–2130 evidence controls into a bounded
professional hydrology review. It is a decision instrument, not a hydrological
finding.

The review asks one narrow question:

> Can the admitted historical daily-flow series and the reported WaterNSW
> near-current `FlowRate` record for station `410033` be compared for a
> specified analytical purpose without changing the meaning of either record?

This card does not authorise data retrieval, API use, new modelling, trend
analysis, current-condition classification, operational advice, engineering
design, or publication of a local safety conclusion.

## 2. Evidence currently before the reviewer

### 2.1 Repository-controlled evidence

- Task2091–2100: bounded official historical-flow intake;
- Task2101–2110: Founder-accepted `S0/L2` historical descriptive baseline,
  with formal trend deferred;
- Task2111–2120: eight-dimension near-current comparability gate;
- Task2121–2130: exact-response admission control;
- current gate result: `NOT_COMPARABLE_YET`;
- current near-current admission result:
  `ADMISSION_BLOCKED_MISSING_RAW_RESPONSE`.

### 2.2 User-observed near-current summary

The following is a copied observation summary, not admitted raw evidence:

| Field | Reported value |
|---|---|
| siteId | `410033` |
| timeStamp | `28-Jul-2026 09:00` |
| variableName | `FlowRate` |
| value | `198.639` |
| unitOfMeasure | `ML/day` |
| qualityCode | `125` |
| reported quality label | `Auto QC - Passed` |

It may guide the review questions, but it must not be substituted for the exact
response body or used to generate comparison statistics.

## 3. Reviewer eligibility and independence

The review should be completed or countersigned by a person with demonstrable
competence in hydrometric data interpretation, catchment hydrology, or closely
related professional practice.

Record:

| Field | Entry |
|---|---|
| Reviewer name | |
| Qualification / professional standing | |
| Relevant hydrology or hydrometric experience | |
| Organisation | |
| Conflicts or limitations | |
| Review date | |
| Evidence version / commit reviewed | |

The reviewer is asked to assess measurement meaning and analytical
comparability. They are not asked to endorse ClimateOS, approve a public
warning, or certify drinking-water, infrastructure, flood, fire, wastewater, or
public-safety conditions.

## 4. Permitted review statuses

Each item must receive exactly one status:

- `PASS` — supported by cited evidence and adequate for the stated purpose;
- `CONDITIONAL` — usable only under explicit transformation or limitation;
- `FAIL` — the two records do not support the proposed comparison;
- `UNRESOLVED` — evidence is missing or insufficient;
- `NOT_APPLICABLE` — justified for the specified comparison purpose.

A blank field is not a pass. If any critical item is `FAIL` or `UNRESOLVED`,
the overall default remains `NOT_COMPARABLE_YET`.

## 5. Eight-dimension professional comparability review

### H1 — Station identity and continuity — CRITICAL

Confirm whether both records refer to the same hydrometric site and whether
station identity, location, datum, control, instrumentation, rating relationship
or station history changed in a way material to the proposed comparison.

| Check | Status | Evidence / citation | Reviewer reasoning |
|---|---|---|---|
| Identifier `410033` resolves to the same site | | | |
| Coordinates and named watercourse/catchment agree | | | |
| Relocation, datum, control or instrumentation history assessed | | | |
| Rating-curve or station-history discontinuities assessed | | | |

**Pass criterion:** same site and no unaccounted material discontinuity.  
**Failure consequence:** no direct comparison; split into defensible eras or
stop.

### H2 — Variable and measurement semantics — CRITICAL

Determine what `FlowRate` means operationally: instantaneous discharge,
derived discharge, rolling value, daily mean, end-of-period value, or another
product. Confirm how the historical daily-flow variable was constructed.

| Check | Status | Evidence / citation | Reviewer reasoning |
|---|---|---|---|
| Near-current `FlowRate` definition established | | | |
| Historical variable definition established | | | |
| Stage-to-discharge derivation and rating treatment assessed | | | |
| Provisional, corrected or published status distinguished | | | |

**Pass criterion:** the measurements express the same hydrological quantity, or
a scientifically justified transformation is specified.  
**Failure consequence:** values must not share a percentile, anomaly, trend, or
“high/normal/low” comparison.

### H3 — Temporal support and aggregation — CRITICAL

Identify the observation interval and aggregation operator for each record.

| Check | Status | Evidence / citation | Reviewer reasoning |
|---|---|---|---|
| Near-current sampling interval known | | | |
| Historical daily aggregation operator known | | | |
| Instantaneous versus mean/total distinction resolved | | | |
| Missing-subinterval and completeness rules known | | | |

**Pass criterion:** temporal support is equivalent, or the near-current series
can be validly aggregated before comparison.  
**Failure consequence:** a single 09:00 value must not be compared directly
with historical daily values.

### H4 — Time zone, daylight saving and day boundary — CRITICAL

| Check | Status | Evidence / citation | Reviewer reasoning |
|---|---|---|---|
| Timestamp time zone established | | | |
| AEST/AEDT handling established | | | |
| Historical daily boundary established | | | |
| Duplicate/missing DST interval treatment established | | | |

**Pass criterion:** both records can be assigned to an equivalent hydrological
day without ambiguity.  
**Failure consequence:** no date-aligned daily comparison.

### H5 — Units, precision and conversion — CRITICAL

Confirm that `ML/day` is a rate representation and not a daily accumulated
volume in the relevant products. Record any conversion to `m³/s` or other
units, including constants and rounding.

| Check | Status | Evidence / citation | Reviewer reasoning |
|---|---|---|---|
| Dimensional meaning of both units confirmed | | | |
| Conversion formula and precision recorded | | | |
| Rounding/significant-figure effects assessed | | | |

**Pass criterion:** dimensions and conversions are equivalent and reproducible.  
**Failure consequence:** no numerical comparison.

### H6 — Quality codes and data revision state — CRITICAL

Establish the official meaning and scope of quality code `125`, including
whether “Auto QC - Passed” represents automated screening only and whether the
record remains provisional or may later be revised. Map it cautiously to the
historical quality scheme; do not infer equivalence from similar labels.

| Check | Status | Evidence / citation | Reviewer reasoning |
|---|---|---|---|
| Official definition of code `125` established | | | |
| Automated versus professional validation distinguished | | | |
| Provisional/revision status established | | | |
| Cross-scheme quality equivalence justified | | | |

**Pass criterion:** both records meet the quality threshold required for the
stated analytical purpose.  
**Failure consequence:** exclude, quarantine, or use only in a sensitivity
analysis explicitly labelled as provisional.

### H7 — Record completeness, censoring and hydrological regime

Assess missing data, zero-flow encoding, censoring, rating extrapolation,
backwater/ice/vegetation effects where relevant, flood-range uncertainty, and
whether the historical reference window is representative for the proposed
question.

| Check | Status | Evidence / citation | Reviewer reasoning |
|---|---|---|---|
| Missingness and gap rules assessed | | | |
| Zero/censored/out-of-range values assessed | | | |
| Rating extrapolation and extreme-flow uncertainty assessed | | | |
| Reference-period suitability assessed | | | |

**Pass criterion:** known defects do not bias the proposed statistic beyond an
explicit tolerance.  
**Failure consequence:** restrict the statistic, change the reference period,
apply a defensible uncertainty treatment, or stop.

### H8 — Spatial and decision-purpose representativeness

Confirm what geographic question this gauge can answer. A station observation
does not automatically represent all of Cooma, water supply, drinking-water
quality, urban drainage, wastewater systems, fire conditions, or downstream
asset risk.

| Check | Status | Evidence / citation | Reviewer reasoning |
|---|---|---|---|
| Contributing catchment and gauge location understood | | | |
| Upstream regulation/diversion/abstraction assessed | | | |
| Spatial transfer to the target place justified | | | |
| Intended decision and required accuracy stated | | | |

**Pass criterion:** the station is representative for one expressly bounded
question and spatial extent.  
**Failure consequence:** narrow the question or obtain other evidence; do not
generalise.

## 6. Comparison-purpose declaration

Comparability is purpose-specific. Complete this before making a final
recommendation.

| Field | Entry |
|---|---|
| Proposed question | |
| Target spatial extent | |
| Target time scale | |
| Proposed statistic / model | |
| Required accuracy | |
| Acceptable uncertainty | |
| Intended user and decision | |
| Explicitly excluded interpretations | |

A record pair may be comparable for descriptive plotting but not for percentile
classification, trend estimation, event attribution, design flow estimation,
forecast verification, or operational decision-making.

## 7. Overall professional determination

Select one:

- [ ] `NOT_COMPARABLE_YET`
- [ ] `COMPARABLE_FOR_NAMED_PURPOSE_ONLY`
- [ ] `COMPARABLE_AFTER_SPECIFIED_TRANSFORMATION`
- [ ] `NOT_COMPARABLE_FOR_PROPOSED_PURPOSE`

Record:

| Field | Entry |
|---|---|
| Determination | |
| Named permitted purpose | |
| Required transformation | |
| Required exclusions | |
| Residual uncertainty | |
| Earliest evidence-maturity stage supported | |
| Maximum conclusion level supported | |
| Re-review trigger | |

### Mandatory logic

1. No exact near-current response and retrieval receipt means the record remains
   a summary, not admitted raw evidence.
2. No H2–H6 critical pass means no numerical historical–near-current comparison.
3. A professional comparability determination does not itself establish a
   trend, cause, forecast, risk level, intervention need, or public warning.
4. Official confirmation is evidence-maturity stage `S6`, not the only route
   by which earlier signals may be examined. Earlier work must still remain
   proportionate to evidence and authority.
5. Any output above the approved conclusion level must return to Human Review /
   Founder Gate.

## 8. Allowed outputs after review

| Overall result | Maximum permitted output |
|---|---|
| `NOT_COMPARABLE_YET` | gap register and evidence request only |
| `COMPARABLE_FOR_NAMED_PURPOSE_ONLY` | bounded descriptive comparison for that purpose |
| `COMPARABLE_AFTER_SPECIFIED_TRANSFORMATION` | transformed comparison plus method, uncertainty and audit trail |
| `NOT_COMPARABLE_FOR_PROPOSED_PURPOSE` | documented refusal and alternative evidence plan |

None of these outcomes authorises drinking-water, supply sufficiency, flood
safety, wastewater, fire, engineering, emergency-management, or other public
safety conclusions.

## 9. Evidence-gap and action register

This register requests evidence; it does not authorise an API call.

| ID | Missing evidence / question | Why material | Owner | Permitted acquisition route | Stop condition | Status |
|---|---|---|---|---|---|---|
| G1 | Exact near-current response and retrieval receipt | provenance and content identity | | separately authorised retrieval or supplied record | no credentials / no authority | OPEN |
| G2 | Official `FlowRate` product semantics | H2/H3 | | official metadata or provider clarification | ambiguity remains | OPEN |
| G3 | Station metadata and change history | H1 | | official station documentation | discontinuity unresolved | OPEN |
| G4 | Time zone and hydrological day rule | H4 | | official metadata | rule unresolved | OPEN |
| G5 | Official quality code `125` definition and revision status | H6 | | official quality documentation | crosswalk unsupported | OPEN |
| G6 | Historical quality/missingness/rating metadata | H6/H7 | | admitted historical metadata | bias cannot be bounded | OPEN |
| G7 | Catchment and decision-purpose boundary | H8 | | QGIS/site/catchment evidence under separate scope | spatial transfer unjustified | OPEN |

## 10. Placement inside Environmental Planning Intelligence

### 10.1 Core object

ClimateOS should increasingly encode **Environmental Planning Intelligence**:
the repeatable professional capacity to observe a place, validate evidence,
reason across terrain, water, land, infrastructure, people and assets, compare
interventions, allocate responsibility, act under authority, monitor outcomes,
and revise the judgement.

The long-term engineering objective is:

> A human-governed Environmental OS for Agents that can safely reproduce
> validated environmental-planning methods at many locations without
> reproducing unsupported conclusions at scale.

Weather, GIS, hydrology, CFD, SWMM, HEC-RAS, remote sensing, AI models, Evidence
Passport, Admission Control, Mission Control and local execution nodes are
tools or organs. They are not the final professional capability.

### 10.2 Missing middle layer

The architectural gap is the **Environmental Planning Reasoning Runtime
(EPRR)**:

```text
Evidence → EPRR → Action
```

EPRR must tell an agent:

- where it is and what question it is answering;
- what has been observed and at what evidence/conclusion level;
- which relationships are established, hypothesised or unknown;
- what evidence or model is justified next;
- which actions are permitted, prohibited or require human authority;
- who may be affected and how the outcome will be verified.

This hydrology review card is an early EPRR component: it converts professional
hydrometric judgement into an auditable stop/go/limit protocol.

## 11. Environmental Planner → Agent Skill pilot

### 11.1 Pilot

`Cooma Environmental Planning Intelligence / Planner Skill v0.1`

The pilot should test whether one complete, real environmental-planning process
can be made repeatable before ClimateOS expands its data-source inventory.

### 11.2 Required workflow

1. Observe.
2. Retrieve already-authorised evidence.
3. Validate evidence.
4. Build a bounded environmental model.
5. Identify relationships.
6. Generate hypotheses.
7. Test or simulate only where justified.
8. Identify risks and opportunities without exceeding authority.
9. Generate distributed interventions.
10. Apply an engineering-necessity test.
11. Allocate responsibility.
12. Rank alternatives.
13. Produce an Action Passport.
14. State uncertainty and prohibited interpretations.
15. Define monitoring.
16. Learn from outcomes.

### 11.3 Hydrology card as a Skill gate

Within that workflow, this card sits between steps 3 and 4:

```text
Observed water record
  → Evidence Passport / Admission Control
  → Hydrology Professional Review Card
  → bounded relationship or model
  → planning hypotheses
```

If this card returns `NOT_COMPARABLE_YET`, the Planner Skill must request
evidence or narrow the question. It must not silently substitute professional
judgement with a calculation.

### 11.4 Founder Gate

The pilot's Founder Gate is not visual polish. It asks:

> If this were submitted by a newly qualified environmental planner, does the
> work show a defensible understanding of the place and a professionally useful
> proposal worthy of further action?

A `YES` does not authorise reality-changing action. It permits the Skill to
advance to the next governed validation stage.

## 12. Initial Environmental Planning Skill Registry

The first proposed sequence is:

| ID | Skill | Core question |
|---|---|---|
| EP-SKILL-001 | Site Reading | What is this place and what is materially present? |
| EP-SKILL-002 | Terrain Reasoning | Where are slopes, divides, low points and accumulation paths? |
| EP-SKILL-003 | Water Path Reasoning | Where does water originate, move, store and leave? |
| EP-SKILL-004 | Land Surface Assessment | How do cover, soil, vegetation and hard surfaces alter processes? |
| EP-SKILL-005 | Urban Flood Planning | How do hazard, exposure, drainage and land form interact? |
| EP-SKILL-006 | Heat Mitigation Planning | Where and for whom is heat produced, retained and reduced? |
| EP-SKILL-007 | Catchment Planning | Which upstream–downstream relationships govern the problem? |
| EP-SKILL-008 | Blue-Green Infrastructure | Which ecological functions can deliver planning value? |
| EP-SKILL-009 | Distributed Intervention Design | Can action be distributed near sources and pathways? |
| EP-SKILL-010 | Engineering Necessity Test | Is large centralised engineering actually necessary? |

Each Skill must include evidence inputs, admission rules, reasoning steps,
uncertainty, refusal conditions, authority boundaries, audit outputs,
monitoring, and a learning loop.

## 13. Hazard-to-Benefit (H2B) protocol

For any hazard-related planning problem, the Planner Skill should ask:

1. **What must be prevented?** Identify unacceptable harm to life, housing,
   essential services, access, ecosystems and other protected values.
2. **What natural function should be preserved or harvested?** Identify useful
   water, sediment, ecological renewal, cooling, recharge or other functions
   without romanticising the hazard.

The intervention sequence should test, in order:

1. source reduction;
2. distributed detention;
3. infiltration where suitable;
4. storage and beneficial reuse;
5. restoration of natural pathways and functions;
6. land-use or exposure adjustment;
7. only then, justified centralised engineering protection.

This is a planning protocol, not a predetermined answer. Each step remains
subject to site evidence, unintended-consequence review and authority.

## 14. Human-governed agent structure

| Level | Role | Authority boundary |
|---|---|---|
| L0 Observer Agent | observes weather, water, land and sensors | no interpretation beyond admitted observations |
| L1 Evidence Agent | checks source, conflict, quality and uncertainty | no planning or real-world action |
| L2 Planning Agent | runs validated planning Skills and alternatives | proposals only |
| L3 Coordination Agent | compares local, council, catchment and regional responsibilities | coordination proposals; no unilateral allocation of legal duty |
| L4 Governance Agent | tests policy, fairness, conflict and consequences | recommendation only; major action enters Human Authority |

This is not a “super-AI” hierarchy. Local agents should be coordinated through
catchment, regional and planetary evidence layers so that upstream or local
actions are tested for downstream and cross-boundary consequences.

## 15. Strategic development rule

Before adding a model, API, data source, dashboard or Agent, ask:

> Does this materially improve ClimateOS's ability to complete one governed,
> evidence-backed environmental-planning action?

If not, it should not displace the current mainline.

The first proof remains Cooma. After the Cooma Planner Skill is validated, a
2026 Shanghai extreme-rainfall reference event may be considered as a separate
cross-scale stress test. That later test requires its own evidence intake,
authority and review; this card does not initiate it.

## 16. Reviewer attestation

> I reviewed the cited evidence for the stated comparison purpose. My
> determination is limited to hydrometric comparability and does not certify a
> trend, causal attribution, forecast, intervention, operational condition or
> public-safety conclusion.

| Field | Entry |
|---|---|
| Reviewer signature / recorded approval | |
| Date | |
| Determination | |
| Conditions | |
| Recommended next gate | |

## 17. CRP — strategic record

- **核心知识点：** ClimateOS的核心对象从数据与模型提升为
  `Environmental Planning Intelligence`；本卡把水文学专业判断编码为
  EPRR中的可审计门。
- **想法点：** EPRR、Planner Skill Registry、H2B、五级Agent结构和
  Planetary Environmental Agent Network。
- **愿望点：** 将一个成熟环境规划师的方法转化为可由许多Agent安全调用、
  仍由人类治理的公共专业能力。
- **推理点：** Evidence、Hydrology、QGIS、Forecast、Mission Control和
  Runtime是器官；缺失层是 `Evidence → Professional Reasoning → Action`。
- **关键决策：** 不扩张API主线；先完成水文学专业复核，再进入首个
  `Environmental Planner → Agent Skill`闭环。
- **首个验证场景：** Cooma。
- **未解决问题：** H1–H8专业签署、Skill评价标准、跨地域责任、仿真调用、
  物理反馈、Agent权限与现实行动边界。
- **下一步行动：** 由合格水文学专业人员填写本卡；在通过前保持
  `NOT_COMPARABLE_YET`。之后另立Founder Gate决定是否启动
  `Cooma Environmental Planning Intelligence / Planner Skill v0.1`。
- **项目关键词：** `ClimateOS`, `410033`, `Hydrology Review`,
  `Environmental Planning Intelligence`, `EPRR`, `Planner Skill`,
  `Evidence Passport`, `H2B`, `Cooma`, `Shanghai`,
  `Distributed Intervention`, `Planetary Agent Network`.
