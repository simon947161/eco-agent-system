# ClimateOS Human Review Role, Independence and Conflict Contract v0.1

Date: 2026-07-18

Status: STATIC_CONTRACT / ROLE_ONLY / NO_PERSON / NO_REVIEW

## 1. Role before person

ClimateOS first defines the review responsibility, evidence and independence
requirements. A real person may fill a role only after separate identification,
consent, competence verification, conflict disclosure and authorization.

Prior conversation about a possible scientist or professional contact is not
consent, appointment, availability, competence evidence or endorsement. No real
person is named or inferred in this contract.

## 2. Review-track separation

| Track | Bounded question | Cannot decide alone |
|---|---|---|
| structural | are required identities, fields and records complete? | scientific validity or release |
| security | are supply-chain, permission, secret and containment risks addressed? | licence or scientific meaning |
| licence | is the intended access, transformation and distribution permitted? | technical safety or scientific validity |
| scientific | are method, evidence, uncertainty and claim scope defensible? | security, licence or publication authority |
| release governance | are all required decisions present for an exact audience/use? | substitute for any missing track |

One reviewer may not collapse tracks merely because they hold more than one
role. Each decision must retain its own scope, evidence and limitations.

## 3. Reviewer-role identity

Every future role record requires:

1. stable `review_role_id` and immutable revision;
2. exact track, question, claim/output scope and prohibited decisions;
3. required competence and evidence of current suitability;
4. independence threshold and reporting relationship constraints;
5. conflict categories and disclosure requirements;
6. confidentiality, data-access and retention boundary;
7. expected effort, timing and compensation status;
8. consent status, start/expiry and withdrawal path;
9. accountable appointing authority;
10. replacement and vacancy procedure.

These are future metadata fields only. No role is assigned here.

## 4. Consent states

| State | Meaning |
|---|---|
| `NO_PERSON_IDENTIFIED` | current state |
| `ROLE_DEFINED_UNFILLED` | responsibilities exist without a person |
| `CANDIDATE_NOT_CONTACTED` | identity separately authorized but no outreach |
| `CONSENT_NOT_REQUESTED` | no invitation has been sent |
| `CONSENT_PENDING` | explicit response absent |
| `CONSENT_DECLINED` | person must not be represented as reviewer |
| `CONSENT_WITHDRAWN` | role authority ends; prior records remain attributed |
| `APPOINTED_TIME_BOUNDED` | future explicit appointment with scope/expiry |

Task1781–1790 uses `NO_PERSON_IDENTIFIED / ROLE_DEFINED_UNFILLED` only.

## 5. Competence evidence

A future appointment must record track-relevant education or experience,
familiarity with the specific method and jurisdiction, recency, limitations,
availability, and whether specialist support is required. Reputation, employer,
title, friendship or past contact alone is insufficient.

The scientific track must be matched to the exact claims. Wind-energy project
development knowledge, atmospheric modelling, measurement uncertainty,
software security, data governance and licensing are distinct competencies.

## 6. Independence and conflicts

Conflicts to disclose include financial interests, employment or advisory
relationships, project advocacy/opposition, authorship, tool/vendor interests,
personal relationships, prior public commitments and decision authority over
the work being reviewed.

Possible future states are:

- `NO_CONFLICT_DECLARED_WITH_EVIDENCE`;
- `CONFLICT_DISCLOSED_MANAGEABLE`;
- `CONFLICT_DISCLOSED_REQUIRES_RECUSAL`;
- `DISCLOSURE_INCOMPLETE`;
- `INDEPENDENCE_UNVERIFIED`.

Absent disclosure is not evidence of absence. `DISCLOSURE_INCOMPLETE` or
`INDEPENDENCE_UNVERIFIED` blocks sign-off for the affected track.

## 7. Review bundle and response

A reviewer must receive one immutable evidence-bundle revision containing the
claim/question, intended use, governing contracts, inputs, receipt/output
identities where applicable, known gaps, competing explanations, uncertainty,
licence/security constraints and requested decision vocabulary.

The response must bind the same bundle revision, list evidence actually
considered, identify exclusions, record findings and dissent, state limitations,
and select one controlled decision. Silence, partial reading or informal advice
cannot be converted into sign-off.

## 8. Current decision

`REVIEW_ROLE_CONTRACT_READY / NO_PERSON_IDENTIFIED / NO_CONSENT / NO_APPOINTMENT / NO_REVIEW`

