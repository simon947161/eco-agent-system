# Agent Review Checklist

## Documentation

- [ ] Agent name and narrow purpose are clear.
- [ ] Scope and excluded capabilities are explicit.
- [ ] Inputs, outputs, fields, assumptions, and examples are documented.
- [ ] Human-readable documentation is available.
- [ ] Future work is not presented as current capability.

## Validation

- [ ] Evidence requirements and provenance are defined.
- [ ] Missing and invalid inputs have conservative handling.
- [ ] Uncertainty and confidence are disclosed.
- [ ] Validation rules and professional-review needs are documented.
- [ ] Statuses are not upgraded without source evidence.

## Governance

- [ ] Human decision and approval boundaries are explicit.
- [ ] Privacy, ownership, cost, audit, and retention needs are considered.
- [ ] No prohibited ranking, recommendation, certification, or autonomous
  decision capability was introduced.
- [ ] External API, LLM, GIS/DEM, payment, or cloud use is explicitly governed.

## Repository Structure

- [ ] The agent uses the correct subsystem directory.
- [ ] Small modular files are preferred.
- [ ] Existing architecture and compatibility are preserved.
- [ ] No existing files or folders were unexpectedly deleted or renamed.
- [ ] Agent Catalog and queue status are updated when appropriate.

## Testing

- [ ] Focused tests cover the declared behavior.
- [ ] Existing repository tests pass.
- [ ] Deterministic outputs are verified where applicable.
- [ ] Test-generated side effects are removed or intentionally documented.
- [ ] Remaining test gaps are stated.

## Completion Summary

- [ ] Created files are listed.
- [ ] Modified files are listed.
- [ ] Test command and results are recorded.
- [ ] Important limitations are stated.
- [ ] Lifecycle and review status are recorded accurately.
