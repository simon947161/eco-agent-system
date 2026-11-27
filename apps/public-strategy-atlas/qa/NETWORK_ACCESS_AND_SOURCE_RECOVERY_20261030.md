# Atlas official-source network access review & controlled recovery
**Date:** 2026-10-30 Australia/Sydney  
**Status:** ENVIRONMENT_SETTINGS_REVIEWED_AS_PROPOSAL / NOT_SAVED_OR_PUBLISHED / RUNTIME_UNBLOCK_UNVERIFIED  
**Target:** existing Codex Cloud environment used for PR #130; **not** the Atlas website deployment and **not** the GitHub repository/network settings.

## 1. Independently confirmed baseline and failure mode

GitHub PR #130 was OPEN / DRAFT / NOT MERGED at HEAD `026d8cc19b4f1df61a55bda734fbe9657af25ddd` before this review. Read `qa/V1_6_SYSTEM_RESULTS.md`, `qa/V1_6_ACCEPTANCE.json`, `qa/system/source-access.json` and `NEXT_SESSION.md`.

The executable test report states **15 native files and 6 actual Chromium runners PASS**, with 98.35% line and 83.18% branch coverage on *loaded Node engine modules only*, not the complete browser UI. Full V1.6 remains PARTIAL: current fresh official PDF retrieval, permission/rights, edition review and formal relationship admission are uncompleted.

Six attempted official URLs in `qa/system/source-access.json` failed with `Tunnel connection failed: 403 Forbidden` during proxy CONNECT (2026-10-29T11:19:48Z). This is consistent with **restricted cloud-task internet allowlisting**, not a missing GitHub token. No credentials, bypass switches or private endpoints should be added.

A **separate public web research interface** could read the Council's official IP&R HTML directory and index its public links on 2026-10-30; this does **NOT** show that the Codex runtime was repaired, and no original PDF bytes were imported or admitted into Atlas.

## 2. Proposed minimal domain policy, not permission already applied

**Phase A: required first for one safe end-to-end source recheck**
- `www.snowymonaro.nsw.gov.au` — official Snowy Monaro council IP&R directory and public PDF assets.
- `www.legislation.nsw.gov.au` — public NSW legislation research; test exact hostname and only add any verified redirect host after inspection.

**Phase B: add only on confirmed domain-specific source need**
- `www.planning.nsw.gov.au` — NSW public planning guidance.
- `www.olg.nsw.gov.au` — NSW Office of Local Government public guidance.
- `snapshotclimate.com.au` — public emissions reference **not a government site**; separately assess access, rights and any exact redirect hostname before enabling.

Treat these as **Additional allowed domains** for a *private, restricted public-research Codex Cloud environment*. Do not enable `Enable all public internet access` or `All unrestricted` when the exact-host allowlist suffices. Keep package manager access no broader than the existing workflow needs. No HTTP secrets, API tokens, environment credentials, Council network VPN access or internal domains are needed for these public documents. Do not add generic wildcards or third-party mirrors simply to evade 403.

If a managed workspace imposes an overriding Agent Security/organisation policy, the authorised administrator must approve and change that policy; project code/README cannot override it.

## 3. Required human environment operation (NOT accomplished by GitHub edit)

This connected GitHub tool can modify source files/PR discussion, **not Codex Cloud environment networking or its Publish/Republish control**. The environment owner must:
1. Open **Settings → Codex Cloud → Environments**, select the *exact environment used by the blocked task*, and **Edit**.
2. In the environment's internet-access/network settings, keep unrestricted public internet OFF; set restricted/custom approved destinations and enter the exact Phase A domains above under **Additional allowed domains**. Inspect existing draft changes for surprising domains, HTTP secrets, service credentials and sharing changes; do not paste any secrets into GitHub.
3. **Save** the environment configuration, then **Publish/Republish** that environment. Confirm a published state rather than a draft. If control unavailable, record `ENVIRONMENT_PERMISSION_REQUIRED` and ask the authorised workspace/environment administrator, not the user to edit arbitrary code files.
4. Start a **new cloud task** using the updated published environment on the **latest GitHub PR #130 HEAD**. Already-running tasks may retain their former network policy/state. Before touching code, test in that new task.
   
Official general reference: https://help.openai.com/en/articles/20001545-using-codex-cloud and Codex Cloud environment guide linked therein.

## 4. Verified public-directory discovery (not fresh PDF admission)

Council public directory: https://www.snowymonaro.nsw.gov.au/Council/Integrated-Planning-and-Reporting .

The directory states CSP 2035 adopted on 1 May 2025; DP 2025–2029 **2026 Revision** and OP 2026–2027 adopted on 26 June 2026. It provides separate links to the Revenue Policy, long-term financial plan, Resourcing Strategy and Water/Wastewater Asset Management Plans. Source discovery URLs identified from the official directory:
- CSP one-page summary: https://www.snowymonaro.nsw.gov.au/files/assets/public/v/4/council/ipr/csp/csp-2035-plan-on-a-page.pdf
- DP 2026 revision: https://www.snowymonaro.nsw.gov.au/files/assets/public/v/4/council/ipr/20262027/adopted-delivery-program-2025-2029-2026-revision-v2.3.1-20260630.pdf
- OP 2026–2027: https://www.snowymonaro.nsw.gov.au/files/assets/public/v/3/council/ipr/20262027/adopted-2026-2027-operational-plan-v3-w-revenue-policy.pdf
- Water asset plan: https://www.snowymonaro.nsw.gov.au/files/assets/public/v/1/council/ipr/20252026/adopted-amp-water-20250619.pdf

**Evidence limits:** the public web view provided directory text and click targets, but the PDF follow-up could not establish current source bytes/byte digest and did not visually confirm exact pages. Therefore all four documents above are `DIRECTORY_LINK_OBSERVED` only, NOT `RETRIEVED`, `BYTE_VERIFIED`, `ANCHOR_VERIFIED`, `VERSION_CONFIRMED` or `ADMITTED`. Treat discovery as a lead to recheck, not an authorised Council-content license or complete catalogue. Do not redistribute original PDFs to the public repo without confirmed rights.

## 5. In the new published Codex environment: smoke test, then continue V1.6

- Make an ordinary HTTPS request through the configured inherited proxy (do NOT disable proxy, spoof user agent or route via an unapproved host) to the Council IP&R directory. Log HTTP status, effective final hostname, content type and timing; distinguish 403 CONNECT vs origin 403 vs redirect/404. Retain a redacted source-access report without credentials.
- Request the small **CSP plan-on-a-page** PDF as the first byte-level smoke, store to `/tmp` only, and run the pre-existing `verify-source.py` against the **summary** PDF (not the full CSP). Capture actual SHA-256, size, page/anchor match, current HTTP status, date and rights status; do not replace historical digest if different—append a new revision/correction event and investigate.
- Test exact DP/OP document URLs by metadata first; larger public PDFs require bounded transfer/time/size limits and explicit reuse review. Never assume a link accessible once means it is the current legally operative revision for every place and date.
- Update `qa/system/source-access.json` or a new dated log with real result and error classification, then use `AtlasIntake.registerSource` / ordered stage events. No automatic `ADMITTED`, official CSP→DP→OP edge, Council budget/expenditure, emissions reduction, LEP parcel status or formal approval from a successful GET.
- Re-run native + Chrome regressions and source/bundle verifiers after integrating permitted observations; preserve base digest, 127 items and PR #130 Draft. Commit + PUSH, update `NEXT_SESSION.md`, re-read remote HEAD, report current `PUBLIC_CORPUS_COVERAGE` and `OFFICIAL_ADMISSION` separately.

## 6. Status to hand off

**Done here:** remote source/QA blocker readback, network allowlist security review and public directory URL discovery; explicit next-step plan committed for cross-device continuity.

**Not done here:** environment Settings Save/Publish, real Codex new-task CONNECT retest, PDF fresh bytes, source licence/human approval, official mappings, V1.6 complete acceptance. They remain `ENVIRONMENT_OWNER_ACTION_REQUIRED`, `RETRIEVAL_BLOCKED_UNTIL_RETEST`, and `OFFICIAL_ADMISSION_PENDING`.

**Do not treat this GitHub document or PR comment as publishing an environment or fixing 403.**
