# Task226 Knowledge Object Lifecycle

## Purpose

Define the lifecycle of a Knowledge Object from capture to retirement.

## Lifecycle Stages

```text
Capture
-> Registration
-> Classification
-> Ownership assignment
-> Authority check
-> Readiness review
-> Mission alignment review
-> Evidence candidacy review
-> Archive
-> Retirement
```

## Allowed Operations Per Stage

| Stage | Allowed Operations |
| --- | --- |
| Capture | Record source, context, origin, and uncertainty |
| Registration | Assign identifier, owner, and review status |
| Classification | Mark source/signal/claim/knowledge category |
| Ownership assignment | Record review owner and responsibility |
| Authority check | Review source authority and limits |
| Readiness review | Assign conceptual readiness state |
| Mission alignment review | Check Mission compatibility |
| Evidence candidacy review | Consider future evidence-gate eligibility |
| Archive | Preserve traceable record |
| Retirement | Mark stale, superseded, rejected, or closed |

## Prohibited Operations Per Stage

- Capture must not interpret.
- Registration must not verify.
- Classification must not score.
- Ownership assignment must not approve evidence.
- Authority check must not certify.
- Readiness review must not create operational evidence.
- Mission alignment review must not bypass Founder authority.
- Evidence candidacy review must not operate an Evidence Passport.
- Archive must not imply current authority.
- Retirement must not delete traceability.

## Human Authority Points

Human Authority is required for:

- interpretation boundary disputes
- evidence candidacy elevation
- high-risk claims
- public communication risk
- ethical responsibility issues
- operational handoff discussions

## PRI Routing Points

PRI / Matrix may route Knowledge Objects for translation, governance review, or system placement.

PRI routing does not create evidence authority.

## Knowledge Harvest Integration Points

Knowledge Harvest may feed the lifecycle at Capture or Registration.

Harvested material still requires classification, ownership, authority, and readiness review.

## Closure And Retirement Rules

A Knowledge Object may be closed, deferred, archived, or retired when it is stale, superseded, out of scope, unsupported, unsafe, or no longer Mission-aligned.

Retirement preserves record history and does not erase review traceability.

## Boundary

This document does not implement lifecycle tracking, databases, runtime workflows, automation, or evidence operations.
