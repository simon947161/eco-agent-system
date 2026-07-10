# Risk Flag Workflow Concept

This document is part of the Task361-420 ClimateOS MVP Architecture v0.1 and Prototype Planning Sprint. It is architecture documentation and prototype planning only. It does not authorize or create runtime, implementation, API, database, MCP, automation, scoring, compliance, assurance, certification, ESG/carbon conclusions, standards interpretation, framework interpretation, operational Evidence Passport, deployment, or Task421.

## Purpose

Risk flags stop or escalate unsafe movement from candidate records toward conclusions, runtime, or implementation.

## Risk Flags

| Risk flag | Architectural treatment |
| --- | --- |
| Source verification risk | Stop before final evidence. |
| Translation / language risk | Require human review. |
| Political sensitivity risk | Require human review and possibly Founder Gate. |
| Compliance / ESG overclaim risk | Block conclusion language. |
| Standards / framework interpretation risk | Stop and defer. |
| Timeliness risk | Require freshness review. |
| News-source caution risk | Treat as event discovery only. |
| Runtime creep risk | Stop before execution work. |

## Boundary

Risk flags are not scores and do not resolve themselves.
