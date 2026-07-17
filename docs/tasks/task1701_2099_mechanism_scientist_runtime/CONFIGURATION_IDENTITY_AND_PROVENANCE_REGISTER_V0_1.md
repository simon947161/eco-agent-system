# ClimateOS Configuration Identity and Provenance Register v0.1

Date: 2026-07-18

Status: EMPTY_STATIC_REGISTER / NO_CONFIGURATION / NO_EXTERNAL_INSPECTION

## 1. Controlled state register

| State | Meaning | Required response |
|---|---|---|
| `MISSING_IDENTITY` | required component has no exact identity | stop manifest promotion |
| `LOCATOR_UNVERIFIED` | locator recorded but content not inspected | identity context only |
| `LICENCE_UNREVIEWED` | access/use/retention rights unresolved | no download, retention or use |
| `CHECKSUM_ABSENT` | no lawful admitted object available to hash | do not fabricate receipt |
| `ENVIRONMENT_UNSPECIFIED` | build/runtime identity absent | no reproducibility claim |
| `CONFIGURATION_NOT_CREATED` | no config artifact exists | no execution or semantic claim |
| `INPUT_NOT_ADMITTED` | input identity/authority absent | no access or run |
| `BOUNDARY_NOT_ADMITTED` | boundary identity/authority absent | no access or run |
| `DIAGNOSTIC_UNBOUND` | diagnostic implementation/version absent | no result interpretation |
| `OUTPUT_NOT_CREATED` | no authorized run/output exists | no result or conclusion |
| `SUPERSEDED` | later controlling revision explicitly replaces use | retain full lineage |
| `QUARANTINED` | integrity, licence or authority unresolved | block downstream use |
| `REPRODUCIBILITY_NOT_TESTED` | no independent later attempt exists | do not claim reproducibility |

## 2. Empty manifest register

| Register field | Current value |
|---|---|
| manifest ID | `MECH-RM-EMPTY-001` |
| purpose | protocol form desk check only |
| hypothesis revision | not selected |
| design revision | not selected |
| source repository identity | `LOCATOR_UNVERIFIED` / none selected |
| dependency identities | `MISSING_IDENTITY` |
| build/runtime environment | `ENVIRONMENT_UNSPECIFIED` |
| configuration | `CONFIGURATION_NOT_CREATED` |
| input | `INPUT_NOT_ADMITTED` |
| boundary asset | `BOUNDARY_NOT_ADMITTED` |
| diagnostic implementation | `DIAGNOSTIC_UNBOUND` |
| checksum receipt | `CHECKSUM_ABSENT` |
| output | `OUTPUT_NOT_CREATED` |
| reproducibility | `REPRODUCIBILITY_NOT_TESTED` |
| review state | `IDENTITY_INCOMPLETE` |

This register is not a model manifest, software bill of materials, environment
file, configuration or run record.

## 3. Desk check A — false completeness request

Request: mark the empty register reproducible because its required field names
are documented.

Decision: `REJECTED`.

Reasons:

1. schema completeness is not artifact completeness;
2. no source, dependency, environment, configuration or data identity exists;
3. no checksum was computed;
4. no build or run occurred;
5. no independent reproduction was attempted;
6. no consenting expert reviewed scientific semantics.

## 4. Desk check B — fabricated receipt request

Request: insert an example digest so downstream tooling sees a complete field.

Decision: `REJECTED / CHECKSUM_ABSENT`.

A digest may exist only after a separately authorized, lawful artifact is
admitted and hashed under a recorded method. Placeholder hexadecimal text,
zero hashes and copied upstream digests must not be represented as a ClimateOS
receipt.

## 5. Review and consent boundary

- a steward role may maintain the register but cannot approve scientific semantics;
- a licence role may review rights but cannot approve model/data fitness;
- an infrastructure role may review environment identity but cannot authorize conclusions;
- a scientific reviewer must consent separately and may return insufficient evidence;
- no person or institution is named, contacted or treated as appointed here.

## 6. Boundary verification

| Boundary | Result |
|---|---|
| external code/repository inspected | no |
| repository cloned/downloaded | no |
| configuration/environment created | no |
| real or synthetic artifact hashed | no |
| data/GIS/model/weight accessed | no |
| model/synthetic execution | no |
| compute/storage/cloud/account | none |
| cost | AUD 0 |
| expert contact/appointment | none |
| scientific/regional conclusion | none |

## 7. Register decision

`EMPTY_IDENTITY_REGISTER_VALID / COMPLETENESS_REJECTED / FABRICATED_RECEIPT_REJECTED / ALL_RUNTIME_GATES_CLOSED`
