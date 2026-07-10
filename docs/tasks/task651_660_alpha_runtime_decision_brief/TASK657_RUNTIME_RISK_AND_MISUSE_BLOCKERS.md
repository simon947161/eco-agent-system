# Task657 Runtime Risk And Misuse Blockers

## Purpose

Identify blockers that should prevent Alpha Runtime authorization until they are
resolved or explicitly accepted by the Founder.

## Runtime Risk Blockers

| Blocker | Why It Matters |
| --- | --- |
| Evidence states are unclear | Users may mistake candidate signals for reviewed evidence. |
| Human authority is unclear | Runtime may appear to decide instead of assisting review. |
| Agent permissions are unclear | Agents may act beyond intended scope. |
| Private asset boundary is unclear | Founder-reserved EcoEngine assets could be exposed or reused. |
| Model outputs are unlabeled | Model suggestions may look like validated findings. |
| Scoring pressure appears early | Inquiry may be converted into rankings or certification. |
| Public-facing use is not blocked | Draft reasoning could be reused as external claims. |
| Audit trail is missing | Decisions and revisions cannot be reconstructed. |
| Deployment boundary is unclear | A local review system may drift toward production. |

## Misuse Patterns To Block

- "The system said it, so it must be true."
- "The agent found it, so it is evidence."
- "The model summarized it, so it is reviewed."
- "The interface shows a green state, so it is certified."
- "A biodiversity signal exists, so a climate benefit exists."
- "A local prototype works, so production is ready."

## Founder Gate Rule

Any unresolved blocker must be visible in a future authorization packet. Hidden
blockers should prevent runtime work.

## Current Capability

This file identifies risks. It does not implement controls.
