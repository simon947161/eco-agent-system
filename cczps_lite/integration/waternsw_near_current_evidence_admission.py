"""Controlled admission for WaterNSW near-current evidence.

The adapter deliberately accepts response bytes supplied by an authorised
retrieval step. It does not contain credentials and cannot reconstruct a raw
response from a copied observation summary.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

SCHEMA_ID = "climateos.waternsw_near_current_admission.v0.1"
RUN_ID = "WATERNSW-410033-NEAR-CURRENT-ADMISSION-V0.1"
MAX_RESPONSE_BYTES = 2 * 1024 * 1024


class WaterNSWAdmissionError(ValueError):
    """Raised when supplied evidence is absent, malformed, or outside scope."""


def _digest(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def blocked_receipt(*, attempted_at: str, reason: str) -> dict[str, Any]:
    """Return a machine-readable refusal without inventing response content."""
    if not attempted_at or not reason:
        raise WaterNSWAdmissionError("attempted_at and reason are required")
    return {
        "schema_id": SCHEMA_ID,
        "run_id": RUN_ID,
        "attempted_at": attempted_at,
        "admission_status": "ADMISSION_BLOCKED_MISSING_RAW_RESPONSE",
        "reason": reason,
        "response_content_digest": None,
        "retrieval_receipt_digest": None,
        "maximum_conclusion_level": "L1",
        "comparison_statistics": None,
        "environmental_conclusion": None,
        "trend_assessment": {
            "status": "DEFERRED_PENDING_QUALIFIED_HYDROLOGY_REVIEW",
            "performed": False,
        },
    }


def admit_response(
    response_bytes: bytes,
    retrieval: dict[str, Any],
    *,
    admitted_at: str,
) -> dict[str, Any]:
    """Validate and content-address an exact WaterNSW JSON response.

    The admitted payload remains L1 evidence. Parameter aggregation, timezone,
    day-boundary and cross-quality-scheme equivalence stay unresolved unless
    separately proven by official metadata.
    """
    if not response_bytes:
        raise WaterNSWAdmissionError("Exact response bytes are required")
    if len(response_bytes) > MAX_RESPONSE_BYTES:
        raise WaterNSWAdmissionError("Response exceeds the 2 MiB ceiling")
    if not admitted_at:
        raise WaterNSWAdmissionError("admitted_at is required")
    try:
        payload = json.loads(response_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise WaterNSWAdmissionError("Response must be UTF-8 JSON") from exc
    if not isinstance(payload, dict):
        raise WaterNSWAdmissionError("Top-level response must be an object")

    required_retrieval = {
        "source_url",
        "retrieved_at",
        "http_status",
        "station_id",
        "parameter",
        "unit",
    }
    missing = sorted(required_retrieval - retrieval.keys())
    if missing:
        raise WaterNSWAdmissionError(f"Retrieval metadata missing: {missing}")
    if retrieval["station_id"] != "410033":
        raise WaterNSWAdmissionError("Only station 410033 is authorised")
    if retrieval["parameter"] != "FlowRate":
        raise WaterNSWAdmissionError("Only FlowRate is authorised")
    if retrieval["unit"] != "ML/day":
        raise WaterNSWAdmissionError("Unexpected canonical unit")
    if int(retrieval["http_status"]) != 200:
        raise WaterNSWAdmissionError("Only HTTP 200 responses are admissible")
    if not str(retrieval["source_url"]).startswith("https://"):
        raise WaterNSWAdmissionError("Source URL must use HTTPS")

    response_digest = _digest(response_bytes)
    retrieval_record = {
        **retrieval,
        "response_bytes": len(response_bytes),
        "response_content_digest": response_digest,
    }
    retrieval_bytes = (
        json.dumps(retrieval_record, sort_keys=True, separators=(",", ":"))
        .encode("utf-8")
    )
    return {
        "schema_id": SCHEMA_ID,
        "run_id": RUN_ID,
        "admitted_at": admitted_at,
        "admission_status": "L1_EVIDENCE_ADMITTED",
        "source": retrieval_record,
        "retrieval_receipt_digest": _digest(retrieval_bytes),
        "raw_response_retention": "LOCAL_GITIGNORED_ONLY",
        "payload_top_level_keys": sorted(payload),
        "measurement_semantics": "UNRESOLVED",
        "aggregation_window": "UNRESOLVED",
        "day_boundary": "UNRESOLVED",
        "timezone_rule": "UNRESOLVED",
        "quality_code_mapping": "UNRESOLVED",
        "comparability_gate_status": "NOT_RERUN",
        "maximum_conclusion_level": "L1",
        "comparison_statistics": None,
        "environmental_conclusion": None,
        "trend_assessment": {
            "status": "DEFERRED_PENDING_QUALIFIED_HYDROLOGY_REVIEW",
            "performed": False,
        },
    }


def write_receipt(receipt: dict[str, Any], output_path: str | Path) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(receipt, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
