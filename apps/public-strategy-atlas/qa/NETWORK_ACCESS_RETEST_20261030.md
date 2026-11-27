# Official-source runtime retest — 30 October 2026

Status: **BLOCKED_BY_PERMISSION / PROXY_CONNECT_403**. Start/readback remote was `94d44c597c057322688640bfd977abd903679eda`, the existing PR #130 branch. Read NEXT_SESSION and the complete NETWORK_ACCESS_AND_SOURCE_RECOVERY_20261030.md before testing. The new directory-discovery leads remain reported external research, not freshly retrieved sources in this executor.

## Exact live result

At **07:09:42 AEDT, 30 October 2026** (2026-10-29T20:09:42Z), ordinary HTTPS GETs through the inherited proxy failed for both:

|Official URL|Actual result|
|---|---|
|https://www.snowymonaro.nsw.gov.au/Council/Integrated-Planning-and-Reporting|`<urlopen error Tunnel connection failed: 403 Forbidden>`|
|https://www.snowymonaro.nsw.gov.au/files/assets/public/v/4/council/ipr/csp/csp-2035-plan-on-a-page.pdf|`<urlopen error Tunnel connection failed: 403 Forbidden>`|

The failure occurred during proxy CONNECT, before an origin HTTP response, redirect or PDF body. `httpStatus` is null rather than falsely reporting an origin 403. Both attempts used default TLS verification and inherited proxy bindings, a 20-second timeout, 2 MiB transfer cap and HTTPS/same-exact-host redirect guard. No user-agent spoofing, proxy bypass, mirror, VPN/private endpoint, credential request or policy mutation was attempted. No original PDF was obtained; verify-source.py is **NOT_TESTED** in this retest. The historical expected digest/receipt is unchanged.

Exact request times/error classes/timings: `system/source-recovery-20261030/access.json`. Only safe public-destination metadata is recorded; no credential values, runtime IDs or raw document bodies are committed.

## Saved configuration versus attached instance

Current cloud status: observations current, running, restricted policy enforced, desired/observed spec revision **1**, custom allowed hosts **[]**. The local startup policy also excludes the Council host. A final status recheck during this attempt still shows the old policy.

The editable draft read succeeds at revision **3** and contains www.snowymonaro.nsw.gov.au, www.legislation.nsw.gov.au, www.planning.nsw.gov.au, www.olg.nsw.gov.au and snapshotclimate.com.au. Its base version matches this task's original runtime version. This confirms saved draft contents, **not** the latest global publication state or activation in this running instance. The tool cannot establish whether a different/new configuration was republished elsewhere. We therefore do not claim that the owner's republish failed or was never done.

Evidence: `system/source-recovery-20261030/runtime-policy.json`. No replacement allowlist or duplicate requirements were saved. The remaining action is to run the probe in a **new cloud task attached to the intended republished environment/version**, as the recovery note specifies. If that task also returns CONNECT 403, the environment/workspace administrator must inspect its enforced destination policy; project source cannot override it.

## Preserved software, source coverage and review gates

**PASS_TESTED_HERE:** all 15 native test files, original base digest and source-catalogue/hash validation. Fresh manifest: `system/source-recovery-20261030/native-results.json`; source/dataset evidence: `coverage.json` in the same directory. The application and source catalogue were not edited. Prior real-browser acceptance remains historical evidence; browser suites were **NOT_TESTED_THIS_ATTEMPT** because no application or source-data integration occurred.

- Register: **15 requirements / 14 families / 2 known concrete CSP documents**; complete official inventory denominator UNKNOWN.
- Fresh retrieved, byte-verified, extracted, anchor-reviewed, version-confirmed and admitted document counts: **0**.
- Official admitted relationships: **0**; actual outcome KPI UNKNOWN; official admission PENDING.
- Original 127 items and base digest `sha256:13e765c81f1340918322b1e985da85f2362da3c72e1997804f952865edf365d2` preserved; default migrated digest remains `sha256:6236a12009115cd338e1f1c0db75906b4dbf4139d85bed84397c471e40a872fc`.
- The recovery note's concrete DP/OP/Water AMP URLs remain leads only. They do not advance DIRECTORY_OBSERVED, retrieval, extraction, version or admission stages, and do not inflate catalogue counts.

After access works, obtain the exact summary PDF into temporary storage, run the existing byte/anchor verifier, and retain unknown rights/current-version/geographical/authorised-review fields until evidenced. A digest mismatch requires a new immutable revision/correction and investigation, not replacement of the historical receipt. A successful GET alone does not admit any official relationship. Full V1.6 remains PARTIAL. No deployment, merge, main/PR129 change or Council nonpublic data.
