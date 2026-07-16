# Bondo Passport Validation and Change Detection Contract v0.1

Date: 2026-07-16

Status: NON_OPERATIONAL_CONTRACT / MANUAL_REVIEW_ONLY / CONCLUSIONS_BLOCKED

Task: ClimateOS Task1641–1650

## 1. Validation outcomes

| Outcome | Meaning |
|---|---|
| `VALIDATION_PASS` | all required structural and authority fields are present and internally consistent |
| `PASS_WITH_GAPS` | the object is usable for bounded provenance review but named evidence remains missing |
| `BLOCKED_SCHEMA` | a required field, relation or controlled value is absent or invalid |
| `BLOCKED_VERSION` | a downstream claim requires one controlling version that is unresolved |
| `BLOCKED_LICENCE` | retention, reuse or derivative-publication authority is absent |
| `BLOCKED_REVIEW` | the required accountable human role is absent |
| `PROHIBITED_USE` | the requested conclusion lies outside the passport purpose |

No numeric score may replace these outcomes.

## 2. Passport header contract

Required fields:

1. stable passport ID;
2. bounded subject and project identities;
3. evidence cut-off date;
4. owner/steward;
5. raw-data, GIS, model/weight and external-account flags;
6. human scientific-approval state;
7. permitted and prohibited uses.

Validation rules:

- project IDs must retain the issuing authority;
- an evidence cut-off is not a claim that all public evidence was found;
- `none`, `no` and `not acquired` must not be interpreted as future permission;
- prohibited uses must survive export, summary and change events;
- a changed project name or ID creates a new identity-review event, not an overwrite.

Current Task1631–1640 header result: `VALIDATION_PASS` for bounded documentation
use only.

## 3. Evidence-object contract

Every future evidence-object version should record:

| Field | Rule |
|---|---|
| Evidence ID | stable family ID plus immutable version identity |
| Source authority | official, proponent, derived context or other explicit class |
| Object title/type | preserve the source description without upgrading authority |
| Locator/document ID | record when public and lawful; never infer from a similar filename |
| Observed/published time | distinguish publication, retrieval and effective dates |
| Version/access state | accessible, identity-only, inaccessible, withdrawn or superseded |
| Content integrity | lawful retained-file checksum, or metadata receipt when content is not retained |
| Licence/reuse state | separate public visibility from retention and redistribution rights |
| Admission boundary | identity, attributed statement, context, or blocked use |
| Parent/previous version | append-only lineage; never destructive replacement |

Current evidence-object registry result: `PASS_WITH_GAPS`. The existing objects
are sufficient for the current provenance shell, but exact locators, retrieval
receipts, content hashes and explicit reuse states are not complete for every
object. These gaps block automated monitoring and republication.

## 4. Claim and relation contract

Every claim requires:

- stable claim ID;
- bounded statement;
- supporting or contradicting evidence-object IDs;
- source/claim classification;
- controlled state;
- version and time support;
- missing-evidence or human-review links where applicable.

Allowed controlled states:

- `ADMITTED_IDENTITY`;
- `ADMITTED_ATTRIBUTED_STATEMENT`;
- `CONTEXT_ONLY`;
- `VERSION_CONFLICT`;
- `MISSING_EVIDENCE`;
- `REJECTED_INFERENCE`;
- `PROHIBITED_CONCLUSION`;
- `HUMAN_REVIEW_REQUIRED`.

The Task1631–1640 table uses readable phrases such as `admitted` and
`rejected`. Its meaning is preserved, but machine normalization remains
`BLOCKED_SCHEMA` until a separately authorized structured representation maps
each row to exactly one or more controlled states without erasing nuance.

## 5. Immutable lineage rules

1. Never edit an earlier observation to resemble a later source.
2. Append a new version node and link it with a typed relation.
3. `SUPERSEDES` is allowed only when the later controlling source says so or
   the responsible authority relationship is documented.
4. `VERSION_DIFFERS_FROM` does not declare either object false.
5. `WITHDRAWN` preserves the prior identity, receipt and withdrawal time.
6. `INACCESSIBLE` preserves the object identity without pretending its content
   was inspected.
7. A duplicate may share content identity but retains each source locator and
   authority context.
8. A changed licence creates a new governance event and never retroactively
   grants rights that were absent at the earlier observation time.

## 6. Change classification

| Class | Examples | Required response |
|---|---|---|
| `NO_CHANGE` | identical retained checksum or equivalent metadata receipt | record check only |
| `NON_MATERIAL_CHANGE` | formatting, navigation, contact styling or update timestamp with no governed-field change | append event; no claim re-review |
| `MATERIAL_METADATA_CHANGE` | project stage, name, ID, turbine count, area, attachment identity or access state | freeze affected claims; provenance review |
| `MATERIAL_SPATIAL_CHANGE` | boundary, layout, turbine coordinates or investigation area | GIS/planning re-review |
| `MATERIAL_SCIENTIFIC_CHANGE` | mast/LiDAR metadata, measurement method, QC, uncertainty or technical wind appendix | wind-science and data-governance re-review |
| `MATERIAL_LICENCE_CHANGE` | retention, reuse, access or redistribution terms change | quarantine affected object; licence review |
| `SOURCE_WITHDRAWAL` | official or proponent object removed or declared withdrawn | retain receipt; mark unavailable; review dependent claims |
| `AUTHORITY_CONFLICT` | official records disagree on the controlling stage/version | retain contradiction; Founder and responsible-role review |

## 7. Source check definitions

These are manual check specifications, not active monitors.

| Source family | Governed fields | Material triggers |
|---|---|---|
| NSW Planning record | application ID, project name, stage, description, turbine count, area, documents | stage/count/area/document-set change or withdrawal |
| EPBC record | referral ID, status, action description, attachments, dates | status, attachment, layout or action-description change |
| Developer record | dated claims, booklet/map identity, mast-campaign statements | new layout, turbine count, mast metadata, method or technical report |

Every check records checker, time, source locator, access state, observed
metadata and comparison base. Failure to access is an event, not proof of
deletion or project change.

## 8. Duplicate and quarantine rules

- byte-identical objects from different authorities are not authority-identical;
- same filename is not proof of same content;
- a later date is not proof of supersession;
- inaccessible content remains `IDENTITY_ONLY`;
- unclear reuse rights remain `LICENCE_UNKNOWN` and outside derivative output;
- raw files, if ever separately authorized, enter quarantine before parsing;
- no quarantined object supports a scientific or project-performance claim.

## 9. Current validation decision

`HEADER_PASS / PROVENANCE_SHELL_PASS_WITH_GAPS / CONTROLLED_STATE_NORMALIZATION_BLOCKED / SCIENTIFIC_AND_PERFORMANCE_USE_PROHIBITED`
