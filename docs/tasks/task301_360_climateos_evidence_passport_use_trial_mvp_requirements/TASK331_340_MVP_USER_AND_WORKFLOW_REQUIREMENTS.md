# Task331-340 MVP User And Workflow Requirements

## Task331 MVP User Roles Requirements

Possible future MVP user roles:

| Role | Requirements-level responsibility | Boundary |
| --- | --- | --- |
| Founder | Reviews gates, authorizations, public-use boundaries, and sensitive escalation. | Founder authority is not delegated to automation. |
| Human reviewer | Reviews ambiguous sources, overclaim risk, conflicts, and sensitive implications. | Review does not create compliance or assurance conclusions. |
| Source analyst | Records citation metadata, source type, access date, and retrieval status. | Source analysis does not admit final evidence automatically. |
| ClimateOS assistant | Suggests classifications, summaries, risk flags, and review prompts. | Suggestions cannot replace human review or Founder Gate. |
| External reader | Reads bounded, reviewed, non-operational packets if approved. | No unreviewed operational or conclusion-bearing output. |
| Future agent | May assist only under future authorization and boundary controls. | No automatic runtime, API, MCP, n8n, or automation. |
| Archive maintainer | Maintains GitHub documentation trail and closure packets. | Archive maintenance does not authorize architecture or implementation. |

## Task332 MVP Workflow Requirements

Minimum future workflow requirements:

1. Create case.
2. Add source.
3. Classify source.
4. Extract signal.
5. Extract claim candidate.
6. Create Knowledge Object candidate.
7. Link evidence candidate.
8. Assign readiness.
9. Flag risk.
10. Request human review.
11. Escalate Founder Gate.
12. Archive output.
13. Close sprint.

This is requirements-only workflow language. It is not implementation or architecture design.

## Task333 Source Intake Requirements

Future source intake should capture:

- Source ID.
- Title.
- Publisher / institution.
- Date.
- URL / citation path.
- Access date.
- Source type.
- Language.
- Translation note if used.
- Reliability caution.
- Version or update status when available.
- Attachment support requirement.
- Public / private source distinction.
- Retrieval status.

No database is designed or authorized.

## Task334 Knowledge Object Registry Requirements

Future Knowledge Object registry requirements:

- KO ID.
- KO type.
- Linked sources.
- Linked claims.
- Linked evidence candidates.
- Readiness status.
- Risk flags.
- Review status.
- Founder Gate status.
- Archive status.
- Stop point.

No schema is created or authorized.

## Task335 Evidence Candidate Store Requirements

Future evidence candidate handling should capture:

- Candidate evidence metadata.
- Source linkage.
- Claim linkage.
- Knowledge Object linkage.
- Readiness level.
- Risk flags.
- Reviewer notes.
- Founder Gate notes.
- Archive trail.

No storage implementation is created or authorized.

## Task336 Evidence Readiness Review Requirements

Allowed readiness labels:

- Not ready.
- Candidate only.
- Needs source verification.
- Needs human review.
- Needs Founder Gate.
- Ready for architecture consideration.
- Blocked.

Requirements:

- Blocked states must preserve the reason for block.
- Human review triggers must be visible.
- Founder Gate triggers must be visible.
- Readiness labels must remain non-scoring.
- Audit trail is required for future review.

## Task337 Risk Flag Requirements

Risk flags should include:

- Political sensitivity.
- Source ambiguity.
- Outdated evidence.
- Translation risk.
- Compliance implication.
- Assurance implication.
- Certification implication.
- ESG / carbon implication.
- Framework / standards interpretation risk.
- Overclaim risk.
- Public-use risk.
- Partner-use risk.

## Task338 Human Review Queue Requirements

Future review queue requirements:

- Queue item type.
- Reason for review.
- Linked source.
- Linked claim.
- Linked Knowledge Object.
- Reviewer note.
- Decision needed.
- Stop condition.
- Archive requirement.

No queue is implemented.

## Task339 Founder Gate Requirements

Must escalate to Founder:

- Future architecture authorization.
- Any operational Evidence Passport proposal.
- Any public or partner-facing use.
- Any compliance, assurance, certification, ESG, carbon, scoring, standards, or framework conclusion risk.
- Any politically sensitive interpretation or external-use risk.
- Any future Task361-420 authorization decision.

May proceed without Founder only as documentation-only candidate tracking within the current authorized sprint boundary.

Must be blocked:

- Architecture design without separate authorization.
- Runtime or implementation without separate authorization.
- Any automatic continuation.

Founder Gate must be recorded as a governance status in future requirements material.

## Task340 Audit / Archive Requirements

Future audit and archive requirements:

- Source archive.
- Decision archive.
- Review archive.
- Founder Gate archive.
- Sprint closure archive.
- GitHub documentation trail.
- Future reproducibility.
- Index update trace.
- Commit message trace.

This is an archive requirement note only. It does not create automation.
