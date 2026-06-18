# Agent Lifecycle

Lifecycle status describes agent maturity, not scientific validity or
regulatory approval.

## Idea

**Description:** an agent concept has been identified.

**Entry conditions:** a domain need, repeated workflow, or evidence gap exists.

**Exit conditions:** the idea is archived or documented as a proposed agent
with a narrow purpose.

## Proposed

**Description:** the proposed agent has an initial purpose, users, and scope.

**Entry conditions:** the concept is recorded in a task or design note.

**Exit conditions:** dependencies, evidence needs, governance boundaries, and
expected files are clear enough for design.

## Designed

**Description:** the agent specification follows `AGENT_STANDARD.md`.

**Entry conditions:** inputs, outputs, assumptions, validation, governance, and
limitations are documented.

**Exit conditions:** design review approves implementation, or requests
changes.

## Implemented

**Description:** approved executable or deterministic reporting functionality
exists in the repository.

**Entry conditions:** implementation task is approved and code or builder
outputs are present.

**Exit conditions:** focused and repository tests pass and validation review
begins.

## Validated

**Description:** specified technical tests and required human or professional
reviews are complete for the declared scope.

**Entry conditions:** implementation, test evidence, limitations, and reviewer
records are available.

**Exit conditions:** operational use is approved for a defined environment, or
validation identifies required changes.

`Validated` must name the validation scope. It does not automatically mean
scientifically confirmed, professionally certified, or approved.

## Operational

**Description:** the agent is approved for a documented operating context with
monitoring and support responsibilities.

**Entry conditions:** release, ownership, version, review, rollback, and
maintenance expectations are documented.

**Exit conditions:** the agent is replaced, suspended, or archived.

## Archived

**Description:** the agent is retained for history but is no longer active.

**Entry conditions:** a decision records the reason, replacement, final
version, and retained artifacts.

**Exit conditions:** none. Reintroduction requires a new proposal and review.
