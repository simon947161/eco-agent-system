# EP-SKILL-002 Option A Exact Network Token — DRAFT / NON-EXECUTABLE

```text
NETWORK_AUTHORISED:
FALSE

EXECUTION_REQUIRES_SEPARATE_FOUNDER_TOKEN:
TRUE
```

This draft is preparation only. It grants no authority and must not be passed to an executor as approval.

| Control | Candidate value requiring Founder confirmation |
|---|---|
| Provider/product | Australian Bureau of Meteorology Daily Weather Observations `IDCJDW2033`, Cooma stations `070278/070217` |
| Literal candidate URL | `https://www.bom.gov.au/climate/dwo/202609/text/IDCJDW2033.202609.csv` |
| Optional second provider/product | BoM Southern Hemisphere ENSO monitoring archive, exact dated archive URL must be inserted by Founder; absent URL means no request |
| Maximum requests | 1; increase to 2 only if the token supplies the literal ENSO URL |
| Maximum bytes | 2 MiB per response; 4 MiB total absolute ceiling |
| Timeout | 20 seconds per request |
| Redirects | Refuse all redirects unless the final URL exactly equals a separately listed Founder-approved URL |
| Raw retention | `runtime_data/ep_skill_002/raw/<token_id>/`, git-ignored, access-controlled local storage |
| Committed/public outputs | Redacted retrieval receipt, SHA-256, product/station identity, coverage metadata and admission decision only; no raw observation rows |
| Cost ceiling | `AUD 0`; stop on authentication, subscription, payment or metered-cost requirement |
| Licence/provenance | Confirm current BoM terms, final URL, HTTP metadata, retrieval time, content digest, product ID, station IDs, coverage and redistribution boundary before admission |
| Stop conditions | Identity/URL drift, redirect, non-200, size/timeout, malformed content, licence ambiguity, unexpected credential/cost, missing digest, or attempted current-condition/public conclusion |
| Expected receipts | retrieval receipt; evidence-admission receipt; Evidence Freshness Record; immutable Run Receipt with network/data truth fields |

WaterNSW, private Council sources, imagery, background jobs and automatic fallback are outside this draft. The candidate URL is not contacted by Option B.
