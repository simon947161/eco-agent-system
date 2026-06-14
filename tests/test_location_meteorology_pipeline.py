"""Tests for the governed Location-to-Meteorology Pipeline."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from cczps_lite.engine.location_meteorology_pipeline import (
    MAX_DATES_PER_RUN,
    MAX_LOCATIONS_PER_RUN,
    build_location_meteorology_output,
    load_intake_profiles,
    select_intake_profiles,
    write_location_meteorology_outputs,
)


def nasa_payload(date: str) -> dict:
    return {
        "properties": {
            "parameter": {
                "T2M": {date: 18.2},
                "PRECTOTCORR": {date: 2.1},
                "RH2M": {date: 52.0},
                "WS2M": {date: 3.0},
                "WD2M": {date: 180.0},
                "ALLSKY_SFC_SW_DWN": {date: 20.0},
            }
        }
    }


def intake_file(path: Path, profile_count: int = 2) -> Path:
    profiles = [
        {
            "scenario_id": f"location_{index}_intake",
            "location_name": f"Location {index}",
            "latitude": -35.0 + index,
            "longitude": 148.0 + index,
            "scenario_status": "intake_only",
        }
        for index in range(profile_count)
    ]
    payload = {
        "scenario_profiles": profiles,
        "invalid_records": [
            {
                "location_name": "Invalid",
                "validation_errors": ["latitude_must_be_between_-90_and_90"],
            }
        ],
    }
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


class LocationMeteorologyPipelineTests(unittest.TestCase):
    def test_valid_profiles_are_read_and_invalid_records_are_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            profiles = load_intake_profiles(intake_file(Path(directory) / "intake.json"))
        self.assertEqual(len(profiles), 2)
        self.assertNotIn("Invalid", {item["location_name"] for item in profiles})

    def test_selected_intake_ids_are_respected(self) -> None:
        profiles = [
            {"scenario_id": "a", "scenario_status": "intake_only"},
            {"scenario_id": "b", "scenario_status": "intake_only"},
        ]
        self.assertEqual(
            [item["scenario_id"] for item in select_intake_profiles(profiles, ["b"])],
            ["b"],
        )

    def test_unknown_selected_intake_id_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "unknown intake"):
            select_intake_profiles([], ["missing"])

    def test_missing_manual_approval_prevents_live_retrieval(self) -> None:
        calls = []
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = build_location_meteorology_output(
                ["20250501"],
                intake_path=intake_file(root / "intake.json", 1),
                cache_path=root / "cache.json",
                fetcher=lambda request: calls.append(request) or nasa_payload(request["date"]),
            )
        self.assertEqual(calls, [])
        self.assertEqual(output["records"][0]["retrieval_status"], "manual_approval_required")

    def test_cache_hit_avoids_network_call_without_manual_approval(self) -> None:
        calls = []
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            intake = intake_file(root / "intake.json", 1)
            cache = root / "cache.json"
            build_location_meteorology_output(
                ["20250501"],
                manual_approval_granted=True,
                intake_path=intake,
                cache_path=cache,
                fetcher=lambda request: calls.append(request) or nasa_payload(request["date"]),
            )
            output = build_location_meteorology_output(
                ["20250501"],
                intake_path=intake,
                cache_path=cache,
                fetcher=lambda request: calls.append(request),
            )
        self.assertEqual(len(calls), 1)
        self.assertTrue(output["records"][0]["from_cache"])
        self.assertEqual(output["records"][0]["usage_governance_status"], "cache_only")

    def test_cache_miss_passes_governance_and_budget_guard(self) -> None:
        governance_calls = []
        guard_calls = []

        def governance(*args, **kwargs):
            governance_calls.append((args, kwargs))
            return {
                "estimated_external_resource_cost": "low",
                "agentic_consumption_risk": "low",
                "requires_user_approval": False,
            }

        def guard(governance_result, request, profile):
            guard_calls.append(request)
            return {
                "budget_status": "within_budget",
                "requires_manual_confirmation": False,
                "budget_guard_summary": "within test budget",
            }

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = build_location_meteorology_output(
                ["20250501"],
                manual_approval_granted=True,
                intake_path=intake_file(root / "intake.json", 1),
                cache_path=root / "cache.json",
                fetcher=lambda request: nasa_payload(request["date"]),
                governance_deriver=governance,
                guard_deriver=guard,
            )
        self.assertEqual(len(governance_calls), 1)
        self.assertEqual(guard_calls[0]["estimated_calls"], 1)
        self.assertEqual(output["records"][0]["retrieval_status"], "success")

    def test_location_limit_is_enforced_before_fetch(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaisesRegex(ValueError, "maximum per run"):
                build_location_meteorology_output(
                    ["20250501"],
                    intake_path=intake_file(root / "intake.json", MAX_LOCATIONS_PER_RUN + 1),
                    cache_path=root / "cache.json",
                )

    def test_date_limit_is_enforced_before_fetch(self) -> None:
        dates = [f"202505{day:02d}" for day in range(1, MAX_DATES_PER_RUN + 2)]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaisesRegex(ValueError, "maximum per run"):
                build_location_meteorology_output(
                    dates,
                    intake_path=intake_file(root / "intake.json", 1),
                    cache_path=root / "cache.json",
                )

    def test_stop_required_stops_remaining_live_retrievals(self) -> None:
        fetch_calls = []
        guard_count = 0

        def governance(*args, **kwargs):
            return {
                "estimated_external_resource_cost": "low",
                "agentic_consumption_risk": "low",
                "requires_user_approval": False,
            }

        def guard(governance_result, request, profile):
            nonlocal guard_count
            guard_count += 1
            status = "within_budget" if guard_count == 1 else "stop_required"
            return {
                "budget_status": status,
                "requires_manual_confirmation": False,
                "budget_guard_summary": status,
            }

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = build_location_meteorology_output(
                ["20250501", "20250508", "20250515"],
                manual_approval_granted=True,
                intake_path=intake_file(root / "intake.json", 1),
                cache_path=root / "cache.json",
                fetcher=lambda request: fetch_calls.append(request) or nasa_payload(request["date"]),
                governance_deriver=governance,
                guard_deriver=guard,
            )
        self.assertEqual(len(fetch_calls), 1)
        self.assertEqual(output["records"][1]["retrieval_status"], "blocked_by_budget_guard")
        self.assertEqual(output["records"][2]["retrieval_status"], "not_retrieved")
        self.assertTrue(output["stopped_early"])

    def test_success_preserves_review_and_approval_boundaries(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = build_location_meteorology_output(
                ["20250501"],
                manual_approval_granted=True,
                intake_path=intake_file(root / "intake.json", 1),
                cache_path=root / "cache.json",
                fetcher=lambda request: nasa_payload(request["date"]),
            )
        record = output["records"][0]
        self.assertEqual(record["approval_support_status"], "not_ready_for_approval")
        self.assertTrue(record["human_review_required"])
        self.assertTrue(record["professional_review_required"])
        self.assertEqual(record["trend_status"], "not_generated")

    def test_json_and_markdown_outputs_are_generated(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = build_location_meteorology_output(
                ["20250501"],
                intake_path=intake_file(root / "intake.json", 1),
                cache_path=root / "cache.json",
            )
            json_path = root / "evidence.json"
            md_path = root / "evidence.md"
            write_location_meteorology_outputs(output, json_path, md_path)
            stored = json.loads(json_path.read_text(encoding="utf-8"))
            report = md_path.read_text(encoding="utf-8")
        self.assertEqual(stored["runtime"], "Governed Location-to-Meteorology Pipeline")
        self.assertIn("# Governed Location-to-Meteorology Pipeline", report)

    def test_module_introduces_no_geocoding_map_gis_or_llm_clients(self) -> None:
        script = (
            Path(__file__).resolve().parents[1]
            / "cczps_lite"
            / "engine"
            / "location_meteorology_pipeline.py"
        ).read_text(encoding="utf-8")
        for forbidden in (
            "google.maps",
            "arcgis",
            "earthengine",
            "OpenAI(",
            "anthropic.",
            "requests.",
            "urlopen(",
        ):
            self.assertNotIn(forbidden, script)


if __name__ == "__main__":
    unittest.main()
