# Environmental Evidence Object and Lineage Contract v0.1

Status: SCHEMA-DESIGN / NO NEW EVIDENCE ADMITTED

## 1. Purpose

An Environmental Evidence Object (`EEO`) is the smallest reviewable unit that
may support a bounded claim. A file, web page, map layer, observation, model
output or human note is not automatically evidence merely because it exists.

## 2. Required fields

| Group | Required fields |
|---|---|
| Identity | `evidence_object_id`, `title`, `object_class`, `version`, `created_at` |
| Subject | `theme`, `question_ids`, `place_scope`, `spatial_boundary_id`, `time_start`, `time_end` |
| Source | `publisher`, `source_uri_or_local_identity`, `source_date`, `retrieved_at`, `licence`, `attribution` |
| Integrity | `content_digest`, `digest_algorithm`, `raw_or_derived`, `immutable_source_identity` |
| Method | `variable`, `units`, `method_id`, `method_version`, `parameters`, `software_identity` |
| Fitness | `intended_use`, `spatial_resolution`, `temporal_resolution`, `coverage`, `quality_controls`, `representativeness` |
| Uncertainty | `uncertainty_method`, `uncertainty_value_or_range`, `missingness`, `known_limitations` |
| Governance | `admission_state`, `privacy_class`, `licence_state`, `review_state`, `reviewer_role`, `expiry_or_recheck_date` |
| Claims | `supports_claim_ids`, `contradicts_claim_ids`, `does_not_support`, `maximum_conclusion_level` |
| Lineage | `parent_object_ids`, `run_receipt_id`, `transformation_steps`, `output_object_ids` |

Unknown values must be represented explicitly. They must not be replaced by a
plausible estimate without a separately identified method and uncertainty.

## 3. Object classes

- `OFFICIAL_OBSERVATION`;
- `OFFICIAL_ASSET_OR_OPERATION_RECORD`;
- `OFFICIAL_OUTLOOK`;
- `LICENSED_THIRD_PARTY_OBSERVATION`;
- `FOUNDER_FIELD_OBSERVATION`;
- `SPATIAL_REFERENCE`;
- `DERIVED_INDICATOR`;
- `MODEL_OUTPUT`;
- `EXPERT_REVIEW`;
- `SCENARIO_ASSUMPTION`;
- `MISSING_EVIDENCE_RECORD`.

An `OFFICIAL_OUTLOOK` is not an observation. A `SCENARIO_ASSUMPTION` is not a
forecast. A `SPATIAL_REFERENCE` is not proof of a current environmental state.

## 4. Admission states

- `IDENTITY_ONLY`;
- `CONTEXT_ONLY`;
- `ADMITTED_FOR_NAMED_USE`;
- `QUARANTINED`;
- `SUPERSEDED`;
- `REJECTED`;
- `HUMAN_REVIEW_REQUIRED`.

Admission is use-specific. An object admitted for spatial orientation may still
be prohibited for quantitative water accounting or safety decisions.

## 5. Lineage contract

Every derived indicator must expose:

```text
source object(s)
→ retrieval/admission record
→ spatial and temporal alignment
→ transformation and parameters
→ validation and uncertainty
→ run receipt
→ derived object
→ claim node
→ conclusion gate
```

No step may silently change units, datum, time zone, aggregation window,
missing-data treatment, spatial boundary or scenario class.

## 6. Claim binding

Each claim must record:

- exact claim text;
- subject, place and time boundary;
- supporting and contradicting object IDs;
- unresolved gaps;
- conclusion level;
- permitted and prohibited use;
- review state and reviewer role;
- valid-until or recheck condition.

Evidence quantity does not override evidence authority, method fitness,
uncertainty or a required human signoff.
