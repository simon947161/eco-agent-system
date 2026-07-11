# Task693 Evidence And Review State Transitions

Supported states are `candidate`, `reviewed`, `disputed`, `rejected`, `stale`,
and `superseded`.

Supported human actions are review, dispute, reject, mark stale, supersede,
correct, and escalate. Rejected or superseded records cannot silently return to
reviewed state; they require a documented correction back to candidate state.

Invalid transitions return a controlled conflict response. Every accepted
transition increments the revision and creates an audit event.
