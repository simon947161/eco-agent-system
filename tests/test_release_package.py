"""Structural tests for the CCZPS-Lite v0.5 release package."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
RELEASE_DIR = REPO_ROOT / "docs" / "08_RELEASES"
OUTPUT_DIR = REPO_ROOT / "cczps_lite" / "output"


class ReleasePackageTests(unittest.TestCase):
    def test_required_release_documents_and_sections_exist(self) -> None:
        requirements = {
            "CCZPS_LITE_V0_5_RELEASE_NOTES.md": (
                "## Release Purpose",
                "## Major Features",
                "## Architecture Summary",
                "## Runtime Overview",
                "## Validation Workflow",
                "## Dashboard Overview",
                "## Demonstration Scenarios",
                "## Known Limitations",
                "## Safety Boundaries",
                "## Future Roadmap",
                "## Relationship to ClimateOS",
                "## Future Application Layers",
            ),
            "CCZPS_LITE_V0_5_ARCHITECTURE_SUMMARY.md": (
                "## Layered Architecture",
                "Scenario Layer",
                "Evidence Traceability Layer",
                "Scenario Comparison Layer",
                "Governance and Budget Guard Layer",
            ),
            "CCZPS_LITE_V0_5_DEMONSTRATION_GUIDE.md": (
                "## Recommended Demonstration Sequence",
                "## Reading Evidence Traceability",
                "## Reading Governance Decision Records",
                "## Reading Scenario Comparison",
                "## Explaining `not_ready_for_approval`",
            ),
            "CCZPS_LITE_V0_5_OUTPUT_INVENTORY.md": ("| File path |",),
            "CCZPS_LITE_V0_5_REPOSITORY_STRUCTURE_REVIEW.md": (
                "## Observed Structure Issues",
                "## Recommended Future Cleanup",
            ),
            "README.md": ("v0.5",),
        }
        for filename, sections in requirements.items():
            path = RELEASE_DIR / filename
            self.assertTrue(path.is_file(), path)
            content = path.read_text(encoding="utf-8")
            for section in sections:
                self.assertIn(section, content)

    def test_inventory_references_existing_major_outputs(self) -> None:
        inventory = (
            RELEASE_DIR / "CCZPS_LITE_V0_5_OUTPUT_INVENTORY.md"
        ).read_text(encoding="utf-8")
        major_outputs = (
            "meteorology_evidence.json",
            "meteorology_timeseries.json",
            "meteorology_trends.json",
            "planning_hypotheses.json",
            "gis_dem_access_plan.json",
            "professional_validation_interface.json",
            "expert_review_records.json",
            "planning_approval_support_report.json",
            "evidence_traceability.json",
            "governance_decision_records.json",
            "scenario_comparison.json",
        )
        for filename in major_outputs:
            self.assertTrue((OUTPUT_DIR / filename).is_file(), filename)
            self.assertIn(f"cczps_lite/output/{filename}", inventory)

    def test_release_preserves_generated_output_boundaries(self) -> None:
        for filename in (
            "governance_decision_records.json",
            "scenario_comparison.json",
        ):
            output = json.loads((OUTPUT_DIR / filename).read_text(encoding="utf-8"))
            for record in output["records"]:
                self.assertTrue(record["human_review_required"])
                self.assertTrue(record["professional_review_required"])
        comparison = json.loads(
            (OUTPUT_DIR / "scenario_comparison.json").read_text(encoding="utf-8")
        )
        for record in comparison["records"]:
            self.assertEqual(
                record["approval_support_status"], "not_ready_for_approval"
            )

    def test_release_package_adds_no_runtime_or_external_clients(self) -> None:
        release_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in RELEASE_DIR.glob("*.md")
        )
        for boundary in (
            "no external API",
            "no LLM",
            "not_ready_for_approval",
            "Human and professional review remain mandatory",
        ):
            self.assertIn(boundary.lower(), release_text.lower())


if __name__ == "__main__":
    unittest.main()
