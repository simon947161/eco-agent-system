# ClimateOS Artifact Licence and Use-Rights Decision Matrix v0.1

Date: 2026-07-18

Status: STATIC_GOVERNANCE_MATRIX / NO_REAL_LICENCE REVIEW / NO_ADMISSION

## 1. Core rule

Public visibility does not establish permission to retain, execute, modify,
redistribute or publish derivatives. Each right is recorded separately and
remains `UNKNOWN_NOT_REVIEWED` until a future authorized review identifies the
controlling terms, version and artifact scope.

This matrix is governance scaffolding, not legal advice.

## 2. Artifact classes

| Class | Examples of future identity scope | Current state |
|---|---|---|
| source code | repository, commit, file/tree identity | none inspected |
| binary/package | package name, version, registry and checksum | none inspected |
| model/weight | architecture, checkpoint, version and file receipt | none inspected |
| dataset/input | dataset release, object, geography/time and receipt | none inspected |
| configuration | immutable config identity and semantic purpose | none created |
| documentation | document/version/locator identity | no external item reviewed |
| diagnostic/output | implementation or result identity | none created |
| hosted service/API | provider, service version, terms and account boundary | none accessed |
| toolchain/runtime | compiler, interpreter, OS, container and library identities | none created |

## 3. Independent rights dimensions

Every future artifact decision must record:

| Dimension | Controlled states |
|---|---|
| visibility | `PUBLICLY_VISIBLE`, `RESTRICTED`, `UNKNOWN` |
| access | `ACCESS_REVIEWED`, `REGISTRATION_REQUIRED`, `PAID`, `UNKNOWN` |
| local retention | `PERMITTED`, `PROHIBITED`, `UNKNOWN` |
| execution | `PERMITTED`, `PROHIBITED`, `SEPARATE_TERMS`, `UNKNOWN` |
| modification | `PERMITTED`, `PROHIBITED`, `CONDITIONAL`, `UNKNOWN` |
| redistribution | `PERMITTED`, `PROHIBITED`, `CONDITIONAL`, `UNKNOWN` |
| derivative output | `PERMITTED`, `PROHIBITED`, `CONDITIONAL`, `UNKNOWN` |
| attribution/notice | `DEFINED`, `NOT_REQUIRED`, `UNKNOWN` |
| source disclosure | `REQUIRED`, `NOT_REQUIRED`, `CONDITIONAL`, `UNKNOWN` |
| patent/trademark | `TERMS_IDENTIFIED`, `SEPARATE_REVIEW`, `UNKNOWN` |
| privacy/confidentiality | `NOT_APPLICABLE`, `RESTRICTIONS_IDENTIFIED`, `UNKNOWN` |
| geographic/use restriction | `NONE_IDENTIFIED`, `RESTRICTIONS_IDENTIFIED`, `UNKNOWN` |

An `UNKNOWN` state blocks the corresponding use. One permitted dimension does
not grant another.

## 4. Licence evidence contract

A future review record requires:

1. exact artifact and version identity;
2. controlling licence/terms identity and version/date;
3. authoritative locator and access date;
4. whether terms were actually inspected;
5. exact rights dimension being assessed;
6. obligations, exclusions and ambiguity notes;
7. dependency and third-party-material carve-outs;
8. conflict or precedence rules;
9. reviewer role and review limitation;
10. append-only decision and supersession history.

Repository-level terms do not automatically control submodules, weights,
datasets, examples, bundled assets or hosted services. A filename such as
`LICENSE` is not proof that every artifact is covered.

## 5. Licence evidence states

| State | Meaning | Response |
|---|---|---|
| `TERMS_NOT_INSPECTED` | no authorized review occurred | block all use beyond identity |
| `TERMS_IDENTITY_ONLY` | terms locator/version known, content not assessed | no permission inferred |
| `SCOPE_UNRESOLVED` | terms inspected later but artifact coverage unclear | quarantine affected artifact |
| `RIGHTS_DIMENSION_UNKNOWN` | required use right unresolved | block that use |
| `THIRD_PARTY_TERMS_REQUIRED` | component/assets have separate terms | split identities and review |
| `TERMS_CONFLICT` | governing terms appear inconsistent | preserve conflict; human/legal review |
| `TERMS_CHANGED` | later terms differ | append revision; no retroactive permission |
| `WITHDRAWN_OR_INACCESSIBLE` | controlling terms unavailable | preserve receipt; block new use |
| `REVIEW_COMPLETE_BOUNDED` | named dimensions reviewed for exact artifact/version | admit only separately authorized dimensions |

## 6. Admission outcomes

| Outcome | Meaning |
|---|---|
| `ADMIT_IDENTITY_ONLY` | retain bounded identity metadata only |
| `ADMIT_METADATA_ONLY` | retain reviewed metadata, not content or execution |
| `CONDITIONAL_REVIEW_REQUIRED` | no use until named condition and review are complete |
| `BLOCKED_LICENCE` | required right or scope unresolved |
| `BLOCKED_DEPENDENCY` | dependency chain prevents admission |
| `QUARANTINE_ARTIFACT` | preserve isolated identity/receipt; no downstream use |
| `DO_NOT_ADMIT` | artifact/use is outside authority or acceptable boundary |
| `LEGAL_OR_GOVERNANCE_REVIEW_REQUIRED` | issue exceeds current role; no decision inferred |

No outcome in Task1741–1750 applies to a real artifact.

## 7. Current decision

`STATIC_RIGHTS_MATRIX_READY / REAL_TERMS_NOT_INSPECTED / ARTIFACTS_NOT_ADMITTED / LEGAL_ADVICE_NOT_PROVIDED`
