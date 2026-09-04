"""Deterministic, evidence-bounded Cooma Site Reading v0.1."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

SCHEMA_ID = "climateos.cooma_site_reading.v0.1"
REASONING_TYPES = {
    "OBSERVED", "KNOWN_FROM_ADMITTED_EVIDENCE", "DERIVED", "INFERRED",
    "UNKNOWN", "MISSING_EVIDENCE", "PROHIBITED_CONCLUSION",
}


class SiteReadingError(ValueError):
    pass


def _digest(value: Any) -> str:
    body = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return "sha256:" + hashlib.sha256(body).hexdigest()


def build_site_reading(real_data_receipt: dict[str, Any], hydrology_receipt: dict[str, Any], *, generated_at: str) -> dict[str, Any]:
    if real_data_receipt.get("schema_id") != "climateos.cooma_official_real_data_public_receipt.v0.1":
        raise SiteReadingError("A validated Cooma public receipt is required")
    if real_data_receipt.get("environmental_conclusion") is not None:
        raise SiteReadingError("Input receipt exceeds its admitted conclusion boundary")
    hydro_status = hydrology_receipt.get("admission_status")
    if hydro_status not in {"ADMISSION_BLOCKED_MISSING_RAW_RESPONSE", "L1_EVIDENCE_ADMITTED"}:
        raise SiteReadingError("Unrecognised hydrology admission state")
    weather, outlook = real_data_receipt["sources"]
    reading = {
        "schema_id": SCHEMA_ID,
        "reading_id": "EP-SKILL-001-COOMA-SITE-READING-V0.1",
        "generated_at": generated_at,
        "place": {"name": "Cooma", "jurisdiction": "New South Wales, Australia", "reasoning_type": "KNOWN_FROM_ADMITTED_EVIDENCE"},
        "workflow": ["LOCATE", "OBSERVE", "CONTEXTUALISE", "COMPARE_WHERE_PERMITTED", "IDENTIFY_EVIDENCE_GAPS", "PRODUCE_BOUNDED_SITE_READING", "RECOMMEND_NEXT_EVIDENCE", "HUMAN_REVIEW"],
        "claims": [
            {"reasoning_type": "OBSERVED", "statement": f"The admitted BoM product contains {weather['parsed_metadata']['row_count']} dated Cooma rows from {weather['parsed_metadata']['coverage_start']} to {weather['parsed_metadata']['coverage_end']}.", "evidence_ids": [weather["source_id"]], "maximum_conclusion_level": "L1"},
            {"reasoning_type": "KNOWN_FROM_ADMITTED_EVIDENCE", "statement": f"The dated BoM outlook recorded {outlook['parsed_metadata']['state'].replace('_', ' ').title()} on {outlook['parsed_metadata']['archive_date']}.", "evidence_ids": [outlook["source_id"]], "maximum_conclusion_level": "L1"},
            {"reasoning_type": "DERIVED", "statement": "The committed public receipt supports source identity and bounded coverage, but intentionally omits public quantitative observation rows.", "evidence_ids": [weather["source_id"], real_data_receipt["pilot_id"]], "maximum_conclusion_level": "L1"},
            {"reasoning_type": "PROHIBITED_CONCLUSION", "statement": "The admitted evidence does not establish Cooma water security, water quality, catchment condition, causation, forecast, planning approval, or operational action.", "evidence_ids": [real_data_receipt["pilot_id"]], "maximum_conclusion_level": "L1"},
        ],
        "comparison": {"status": "NOT_COMPARABLE_YET" if hydro_status == "ADMISSION_BLOCKED_MISSING_RAW_RESPONSE" else "PERMITTED_ONLY_AFTER_SEMANTIC_REVIEW", "statistics": None, "reasoning_type": "MISSING_EVIDENCE"},
        "evidence_gaps": [
            {"reasoning_type": "MISSING_EVIDENCE", "status": hydro_status, "item": "Exact near-current WaterNSW raw response and retrieval receipt"},
            {"reasoning_type": "UNKNOWN", "status": "TREND_DEFERRED", "item": "Qualified hydrology interpretation of station representativeness, aggregation, timezone and quality semantics"},
            {"reasoning_type": "MISSING_EVIDENCE", "status": "OPEN", "item": "Admitted local ecological, soil, land-cover and catchment-scale observations"},
        ],
        "site_reading": "Cooma is located and represented by admitted official source identities and a bounded July 2026 BoM receipt. The receipt proves product coverage and a dated large-scale outlook state, not a complete local environmental condition. Hydrology comparison and trend remain deferred; this does not prevent the bounded location, evidence inventory, gap finding, and next-evidence recommendation.",
        "next_evidence": [
            "Retrieve and content-address the exact authorised WaterNSW 410033 response with its receipt.",
            "Obtain qualified hydrology review before any cross-period comparison or trend statement.",
            "Admit spatially explicit catchment, terrain, land-cover and ecological observations under existing evidence contracts.",
        ],
        "human_review": {"required": True, "status": "PENDING_HUMAN_REVIEW", "professional_signoff_simulated": False},
        "evidence_maturity": "S0",
        "maximum_conclusion_level": "L1",
    }
    used = {c["reasoning_type"] for c in reading["claims"]} | {g["reasoning_type"] for g in reading["evidence_gaps"]} | {reading["comparison"]["reasoning_type"]}
    if not used <= REASONING_TYPES:
        raise SiteReadingError("Unsupported reasoning type")
    reading["content_digest"] = _digest(reading)
    return reading


def build_passport(reading: dict[str, Any], inputs: list[dict[str, Any]]) -> dict[str, Any]:
    return {"schema_id": "climateos.cooma_site_reading.evidence_passport.v0.1", "reading_id": reading["reading_id"], "reading_digest": reading["content_digest"], "evidence_maturity": reading["evidence_maturity"], "maximum_conclusion_level": reading["maximum_conclusion_level"], "input_digests": [_digest(item) for item in inputs], "human_review_required": True, "release_status": "QUARANTINED_PENDING_HUMAN_REVIEW"}


def run(output_root: str | Path, *, repo_root: str | Path | None = None, generated_at: str | None = None) -> dict[str, Path]:
    root = Path(repo_root) if repo_root else Path(__file__).resolve().parents[2]
    real_path = root / "cczps_lite/output/cooma_official_real_data_pilot_receipt.json"
    hydro_path = root / "cczps_lite/output/waternsw_near_current_evidence_admission/blocked_receipt.json"
    if not hydro_path.exists():
        matches = sorted((root / "cczps_lite/output/waternsw_near_current_evidence_admission").glob("*.json"))
        if not matches:
            raise SiteReadingError("Hydrology admission receipt is missing")
        hydro_path = matches[0]
    real = json.loads(real_path.read_text(encoding="utf-8"))
    hydro = json.loads(hydro_path.read_text(encoding="utf-8"))
    timestamp = generated_at or datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    reading = build_site_reading(real, hydro, generated_at=timestamp)
    passport = build_passport(reading, [real, hydro])
    receipt = {"schema_id": "climateos.cooma_site_reading.run_receipt.v0.1", "run_id": reading["reading_id"], "generated_at": timestamp, "network_used": False, "inputs": [str(real_path.relative_to(root)), str(hydro_path.relative_to(root))], "reading_digest": reading["content_digest"], "passport_digest": _digest(passport), "result": "BOUNDED_SITE_READING_PRODUCED", "limitations": ["ADMISSION_BLOCKED_MISSING_RAW_RESPONSE", "NOT_COMPARABLE_YET", "TREND_DEFERRED"]}
    out = Path(output_root); out.mkdir(parents=True, exist_ok=True)
    paths = {"reading": out / "site_reading.json", "passport": out / "evidence_passport.json", "receipt": out / "run_receipt.json", "markdown": out / "FOUNDER_SITE_READING.md"}
    for key, value in (("reading", reading), ("passport", passport), ("receipt", receipt)):
        paths[key].write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    paths["markdown"].write_text("# Cooma Site Reading v0.1\n\n" + reading["site_reading"] + "\n\n## What is known\n\n" + "\n".join(f"- **{c['reasoning_type']}** — {c['statement']}" for c in reading["claims"]) + "\n\n## Evidence gaps\n\n" + "\n".join(f"- **{g['status']}** — {g['item']}" for g in reading["evidence_gaps"]) + "\n\n## Recommended next evidence\n\n" + "\n".join(f"{i}. {v}" for i, v in enumerate(reading["next_evidence"], 1)) + "\n\n## Human review\n\nPending. No professional sign-off has been simulated.\n", encoding="utf-8")
    return paths

