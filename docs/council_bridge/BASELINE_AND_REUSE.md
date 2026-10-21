# Council Bridge baseline and reuse audit

Task: CLIMATEOS-BRIDGE-COUNCIL-001. Checked 2026-10-21 (Australia/Sydney).
Authoritative main: `9eb7577e145e76161f9f1cd8509348b19c2904cc`.
Isolated branch: `codex/council-bridge-001`. This checkout started clean; synced project `sources/` and other workspaces were not changed.

## Authority and history

The Founder supplied a new Council-level implementation task on 2026-10-21 authorising isolated implementation, synthetic verification, README updates, normal push and a Draft PR. It does not authorise main changes, old PR merges, contacts, private-code disclosure, paid compute or production deployment.

PR121's `TASK3000_HISTORY_PREFLIGHT_AND_FREEZE.md` permits a Founder-released bounded exception. This task supplies that exception for Council Bridge only. Task3000's mission/DNA review and PR120 HOLD are preserved. No claim that the wider freeze has ended; no old implementation is silently promoted.

## Remote state rechecked

| Work | State | Exact head |
| --- | --- | --- |
| PR118 Site Reading | Closed, merged | `247f94ab3d35a7983dce1956a4443833b7e6b189` |
| PR120 freshness/convergence | Open Draft | `f82d975526ea73f44d1d4a82cf3539f5b4d899b8` |
| PR121 mission review/freeze | Open Draft | `2bd582ef1df81accbee8538dffd04115c5634ca5` |
| PR125 farm evidence research | Open Draft | `f6787d9e7e759bc2b61b37da463609a587922144` |
| Issue126 orchestration | Open | Task specification, not execution proof |

Review refs 120/121/125 were fetched and their changed-file inventories inspected. No branch was merged. PR125's farm assumptions and PR120's implementation were inspected as reference; they remain in their original branches. Historical test counts are not this delivery's results.

## Reuse / extend / add / defer

| Need | Disposition and exact source | Entry/verification | Limit and Bridge treatment |
| --- | --- | --- | --- |
| Project lineage | REUSE `AGENTS.md`, `README.md`, `ROADMAP.md`, `CONTRIBUTING.md`, `docs/project-principles.md` | Read at main baseline | Preserve physical reality, stewardship, human judgement and feedback |
| Canonical serialization/digests | REUSE `cczps_lite/scientist_runtime/contracts.py` | Existing unit suite; imported by Bridge | Digest consistency is not authenticity |
| Time-bounded answer | REUSE `schemas/climateos_v2/time_bounded_environmental_answer.schema.json` | Existing schema; new end-to-end test checks required shape | Same schema identity; synthetic Bridge output held at L0/S0 |
| Evidence Passport | EXTEND representation used by `cczps_lite/site_reading/cooma.py` | `python run_cooma_site_reading.py --verify-fixture` | Preserve source/method/derived-claim/review/retrospective structure; no real evidence admission |
| Run Receipt | EXTEND existing receipt pattern | Bridge `progress` and provider tests | Provider/request/output/attempt identities; a distinct receipt subtype |
| Local persistence | REUSE SQLite/transaction pattern from `scientist_runtime/store.py` | Restart, rollback and audit tests | Separate node databases; no migration or coupling to old sessions |
| Question/research continuity | REFERENCE `environmental_question_runtime/program.py` and `continuity.py` | `run_environmental_question_runtime.py` | Old monthly records untouched; Bridge does not ingest them |
| Source admission | REFERENCE `integration/cooma_*`, `mittagang_*`, `waternsw_*` | Existing suite | Fixed gates retain scope; real receipt data is not relabelled synthetic |
| Spatial foundation | REUSE REFERENCES `qgis_local_spatial_foundation/contract.py` and site-reading spatial registry | Existing QGIS tests | Cooma navigation extent cannot become Council boundary; no QGIS binary required for Bridge |
| Freshness/convergence | DEFER PR120 implementation | Unmerged `evidence_watch/cooma.py`, 39 historical targeted tests reported | No cherry-pick; Bridge has only synthetic expiry/withdrawal checks, not real convergence |
| Farm case | PRESERVE PR125 | Original research paths and fixed PR head | Named child-case lineage, no copied assumptions or scientific promotion |
| Provider boundary | ADD narrow Protocol and mock implementations; REFERENCE Issue99 requirements | Compute contract and failure tests | No claim Issue99 backlog is implemented or real provider admitted |
| Council node/workspace | ADD `cczps_lite/council_bridge/` | `run_council_bridge.py` | Local synthetic rehearsal only |
| Federation | ADD approved local metadata exchange | Isolation, duplicate, expiry, withdrawal tests | Trusted same-host broker, not distributed federation |
| Identity | ADD local session capability and Council-scoped Principal | Host/origin/auth tests | One operator; no independent professional identity or signatures |

## Official context and boundary admission

- Council identity/context: https://www.snowymonaro.nsw.gov.au/Community/Welcome-to-the-Snowy-Monaro-Region . The official page confirms the Council name and former LGA composition. This is context, not an endorsement or live partnership.
- Candidate administrative boundary source: https://portal.spatial.nsw.gov.au/server/rest/services/NSW_Administrative_Boundaries_Theme/MapServer/8 . LocalGovernmentArea is a separate layer; parent service declares EPSG:3857.
- Dataset catalogue: https://data.nsw.gov.au/data/dataset/nsw-administrative-boundaries . Catalogue lists CC Attribution 3.0; the portal overview uses a broader Creative Commons label. This does not establish a version-pinned exact geometry licence.

Official context pages/service metadata checked 2026-10-21. No boundary features or environmental datasets were downloaded. Exact layer licence/attribution, feature identity, snapshot date, CRS transformation and geometry digest remain pending. `geometry=null`, `version=NOT_ADMITTED` are deliberate. The UI is a labelled relationship schematic, never a boundary map.

## Material gaps

Real Council pilot consent, authoritative geometry, representative observations, independent model evidence, scientific convergence, professional sign-off, multi-user identity, remote node authentication, signed exchanges, revocation delivery guarantees and live provider terms are not implemented. They require further bounded work and applicable authorisation.
