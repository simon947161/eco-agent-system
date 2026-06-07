"""Tests for the CCZPS-Lite Budget Guard Runtime."""

from __future__ import annotations

import csv
import unittest
from pathlib import Path

from cczps_lite.engine.budget_guard import augment_runtime_outputs, derive_budget_guard, summarize_budget_guard
from cczps_lite.engine.scenario_compare import main as run_scenario_compare
from cczps_lite.engine.usage_cost_governance import augment_runtime_outputs as run_usage

REPO_ROOT = Path(__file__).resolve().parents[1]
LIMITS = {"monthly_budget_limit": "medium", "daily_call_limit": 20, "agent_run_limit": 5, "stop_if_budget_exceeded": True}


def governance(mode: str = "idea_mode", risk: str = "low", approval: bool = False) -> dict:
    return {"usage_mode": mode, "estimated_external_resource_cost": risk, "agentic_consumption_risk": risk, "requires_user_approval": approval}


class BudgetGuardRuntimeTests(unittest.TestCase):
    def test_low_cost_idea_mode_remains_within_budget(self) -> None:
        self.assertEqual(derive_budget_guard(governance(), {"estimated_calls": 1}, LIMITS)["budget_status"], "within_budget")

    def test_medium_risk_research_requires_approval(self) -> None:
        result = derive_budget_guard(governance("research_mode", "medium", True), {"resource_classes": ["NASA POWER"], "estimated_calls": 10, "estimated_monthly_cost": "medium", "repeated_external_calls": True}, LIMITS)
        self.assertEqual(result["budget_status"], "approval_required")

    def test_agent_repeated_calls_require_manual_confirmation(self) -> None:
        result = derive_budget_guard(governance("agent_mode", "high", True), {"resource_classes": ["OpenAI"], "estimated_calls": 10, "estimated_monthly_cost": "medium", "repeated_external_calls": True}, LIMITS)
        self.assertTrue(result["requires_manual_confirmation"])

    def test_calls_above_limit_stop(self) -> None:
        self.assertEqual(derive_budget_guard(governance(), {"estimated_calls": 21}, LIMITS)["budget_status"], "stop_required")

    def test_agent_runs_above_limit_stop(self) -> None:
        self.assertEqual(derive_budget_guard(governance(), {"estimated_calls": 1, "agent_run_count": 6}, LIMITS)["budget_status"], "stop_required")

    def test_very_high_risk_without_approval_stops(self) -> None:
        result = derive_budget_guard(governance("enterprise_mode", "very_high", True), {"resource_classes": ["satellite"], "estimated_calls": 1}, LIMITS)
        self.assertEqual(result["budget_status"], "stop_required")

    def test_approval_clears_approval_only_but_not_hard_stop(self) -> None:
        approved = {"resource_classes": ["OpenAI"], "estimated_calls": 10, "estimated_monthly_cost": "medium", "repeated_external_calls": True, "manual_approval_granted": True}
        self.assertEqual(derive_budget_guard(governance("research_mode", "medium", True), approved, LIMITS)["budget_status"], "warning")
        approved["estimated_calls"] = 21
        self.assertEqual(derive_budget_guard(governance("research_mode", "medium", True), approved, LIMITS)["budget_status"], "stop_required")

    def test_summary_is_cautious_and_explicit(self) -> None:
        summary = summarize_budget_guard(derive_budget_guard(governance(), {"estimated_calls": 1}, LIMITS))
        self.assertIn("pre-execution governance check only", summary)
        self.assertIn("no metering, billing, payment", summary)

    def test_scenario_outputs_include_budget_guard_fields(self) -> None:
        run_scenario_compare()
        run_usage()
        rows = augment_runtime_outputs()
        self.assertEqual(len(rows), 8)
        with (REPO_ROOT / "cczps_lite" / "output" / "comparison_matrix.csv").open("r", encoding="utf-8", newline="") as file_obj:
            first = next(csv.DictReader(file_obj))
        for field in ("monthly_budget_limit", "daily_call_limit", "agent_run_limit", "estimated_calls", "estimated_cost_level", "budget_status", "budget_warning", "requires_manual_confirmation", "stop_if_budget_exceeded", "budget_guard_summary"):
            self.assertIn(field, first)


if __name__ == "__main__":
    unittest.main()
