# ClimateOS Planner Cycle Architecture Map v0.1

Status: `STATIC ARCHITECTURE / NO RUNTIME / NO LOCAL CONCLUSION`

## Purpose

The Planner Cycle is a governed reasoning chain between admitted evidence and
a human-owned decision. It must preserve the identity of facts, derivations,
interpretations, hypotheses and proposals rather than flattening them into one
confident narrative.

```text
Question + Place + Time + Authority
  -> Observe -> Retrieve -> Validate -> Build State
  -> Relationships -> Hypotheses -> Test/Simulate
  -> Risk/Opportunity -> Interventions -> Engineering Necessity
  -> Responsibility -> Rank Alternatives -> Action Passport
  -> Monitoring -> Learn
  -> revised question, evidence, method or Skill
```

This is a cycle, not an automatic pipeline. Any gate may return `STOP`,
`REQUEST_EVIDENCE`, `REQUEST_REVIEW`, `NARROW_SCOPE`, `DEMOTE` or
`SUPERSEDE`. A later stage cannot cure a failed evidence, authority,
professional-review, scale or uncertainty gate.

## Entry envelope

Every cycle begins with:

- a stable `planner_cycle_id` and revision;
- a bounded planning question;
- place and spatial-boundary identity;
- observation period, decision horizon and evidence cut-off;
- intended use and prohibited uses;
- requester, accountable human owner and decision authority;
- maximum permitted evidence stage, conclusion level and intervention class;
- applicable professional-review gates;
- budget, compute, licence, privacy and network constraints.

If question, place, time or authority is unresolved, the cycle may only produce
a scoping record or evidence request.

## Stage map

| Stage | Question answered | Input | Output | Mandatory gate / stop |
|---|---|---|---|---|
| Observe | What is present or reported? | entry envelope, admitted spatial/context objects | typed observations and unknowns | do not convert visual impression or context into measured fact |
| Retrieve | What evidence is needed for the question? | observation record, gap and intended use | purpose-bound evidence requests | stop for absent authority, licence, credential or source identity |
| Validate | Is each object fit for this named use? | candidate evidence and lineage | admission decision, limitation, max claim level | quarantine or human/professional review when required |
| Build State | What bounded environmental state is supportable? | admitted evidence only | state assertions, conflicts, missingness and validity | unresolved boundary/time/unit mismatch remains visible |
| Relationships | Which associations or dependencies are supported or proposed? | state assertions and evidence | typed relationship claims | never silently promote association to causation |
| Hypotheses | What testable explanations could account for the state? | relationships, alternatives and question | falsifiable hypothesis records | require alternatives, falsifiers and stop conditions |
| Test/Simulate | Would a test materially reduce a decision-relevant uncertainty? | hypothesis, diagnostics and authority | necessity decision; later, separately authorised test plan | `NOT_JUSTIFIED` is normal; architecture does not authorise a run |
| Risk/Opportunity | What adverse and beneficial possibilities warrant attention? | bounded state, exposure, vulnerability and uncertainty | paired risk–opportunity entries | no local risk promotion without local fitness and review |
| Interventions | What options preserve, reduce, adapt, restore or capture benefit? | risk/opportunity and objective | structured option set including no-action/monitoring | options are proposals, not recommendations or authority |
| Engineering Necessity | Is material engineering necessary and proportionate? | option set and constraints | distributed/nature-based/operational/engineering comparison | irreversible or critical action requires applicable authority |
| Responsibility | Who is affected, competent, accountable and authorised? | options, jurisdictions and stakeholders | actor–authority matrix | responsibility cannot be inferred from technical capability |
| Rank Alternatives | Which options remain preferable under declared criteria? | admissible options and authority matrix | bounded comparison with sensitivity and non-compensable gates | scores cannot override failed legal, safety, evidence or equity gates |
| Action Passport | What may a named human consider doing, and why? | complete bounded comparison and reviews | reviewable decision-support package | no automatic execution; state permitted action class |
| Monitoring | What outcome or evidence would trigger review? | Action Passport and decision record | indicators, owners, cadence, expiry and triggers | monitoring without an owner and response rule is incomplete |
| Learn | What should change after outcome review? | observations, outcome, deviations and audit | Skill Revision Record | never rewrite prior records; revisions are append-only and reviewed |

## Shared object flow

The cycle uses three distinct object families:

1. **Reality and evidence:** observation, Environmental Evidence Object,
   admission record and Environmental State assertion.
2. **Reasoning:** relationship claim, hypothesis, simulation-necessity
   decision, risk/opportunity and alternative comparison.
3. **Governance and action:** professional review, actor–authority mapping,
   Action Passport, monitoring plan and Skill revision.

Object IDs and revisions provide traceability. Narrative documents may render
these objects, but may not replace their lineage or status fields.

## Authority model

| Output class | Normal capability | Required human control |
|---|---|---|
| A0 observation/evidence request | routine supervised preparation | named cycle owner |
| A1 low-regret preparation | bounded suggestion | named human owner confirms |
| A2 operational precaution | decision support only | domain owner/professional review |
| A3 material commitment | comparison and briefing only | accountable manager and applicable professional |
| A4 critical/irreversible/statutory | evidence organisation only | external responsible authority; no Agent authorization |

Evidence maturity (`S0–S7`), conclusion level (`L0–L4`) and intervention class
(`A0–A4`) remain separate. A high evidence stage does not create legal or
professional authority.

## Hydrology branch rule

Any route that requires historical-to-near-current comparison for station
`410033` stops before relationship, risk or intervention use until H1–H8 are
completed or jointly signed by a qualified hydrology professional and returned
to Founder review. Site Reading may cite the gap and request review; it may not
infer a trend.

## First vertical slice

The recommended implementation candidate is
`EP-SKILL-001 — Cooma Site Reading v0.1`:

```text
bounded question
-> existing admitted evidence
-> typed observation
-> validation status
-> minimal Environmental State
-> evidence-gap register
-> A0-only Action Passport
-> Founder professional review
```

It excludes hazard prediction, trend comparison, option ranking, engineering
advice and public-safety advice. The slice demonstrates end-to-end provenance
and stopping behaviour rather than breadth.
