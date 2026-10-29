# Atlas M1 bounded contract — atlas-1
Actual implementation: atlas-data.js (serializable fixture), atlas-model.js (pure contracts and checks), atlas.js (rendering). Browser classic scripts retain direct file opening; no dependency installation.

|Object|Identity and fields|Boundary|
|---|---|---|
|SourceArtifact|id, url, classification, revisionId, rawDigest, observedAt, licence, verification|Two official directory URLs only; observedAt/revision/digest UNKNOWN; not clause evidence|
|DocumentRevision|id, logicalId, validFrom/to, region, rawDigest, sourceId|One synthetic version; source bytes and node identity separate|
|ContentBlock|id, sourceId, offset, length, digest, algorithm, chunking|Whole-file UTF-8 synthetic source; byte offset, not PDF text position|
|KnowledgeNode|logicalId, versionId, revisionId, status; layout x/y|Current nodes SYNTHETIC; geometry not authority|
|RelationshipAssertion|id/from/to/predicate, status, revisionId, issuer/reviewer, evidenceRefs/counterevidenceRefs, valid interval/region, reviewStatus, algorithmVersion|Official promotion requires reviewer, approved evidence and non-synthetic endpoints; directory entry cannot qualify|
|DiscoveryHypothesis|id, assertionIds, explanation, ruleVersion, counterevidence, reviewStatus|Manual candidate fixture, no AI discovery engine|
|ChangeEvent|id/type/objectId/actor/reason/observedAt/sequence/previousDigest/digest|appendEvent returns new array; rejects altered history and duplicate IDs; not persistent storage or independent witness|

canonical uses sorted JSON object keys, UTF-8, ordered arrays, finite numbers; unsupported values rejected. It is atlas-1 serialization, NOT a claimed RFC canonicalization implementation. raw digest protects exact synthetic bytes; object digest protects serialized records. No official source hash, Merkle proof, signature or SCITT receipt is claimed. A writer can rewrite the whole chain; no tamper-proof guarantee.

paths is bounded simple-path forward search with cycle exclusion, maximum depth/outputs; candidates excluded by default, UI shows synthetic edge IDs. Reverse traversal is currently adjacent UI navigation, not an independent backwards query API. applicability rejects mismatched revision/date/region; matching synthetic metadata returns SYNTHETIC_ONLY, never legal approval. Missing or malformed dates return UNKNOWN.

Tests: node apps/public-strategy-atlas/model.test.cjs. Includes three counterexamples: false official promotion, expired time, different region; plus missing endpoint, digest/history tampering and duplicate events. Existing fixture event and raw source digest verified. These are actual Node unit tests, separate from browser QA.

Remaining: richer machine-readable schema validation (all field types, anchors, references), durable event storage and conflict handling, source admission review, clause anchors, larger graph and mobile device tests. No database created. No official clauses admitted. Content hashes cannot prove semantic truth, legal applicability or KPI causation.

## Recursive content extension (English continuation)

`contentItems` is a separate containment layer. Its records carry id, logicalId, versionId, revisionId, ownerNodeId, parentId, kind, title, text, status and observationId. The kind vocabulary is TOPIC, DOCUMENT, SECTION, CLAUSE, ACTION, INDICATOR, EVIDENCE and QUESTION. Kind is descriptive; a containment edge does not imply statutory hierarchy.

All 15 synthetic graph topics have authored internal examples. Observed public content has a null graph owner/revision and an explicit observation reference. It may not become EXPLICIT_OFFICIAL through this layer. Parent and child must retain the same owner, revision, observation and status. Duplicate IDs/versions, missing parents, mixed scope, cycles, unknown owners/observations, more than 500 items or ancestry deeper than 20 are rejected.

`contentTrail`, `contentChildren` and `layoutContent` provide recursive navigation. Coordinates are determined using the complete subtree before visible expansion, so expansion does not relocate already visible nodes. Views are capped at 200 nodes and explicitly mark truncation. Synthetic density fixtures add 60 or 200 records; they are not real source ingestion.

`contentReceipt` hashes the item and a child-ID-sorted array of child subtree digests using deterministic lexical ordering. This provides local child-linked hash propagation. It is not an official Merkle inclusion proof, signed checkpoint, distributed consensus or chain deployment. `exportSnapshot` includes every root receipt; `verifySnapshot` recomputes both content roots and the dataset/event audit and can compare a separately retained expected digest. Export verification does not establish a licence, authenticity, applicability or truth.

Current history includes the original synthetic fixture event and a linked ADD event recording the English content implementation. No persistent content editor or version-diff interface exists. Git commit history remains the durable engineering history. Public observation content is limited to its recorded scope; no official full-document clause mappings have been admitted.

Additional tests: `node apps/public-strategy-atlas/content.test.cjs` covers all topic roots, six-level traversal, subtree mutation propagation, unrelated-root independence, input order, containment counterexamples, 60/200 stable layouts, bounded truncation, export verification and English UI/content checks.

## Source-admission and local-workspace extension

The standalone `sources/csp61-admission.json` is an admission receipt, mirrored in a classic script for direct-file compatibility. It records the exact official URL/retrieval time, response media type/byte length, original byte digest, page/section/clause and bounded word-origin coordinates, normalized excerpt/digest, revision evidence, geographic context, unknown effective interval, permission status and human reviewer/decision fields. `verify-source.py` recomputes the original digest before extracting the recorded anchor. It does not fetch or redistribute a PDF. `assessAdmission` exposes separate observation/bytes/extraction/revision/review/admitted stages. Only the first three pass for this record; approval and reuse are not invented. The browser does not contain an approval/signature-issuing control.

Local workspace schema `atlas-local-workspace-1` has a base dataset digest, ordered revisions/events and a null signature. Each revision contains target ID, base-item digest, prior local-revision digest, title/text-only content, action/state, reason/time, fixed local actor/classification, optional revert target and canonical digest. Events bind the revision digest to a global previous-event digest. Corrections, supersession, contests, retractions and reverts append new entries. Original `contentItems` never mutate; local overlay records remain LOCAL_ANNOTATION. Superseded-history labels are projections rather than edits to earlier records. Retract cannot change the text it withdraws.

`commit` requires the target's expected local head, `compare` returns explicit field before/after values, and `replay` reconstructs a chosen point. `subtreeReceipt` binds base source-item digests, classified local views and sorted child receipts; independent roots are unaffected by unrelated annotations. Import validates the base, bounded record count/size, hashes, event links, same-target revert, title/text-only fields, action/state and signature boundary. Signatures are unsupported and rejected, not cryptographically certified.

IndexedDB `saveLocal` atomically checks the expected stored checkpoint and monotonic revision prefix before saving a head plus a checkpoint-keyed snapshot. Saves/loads require explicit UI actions; nothing is restored or transmitted automatically. A branch that diverges from the saved prefix cannot overwrite it. Import does not silently replace/truncate the current in-memory history. Resolving divergent branches currently requires retaining/exporting the unsaved branch and deliberate reconciliation; there is no automated merge.

Old statements about absence of editing above describe the previous implementation boundary. The new scope is local annotation editing only; official document replacement, public-source approval, independent signatures/witnessing and server synchronization remain unimplemented. Source admission, base snapshots and local-workspace exports have distinct formats and do not imply each other's checks have passed.
