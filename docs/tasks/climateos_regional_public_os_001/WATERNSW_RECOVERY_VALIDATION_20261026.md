# WaterNSW existing-access recovery validation

Baseline: `609e94cd93881aec3ec7137c96b809ad66726ab4`; same #128 / Draft #129 branch. Consumed Issue comment [6411695965](https://github.com/simon947161/eco-agent-system/issues/128#issuecomment-6411695965) and the versioned prior-access handoff. Historical successful account/API use is acknowledged; today's missing configuration does not invalidate it. Earlier P03 acceptance is retained as a dated observation, not rewritten.

## Results

| Gate | Actual result |
|---|---|
| Prior code | VERIFIED: PR111/112/113 are merged; current checkout contains historical characterisation, eight-dimensional comparability gate and exact-byte WaterNSW admission adapter |
| Existing intake | `mittagang_410033_flow_intake.py` is a BOM HRS CSV intake, not an authenticated WaterNSW client; do not substitute it for Daily/Combined/FlowRate |
| Secret configuration | BLOCKED: no WaterNSW-named variables in current process, User or Machine environment; no `.env*` candidate in inspected project tree. No secret values printed |
| Old capture | NOT_RECOVERED: exact named `WATERNSW_410033_DAILY_FLOWRATE_CAPTURE_2026-08-04.json` not found in accessible authorized workspace |
| Old branch/commit | NOT_RECOVERED: no matching WaterNSW branch or resolvable `b6197e2e` in inspected ClimateOS root and seven project checkouts. No claim about other machines/unreachable Git objects |
| Subscription entitlement/cost | UNVERIFIED_CURRENT: historical subscription exists; current account product, limits and fee conditions cannot be inspected without restored access |
| Authenticated source read | NOT_ATTEMPTED: zero WaterNSW data requests; no guessed endpoint, subscription, purchase, proxy or 403 bypass |
| Exact-byte admission | BLOCKED_MISSING_RAW_RESPONSE: new dated blocked receipt produced with the existing PR113 function; original historical receipt not overwritten |
| Science | NOT_COMPARABLE_YET; no historical percentile, trend, current water-condition or causal claim |

Search scope was the existing authorized ClimateOS workspace, project filenames/code and local Git refs, plus WaterNSW-specific environment-name presence. Unrelated password managers, browser credentials and Council systems were not inspected. An old prototype cache directory was inaccessible; no claim of exhaustive recovery beyond readable project files. No matching credential location was found, so no generalized secret-store search was attempted.

## The one configuration gate

Restore the **existing Water Data / Surface Water Data API subscription key to the authorized local runtime's secret configuration**, from the existing account at the [official WaterNSW portal](https://api-portal.waternsw.com.au/). Do not register again, create a paid subscription, or paste a key into chat/GitHub. No historical environment-variable name or secret-store binding was recovered, so none is falsely documented as an established binding.

Alongside that local binding, recover the subscription's official operation definition and zero-cost entitlement/limits: station410033, Daily/Combined/FlowRate, one bounded date window, exact endpoint and authentication header. Current key presence is not proof of validity. Once available, the already authorized next action is one read-only request, with redirects/retries disabled and a size ceiling, exact bytes retained Git-ignored, sanitized retrieval receipt and SHA256 fed to `admit_response`. Keep operational evidence separate from HRS. No request was issued in this run.

PR113 is a byte/provenance admission helper, not a complete payload schema validator: it checks top-level JSON and retrieval metadata; its current implementation does not itself parse observation timestamps or quality codes from arbitrary payloads. The official response schema must therefore be validated by the recovered retrieval path before L1 admission. This limitation is not concealed by passing fixture tests. PR112 scientific gates remain separate.

## Actual testing

```powershell
python -B -m unittest discover -s tests -p 'test_waternsw_near_current_evidence_admission.py' -v
python -B -m unittest discover -s tests -p 'test_mittagang_410033*.py' -v
python -B -m unittest discover -s tests -p 'test_p04_preflight.py' -v
```

Results: 4 + 14 + 1 = **19 passed**, no skipped tests. Initial sandbox execution of the middle group had 5 temporary-directory permission errors; the permission-enabled rerun passed all14 without code changes. These are unit/reproduction checks, not successful authenticated network acceptance. No production code was rewritten. The prior 499-test regression remains historical; it was not relabelled a new full run. Four pre-existing report modifications remain untouched and excluded from commits.

P04 proceeds independently through [P04_INPUT_ADMISSION_20261026.md](P04_INPUT_ADMISSION_20261026.md). Sites owner-private v2 and reviewed July records were not modified. Rollback this documentation/state commit if needed; no API data, account, deployment or runtime schema was changed in this recovery turn.

Radar: knowledge—historical access differs from current configuration; decision—reuse PR113 and retain PR112; risk—unknown present entitlement and incomplete payload validation; open question—local secret binding and official operation definition; next action—restore existing key locally while continuing P04 product admission; keywords—WaterNSW, ClimateOS, 410033, L1, provenance, P04.
