# ClimateOS Original Roadmap Traceability and Readiness Review v0.1

Date: 2026-07-18

Status: TRACEABILITY_COMPLETE / ROADMAP_NOT_COMPLETE / NO_EXECUTION

## 1. Source plan

The authoritative long-range plan is
`TASK1701_2099_MECHANISM_EXPERIMENT_AND_ENVIRONMENTAL_AI_SCIENTIST_ROADMAP.md`,
dated 2026-07-12. It divides work into a Mechanism Experiment Layer
(Task1701–1899) and an Environmental AI Scientist Runtime (Task1900–2099).

## 2. Milestone assessment

| Original range | Original milestone | Current assessment | Evidence and missing work |
|---|---|---|---|
| 1701–1749 | Mechanism Hypothesis Protocol | `SPECIFICATION_SUBSTANTIALLY_COMPLETE` | hypothesis, alternatives, falsification, design and reproducibility contracts exist; no real hypothesis, diagnostics or expert owner |
| 1750–1799 | Numerical Experiment Contract | `SPECIFICATION_SUBSTANTIALLY_COMPLETE / NO_EXECUTION` | admission, sandbox, permissions, audit, quarantine and review rules exceed the original minimum; no model/config/input/compute/run |
| 1800–1849 | Mechanism Evidence Passport | `NOT_STARTED_AS_OPERATIONAL_MILESTONE` | earlier evidence-passport ideas exist, but no mechanism-run passport or supported/contradicted result from an experiment |
| 1850–1899 | Limited Atmospheric Environment Pilot | `NOT_STARTED` | no data, model, compute, expert or pilot authorization |
| 1900–1949 | Scientific Workflow Roles | `NOT_STARTED` | some human/process roles are described, but no agent workflow or runtime roles are implemented |
| 1950–1999 | Tool and Permission Boundaries | `PARTIALLY_SPECIFIED_EARLY` | static permissions/safety contracts exist; no allowlisted toolchain, validator or enforced runtime boundary |
| 2000–2049 | Closed-Loop Scientific Prototype | `NOT_STARTED` | no question-to-run-to-diagnostics-to-reviewed-report loop |
| 2050–2099 | Governance and Readiness Review | `PARTIALLY_SPECIFIED_EARLY` | strong static governance exists; no reproducibility audit of a real run, bias/data-quality review or runtime dossier |

## 3. Did we finish the original plan?

No.

What is substantially complete is the *paper architecture* for the front half of
the Mechanism Experiment Layer. The original roadmap also requires operational
evidence passports, a bounded pilot and ultimately a controlled scientific
workflow runtime. None of those has been demonstrated.

Task numbers are sequencing labels, not completion percentages. Task1800 marks a
handoff into the Evidence Passport range; it does not close Task1800–1849.

## 4. Readiness dimensions

| Dimension | State at Task1800 | Meaning |
|---|---|---|
| governance vocabulary | strong | identities, states, refusal paths and human-review boundaries are detailed |
| repository no-run validation | available | one return-gate schema/validator/test path exists |
| hypothesis instance | absent | no selected scientific mechanism question is registered for execution |
| experiment package | absent | no filled design, diagnostics, thresholds or configuration |
| model/tool admission | blocked | WRF 4.8.0 remains candidate-only; WRF-Chem/WPS/dependencies unresolved |
| licence/security review | absent for real target | matrices exist but no external target has been assessed |
| input data | absent | no real or synthetic input admitted for a mechanism run |
| compute/environment | absent | no sandbox, local configuration, ceiling or execution authority |
| expert ownership | absent | no person identified, contacted, consenting or appointed |
| run evidence | absent | no audit event, receipt, output or diagnostic |
| scientific evidence | absent | no mechanism link is supported, contradicted or tested |
| regional conclusion | prohibited and absent | no Bondo/Riverina/Cooma scientific conclusion exists |

## 5. What was worth doing

Several results are genuinely valuable:

1. The system cannot honestly turn an attractive mechanism story into a causal
   claim without diagnostics, alternatives, falsification and review.
2. Model code, data, configuration, licence, security and compute are kept as
   separate admission decisions instead of being bundled under “run the model.”
3. A future run must be reproducible and leave evidence; output begins
   quarantined and an exit code is not treated as science.
4. Structural, security, licence and scientific review are separate; dissent is
   preserved and a familiar name cannot be assumed to be a reviewer.
5. The work has maintained zero cost, no external commitments and clean project
   isolation while the architecture was uncertain.

## 6. What was overdone or deferred too long

- The same zero-cost/no-data/no-contact boundary was restated in many files.
- Ten-task numbering encouraged artificial granularity and frequent approvals.
- Static contracts became much more mature than the executable validator path.
- No end-to-end fixture exercised whether all identities actually join cleanly.
- Scientific question selection and expert strategy remained deferred, so the
  system accumulated governance without testing usability.

These are process findings, not reasons to discard the contracts. The next phase
should test and simplify them.

## 7. Minimum meaningful next gate

Do not begin another broad policy-document series. Choose one of the following:

### Option A — tabletop integration check

Fill every existing object with one explicitly fictional case, without executing
code. This tests naming and handoffs cheaply but produces no runtime evidence.

### Option B — tiny-synthetic vertical slice (recommended)

Authorize one deliberately non-regional, non-scientific tiny fixture and local
execution with exact code, configuration, resource ceiling and expected outputs.
Use it only to test the lifecycle from registration to receipt, quarantine and
review. It must not be represented as environmental evidence.

### Option C — real bounded science pilot

Select a real question, admit data/model/licences/compute and obtain a consenting
expert owner. This creates the most scientific value but is premature until the
vertical slice proves the machinery and costs are understood.

## 8. Readiness decision

`ORIGINAL_PLAN_NOT_COMPLETE / STATIC_FRONT_HALF_STRONG / EXECUTABLE_VERTICAL_SLICE_ABSENT / RECOMMEND_TINY_SYNTHETIC_DECISION_BEFORE_MORE_GOVERNANCE`

