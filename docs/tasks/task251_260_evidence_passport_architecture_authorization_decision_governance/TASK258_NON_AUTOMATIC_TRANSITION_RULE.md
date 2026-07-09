# Task258 Non-Automatic Transition Rule

## Purpose

Define that completion of Task251-260 does not automatically start Task261-270, architecture work, implementation work, or runtime work.

## Core Statement

Task251-260 closure may recommend a next step, but it cannot authorize or begin that next step.

## No Automatic Task261-270 Start

Task261-270 must not begin automatically.

Task261-270 requires separate Founder review, separate Founder authorization phrase, and a separate kickoff brief.

## No Automatic Architecture Start

Architecture design must not begin automatically after Task251-260 closure.

Any future architecture design work requires a separate Founder-approved brief and explicit boundary confirmation.

## No Automatic Implementation Start

Implementation must not begin automatically after Task251-260 closure or any future architecture decision.

Implementation requires a separate Founder-approved phase.

## No Automatic Runtime Start

Runtime must not begin automatically after Task251-260 closure, future architecture design, or future implementation planning.

Runtime requires a separate Founder-approved phase.

## Separate Founder Authorization Requirement

Every transition requires separate Founder authorization:

- Decision governance to future work request.
- Future work request to architecture design.
- Architecture design to implementation.
- Implementation to runtime.

## Separate Batch Brief Requirement

Any future Task261-270 work requires its own batch brief.

Task251-260 does not create that brief.

## Separate Boundary Confirmation Requirement

Any future batch must restate boundaries, including no Runtime, no implementation, no operational Evidence Passport, no compliance guidance, no assurance guidance, no certification guidance, no framework interpretation, and no standards interpretation unless separately authorized in a future phase.

## Separate Repository State Confirmation Requirement

Any future batch must begin with repository identity and working tree confirmation.

## Separate Closure Criteria Requirement

Any future batch must define its own closure criteria and final report requirements.

## Status

```text
No automatic Task261-270 start: DEFINED
No automatic architecture start: DEFINED
No automatic implementation start: DEFINED
No automatic runtime start: DEFINED
Task261+: NOT STARTED
```
