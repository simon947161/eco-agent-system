# Task311-320 Signal Claim Knowledge Object Trial

## Task311 Signal Register

The signal register is maintained in [SIGNAL_REGISTER.md](SIGNAL_REGISTER.md).

Required fields:

- Signal ID.
- Signal theme.
- Source link.
- Description.
- Related claim candidate.
- Evidence candidate.
- Risk flag.
- Human review need.
- Founder Gate need.
- Status.

## Task312 Claim Candidate Method

A claim candidate is a provisional statement or paraphrase discovered from a candidate source that may require future review.

Allowed claim candidate types:

- Case boundary claim candidate.
- Planning-document claim candidate.
- Climate hazard event claim candidate.
- Wetland / water condition claim candidate.
- Future city / urban resilience claim candidate.
- Source limitation claim candidate.

Forbidden conclusion types:

- Compliance conclusion.
- Assurance conclusion.
- Certification conclusion.
- ESG conclusion.
- Carbon conclusion.
- Standards interpretation.
- Framework interpretation.
- Scoring conclusion.
- Political performance conclusion.

Source quotation / paraphrase caution:

- Quotations must be limited and source-linked.
- Paraphrases must not strengthen the source beyond what the candidate record supports.
- Human review is required before future use in public, partner, or architecture-facing material.

## Task313 Claim Candidate Register

The claim candidate register is maintained in [CLAIM_CANDIDATE_REGISTER.md](CLAIM_CANDIDATE_REGISTER.md).

Required fields:

- Claim ID.
- Claim text or paraphrase.
- Source ID.
- Claim type.
- Evidence candidate link.
- Readiness status.
- Risk flag.
- Human review need.
- Founder Gate need.
- Status: provisional.

## Task314 Knowledge Object Candidate Definition

A Knowledge Object candidate in this sprint may be:

- A climate hazard signal.
- A wetland condition signal.
- A water security signal.
- A planning governance signal.
- A source cluster.
- A provisional evidence bundle.
- A review-needed object.

No Knowledge Object candidate is operational or final in this sprint.

## Task315 Knowledge Object Candidate Register

The Knowledge Object candidate register is maintained in [KNOWLEDGE_OBJECT_CANDIDATE_REGISTER.md](KNOWLEDGE_OBJECT_CANDIDATE_REGISTER.md).

Required fields:

- KO ID.
- KO name.
- KO type.
- Linked source IDs.
- Linked claim IDs.
- Evidence candidate IDs.
- Readiness status.
- Risk flags.
- Human review need.
- Founder Gate need.
- Stop point.

## Task316 Evidence Candidate Classification

The evidence candidate register is maintained in [EVIDENCE_CANDIDATE_REGISTER.md](EVIDENCE_CANDIDATE_REGISTER.md).

Required fields:

- Evidence Candidate ID.
- Source ID.
- Linked signal.
- Linked claim.
- Linked KO.
- Evidence type.
- Evidence strength caution.
- Evidence limitation.
- Readiness status.
- Human review need.
- Status: candidate only.

## Task317 Evidence Readiness Preliminary Rules

Readiness labels for this sprint:

- Not ready.
- Candidate only.
- Needs source verification.
- Needs human review.
- Needs Founder Gate.
- Ready for architecture consideration.
- Blocked.

These labels are workflow metadata only. They are not scores and do not rank sources, claims, Knowledge Objects, or evidence candidates.

## Task318 Human Review Need Register

The human review need register is maintained in [HUMAN_REVIEW_NEED_REGISTER.md](HUMAN_REVIEW_NEED_REGISTER.md).

Human review may be required due to:

- Ambiguous source.
- Outdated source.
- Potential political sensitivity.
- Potential compliance implication.
- Potential ESG / carbon implication.
- Potential standards interpretation.
- Potential overclaim.
- Source conflict.
- Missing context.

## Task319 Founder Gate Need Register

The Founder Gate need register is maintained in [FOUNDER_GATE_NEED_REGISTER.md](FOUNDER_GATE_NEED_REGISTER.md).

Founder Gate is required before any future architecture, implementation, public communication, partner-facing use, conclusion-making, operational Evidence Passport, compliance / assurance / certification language, ESG / carbon conclusion, scoring, or automatic transition.

## Task320 Interim Use Trial Summary

Tasks301-319 revealed workflow needs, not case conclusions:

- Candidate sources need explicit provenance and retrieval-status tracking.
- Source access limitations must be preserved rather than smoothed over.
- Claim candidates need separate status from source records.
- Knowledge Object candidates need linked sources, claims, evidence candidates, readiness labels, risk flags, human review needs, and Founder Gate needs.
- Readiness labels must remain non-scoring.
- Human review and Founder Gate are necessary to prevent overclaim and inappropriate public use.

No substantive conclusion is made about Xiong'an, Baiyangdian, any institution, any government, or any policy performance.
