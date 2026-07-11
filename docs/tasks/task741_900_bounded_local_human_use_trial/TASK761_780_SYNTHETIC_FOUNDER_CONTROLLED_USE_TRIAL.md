# Task761-780 Synthetic Founder-Controlled Use Trial

## Protocol

The deterministic trial creates synthetic/public-safe evidence, records a
declared local reviewer action, retrieves the resulting state and inspects the
audit sequence. No live observation, scientific inference or verified identity
is used.

## Findings

The first trial design used natural-language actions `challenge` and `refuse`.
The frozen backend correctly rejected them because its governed actions are
`dispute` and `reject`. The workbench was corrected to display human-readable
labels while submitting the valid governed action names. No backend rule or
test assertion was weakened.

The trial then passed for create and dispute, with the evidence remaining
candidate-governed and both creation and dispute recorded in order.

## Trial Boundary

This is a deterministic workflow validation, not usability research with an
independent participant sample. Claims about general usability would exceed the
evidence.
