# Task341-350 MVP Data Interface And Architecture Question Requirements

## Task341 MVP Interface Information Requirements

Future interface screens may need to display the following information. This is not UI design.

- Case overview.
- Source register.
- Signal register.
- Claim candidate register.
- Knowledge Object candidate register.
- Evidence readiness matrix.
- Risk flags.
- Human review queue.
- Founder Gate queue.
- Closure packet.

The purpose is to preserve information needs for future review, not to design screens.

## Task342 Data Field Inventory

Requirements-level field inventory only.

No schema authorized.

No implementation authorized.

Candidate future fields:

| Area | Requirements-level fields |
| --- | --- |
| Case | Case ID, case name, boundary, themes, authorization scope, stop point |
| Source | Source ID, title, publisher, date, URL / citation path, language, source type, access date, retrieval status, reliability caution |
| Signal | Signal ID, theme, source link, description, related claim, risk flag, review status |
| Claim candidate | Claim ID, paraphrase, source ID, claim type, evidence candidate, readiness, risk flag, review need |
| Knowledge Object candidate | KO ID, KO name, KO type, linked sources, linked claims, linked evidence candidates, readiness, risks, stop point |
| Evidence candidate | Evidence ID, linked source, linked signal, linked claim, linked KO, evidence type, limitation, readiness, status |
| Review | Human review need, reviewer note, decision needed, stop condition, archive status |
| Founder Gate | Gate ID, trigger, decision needed, future authorization relevance, stop condition |

## Task343 Workflow State Inventory

Allowed future states may include:

- Draft.
- Candidate.
- Needs source verification.
- Needs human review.
- Needs Founder Gate.
- Blocked.
- Ready for architecture consideration.
- Archived.
- Closed.

No state machine logic is implemented or authorized.

## Task344 Model Assistance Requirements

Future AI / model assistance may help with:

- Source summarization.
- Claim candidate extraction.
- Signal clustering.
- Risk flag suggestion.
- Readiness suggestion.
- Review note drafting.
- Archive summary drafting.

Model suggestions cannot replace human review or Founder Gate.

Model assistance must not create compliance, assurance, certification, ESG, carbon, standards, framework, scoring, or political conclusions.

## Task345 Citation / Provenance Requirements

Future citation and provenance requirements:

- URL.
- Publisher.
- Date.
- Access date.
- Source type.
- Quote / paraphrase distinction.
- Version if available.
- Language.
- Translation note if used.
- Archived file path if later stored.
- Retrieval status.
- Human review status.

## Task346 GitHub Archive Requirements

Future GitHub archive requirements:

- What should be archived.
- Folder naming expectations.
- Commit message expectations.
- Closure packet expectations.
- Index update expectations.
- Review trace expectations.
- Source candidate status preservation.
- Boundary confirmation preservation.

No GitHub automation is implemented.

## Task347 Security / Access / Role Requirements

High-level future requirements:

- Founder-only actions for gates, external use, and future authorization.
- Reviewer actions for source review, claim review, risk review, and stop conditions.
- Read-only archive access where appropriate.
- Public vs private source handling.
- Sensitive source caution.
- Political sensitivity caution.
- No authentication implementation in this sprint.

## Task348 Testing / Evaluation Questions

Future testing questions:

- Can a user trace every claim candidate to a source candidate?
- Can risk flags stop overreach?
- Can human review be required before conclusions?
- Can Founder Gate block architecture escalation?
- Can the system avoid scoring?
- Can the archive reproduce the decision trail?
- Can candidate-only sources remain visibly provisional?
- Can late-arriving context packets be recorded without invented content or boundary drift?
- Can public-use risk be blocked before external communication?

## Task349 Architecture Questions For Task361-420

The backlog of future questions is maintained in [ARCHITECTURE_QUESTIONS_FOR_TASK361_420.md](ARCHITECTURE_QUESTIONS_FOR_TASK361_420.md).

These questions are not answered in this sprint.

Task349 does not start Task361-420.

Task349 does not create architecture design.

## Task350 MVP Requirements Interim Summary

The use trial suggests that a future ClimateOS MVP may need:

- Case boundary records.
- Source candidate intake.
- Source retrieval status.
- Signal classification.
- Claim candidate tracking.
- Knowledge Object candidate grouping.
- Evidence candidate linkage.
- Readiness labels.
- Risk flags.
- Human review needs.
- Founder Gate needs.
- Archive and closure records.

This prepares future review questions only. It does not start architecture work.
