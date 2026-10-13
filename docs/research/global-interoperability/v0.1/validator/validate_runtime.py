#!/usr/bin/env python3
"""Dependency-free bounded validator for Mission Runtime v0.1 fixtures."""
from __future__ import annotations

import copy
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALID = ROOT / "fixtures" / "valid"
INVALID = ROOT / "fixtures" / "invalid"

REQUIRED = {
    "schema_version", "mission_id", "title", "domain", "north_star", "state",
    "transition", "authority", "evidence_refs", "declared_write_set",
    "protected_write", "capability_envelope", "resume_safety",
    "interoperability", "privacy_boundary",
}
STATES = {"DRAFT", "PLANNED", "APPROVED", "EXECUTING", "VALIDATING", "PAUSED_RECOVERY", "COMPLETED", "REJECTED"}
TRANSITIONS = {
    "DRAFT": {"PLANNED", "REJECTED"},
    "PLANNED": {"APPROVED", "REJECTED"},
    "APPROVED": {"EXECUTING", "PAUSED_RECOVERY", "REJECTED"},
    "EXECUTING": {"VALIDATING", "PAUSED_RECOVERY"},
    "VALIDATING": {"COMPLETED", "EXECUTING", "PAUSED_RECOVERY", "REJECTED"},
    "PAUSED_RECOVERY": {"PLANNED", "APPROVED", "REJECTED"},
    "COMPLETED": set(), "REJECTED": set(),
}
TRANSIENT = {"EXECUTING", "VALIDATING"}
DOMAINS = {"MISSION_CONTROL", "CLIMATEOS", "CARBONOS", "BUILDINGOS", "ECOCHAIN", "GEGG"}


def validate(doc: dict) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED - set(doc))
    if missing:
        errors.append("MISSING_REQUIRED_FIELDS:" + ",".join(missing))
        return errors
    if set(doc) - REQUIRED:
        errors.append("UNDECLARED_TOP_LEVEL_FIELDS")
    if doc["schema_version"] != "mission-runtime-v0.1":
        errors.append("INVALID_SCHEMA_VERSION")
    if not re.fullmatch(r"[A-Z0-9-]{3,80}", doc["mission_id"]):
        errors.append("INVALID_MISSION_ID")
    if doc["domain"] not in DOMAINS:
        errors.append("INVALID_DOMAIN")
    if doc["north_star"] != "EVIDENCE_TRUST_GOVERNANCE_RUNTIME":
        errors.append("NORTH_STAR_MISMATCH")
    if doc["state"] not in STATES:
        errors.append("INVALID_STATE")
    transition = doc["transition"]
    if transition.get("to") != doc["state"] or transition.get("to") not in TRANSITIONS.get(transition.get("from"), set()):
        errors.append("INVALID_TRANSITION")
    authority = doc["authority"]
    if authority.get("external_action_authorized") is not False:
        errors.append("EXTERNAL_ACTION_NOT_BOUNDED")
    protected = doc["protected_write"]
    if protected.get("requested") and protected.get("approval_required") and not protected.get("approval_present"):
        errors.append("PROTECTED_WRITE_APPROVAL_MISSING")
    envelope = doc["capability_envelope"]
    if not set(envelope.get("child", [])) <= set(envelope.get("parent", [])):
        errors.append("CHILD_CAPABILITY_ESCALATION")
    resume = doc["resume_safety"]
    if resume.get("persisted_state") in TRANSIENT and resume.get("restart_state") != "PAUSED_RECOVERY":
        errors.append("UNSAFE_RESUME_STATE")
    for ref in doc["evidence_refs"]:
        if not re.fullmatch(r"[a-f0-9]{64}", ref.get("sha256", "")):
            errors.append("INVALID_EVIDENCE_HASH")
    privacy = doc["privacy_boundary"]
    if privacy.get("private_person_assets_included") is not False or privacy.get("biometric_assets_included") is not False:
        errors.append("PRIVATE_ASSET_BOUNDARY_BREACH")
    return sorted(set(errors))


def main() -> int:
    results = []
    valid_docs = {}
    for path in sorted(VALID.glob("*.json")):
        doc = json.loads(path.read_text(encoding="utf-8"))
        valid_docs[path.name] = doc
        errors = validate(doc)
        results.append({"case": path.name, "class": "valid", "passed": not errors, "errors": errors})
    for path in sorted(INVALID.glob("*.json")):
        mutation = json.loads(path.read_text(encoding="utf-8"))
        doc = copy.deepcopy(valid_docs[mutation["base_fixture"]])
        doc[mutation["mutation"]] = mutation["value"]
        errors = validate(doc)
        expected = mutation["expected_error"]
        results.append({"case": path.name, "class": "negative", "passed": expected in errors, "expected": expected, "errors": errors})
    passed = sum(1 for r in results if r["passed"])
    output = {"validator": "mission-runtime-v0.1", "total": len(results), "passed": passed, "failed": len(results)-passed, "result": "PASS" if passed == len(results) else "FAIL", "cases": results}
    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0 if output["result"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
