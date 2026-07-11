# ClimateOS Design Orientation

## Purpose

This is a concise design index. It explains stable relationships and points to detailed records. It does not replace the PRD, Architecture Baseline v1.1, Domain Federation documents, Evidence Contract documents, or task closures.

## Design Position

ClimateOS is designed to translate environmental reality into traceable evidence, validation, governed deliberation, and human action.

```text
Observation
-> Evidence Candidate
-> Evidence Contract
-> Validation and Challenge
-> Human Review
-> Governance Decision
-> Action and Learning
```

## Domain Federation

ClimateOS coordinates common Mission, evidence, validation, audit, and human-responsibility rules. Domain systems retain scientific autonomy:

- WaterOS
- LandOS
- EnergyOS
- CarbonOS
- BiodiversityOS
- future approved domains

Domain outputs do not become authoritative merely because they are machine-readable.

## Alpha Runtime Concept

The future Alpha Runtime is a local-first coordination environment, not an autonomous environmental authority.

Conceptual components:

- human review interface;
- agent capability interface;
- internal application boundary;
- administrative CLI boundary;
- future bounded MCP exposure;
- Evidence Contract intake and state handling;
- domain registry;
- provider-neutral adapter boundary;
- audit, rollback, refusal, and Founder Gate records.

Task681–690 defines the architecture. Task691–700 implements only a bounded
local skeleton: in-memory Evidence Contract candidates, fixture-only domains,
human controls, deliberation records, audit, rollback, diagnostics, and a
minimal local review screen. It does not implement production capability.

## Interface Separation

- Human UI: questions, evidence review, uncertainty, consent, approval, and refusal.
- Agent Interface: bounded capability discovery, requests, evidence return, challenge, and escalation.
- Internal API: future component communication boundary.
- CLI: future administration, diagnostics, replay, and controlled maintenance.
- MCP: future agent-facing exposure only after a separate gate.

## Evidence and Deliberation

Claims, observations, model outputs, inferences, values, decisions, and actions remain separate record types. ClimateOS must support counter-evidence, uncertainty, abstention, refusal, and escalation rather than automatic agreement.

## Trust Boundary

No external provider, model, agent, or private engine is trusted solely by identity. Trust depends on provenance, scope, version, assumptions, uncertainty, validation state, permissions, and human responsibility.

Cryptographic integrity can show whether content changed; it does not prove scientific truth.

## Implemented / Planned / Vision

- Implemented: repository governance, documentation foundations, static
  skeleton, bounded local controlled prototype and hardening, and a local
  in-memory Alpha Runtime Skeleton.
- Planned: durable governed Alpha state, approved interfaces, domain adapters,
  stronger security controls, and deliberation workflow maturity.
- Vision: mature multi-domain ClimateOS supporting institutions, Sustainable Offices, communities, and individuals.

## Private Asset Boundary

Founder-reserved EcoEngine and `D:\eco_engine_v200` remain outside this design. Only a neutral future private-extension boundary may be discussed until separate Founder authorization.

## Authoritative References

- `PRD.md`
- `AGENTS.md`
- `MASTER_DIRECTORY_MAP.md`
- `PROJECT_INDEX.md`
- Architecture Baseline v1.1 freeze record
- Task601–620 Domain Federation and Life System foundation
- Task631–640 Evidence Contract examples
- Task651–660 Alpha Runtime Decision Brief
- Task671–680 External Model Adapter Readiness Review
- Task681–690 Alpha Runtime Architecture Brief

When conflicts occur, the latest committed Founder-approved governance record and frozen architecture baseline prevail.
