# V1.6 E0 — actual baseline stabilisation

2026-10-29 (Australia/Sydney). Remote baseline: c0683cf504333d97fc593660fd18f4b3fa006af5; branch feature/public-strategy-atlas-web-mvp-20261029; PR #130.

PASS_TESTED_HERE: six native Node suites, audit CLI, JavaScript syntax, actual system Chromium through Python Playwright at 1440×900, 390×844 and 2560×1080. `node apps/public-strategy-atlas/run-tests.cjs qa-output.json` discovers every native suite, preserves failure/spawn-error status and records output. `python3 apps/public-strategy-atlas/qa/e0-browser.py` runs the browser regression against a static server at port 8877.

Verified csp6/water/area accounting, explicit observed/synthetic labels, units and UNKNOWNs, keyboard Escape/focus return, viewport/panel overflow, local editing/diff, explicit IndexedDB save/load, two-tab stale-save rejection, actual downloaded snapshot and workspace independently checked in Node. No browser script errors. Source statuses remain unchanged. Saved actual screenshots and machine-readable outputs are in `qa/e0/`.

Fixed a real accounting usability problem: the shortcut could scroll the section heading under the sticky inspector heading. Added scroll margin and definition-list styles; the browser runner now waits for the section to clear the sticky heading before taking screenshots. The first screenshots were taken during smooth scrolling and were replaced by settled-scroll captures.

The original 127-item dataset digest remains sha256:13e765c81f1340918322b1e985da85f2362da3c72e1997804f952865edf365d2. Original event head remains sha256:963d8d32f0807a40a90db8c255cba4da5cac53a2491b94589139e96d3b372126. Downloaded legacy snapshots/workspaces verify unchanged.

BLOCKED_BY_PERMISSION / NOT_TESTED: fresh PDF byte verification. The original summary PDF is not present in this new checkout; fetching the official public URL through the inherited proxy returned CONNECT 403. No PDF was redistributed; no hashes or TLS settings bypassed. Fresh public-source verification requires saved Council/NSW domain additions to be applied in environment settings.

PR public page title retrieved successfully and identifies Draft PR #130. API check was denied; Git pull/130/head equals the named branch baseline. No draft-state mutation, merge, deployment, main/PR129 write or paid service.

SOFTWARE_CAPABILITY: PARTIAL — E0 verified; E1–E10 remain. PUBLIC_CORPUS_COVERAGE: PARTIAL/UNKNOWN. OFFICIAL_ADMISSION: PENDING, zero official mappings. Physical hardware, full screen-reader/WCAG, 32:9 and full official corpus are NOT_TESTED.
