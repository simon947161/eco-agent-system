"""Emit the Task2121-2130 real-run admission state."""

from pathlib import Path

from cczps_lite.integration.waternsw_near_current_evidence_admission import (
    blocked_receipt,
    write_receipt,
)


def main() -> None:
    receipt = blocked_receipt(
        attempted_at="2026-07-31T00:00:00Z",
        reason=(
            "The authorised runtime has neither the exact 2026-07-28 WaterNSW "
            "response bytes nor a configured subscription key. A copied field "
            "summary cannot be promoted to raw evidence."
        ),
    )
    write_receipt(
        receipt,
        Path(
            "cczps_lite/output/waternsw_near_current_evidence_admission/"
            "admission_receipt.json"
        ),
    )


if __name__ == "__main__":
    main()
