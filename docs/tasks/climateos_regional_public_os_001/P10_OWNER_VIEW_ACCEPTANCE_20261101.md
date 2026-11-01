# Owner research progress/evidence view — 2026-11-01

**PASS: bounded local product batch. NOT_DEPLOYED. P08/P10 remain partial; no scientific gate has passed.** Continues Draft PR #129 from `9a2f31660889e6272cdeb8a21d34583c838947c3`. PR #130 and the existing private water Site were not changed.

## Founder-readable result

The existing app now has a Chinese read-only page, `/research`, linked from the historical flow page. It explains three different levels of progress:

- **P02: published private historical website.** 22,645 HRS daily records, 1964-03-01 through 2026-02-28. September2026 is the dataset label, not observation freshness. Publication is identified by the previously recorded Sites v2 source/implementation SHAs and 2026-10-26 acceptance; this batch does not recheck the live site.
- **P03: verified retrospective reference, not on Sites.** Repository acceptance says one supplementary HRS reference was attached to the existing July2026 local cycle after its original review. No original monthly database was read, exported or migrated for this view; the original records and Receipt remain untouched.
- **P04: limited soil finding, rainfall still blocked.** The already recorded one-cell July2000 result agrees with the mean of31 daily soil values, not the final-day value. This is not a general product contract or catchment/scientific admission. Exact rainfall daily/monthly lineage remains unverified; the prior ArcGIS499 Token Required inventory action is explicitly stopped.

The page states **automatic updates have not been established** and **NOT_DEPLOYED**. It does not suggest ClimateOS as a whole is complete. Existing owner-private [Sites v2](https://climateos-snowy-monaro.minshu.chatgpt.site) remains the historical HRS release. Parent review and a separate publication decision are next; no credential or taskbook transfer is needed from Founder for this implementation.

## Actual implementation and evidence binding

- Existing `apps/regional-public-os` Worker only; no new app, framework, hosting service, dependency, database or account.
- New `worker/research.html`, `worker/research.js`, `worker/research-progress.mjs`; route additions in `worker/handler.mjs`; navigation link only in the old `worker/page.html`.
- `scripts/generate-research-progress.mjs` produces [research-progress.json](../../../apps/regional-public-os/data/research-progress.json) from eight fixed public-safe Git blobs at baseline `9a2f31660889e6272cdeb8a21d34583c838947c3`. It records full source commit, file path, SHA256, byte count, record date, scope and pinned GitHub URL. Original task records, not copied monthly research data, support the cards.
- Manifest SHA256: `de1ae2d9ee11b9bc4f30eb551e1183f4082a2a88bcb34f938c4716295422ab29`. Evidence-as-of2026-10-31; manifest generated2026-11-01. The evidence SHA is intentionally distinct from the new implementation SHA.
- Build compares the entire manifest against deterministic regeneration from the pinned blobs. It rejects changed prose, changed digest receipts and wrong source bindings. Runtime checks the bundle-pinned manifest digest plus source/card/path/URL/date/state bindings. Hash trust assumes code/trust-root review, not resistance to a malicious authorized replacement of both.
- Unknown/corrupt/missing/future state returns503 with no cards. After the seven-day manual status-review window, **all** cards become `STALE_SNAPSHOT`; last-known records remain visible with explicit stale language. Seven days is a conservative UI review convention, not a scientific data expiration rule. No provider refresh or live-status claim occurs at any age.
- `/api/research-progress`, `/research`, `/research.html`, `/research.js` remain GET/HEAD only with private/no-store headers and same-origin CSP. Unknown query parameters are rejected. Existing Sites dispatch remains the required hosted access boundary; no standalone public origin is created.
- `scripts/build.mjs` still emits the single-module Worker. Release metadata now says `OWNER_RESEARCH_PROGRESS_PREVIEW`, `NOT_DEPLOYED`, code HEAD and dirty-worktree flag. `package.json`, README and a read-only CI workflow cover the new checks/build. `.openai/hosting.json`, all63 HRS data shards/index/manifest, original streamflow.js and scientific evidence are unchanged.

## Validation actually run

| Check | Result and scope |
|---|---|
| Node tests | **17/17 PASS**:9 new progress tests,8 existing HRS Worker regressions |
| Evidence link validation | All8 unique URLs resolve to existing local Git blobs at the exact pinned commit; lengths/SHA256 regenerated and entire manifest byte-matched. No HTTP requests to providers or GitHub links during this check |
| Negative cases | Wrong path/card/date/commit/link, unsupported state/schema, future/unknown clock, manifest absence/corruption, fabricated claim/digest, unsafe release/automation/scientific promotion all rejected |
| Staleness | Nov7 end of day still inside review window; Nov8 all cards marked stale. Last-known evidence preserved, never relabelled live |
| Existing HRS/monthly Python | **9/9 PASS**; test fixtures only, no original database |
| Full Python regression | **533 run,529 passed,4 skipped**, exit0, isolated tracked-source copy; skips are existing optional GIS audit dependencies. No generated output pollution in working checkout |
| Build / artifact | Deterministic evidence check, build and generated ESM/default.fetch validation PASS; no deployment |
| Desktop browser | Chromium1440px:3 cards, publication/automation markers, keyboard evidence disclosure, pinned links, no horizontal overflow |
| Mobile browser | Chromium390px:3 cards and all expanded paths/hashes readable without horizontal overflow; HRS February28 rows, stale label, empty March clears rows, navigation back |
| Browser failure modes | Explicitly simulated stale,503 unavailable and unknown-state responses show warning or hide all cards. No JavaScript page errors; zero external browser requests |

The first browser-test attempt used a string-expression polling helper that collided with the existing CSP during the HRS empty-state wait. The harness was corrected to locator assertions; CSP and application code were not relaxed. The full browser check then passed. This was a test-harness issue, not an unavailable feature or bypass.

Committed [browser result](evidence/p10_owner_view_20261101/browser-result.json) records the precommit local QA release as baseline plus `working_tree_dirty=true`; it does not pretend that baseline alone contains the new UI. After committing, rebuild from the clean exact HEAD and verify `/api/release` before handoff. GitHub CI/remote SHA are reported from actual post-push results, not predicted here.

Screenshots, all local preview and public-safe metadata:

- [Desktop](evidence/p10_owner_view_20261101/desktop.png)
- [Mobile](evidence/p10_owner_view_20261101/mobile.png)
- [Simulated expired snapshot](evidence/p10_owner_view_20261101/stale-mobile.png)
- [Simulated unavailable evidence](evidence/p10_owner_view_20261101/unavailable-mobile.png)

## Reproduce, generated outputs and rollback

From repository root:

```sh
node apps/regional-public-os/scripts/generate-research-progress.mjs --check
npm test --prefix apps/regional-public-os
npm run build --prefix apps/regional-public-os
npm run validate --prefix apps/regional-public-os
node apps/regional-public-os/scripts/preview.mjs
# Local browser only: http://127.0.0.1:8788/research
# In a second terminal, with already installed Playwright and Chromium:
python apps/regional-public-os/tests/browser_qa.py --output .local/p10-owner-view/browser
python -B -m unittest tests.test_hrs_streamflow tests.test_monthly_evidence_links
```

Full `python -B -m unittest discover -s tests` runs in an isolated tracked-source copy because existing tests generate reports. No dependency was installed in this batch.

| Generated output | Producer / source / behavior / consumer |
|---|---|
| Committed `apps/regional-public-os/data/research-progress.json` | Generator without `--check`, eight fixed local Git blobs only; deterministic overwrite; build/UI consumer; unavailable source or unexpected state throws, never invents data; deployment NOT_DEPLOYED, scientific_admission false, automation NOT_ESTABLISHED |
| Ignored app `dist/server/index.js` and `dist/.openai/hosting.json` | Existing build, existing HRS snapshot plus new manifest/UI; overwritten each build; loopback preview only in this batch; no credentials or new network operation |
| Committed `evidence/p10_owner_view_20261101/*` | Optional loopback browser QA screenshots/result; exact bytes copied from ignored local output; includes clearly simulated negative states; tests fail on unexpected state rather than emitting PASS; reviewer-only acceptance artifacts, not a website deployment |
| Ignored `.local/p10-owner-view/*` | Regression copy/log and QA artifacts; no original private source files; no operational consumer or background job |

No live data acquisition, database mutation, automated spending, permissions, credentials, source access retries or scheduler was added. The read-only page has no live API consumer requiring a new Budget Guard exemption. Rollback is an ordinary revert of this implementation batch, preserving concurrent work. No deployed-site or database rollback is necessary.

## Unchanged blockers and next action

Rainfall lineage remains `BLOCKED_EXACT_DAILY_MONTHLY_LINEAGE_UNVERIFIED`; the specific official inventory schema action previously returned HTTP200/ArcGIS499 Token Required (confirmed denial, not pending or uncertain). This batch did not retry it or any known404, and did not acquire tokens. WaterNSW's current credential binding remains blocked with zero authenticated requests. HRS daily/DST, monthly QC/completeness and catchment admission remain independent unresolved gates. The working soil result was displayed from existing evidence, not recomputed or broadened.

Parent should review this local product result and explain it to Founder; any website publication is a separate decision. P08 public deployment acceptance and full P10 long-term operations remain unfinished. No merge or publication was performed.
