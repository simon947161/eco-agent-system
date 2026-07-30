# Early-Warning Evidence Maturity Standard v0.1

## Two-axis rule

ClimateOS must not replace the existing L0–L4 conclusion protocol. It adds a
second axis:

- **Conclusion level (L0–L4):** what type and authority of statement is
  supportable;
- **Evidence maturity stage (S0–S7):** how an evolving signal has developed
  over time.

An assessment may be `S3/L2`, for example: evidence is converging and a
reproducible descriptive local indicator is supportable. It is not yet a
reviewed L3 assessment or public warning.

## Evidence maturity stages

| Stage | Name | Minimum condition | Default output |
|---|---|---|---|
| S0 | `BASELINE_MONITORING` | admitted sources and baseline exist | monitoring record |
| S1 | `SIGNAL_DETECTED` | one valid deviation or model signal | internal observation |
| S2 | `EMERGING_PATTERN` | persistence, repetition or a second supporting line | watch note with expiry |
| S3 | `EVIDENCE_CONVERGING` | multiple partly independent lines; key conflicts visible | bounded assessment candidate |
| S4 | `LOCAL_RISK_ELEVATED` | local translation, exposure and consequence pass review | local risk assessment |
| S5 | `INTERVENTION_WINDOW_OPEN` | action lead time matters and proportional action passes authority gate | action/monitoring brief |
| S6 | `OFFICIAL_CONFIRMATION_OR_EQUIVALENT` | relevant institution issues a dated conclusion, or qualified review reaches equivalent declared state | evidence update, not automatic override |
| S7 | `RETROSPECTIVE_VALIDATION` | outcome period closes and evidence is available | skill, error and learning record |

S6 is not always reached and is not always after S5. An official statement can
arrive earlier, later or never. It must be assessed for scope and local fitness.

## Mandatory dimensions

Every S1+ object records:

- observation strength;
- source independence;
- model agreement and disagreement;
- spatial relevance;
- temporal relevance and lead time;
- causal uncertainty and alternatives;
- local exposure and vulnerability;
- consequence severity;
- false-positive and false-negative costs;
- action reversibility and cost;
- human-review status;
- evidence cut-off, validity and expiry;
- update, escalation, demotion and stop triggers.

## Promotion rules

Promotion requires new evidence or completed review, not elapsed time alone.

- S1 → S2: persistence, recurrence or independent support;
- S2 → S3: triangulation plus explicit counterevidence review;
- S3 → S4: local mechanism, exposure and boundary established;
- S4 → S5: decision window, action owner and proportionality established;
- any stage → S6: official statement admitted with scope and date;
- assessment period → S7: outcome evidence and retrospective review.

Any stage may be demoted for expiry, source correction, model failure,
contradiction, boundary change or loss of local relevance.

## Intervention classes

| Class | Examples | Earliest normal stage | Authority |
|---|---|---|---|
| A0 Observe | refresh evidence, check sensor, inspect map | S1 | routine supervised workflow |
| A1 Low-regret prepare | schedule inspection, preserve options, communicate uncertainty internally | S2/S3 | named human owner |
| A2 Operational precaution | adjust reversible maintenance planning, increase monitoring | S3/S4 | domain owner review |
| A3 Material commitment | procurement, major operations change, public-facing advice | S4/S5 | accountable manager/professional |
| A4 Critical/irreversible | engineering, statutory, emergency or public-safety direction | normally L4 and applicable authority | external responsible authority |

The stage never grants legal authority by itself.

## Communication rule

Every message must state:

- “what we see”;
- “what it might mean”;
- “what evidence disagrees or is missing”;
- “how long this answer is valid”;
- “what low-regret action is proportionate now”;
- “what would change or stop the assessment”.

