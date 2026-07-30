# Unfinished PR Disposition Register

Review date: 2026-07-30  
No disposition in this register has been executed.

| PR | Exact review state | Classification | Finding | Recommendation |
|---|---|---|---|---|
| #109 | open Draft, mergeable, exact Head `3aeea740`, 1 file, 0 behind/1 ahead | `SUPPORTING_INFRASTRUCTURE` | valid ACTP and provenance packet | keep open during Founder review; merge or close only after the v2 package provenance decision |
| #108 | open Draft, mergeable, Head `5813f4c`, 1 behind/2 ahead main, 7 files | `SCIENTIFIC_FOUNDATION` / `V2_CORE` | exact-head tests passed 451; bounded official historical flow intake; not an assessment | revise onto current main or confirm clean controlled merge, then Founder-authorised merge before first assessment |
| #104 | open Draft, mergeable, Head `a856018`, 15 behind/16 ahead main, 16 files | `SUPPORTING_INFRASTRUCTURE` / `ROUTE_TO_OTHER_PROJECT` | useful mission schemas and fixtures; cross-system rather than Cooma science | route to Mission Control; narrow shared contracts; do not make it a Phase II prerequisite |
| #102 | open Draft, mergeable, Head `fdbb4a9`, 15 behind/1 ahead main, 1 file | `DUPLICATE_OR_SUPERSEDED` | post-merge ACTP for already accepted PR #101; operational handoff has passed | preserve history, then close/archive after Founder approval |
| #100 | open Draft, mergeable, Head `79705d8`, 45 behind/3 ahead main, 3 files | `SCIENTIFIC_FOUNDATION` | useful earth-system ontology and driver registry; currently static | revise/rebase and connect objects to convergence and local translation before merge |
| #90 | open Draft, mergeable, Head `3a1485b`, 60 behind/36 ahead main, 16 files | `DEMO_ONLY` | Build Week and integrity materials; not core science | preserve integrity covenant separately; archive or close stale submission material after Founder approval |
| #61 | open Draft, mergeable, Head `e15e5a7`, 226 behind/332 ahead main, 8 files relative to declared base | `SCIENTIFIC_FOUNDATION` / `CLOSE_OR_ARCHIVE_CANDIDATE` | external-model observation ideas remain useful, but branch lineage is obsolete and merging would import massive historical divergence | extract still-missing concepts into a fresh main-based change; archive old PR |
| #50 | open Draft, mergeable, Head `8bcde33`, 226 behind/224 ahead main, 1 file relative to declared base | `DUPLICATE_OR_SUPERSEDED` | hybrid-weather preflight preceded later mainline source registry and orchestration work | confirm unique policy clauses are preserved, then archive old PR |

## Queue rule

`mergeable=true` means GitHub can currently compute a merge. It does not mean
the content is current, desirable or safe to merge.

## Recommended order

1. decide v2 architecture;
2. update and decide #108;
3. route #104 to Mission Control;
4. revise #100 into an operational tree-to-leaf foundation;
5. preserve unique content from #90, #61 and #50;
6. close/archive superseded PRs only under explicit Founder authorization;
7. keep #102 until its provenance value is confirmed.

