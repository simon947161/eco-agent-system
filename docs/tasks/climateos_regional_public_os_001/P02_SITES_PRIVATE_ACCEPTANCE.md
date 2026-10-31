# P02 private Sites acceptance — 2026-10-26

Status: **VERIFIED**. Owner browser completion is recorded in the final addendum below. Earlier pending statements describe the pre-login stage. Private deployment, server-side access, source matching and rollback/restore are verified. No public publication or Draft merge occurred.

## Actual site and access boundary

- Site: `appgprj_6adefcfe720881918b4e32874f12dd86`.
- URL: https://climateos-snowy-monaro.minshu.chatgpt.site
- Access: Sites `custom` policy revision 1; sole allowed viewer is the owner; no editors, groups or external visitors. Rechecked after rollback/restore. No unrelated Site changed.
- Sites dispatch performs server-side authentication/authorization before the Worker for HTML, scripts and APIs. Private deploy operations independently verified the owner-only policy. Hidden URLs and frontend controls are not the security mechanism.
- Anonymous GETs for `/`, `/api/streamflow`, `/api/release`, `/streamflow.js`: **401**, no source data/Receipt leaked. Spoofed `oai-authenticated-user-id/email` without legitimate authorization: **401**.
- Supported Sites service authorization: `/api/release` and February API **200**. Credentials used only in hidden stdin/process memory, never committed or written to disk. Service access does not manufacture human identity or prove a human login journey.
- Real browser showed the platform sign-in gate; sign-in link led to ChatGPT authentication. The owner completed ChatGPT authentication directly; authenticated hosted browser displayed the research page, 28 February records and linked evidence. No password or code was collected in chat.

## Snapshot provenance and integrity

Source SQLite remains local, read-only during export. Export requires raw SHA256, reparses raw using the existing Python parser, compares every persisted source row/header and verifies the existing Receipt. Nothing is fetched from BOM during this stage. No raw SQLite, private paths, Council records or Work content exported.

| Item | Accepted value |
|---|---|
| Source | BOM HRS / WaterNSW, 410033, Mittagang Crossing, upstream catchment 1889.8 km² |
| Source edition | September, 2026; **not the last observation date** |
| Coverage | 1964-03-01–**2026-02-28**, 22,645 daily records |
| Source SHA256 | `78e8188f3f445afa33ad466dd0554e653761ef617832b6df3a9eac6b1240ca1a` |
| Index SHA256 | `bd4728ea129330d5e1abd35dce9b223df87c6801c18ad52e7d9db0eb7e0d45ca` |
| Data-package SHA256 | `f664b75674059bcdd907941afcfdf0b6c4a19ffa79f3835bfaa79b5967097452` |
| Input implementation baseline | `6ca8f9d913e99ba66d4743790b2e4f0df11cf571` |
| Hosted implementation | `6a5c3b88af4536066fbc66f379decd74318e6571` |
| Receipt | `HRS-RECEIPT-E70B4670978ABFD6` |
| Passport | `HRS-PASSPORT-3CCD749190E38305`; human scientific review pending |
| Licence | CC BY 3.0 AU, © WaterNSW; BOM attribution and transformation notice retained |

63 annual shards plus index and independent manifest (65 JSON files). Exported twice to separate directories: byte-identical. Corrupted raw snapshot and changed metadata were rejected. Cross-platform `.gitattributes` pins checksum-bearing files to LF. Digests detect corruption, not malicious authorized replacement of both code and trust root.

Versioned immutable Worker bundle is the storage for this bounded snapshot; D1/R2 are unused, no Python/SQLite assumption at runtime. Each API response is limited to at most 366 calendar days; only relevant shards are parsed. No standalone shard-download or write endpoint. Index digest is checked before API use and selected shard hashes before parsing; corruption/missing selected shard returns **503** with no records. No automatic upstream fetching or paid dependency.

The page retains original quality codes; E unreliable is shown separately from A/B, with an accessible data table. G means gap-filled, not measured. Header `Flow (ML)` versus description `ML/day`, 09:00 local reporting with unspecified UTC offset, and `4/06/2024` extraction date versus later records remain explicit. No causal, pollution, drinking-water capacity or official decision claim. Historical/stale status and **Python HTTP403 / automatic updates not established** are visible.

## Actual acceptance checks

| Criterion | Result |
|---|---|
| Server-side private authorization | Verified policy, anonymous/spoofed identity401, authorized service200; owner ChatGPT browser sign-in verified |
| Local/hosted data match | All returned February rows exactly equal local shard; source/index/package hashes match |
| February 2026 | 28 records, 2026-02-01–2026-02-28; E present |
| Evidence | Source header, quality, station/catchment, licence, Receipt/Passport and release provenance read back |
| Corruption | Index, selected shard and missing shard rejected; exporter rejects raw/metadata tampering |
| Failure/empty/stale UI | Local browser: oversize gives unavailable and clears chart/table; authenticated hosted browser: empty March gives no-data/28 absent dates and clears chart/table; February stale status visible |
| Desktop/mobile | Local browser interaction passed; 390px requested mobile viewport rendered at375px CSS content width, no horizontal overflow; authenticated hosted desktop/mobile also passed |
| Regression | Existing HRS4 passed; Worker8 passed; full Python493 OK, 1 skipped in isolated copy |
| Deploy and rollback | Version2→version1→version2 all native succeeded; release SHA/28 rows/anonymous401 verified at each checkpoint |

Commands:

```text
python -B tools/export_hrs_sites.py --db .local/p02-verified.sqlite3
node --test apps/regional-public-os/tests/worker.test.mjs
node apps/regional-public-os/scripts/build.mjs
node apps/regional-public-os/scripts/validate-artifact.mjs
python -B -m unittest discover -s tests -p test_hrs_streamflow.py -v
python -B -m unittest discover -s tests
```

Full regression ran from an isolated source copy, using workspace-local temporary storage and authorized localhost sockets. Four pre-existing generated reports were SHA256 checked before/after and remain unchanged, unstaged. Core Python/SQLite importer and policy Console were not rewritten. Existing PR129 continues; PR127/129 remain unmerged.

## Exact releases and rollback procedure

Machine-readable records: `P02_SITES_DEPLOYMENT_MANIFEST.json`, `P02_SITES_ACCESS_EVIDENCE.json`. Do not confuse GitHub implementation SHA with Sites source SHA.

| Version | GitHub implementation | Sites source | Saved version ID suffix |
|---|---|---|---|
| 1 | `cff9ea16dd945b91e4b37cf8a9502ee23846caf6` | `34d34d6fb82398ca072b3902969c3bc7d5322a8f` | `appgver_f71958ef4d248191a9082801bb59fede` |
| 2 (restored/current) | `6a5c3b88af4536066fbc66f379decd74318e6571` | `9f3a201d40c4b70d72f0b69c319805258769c242` | `appgver_6e7858f94ab881918228f1f9a742ff59` |

Initial v1 deployment: `appgdep_6adefed4f16c8191850ef882bd88e9ac`. V2: `appgdep_6adeffea197881918728459d994ca0e9`. Rollback v1: `appgdep_6adf004bb3b48191899ebf9318bf029c`. Restore v2: `appgdep_6adf008a3d1c81918a673531038410d1`. All succeeded. V2 archive SHA256: `451ef5d3df12c32ac0ed865b07fe490299c05941077d847a54693eb8e8a7022e`.

To repeat rollback:

1. `get_site` for the saved project; confirm sole owner/no groups/editors/external visitors. Stop on audience mismatch; never use public deployment as fallback.
2. `deploy_private_site_version` with project ID and full version1 ID `appgprj_6adefcfe720881918b4e32874f12dd86~appgver_f71958ef4d248191a9082801bb59fede`.
3. Poll the returned deployment ID only if nonterminal; require succeeded. Authorized `/api/release` must identify GitHub `cff9ea1…`; February must still have28 unchanged records; anonymous API must401.
4. Restore by deploying existing full version2 ID `appgprj_6adefcfe720881918b4e32874f12dd86~appgver_6e7858f94ab881918228f1f9a742ff59`. Require succeeded and GitHub `6a5c3b8…` plus `P02_PRIVATE_ACCEPTANCE`, matching hashes/28rows/anonymous401.

No rebuild, source overwrite, force push, data mutation or access change is needed for rollback. Local source-package credential expired once; renewed for this same project, no duplicate Site or version creation attempt for the expired push.

## Remaining and next minimum task

Next minimum task is P03: attach this accepted snapshot/Receipt/Passport as a read-only evidence reference to one existing monthly research cycle. Preserve scientific-review pending and historical status. Automatic updates, scientific approval, recovered Work prototype and KITTY scheduler remain outside this acceptance. No need to repeat policy Console engineering or rebuild the snapshot.

Conversation Radar: knowledge—private dispatch gates APIs as well as pages; decision—immutable versioned snapshot, no D1/R2 or new research core; risk—human sign-in still unverified, stale source/quality ambiguity retained; open question—owner post-login journey; next action—finish that bounded check; keywords—ClimateOS/P02/Sites/410033/Receipt/Passport/private-access/rollback.

## Owner browser completion addendum

Owner completed sign-in in the test browser. On the real deployed version2, February2026 returned28 records and the Evidence details contained the accepted Passport. Selecting March1�28 returned0 records/28 absent dates and cleared the chart. At a requested390px mobile viewport (375px CSS content area), selecting February again returned28 records with distinct quality styling, stale label and no horizontal overflow. Temporary viewport override reset; owner Site tab retained as deliverable. This completes the previously pending human-browser criterion. Deployment version/source/hashes are unchanged; only acceptance records were updated.
