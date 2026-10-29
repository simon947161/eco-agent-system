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
