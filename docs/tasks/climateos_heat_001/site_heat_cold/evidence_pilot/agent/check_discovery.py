"""Exercise the offline chain and the live code path with both transports replaced."""
import json
import os
import tempfile
import time
from pathlib import Path
from unittest.mock import patch

from discover import MODEL, reserve, run

job = json.loads(Path(__file__).with_name("example_job.json").read_bytes())


def must_stop(fn, exception=ValueError):
    try:
        fn()
    except exception:
        return
    raise AssertionError("expected controlled failure")


def transport(url, data=None, headers=None):
    if url.startswith("https://zenodo.org/api/records?"):
        return {"hits": {"hits": [{"metadata": {"title": "SYNTHETIC", "doi": "10.5281/zenodo.1"}}]}}
    assert url == "https://api.openai.com/v1/responses"
    assert headers["OpenAI-Project"] == "fixture"
    request = json.loads(data)
    assert request["store"] is False and request["model"] == MODEL and "tools" not in request
    return {"model": MODEL, "status": "completed", "id": "mock",
            "usage": {"input_tokens": 1, "output_tokens": 2},
            "output": [{"type": "message", "content": [
                {"type": "output_text", "text": '{"action":"select","index":0}'}]}]}


with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {
    "OPENAI_PROJECT_ID": "fixture", "OPENAI_API_KEY": "fixture"
}):
    root = Path(tmp)
    with patch("discover.read_json", side_effect=AssertionError("unexpected network call")):
        receipt = run(job, False, root)
        assert receipt["mode"] == "offline_fixture" and receipt["reserved_micro_usd"] == 0
        assert receipt == run(job, False, root)
        must_stop(lambda: run(dict(job, max_model_calls=1), False, root))
        must_stop(lambda: run(job, True, root))
    live = dict(job, job_id="mock", rates_verified_today_utc=time.strftime("%Y-%m-%d", time.gmtime()),
                input_rate_micro_usd_per_million=450000, output_rate_micro_usd_per_million=1800000)
    with patch("discover.read_json", side_effect=transport) as http:
        must_stop(lambda: run(live, True, root))
        assert http.call_count == 0
        live["budget_micro_usd"] = reserve(live)
        receipt = run(live, True, root)
        assert receipt["selected"]["doi"] == "10.5281/zenodo.1"
        assert receipt["reserved_micro_usd"] == reserve(live)
        run(live, True, root)
        assert http.call_count == 2
    with patch("discover.candidates", return_value=[]), patch("discover.select_live", side_effect=TimeoutError) as model:
        live["job_id"] = "timeout"
        must_stop(lambda: run(live, True, root), TimeoutError)
        must_stop(lambda: run(live, True, root))
        assert model.call_count == 1
        assert json.loads((root / "timeout" / "receipt.json").read_text())["reserved_micro_usd"] == reserve(live)
print("PASS offline two-step, replay, input collision, zero-budget block, mocked live routing, timeout reservation and duplicate blocking")
