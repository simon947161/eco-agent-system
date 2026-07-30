# ClimateOS Original Intent Traceability Matrix

## Source index

| ID | Authoritative source | Introduced | Original intent contribution |
|---|---|---|---|
| OI-01 | `eco_agent_system/README.md` at initial commit | `eab86d9` | first professional-agent interface translating EcoEngine data into a combined report |
| OI-02 | root `README.md` | `b15330d` and major landing-page revision `58f53f9` | environmental observations become practical, human-reviewed planning, maintenance, resilience and governance decisions |
| OI-03 | `ROADMAP.md` | `9cc5c98` | staged path from core prototype to agents, contribution evidence, climate risk, GIS/simulation integration and field pilots |
| OI-04 | `docs/project-principles.md` | `f5b63af` | physical reality first, dialogue before control, revision under new evidence and human–AI co-stewardship |
| OI-05 | `docs/00_MASTER_ARCHITECTURE/CCZPS_2_0_MASTER_ARCHITECTURE.md` | `5e5fe5f` | possibility computing and continuous reality-to-action-to-feedback governance loop |
| OI-06 | `docs/00_MASTER_ARCHITECTURE/SYSTEM_RELATIONSHIP_MAP.md` | `467ed3d` | distinct roles for purpose, governance, environmental inference, institutional translation, evidence/trust and implementation |
| OI-07 | `docs/00_MASTER_ARCHITECTURE/ECOENGINE_V2_SYSTEM_DEFINITION.md` | `d10b12a` | EcoEngine interprets environmental state and response; agents coordinate but do not become the system; humans retain major decision authority |
| OI-08 | `docs/06_ROADMAP/OPENAI_WORLD_MODEL_STRATEGY_FOR_ENVIRONMENTAL_GOVERNANCE.md` | `62d40a1` | AI organises evidence and scenarios; weak validation and concept-without-demonstration are explicit risks |
| OI-09 | `docs/07_CODEX_TASKS/CODEX_TASK_01_BUILD_CCZPS_LITE_ENGINE.md` | `e918746` | small transparent Batlow pathway comparison; useful output without pretending indicative scores are validated facts |
| OI-10 | `docs/00_VISION/CLIMATEOS_STEWARDSHIP_AND_CIVILIZATION_CARE.md` | `0162345` | long-term care, monitoring, adaptation, memory and responsibility rather than one-time prediction or approval |
| OI-11 | historical `docs/context-packets/ACTP_2026-07-11_CLIMATEOS_TASK001_640_GROWTH_AND_WORKING_MODE.md` | `2da7cdc` | governance must serve scientific inquiry rather than replace it; Founder must understand why each batch matters |
| OI-12 | `docs/tasks/task2061_2070_cooma_environmental_evidence_readiness/CONCLUSION_MATURITY_AND_LANGUAGE_PROTOCOL_V0_1.md` | main lineage | L0–L4 conclusion maturity, reproducible L2 indicators and reviewed L3 assessments with validity and demotion rules |

## Traceability matrix

| Original intent | Current implementation evidence | Verified state | Gap | v2 disposition |
|---|---|---|---|---|
| Translate environmental observations into decisions | source registries, Evidence Passports, question Runtime, planning hypotheses | partly executable | observation-to-local-assessment bridge is incomplete | make time-bounded local assessment the Phase II product |
| Physical reality first | QGIS Cooma v0.4, official BoM intake, 410033 intake in PR #108 | executable foundations | datasets are not yet joined into one scientific question | preserve and connect them through declared boundaries |
| One site, many futures | deterministic CCZPS-Lite scenario engine | executable demonstrator | scores remain illustrative and weakly tied to current evidence | use scenarios only after evidence-state and local-fitness gates |
| Human-reviewed reasoning | supervised Runtime, state machines, audit records and Founder Gates | strong and tested | excessive gates sometimes halt low-risk analysis | apply proportional authority by action class |
| Prediction to intervention to feedback | roadmap and stewardship documents | mostly static | no complete outcome feedback or forecast-skill record | add intervention window and retrospective validation |
| GIS and simulation interface | QGIS builders and source registries | executable spatial foundation | no common spatial evidence graph for assessment | treat QGIS as authoritative spatial workbench |
| Local and community usefulness | Batlow, Bondo, Cooma cases | partially demonstrated | outputs are often task-facing rather than decision-facing | require one answer contract per local question |
| Evidence and trust continuity | provenance, licences, hashes, receipts, quarantine | strong | governance metadata is duplicated across many documents | consolidate reusable controls into shared contracts |
| Human–AI co-stewardship | supervised runtimes and plain-language records | present | current “AI” is largely deterministic structuring | describe capability honestly; do not claim autonomous science |
| Long-term care and learning | persistent Cooma question program | partially executable | no systematic outcome observation and recalibration | add forecast/assessment ledger and retrospective skill review |

## N1/N2 provenance finding

The ACTP asked the review to read early `N1/N2` concepts. A full reachable-history
search found no literal `N1`, `N2`, `North Star N1` or `North Star N2` record in
the repository. The review therefore does not invent their content.

Possible explanations:

- the concepts existed only in conversation history;
- they used different names in the repository;
- they existed on an unreachable local branch or external file.

Founder action is optional: if the original N1/N2 text still matters, provide
or identify it for a later provenance patch. Its absence does not block the
v2 decision because the earliest committed intent is internally consistent.

## Intent conclusion

ClimateOS did not begin as an evidence-compliance filing cabinet. Its stable
lineage is:

> observe physical reality, compare possible futures, support local and
> institutional decisions, preserve human responsibility, and learn from the
> consequences.

The evidence-governance work is valuable infrastructure, but it is subordinate
to that purpose.

