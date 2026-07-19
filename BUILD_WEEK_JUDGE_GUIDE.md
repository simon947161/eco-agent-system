# ClimateOS — Build Week Judge Guide

## Recommended evaluation path

ClimateOS is a long-horizon human–AI operating-system direction for climate
stewardship. The Build Week entry demonstrates one new, bounded Runtime slice;
it does not claim that the whole ClimateOS vision was built during the event.

### Requirements

- Python 3.10 or newer;
- a desktop browser;
- no API key, account, payment or network access;
- no dependency installation for the Task2002 Runtime.

### Run the stable merged demonstration

From the repository root:

```bash
python run_environmental_question_runtime.py
```

Open <http://127.0.0.1:8766> and keep the terminal process running. Press
`Ctrl+C` when finished.

Suggested review sequence:

1. Read the meaningful environmental question.
2. Inspect how the Runtime separates the question into climate, fire,
   drinking-water, wastewater and cross-system workstreams.
3. Confirm that the real-place path is a plan and does not manufacture a
   regional answer.
4. Use the separate fictional rehearsal to inspect explicit approval,
   deterministic execution, the Run Receipt, quarantined Evidence Passport and
   post-run human review.

### Tests

```bash
python -m unittest discover
```

The Task2002 merge record reports 321 passing tests. Test totals may increase
on later frozen submission commits and must be recorded exactly before final
submission.

## Optional Draft Task2003 page

Draft PR #89 contains an emerging persistent research-program interface at
`/program.html`. The Founder reported that the HTML opened and appeared normal.
Its evidence label is `HTML_CHECK_PASS`: it is not a completed monthly-cycle
review, a merged feature or proof of environmental validity. Judges should use
the stable Task2002 path above as the primary working demo unless the submission
snapshot later records a stronger, explicitly approved Task2003 state.

## What the demo proves

- a meaningful human question can be preserved and structured;
- real-place conclusions can remain blocked when evidence is absent;
- a fictional, local, deterministic workflow can rehearse approval, execution,
  provenance and review;
- the Build Week increment is reproducible without paid services.

## What the demo does not prove

- a current environmental condition or forecast;
- a completed long-term research program;
- scientific validity for a real place;
- professional, statutory, engineering, financial or emergency advice.

## Repository and licence

- Repository: <https://github.com/simon947161/eco-agent-system>
- Licence: MIT
- Build Week prior/new-work record: `BUILD_WEEK_CHANGELOG.md`
- ClimateOS integrity covenant:
  `docs/00_VISION/CLIMATEOS_INTEGRITY_LONG_HORIZON_AND_HUMAN_AI_COVENANT.md`

## Submission-time verification placeholders

- Frozen submission commit: `PENDING_FINAL_FREEZE`
- Public video URL: `PENDING_FOUNDER_APPROVED_PUBLIC_UPLOAD`
- Codex `/feedback` Session ID:
  `PENDING_FOUNDER_PRIMARY_THREAD_FEEDBACK`
- Public judge access verified without login: `PENDING_FINAL_CHECK`

Keep the repository and demonstration available free of charge through at
least 2026-08-07, the longer judging date stated on the OpenAI event page.
