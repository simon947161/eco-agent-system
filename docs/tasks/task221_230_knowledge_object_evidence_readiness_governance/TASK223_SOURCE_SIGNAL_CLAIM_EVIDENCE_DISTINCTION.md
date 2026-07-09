# Task223 Source Signal Claim Evidence Distinction

## Purpose

Establish clear distinctions between source, signal, claim, Knowledge Object, Evidence Candidate, Evidence-Ready Object, and Operational Evidence.

## Definitions

| Type | Definition | Current Batch Status |
| --- | --- | --- |
| Source | An origin record, document, observation, publication, conversation, dataset, or authority location. | May be referenced as metadata |
| Signal | A possible input that may matter to ClimateOS. | May be captured conceptually |
| Claim | A statement that asserts something about reality, meaning, performance, compliance, carbon, ESG, or governance. | May be registered as requiring review |
| Knowledge Object | A governed unit of knowledge with provenance, maturity, uncertainty, and routing state. | May be defined conceptually |
| Evidence Candidate | A Knowledge Object or claim package that may later be reviewed for evidence readiness. | Future review category only |
| Evidence-Ready Object | A reviewed object that satisfies future admission criteria but is not yet operational evidence. | Future-state readiness category only |
| Operational Evidence | Evidence admitted for use in an authorized operational Evidence Passport or runtime process. | Not authorized in this batch |

## Transition Rules

- A Source may produce a Signal.
- A Signal may become a Claim or Knowledge Object candidate.
- A Claim requires review before any evidence status.
- A Knowledge Object may become an Evidence Candidate only after governance review.
- An Evidence Candidate may become Evidence-Ready only after admission-gate review.
- Operational Evidence requires future Evidence Passport / Runtime authorization.

## Prohibited Shortcuts

- Source to Operational Evidence.
- Signal to conclusion.
- Claim to compliance guidance.
- Knowledge Object to evidence without admission.
- Evidence Candidate to operational use.
- Evidence-Ready Object to runtime use without future authorization.

## Operational Evidence Future-State Notice

Operational Evidence is future-state only.

Task221-230 does not admit, create, operate, or use Operational Evidence.

## Boundary

This document defines distinctions only. It does not create evidence records, runtime evidence processes, scoring, verification, or claim review operations.
