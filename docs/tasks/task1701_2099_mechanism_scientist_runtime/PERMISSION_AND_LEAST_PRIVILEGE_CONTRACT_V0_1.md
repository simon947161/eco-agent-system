# ClimateOS Permission and Least-Privilege Contract v0.1

Date: 2026-07-18

Status: STATIC_CONTRACT / ALL_PERMISSIONS_DENIED / NO_ENVIRONMENT

## 1. Permission request identity

Every future request requires:

| Field | Rule |
|---|---|
| `permission_request_id` | stable `MECH-PERM-NNN`; never reused |
| `request_revision` | immutable revision identifier |
| `actor_role` | accountable role; person only after separate consent |
| `process_identity` | exact artifact, manifest and executable identity |
| `purpose` | one bounded, reviewable purpose |
| `scope` | exact resources and actions; no implied access |
| `valid_from` / `expires_at` | bounded interval; no perpetual approval |
| `revocation_owner_role` | role able to revoke immediately |
| `state` | one controlled permission state |

Allowed states are `DENIED_DEFAULT`, `REQUESTED_UNREVIEWED`,
`APPROVED_BUT_INACTIVE`, `ACTIVE_TIME_BOUNDED`, `EXPIRED`, `REVOKED`, and
`BLOCKED_POLICY`. Task1761–1770 uses only `DENIED_DEFAULT`.

## 2. Permission dimensions

Each dimension is independently denied unless a future exact request is
separately authorized:

| Dimension | Required future scope |
|---|---|
| process execution | exact executable/arguments and parent process |
| child process | exact permitted child identities and count |
| filesystem read | exact read-only path/object set |
| filesystem write | exact temporary/output path, quota and retention |
| create/delete/rename | explicit operations and bounded paths |
| environment | exact non-secret variables and values' provenance |
| secret access | secret metadata ID, consumer and injection boundary |
| DNS resolution | exact approved names and resolver boundary |
| outbound connect | exact destination, protocol, port and purpose |
| inbound listen | explicit interface/port and necessity; default denied |
| IPC | exact mechanism and peer identity |
| device/hardware | exact device class; default denied |
| clock/time | fixed or real-time requirement and reproducibility effect |
| resource use | CPU, memory, process, time, disk and output ceilings |

One granted dimension does not imply another. Read access does not grant write,
DNS does not grant connection, and connection does not grant arbitrary data
transfer.

## 3. Least-privilege rules

1. Deny by default.
2. Bind permission to one actor role, process identity, purpose and revision.
3. Prefer no secret, no network, read-only inputs and temporary bounded writes.
4. Prohibit wildcard paths, destinations, protocols, subprocesses and durations.
5. Separate build, test, runtime and output-release authority.
6. Make approvals time-bounded, revocable and non-transferable.
7. Record denied attempts without expanding authority automatically.
8. Expiry or revocation terminates authority; it does not merely warn.
9. A changed artifact, manifest, configuration or purpose requires a new request.
10. Human approval cannot replace missing identity, licence or security evidence.

## 4. Approval record requirements

A future approval record must include reviewed request revision, approving role,
evidence considered, exclusions, exact permissions, start/expiry, revocation
method, logging destination, incident path and residual uncertainty.

No approval record is created in Task1761–1770.

## 5. Breach responses

| Breach | Static response |
|---|---|
| unknown process or child | deny/stop; preserve audit evidence |
| path outside scope | deny/abort future execution |
| unapproved environment/secret request | deny; treat as possible exposure |
| destination/protocol outside scope | block connection; contain |
| expired/revoked request used | deny and escalate governance review |
| logging unavailable/tampered | invalidate future run/result promotion |
| resource ceiling exceeded | terminate under pre-registered rule |

## 6. Current decision

`STATIC_PERMISSION_CONTRACT_READY / ALL_DIMENSIONS_DENIED_DEFAULT / NO_APPROVAL / NO_ENVIRONMENT / NO_EXECUTION`
