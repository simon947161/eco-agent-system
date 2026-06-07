"""Tests for the CCZPS-Lite Usage & Cost Governance Runtime."""

from __future__ import annotations

import csv
import unittest
from pathlib import Path

from cczps_lite.engine.scenario_compare import main as run_scenario_compare
from cczps_lite.engine.usage_cost_governance import (
    augment_runtime_outputs,
    derive_usage_cost_governance,
    governance_for_scenario,
    load_usage_profiles,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


class UsageCostGovernanceRuntimeTests(unittest.TestCase):
    def test_usage_modes_and_risk_levels(self) -> None:
        self.assertEqual(
            derive_usage_cost_governance("idea_mode", "user")["estimated_cost_level"],
            "low",
        )
        self.assertEqual(
            derive_usage_cost_governance(
                "project_mode", "user", external_resource_count=1
            )["estimated_cost_level"],
            "medium",
        )
        self.assertEqual(
            derive_usage_cost_governance(
                "agent_mode",
                "user",
                external_resource_count=1,
                continuous_execution=True,
                agent_count=1,
            )["agentic_risk_level"],
            "high",
        )
        self.assertEqual(
            derive_usage_cost_governance(
                "enterprise_mode",
                "program_owner",
                external_resource_count=3,
                agent_count=2,
                budget_controlled=False,
                platform_service_model="enterprise_support",
            )["estimated_cost_level"],
            "very_high",
        )

    def test_budget_warning_and_approval_rules(self) -> None:
        repeated = derive_usage_cost_governance(
            "project_mode",
            "user",
            external_resource_count=2,
            repeated_external_calls=True,
        )
        no_external = derive_usage_cost_governance("idea_mode", "user")
        self.assertTrue(repeated["budget_warning"])
        self.assertTrue(repeated["requires_user_approval"])
        self.assertFalse(no_external["budget_warning"])
        self.assertFalse(no_external["requires_user_approval"])

    def test_summary_states_governance_boundary(self) -> None:
        reading = derive_usage_cost_governance(
            "agent_mode",
            "user",
            external_resource_count=2,
            continuous_execution=True,
            agent_count=1,
            platform_service_model="service_fee",
        )
        self.assertIn("Explicit user approval is required", reading["governance_summary"])
        self.assertIn("no billing", reading["governance_summary"])

    def test_profiles_cover_every_generated_scenario(self) -> None:
        profiles = load_usage_profiles()
        expected = {
            "BATLOW_WATER_PRIORITY",
            "BATLOW_ENERGY_RESILIENCE",
            "BATLOW_ECOLOGY_FIRE_BUFFER",
            "KUNLUN_ECO_WATER",
            "IRAQ_AGRICULTURE_RECOVERY",
            "XIONGAN_WUTAI_HEADWATERS",
            "XIONGAN_BAIYANGDIAN_WETLAND",
            "XIONGAN_DOWNSTREAM_URBAN",
        }
        self.assertEqual(set(profiles["scenarios"]), expected)
        for scenario_id in expected:
            self.assertIn("governance_summary", governance_for_scenario(scenario_id))

    def test_output_and_report_integration(self) -> None:
        run_scenario_compare()
        rows = augment_runtime_outputs()
        self.assertEqual(len(rows), 8)
        output_dir = REPO_ROOT / "cczps_lite" / "output"
        with (output_dir / "comparison_matrix.csv").open(
            "r", encoding="utf-8", newline=""
        ) as file_obj:
            csv_rows = list(csv.DictReader(file_obj))
        for field in (
            "usage_mode",
            "external_resource_owner",
            "estimated_cost_level",
            "budget_warning",
            "requires_user_approval",
            "platform_service_model",
            "agentic_risk_level",
            "governance_summary",
        ):
            self.assertIn(field, csv_rows[0])
        self.assertIn(
            "## Usage & Cost Governance Reading",
            (output_dir / "scenario_report.md").read_text(encoding="utf-8"),
        )
        self.assertIn(
            "## Usage & Cost Governance Reading",
            (output_dir / "governance_summary.md").read_text(encoding="utf-8"),
        )
        self.assertIn(
            "## Task 19 Usage and Cost Governance Validation",
            (
                REPO_ROOT / "docs" / "CCZPS_LITE_SYSTEM_VALIDATION_REPORT.md"
            ).read_text(encoding="utf-8"),
        )


if __name__ == "__main__":
    unittest.main()
