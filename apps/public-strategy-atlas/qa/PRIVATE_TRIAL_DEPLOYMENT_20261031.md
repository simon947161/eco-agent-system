# Council owner-private trial — 31 October 2026

Published URL: https://council-strategy-intelligence.minshu.chatgpt.site

This is the existing `apps/public-strategy-atlas` application, not a replacement implementation. The Founder explicitly authorised an owner-only trial. Sites project `appgprj_6ae5b063565c8191802c9d7f7eb3214b` was created exactly once after checking app/root hosting manifests and all owner Sites. Its identity is persisted in the app-scoped `.openai/hosting.json`; the protected water Site was never reused.

## Publication and source

- Version 1; deployment `appgdep_6ae5b102d3c48191b2c6da8b77417b92`, native private publication returned `succeeded` with the URL above.
- Saved version `appgprj_6ae5b063565c8191802c9d7f7eb3214b~appgver_92bb5f7bf77481918a10f954d9067e9e`.
- Sites source SHA `54fed0a1b624a13c8670dc8bf01854587a73bb9b` is an exact app-scoped source snapshot from GitHub PR130 packaging commit `997a55a01e3571ebb91aa67eea36b767e3cca442`, with `UPSTREAM.json` identifying the canonical source. The tested application baseline is `13c64f44aa6b6dac40748bb7096a7dadd3d7352d`; all previously tested application code hashes are unchanged.
- The installed Sites source helper was unavailable in this executor. Native short-lived source credentials were supplied through hidden stdin; Git committed/pushed the exact source and independently read the same remote SHA. The static artifact was then passed to the native owner-private publishing operation. No persistent credentials, access settings, invitations or purchases were changed.
- The artifact has 35 runtime assets plus its asset manifest and hosting configuration, 37 files total. QA/source evidence is not served. No private Council/customer content was imported. Local deployment-source staging is a mirror, not a second source application.

## Access and actual verification

`get_site` confirms `custom` access, exactly one allowed user with role `owner`, zero editors, groups or external visitors, policy revision 1. This is an enforced private audience, not an unlisted public URL. No sharing changes were made.

Unauthenticated HTTPS requests to the homepage, `atlas.js` and the default snapshot asset returned 403. All 35 live runtime assets were fetched through the documented Sites service-access header and matched the canonical packaged SHA-256 hashes. Hosting redirects `index.html` to `/`; the verifier follows only that observed same-origin canonical redirect.

Two existing real Chromium suites passed against the deployed origin using supported Site service authentication, including 1440×900 and 390×844 layouts (the existing E0 suite also checks 2560×1080):

- PHE historical cards → exact source/clause evidence → independent review → work card → Annual Calendar; independent snapshot/path-proof export verification; explicit withdrawn-source import and source-isolated blocking.
- Route-first map and original 127-item base; accounting/source distinctions; explicit local edit/diff/IndexedDB save/load; two-tab stale-save rejection; exported workspace verification and no script errors/overflow.

The browser transport fetched actual deployed responses through the inherited HTTPS proxy and fulfilled requests on the deployed origin; it did not substitute local source files or fabricate visitor identity headers. 204 browser requests used GET, with no application network mutations or external origins. Initial Playwright `route.fetch` used an unavailable direct IPv6 route; the transport was corrected to use the inherited proxy. No app code, test assertions, timeouts, network policy or TLS verification was weakened.

**Owner interactive sign-in is not verified.** This executor has no signed-in owner browser session. Service access proves the deployed application works, but supplies no visitor identity and is not proof of the Founder's sign-in flow. Open the URL with the owning ChatGPT account for that final user check. A separate anonymous browser/proxy attempt failed with `net::ERR_CERT_AUTHORITY_INVALID`; TLS checks were not disabled. This infrastructure limitation is distinct from the verified anonymous HTTP denial. No login or authentication bypass was attempted.

Review/calendar plans remain in the current page's research state and are portable through explicit snapshot export/import. Existing workspace annotations require explicit local save/load. There is no server-side sync, automatic reminder, email, Council assignment or shared persistence; a different browser/origin does not automatically inherit local work. Current legal applicability, actual execution, spend and outcomes retain their UNKNOWN/PENDING boundaries.

## Protected website and remaining work

Read-only before/after comparisons confirm the original water Site remains unchanged: https://climateos-snowy-monaro.minshu.chatgpt.site, project `appgprj_6adefcfe720881918b4e32874f12dd86`, version 2, source `9f3a201d40c4b70d72f0b69c319805258769c242`, deployment `appgdep_6adf008a3d1c81918a673531038410d1`, access revision 1. Identity, URL, version/source history, deployment and complete access policy compare equal.

Evidence: `private-trial/deployment-receipt.json`, `private-trial/live-validation.json`, `private-trial/browser-phe-context.json`, `private-trial/browser-results.json`, `private-trial/anonymous-browser.json` and actual screenshots in `private-trial/`. `verify-private-trial.py` reuses existing browser assertions and takes only the supported transient service credential through hidden stdin. No credential values are in these files.

This completes private trial deployment, not CSOI overall. The engineering registry remains 49 VERIFIED / 28 PARTIAL / 3 BLOCKED; the three private WCOS dependencies remain deferred. No GitHub merge or change to main/PR129 occurred. The previous batch's 38-native/16-browser results are preserved as prior application evidence; this deployment adds byte verification and two live suites, not a falsely claimed fresh full regression.
