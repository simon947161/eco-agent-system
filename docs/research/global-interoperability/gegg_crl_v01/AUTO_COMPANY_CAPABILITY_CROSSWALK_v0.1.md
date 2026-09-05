# Auto-Company Capability Crosswalk v0.1

| Reference capability | GEGG mapping | Decision | Required replacement/control |
|---|---|---|---|
| continuous loop | Mission Control worker | design only | bounded iterations, expiry and Founder pause |
| `consensus.md` baton | ACTP/CRP runtime state | adapt | schema, evidence ledger, authority and hashes |
| dynamic expert team | capability router | adapt | verified capability, not celebrity persona |
| CEO final decision | governance authority | reject | Founder/board/object-specific grant |
| crash recovery | resume safety | adopt concept | checkpoint validation and idempotency |
| circuit breaker | runtime control | adopt concept | failure budget and protected stop |
| dashboard | observability | adopt concept | provenance, spend, gate and evidence status |
| autonomous deploy/marketing | protected external action | prohibit | contact/deployment gates |
| host-level CLI permissions | execution boundary | prohibit | least privilege and isolated workspace |

Status: `REFERENCE_ONLY`; code ingestion `HOLD`; daemon installation `FALSE`.

