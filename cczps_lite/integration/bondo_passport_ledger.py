"""Dependency-free validator and local manual ledger for a static Bondo passport.

The prototype reads repository-authored JSON only.  It contains no HTTP client,
scheduler, scraper, notification sender, scientific scoring, or data download.
Ledger events must explicitly preserve those boundaries.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any

SCHEMA_ID = "climateos.bondo.evidence_passport.v0.1"
CONTROLLED_STATES = {
    "ADMITTED_IDENTITY", "ADMITTED_ATTRIBUTED_STATEMENT", "CONTEXT_ONLY",
    "VERSION_CONFLICT", "MISSING_EVIDENCE", "REJECTED_INFERENCE",
    "PROHIBITED_CONCLUSION", "HUMAN_REVIEW_REQUIRED",
}
EVENT_CLASSES = {
    "NO_CHANGE", "NON_MATERIAL_CHANGE", "MATERIAL_METADATA_CHANGE",
    "MATERIAL_SPATIAL_CHANGE", "MATERIAL_SCIENTIFIC_CHANGE",
    "MATERIAL_LICENCE_CHANGE", "SOURCE_WITHDRAWAL", "AUTHORITY_CONFLICT",
}
EVENT_ORIGINS = {"FICTIONAL_MANUAL", "REPOSITORY_STATIC_MANUAL"}
REVIEW_CLASSES = EVENT_CLASSES - {"NO_CHANGE", "NON_MATERIAL_CHANGE"}
EVENT_FIELDS = {
    "event_id", "observed_at", "event_origin", "classification", "summary",
    "affected_claim_ids", "affected_evidence_ids", "re_review_required",
    "source_access_performed", "real_data_acquired", "external_contact",
    "notification_sent", "scientific_conclusion_formed",
}
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "input"


class PassportContractError(ValueError):
    """Raised when a passport or ledger event crosses the bounded contract."""


def _strict_keys(value: Any, required: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise PassportContractError(f"{label} must be an object")
    missing, unknown = required - set(value), set(value) - required
    if missing or unknown:
        raise PassportContractError(f"{label} fields invalid; missing={sorted(missing)}, unknown={sorted(unknown)}")
    return value


def _ids(items: Any, prefix: str, label: str) -> set[str]:
    if not isinstance(items, list):
        raise PassportContractError(f"{label} must be a list")
    ids: list[str] = []
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get(prefix), str):
            raise PassportContractError(f"{label} entries require {prefix}")
        ids.append(item[prefix])
    if len(ids) != len(set(ids)):
        raise PassportContractError(f"{label} IDs must be unique")
    return set(ids)


def load_static_passport(path: str | Path) -> dict[str, Any]:
    """Load a JSON fixture only from the repository input directory."""
    fixture = Path(path).resolve()
    try:
        fixture.relative_to(FIXTURE_ROOT.resolve())
    except ValueError as exc:
        raise PassportContractError("Passport fixtures must stay under cczps_lite/input") from exc
    with fixture.open("r", encoding="utf-8") as stream:
        value = json.load(stream)
    validate_passport(value)
    return value


def validate_passport(value: Any) -> None:
    """Validate safety-critical v0.1 structure and cross-references."""
    passport = _strict_keys(value, {"schema_id", "passport", "evidence", "claims", "version_conflicts", "gaps"}, "root")
    if passport["schema_id"] != SCHEMA_ID:
        raise PassportContractError("Unsupported schema_id")
    header_fields = {
        "passport_id", "subject", "project_identities", "evidence_cutoff", "steward",
        "raw_data_included", "machine_readable_gis_included", "models_or_weights_included",
        "external_account_or_paid_source", "human_scientific_approval", "permitted_uses", "prohibited_uses",
    }
    header = _strict_keys(passport["passport"], header_fields, "passport")
    blocked_flags = ("raw_data_included", "machine_readable_gis_included", "models_or_weights_included", "external_account_or_paid_source")
    if any(header[name] is not False for name in blocked_flags):
        raise PassportContractError("Raw data, GIS, model/weights, accounts, or paid sources are blocked")
    if header["human_scientific_approval"] != "NONE":
        raise PassportContractError("v0.1 cannot record scientific approval")
    if not header["prohibited_uses"]:
        raise PassportContractError("prohibited_uses must be retained")
    try:
        datetime.fromisoformat(header["evidence_cutoff"])
    except (TypeError, ValueError) as exc:
        raise PassportContractError("evidence_cutoff must be an ISO date") from exc

    evidence_ids = _ids(passport["evidence"], "evidence_id", "evidence")
    gap_ids = _ids(passport["gaps"], "gap_id", "gaps")
    claim_ids = _ids(passport["claims"], "claim_id", "claims")
    for claim in passport["claims"]:
        states = claim.get("controlled_states")
        if not isinstance(states, list) or not states or not set(states) <= CONTROLLED_STATES:
            raise PassportContractError(f"{claim['claim_id']} has invalid controlled_states")
        if not isinstance(claim.get("readable_state"), str) or not claim["readable_state"].strip():
            raise PassportContractError(f"{claim['claim_id']} must preserve readable_state")
        refs = set(claim.get("supporting_evidence_ids", [])) | set(claim.get("contradicting_evidence_ids", []))
        if not refs <= evidence_ids or not set(claim.get("gap_ids", [])) <= gap_ids:
            raise PassportContractError(f"{claim['claim_id']} contains unresolved references")
        if "PROHIBITED_CONCLUSION" in states and claim.get("human_review_required") is not True:
            raise PassportContractError("Prohibited conclusions must retain human_review_required")
    for conflict in passport["version_conflicts"]:
        if not set(conflict.get("node_ids", [])) <= claim_ids | evidence_ids:
            raise PassportContractError("version_conflict contains unresolved node IDs")


def _utc(value: Any) -> None:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise PassportContractError("observed_at must be an ISO-8601 UTC string")
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise PassportContractError("observed_at must be valid ISO-8601") from exc


def validate_event(event: Any) -> None:
    record = _strict_keys(event, EVENT_FIELDS, "event")
    _utc(record["observed_at"])
    if record["event_origin"] not in EVENT_ORIGINS:
        raise PassportContractError("Only fictional or repository-static manual events are allowed")
    if record["classification"] not in EVENT_CLASSES:
        raise PassportContractError("Unsupported event classification")
    if record["re_review_required"] != (record["classification"] in REVIEW_CLASSES):
        raise PassportContractError("re_review_required does not match classification")
    for field in ("affected_claim_ids", "affected_evidence_ids"):
        if not isinstance(record[field], list) or any(not isinstance(item, str) for item in record[field]):
            raise PassportContractError(f"{field} must be a string list")
    boundaries = ("source_access_performed", "real_data_acquired", "external_contact", "notification_sent", "scientific_conclusion_formed")
    if any(record[field] is not False for field in boundaries):
        raise PassportContractError("Source access, real data, contact, sending, and conclusions are blocked")


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def verify_ledger(path: str | Path) -> list[dict[str, Any]]:
    ledger = Path(path)
    if not ledger.exists():
        return []
    records: list[dict[str, Any]] = []
    previous_hash = "GENESIS"
    for expected_sequence, line in enumerate(ledger.read_text(encoding="utf-8").splitlines(), start=1):
        record = json.loads(line)
        event = record.get("event")
        validate_event(event)
        if record.get("sequence") != expected_sequence or record.get("previous_hash") != previous_hash:
            raise PassportContractError("Ledger sequence or previous_hash is invalid")
        expected_hash = hashlib.sha256(_canonical({"sequence": expected_sequence, "previous_hash": previous_hash, "event": event}).encode()).hexdigest()
        if record.get("record_hash") != expected_hash:
            raise PassportContractError("Ledger record_hash is invalid")
        records.append(record)
        previous_hash = expected_hash
    return records


def append_manual_event(path: str | Path, event: dict[str, Any]) -> dict[str, Any]:
    """Append one validated local event after verifying the complete hash chain."""
    validate_event(event)
    ledger = Path(path)
    if ledger.suffix != ".jsonl":
        raise PassportContractError("Ledger path must use .jsonl")
    prior = verify_ledger(ledger)
    sequence = len(prior) + 1
    previous_hash = prior[-1]["record_hash"] if prior else "GENESIS"
    payload = {"sequence": sequence, "previous_hash": previous_hash, "event": event}
    record = {**payload, "record_hash": hashlib.sha256(_canonical(payload).encode()).hexdigest()}
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open("a", encoding="utf-8") as stream:
        stream.write(_canonical(record) + "\n")
    return record


def preview_internal_alert(event: dict[str, Any]) -> dict[str, Any]:
    """Build a deterministic internal preview; this function never sends it."""
    validate_event(event)
    return {
        "preview_only": True,
        "dispatch_performed": False,
        "severity": "REVIEW_REQUIRED" if event["re_review_required"] else "RECORD_ONLY",
        "event_id": event["event_id"],
        "classification": event["classification"],
        "affected_claim_ids": sorted(event["affected_claim_ids"]),
        "affected_evidence_ids": sorted(event["affected_evidence_ids"]),
        "boundary": "No source refresh, scientific conclusion, external contact, or notification dispatch.",
    }
