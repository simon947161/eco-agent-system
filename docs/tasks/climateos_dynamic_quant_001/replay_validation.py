"""Explicit offline artifact writer: run from repository root using python -m.

No acquisition, scheduling, database, LLM, or deployment side effects.
"""
import json
from cczps_lite.integration import dynamic_quantification as dq


def main():
    path = dq.EVIDENCE_DIR
    request = json.loads((path / "request.json").read_text(encoding="utf-8"))
    raw = (path / "noaa-daily.json").read_bytes()
    receipt = json.loads((path / "noaa-receipt.json").read_text(encoding="utf-8"))
    output = dq.run_agent(request, raw, receipt)
    (path / "actual-run.json").write_text(json.dumps(output, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    if "report_zh" in output:
        (path / "ACTUAL_OBSERVATION_REPORT_ZH.md").write_text(output["report_zh"], encoding="utf-8")
    changes = {
        "incompatible_unit": {"variables": {"daily_max_temperature": "K"}},
        "wrong_space": {"coordinates": [148.15, -35.52]},
        "wrong_time": {"start_date": "2025-05-10"},
        "unverified_time_basis": {"time_basis": "UTC"},
        "unauthorized_model": {"model_id": "methane_inversion"},
        "insufficient_evidence": {"end_date": "2025-05-02"},
        "methane_not_ready": {"source_id": "methane_d3"},
    }
    failures = {name: dq.run_agent({**request, **change}, raw, receipt) for name, change in changes.items()}
    failures["missing_data"] = dq.run_agent(request)
    failures["tampered_bytes"] = dq.run_agent(request, raw + b" ", receipt)
    (path / "negative-runs.json").write_text(json.dumps({"evidence_class": "REAL_RAW_REPLAY_WITH_MUTATED_REQUESTS_NOT_ENVIRONMENTAL_EXPERIMENT", "runs": failures}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output["status"])
    print("Negative paths:", len(failures), "all refused:", all(r["status"] == "REFUSED" for r in failures.values()))


if __name__ == "__main__":
    main()
