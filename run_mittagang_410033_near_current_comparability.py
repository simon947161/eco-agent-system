"""Run the Task2111-2120 bounded near-current comparability gate."""

from __future__ import annotations

from pathlib import Path

from cczps_lite.analysis.mittagang_410033_near_current_comparability import (
    evaluate_comparability,
    write_gate,
)

HISTORICAL = {
    "station_id": "410033",
    "measurement": "daily streamflow",
    "unit": "ML/day",
    "aggregation_window": "previous 24 hours",
    "day_boundary": "09:00 source-local time",
    "timezone": None,
    "quality_scheme": "BoM HRS A/B/C/E/G",
    "content_digest": "sha256:12740d6edc884b3f7a960935215cdff1bdbe5bd85c9c9a96d3aa219272d31534",
}

NEAR_CURRENT = {
    "source": "WaterNSW Surface Water Data API",
    "station_id": "410033",
    "measurement": "FlowRate",
    "unit": "ML/day",
    "aggregation_window": None,
    "day_boundary": None,
    "timezone": "AEST as displayed; DST rule unresolved",
    "quality_scheme": "WaterNSW numeric code",
    "quality_code": 125,
    "observed_at": "2026-07-28T19:45:00+10:00",
    "value": 194.296,
    "content_digest": None,
    "retrieval_receipt_digest": None,
}


def main() -> None:
    result = evaluate_comparability(
        HISTORICAL,
        NEAR_CURRENT,
        issued_at="2026-07-31T00:00:00Z",
    )
    write_gate(
        result,
        Path("cczps_lite/output/mittagang_410033_near_current_comparability/gate_result.json"),
    )


if __name__ == "__main__":
    main()
