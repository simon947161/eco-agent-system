# ClimateOS Public Strategy Atlas

English, local-first public-strategy research website. Explore cross-document relationships and recursively inspect the content inside each topic. The main graph has 15 synthetic topics; the internal model has 127 items, including separately labelled public-source observations.

**Status:** working research prototype; M0 retained, M1 validation extended, M2 recursive-content slice verified. Not a complete authoritative knowledge system. No deployment, official endorsement or real Council KPI.

## Run

Keep this entire directory together. No package installation is required.

```bash
cd apps/public-strategy-atlas
python -m http.server 8877 --bind 127.0.0.1
```

Open `http://127.0.0.1:8877/`. Direct `index.html` opening also uses classic scripts; final browser checks used HTTP. The portable SHA-256 implementation supports contexts without Web Crypto.

## Explore

1. Select a topic in **Relationships** to inspect its source entry and upstream/downstream links. Links themselves are also keyboard-selectable.
2. In **Inside this topic**, expand the nested disclosure controls or select any content item.
3. **Inside content** displays the selected topic's internal tree. Synthetic paths can run through topic → section → clause → action → indicator → evidence. These are demonstration breakdowns, not extracted Council provisions.
4. Follow the breadcrumb trail or **Parent content**, **Focus this subtree**, and **Back to relationship topic**. Leaves explicitly state that no further content has been admitted.
5. Search titles and internal text. Results show their topic context, with up to 12 displayed matches. Other topics remain accessible through the graph.
6. Use **Expand progressively**, **Expand selected**, **Reset expansion**, **Fit scope**, and zoom. Reduced zoom is an overview; use normal zoom and the inspector to read details.
7. **Public sources** opens five dated observations. The CSP one-page summary observation decomposes into document → Objective 6 → clause 6.1, preserving its exact public locator and observation status. It has no invented downstream actions.
8. **Discover links** computes bounded cross-root structural convergence, shows the actual paths and evidence count, and retains authored hypotheses and synthetic counterexamples. Structural detection is not semantic or legal validation.
9. **Layout demo** loads explicitly synthetic 60/200-item fixtures. They test rendering and selection, not the completeness or usability of real policy data.

## Content addressing and portable evidence

Each content item has separate logical and version IDs. Item hashes protect the serialized item. Child-linked subtree hashes propagate a changed descendant into ancestor receipts while leaving unrelated roots unchanged. This is a local hierarchical hash structure, not a blockchain deployment or an independent attestation.

**Export snapshot** downloads a public/synthetic JSON bundle with the dataset, audit result and content-root receipts. Verify it offline:

```bash
node apps/public-strategy-atlas/verify-snapshot.cjs PATH_TO_EXPORTED_JSON
node apps/public-strategy-atlas/verify-snapshot.cjs PATH_TO_EXPORTED_JSON sha256:EXPECTED_CHECKPOINT
```

A digest retained separately provides a comparison checkpoint. A receipt stored alongside editable content is not an independent witness. No signatures, statutory conclusions or tamper-proof guarantee are claimed. Git retains committed source history; the browser does not offer persistent content editing or revision conflict resolution.

## Tests

Run from the repository root:

```bash
node apps/public-strategy-atlas/model.test.cjs
node apps/public-strategy-atlas/content.test.cjs
node apps/public-strategy-atlas/audit-cli.cjs
node --check apps/public-strategy-atlas/atlas.js
```

`qa/ENGLISH_CONTENT_RESULTS.md` records actual browser checks, limitations and screenshots. `qa/narrow-screen.html` is a 390px iframe harness, not physical-device certification. Older QA reports are historical evidence and remain unchanged.

## Evidence and continuity

Current official graph mappings: **0**. Source observations do not complete raw-byte, reuse-permission, formal-version, geographic or temporal admission. Actual KPI remains UNKNOWN; coverage and elapsed-time demonstrations remain separate.

Read [NEXT_SESSION.md](NEXT_SESSION.md) before continuing from the latest remote HEAD. Development authority remains [V1.3](../../docs/research/public-strategy-atlas/PROJECT_TASKBOOK_V1_3_BUILD_AND_CONTINUITY_20261029.md); it has not been rewritten.

Use only public/synthetic material. Do not upload Council nonpublic records, personal cases or employer system data. No new procurement, deployment, changes to PR129/main, or merge is authorised. Commit verified stages to `feature/public-strategy-atlas-web-mvp-20261029`, push through authorised GitHub access, and read back remote HEAD.
