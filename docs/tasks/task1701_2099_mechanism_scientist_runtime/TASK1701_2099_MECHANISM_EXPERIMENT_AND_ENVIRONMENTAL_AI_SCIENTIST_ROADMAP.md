# Task1701–2099 — Mechanism Experiment and Environmental AI Scientist Roadmap

Date: 2026-07-12
Status: Long-range founder roadmap / no implementation authorization
Project: ClimateOS / Eco-Agent-System

## Purpose

Extend ClimateOS beyond prediction and association toward controlled mechanism testing, auditable scientific evidence and, only after sufficient safeguards, a bounded Environmental AI Scientist Runtime.

## Task1701–1899 — Mechanism Experiment Layer

### Task1701–1749 — Mechanism Hypothesis Protocol

Define a standard hypothesis object:

```yaml
research_question:
hypothesis:
mechanism_chain:
expected_direction:
required_diagnostics:
alternative_explanations:
evidence_threshold:
expert_owner:
```

Rules:

- correlation is not causation;
- each mechanism link must have a diagnostic;
- incomplete evidence is a valid result;
- hypotheses require human ownership and review.

### Task1750–1799 — Numerical Experiment Contract

Define reproducible contracts for:

- baseline experiments;
- perturbation experiments;
- control and sensitivity experiments;
- model version and configuration hashes;
- input datasets and boundary conditions;
- compute environment and failure logs;
- pre-registered evidence criteria.

Candidate models may include WRF-Chem, WRF-Hydro, land-surface, ecological or energy-system models. Their inclusion requires separate scientific and licence review.

### Task1800–1849 — Mechanism Evidence Passport

Evidence states:

- `SUPPORTED`
- `PARTIALLY_SUPPORTED`
- `INCOMPLETE_EVIDENCE`
- `CONTRADICTED`
- `NOT_TESTABLE_WITH_CURRENT_OUTPUTS`
- `MODEL_FAILURE`

The passport must preserve hypothesis, experiment design, configuration, diagnostics, unsupported links, alternative explanations, uncertainty and human review.

### Task1850–1899 — Limited Atmospheric Environment Pilot

Use TianJi-Environ as an independent reference architecture for a bounded pilot, not as an automatic code dependency.

Candidate pilot:

```text
South-eastern Australian smoke / black carbon
→ radiation and vertical heating
→ boundary-layer response
→ PM2.5 persistence or transport
→ evidence and governance interpretation
```

The pilot must be small enough to audit and must not begin without data, compute, model and expert readiness.

**Deliverable:** Mechanism Experiment Layer v0.1 and one bounded evidence-chain pilot.

## Task1900–2099 — Environmental AI Scientist Runtime

### Task1900–1949 — Scientific Workflow Roles

Candidate bounded roles:

- Literature and Evidence Agent;
- Hypothesis Structuring Agent;
- Experiment Planner;
- Configuration Validator;
- Execution Agent;
- Diagnostic Agent;
- Evidence Critic;
- Human Review Coordinator.

Agents are workflow roles, not independent scientific authorities.

### Task1950–1999 — Tool and Permission Boundaries

- allowlisted scientific tools and models;
- no unrestricted configuration changes;
- mandatory pre-run validation;
- immutable experiment registration;
- compute and cost ceilings;
- safe stop and human escalation;
- no automatic publication or policy claim.

### Task2000–2049 — Closed-Loop Scientific Prototype

Demonstrate:

```text
research question
→ structured hypothesis
→ approved experiment plan
→ controlled model run
→ diagnostics
→ evidence-chain assessment
→ human-reviewed report
```

The system must be able to conclude that evidence is insufficient.

### Task2050–2099 — Scientific Governance and Readiness Review

- reproducibility audit;
- expert review process;
- model-bias and data-quality review;
- scientific claim taxonomy;
- publication and external-use boundaries;
- decision on whether any further autonomy is justified.

**Deliverable:** Environmental AI Scientist Runtime v0.1 readiness dossier, not an unrestricted autonomous scientist.

## Independent reference framework separation

TianJi-Environ is a reference for mechanism workflow architecture. It is not combined with PhysMetrics.Weather or AICON into one development item:

- PhysMetrics.Weather: model assurance reference;
- AICON: hybrid operational weather reference;
- TianJi-Environ: mechanism experiment and auditable science-workflow reference.

## Permanent reminders

> **Task1701 is the return point for Mechanism Experiment Layer design.**

> **Task1900 is the return point for Environmental AI Scientist Runtime design.**

Task1701–1710 returned on 2026-07-17 as a no-run readiness pack. Its result is
`REFERENCE_REVIEW_INCOMPLETE`: WRF 4.8.0 is candidate-locked pending a
consistent Release recheck, TianJi-Environ remains a curated-artifact reference,
and model components, data, compute and expert ownership are not admitted.
This update does not activate Task1711+, a tiny-synthetic run or any scientific
model.

At these gates, retrieve this roadmap, verify the latest TianJi-Environ work and alternative scientific-agent systems, reassess data, compute, licences and expert support, then obtain fresh Founder authorization.

## Keywords

ClimateOS; Task1701; Task1900; Task2099; TianJi-Environ; Mechanism Experiment Layer; WRF-Chem; hypothesis protocol; Numerical Experiment Contract; Mechanism Evidence Passport; Environmental AI Scientist Runtime; reproducibility; human review; scientific governance.
