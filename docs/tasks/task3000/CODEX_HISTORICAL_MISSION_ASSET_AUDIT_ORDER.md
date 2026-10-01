# Codex Historical Mission & Asset Audit Order

## ClimateOS Task 3000 — Mission Reconstitution & ClimateOS DNA

**Status:** authorised research/evidence work only  
**Implementation:** prohibited  
**Network data fetch:** prohibited  
**Base:** current authoritative `main` at execution time  
**Founder brief:** `docs/tasks/task3000/TASK3000_FOUNDER_STRATEGIC_BRIEF.md`

---

## 0. Role

Codex is the historical archaeologist and asset auditor for Task 3000.

Codex does **not** define the new ClimateOS mission.

Codex must provide:

- primary-source repository evidence;
- chronology;
- crosswalks;
- contradictions;
- asset inventory;
- dependency and lineage maps;
- evidence for later Founder + ChatGPT judgement.

Do not convert current Founder language into historical fact unless a dated source supports it.

---

## 1. Hard stop on implementation

During this audit:

```text
NO NEW RUNTIME CODE
NO NEW SKILL IMPLEMENTATION
NO NEW AGENT
NO NEW MODEL INTEGRATION
NO DATA FETCH
NO API CALL
NO UI WORK
NO OLD-PR MERGE/CLOSE
NO REFACTOR
NO PRODUCT EXPANSION
```

PR #120 (`EP-SKILL-002: Offline freshness and convergence runtime`) already exists as a Draft implementation result. Preserve it exactly as evidence of the pre-Task3000 engineering frontier.

Do not merge, close, amend or discard PR #120 in this audit.

Likewise do not modify PR #115, #116 or other open PRs.

---

## 2. Primary research question

Answer with evidence:

> What has remained invariant in ClimateOS from its earliest reachable form to the current system, what changed materially, what was temporary, and what existing assets still serve the Founder-proposed ClimateOS DNA?

Separate every claim into one of:

```text
PRIMARY_REPOSITORY_EVIDENCE
FOUNDER_CURRENT_REFLECTION
INFERRED_CONTINUITY
DOCUMENTED_CHANGE
DOCUMENTED_CONTRADICTION
UNRESOLVED_PROVENANCE
```

Do not hide contradictions to make the history look cleaner.

---

## 3. Workstream A — Origin Reconstruction

Inspect the earliest reachable history and identify at least:

- repository initial commit(s);
- earliest `eco_agent_system/README.md`;
- root `README.md` revisions;
- `ROADMAP.md`;
- `docs/project-principles.md`;
- earliest CCZPS/EcoEngine definitions;
- Task001-era documents;
- Task001–640 ACTP/growth/working-mode records;
- N1/N2 references or evidence of absence;
- early Climate Leadership / Ecological Civilization records;
- early climate warning, planning, resilience and stewardship language.

For each source record:

```text
source_id
path
commit_sha
date
source_type
relevant_excerpt_or_paraphrase
mission_claim_supported
limits
superseded_by
```

Do not use current README text as a substitute for historical versions when Git history can recover the older source.

---

## 4. Workstream B — Evolution Map

Create:

`docs/tasks/task3000/evidence/CLIMATEOS_EVOLUTION_MAP_EVIDENCE.md`

Use this candidate sequence only as a hypothesis to test:

```text
Early Warning
→ Ecological Planning
→ Climate / Resource Coordination
→ ClimateOS
→ Agent / Evidence Architecture
→ Physical Consistency
→ Mission Control
→ Governance Runtime
→ Stewardship
→ Human Capability
```

For every transition identify:

- evidence-backed date/range;
- trigger/problem;
- new capability or concept;
- what improved;
- what became over-complex or was lost;
- what survived into later stages;
- confidence in the transition label.

If the evidence supports a different sequence, say so.

---

## 5. Workstream C — Founder Reflection Evidence Support

Do not write the final Founder Reflection in Codex's voice.

Instead create:

`docs/tasks/task3000/evidence/FOUNDER_REFLECTION_EVIDENCE_CROSSWALK.md`

Crosswalk the Founder-provided 2026 reflection themes against repository evidence:

- early-warning orientation;
- builder identity / real-world implementation orientation;
- frustration with warning-to-action gaps;
- stewardship transition;
- commercial / finance experimentation;
- public-good motivation;
- regulation as memory / governance learning where repository evidence exists;
- AI/agent expansion and later concern about overproduction;
- human decision boundary.

For each theme mark:

```text
REPOSITORY_CORROBORATED
PARTIALLY_CORROBORATED
CURRENT_FOUNDER_ONLY
NO_REPOSITORY_EVIDENCE_FOUND
CONTRADICTED_BY_REPOSITORY
```

The final first-person reflection remains Founder + ChatGPT work.

---

## 6. Workstream D — Asset Audit

Create:

`docs/tasks/task3000/evidence/CLIMATEOS_ASSET_INVENTORY.md`

Inventory major assets across at least:

- core deterministic engines;
- model registries and source registries;
- Agent/runtime components;
- Evidence Passport / Run Receipt / admission contracts;
- S0–S7 and L0–L4 systems;
- QGIS / Geo / GeoLibre-related assets;
- weather/climate sources;
- hydrology sources;
- Water components;
- Building-related concepts that live inside this repo;
- Carbon/ESG/EcoChain concepts;
- Mission Control/shared runtime material;
- Radar;
- regional pilots and fixtures;
- Planner Cycle;
- EP-SKILL-001/002;
- stewardship documents;
- climate leadership/civilization documents;
- commercial/GEGG material currently mixed into the repo.

For every meaningful asset classify:

```text
KEEP_CORE
MERGE_CONSOLIDATE
ARCHIVE_PROVENANCE
EXPERIMENT_OUTSIDE_CORE
REMOVE_FROM_CLIMATEOS_CORE
HUMAN_REVIEW_REQUIRED
```

Do not actually move/delete/merge anything.

Required fields:

```text
asset_id
name
path_or_pr
origin_task_or_commit
current_state
current_dependencies
mission_role
DNA_candidate_mapping
classification
reason
cost_of_retaining
cost_of_removing
unique_value
replacement_if_removed
uncertainty
```

---

## 7. Workstream E — Architecture / Dependency Compression Evidence

Create:

`docs/tasks/task3000/evidence/CLIMATEOS_DEPENDENCY_AND_LINEAGE_MAP.md`

Distinguish:

1. philosophical / mission layer;
2. environmental reasoning layer;
3. evidence/trust layer;
4. professional planning layer;
5. runtime/orchestration layer;
6. GIS/spatial tool layer;
7. provider/model/tool integrations;
8. application/domain extensions;
9. commercial/company material.

Mark dependencies as:

```text
ESSENTIAL
REPLACEABLE
OPTIONAL_PROVIDER
HISTORICAL_ONLY
WRONGLY_COUPLED
SHOULD_ROUTE_ELSEWHERE
```

Explicitly test whether the current system could survive replacement of:

- ChatGPT;
- Codex;
- DeepSeek;
- GeoLibre;
- QGIS;
- a particular weather provider;
- a particular model provider.

Do not claim a dependency is replaceable if the repository currently hardcodes it without an adapter or migration path.

---

## 8. Workstream F — DNA Mapping Evidence

Create:

`docs/tasks/task3000/evidence/DNA_TO_EXISTING_ASSET_CROSSWALK.md`

Do **not** define final DNA.

Use Founder candidate DNA only as test labels:

```text
CONTEXT
SENSE
FORESEE
KNOW
UNDERSTAND
RESPONSIBILITY
OPTIONS
ACT
VERIFY
LEARN
```

For each candidate map:

- existing supporting assets;
- missing capabilities;
- duplicated mechanisms;
- assets that do not map to any candidate;
- dangerous overreach;
- whether the candidate appears historically continuous or newly introduced.

Highlight any significant asset with `NO_DNA_FIT`.

---

## 9. Workstream G — First Human Journey evidence preparation

Do not build the user journey UI or final narrative.

Create:

`docs/tasks/task3000/evidence/FIRST_HUMAN_JOURNEY_INPUT_REQUIREMENTS.md`

Use the candidate case:

> ordinary NSW household

Define the minimum input evidence needed to answer:

> “作为这里的一个普通家庭，我今天应该知道什么？”

Cover only the minimum viable domains supported by evidence:

- location/context;
- climate/weather;
- water;
- land/terrain;
- shelter/building;
- energy where evidence exists;
- relevant rules/obligations;
- risk;
- evidence quality;
- responsibility/action boundaries.

Identify where ClimateOS currently lacks lawful/current sources or regulatory interpretation contracts.

Do not fill missing fields with generic advice.

---

## 10. Open-PR archaeology

Audit all open PRs and classify mission value, especially:

- #120 EP-SKILL-002 implementation — current frontier; HOLD during Task 3000;
- #116 Planner Cycle — extract possible long-term professional reasoning value;
- #115 Hydrology review — professional review boundary;
- #109 v2 ACTP/CRP provenance;
- #104 Mission Runtime — likely shared runtime, not ClimateOS core;
- #100 Earth System Ontology;
- #90 integrity covenant / Build Week history;
- #61 external model observation foundation;
- #50 hybrid weather preflight;
- #114 GEGG/GGG material — likely outside ClimateOS core.

Do not use GitHub mergeability as evidence of mission relevance.

Create:

`docs/tasks/task3000/evidence/OPEN_PR_MISSION_DISPOSITION.md`

This is recommendation only. Do not change PR states.

---

## 11. Required Evidence Pack

Create an index:

`docs/tasks/task3000/evidence/TASK3000_EVIDENCE_PACK_INDEX.md`

It must link all audit outputs and record:

- main/base SHA;
- command/query methods used;
- source count;
- commit range inspected;
- branches/PRs inspected;
- inaccessible/unreachable history;
- conversation-only gaps;
- known uncertainty;
- no-code/no-network attestation.

Evidence pack must include at minimum:

1. Origin reconstruction source register;
2. Evolution Map evidence;
3. Founder Reflection evidence crosswalk;
4. Asset inventory;
5. Dependency/lineage map;
6. DNA-to-asset crosswalk;
7. First Human Journey input requirements;
8. Open PR mission disposition;
9. unresolved provenance register;
10. executive evidence summary.

---

## 12. Explicit non-goals

Do not create:

- `CLIMATEOS_DNA_v0.1.md` final version;
- `EARTH_CITIZEN_CAPABILITY_MODEL_v0.1.md` final version;
- final Founder Reflection;
- final Task 4000 architecture;
- new runtime code;
- new UI;
- new model/provider integration;
- new commercial strategy;
- marketing/valuation material.

Those require Founder + ChatGPT judgement after the Evidence Pack.

---

## 13. Execution checkpoints

Use bounded checkpoints:

```text
CP1 — repository/history source map
CP2 — origin reconstruction
CP3 — evolution + Founder crosswalk
CP4 — asset inventory
CP5 — dependency + DNA crosswalk
CP6 — human journey input requirements
CP7 — open PR mission disposition
CP8 — evidence pack validation and Draft PR
```

Each checkpoint must produce durable files before continuing.

No checkpoint may end only with planning prose.

---

## 14. Final delivery

Open one Draft PR from a fresh branch based on then-current main containing only Task 3000 evidence/audit documents.

Do not merge it.

Return:

```text
=== TASK3000 CODEX HISTORICAL MISSION & ASSET AUDIT DELIVERY ===

STATE:
DELIVERED_FOR_FOUNDER_REVIEW / PARTIAL / BLOCKED

BASE_MAIN_SHA:

BRANCH:

DRAFT_PR:

PRIMARY_SOURCES_INSPECTED:

COMMITS_OR_HISTORY_RANGE:

OPEN_PRS_INSPECTED:

ORIGIN_RECONSTRUCTION:

EVOLUTION_MAP:

FOUNDER_REFLECTION_CROSSWALK:

ASSET_INVENTORY:

DEPENDENCY_MAP:

DNA_CROSSWALK:

FIRST_HUMAN_JOURNEY_INPUTS:

OPEN_PR_DISPOSITION:

UNRESOLVED_PROVENANCE:

CODE_CHANGED:
NO

NETWORK_DATA_FETCHED:
NO

PR120_CHANGED:
NO

PR115_CHANGED:
NO

PR116_CHANGED:
NO

FOUNDER_DECISION_REQUIRED:
MISSION / DNA / ASSET DISPOSITION REVIEW

RESUME_POINTER:

=== END DELIVERY ===
```

Stop in Founder Review.
