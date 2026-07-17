# ClimateOS Output Quarantine, Inspection and Release Register v0.1

Date: 2026-07-18

Status: EMPTY_STATIC_REGISTER / QUARANTINE_BY_DEFAULT / NO_OUTPUT

## 1. Quarantine principle

Any future runtime-generated output enters quarantine before viewing, copying,
interpretation, publication or downstream use. Existence of a receipt, exit code
or file does not grant release. Quarantine is a governance state, not a storage
location created by this task.

No runtime output, directory, storage object or quarantine environment exists in
this batch.

## 2. Future output-set identity

Every future output set requires:

| Field | Rule |
|---|---|
| `output_set_id` | stable `MECH-OUTPUT-SET-NNN`; one run attempt only |
| `run_receipt_id` | exact receipt binding; cannot be blank |
| `member_manifest_revision` | immutable list revision |
| `producer_process_identity` | exact admitted producer identity |
| `declared_format_class` | bounded format/media/data class |
| `provenance_state` | source and transformation evidence status |
| `licence_state` | inherited/admitted obligations and unresolved terms |
| `integrity_state` | receipt-bound evidence status, not an invented hash |
| `sensitivity_class` | public, restricted, secret-risk or unknown |
| `retention_decision` | bounded retain/destroy decision after authority |
| `quarantine_state` | one controlled state below |

The member manifest must describe paths or object identities, sizes, formats,
expected/observed classification, producer, timestamps, declared content risks
and prohibited downstream uses. These are future requirements only.

## 3. Quarantine states

| State | Meaning |
|---|---|
| `NO_OUTPUT` | current state; no runtime output exists |
| `QUARANTINE_REQUIRED` | default for any future claimed output |
| `QUARANTINED_UNINSPECTED` | contained but inspection not authorized/performed |
| `PROVENANCE_UNRESOLVED` | receipt or transformation chain is incomplete |
| `INTEGRITY_UNVERIFIED` | integrity evidence is absent or inconsistent |
| `SECRET_OR_SENSITIVE_RISK` | content may breach access/redaction rules |
| `LICENCE_OR_USE_UNRESOLVED` | downstream use rights are unclear |
| `INSPECTION_FAILED` | inspection evidence is incomplete or unsafe |
| `REDACTION_REQUIRED` | release cannot occur before governed redaction |
| `RELEASE_BLOCKED` | output must not leave quarantine |
| `RELEASE_APPROVED_INACTIVE` | static decision only; transfer still separate |
| `DESTROY_OR_RETAIN_PENDING` | disposition requires explicit authority |

No release state is assigned to a real object in Task1771–1780.

## 4. Future inspection record

Inspection requires independent authority and must record:

1. inspection request/revision and accountable reviewer role;
2. output-set and receipt identities;
3. isolated inspection method and admitted tool identity;
4. permissions, secret/network state and resource ceilings;
5. format, malware, corruption and unexpected-content checks;
6. provenance, integrity, licence and sensitive-content findings;
7. scientific-content review status, kept separate from security inspection;
8. redactions or transformations as new derived-output identities;
9. exceptions, unavailable evidence and residual uncertainty;
10. decision, validity interval, conditions and revocation path.

This list does not authorize an inspection, tool, reviewer or environment.

## 5. Release decision contract

A future release decision must separately answer:

- is the receipt structurally accepted and free of unresolved tamper signals?
- is the exact output-set identity complete and provenance-bound?
- are format/security inspection results acceptable for the intended use?
- are secrets, personal/restricted data and licence terms resolved?
- is scientific interpretation separately reviewed where required?
- are destination, audience, purpose, retention and prohibited uses exact?
- is transfer itself authorized under permission/network contracts?
- are release conditions time-bounded, revocable and logged?

All answers must be evidenced. A missing answer means `RELEASE_BLOCKED`.

## 6. Static release register

| Register field | Current value |
|---|---|
| real output-set records | none |
| receipt-bound objects | none |
| quarantine location | not created |
| inspection request/tool/reviewer | none |
| release request/approval | none |
| retention/destruction action | none |
| transfer/destination/audience | none |
| current decision | `NO_OUTPUT / EMPTY_REGISTER` |

## 7. Desk check A — output without receipt

Fictional claim: a file appears useful but has no receipt or producer identity.

Decision: `PROVENANCE_UNRESOLVED / INTEGRITY_UNVERIFIED / RELEASE_BLOCKED`.
Usefulness cannot replace provenance. No file is created or inspected.

## 8. Desk check B — clean structure but unreviewed meaning

Fictional claim: a structurally complete receipt and expected file format justify
publishing a scientific interpretation.

Decision: `QUARANTINE_REQUIRED / RELEASE_BLOCKED`.
Structural evidence does not validate scientific meaning, fitness or regional
conclusions. Independent scientific review and release authority remain absent.

## 9. Boundary verification

| Boundary | Result |
|---|---|
| logger/runtime/receipt instance | none |
| runtime output or quarantine store | none |
| inspection/release execution | none |
| sandbox/configuration | none |
| secret/account/network | none |
| clone/download/install/execute | none |
| compute/storage/cloud/payment | none / AUD 0 |
| expert contact | none |
| scientific/security conclusion | none |

## 10. Register decision

`EMPTY_REGISTER_VALID / QUARANTINE_BY_DEFAULT / NO_OUTPUT / NO_INSPECTION / NO_RELEASE`

