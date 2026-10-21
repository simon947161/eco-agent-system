# ClimateOS

**Trustworthy, time-bounded local environmental intelligence — connecting global, regional and local evidence while preserving human responsibility.**

ClimateOS helps environmental practitioners, land managers, communities and infrastructure stewards organise evidence around practical questions, compare possibilities, review uncertainty and learn from outcomes.

This repository retains the historical name `eco-agent-system`. Its accepted foundations include local research runtimes, evidence admission, official-data pilots, QGIS spatial-workbench workflows and bounded Cooma site reading. The [original README](docs/council_bridge/LEGACY_README_2026-09-28.md) is preserved as history; its relative links refer to the repository root.

## Council-level Bridge

The standard implementation unit is a **Council**, including its jurisdiction and responsibilities. Farms, settlements, catchments, ecosystems and infrastructure are connected local objects. The earlier hypothetical farm remains a child case, not the whole deployment scope.

This branch adds an offline Council Bridge rehearsal:

```text
Question and scope → evidence → compute request → quarantined result
→ local fitness check → human review → time-bounded answer → outcome record
```

Snowy Monaro Regional Council is the first candidate context. Official boundary geometry is not admitted. The second node is fictional. Neither is a real Council deployment or endorsed service.

```bash
python run_council_bridge.py
```

Open the full local URL printed by the process. It runs on loopback only, uses Python's standard library, and stores ignored runtime data locally. See the [Bridge guide](docs/council_bridge/README.md) for the complete walkthrough and limitations.

## What is implemented

| Capability | Current scope |
| --- | --- |
| Environmental question and persistent research workflows | Local questions, research cycles, receipts and human review |
| Scientist runtime | Deterministic structuring and fixed synthetic execution; not an autonomous scientist |
| Evidence admission | Source identity, provenance, spatial/temporal fitness and bounded official-data pilots |
| QGIS workbench | Cooma terrain/hydrology/spatial-context builder workflows; not causal inference |
| Site Reading | Accepted bounded historical context and evidence requests; current-flow/trend gaps remain |
| Council Bridge | Separate local node databases, spatial relationship schematic, exact synthetic requests, mock compute, L0/S0 answers, demo review and outcome records |
| Evidence Commons rehearsal | Preview, exact approval and export of synthetic metadata; same-host broker exchange, expiry and withdrawal reconciliation |

The Bridge uses existing canonical digest helpers and the Time-Bounded Environmental Answer schema. It follows existing Passport and Receipt patterns without importing private records or merging old draft work.

## What remains unconnected

- Representative real multi-source Council assessments and retrospective model-skill validation.
- Verified, version-pinned Council geometry and its exact licence/attribution.
- Global/regional model computation and real Matrix One access.
- Independent scientific/professional sign-off.
- Multi-user identity, signed cross-host federation and production deployment.

Synthetic, historical, observed, projected and modelled evidence must remain distinguishable. Accepting a workflow demonstration does not create an environmental conclusion. Missing evidence stays visible.

## Existing local entry points

```bash
python run_environmental_question_runtime.py
python run_scientist_runtime.py
python run_cooma_site_reading.py --verify-fixture
```

The environmental-question server uses port 8766, the fixed scalar demonstration 8765, and Council Bridge 8767. They have separate purposes and storage. The existing research workflow's manual allowlisted source refresh does not grant Bridge permission to fetch data.

## Work status checked 2026-10-21

| Work | State |
| --- | --- |
| PR118 Site Reading | Merged |
| PR120 offline freshness/convergence | Draft; not merged |
| PR121 Task3000 mission review | Draft; broader freeze preserved |
| PR125 hypothetical farm evidence | Draft; preserved as lineage |
| Issue126 agent/tool orchestration | Task registered; execution must be independently verified |
| Council Bridge | Isolated local synthetic implementation in this branch, awaiting review |

The Founder supplied a bounded Council Bridge implementation authorisation. It does not approve old PR merges, a mission rewrite, external contacts, private disclosures, paid compute or production activation.

## Verification and documentation

```bash
python -m unittest tests.test_council_bridge
python -m unittest discover
```

- [Bridge operation and architecture](docs/council_bridge/README.md)
- [Baseline, reuse and official-source checks](docs/council_bridge/BASELINE_AND_REUSE.md)
- [Validation and delivery status](docs/council_bridge/VALIDATION.md)
- [Unsent partner entry pack](docs/council_bridge/PARTNER_ENTRY_UNSENT.md)
- [ClimateOS v2 architecture](docs/architecture/climateos_v2_review/README.md)
- [Project principles](docs/project-principles.md)
- [Contributing](CONTRIBUTING.md)

## Collaboration and licence

Contributions are welcome in environmental methods, local evidence, uncertainty, adapters, professional review and usable workflows. Include source, scope, validation and limitations. Do not commit personal, customer or Council-internal records, secrets or unauthorised material.

Maintained by **Min Shu / Simon Shu**. Repository code uses the [MIT License](LICENSE); third-party data, models and services retain their own terms.
