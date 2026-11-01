# Recovery and P02 local acceptance — 2026-10-26

## Observed recovery

Recovered the existing `codex/regional-public-os-001-taskbook` branch in an isolated checkout from `simon947161/eco-agent-system`. HEAD `11327bc70ba1fa4c2ff995b604acbca48622a3d4` contains predecessor `42e8df72a549752a7f15a64f0ba6c58c1f11f49d`. PR129 is open Draft, unmerged. PR127 remains open Draft, unmerged at `6a20de8c21ed3587e521e3d10b0785b11be6d8f5`. Read Issue128's latest continuity comments and all eight requested task/research/state documents. Old START_HERE/TASKBOOK UI-pending statements are superseded by VALIDATION and actual code.

The workspace parent is not the executable repository. Several historical checkouts exist; the old primary checkout contains unrelated modified/untracked files. None was altered. An old untracked `prototype/climateos-local-controlled-prototype-core/` scaffold exists, with runtime export folders, but inspected source/test directories contain no files. It is not established as the Work research extension. No `Codex工作任务书.md`, `验收记录.md` or corresponding eleven-test implementation was recovered in the authorized workspace or recovered branch history. Status: **LOCAL_PROTOTYPE_NOT_RECOVERED**. This does not block the independently complete GitHub continuation path.

## Reused and implemented

Reused the existing localhost server, `/program.html`, policy Console, research lines and persistent research database. Reused the existing program digest/stable-ID functions and Receipt/Passport review semantics. Added one source adapter/table and a read-only `/api/streamflow?start=YYYY-MM-DD&end=YYYY-MM-DD` endpoint. Monthly record meanings and prior policy UI are preserved. The quantitative source Receipt/Passport is a research extension and does not promote or amend a reviewed monthly cycle.

Fixed-source public data → CSV validation → immutable SQLite revision including raw snapshot → date-filtered chart/table → original source header/quality/licence/digests → reproducible Receipt/Passport. Corrupted stored evidence is rejected; no GET performs a network refresh. No automatic scientific or governmental assessment is produced. No paid dependency was added.

## Actual public source and permission

- [BOM HRS official download](https://www.bom.gov.au/water/hrs/content/data/410033/410033_daily_ts.csv).
- [Product-specific copyright table](https://www.bom.gov.au/water/hrs/copyright.shtml): Water NSW links to **CC BY 3.0 AU**, attribution **© WaterNSW**. This is more specific than the HRS page-wide CC BY 4.0 notice. Retain owner/BOM attribution, licence and parsing modification notice. No logos or endorsement.
- [Quality definitions](https://www.bom.gov.au/water/hrs/qc_doc.shtml). Preserve A/B/C/E/G; G is modeled gap filling, E unreliable. No silent filtering, interpolation or causality inference.
- Station 410033: Murrumbidgee River at Mittagang Crossing, 149.09 E / 36.17 S, upstream catchment 1889.8 km². Station selector metadata and CSV agree. Catchment is not Council boundary or a town supply service area.
- Dataset version: September, 2026; 22,645 daily records, 1964-03-01–2026-02-28. A=12058, B=7192, C=160, E=3235, G=0; absent dates=0, null values=0. No claim that this establishes completeness of the underlying measurements.
- SHA256 `78e8188f3f445afa33ad466dd0554e653761ef617832b6df3a9eac6b1240ca1a`.
- Source header says `Flow (ML)` but description says `ML/day`; display as ML per daily interval, preserve both. Previous 24-hour total reported at 09:00 local time; no UTC offset is provided, so calendar labels are not falsely converted. Retrieval timestamp is UTC.
- Header extraction date `4/06/2024` conflicts with records through 2026; retained verbatim and flagged. No claim that extraction date is current.
- Historical coverage is 240 days old at acceptance; status **HISTORICAL_STALE_FOR_CURRENT_USE**. This is a 90-day display freshness rule, not a hydrological safety threshold.

Official bytes downloaded successfully using Windows `Invoke-WebRequest`. Python `urlopen` independently returned HTTP403: direct Python refresh is **not verified**. Do not retry indefinitely, bypass source controls or claim unattended acquisition. Snapshot import is the verified path. Raw bytes, SQLite, source HTML/JS and browser evidence remain local and ignored.

## Reproduce

From the repository root:

```powershell
New-Item -ItemType Directory -Force .local | Out-Null
Invoke-WebRequest 'https://www.bom.gov.au/water/hrs/content/data/410033/410033_daily_ts.csv' -OutFile .local/410033_daily_ts.csv -TimeoutSec 30
python -B tools/import_hrs_streamflow.py --snapshot .local/410033_daily_ts.csv --db .local/p02-verified.sqlite3
python -B run_environmental_question_runtime.py --db .local/p02-verified.sqlite3 --port 8777
```

Open `http://127.0.0.1:8777/program.html`. Import and server must use the same database. Reimporting unchanged bytes preserves its stored revision/Receipt. Raw records and the full source header are persisted in `hrs_revisions`; no production database is required. Stop the server to close the local demonstration; rollback code through a normal revert, preserve or separately archive local research data.

## Actual checks

- `python -B -m unittest discover -s tests -p test_smrc_policy_console.py -v`: 5 passed.
- `python -B -m unittest discover -s tests -p test_policy_console_integration.py -v`: 2 passed, including `/api/policy-context`, `/program.html` and source-gap propagation. Three original policy PDFs not recovered here: resolver reports missing, not matching. Recorded historical hashes are retained, not re-certified.
- Baseline `python -B -m unittest discover -s tests`: 489, OK, 1 skipped.
- New `python -B -m unittest discover -s tests -p test_hrs_streamflow.py -v`: 4 passed. Synthetic fixtures are explicitly labelled; tests cover station/unit/quality rejection, duplicate dates, nonfinite/negative values, missingness, gap-filled values, persistent replay/idempotence, tamper rejection and bounded HTTP readback.
- Final `python -B -m unittest discover -s tests`: 493, OK, 1 skipped. Initial new-test failure exposed unclosed SQLite connections on Windows; fixed using explicit closing, then rerun passed. Initial sandbox TEMP/socket failures resolved with workspace-local TEMP and authorized socket access.
- `node --check cczps_lite/environmental_question_runtime/static/streamflow.js`: passed. `git diff --check`: checked before commit.
- Browser: existing five policy cards/three lines loaded; historical flow chart loaded; selecting 2026-02-01–2026-02-28 returned 28 rows; quality distinction and expanded licence/header/Receipt/Passport visible. No trend, current supply, water-quality or causal conclusion. Mobile acceptance not performed.
- Regression tests generate four existing tracked report outputs; these unrelated generated changes are excluded from the implementation commit and preserved unstaged.

## Deployment and remaining scope

Sites account access confirmed; no ClimateOS site found. Existing unrelated Sites were not changed. No Site created or deployed. Python/SQLite cannot simply be uploaded as a Worker: a public-safe data package and read-only Worker adapter need separate acceptance. No scheduler, canonical KITTY readback or human scientific approval is claimed. **P02 local vertical slice VERIFIED; parent P02 remains in_progress with private Sites staging outstanding.**

## Conversation Radar

- Knowledge: registered HRS source has a real historical daily series; supplier licence overrides generic footer; poor/unreliable records matter.
- Idea: use this same evidence layer for T1 water and T2 catchment questions; T3 supplies shared traceability.
- Decision: extend the existing Console; manual snapshot import; immutable local revision; no parallel OS, team or Issue.
- Risks: stale coverage, source-header date conflict, quality uncertainty, unspecified UTC offset and Python403.
- Open questions: current-data acquisition permission/availability, source-header correction, private Worker persistence/version mapping, missing Work prototype.
- Next action: package this verified historical slice for private Sites with exact code/data version and owner-only access readback, preserving explicit historical status.
- Keywords: ClimateOS, P02, T1, T2, T3, HRS, WaterNSW, 410033, Evidence Passport, Run Receipt, public-data licence.
