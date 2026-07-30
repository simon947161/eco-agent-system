"""Bounded comparability gate for Mittagang 410033 near-current evidence."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SCHEMA_ID = "climateos.mittagang_410033_near_current_comparability.v0.1"
METHOD_VERSION = "0.1.0"
REQUIRED_DIMENSIONS = (
    "station_identity",
    "measurement",
    "unit",
    "aggregation_window",
    "day_boundary",
    "timezone",
    "quality_semantics",
    "provenance",
)


class ComparabilityGateError(ValueError):
    """Raised when evidence cannot be evaluated safely."""


@dataclass(frozen=True)
class Dimension:
    name: str
    status: str
    historical: Any
    near_current: Any
    reason: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "dimension": self.name,
            "status": self.status,
            "historical": self.historical,
            "near_current": self.near_current,
            "reason": self.reason,
        }


def _same(left: Any, right: Any) -> bool:
    return left is not None and right is not None and left == right


def evaluate_comparability(
    historical: dict[str, Any],
    near_current: dict[str, Any],
    *,
    issued_at: str,
) -> dict[str, Any]:
    """Evaluate equivalence without calculating a percentile or environmental trend."""
    if not issued_at:
        raise ComparabilityGateError("issued_at is required")

    checks = [
        Dimension(
            "station_identity",
            "PASS" if _same(historical.get("station_id"), near_current.get("station_id")) else "FAIL",
            historical.get("station_id"),
            near_current.get("station_id"),
            "The same gauge identifier must be explicit in both products.",
        ),
        Dimension(
            "measurement",
            "PASS" if _same(historical.get("measurement"), near_current.get("measurement")) else "BLOCKED",
            historical.get("measurement"),
            near_current.get("measurement"),
            "A FlowRate label does not by itself prove equivalence to a daily discharge total.",
        ),
        Dimension(
            "unit",
            "PASS" if _same(historical.get("unit"), near_current.get("unit")) else "FAIL",
            historical.get("unit"),
            near_current.get("unit"),
            "Canonical units must match before values can be compared.",
        ),
        Dimension(
            "aggregation_window",
            "PASS" if _same(historical.get("aggregation_window"), near_current.get("aggregation_window")) else "BLOCKED",
            historical.get("aggregation_window"),
            near_current.get("aggregation_window"),
            "Instantaneous, interval and previous-24-hour values are not interchangeable.",
        ),
        Dimension(
            "day_boundary",
            "PASS" if _same(historical.get("day_boundary"), near_current.get("day_boundary")) else "BLOCKED",
            historical.get("day_boundary"),
            near_current.get("day_boundary"),
            "The observation timestamp must be mapped to the historical 09:00 local reporting boundary.",
        ),
        Dimension(
            "timezone",
            "PASS" if _same(historical.get("timezone"), near_current.get("timezone")) else "BLOCKED",
            historical.get("timezone"),
            near_current.get("timezone"),
            "A stable timezone rule, including daylight-saving treatment, is required.",
        ),
        Dimension(
            "quality_semantics",
            "PASS" if _same(historical.get("quality_scheme"), near_current.get("quality_scheme")) else "BLOCKED",
            historical.get("quality_scheme"),
            near_current.get("quality_scheme"),
            "Numeric WaterNSW quality code 125 is not yet mapped to the HRS A/B/C/E/G definitions.",
        ),
        Dimension(
            "provenance",
            "PASS"
            if near_current.get("content_digest")
            and near_current.get("retrieval_receipt_digest")
            else "BLOCKED",
            historical.get("content_digest"),
            {
                "content_digest": near_current.get("content_digest"),
                "retrieval_receipt_digest": near_current.get("retrieval_receipt_digest"),
            },
            "The exact near-current response and retrieval receipt must be content-addressed.",
        ),
    ]
    statuses = {item.status for item in checks}
    gate_status = "COMPARABLE" if statuses == {"PASS"} else "NOT_COMPARABLE_YET"
    return {
        "schema_id": SCHEMA_ID,
        "method_version": METHOD_VERSION,
        "issued_at": issued_at,
        "station_id": historical.get("station_id"),
        "gate_status": gate_status,
        "evidence_maturity": "S0",
        "maximum_conclusion_level": "L1",
        "checks": [item.as_dict() for item in checks],
        "required_dimensions": list(REQUIRED_DIMENSIONS),
        "near_current_value_retained_for_identity_only": {
            "observed_at": near_current.get("observed_at"),
            "value": near_current.get("value"),
            "unit": near_current.get("unit"),
            "quality_code": near_current.get("quality_code"),
        },
        "comparison_statistics": None,
        "environmental_conclusion": None,
        "trend_assessment": {
            "status": "DEFERRED_PENDING_QUALIFIED_HYDROLOGY_REVIEW",
            "performed": False,
        },
        "next_admissible_actions": [
            "retain the exact WaterNSW response bytes and SHA-256 receipt",
            "obtain official parameter and aggregation metadata for FlowRate",
            "resolve AEST/AEDT and historical local-time day boundaries",
            "obtain an official mapping or documented treatment for quality code 125",
            "rerun this gate before calculating any percentile",
        ],
        "prohibited_actions": [
            "compare 194.296 ML/day directly with the historical distribution",
            "label the observation above, below or within normal",
            "make a current water, supply, drinking-water, engineering or public-safety claim",
            "perform or imply a formal trend assessment",
        ],
    }


def write_gate(result: dict[str, Any], output_path: str | Path) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
