# Task673 Provider Output Evidence Candidate Distinction

## Purpose

Prevent ClimateOS from confusing model-provider authority with reviewed
ClimateOS evidence.

## Distinctions

| Layer | Meaning | Authority Limit |
| --- | --- | --- |
| Model provider | Entity or project that maintains the model or tool. | Provider reputation does not automatically validate local use. |
| Model input | Data or assumptions supplied to the model. | Bad or mismatched inputs can make outputs misleading. |
| Model output | Result produced by the model. | Output is not proof by itself. |
| Evidence candidate | Model output plus context that may be reviewed. | Candidate status means review is still required. |
| Reviewed evidence | Candidate reviewed against provenance, assumptions, uncertainty, and domain fit. | Review remains bounded and revisable. |
| Governance conclusion | Human-authorized judgment that may use reviewed evidence. | Cannot be automated by model output. |

## Evidence Rule

External model output can enter ClimateOS only as a candidate for evidence. It
must not skip directly to conclusion, recommendation, scoring, certification,
compliance interpretation, or operational decision.

## Example In Plain Language

If a heat-risk model says an office district may become hotter under a future
scenario, ClimateOS should not say "the model proves the district will become
unsafe." ClimateOS may say: "This model output is a candidate signal. We need to
know the scenario, spatial resolution, assumptions, validation history,
uncertainty, local observations, and review status before using it."

## Failure Modes

- treating a respected provider as automatic truth;
- hiding assumptions inside a chart;
- losing the distinction between scenario and forecast;
- using outputs outside their intended domain;
- combining outputs from incompatible models without review;
- converting candidate signals into rankings or scores;
- using model output to bypass human judgment.

## Current Capability

This distinction is a documentation rule only. It does not create an evidence
engine or model-output ingestion path.
