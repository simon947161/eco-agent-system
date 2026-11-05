"""Check local documentation, raw integrity and exact offline result replay."""
import hashlib
import json
import re
from pathlib import Path
from cczps_lite.integration.dynamic_quantification import replay


def main():
    folder = Path(__file__).resolve().parent
    evidence = folder / "evidence"
    destination = evidence / "document-validation.json"
    # The validation document links to this output; create it before link audit.
    if not destination.exists():
        destination.write_text("{}\n", encoding="utf-8")
    errors, checked = [], 0
    for md in folder.rglob("*.md"):
        for target in re.findall(r"(?<!!)\[[^\]]*\]\(([^)]+)\)", md.read_text(encoding="utf-8")):
            if "://" in target or target.startswith("#"):
                continue
            checked += 1
            if not (md.parent / target.split("#")[0]).exists():
                errors.append(f"{md.name}: {target}")
    for path in evidence.glob("*.json"):
        json.loads(path.read_text(encoding="utf-8"))
    receipt = json.loads((evidence / "noaa-receipt.json").read_text(encoding="utf-8"))
    assert hashlib.sha256((evidence / "noaa-daily.json").read_bytes()).hexdigest() == receipt["sha256"]
    assert replay() == json.loads((evidence / "actual-run.json").read_text(encoding="utf-8"))
    failures = json.loads((evidence / "negative-runs.json").read_text(encoding="utf-8"))["runs"]
    assert len(failures) == 9 and all(r["status"] == "REFUSED" and "result" not in r for r in failures.values())
    result = {"status": "FAIL" if errors else "PASS", "local_markdown_links_checked": checked,
              "broken_links": errors, "json_parse": "PASS", "raw_sha256": "PASS",
              "actual_replay_equality": "PASS", "nine_refusals_without_result": "PASS",
              "scientific_validation": "NOT_ESTABLISHED",
              "scope": "Task folder links and archived outputs only; not external link uptime."}
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))
    assert not errors


if __name__ == "__main__":
    main()
