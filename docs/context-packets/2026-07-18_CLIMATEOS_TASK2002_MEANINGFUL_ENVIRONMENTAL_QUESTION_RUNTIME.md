# ClimateOS Task2002 — Meaningful Environmental Question Runtime

Date: 2026-07-18  
Status: COMPLETED / FOUNDER REVIEWED / PR #88 MERGED
Founder direction: stop polishing the scalar-box demonstration and advance to a Runtime that can receive the meaningful Cooma water, snow, bushfire, drinking-water and wastewater question.

## Capability milestone

Task2002 adds one bounded vertical slice. It must:

1. accept the Founder's real question in the Founder's own words;
2. structure it into climate outlook, bushfire risk, drinking-water security, wastewater resilience and cross-system integration workstreams;
3. label the real-place path `REAL_WORLD_PLAN_ONLY` and refuse to execute or manufacture a real Cooma conclusion without current authoritative evidence and separate approvals;
4. translate the research structure into a repository-authored fictional Australian highland-town rehearsal;
5. require explicit human approval before local execution;
6. produce deterministic synthetic results, a Run Receipt, an Evidence Passport and a post-run human review decision.

## Fixed boundaries

- Real Cooma, ENSO, bushfire, drinking-water or wastewater findings are not produced by this task.
- The real-place plan identifies evidence needed; it does not fetch it.
- The executable fixture is fictional, tiny-synthetic, local, zero-cost and network-free.
- Synthetic results remain quarantined and cannot support an environmental, operational or policy decision.
- GraphCast remains LATER.
- No Bondo or Riverina wind-resource or project-feasibility conclusion.
- Constellation Journey and WorkOS private material remain isolated.

## Human meaning

The old Runtime tested the control mechanism. This Runtime tests whether the same supervised mechanism can preserve a person's meaningful environmental question, show what would be needed to answer it responsibly, and rehearse the full research workflow without pretending that synthetic values are real evidence.

## Stop condition

Publish as a Draft milestone PR with a clear local test entry. Do not start real Cooma evidence acquisition or Task2003+ automatically.

## Local entry

```bash
python run_environmental_question_runtime.py
```

Open `http://127.0.0.1:8766`. Port 8765 remains the frozen scalar control
demonstration and is not the Task2002 entry.

## Validation record

- 2026-07-18: `python -m unittest discover`
- Result: 321 tests passed.
- Local smoke check: health endpoint returned `real_execution=blocked`,
  `synthetic_execution=local_only`, `network_egress=false`, and `cost_aud=0`.
- Browser entry served the meaningful-question page on port 8766.
- Founder tested the meaningful-question flow and directed the next upgrade to
  a persistent monthly research program.
- PR #88 merged on 2026-07-18 at
  `c9c16a917c9469b38c204a1726f9497daa3a73b5`.
