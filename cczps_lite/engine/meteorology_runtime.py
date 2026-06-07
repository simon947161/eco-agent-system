"""Generate transparent meteorology evidence records for configured scenarios."""

from __future__ import annotations

import json
from pathlib import Path

from evidence_layer import meteorology_evidence_record
from meteorology_connector import (
    configured_scenario_reading,
    load_scenario_configuration,
)

PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_PATH = PROJECT_DIR / "output" / "meteorology_evidence.json"


def build_meteorology_output(fetcher=None, retrieved_at: str | None = None) -> dict:
    """Build observation records without changing any scenario score."""
    scenario_keys = load_scenario_configuration()["scenarios"]
    records = {}
    for scenario_key in scenario_keys:
        reading = configured_scenario_reading(
            scenario_key, fetcher=fetcher, retrieved_at=retrieved_at
        )
        records[scenario_key] = {
            "meteorology_reading": reading,
            "evidence": meteorology_evidence_record(reading),
        }
    return {
        "runtime": "Meteorology Connector Runtime",
        "decision_boundary": (
            "Supporting observational evidence only. No forecast, conclusion, "
            "recommendation, or automated scoring change."
        ),
        "scenarios": records,
    }


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(build_meteorology_output(), indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    print(f"Generated {OUTPUT_PATH.relative_to(PROJECT_DIR.parent)}")


if __name__ == "__main__":
    main()
