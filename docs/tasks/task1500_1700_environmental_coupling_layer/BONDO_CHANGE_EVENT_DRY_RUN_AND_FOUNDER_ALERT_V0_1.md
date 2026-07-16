# Bondo Change Event Dry Run and Founder Alert v0.1

Date: 2026-07-16

Status: FICTIONAL_EVENTS_ONLY / NO_SOURCE_REFRESH / NO_ALERT_SENT

Task: ClimateOS Task1641–1650

## 1. Dry-run boundary

Both events below are invented to test routing. They do not describe a real
change to Bondo, NSW Planning, EPBC or the developer record.

## 2. Event A — non-material change

Hypothesis: the NSW page displays a new page-update timestamp, but project ID,
name, stage, description, turbine count, area and document identities remain
unchanged.

| Field | Dry-run result |
|---|---|
| Event ID | `DRY-NM-001` |
| Classification | `NON_MATERIAL_CHANGE` |
| New evidence version | metadata event only |
| Claim nodes frozen | none |
| Re-review | not required |
| Alert priority | log only |
| Scientific conclusion | none |

Decision:

`TRIGGER_RECORDED_NO_REVIEW_REQUIRED`

## 3. Event B — material layout/version change

Hypothesis: a later official EPBC layout attachment becomes accessible and is
clearly identified as a newer referral-stage layout containing 164 proposed
turbine positions, while the recorded NSW page still states up to 149.

| Field | Dry-run result |
|---|---|
| Event ID | `DRY-MAT-001` |
| Classification | `MATERIAL_SPATIAL_CHANGE` plus `AUTHORITY_CONFLICT` |
| Affected nodes | `C-002`–`C-006`, `V-001`, `V-002`, `G-001` |
| New object treatment | append new immutable EPBC layout version |
| Earlier objects | retained unchanged |
| Immediate route | provenance, licence and GIS/planning record review |
| Wind-science route | not opened unless scientific measurement evidence also changes |
| Controlling layout | unresolved pending stage/authority review |
| Scientific/project conclusion | prohibited |

Decision:

`CONTRADICTION_RETAINED / WAIT_FOR_FOUNDER_AUTHORIZATION`

The new attachment must not be called the approved or final layout solely
because it is later or contains coordinates.

## 4. Founder alert template

```text
CLIMATEOS INTERNAL FOUNDER ALERT — NOT EXTERNALLY SENT

Passport: <passport_id>
Event ID: <event_id>
Detected/recorded at: <timestamp>
Source family and authority: <source>
Previous object/version: <id>
New object/version: <id>
Access/licence state: <state>
Change class: <class>
Changed governed fields: <fields>
Affected claims/gaps: <ids>
Current contradiction: <summary>
Required review roles: <roles>
Acquisition/contact/cost requested: <none or explicit request>
Prohibited conclusions retained: <list>
Recommended Founder decision: <record / hold / authorize bounded next step>
```

## 5. Alert controls

- internal draft only; no email, Slack, API or notification dispatch;
- quote the source class and version rather than presenting all text as fact;
- expose what did not change;
- never use urgency to bypass licence, scientific or Founder gates;
- retain `no conclusion` when the event only changes document availability.
