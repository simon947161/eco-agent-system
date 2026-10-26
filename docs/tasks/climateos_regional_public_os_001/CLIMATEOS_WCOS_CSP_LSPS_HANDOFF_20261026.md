# ClimateOS × WCOS × CSP 2035 × LSPS 2040 — Continuity Handoff

**Date:** 2026-10-26 (Australia/Sydney)  
**Home:** ClimateOS / eco-agent-system / existing Issue #128 and Draft PR #129  
**Scope:** Independent, public-safe research and software continuity. This is not a Council task assignment or policy decision.  
**Status:** P02 privately deployed and verified; P03 in progress; legacy Work chat/local prototype not fully recovered.

## 0. Why this handoff exists

The inquiry began within COOMA Water Compliance WorkOS (WCOS) while learning SMRC Community Strategic Plan 2035 (CSP), Local Strategic Planning Statement 2040 (LSPS), and water/environmental compliance. The founder corrected a slow ten-year 'first compliance, later strategic thinking' plan: build **the cross-system analytical framework now**, spend the next **1–2 years testing assumptions with lawful public evidence and non-confidential professional learning**, and use a **ten-year horizon** to pursue independently reviewed research, collaboration, career and possible industry opportunities.

Make this body of work durable within ClimateOS, without moving private Council case information or creating a second OS. A ChatGPT Work conversation may be missing from the UI; the canonical engineering state is in the existing repository. Do not mistake this handoff for a recovered verbatim transcript.

## 1. Big question and governing theory

**Main inquiry:** Under climate variability, drought, and regional growth, how can water, soil, vegetation, energy, carbon, land use, infrastructure, and social/economic systems be studied together to support resilient and affordable development and a defensible 'dryland ecological civilisation' vision?

- CSP 2035: public/community outcomes and measures, not the Council's personal performance contract.
- LSPS 2040: land-use/spatial development priorities and historical actions, not a development consent.
- Current Delivery Program / Operational Plan: implementation, resource and timing hypotheses; latest versions must be independently verified.
- ClimateOS: scientific observation, mechanisms, models, traceable evidence and scenarios; not a substitute for Council-approved systems.
- WCOS: first-hand professional learning context only; no real customers, addresses, device IDs, inspection photos, recordings, or confidential Council data in ClimateOS.
- AI: source discovery, comparison, provenance, contradiction detection, reproducible scenarios, review support. Not automatic regulatory, ecological, hydrological, statutory or commercial authority.
- Always distinguish fact, document intention, officer learning, scientific hypothesis, model scenario and unresolved unknown.

## 2. Three research lines (parallel, shared evidence)

**T1 — Water service resilience × water–energy–carbon.** Public evidence on streamflow, demand boundaries, system reliability, water/wastewater energy and emissions; clarify asset/service-area/catchment distinctions. Develop falsifiable questions; do not infer town water supply capacity from a river gauge.

**T2 — Soil–vegetation–catchment resilience.** Drought, precipitation, evapotranspiration, runoff, vegetation cover, soil condition, land management, agriculture and ecology. Compare sites/time periods; remote-sensing greenness is neither causal proof nor accredited soil carbon.

**T3 — Regional evidence and scenario governance.** Shared policy crosswalk, SourceRevision, Claim, Hypothesis, Indicator, ScenarioRun, Counterevidence, Review, Outcome and Opportunity gates. Link CSP/LSPS/DP/OP targets to measurable evidence and alternative explanations with units, time/space extent and uncertainty.

All three are ongoing; do not misinterpret as sequential project phases. ClimateOS research should lead to career, scholarly and potential market opportunities only after separate demand, legal and conflict-of-interest validation.

## 3. Verified engineering baseline

Canonical repository: https://github.com/simon947161/eco-agent-system  
Parent issue: https://github.com/simon947161/eco-agent-system/issues/128  
Existing open Draft: https://github.com/simon947161/eco-agent-system/pull/129  
Branch: codex/regional-public-os-001-taskbook

First read AGENTS.md, docs/tasks/climateos_regional_public_os_001/TASKBOOK.md and EXECUTION_STATE.json; then smrc_policy_console/RESEARCH_FINDINGS_INITIAL.md, decision-matrix.json, CONSOLE_INTEGRATION.md, VALIDATION.md, and P02_SITES_PRIVATE_ACCEPTANCE.md. Early UI-pending remarks in older files are superseded by later acceptance.

Prior implementation commits:
- 42e8df72a549752a7f15a64f0ba6c58c1f11f49d: public policy sources/provenance.
- 11327bc70ba1fa4c2ff995b604acbca48622a3d4: existing Console policy API and three research-line UI.
- 6ca8f9d913e99ba66d4743790b2e4f0df11cf571: local historical HRS streamflow evidence chain.
- 6a5c3b88af4536066fbc66f379decd74318e6571: private Sites Worker implementation.

**P02 accepted:** https://climateos-snowy-monaro.minshu.chatgpt.site ; owner-private, site version 2; server-side owner access, hosted desktop/mobile, rollback/restore verified in GitHub acceptance records. P02 test snapshot: BOM HRS / WaterNSW station 410033 Mittagang Crossing, 22,645 daily rows, 1964-03-01 to **2026-02-28**, source edition September 2026, licence CC BY 3.0 AU / © WaterNSW with BOM attribution. Quality codes preserved; scientific human review remains pending. This is historical catchment streamflow, not current water conditions, drinking water sufficiency, or a Council compliance decision. Source SHA256: 78e8188f3f445afa33ad466dd0554e653761ef617832b6df3a9eac6b1240ca1a.

Historical reference-station CSV direct Python retrieval produced HTTP 403; an authorised desktop snapshot import worked. The immutable private site serves a verified snapshot, does not fetch automatically. Do not confuse a September 2026 source edition with last observation date (February 2026).

Remaining defects/unknowns: older Work research prototype and two Chinese local artifacts not recovered; current 2026 DP/OP content not fully verified; no demonstrated unattended ingestion or scheduler. Existing dirty worktrees and unrelated generated report edits are not to be touched; Draft PR #127 remains unmerged.

## 4. New public-source discovery (verify again before implementation)

**Key finding:** BOM Hydrologic Reference Stations (HRS) is designed for *long historical records* and reviewed/updated roughly every two years. Solving a single HTTP 403 on HRS cannot itself provide a current river-feed product. Preserve HRS as the historical/reference series.

Candidates to investigate in order, without presuming their current station coverage or permission:
1. WaterNSW official developer portal / Water Data API: https://api-portal.waternsw.com.au/ . Registration/subscription key required; price, entitlement, quotas, station 410033 support and reuse licence **unverified**. WaterNSW WaterInsights: https://www.waternsw.com.au/water-services/water-data/water-insights .
2. NSW public ArcGIS WaterInsights River_Gauge_Data layer: https://portal.data.nsw.gov.au/arcgis/rest/services/Hosted/WaterInsights_Data_Public/FeatureServer/1 . Fields include station_id, date_, flow_rate_, level_. Check actual 410033 station match, last-observed timestamp, units, provenance, update cadence, attribution and permission for repeated automated use; a public point layer may be only the *latest* snapshot, not historical time series.
3. BOM Water Data Online: https://www.bom.gov.au/waterdata/wiski-web-public/faq.htm . Often updated daily, but explicitly **not real-time**. SOS2 web service exists with anti-scraping/rate protections; respect documented rate bounds and owner licensing.
4. NSW SEED metadata API: https://www.seed.nsw.gov.au/help-guides/how-access-metadata-seed-api . It discovers data/resources, not a guaranteed live measurement feed.
5. HRS official FAQs: https://www.bom.gov.au/water/hrs/faq.shtml . Long-term reference context only.

Do not pay a scraping proxy, buy an API subscription, simulate human browsing to defeat an access control, or assume a DeepSeek tool grants data rights. If an endpoint rejects automation, record the 403/429, identify its formal access route, and move to approved alternatives. No external spending authorised.

**Scientific distinction:** Historical validated reference series and recent provisional operational observations differ in cadence, QC, local-day interval, units, schema and possible revisions. Maintain separate SourceRevision identities and link by a tested, explicit comparison protocol; never append blindly into one 'continuous and fully comparable' river record.

## 5. Next bounded work — P03 continuity first, public feed feasibility alongside

**P03-A — Monthly research evidence attachment (implement now).**
- Reuse existing monthly research Console / persistence, Run Receipt and Evidence Passport, not a new dashboard or OS.
- Attach the accepted HRS 410033 snapshot *read-only* as a source/version reference to ONE existing monthly research cycle with a provenance link, historical/stale status, spatial meaning and pending human scientific review.
- Do not rewrite already-reviewed cycles, promote evidence into statutory conclusions or mark it 'live'. Verify reload/idempotence, conflict, source hash and rollback.
- Tests and acceptance: same Source SHA, one cycle linked, owner-private page still works, source mismatch degrades to UNKNOWN, prior monthly outputs unchanged.

**P03-B — Recent public hydrology source feasibility (short spike, in parallel).**
- For WaterNSW API and the NSW River_Gauge_Data layer first, test discoverability, station match (410033 or explicitly alternative), public data/sample read, field units, source timestamps, update recency, provenance, licence, automation rights, quotas, costs, revised/QC status.
- Produce a short source decision matrix (VERIFIED / PARTIAL / BLOCKED) with exact URLs and response snapshots/hashes where redistribution is permitted.
- Implement only ONE small approved read-only incremental adapter if permissions and measurement semantics are explicitly verified; do not claim current or real-time if not. Display 'latest observed at' and 'last fetched at' separately.
- Test: 200 with new data; 200 unchanged; missing station; null/low quality; 403/429/5xx; new/changed schema; repeated fetch idempotence; no false fresh label.
- If access needs account/API key, return precise self-service authorisation steps for the founder; never hard-code credentials or create paid subscriptions.

**P06 dependency — Unattended updates, later.** Do not mark automated refresh VERIFIED until a legitimate scheduler/service identity performs a real no-human fetch, persists a revision, and independently reads it back; verify retry, stale-mode, rate controls, cost and failure notifications. Do not quietly turn a P03 experiment into a P06 deployment.

## 6. 90-day and 10-year return path

0–30 days: CSP × LSPS versioned crosswalk, 3 research hypotheses, evidence terminology, monthly cycle attachment and source feasibility report; baseline public data/reuse register.

30–90 days: one water/catchment research question with competing explanations and historical/current-source separation; a soil/vegetation public-data feasibility example; one external-independent check of ten source-to-claim references. Measure evidence accuracy and reproducibility before expanding the website.

1–2 years: worksite learning stays in approved Council systems; only abstract, non-sensitive concepts transfer. Independently review water–soil–carbon mechanisms, build scenario comparisons, verify any claimed interventions via suitable data/partners.

2–10 years: contribute to broader dryland ecological resilience, active controllable emission reduction, energy-water efficiency, land use and equitable regional development through lawful research/partners, then validate service/product demand separately. Geographic extension only after measured transferability.

## 7. Safety / governance boundary

Council systems remain authoritative; private ClimateOS must not import real customer identities, addresses, inspection details, sensitive asset topology, official photos, recordings, internal emails or confidential Council data. Use public, fictional, anonymised or abstract sources only. Keep fact, customer statement, officer observation, and modelling inference separate. Human scientific review is distinct from operational/government authorisation. No Council endorsement, financial approval, unpublished plans, or regulatory decisions should be implied.

Research may publicly reference a published government gauge or policy, but a private employee's inspection contacts or organisational access cannot be repurposed into lead generation. Conflict-of-interest/IP/secondary employment requirements must be checked before services or commercial pilots.

## 8. Immediate Codex continuation / gate

Read this document AND the latest EXECUTION_STATE.json/Issue #128/PR #129; compare actual HEAD, branch and worktree. Continue P03-A and a bounded P03-B source feasibility review. Do not rework P02. Preserve existing private site/version 2, earlier receipts, reports and unmerged Drafts. Commit verified changes only to the established implementation branch (or a clearly identified isolated worktree) and update Issue #128 + EXECUTION_STATE.json.

Deliver: actual code/test/commit for P03-A; a source/access/licence matrix and precise feasible next step for P03-B; human/authorisation blockers; one line for next Codex session. No silent new OS, automatic merge, public release or external spending.

## 9. Canonical continuation links

- ClimateOS task: https://github.com/simon947161/eco-agent-system/issues/128
- Draft implementation: https://github.com/simon947161/eco-agent-system/pull/129
- Owner-private demonstration: https://climateos-snowy-monaro.minshu.chatgpt.site
- P02 acceptance: docs/tasks/climateos_regional_public_os_001/P02_SITES_PRIVATE_ACCEPTANCE.md
- Source state: docs/tasks/climateos_regional_public_os_001/EXECUTION_STATE.json
- This handoff is a thematic transition from WCOS to ClimateOS; it does not relocate ChatGPT conversation history by itself.
