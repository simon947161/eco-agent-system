# Queue Rules

1. One primary task per Codex session.
2. Do not combine unrelated tasks.
3. Complete repository-control tasks before subsystem expansion.
4. Review outputs before advancing dependencies.
5. Update queue status after task completion.
6. Prefer small incremental changes.
7. Avoid repository-wide refactors unless explicitly approved.
8. Preserve backward compatibility.
9. Do not skip acceptance criteria.
10. Record completion summaries.

## Operating Guidance

- A task may move to `Ready` only when its purpose, scope, files, acceptance
  criteria, prohibited changes, and tests are clear.
- `In Progress` means active implementation, not completion.
- `Review` means implementation exists but still requires repository-owner
  review.
- `Completed` requires acceptance criteria, tests, review, and a completion-log
  entry.
- `Blocked` must include the blocking condition and the evidence needed to
  resume.

## Emergency Stop Rules

Stop the current task and inspect the repository when any of these occur:

- failing tests;
- unexpected deletions;
- large-scale file modifications;
- architectural conflicts;
- dependency explosions;
- unrelated runtime, evidence, validation, GIS, dashboard, or API changes;
- uncertainty about whether existing user work would be overwritten.

Do not hide or work around an emergency-stop condition. Record it in
`QUEUE_STATUS.md` and return the task to review or blocked status.
