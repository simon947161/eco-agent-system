# CLIMATEOS–AWT–001｜可信甲烷减排与环境主张验证试点（Codex 执行任务书）
**Issued:** 2026-11-23
**Sponsor:** Founder / ClimateOS
**Execution:** Codex on authorized local workstation, with GitHub evidence receipts
**Status:** AUTHORIZED FOR P0 READ-ONLY AUDIT AND BOUNDED P1–P3 IMPLEMENTATION ON ISOLATED BRANCH; NO PRODUCTION RELEASE OR REGULATORY CLAIM

## 0. Why this task exists
The Founder reviewed a Chinese analytical essay based on the 2026 ARRC AWT consultation (56 questions), titled 《一吨减排，究竟值不值得相信？》. Core hypothesis: a measured methane value, a counterfactual emissions reduction, additionality, method eligibility, and credit issuance are DISTINCT assertions. Build a demonstrable, reproducible ClimateOS pilot that traces them independently. **Do not create another generic carbon calculator or another agent platform.**

This issue extends existing [CarbonOS #131](https://github.com/simon947161/eco-agent-system/issues/131), P1-A, D/D3 constrained computation and evidence-admission work, related PRs (#132 CarbonOS, #137 Chinese report), EcoEngine, Public Strategy Atlas (#130), and EcoChain/E4 where genuinely present. Verify actual statuses rather than assuming those PRs are merged or that local research was published.

## 1. Mandatory P0 — inventory before writing code
1. Fetch latest origin/main HEAD and examine existing active/draft PR heads, `NEXT_SESSION.md` where actually located, repository conventions, CarbonOS/Methane/EcoEngine/Atlas/EcoChain assets, issues #131 and relevant PRs. Record branch/SHA/path; if inaccessible, mark `NOT_VERIFIED`, do not invent.
2. Locate available local outputs from `CLIMATEOS-CARBON-P1A-001`, D3 gas-observation admission and constrained calculations; differentiate local-only, committed, draft-PR and scientifically admitted outputs. Keep paid/licensed/private files and secrets local.
3. Produce `EXISTING_ASSETS_AND_GAPS.md` identifying *reuse / extend / missing / blocked*, with links and verifiable file hashes when available; cross-reference #131 and existing branch. Explicitly identify any unfinished D3 permit/data/clock/QC validation and **do not redo an already accepted batch**.
4. Before implementation, choose one **canonical** place in existing research structure. Do not modify unrelated PR #129/#130/#132/#137; prefer a new isolated branch and **Draft PR**. If baseline workflows are blocked, log blocker and stop affected scope without substituting invented data.

## 2. Minimum scientific conceptual separation
Track separate, typed entities for:
- `OBSERVATION`: measured concentration/flux/conditions with instrument, unit, location/time, uncertainty and QC.
- `PHYSICAL_ESTIMATE`: methane generation, oxidation, capture, escape/emitted mass flux, and atmospheric dispersion **as different quantities**; separate source flux from downwind concentration.
- `BASELINE_COUNTERFACTUAL`: what would plausibly happen without the project; waste composition, applicable period, plausible landfill capture, evidence.
- `PROJECT_EMISSIONS` and `LEAKAGE`: included energy, transport and residue CH4/N2O/fossil CO2 where within the relevant method boundary; no arbitrary double subtraction.
- `NET_ABATEMENT_ESTIMATE`: defensible mathematical computation with provenance and propagated uncertainty, *not itself a credit*.
- `ADDITIONALITY_AND_ELIGIBILITY`: jurisdiction, legal obligations and commencement dates, method eligibility/version, transition/safeguard overlaps; uncertainty in policy interpretation made explicit.
- `CLAIM_AND_CREDIT_RIGHTS`: waste-batch/material flow, project/method/registry references and possible double-claim conflicts; do not equate a claim risk flag with definitive fraud.
- `ASSURANCE_STATUS`: evidence-backed / insufficient / conditions not met, plus unknowns and independent reviewer.

Method-approved statutory inputs must not silently be replaced by experimental methane-physics coefficients. Physics can be a supplementary sensitivity/monitoring analysis unless method allows otherwise. AWT consultative proposals **are not enacted rules**.

## 3. Data and governance contract (P1)
Implement a minimal versioned, auditable **claim passport** (JSON Schema or compatible existing format, NOT a competing database) with: claim ID; scenario; geographic/regulatory scope; dataset source/licence/byte SHA256; measured vs simulated; formula and source versions; units; observation time/timezone/QC; assumption owners; parameter uncertainty; output provenance; legal effective dates; potential overlap; review gate; immutable revisions; human reviewer notes. Integrate with the existing evidence-passport / Atlas structures if actually present, and record explicit rationale for reuse. Provide deterministic schema tests and illustrative **synthetic fixtures clearly labelled SYNTHETIC**.

## 4. Bounded experiment (P2)
A teaching case of **1,000 tonnes of organic waste** (not an actual site claim), with four comparable scenarios:
A. existing landfill pathway with plausible, sourced varying landfill-gas capture assumptions;
B. diversion to anaerobic digestion, with project emissions and digestate/residue endpoints;
C. evolving mandatory FOGO separation/collection rules in NSW: separately test *collection obligation* vs *required processing pathway*, based on effective-date and jurisdictional evidence;
D. missing residual emissions or potential duplicate accounting across AWT / safeguard / other mechanisms.

For each scenario report:
- baseline, project and applicable leakage emissions, with units and conservative uncertainty/sensitivity ranges;
- physical science ledger vs counterfactual/method accounting ledger vs legal/eligibility ledger, without mixing them;
- `estimated net abatement` and **`credit quantity = NOT_DETERMINED`** unless method-specific eligibility and comprehensive required inputs truly supported;
- evidence references and explicit stop/fail/unknown reasons; a reproducible script/test invocation.
Use official openly licensed data only after checking source, allowed reuse, byte checksum, schema, time/QC and provenance, else use SYNTHETIC inputs. No extrapolated national inventory, no invented site measurements, no unlicensed downloads, no 403/499 bypass, no guessed credit rates.

## 5. Decision & assurance demonstration (P3)
Implement limited rule-based checks and a **reviewable explanation** (not an unreviewable LLM assertion):
1. physically coherent vs physically inconsistent input;
2. baseline evidence present vs missing;
3. applicable legal requirement in scope vs uncertain;
4. potential duplicate-credit linkage;
5. method version / transition issue;
6. uncertainty and data quality inadequacy.
Provide tests where the system returns `INSUFFICIENT_EVIDENCE` rather than falsely approving; distinguish `NOT_ELIGIBLE` only when a verified rule warrants it. Any language model use is advisory, not authoritative.

## 6. Acceptance and delivery
On a dedicated `codex/climateos-awt-001-...` branch:
- `EXISTING_ASSETS_AND_GAPS.md`
- `CLAIM_PASSPORT_SCHEMA.*` and validated examples
- `COUNTERFACTUAL_CASE_1000T.md` with reproducible calculations and sensitivities
- `LEGAL_METHOD_VERSION_REGISTER.md` dated sources and status (consultation vs operative)
- `ASSURANCE_DECISION_TESTS.md` test evidence, fixtures, pass/fail/logs
- `FOUNDER_ACCEPTANCE_CN.md`: Chinese Slides-style page-by-page reading, headline first, supporting details expandable/referenced. Explain what was NOT verified.
- update existing canonical index and `NEXT_SESSION.md` if present; link issue #131, PR #132/#137 where relevant, issue/PR HEAD SHA, source receipts and CRP handoff.

Run unit/schema and reproducibility tests, verify no secrets/private Council/workplace data, provide git diff and regression summary. Push branch, open **Draft PR** referencing this issue, include screenshot/browser QA **only if a UI exists**. Do not assert tests ran if they did not.

## 7. Approval gates / non-goals
**Founder approval required** before: merging, production deployment, public regulatory submission, official ACCU claims, purchasing, account/credential changes, touching Council data, expanding into another platform, or asserting scientific/independent assurance. Do not overwrite existing work or close #131. If P0 reveals unresolved data-admission barriers, complete what can honestly be proven using explicitly synthetic data and report `DATA_NOT_READY` for real-data claims. Stop before any action that could risk data or system integrity.

## 8. Required Codex reply
Reply in Chinese with: actual baseline HEAD; reuse inventory; exact branch/Draft PR URL and new commit SHA; work done by phase; tests and raw receipts; which statements are real-data vs synthetic; missing evidence/blockers; approvals required; next atomic task. If unable to push, show reason and local diff paths without saying GitHub was updated.

### Founder strategic test
**Can ClimateOS explain why the same 1,000 tonnes of organic waste yields different modeled abatement estimates and different eligibility/assurance results under different capture, disposal, law and data-quality conditions, without equating modeled tonnes to issued ACCUs?**

CRP keywords: ClimateOS, AWT, CarbonOS, Methane, Evidence Passport, Counterfactual, MRV, FOGO, Additionality, EcoChain, Regulatory Temporal Validity, Assurance.
