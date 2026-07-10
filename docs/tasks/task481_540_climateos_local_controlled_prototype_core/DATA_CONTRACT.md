# Data Contract

All records use the boundary label:

```text
Prototype / Candidate / Non-Operational
```

## Candidate Record Types

- `source_candidate`
- `signal_candidate`
- `claim_candidate`
- `knowledge_object_candidate`
- `evidence_candidate`

## Permitted Candidate Statuses

- Draft Candidate.
- Needs Source Verification.
- Needs Translation Review.
- Needs Human Review.
- Blocked.
- Founder Gate Required.
- Human-Reviewed Candidate.
- Archived.
- Superseded.

## Prohibited Status Meanings

The prototype must not create or imply:

- Certified.
- Assured.
- Compliant.
- Final Truth.
- Officially Verified.
- Approved ESG Performance.
- Verified Carbon Outcome.
- Regulatory Acceptance.

## Relationship Model

Relationships link candidate records with:

- source candidate to signal candidate;
- source candidate to claim candidate;
- claim candidate to Knowledge Object candidate;
- evidence candidate to claim candidate;
- risk or review cluster to related candidates.

Every relationship requires a creator label and reason.

## Human Review Transition Model

Sensitive status transitions require:

- record identifier;
- previous status;
- new status;
- timestamp;
- reviewer label;
- review reason;
- linked risk flags where applicable;
- Founder Gate trigger where applicable.

No model suggestion or workflow rule may mark itself as human review.

## Founder Gate Record Model

Founder Gate records include:

- gate trigger;
- affected records;
- decision date;
- decision status;
- Founder instruction text;
- scope allowed;
- scope prohibited;
- review or expiry requirement;
- archive reference.

No route, model output, database trigger, or test fixture may automatically pass the Founder Gate.

## Audit Event Model

Audit events record:

- event type;
- actor type;
- actor label;
- linked record;
- detail JSON;
- timestamp.

Audit events are traceability metadata only. They are not legal assurance, certification, compliance records, blockchain entries, or Evidence Assets.
