# New runtime — official access restored, revision guard held

At **08:39:06–08 AEDT, 30 October 2026** (2026-10-29T21:39:06–08Z), the newly attached cloud runtime successfully retrieved both requested official URLs through the inherited proxy. This is a different runtime and published configuration version from the previous blocked attempt. No environment settings were edited or published by this task.

**Phase 1 network: PASS_TESTED_HERE. Continuation: ENVIRONMENT_POLICY_BLOCKED under the user's explicit numeric revision-1 safeguard only. No actual destination-policy denial or CONNECT 403 was observed.** The user's instruction says: “If the new runtime still uses revision 1 or reports CONNECT 403, stop repeated network attempts and return ENVIRONMENT_POLICY_BLOCKED with the exact diagnostic evidence.” Current desired and observed spec revisions both report `1`, so no further official-source requests were made after the initial pair. Clarification was requested because the effective policy and observed access differ from the previous instance.

## Effective runtime evidence

- Current observations: running, connected, `observations_current: true`.
- Desired/observed spec revision: `1` / `1`.
- Effective HTTP policy: `unrestricted`, state `enforced`.
- Local supported startup policy: version 1, HTTP type `unrestricted`; VPN false; no TCP destination grants.
- The previous runtime had restricted/enforced HTTP policy with zero custom allowed hosts. Its environment identity and source configuration version differ from this task's current observations. The spec revision returned by the runtime status tool is distinct from an editable draft revision; we do not infer a global published revision number from it.
- No proxy bypass, TLS override, user-agent impersonation, alternate source host, credential change or policy mutation.

Sanitized runtime snapshot: `system/new-runtime-recovery-20261030/runtime-policy.json`. Runtime identifiers, configuration identifiers and credential values are omitted.

## Actual initial HTTPS pair

| Official source | HTTP result | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| [Council IP&R directory](https://www.snowymonaro.nsw.gov.au/Council/Integrated-Planning-and-Reporting) | 200, text/html | 174872 | `2eaccf43d00daaf09c3e7fb61ece3410240341cf52405a870c275fe6e9528c63` |
| [Original CSP summary](https://www.snowymonaro.nsw.gov.au/files/assets/public/v/4/council/ipr/csp/csp-2035-plan-on-a-page.pdf) | 200, application/pdf | 416031 | `1f1be67a25c0c2468b7f69d5959300430b840ebe5beb05eb1e77dd8516c3261e` |

Both final URLs matched the requested URLs. Each used a 20-second timeout, bounded body limit (1 MiB HTML / 2 MiB PDF), default TLS verification, inherited proxy and HTTPS/same-exact-host redirect guard. Exact times, media types, timings and failure classifications are in `system/new-runtime-recovery-20261030/access.json`. Classification is `HTTP_SUCCESS` for both; no error is present. Bodies exist only under `/tmp/atlas-new-runtime-20261030/` and may not survive another runtime.

## Original-byte and page-anchor verification

Executed offline:

```sh
python3 apps/public-strategy-atlas/verify-source.py /tmp/atlas-new-runtime-20261030/csp-summary.pdf
```

Exit 0: **PASS: original PDF bytes, page count, bounded anchor extraction and excerpt digest. Admission/permission approval is not implied.**

The raw digest equals the immutable historical receipt. One page; page 1, Strategic Objective 6, clause 6.1, bounding box `[490,316,705,337]`. Bounded excerpt digest remains `sha256:49300a9a5424250d5a543fbc08007e29f73b792b361240d0dc9fae775287f5f3`. The historical receipt was preserved byte-for-byte. The verifier/receipt hashes and structured results are recorded in `source-verification.json`. No original PDF, full HTML or page image was added to Git.

This proves byte/anchor reproducibility for this one summary. It does not prove reuse rights, current full-document equivalence, adopted revision, legal effective period, geographic/parcel applicability, official implementation links, budget/spend or an environmental result. Those fields remain UNKNOWN/PENDING.

## Preserved software and coverage

Fresh **15/15 native test files PASS**, zero failures, recorded in `native-results.json`. Application code, original 127 content items, source catalogue and historical receipt are unchanged. Browser checks are **NOT_TESTED_THIS_ATTEMPT** because there was no application/source-data integration; prior browser results remain historical.

Fresh QA observations: **1 accessible and byte/anchor-verified original document**, plus 1 accessible official directory. These have not been appended to catalogue stages under the numeric stop condition. The unchanged catalogue still reports 15 requirements / 14 families / 2 known concrete CSP documents and zero retrieved/byte-verified/extracted/version-confirmed/admitted stage counts. Complete inventory denominator UNKNOWN. `coverage.json` keeps these two scopes separate. Official admitted relationships remain 0; actual outcome KPI UNKNOWN.

**SOFTWARE_CAPABILITY PARTIAL; PUBLIC_CORPUS_COVERAGE PARTIAL; OFFICIAL_ADMISSION PENDING. Full V1.6 acceptance is not claimed.**

## Next executable step after revision-gate clarification

Use the existing successful directory/PDF observations to append ordered `DIRECTORY_OBSERVED`, `SOURCE_RETRIEVED` and `RAW_BYTES_VERIFIED` events without replacing any historical records. Preserve UNKNOWN/METADATA_ONLY rights: the intake `EXTRACTED` gate remains blocked until permitted reuse is evidenced, even though the separate historical short-anchor verifier passed. Independently inspect permitted current-edition/geographical/rights evidence; extend the source inventory from real directory links and then obtain bounded current DP/OP/LSPS/resourcing/budget/asset/planning/performance documents. No automatic official relationships or admission.

Before integrating newly accessible stages, repair `AtlasIntake.sourceGaps()` so an immutable historical `source.access.state = BLOCKED_BY_PERMISSION` does not continue sending a successfully retrieved source to ENVIRONMENT_ADMIN. Derive the current gap from replayed stages, retain historical observations, and test downgrade/correction behavior. Re-run affected browser/native suites and independent verifiers, then commit/push only this branch and update NEXT_SESSION.

No merge, deployment, paid services, main/PR129 changes, Council nonpublic data or environment publication.
