# EP-SKILL-001 Cooma Site Reading

The committed R1 fixture is immutable and can be verified without changing tracked files:

```powershell
python run_cooma_site_reading.py --verify-fixture
```

To run a new request, copy the request fixture, assign an explicit unique `request_id` and `revision_id`, set its lineage fields, then run:

```powershell
python run_cooma_site_reading.py --request <new-request.json> --output-root runtime_data/site_readings
```

New runs default to the untracked `runtime_data/site_readings` artifact root. Each revision is written under `runs/<revision_id>/`. The run receipt declares `artifact_root`, and its output paths are POSIX-normalised paths relative to that root.

An existing revision directory is refused rather than overwritten. Use a new, caller-supplied revision identity when evidence, method, scope or review state changes. The CLI never invents an identity.

The skill remains bounded to A0 evidence requests, monitoring preparation, record preservation and review preparation. It does not authorise current-flow or trend conclusions, professional sign-off, engineering, regulatory, procurement or public-warning action.
