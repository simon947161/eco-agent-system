# Task721-729 Preflight And Concurrency Hardening

## Task721 Preflight

- repository: `simon947161/eco-agent-system`;
- local path: `D:\Codex\ClimateOS\eco-agent-system-codex-working`;
- branch: `task46-repository-control-codex-batch-queue`;
- authorized baseline and aligned HEAD: `676cadfa7e77cf96df7c215e3436ef5748d3647b`;
- worktree was clean before implementation;
- Python 3.13.10 and the repository-local virtual environment were used;
- all test temporary files were directed to ignored `local_data` paths.

Preflight did not pass initially. Founder-provided evidence showed a repeatable
`sqlite3.OperationalError: database is locked` in concurrent candidate writes.
The isolated failure had repeated and was treated as a baseline blocker, not a
timing fluctuation. A pre-change full-suite attempt also exceeded its execution
window and was recorded as incomplete rather than passed.

## Tasks722-728 Inspection And Design Decision

Inspection found that SQLite used a 2000 ms busy timeout, but candidate and
audit inserts occurred in separate implicit transactions. Concurrent writers
could contend at the candidate insert, and a successful candidate insert could
be separated from its audit insert.

The bounded response is:

1. acquire the foreground write transaction explicitly with `BEGIN IMMEDIATE`;
2. retry only recognized busy/locked operational errors;
3. use a fixed finite retry schedule of 25, 50 and 100 ms after the existing
   SQLite busy timeout;
4. commit or roll back through one explicit transaction boundary;
5. insert each candidate and its matching audit event atomically;
6. serialize audit sequence allocation inside the acquired write transaction.

WAL was considered but not selected. The observed failure was writer/writer
contention, and WAL does not permit multiple simultaneous SQLite writers. A
schema or journal-mode change was therefore unsupported by the evidence.

## Task729 Bounded Concurrency Hardening

The shared database helper now provides one bounded foreground write
transaction. Candidate creation and audit insertion use that transaction.
The regression test starts four foreground writers together, creates twelve
records, and verifies exact candidate/audit identity matching, contiguous audit
sequence numbers and unique operation identifiers.

No sleep was added to the test, no assertion was weakened, and no worker,
scheduler or asynchronous queue was introduced.
