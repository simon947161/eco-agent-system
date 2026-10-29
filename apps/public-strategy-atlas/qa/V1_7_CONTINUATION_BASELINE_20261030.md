# V1.7 handoff intake and existing-system repair

Date: 30 October 2026 Australia/Sydney. Remote branch and PR #130 head independently read as `c1a859af97c0bc0e22411c303db94d67f252f422` at start; local checkout was clean. Current runtime status reports running/connected, observations current and unrestricted/enforced HTTP policy. No environment settings were changed.

## V1.7 acceptance is blocked by unavailable handoff input

The user's message names `CSOI_V1_7_CODEX_HANDOFF_PACK.zip`, but no accessible attachment reference/file ID was delivered to the tools. Recursive workspace filename/content searches did not find the archive or its three authoritative files; attachment/scratch/shared locations were also checked. `/mnt/data` does not exist. The repo's latest remote matches the local checkpoint and contains no matching V1.7 task definitions.

Required input remains:

1. `CSOI_V1_7_80_Task_Master_Plan.md`
2. `COI_TASK_REGISTRY_V1_7.json`
3. `CODEX_CSOI_V1_7_START_HERE.txt`

**BLOCKED_HANDOFF_NOT_AVAILABLE.** COI-001's definition and acceptance criteria have not been read. No task registry was invented, no COI task was marked VERIFIED and no V1.7 pack was marked complete. Machine-readable evidence: `V1_7_HANDOFF_INTAKE_STATUS.json`. This report records an actual existing-system repair, not a replacement 80-task plan.

## Executable repair completed while handoff is blocked

Previously, `sourceGaps()` used immutable registration-time `source.access` for current gap ownership. Appending successful retrieval/byte-verification events could leave a source labelled BLOCKED_BY_PERMISSION with obsolete environment-admin instructions. The source detail also read old access directly and could say content was never retrieved when only extraction was missing.

- `AtlasIntake.sourceStatus` / `sourceGaps` now use retained replay evidence. An HTTP 200 retrieval reports AVAILABLE **at its recorded retrieval time**, without claiming live current connectivity. Original source records and prior events are unchanged.
- `historicalAccess` remains available separately. Corrections above retrieval retain its evidence; a correction withdrawing retrieval gives NOT_CHECKED and requires a new check. An unrelated correction without prior retrieval preserves recorded historical access.
- The next action follows the actual stage: byte verification, permitted extraction, anchor review, edition/scope or authorised review. Metadata-only rights route to SOURCE_RIGHTS_REVIEWER. Public admission stays disabled without an independent authority verifier. Synthetic research can never receive official admission.
- Source detail separates retained evidence from historical registration metadata and distinguishes missing extraction from missing retrieval. README/DATA_CONTRACT were updated.

## Actual checks and evidence

**PASS_TESTED_HERE:** baseline 15/15 native files, then final **16/16 native files** after the fix. New `intake-access.test.cjs` covers retained/withdrawn/re-restored retrieval, unrelated correction, rights/review owners, synthetic/public admission boundaries, unchanged source revisions/events/digests and historical access. `system/intake-access-20261030/native-results.json` contains the final actual outputs.

**PASS_TESTED_HERE:** focused real Chromium `qa/intake-access-browser.py`, 1440×900 and 390×844, six source-access cases plus independently verified downloaded snapshots. Fixtures are explicitly **QA ONLY**, use `example.invalid`, are imported in temporary browser memory, and make no source requests or public-catalogue updates. Screenshots/ARIA trees/browser results and tested code hashes are in `system/intake-access-20261030/`.

**PASS_TESTED_HERE:** existing `qa/system-browser.py` at desktop/mobile, preserving route/dossier/source/work/accounting/applicability/local-challenge/snapshot workflows, with no script errors or horizontal overflow. Updated source screenshots: `system/source-1440.png`, `system/source-390.png`. Other five historical browser runners and Node coverage percentages were **NOT_REMEASURED_THIS_BATCH**. Physical devices/professional screen readers/cross-browser certification remain NOT_TESTED. Historical V1.6 coverage percentages are not represented as fresh V1.7 acceptance.

Peer review identified and corrected misleading synthetic admission guidance before final native/focused-browser checks. Native catalogue/hash tests retain the original 127-item base digest and JSON/JS source-register mirror. No original PDF, full HTML, private business record or private production integration was added.

## Source coverage and next executable action

No new official-source requests or stage integration occurred in this batch. Catalogue remains 15 requirements / 14 families / 2 concrete CSP document URLs; integrated current retrieval/extraction/version-confirmation/admission stage counts remain 0. Previous successful CSP summary byte/anchor verification remains separate dated QA evidence. Official admitted relationships 0; inventory denominator and actual environmental outcome KPI UNKNOWN.

**SOFTWARE_CAPABILITY PARTIAL; PUBLIC_CORPUS_COVERAGE PARTIAL; OFFICIAL_ADMISSION PENDING. V1.7 TASK ACCEPTANCE BLOCKED.** No full-system completion claim.

Next: obtain and completely read the supplied ZIP's three authoritative files, reconcile their exact COI-001 onward definitions against the tested V1.6 architecture, and execute the actual registry order. Keep tasks unverified until their specific code/tests/acceptance evidence pass. Continue on the same Draft PR #130 branch, with per-pack tests/evidence/registry/NEXT_SESSION/commit/push. No deployment, merge, paid service, Council nonpublic data or WCOS private-production changes.
