"""Offline checks for Issue164 authored metadata only; never import a model or fetch data."""
import copy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE = "9aea387a4261b913163b3be3197597089d9e9414"
PREFIX = "docs/tasks/climateos_awt_001/p4/"
DATE = "2026-11-24"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True).strip()


def check_register(register, sources):
    require(register["assessment_date"] == DATE, "ASSESSMENT_DATE")
    require(register["mode"] == "READ_ONLY", "MODE")
    require(register["raw_data_status"] == "NO_RAW_DATA_DOWNLOADED", "RAW_SCOPE")
    require(register["frozen_baseline"] == BASE, "BASELINE")
    require(register["scientific_admission"] == "PENDING", "SCIENCE_GATE")
    require(register["real_data_status"] == "DATA_NOT_READY", "DATA_GATE")
    require(register["credit_eligibility"] == "NOT_DETERMINED", "CREDIT_GATE")
    candidates = register["candidates"]
    require(0 < len(candidates) <= 6, "CANDIDATE_CAP")
    require(len({c["id"] for c in candidates}) == len(candidates), "DUPLICATE_CANDIDATE")
    detailed = sum(c["assessment_depth"] == "DETAILED" for c in candidates)
    require(detailed <= 3, "DETAILED_CAP")
    require(register["discovered_count"] == len(candidates), "COUNT_MISMATCH")
    require(register["detailed_count"] == detailed, "DETAIL_COUNT_MISMATCH")
    approved = []
    allowed = {"DIRECT_MEASURED", "CALCULATED", "REPORTED", "MISSING", "UNKNOWN"}
    for c in candidates:
        require(c["source_ids"] and set(c["source_ids"]) <= sources, "SOURCE_REF")
        require(c["assessment_date"] == DATE and c["mode"] == "READ_ONLY", "CANDIDATE_MODE")
        require(c["raw_data_status"] == "NO_RAW_DATA_DOWNLOADED", "CANDIDATE_RAW_SCOPE")
        require(not c["admitted"] and not c["raw_access_tested"], "UNSUPPORTED_ADMISSION")
        require(c["raw_file_sha256"] is None and c["actual_rows"] is None
                and c["actual_missing_fraction"] is None, "FALSE_RAW_EVIDENCE")
        require(c["status"] in {"CANDIDATE_FOR_FOUNDER_APPROVAL", "PARTIAL_METHOD_ONLY",
                               "BLOCKED", "NO_SUITABLE_DATASET"}, "INVALID_STATUS")
        require(set(c["gates"]) == {f"G{i}" for i in range(1, 8)}, "GATE_COVERAGE")
        for g in c["gates"].values():
            require(g["reason"] and g["source_ids"] and set(g["source_ids"]) <= sources,
                    "GATE_EVIDENCE")
        for _, classification in c["field_evidence"]:
            require(classification in allowed, "FIELD_CLASS")
        for f in c["expected_files"]:
            require(not f["downloaded"] and f["sha256"] is None
                    and f["request_status"] == "NOT_REQUESTED", "RAW_FILE_CLAIM")
            require(f["download_url"] is None or f["download_url"].startswith("https://"),
                    "FILE_URL")
        if c["licence"]["status"] == "LICENCE_UNVERIFIED":
            require(c["status"] == "BLOCKED", "UNVERIFIED_LICENCE_ADMISSION")
        if c["status"] == "CANDIDATE_FOR_FOUNDER_APPROVAL":
            require(c["full_chain_suitable"]
                    and all(g["status"] == "SUPPORTED_METADATA" for g in c["gates"].values()),
                    "INCOMPLETE_CHAIN_APPROVAL")
            approved.append(c["id"])
    if register["decision"] == "NO_SUITABLE_DATASET":
        require(not approved and all(not c["full_chain_suitable"] for c in candidates),
                "STOP_CONTRADICTION")
    return len(candidates), detailed


def main():
    register = read_json(HERE / "candidate_register.json")
    source_doc = read_json(HERE / "source_register.json")
    sources = {s["id"] for s in source_doc["sources"]}
    require(len(sources) == len(source_doc["sources"]), "DUPLICATE_SOURCE")
    for source in source_doc["sources"]:
        require(source["url"].startswith("https://") and source["locator"] and source["note"],
                "SOURCE_METADATA")
        require(source["raw_file_sha256"] is None, "SOURCE_RAW_HASH")
    candidates, detailed = check_register(register, sources)
    schema = read_json(HERE.parent / "CLAIM_PASSPORT_SCHEMA.json")
    entity_types = schema["properties"]["entities"]["items"]["properties"]["type"]["enum"]
    mapping = (HERE / "FIELD_TIME_QC_MAPPING.md").read_text(encoding="utf-8")
    require(len(entity_types) == 9 and all(t in mapping for t in entity_types), "PASSPORT_COVERAGE")

    # Guard checks mutate only authored metadata in memory, not environmental values.
    negatives = [
        ("candidate cap", lambda x: x["candidates"].extend(copy.deepcopy(x["candidates"]))),
        ("science gate", lambda x: x.update(scientific_admission="APPROVED")),
        ("false raw hash", lambda x: x["candidates"][3].update(raw_file_sha256="0" * 64)),
        ("unresolved source", lambda x: x["candidates"][3].update(source_ids=["NONEXISTENT"])),
        ("incomplete approval", lambda x: x["candidates"][3].update(
            status="CANDIDATE_FOR_FOUNDER_APPROVAL", full_chain_suitable=True)),
    ]
    negative_results = []
    for name, mutate in negatives:
        bad = copy.deepcopy(register)
        mutate(bad)
        try:
            check_register(bad, sources)
        except ValueError as error:
            negative_results.append({"case": name, "result": "REJECTED", "reason": str(error)})
        else:
            raise ValueError("NEGATIVE_GUARD_NOT_REJECTED:" + name)

    local_links = 0
    markdown_count = 0
    for path in HERE.glob("*.md"):
        body = path.read_text(encoding="utf-8")
        require(all(x in body for x in (DATE, "READ_ONLY", "NO_RAW_DATA_DOWNLOADED")),
                "REPORT_BOUNDARY:" + path.name)
        require("https://" in body, "REPORT_SOURCE:" + path.name)
        markdown_count += 1
        for link in re.findall(r"\]\(([^)]+)\)", body):
            if link.startswith(("http:", "https:", "#", "mailto:")):
                continue
            target = (path.parent / link.split("#")[0]).resolve()
            require(target.is_file(), "BROKEN_LOCAL_LINK:" + link)
            require(target.is_relative_to(ROOT), "OUTSIDE_REPO_LINK")
            local_links += 1

    parent_manifest = read_json(HERE.parent / "manifest.json")
    frozen_count = 0
    for rel, expected in parent_manifest["files"].items():
        path = ROOT / rel
        payload = path.read_bytes()
        if path.suffix != ".png":
            payload = payload.replace(b"\r\n", b"\n")
        require(hashlib.sha256(payload).hexdigest() == expected, "FROZEN_HASH_CHANGED:" + rel)
        frozen_count += 1
    reuse = read_json(HERE.parent / "evidence/reuse-hashes.json")["files"]
    for rel, expected in reuse.items():
        data = (ROOT / rel).read_bytes().replace(b"\r\n", b"\n")
        require(hashlib.sha256(data).hexdigest() == expected, "REUSE_HASH_CHANGED:" + rel)

    changed = git("diff", "--name-only", BASE).splitlines()
    untracked = git("ls-files", "--others", "--exclude-standard").splitlines()
    require(all(x.startswith(PREFIX) for x in changed + untracked), "OUT_OF_SCOPE_CHANGE")
    require(git("merge-base", BASE, "HEAD") == BASE, "WRONG_ANCESTRY")
    allowed_suffixes = {".md", ".json", ".py"}
    patterns = [r"gh[pousr]_[A-Za-z0-9]{20,}", r"github_pat_[A-Za-z0-9_]{20,}",
                r"AKIA[0-9A-Z]{16}", r"-----BEGIN [A-Z ]*PRIVATE KEY-----"]
    file_count = 0
    for path in HERE.rglob("*"):
        if path.is_file():
            require(path.suffix in allowed_suffixes, "UNEXPECTED_FILE_TYPE:" + path.name)
            body = path.read_text(encoding="utf-8")
            require(not any(re.search(p, body) for p in patterns), "SENSITIVE_EXPORT:" + path.name)
            if path.suffix == ".json":
                json.loads(body)
            file_count += 1

    print(json.dumps({
        "assessment_date": DATE,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "mode": "READ_ONLY",
        "raw_data_status": "NO_RAW_DATA_DOWNLOADED",
        "status": "PASS_METADATA_PACKAGE_ONLY",
        "checkout_head_at_check": git("rev-parse", "HEAD"),
        "frozen_baseline": BASE,
        "candidate_count": candidates, "detailed_count": detailed,
        "passport_entity_types_mapped": len(entity_types),
        "source_records": len(sources), "markdown_reports": markdown_count,
        "local_links_checked": local_links, "p4_files_checked": file_count,
        "frozen_manifest_entries_checked": frozen_count,
        "inherited_component_hashes_checked": len(reuse),
        "changed_tracked_paths": len(changed), "untracked_paths": len(untracked),
        "only_p4_changes": True, "sensitive_patterns": "NO_MATCH",
        "negative_metadata_guards": negative_results,
        "numerical_model_runs": 0,
        "raw_file_checks": "NOT_PERFORMED_NOT_AUTHORIZED",
        "decision": register["decision"],
        "science": "PENDING", "real_data": "DATA_NOT_READY", "credit": "NOT_DETERMINED",
        "ci": "REMOTE_STATUS_REPORTED_SEPARATELY_NOT_CLAIMED_PASS",
        "limitations": "Hashes cover frozen authored files, not raw data or scientific truth."
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
