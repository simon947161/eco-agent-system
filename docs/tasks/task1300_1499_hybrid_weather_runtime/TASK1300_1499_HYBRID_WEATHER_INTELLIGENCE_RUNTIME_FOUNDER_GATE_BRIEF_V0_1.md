# ClimateOS Task1300-1499 Hybrid Weather Intelligence Runtime

## Founder Gate Brief v0.1

Date: 2026-07-12

Status: DRAFT_FOR_FOUNDER_REVIEW

Authorization: NOT_EXECUTABLE

Proposed prerequisite: merge and authoritative verification of validated
Task1290-1299 PR #49.

## Gate Question

Should ClimateOS establish a provider-neutral Hybrid Weather Intelligence
Runtime foundation that can register and compare physical models, AI models,
observations and downscaling products without silently treating any source as
truth or automatically exposing unverified sources to users?

## Founder Direction

An unavailable, unverified, licence-unclear or scientifically immature source
does not need to be integrated now and is not permanently rejected. ClimateOS
must preserve it as a transparent future option, state why it is not connected,
and define what evidence or permission would allow reconsideration.

Customer interest does not turn an unverified source into an endorsed source.
A customer-requested experiment requires explicit opt-in, limitations and risk
disclosure, bounded use, audit, stop conditions and a separate approval path.
ClimateOS retains its own safety, legal and platform responsibilities.

## Proposed Source States

- `VERIFIED_CANDIDATE`: sufficiently verified to enter a bounded integration
  proposal; not yet connected.
- `CONNECTED_FOR_RESEARCH`: connected only within an approved research scope.
- `CONNECTED_WITH_LIMITATIONS`: connected with declared constraints.
- `DEFERRED_UNVERIFIED`: plausible but current evidence is insufficient.
- `DEFERRED_ACCESS_OR_LICENCE`: access, commercial right or licence unresolved.
- `CUSTOMER_REQUESTED_EXPERIMENT`: separately approved opt-in trial; no
  ClimateOS endorsement or production authority.
- `NOT_SUITABLE_FOR_DECLARED_USE`: unsuitable for the specific reviewed use,
  with reasons and re-review conditions.
- `RETIRED_OR_UNAVAILABLE`: previously considered source no longer usable.

No state is a permanent universal verdict. Every record requires source,
version, intended use, evidence date, limitations, decision owner and next
review trigger.

## Proposed Task Map

### Task1300-1339 — Forecast Source Registry

Register physics-based models, AI models, observations, ensembles and
downscaling products separately. Record provider, version, variables, grids,
vertical levels, update cycle, latency, archive, licence, access, commercial
rights, service level, cost, support, maturity and source state.

### Task1340-1379 — Common Weather Data Contract

Define time, run time, valid time, lead, ensemble member, coordinates, grid,
vertical levels, units, quality flags, transformations, provenance, checksum,
missingness and source-specific limitations. Grid spacing must not be described
as effective physical resolution.

### Task1380-1419 — Hybrid Forecast Orchestrator Foundation

Design physics and AI sources to operate in parallel. Preserve independent
reference and fallback routes. Do not silently average disagreement or let a
source become unquestioned truth. This batch should initially use adapters,
contracts and controlled fixtures unless a source-specific integration receives
separate approval.

### Task1420-1459 — Comparison And Divergence Layer

Represent agreement, event-specific disagreement, systematic bias,
out-of-distribution conditions, stale inputs and transformation uncertainty.
Expose relevant divergence to downstream systems without creating an automatic
public forecast or safety decision.

### Task1460-1489 — Failure, Fallback And Human Review

Define source outage, stale-run, invalid-field, degraded-mode, fallback,
escalation, audit and human-review rules. Consequential use requires declared
human authority and the appropriate professional or operational source.

### Task1490-1499 — Task1500 Coupling Input Gate

Review whether any governed weather inputs are ready to support future
Environmental Coupling Layer work. Task1500 remains separately gated.

## Current Preflight Source Findings

### AICON / DWD

Current official evidence supports AICON as an architecture and
operationalisation reference. Public code, weights, feed, licence and stable
external service have not been verified. Initial state:
`DEFERRED_UNVERIFIED`. Re-review when DWD publishes authoritative operational
status, access, interface and licensing documentation.

References:

- https://www.dwd.de/EN/press/press_release/EN/2025/20250806_new-ai-centre.pdf
- https://www.dwd.de/EN/specialusers/research_education/seminar/2026/iccarus2026/final_programme_en.pdf

### ECMWF IFS And AIFS Open Data

ECMWF achieved fully open Real-time Catalogue status under CC BY 4.0 in October
2025. Open subsets and commercial reuse are promising; enhanced delivery may
still create service charges. Rolling open-data retention is short and does not
replace historical verification data. Initial state:
`VERIFIED_CANDIDATE` for registry and small controlled sample planning, not
automatic connection.

References:

- https://www.ecmwf.int/node/29013
- https://www.ecmwf.int/en/forecasts/datasets/open-data
- https://www.ecmwf.int/en/forecasts/accessing-forecasts/service-agreements

### Australian Bureau Of Meteorology ACCESS

ACCESS is the priority Australian physics-based source family. Product-level
access, Bureau Express Licence scope, redistribution, automation, archive,
latency and commercial terms require current verification. Initial state:
`DEFERRED_ACCESS_OR_LICENCE` until the selected product and use are reviewed.

Reference:

- https://www.bom.gov.au/nwp/doc/access/NetCDFnotes.shtml

### Google DeepMind WeatherNext / GraphCast / GenCast

Code and notebooks may use Apache 2.0 while model weights are published under
CC BY-NC-SA 4.0 and the repository is not an officially supported product.
Commercial ClimateOS use cannot be assumed compatible. Initial state:
`DEFERRED_ACCESS_OR_LICENCE`. Research comparison remains possible under a
separate licence-reviewed gate.

Reference:

- https://github.com/google-deepmind/weathernext

## External Service And Commercial Rule

ClimateOS may use paid APIs, external models, commercial software and hosted
services. Free resources are preferred when fit for purpose, not required when
a paid source offers justified value. Before a chargeable commitment, provide
the Founder with need, provider, licence, billing basis, initial and recurring
cost, ceiling, alternatives, ownership, export, retention, cancellation,
lock-in, benefit measures, trial bounds and exit plan.

Future users may pay approved third-party usage costs. ClimateOS may separately
charge for governed access, orchestration, provenance, comparison, audit,
support and platform value, subject to provider resale terms, consumer law,
tax, privacy, service-level and commercial approval.

## Proposed Executable Scope

If separately authorised, Task1300-1499 may create provider-neutral registry,
data-contract, adapter-interface, orchestration, comparison, failure/fallback
and human-review foundations with synthetic or already-authorised tiny samples.

Any source-specific download, API call, model execution, paid use or customer
experiment must remain inside its own declared approval.

## Excluded Without Separate Approval

- production or public forecast service;
- automatic public-safety, emergency, legal, compliance or investment decision;
- silent activation of a deferred or customer-requested source;
- purchase, subscription, metered cost or paid API commitment;
- unrestricted historical data acquisition or material compute;
- use of non-commercial weights in a commercial service without permission;
- private Founder-reserved EcoEngine access;
- PR merge;
- Task1500 or later work.

## Preflight Decision

Current result: `CONDITIONALLY_READY_FOR_FOUNDER_GATE_DESIGN`.

Task1300 implementation should remain blocked until PR #49 is merged and the
authoritative branch is re-verified. The first executable batch should be
smaller than the full Task1300-1499 range and should start with source registry,
source-state governance and common-contract fixtures rather than live model
integration.

## Founder Decision Options

1. Authorise a bounded Task1300-1339 Forecast Source Registry and source-state
   governance batch only.
2. Revise the source states, customer opt-in rule or source priorities.
3. Defer implementation while retaining this preflight record.

No option is selected by this Brief.
