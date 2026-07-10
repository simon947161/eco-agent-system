# Task441-450 Evidence Passport Workflow Screens

This document is part of the Task421-480 ClimateOS Evidence Passport Web MVP Skeleton Sprint. It is limited to static Web MVP skeleton, screen specifications, mock data, page inventory, and prototype boundary records. It does not authorize or create runtime, backend service, production API, database schema, MCP, n8n, QCloud integration, automation, scoring, compliance guidance, assurance guidance, certification guidance, ESG/carbon conclusions, standards interpretation, framework interpretation, operational Evidence Passport, deployment, or Task481.

## Purpose

Represent the Evidence Passport workflow as human-visible static screens.

## Workflow Screens

| Screen | Purpose | Required visible warning |
| --- | --- | --- |
| Case Overview | Show the review case and workflow position. | Static review skeleton only. |
| Source Intake | Display source candidate metadata fields. | Source candidates are not verified evidence. |
| Signal Register | Display signal candidates linked to sources. | Signals do not prove outcomes. |
| Claim Candidate Register | Display provisional claim candidates. | Claims are not validated. |
| Knowledge Object Candidate Register | Display grouped candidates and traceability. | Knowledge Objects are candidates only. |
| Evidence Candidate Register | Display evidence candidate metadata. | Evidence is not admitted or operational. |
| Evidence Readiness Matrix | Display non-scoring readiness labels. | Readiness is not a score. |
| Risk Flag Matrix | Display stop controls and required handling. | Risk flags do not resolve themselves. |

## Screen Spec References

- [Screen Spec Case Overview](SCREEN_SPEC_CASE_OVERVIEW.md)
- [Screen Spec Source Intake](SCREEN_SPEC_SOURCE_INTAKE.md)
- [Screen Spec Signal Register](SCREEN_SPEC_SIGNAL_REGISTER.md)
- [Screen Spec Claim Candidate Register](SCREEN_SPEC_CLAIM_CANDIDATE_REGISTER.md)
- [Screen Spec Knowledge Object Register](SCREEN_SPEC_KNOWLEDGE_OBJECT_REGISTER.md)
- [Screen Spec Evidence Candidate Register](SCREEN_SPEC_EVIDENCE_CANDIDATE_REGISTER.md)
- [Screen Spec Evidence Readiness Matrix](SCREEN_SPEC_EVIDENCE_READINESS_MATRIX.md)
- [Screen Spec Risk Flag Matrix](SCREEN_SPEC_RISK_FLAG_MATRIX.md)

## No-Conclusion Requirement

Each screen must preserve candidate-only language and must not imply verification, evidence admission, claim validation, certification, assurance, compliance, ESG performance, carbon performance, standards interpretation, or framework interpretation.

## Task441-450 Closure

Task441-450 created screen specifications and static screen skeleton references only. No operational Evidence Passport, runtime, backend, API, database, automation, scoring, deployment, or Task481 was created.
