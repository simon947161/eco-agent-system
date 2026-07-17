# ClimateOS Secret and Network Egress Decision Register v0.1

Date: 2026-07-18

Status: EMPTY_STATIC_REGISTER / NO_SECRET / NO_ENDPOINT / NO_NETWORK

## 1. Secret metadata contract

Future secret records must contain metadata only—never the secret value:

1. stable secret metadata ID;
2. secret class and purpose;
3. issuing authority and account boundary;
4. permitted consumer process identity;
5. injection method and non-persistence rule;
6. scope and least privilege;
7. creation, expiry and rotation times;
8. revocation owner and incident path;
9. logging/redaction requirements;
10. proof that source, logs and outputs do not contain the value.

Possible classes include API token, access key, certificate/private key,
password, session credential and service identity. These are vocabulary only;
none exists or is requested here.

## 2. Secret states

| State | Meaning |
|---|---|
| `SECRET_NOT_REQUIRED` | design can operate without a secret |
| `SECRET_REQUIREMENT_UNJUSTIFIED` | claimed need lacks bounded evidence |
| `SECRET_METADATA_INCOMPLETE` | identity/scope/consumer/expiry absent |
| `SECRET_CREATION_NOT_AUTHORIZED` | no account or credential authority |
| `SECRET_INJECTION_NOT_CONFIGURED` | no environment/sandbox injection path |
| `SECRET_PRESENCE_UNVERIFIED` | non-presence evidence absent |
| `SECRET_REVOKED` | authority ended; use must fail |
| `POTENTIAL_SECRET_EXPOSURE` | access/log/output boundary may be breached |

Current state: `SECRET_NOT_REQUIRED / SECRET_CREATION_NOT_AUTHORIZED`.

## 3. Network egress request contract

A future egress request must declare:

| Field | Requirement |
|---|---|
| destination identity | exact hostname/service identity; wildcard prohibited |
| resolution | DNS/IP relationship and change handling |
| protocol/port | exact values; no “any” |
| direction | outbound only unless independently justified |
| purpose | one bounded operation |
| request/data class | exact metadata/content classification |
| response/data class | expected return classification |
| byte/request ceiling | pre-authorized finite ceiling |
| valid interval | start, expiry and revocation |
| redirects | deny or list exact approved behaviour |
| proxy/TLS | exact trust and verification boundary |
| logging | connection, volume, status and denial records without secrets |
| output handling | quarantine and release-review path |

No destination, allowlist or network rule is created in this batch.

## 4. Egress states

| State | Meaning |
|---|---|
| `DENY_ALL_DEFAULT` | no network authority |
| `DESTINATION_UNSPECIFIED` | exact destination absent |
| `PURPOSE_OR_DATA_FLOW_UNCLEAR` | transfer need/content unresolved |
| `TERMS_OR_ACCOUNT_REQUIRED` | separate service/account gate needed |
| `ALLOWLIST_PROPOSED_INACTIVE` | static future proposal only |
| `TIME_BOUNDED_APPROVAL_REQUIRED` | separate Founder/security authority needed |
| `EXPIRED_OR_REVOKED` | connection must fail |
| `BLOCK_AND_ESCALATE` | attempted use exceeds approved scope |

Current state: `DENY_ALL_DEFAULT`.

## 5. Desk check A — wildcard internet request

Request: allow all HTTPS destinations so a future process can retrieve whatever
it needs.

Decision: `REJECTED / DESTINATION_UNSPECIFIED / PURPOSE_OR_DATA_FLOW_UNCLEAR`.

Wildcard destination, open-ended purpose, unknown redirects, unbounded transfer
and absent terms/account review violate least privilege.

## 6. Desk check B — long-lived secret injection

Request: create a reusable credential and place it in a general environment
variable for any child process.

Decision: `REJECTED / SECRET_REQUIREMENT_UNJUSTIFIED / SECRET_CREATION_NOT_AUTHORIZED`.

The request lacks an exact consumer, scope, expiry, revocation, injection,
redaction and non-persistence boundary. No secret or environment variable is
created.

## 7. Revocation and evidence

- expiry and revocation are enforced states, not annotations;
- a changed destination, process, purpose or data class requires a new request;
- denial and attempted use records are append-only;
- secret values never enter tickets, manifests, logs, Git, prompts or outputs;
- a suspected exposure triggers containment, revocation and specialist review;
- recovery never reactivates permission automatically.

## 8. Boundary verification

| Boundary | Result |
|---|---|
| real actor/process/endpoint selected | no |
| secret/key/token/certificate/account created | no |
| allowlist/firewall/proxy/DNS rule created | no |
| network request/connection performed | no |
| sandbox/config/environment created | no |
| clone/install/execute | no |
| compute/storage/cloud/payment | none / AUD 0 |
| expert contact | none |
| security/scientific conclusion | none |

## 9. Register decision

`EMPTY_REGISTER_VALID / ALL_PERMISSIONS_DENIED / NO_SECRET / NO_EGRESS / WILDCARD_AND_LONG_LIVED_REQUESTS_REJECTED`
