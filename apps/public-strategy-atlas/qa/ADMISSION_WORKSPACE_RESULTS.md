# Source admission, local revisions and readability — actual engineering evidence

Date: 2026-10-29 Australia/Sydney. Remote baseline 3024a6acf597602167be8a19bead200df9dd821c. Read remote HEAD, NEXT_SESSION.md, README.md, DATA_CONTRACT.md and PR130 continuation comment 6491788231 before implementation. Existing English 15-topic/127-item system retained; no M0 rebuild or taskbook rewrite.

## Source-chain evidence

Actual unauthenticated public retrieval of the official summary URL returned HTTP 200, application/pdf, 416031 bytes at 2026-10-29T09:06:13.338982Z. SHA-256: 1f1be67a25c0c2468b7f69d5959300430b840ebe5beb05eb1e77dd8516c3261e. Source URL and all gates are in sources/csp61-admission.json. Original PDF bytes remain outside Git because reuse permission was not verified.

The downloaded PDF was opened with pdfplumber and rendered with Poppler. Actual page image visually inspected: one-page landscape summary; Objective 6 is in the environment column and clause 6.1 is present. Raw whole-page text order interleaves adjacent columns, so extraction uses a bounded word-origin filter (x0/top in 490,316,705,337 PDF points, top-left origin), not an unqualified full-page string search. The short normalized anchor and its digest are in the receipt. No full PDF/page screenshot or long extracted text is committed.

`python verify-source.py ORIGINAL_PDF`: PASS, raw bytes/page count/bounded text/excerpt digest. An independently altered byte stream was actually tested and rejected with RAW_DIGEST_MISMATCH. No automatic network fetch occurs in the verifier.

Official directory search retrieval lists the CSP adoption on 1 May 2025 and links the summary. Direct directory open in this session returned 403; full adopted-version/current equivalence was not confirmed. The general copyright URL could not be retrieved and no explicit permission for this PDF was verified. Document title/publisher provide Snowy Monaro strategic context, not parcel applicability or a proved legal effective interval. Human reviewer/decision remain null/PENDING.

Actual stage results: SOURCE_OBSERVED PASS; BYTE_VERIFIED PASS; CONTENT_EXTRACTED PASS; OFFICIAL_REVISION_CONFIRMED UNKNOWN; ADMISSION_PENDING_REVIEW PENDING; ADMITTED NO. No official relationship or Council signature created. This is a verifiable safe partial chain, not complete admission.

## Model and verifier execution

- model.test.cjs: PASS retained regressions.
- content.test.cjs: PASS retained recursive-content/hash/layout tests.
- workspace.test.cjs: PASS edit/diff, immutable base and prior versions, supersede/revert/retract/contest, historical replay, target-head conflict, monotonic prefixes, object/subtree propagation and unrelated-root independence, workspace export/import/checkpoint, changed content/event/parent/base rejection, unsupported signature claim and official-promotion rejection, empty reason/invalid calendar date/size rejection, pending source gates/excerpt digest and JSON/script receipt equality.
- A real five-revision browser-exported workspace was verified with verify-workspace.cjs and expected checkpoint f52e9889094fb8c803dce40af2e434afa95d6fa498fe06aba5f871e5f186885a: PASS. This was synthetic QA annotation content; no case data.
- Syntax and diff checks executed at final preparation. No new website dependency installed.

## Real Chrome browser execution

Private managed engineering preview, not a deployment.

1. Source admission panel actually displayed the six separate stages, retrieval metadata, byte and excerpt digests, page/section/clause anchor, public link, pending permission/scope/reviewer gates and no ADMITTED claim.
2. Opened observed CSP clause content → local editor. Changed local title/text, supplied a synthetic QA reason and compared explicit before/after fields. Appended CORRECT and explicitly saved to IndexedDB. Source record remained PUBLIC_TEXT_OBSERVED with its original wording.
3. Reloaded page: workspace started with 0 in-memory revisions despite saved data. Explicit Load restored 1 verified revision.
4. Opened a second browser tab, explicitly loaded the same revision, appended SUPERSEDE and saved. First stale tab's save rejected with STORAGE_CONFLICT. Explicit Load then restored 2 revisions. This exercised the real atomic IndexedDB transaction, not a storage mock.
5. Compared retained source/local versions, appended REVERT to original base text, CONTEST and RETRACT. History retained 5 revisions/events; previous entries displayed SUPERSEDED_HISTORY, current one RETRACTED. Saved and exported through actual browser download.
6. Reloaded: still 0 in memory until explicit import. Used actual file chooser to import the exported JSON; import verified 5 revisions without automatic save. Explicit Load verified the saved checkpoint. The file chooser call was unusually slow in this cloud browser but completed; no remote upload occurred.
7. Local source inspector showed separate LOCAL_ANNOTATION/RETRACTED card and source PUBLIC_TEXT_OBSERVED badge. It linked the newer byte-backed admission receipt without replacing the original observation. Local editor displayed a canonical root receipt binding the source and local view separately.
8. Overview Fit scope showed unscaled 13px labels. Three labels for the observed CSP subtree; 12 shown for the 200-item fixture. They open full-size inspector content. Labels beyond the first 12 remain accessible via normal zoom/search.
9. 60 and 200 fixture DOM counts actually matched. Demo item 199 selected successfully after this change. Existing O2 coordinates and discovery code were preserved.
10. 390px iframe: loaded saved workspace explicitly, opened editor, actual title focus true, no document horizontal overflow; proposed-text diff and local root receipt rendered. Synthetic mobile proposal was not committed. Full-size controls/labels remained usable. Final editor context change was desktop checked: observed source tree 3 nodes, local receipt, 3 overview buttons; closing restored focus to the observed clause node.
11. Inspected captured warn/error entries originating from the Atlas preview URL: none. This does not certify unrelated browser extension logs.

Actual screenshots: admission-chain.jpg, workspace-desktop.jpg, workspace-mobile.jpg. They contain only public/synthetic app data and no unrelated tabs/accounts or original PDF image.

## Limits and next work

Complete official admission remains blocked on explicit reuse basis, independently confirmed current adopted version/effective scope and an identified human decision. No claim that this agent approved as Council. Source hashes are not official signatures.

Editing is local research annotation only. Existing observed source content is immutable. Divergent branch saving/import replacement is rejected; automatic three-way merge is not implemented. Browser snapshots can be exported; browser storage can be cleared/lost. A privileged writer can replace a whole unsigned history unless checked against an externally retained checkpoint. No encrypted secret store, server sync, multi-user authority or independent witness.

No physical touch-device, Safari/Firefox, screen-reader/full WCAG or exhaustive real-corpus readability acceptance. Source verifier needs pdfplumber (available in this runtime). Historical R0-K remains unavailable. Official graph mappings remain 0, real KPI UNKNOWN. No deployment/procurement/merge/PR129/main/Council-system access.

CRP: knowledge — bytes, extraction, permission, applicability and review are distinct gates; local interpretation must retain source identity. Idea/wish — auditable source evidence plus a usable correction lifecycle. Decision/reasoning — preserve uncertain admission and append local changes instead of mutating source/history. Open — permission/current-version/human decision and divergent-branch reconciliation. Next — independent admission review and deliberate merge preview for exported local branches. Keywords — ClimateOS, CSP 6.1, source admission, O2, optimistic concurrency, IndexedDB, content receipts, correction events.
