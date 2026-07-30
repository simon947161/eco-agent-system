# ClimateOS v1 Capability and Debt Map

## Evidence-backed capability baseline

| Capability | State | Evidence | Honest limit |
|---|---|---|---|
| deterministic scenario comparison | executable | `cczps_lite/engine/` and committed outputs | indicative logic is not a validated environmental model |
| evidence, claim and provenance contracts | executable/static mix | contracts, validators, receipts and Passports | multiple overlapping vocabularies need consolidation |
| supervised human–AI workflow | executable | scientist and environmental-question runtimes | deterministic structuring, not autonomous scientific reasoning |
| persistent local continuity | executable | SQLite state, audit chain and Cooma program | local state is not yet a continuous data assimilation system |
| model/source admission | executable/static mix | source registries, admission gates and synthetic adapters | few real models and datasets are operationally connected |
| official real-data intake | executable | Cooma BoM pilot; PR #108 flow intake | mostly L1 source facts and intake receipts |
| QGIS local spatial foundation | executable builder/workflow | terrain, hydrology, roads, imagery and integrated project | spatial presence is not environmental interpretation |
| conclusion maturity | specified | L0–L4 protocol | not yet bound to a live evolving signal state |
| tests and denial controls | executable | `445/445` main; `451/451` PR #108 | tests modify tracked generated outputs and are not hermetic |
| public warning/decision authority | absent by design | explicit prohibitions | must remain absent unless separately governed |

## Architecture debt

### Scientific debt

- no completed multi-source, time-bounded Cooma assessment;
- no operational evidence-convergence engine with counterevidence and
  disagreement handling;
- historical flow, current weather, climate state, terrain and exposure are
  not yet joined at a declared scientific boundary;
- no systematic hindcast/forecast-skill ledger for local assessments;
- no complete observation → assessment → action → outcome feedback loop.

### Product debt

- task and gate documents outnumber decision-facing outputs;
- users can inspect maps and receipts but cannot yet ask one question and
  receive one valid, expiring environmental answer;
- many technically correct outputs say what cannot be concluded without also
  stating the next evidence that would change the answer;
- Founder review is repeatedly expressed as mechanical task sequences rather
  than clear decision options.

### Governance debt

- repeated boundary language is copied across many task documents;
- high-safety controls are sometimes applied equally to low-regret,
  reversible observation and to high-impact decisions;
- “official source fact”, “official institutional conclusion”, “reviewed
  ClimateOS assessment” and “public warning” are not always separated clearly;
- conclusion maturity and temporal signal maturity are currently conflated.

### Repository debt

- eight open PRs span fresh mainline work, old stacked work, demos and
  cross-system infrastructure;
- old branches can remain technically mergeable while being hundreds of
  commits behind current main;
- test runs rewrite tracked reports and CSVs;
- historical context packets sometimes remain open after their operational
  purpose has passed;
- some important concepts, including N1/N2, have no recoverable repository
  provenance.

## ACTP capability assertions: verified or revised

| ACTP working assertion | Review finding |
|---|---|
| strong evidence and governance foundations | verified |
| persistent local Runtime continuity | verified |
| meaningful question structuring | verified |
| Cooma QGIS spatial representation | verified |
| controlled official intake | verified |
| no complete governed local multi-source assessment | verified |
| binary `NO CONCLUSION / OFFICIAL CONFIRMATION` must be replaced | revised: the existing L0–L4 protocol is already non-binary; v2 should add an orthogonal temporal evidence-maturity axis |
| official confirmation is currently the only conclusion prerequisite | not supported by the L0–L4 protocol; L2 and L3 can exist without an institutional declaration if their own gates pass |

## v2 keep / change / stop

### Keep

- provenance, licences, hashes and immutable receipts;
- QGIS v0.4 as accepted spatial baseline;
- human review, dissent and stop conditions;
- L0–L4 conclusion maturity;
- Cooma as principal local proving ground.

### Change

- gates become proportional to consequence and reversibility;
- task-number progress becomes capability and decision progress;
- every assessment gets validity, expiry and update triggers;
- official confirmation becomes evidence, not a magic permission switch;
- ontology objects must participate in real inference paths.

### Stop

- equating document volume with capability;
- adding registries without a named downstream decision;
- repeating easy weather intake while core water-accounting terms remain open;
- treating an old mergeable PR as current merely because GitHub reports no
  textual conflict;
- using “no conclusion” as the end product when a bounded descriptive answer
  is supportable.

