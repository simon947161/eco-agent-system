# P02 private Sites adapter

This is the read-only hosted adapter of the existing HRS Console, not a new research system. It uses the original streamflow.js unchanged. Python/SQLite remain the authoritative local replay.

## Build and checks

From repository root:

```powershell
python -B tools/export_hrs_sites.py --db .local/p02-verified.sqlite3
node --test apps/regional-public-os/tests/worker.test.mjs
node apps/regional-public-os/scripts/build.mjs
node apps/regional-public-os/scripts/validate-artifact.mjs
```

Export checks pinned raw SHA256, reparses raw bytes with the existing parser, compares all 22,645 records with SQLite and verifies the existing Receipt. It emits calendar-year shards, index and independent manifest. No raw SQLite, private paths, source session or credentials are exported. Conversion is deterministic; source observations and original quality flags are unchanged. Metadata retains source header, version, attribution, licence, Receipt, Passport and limitations.

The Worker embeds the verified index and shards server-side. Only requested shards are parsed; HTTP responses are limited to 366 calendar days. It serves no shard-download or write route. Index is pinned at build; selected shards are SHA256 checked before use. Hashes detect accidental corruption; authorized code changes can replace the trust root, so this is not a digital signature.

## Identity and storage

Sites dispatch owns authentication and authorization for the entire hosted origin, including API and JavaScript routes. The Site must remain owner-only (`custom`, sole owner viewer, no groups/editors/external visitors); the native private deploy operation rechecks this. Identity comes from Sites-injected `oai-authenticated-user-*` headers; service access is separately validated/consumed at dispatch. Do not trust client-supplied identity headers, implement a second login, or deploy this Worker at a separate public origin. No standalone Workers URL is supported. If the platform boundary cannot be confirmed, stop deployment as PRIVATE_ACCESS_BLOCKED.

Snapshot storage is immutable in the versioned Worker bundle; D1/R2 are unused (`null`). No Python or local SQLite at hosted runtime. Responses are private/no-store with no permissive CORS. Local loopback preview intentionally lacks hosted identity and cannot validate hosted access control.

## Deployment and rollback

Use the Site ID in .openai/hosting.json. Build only from a committed GitHub implementation; build output embeds that GitHub SHA. Copy the exact generated Worker and manifest to a separate ignored Sites source checkout. Push/package that checkout using the Sites source helper. Save/deploy with the exact returned Sites source SHA and archive, through save_version_and_deploy_private only. Record GitHub SHA, Sites source SHA, snapshot hashes, saved version and deployment ID together.

Rollback uses deploy_private_site_version with the exact previously saved version ID, on this same owner-private Site. It must not rebuild, overwrite source data or change audience. Verify /api/release and February 2026 records after rollback; restore the accepted release by redeploying its existing saved version. Credentials stay in session memory/stdin and never source or reports.

See docs/tasks/climateos_regional_public_os_001/P02_SITES_PRIVATE_ACCEPTANCE.md for actual status and version evidence. Current dataset ends 2026-02-28; September 2026 is the dataset edition. Python refresh HTTP403 and no automation remain explicit.
# Owner research progress preview — 2026-11-01

`/research` adds a read-only progress/evidence view to this same adapter. **NOT_DEPLOYED**: existing owner-private Sites v2 is unchanged. `/` remains the HRS chart. This is a bounded P10/P08 contribution, not completion of those task packages or scientific acceptance.

The three cards distinguish P02 published private historical HRS, P03 repository-verified retrospective monthly references not on Sites, and P04's single-cell July2000 soil comparison with stopped rainfall lineage work. Automation is absent. The view does not read/export any monthly database, fetch providers, migrate records or schedule work.

`data/research-progress.json` is a committed generated manifest. `scripts/generate-research-progress.mjs` reads only eight allowlisted public-safe repository files using `git show` at **9a2f31660889e6272cdeb8a21d34583c838947c3**. It stores exact blob SHA256/length, pinned GitHub links, evidence dates and scopes. It never treats current working-tree execution state as new evidence. Keep that commit available (full-history checkout in CI); a missing blob, unrecognized source state or projection mismatch stops the build. Refreshing the reviewed snapshot requires an explicit code/evidence-contract update, not changing a date or rerunning a provider call.

```sh
node apps/regional-public-os/scripts/generate-research-progress.mjs --check
npm test --prefix apps/regional-public-os
npm run build --prefix apps/regional-public-os
npm run validate --prefix apps/regional-public-os
node apps/regional-public-os/scripts/preview.mjs
# Open http://127.0.0.1:8788/research locally; not a shareable deployed website.
# Optional browser QA with already installed Python Playwright and /usr/bin/chromium:
python apps/regional-public-os/tests/browser_qa.py --output .local/p10-owner-view/browser
```

Run the generator without `--check` only to overwrite the manifest deterministically from the fixed Git evidence. Build always compares the complete generated bytes, including claims and hash receipts. At runtime the manifest's bundle-pinned SHA256 and fixed source/card bindings are checked before `/api/research-progress` returns cards. Unknown/corrupt/future-dated evidence gives 503 and no cards. Older than seven calendar days from `evidence_as_of` gives `STALE_SNAPSHOT` on **all** cards, retaining clearly labelled last-known records. Seven days is a manual status-review convention, not scientific freshness. No live status is claimed, even inside that window. Digests do not defend against an authorized replacement of both code and trust roots.

New routes inherit the existing private/no-store, same-origin CSP and read-only policy. Sites dispatch would still need to gate all routes in any separately authorized publication; loopback QA does not validate hosted authorization. `dist/server/index.js` remains the ignored single-module generated artifact. Its release metadata identifies the code HEAD, dirty-worktree flag, `NOT_DEPLOYED` and the distinct evidence baseline. `.openai/hosting.json` and HRS data are unchanged. CI tests/builds only; it does not deploy.

Acceptance and public-safe screenshots: `docs/tasks/climateos_regional_public_os_001/P10_OWNER_VIEW_ACCEPTANCE_20261101.md`. Rollback is a normal revert of this batch; no database or deployed-site rollback is involved.
