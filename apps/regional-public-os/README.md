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
