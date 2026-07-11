# Task901-920 Founder Human Test Kit

Status: Prepared; waiting for Shu Min's daytime test.

## Start

Open PowerShell:

```powershell
cd D:\Codex\ClimateOS\eco-agent-system-codex-working
git switch task46-repository-control-codex-batch-queue
git pull --ff-only origin task46-repository-control-codex-batch-queue
cd prototype\climateos-local-controlled-prototype-core
.\.venv\Scripts\Activate.ps1
uvicorn climateos_local_prototype.main:app --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000` in Chrome and select **Alpha Review**.

## Test Task

Without reading code or asking Codex what to click:

1. create a fictional biodiversity evidence candidate;
2. explain its uncertainty in the form;
3. challenge/dispute it;
4. find the updated record and audit evidence;
5. refresh the page;
6. stop and restart the local server and check that the record survives;
7. say aloud what the system has and has not proved.

## Record Sheet

For every step record one status: `PASS`, `CONFUSED`, `FAILED`, or
`NEEDED_HELP`.

| Step | Status | What happened in ordinary words | Time or help needed |
| --- | --- | --- | --- |
| Find Alpha Review |  |  |  |
| Understand warnings |  |  |  |
| Create synthetic evidence |  |  |  |
| Record uncertainty |  |  |  |
| Dispute evidence |  |  |  |
| Find audit history |  |  |  |
| Refresh and recover |  |  |  |
| Explain what is not proved |  |  |  |

## Three Safety Questions

Answer in your own words:

1. Did you ever think the system had approved the evidence as true?
2. Did you understand that the reviewer name was only a typed label?
3. Would you feel safe showing this record to another person without extra
   explanation?

Do not change a `CONFUSED` or `FAILED` result to `PASS`. Confusion is useful
design evidence.
