# Task901-960 Founder Human Test Evidence

Date: 2026-07-12

Tester: Shu Min, using the declared label `Shu Min - Founder Test`

Environment: Windows, Chrome, localhost-only ClimateOS Alpha

## Result

Decision: `PASS_WITH_GUIDANCE`

The Founder completed the core synthetic evidence workflow:

1. opened the local prototype;
2. explored the existing candidate, review, gate, model bridge, archive and
   audit areas;
3. created `Synthetic Tumut Bee Observation` in the biodiversity domain;
4. received Evidence ID `ALPHA-EVIDENCE-206db17f7755`;
5. recorded uncertainty and disputed the candidate using the declared local
   reviewer label;
6. located sequential create and dispute audit events;
7. refreshed the browser and recovered evidence state, revision and history;
8. stopped and restarted the service and recovered the SQLite-backed record;
9. completed keyboard-only navigation and Chrome 200% zoom checks;
10. understood that the record did not prove a real bee decline, verify the
    reviewer's identity or support external environmental conclusions.

## Passed Evidence

- candidate creation;
- Human Review dispute;
- candidate-to-disputed state transition;
- revision 1 preserved after revision 2;
- sequential audit history;
- browser refresh persistence;
- service restart persistence;
- keyboard navigation;
- visible focus and menu activation;
- 200% zoom readability and continued operation;
- no-conclusion and declared-label boundary comprehension.

## Human-Test Findings

| ID | Result | Finding |
| --- | --- | --- |
| HUT-001 | Failed instruction | Test kit referenced nonexistent `climateos_local_prototype.main`; correct entry is `scripts/run_local_service.py`. |
| HUT-002 | Needed help | The landing page did not tell a new user what to do first. |
| HUT-003 | Confused | Browser translation rendered Candidate as a person-like “候选人” rather than a candidate record. |
| HUT-004 | Confused | Founder Gate, Model Bridge and Archive Export lacked plain-language purpose descriptions. |
| HUT-005 | Future requirement | Local/project/organisation nodes, spatial IDs, GIS coordinates and map boundaries are required for future real use. |
| HUT-006 | Pass | Synthetic evidence creation succeeded and candidate-only meaning was broadly understood. |
| HUT-007 | Pass | Dispute action succeeded and retained human responsibility without issuing a conclusion. |
| HUT-008 | Pass | The Founder found and understood the create/dispute audit chain. |
| HUT-009 | Gap | Creation audit used generic `human_submitter`; declared submitter and verified identity remain distinct future needs. |
| HUT-010 | Gap | UTC timestamps were accurate but not presented in local human-readable time. |
| HUT-011 | Pass | Evidence, disputed state and revision history survived browser refresh. |
| HUT-012 | Needs improvement | Evidence and audit are primarily raw JSON rather than readable cards and timelines. |
| HUT-013 | Pass | Evidence and audit survived service restart. |
| HUT-014 | Needed help | PowerShell start/stop required guidance and is unsuitable for ordinary NGO users. |

## Emerging Evidence Growth Requirements

Future evidence intake should distinguish casual, structured, professional and
validated observations. Real observations may progressively add observer,
time, location, spatial boundary, method, duration, species identification,
count, attachments, permissions and uncertainty without requiring an ordinary
community observer to complete a professional survey form.

## Accessibility Boundary

Keyboard and 200% zoom checks passed in the Founder session. Windows Narrator
and an independent assistive-technology participant were not tested and are not
reported as passed.
