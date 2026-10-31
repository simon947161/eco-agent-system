# P04 semantics validation â€” 2026-10-27

Baseline f5967f25d2829183b8fb60cd3cc178c3927f1a75. Python3.14; optional GIS dependencies supplied via isolated PYTHONPATH; native header acquisition used isolated h5py3.15.1/numpy2.5.4. No production dependency change.

| Actual command/check | Result |
|---|---|
| `python -B tools/inspect_awra_netcdf_header.py --variable rain_day --output .local/p04-semantics-20261027/native` | HTTP206;10ranges;81920bytes; native metadata and coordinates captured |
| Same command with `--variable sm_pct` | HTTP206;10ranges;81920bytes; native metadata and coordinates captured |
| `python -B -m unittest tests.test_p04_semantics tests.test_p04_spatial_admission` |19run,19passed (10new semantic/HTTP guard tests,9existing spatial tests) |
| `python -B -m unittest discover -s tests` in isolated source copy |518run, OK,1skipped;517passed |
| SHA256 of four pre-existing generated-report modifications | All4 unchanged against prior preserved-report baseline; excluded from commit |
| `git -c core.whitespace=cr-at-eol diff --cached --check` | Passed for current tracked changes |

An initial targeted invocation also named nonexistent `tests.test_p04_water_soil_climate_preflight`:19actual tests passed and one module-import error occurred. The correct existing module is `tests.test_p04_preflight`, which passed in full discovery. This invocation error is not hidden or represented as a science/data failure.

The full suite ran in `.local/p04-semantics-regression-copy`, excluding git metadata, local state, runtime databases and dependency trees. Generated reports were written only inside that copy. No owner-private site changes or redeployment occurred; prior site acceptance was reused, not claimed as retested.

Offline tests verify exact evidence hashes, leap-February bounds, rejection of changed calendar/unit/incomplete bounds, refusal of full or oversized range responses and changed remote size, and the retained BLOCKED result. Passing software tests does not approve unresolved scientific semantics, source quality or cross-product comparability.

Exact publisher response bytes retain original whitespace; evidence-directory attributes disable whitespace rewriting/checks. Execution-state CRLF style is preserved from baseline.
