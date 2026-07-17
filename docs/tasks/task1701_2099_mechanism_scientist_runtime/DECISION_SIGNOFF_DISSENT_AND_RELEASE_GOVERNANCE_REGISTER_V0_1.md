# ClimateOS Decision Sign-off, Dissent and Release Governance Register v0.1

Date: 2026-07-18

Status: EMPTY_STATIC_REGISTER / NO_SIGNOFF / NO_RELEASE

## 1. Decision identity

Every future review decision requires a stable decision ID, immutable review
bundle revision, reviewer-role ID, consenting reviewer identity, track, exact
scope, evidence considered, exclusions, findings, limitations, state, validity
interval, revocation conditions and signature/integrity method if separately
authorized.

No signature, reviewer identity or decision instance is created here.

## 2. Controlled decision states

| State | Meaning |
|---|---|
| `NO_DECISION` | current state |
| `REVIEW_NOT_STARTED` | valid appointment/evidence bundle absent |
| `MORE_EVIDENCE_REQUIRED` | bounded gaps prevent a decision |
| `REJECTED` | evidence does not meet the track's threshold |
| `CONDITIONALLY_ACCEPTED` | exact conditions remain and release is not implied |
| `ACCEPTED_WITHIN_SCOPE` | track-specific acceptance only |
| `ABSTAINED` | reviewer cannot or should not decide |
| `RECUSED` | conflict prevents participation |
| `EXPIRED` | validity interval ended |
| `REVOKED` | decision authority withdrawn for recorded reason |

“Approved” without track, scope and state is invalid vocabulary.

## 3. Sign-off rules

- a sign-off applies only to the exact bundle revision and intended use;
- structural acceptance never implies scientific, security or licence acceptance;
- conditions must be machine- and human-readable and independently closed;
- material changes create a new bundle and invalidate automatic carry-over;
- expiry and revocation are effective states, not warning labels;
- a sign-off cannot authorize execution, access, payment, publication or contact;
- informal conversation, silence or lack of objection is not sign-off;
- signatures/integrity mechanisms require separate admission and execution gates.

## 4. Dissent and minority record

Every future disagreement remains attributable and append-only. A dissent record
must state the exact disputed finding, evidence, alternative interpretation,
materiality, requested remedy and whether the dissenter recommends rejection,
delay, narrower use or additional evidence.

Majority or Founder authority may make a governance decision but cannot erase a
scientific or security dissent. Any override must name the authority, rationale,
scope, residual risk, expiry and prohibited representations.

## 5. Quorum and aggregation

Quorum is defined per release class, never globally. A future aggregation record
must show required tracks, filled roles, independent decisions, recusals,
unresolved conditions, dissents and the exact aggregation rule.

The following always block release:

- a required track has no valid consenting reviewer;
- evidence-bundle revisions differ across decisions;
- independence or conflict disclosure is incomplete;
- security/licence/scientific rejection affects the intended use;
- conditions or material dissent are hidden or unresolved;
- the output/claim identity differs from what was reviewed;
- the proposed destination, audience or use exceeds the reviewed scope.

## 6. Release governance record

A future release record must bind:

1. exact claim/output and run-receipt identities;
2. destination, audience, purpose, format and retention;
3. all required track decisions and their current validity;
4. conditions, redactions, dissent and prohibited uses;
5. accountable release-authority role and bounded approval;
6. transfer permission, secret/network and audit requirements;
7. expiry, revocation, correction and withdrawal paths;
8. post-release incident and notification duties.

A governance record is not the transfer itself. Transfer remains independently
gated.

## 7. Empty register

| Item | Current value |
|---|---|
| real reviewer/person | none |
| consent/appointment | none |
| evidence bundle | none |
| structural/security/licence/scientific decision | none |
| dissent/override | none |
| quorum/aggregation | none |
| signature/integrity artifact | none |
| release/transfer | none |
| decision | `NO_DECISION / EMPTY_REGISTER` |

## 8. Desk check A — famous person assumed willing

Fictional request: list a well-known or previously known scientist as scientific
reviewer because they might be willing.

Decision: `REJECTED / NO_PERSON_IDENTIFIED / CONSENT_NOT_REQUESTED`.
Possible familiarity or reputation is not appointment or consent.

## 9. Desk check B — one reviewer approves everything

Fictional request: treat one structural review as security, licence, scientific
and release approval.

Decision: `REJECTED / REQUIRED_TRACKS_MISSING / RELEASE_BLOCKED`.
Track separation and scoped competence cannot be bypassed.

## 10. Desk check C — majority hides dissent

Fictional request: delete a material minority concern after a majority accepts.

Decision: `REJECTED / DISSENT_MUST_BE_PRESERVED / RELEASE_BLOCKED`.

## 11. Boundary verification

| Boundary | Result |
|---|---|
| person identified/contacted | no |
| consent/appointment/review | no |
| sign-off/signature/release | no |
| output inspection/transfer | no |
| runtime/sandbox/configuration | no |
| secret/account/network | no |
| clone/install/execute/data | no |
| resources/payment | none / AUD 0 |

## 12. Register decision

`EMPTY_REGISTER_VALID / TRACKS_SEPARATED / DISSENT_PRESERVED / NO_PERSON / NO_SIGNOFF / NO_RELEASE`

