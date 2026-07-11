# Task671-680 External Model Adapter Readiness Review

## Purpose

Task671-680 reviews what ClimateOS must understand before any future external
scientific model adapter can be proposed.

This work is documentation-only. It does not connect to any external model,
call any provider, create an adapter, create an API, create runtime code, create
database schema, create automation, or begin Task681.

## Plain-Language Meaning

ClimateOS will eventually need to learn from many kinds of external models:
climate models, hydrology models, biodiversity models, energy models, urban
comfort models, satellite-derived products, and specialist research tools. The
question in this batch is not "how do we plug them in?" The question is "what
must be true before plugging anything in would be responsible?"

Task671-680 treats every external model output as a possible evidence
candidate. It is not proof by itself. It must carry method context,
assumptions, licensing, provenance, uncertainty, failure modes, and human review
requirements before it can support ClimateOS deliberation.

## Documents

- [Task671 Authorization And Adapter Review Boundary](TASK671_AUTHORIZATION_AND_ADAPTER_REVIEW_BOUNDARY.md)
- [Task672 External Model Category Map](TASK672_EXTERNAL_MODEL_CATEGORY_MAP.md)
- [Task673 Provider Output Evidence Candidate Distinction](TASK673_PROVIDER_OUTPUT_EVIDENCE_CANDIDATE_DISTINCTION.md)
- [Task674 Adapter Concept Versus Implementation Boundary](TASK674_ADAPTER_CONCEPT_VERSUS_IMPLEMENTATION_BOUNDARY.md)
- [Task675 Model Assumption And Provenance Review Checklist](TASK675_MODEL_ASSUMPTION_AND_PROVENANCE_REVIEW_CHECKLIST.md)
- [Task676 Cross-Domain Evidence Contract Mapping For Model Outputs](TASK676_CROSS_DOMAIN_EVIDENCE_CONTRACT_MAPPING_FOR_MODEL_OUTPUTS.md)
- [Task677 Private EcoEngine And Founder Reserved Model Boundary](TASK677_PRIVATE_ECOENGINE_AND_FOUNDER_RESERVED_MODEL_BOUNDARY.md)
- [Task678 Founder Gate Triggers For Future Model Integration](TASK678_FOUNDER_GATE_TRIGGERS_FOR_FUTURE_MODEL_INTEGRATION.md)
- [Task679 Task681-690 Gate Questions](TASK679_TASK681_690_GATE_QUESTIONS.md)
- [Task680 Closure Packet And Hard Stop](TASK680_CLOSURE_PACKET_AND_HARD_STOP.md)

## Current Capability

Current capability remains documentation and conceptual review only.

No external model connector, live model call, model execution, data retrieval,
runtime bridge, CLI, API, database, MCP server, automation, agent, sensor,
scoring system, certification process, deployment, or operational Evidence
Passport is created by Task671-680.

## Private Asset Boundary

Task671-680 does not access, scan, list, read, summarize, migrate,
reconstruct, upload, publish, or integrate any Founder-reserved private
EcoEngine asset or `D:\eco_engine_v200` material.
