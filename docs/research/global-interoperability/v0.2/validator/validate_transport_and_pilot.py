#!/usr/bin/env python3
"""Dependency-free validator and synthetic cross-OS pilot for GGG v0.2."""
from __future__ import annotations

import copy
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUTS = ROOT / "pilot" / "inputs"
OUTPUTS = ROOT / "pilot" / "outputs"
VALIDATOR_VERSION = "ggg-transport-validator-v0.2"
SYSTEMS = {"MISSION_CONTROL", "CLIMATEOS", "CARBONOS", "BUILDINGOS", "ECOCHAIN", "GEGG"}
STATES = {"OBSERVED", "PUBLISHED_PLAN", "MODELLED", "INFERRED", "SYNTHETIC"}
REQUIRED = {"contract_version", "handoff_id", "correlation_id", "object_id", "object_type", "source_system", "target_system", "evidence_state", "synthetic", "authority", "provenance", "boundaries", "measurement", "transformations", "uncertainty", "limitations", "permitted_use", "governance", "privacy_boundary", "payload"}
ROUTES = {
    ("CLIMATEOS", "BUILDINGOS", "EvidenceObject"),
    ("BUILDINGOS", "ECOCHAIN", "DomainClaim"),
    ("ECOCHAIN", "MISSION_CONTROL", "RegistrySubmission"),
}


def canonical_bytes(doc: dict) -> bytes:
    return json.dumps(doc, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def set_path(doc: dict, dotted: str, value) -> None:
    parts = dotted.split(".")
    node = doc
    for part in parts[:-1]:
        node = node[part]
    node[parts[-1]] = value


def validate(doc: dict) -> list[str]:
    errors: list[str] = []
    missing = REQUIRED - set(doc)
    if missing:
        return ["MISSING_REQUIRED_FIELDS:" + ",".join(sorted(missing))]
    if set(doc) - REQUIRED:
        errors.append("UNDECLARED_TOP_LEVEL_FIELDS")
    if doc["contract_version"] != "ggg-transport-v0.2":
        errors.append("INVALID_CONTRACT_VERSION")
    if not re.fullmatch(r"HO-[A-Z0-9-]{3,80}", doc["handoff_id"]):
        errors.append("INVALID_HANDOFF_ID")
    if doc["source_system"] not in SYSTEMS or doc["target_system"] not in SYSTEMS:
        errors.append("INVALID_SYSTEM")
    if doc["evidence_state"] not in STATES:
        errors.append("INVALID_EVIDENCE_STATE")
    if doc.get("synthetic") is not True:
        errors.append("REAL_DATA_NOT_AUTHORIZED")
    if doc["evidence_state"] != "SYNTHETIC":
        errors.append("SYNTHETIC_STATE_NOT_PRESERVED")
    if (doc["source_system"], doc["target_system"], doc["object_type"]) not in ROUTES:
        errors.append("ROUTE_OR_OBJECT_AUTHORITY_MISMATCH")
    authority = doc["authority"]
    if authority.get("decision_authorized") is not False:
        errors.append("DECISION_AUTHORITY_NOT_BOUNDED")
    if doc["source_system"] == "ECOCHAIN" and authority.get("claim_authority") != "REGISTRY_ADAPTER_ONLY":
        errors.append("ECOCHAIN_AUTHORITY_MISMATCH")
    provenance = doc["provenance"]
    if not re.fullmatch(r"[a-f0-9]{64}", provenance.get("sha256", "")):
        errors.append("INVALID_SOURCE_HASH")
    for key in ("source_id", "publisher_or_provider", "source_version", "retrieved_at", "event_time", "upstream_object_ids"):
        if key not in provenance:
            errors.append("PROVENANCE_FIELD_MISSING:" + key)
    for key in ("spatial", "process", "time"):
        if not doc["boundaries"].get(key):
            errors.append("BOUNDARY_FIELD_MISSING:" + key)
    if not doc["limitations"] or not doc["uncertainty"]:
        errors.append("UNCERTAINTY_OR_LIMITATIONS_REMOVED")
    gov = doc["governance"]
    if not set(gov.get("child_capabilities", [])) <= set(gov.get("parent_capabilities", [])):
        errors.append("CHILD_CAPABILITY_ESCALATION")
    if gov.get("protected_write_requested") and not gov.get("protected_write_approval_present"):
        errors.append("PROTECTED_WRITE_APPROVAL_MISSING")
    if gov.get("external_action_authorized") is not False:
        errors.append("EXTERNAL_ACTION_NOT_BOUNDED")
    privacy = doc["privacy_boundary"]
    if any(privacy.get(k) is not False for k in ("private_person_assets_included", "biometric_assets_included", "personal_os_connected")):
        errors.append("PRIVATE_ASSET_BOUNDARY_BREACH")
    if doc["source_system"] == "ECOCHAIN" and doc["payload"].get("truth_status_upgraded") is not False:
        errors.append("REGISTRY_TRUTH_UPGRADE_FORBIDDEN")
    return sorted(set(errors))


def receipt(doc: dict, errors: list[str], sequence: int) -> dict:
    digest = hashlib.sha256(canonical_bytes(doc)).hexdigest()
    return {
        "receipt_version": "ggg-receipt-v0.2",
        "receipt_id": f"RCP-GGG-PILOT-001-{sequence:03d}",
        "handoff_id": doc["handoff_id"],
        "correlation_id": doc["correlation_id"],
        "receiver": doc["target_system"],
        "status": "REJECTED" if errors else "ACCEPTED",
        "received_at": f"2026-08-01T00:00:0{sequence}Z",
        "envelope_sha256": digest,
        "validator_version": VALIDATOR_VERSION,
        "evidence_state_preserved": "SYNTHETIC_STATE_NOT_PRESERVED" not in errors,
        "authority_preserved": not any(e in errors for e in ("ROUTE_OR_OBJECT_AUTHORITY_MISMATCH", "ECOCHAIN_AUTHORITY_MISMATCH", "DECISION_AUTHORITY_NOT_BOUNDED", "REGISTRY_TRUTH_UPGRADE_FORBIDDEN")),
        "external_action": False,
        "mainline_write": False,
        "reasons": errors,
    }


def main() -> int:
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    docs: dict[str, dict] = {}
    receipts = []
    cases = []
    previous_object_ids: set[str] = set()
    for sequence, path in enumerate(sorted(INPUTS.glob("*.json")), 1):
        doc = json.loads(path.read_text(encoding="utf-8"))
        docs[path.name] = doc
        errors = validate(doc)
        upstream = set(doc["provenance"]["upstream_object_ids"])
        if sequence > 1 and not upstream & previous_object_ids:
            errors.append("UPSTREAM_LINEAGE_MISSING")
        previous_object_ids.add(doc["object_id"])
        rcp = receipt(doc, sorted(set(errors)), sequence)
        receipts.append(rcp)
        cases.append({"case": path.name, "class": "pilot_handoff", "passed": not errors, "errors": sorted(set(errors))})
        (OUTPUTS / f"{sequence:02d}_receipt.json").write_text(json.dumps(rcp, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    mutations = json.loads((ROOT / "pilot" / "negative_mutations.json").read_text(encoding="utf-8"))
    for mutation in mutations:
        doc = copy.deepcopy(docs[mutation["base"]])
        set_path(doc, mutation["path"], mutation["value"])
        errors = validate(doc)
        cases.append({"case": mutation["case"], "class": "negative", "passed": mutation["expected"] in errors, "expected": mutation["expected"], "errors": errors})

    accepted = all(r["status"] == "ACCEPTED" for r in receipts)
    lineage = receipts[0]["correlation_id"] == receipts[1]["correlation_id"] == receipts[2]["correlation_id"]
    states = all(json.loads(p.read_text(encoding="utf-8"))["evidence_state"] == "SYNTHETIC" for p in sorted(INPUTS.glob("*.json")))
    passed = sum(1 for c in cases if c["passed"])
    report = {
        "pilot": "GGG synthetic cross-OS handoff pilot v0.2",
        "route": ["CLIMATEOS", "BUILDINGOS", "ECOCHAIN", "MISSION_CONTROL"],
        "validator": VALIDATOR_VERSION,
        "handoffs_accepted": f"{sum(r['status'] == 'ACCEPTED' for r in receipts)}/3",
        "correlation_lineage_preserved": lineage,
        "synthetic_state_preserved": states,
        "external_action": False,
        "mainline_write": False,
        "real_data": False,
        "private_person_or_biometric_assets": False,
        "total_cases": len(cases),
        "passed": passed,
        "failed": len(cases) - passed,
        "result": "PASS" if accepted and lineage and states and passed == len(cases) else "FAIL",
        "receipts": receipts,
        "cases": cases,
    }
    (OUTPUTS / "PILOT_EXECUTION_RESULT_v0.2.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["result"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
