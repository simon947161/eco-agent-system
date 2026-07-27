# Source, Licence and Retention Register

## 1. Register

| Source | Authority | Access | Raw retention | Public repository retention | Admission |
|---|---|---|---|---|---|
| BoM Cooma Daily Weather Observations July 2026 | Australian Bureau of Meteorology | direct official HTTPS CSV, zero cost | local gitignored evidence area | URL, digest, byte count, coverage and missingness metadata only | `OFFICIAL_OBSERVATION / L1_MAXIMUM` |
| BoM Southern Hemisphere monitoring archive 14 July 2026 | Australian Bureau of Meteorology | direct official HTTPS HTML, zero cost | local gitignored evidence area | URL, digest and bounded attributed source facts only | `OFFICIAL_OUTLOOK / L1_MAXIMUM` |

## 2. Why raw data is not committed

The Bureau's general copyright notice requires the user to check product-specific
terms. Where no broader licence is stated, it permits personal or organisational
use but does not create a general right to supply original content to third
parties or use it commercially.

This public repository therefore does not copy the original CSV rows or HTML
body. The real-data pilot remains auditable through:

- exact source URL;
- retrieval timestamp;
- HTTP and content type;
- response byte count;
- SHA-256 digest;
- local raw-path identity in the full private receipt;
- parser and validator version;
- bounded public coverage/missingness metadata.

If a later review confirms a product-specific open licence, the retention policy
may be revised prospectively. No open-reuse status is inferred here.

## 3. Refresh rule

Retrieval is manual only. Every refresh requires:

- explicit human approval;
- exact HTTPS allowlist;
- response-size ceiling;
- redirect validation;
- new immutable digest and receipt;
- no silent overwrite of a prior evidentiary identity;
- no automatic promotion from changed data to changed environmental condition.
