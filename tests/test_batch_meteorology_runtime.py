"""Tests for controlled batch meteorology refresh behavior."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from cczps_lite.engine.meteorology_runtime import (
    MAX_DATES_PER_RUN,
    build_batch_meteorology_output,
    parse_observation_dates,
)


def nasa_payload(date: str) -> dict:
    return {
        "properties": {
            "parameter": {
                "T2M": {date: 12.5},
                "PRECTOTCORR": {date: 3.2},
                "RH2M": {date: 78},
                "WS2M": {date: 4.0},
                "ALLSKY_SFC_SW_DWN": {date: 8.4},
            }
        }
    }


class BatchDateParsingTests(unittest.TestCase):
    def test_explicit_list_is_validated_deduplicated_and_sorted(self) -> None:
        self.assertEqual(
            parse_observation_dates("20250515, 20250501,20250508,20250501"),
            ["20250501", "20250508", "20250515"],
        )

    def test_date_range_honors_interval_and_includes_end(self) -> None:
        self.assertEqual(
            parse_observation_dates(
                start_date="20250501",
                end_date="20250515",
                interval_days=7,
            ),
            ["20250501", "20250508", "20250515"],
        )

    def test_limit_accepts_ten_and_rejects_more(self) -> None:
        ten_dates = ",".join(f"202501{day:02d}" for day in range(1, 11))
        eleven_dates = ",".join(f"202501{day:02d}" for day in range(1, 12))
        self.assertEqual(len(parse_observation_dates(ten_dates)), MAX_DATES_PER_RUN)
        with self.assertRaisesRegex(ValueError, "maximum per run is 10"):
            parse_observation_dates(eleven_dates)

    def test_invalid_or_ambiguous_inputs_fail(self) -> None:
        invalid_inputs = ("", "20250230", "2025-05-01", "20250501,")
        for value in invalid_inputs:
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse_observation_dates(value)
        with self.assertRaisesRegex(ValueError, "either observation_dates"):
            parse_observation_dates("20250501", "20250501", "20250502")
        with self.assertRaisesRegex(ValueError, "positive"):
            parse_observation_dates(
                start_date="20250501", end_date="20250502", interval_days=0
            )
        with self.assertRaisesRegex(ValueError, "must not be after"):
            parse_observation_dates(
                start_date="20250502", end_date="20250501", interval_days=1
            )


class BatchGovernanceTests(unittest.TestCase):
    def test_each_date_is_governed_and_cache_hit_makes_no_request(self) -> None:
        governance_calls = []
        fetch_calls = []

        def governance(*args, **kwargs):
            governance_calls.append((args, kwargs))
            return {
                "requires_user_approval": True,
                "agentic_consumption_risk": "medium",
                "estimated_external_resource_cost": "medium",
            }

        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory) / "cache.json"
            timeseries = Path(directory) / "timeseries.json"
            fetcher = lambda request: (
                fetch_calls.append(request) or nasa_payload(request["date"])
            )
            build_batch_meteorology_output(
                ["20250501"],
                manual_approval_granted=True,
                fetcher=fetcher,
                cache_path=cache,
                timeseries_path=timeseries,
                governance_deriver=governance,
            )
            output, _ = build_batch_meteorology_output(
                ["20250501", "20250508"],
                manual_approval_granted=True,
                fetcher=fetcher,
                cache_path=cache,
                timeseries_path=timeseries,
                governance_deriver=governance,
            )
        self.assertEqual(len(governance_calls), 3)
        self.assertEqual(len(fetch_calls), 12)
        first_date_records = output["date_results"][0]["scenarios"].values()
        self.assertTrue(all(record["from_cache"] for record in first_date_records))

    def test_stop_required_prevents_remaining_dates(self) -> None:
        guard_calls = []
        fetch_calls = []

        def guard(governance, request, profile):
            guard_calls.append(request["estimated_calls"])
            stopped = request["estimated_calls"] > 6
            return {
                "budget_status": "stop_required" if stopped else "within_budget",
                "requires_manual_confirmation": False,
                "budget_guard_summary": "test stop" if stopped else "test pass",
            }

        with tempfile.TemporaryDirectory() as directory:
            output, timeseries = build_batch_meteorology_output(
                ["20250501", "20250508", "20250515"],
                manual_approval_granted=True,
                fetcher=lambda request: (
                    fetch_calls.append(request) or nasa_payload(request["date"])
                ),
                cache_path=Path(directory) / "cache.json",
                timeseries_path=Path(directory) / "timeseries.json",
                guard_deriver=guard,
            )
        self.assertEqual(guard_calls, [6, 12])
        self.assertEqual(len(fetch_calls), 6)
        self.assertEqual(
            [result["status"] for result in output["date_results"]],
            ["within_budget", "stop_required", "not_retrieved"],
        )
        self.assertTrue(output["stopped_early"])
        self.assertEqual(len(timeseries["observations"]), 6)
        blocked = output["date_results"][1]["scenarios"].values()
        self.assertTrue(
            all(record["retrieval_status"] == "blocked_by_budget_guard" for record in blocked)
        )

    def test_missing_approval_blocks_every_uncached_reading(self) -> None:
        fetch_calls = []
        with tempfile.TemporaryDirectory() as directory:
            output, timeseries = build_batch_meteorology_output(
                ["20250501"],
                fetcher=lambda request: fetch_calls.append(request),
                cache_path=Path(directory) / "cache.json",
                timeseries_path=Path(directory) / "timeseries.json",
            )
        self.assertFalse(fetch_calls)
        self.assertFalse(timeseries["observations"])
        self.assertTrue(
            all(
                record["retrieval_status"] == "blocked_by_budget_guard"
                for record in output["scenarios"].values()
            )
        )


if __name__ == "__main__":
    unittest.main()
