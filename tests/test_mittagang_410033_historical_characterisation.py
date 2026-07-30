from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from cczps_lite.analysis.mittagang_410033_historical_characterisation import (
    HistoricalCharacterisationError,
    build_time_bounded_answer,
    characterise,
    validate_time_bounded_answer,
    write_outputs,
)


def _fixture() -> bytes:
    header = """#,"Australian Bureau of Meteorology"
#,"Hydrologic Reference Stations"
#,"Dataset version: August, 2024"
#,"Daily streamflow (ML/day) and quality code"
#,"Murrumbidgee River at Mittagang Crossing (410033)"
#,"Source used:",WISKI (validated data only)
#,"Data gaps were in filled by using daily rainfall-runoff model"
#,"Data extraction date:",14/06/2024
Date,Flow (ML),Bureau QCode
"""
    rows = [
        "2020-01-01,10,A",
        "2020-01-02,20,B",
        "2020-01-03,30,C",
        "2020-01-04,40,E",
        "2020-01-05,50,A",
    ]
    return (header + "\n".join(rows) + "\n").encode()


class HistoricalCharacterisationTests(unittest.TestCase):
    def test_characterisation_preserves_quality_and_two_axes(self) -> None:
        result = characterise(_fixture(), issued_at="2026-07-30T00:00:00Z")
        self.assertEqual(result["maximum_conclusion_level"], "L2")
        self.assertEqual(result["evidence_maturity"], "S0")
        self.assertEqual(
            result["quality_profile"]["quality_code_counts"],
            {"A": 2, "B": 1, "C": 1, "E": 1, "G": 0},
        )
        self.assertEqual(
            result["overall_distribution"]["all_published"]["median_ml_per_day"],
            30.0,
        )
        self.assertEqual(
            result["overall_distribution"]["quality_screen_a_b"][
                "median_ml_per_day"
            ],
            20.0,
        )
        self.assertEqual(result["trend_assessment"]["status"], "NOT_PERFORMED_IN_V0_1")

    def test_answer_is_bounded_and_validated(self) -> None:
        result = characterise(_fixture(), issued_at="2026-07-30T00:00:00Z")
        answer = build_time_bounded_answer(
            result, issued_at="2026-07-30T00:00:00Z"
        )
        validate_time_bounded_answer(answer)
        self.assertIn("not a statement of current conditions", answer["answer"])
        self.assertIn("issue a public warning", answer["prohibited_actions"])
        self.assertEqual(
            answer["human_review"]["qualified_hydrology_review"],
            "REQUIRED_BEFORE_L3",
        )

    def test_answer_rejects_level_promotion(self) -> None:
        result = characterise(_fixture(), issued_at="2026-07-30T00:00:00Z")
        answer = build_time_bounded_answer(
            result, issued_at="2026-07-30T00:00:00Z"
        )
        answer["conclusion_level"] = "L3"
        with self.assertRaises(HistoricalCharacterisationError):
            validate_time_bounded_answer(answer)

    def test_outputs_are_reproducible_and_machine_readable(self) -> None:
        result = characterise(_fixture(), issued_at="2026-07-30T00:00:00Z")
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            digests = write_outputs(
                result, root, issued_at="2026-07-30T00:00:00Z"
            )
            self.assertIn("monthly_distribution.svg", digests)
            receipt = json.loads((root / "run_receipt.json").read_text())
            self.assertEqual(receipt["conclusion_level"], "L2")
            self.assertFalse(receipt["public_warning_issued"])
            self.assertIsNone(receipt["current_condition_conclusion"])
            self.assertTrue((root / "METHOD_AND_RESULTS.md").exists())
            self.assertTrue((root / "annual_complete_year_profile.csv").exists())


if __name__ == "__main__":
    unittest.main()
