"""Structural tests for the manual meteorology refresh workflow."""
from __future__ import annotations
import unittest
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "manual-meteorology-refresh.yml"


class ManualMeteorologyRefreshWorkflowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.assertTrue(WORKFLOW_PATH.is_file())
        self.workflow = WORKFLOW_PATH.read_text(encoding="utf-8")

    def test_workflow_is_manual_only(self) -> None:
        self.assertIn("workflow_dispatch:", self.workflow)
        self.assertNotIn("schedule:", self.workflow)
        self.assertNotIn("cron:", self.workflow)

    def test_required_dispatch_inputs_exist(self) -> None:
        for name in (
            "observation_dates:", "start_date:", "end_date:", "interval_days:",
            "manual_approval:", "force_refresh:", "commit_outputs:",
        ):
            self.assertIn(name, self.workflow)

    def test_workflow_calls_guarded_runtime(self) -> None:
        self.assertIn("python cczps_lite/engine/meteorology_batch_runtime.py", self.workflow)
        for argument in ("--manual-approval", "--dates", "--start-date", "--end-date", "--interval-days", "--force-refresh"):
            self.assertIn(argument, self.workflow)
        self.assertIn("python -m unittest discover", self.workflow)

    def test_manual_approval_is_required_before_runtime(self) -> None:
        approval = 'if [[ "$MANUAL_APPROVAL" != "true" ]]'
        runtime = 'python cczps_lite/engine/meteorology_batch_runtime.py'
        self.assertIn(approval, self.workflow)
        self.assertLess(self.workflow.index(approval), self.workflow.index(runtime))

    def test_artifact_fallback_contains_all_outputs(self) -> None:
        self.assertIn("actions/upload-artifact@v4", self.workflow)
        self.assertIn("name: meteorology-refresh-output", self.workflow)
        for path in (
            "cczps_lite/output/meteorology_evidence.json",
            "cczps_lite/output/meteorology_cache.json",
            "cczps_lite/output/meteorology_timeseries.json",
            "cczps_lite/output/meteorology_trends.json",
            "cczps_lite/output/meteorology_trends.md",
        ):
            self.assertIn(path, self.workflow)

    def test_commit_is_conditional_and_avoids_empty_commit(self) -> None:
        self.assertIn("if: ${{ inputs.commit_outputs }}", self.workflow)
        self.assertIn("git diff --cached --quiet", self.workflow)
        self.assertIn('git commit -m "Refresh batch meteorology evidence"', self.workflow)

    def test_commit_targets_selected_branch(self) -> None:
        self.assertIn("ref: ${{ github.ref_name }}", self.workflow)
        self.assertIn("fetch-depth: 0", self.workflow)
        self.assertIn('if [[ "$GITHUB_REF_TYPE" != "branch" ]]', self.workflow)
        self.assertIn('git push origin "HEAD:refs/heads/${GITHUB_REF_NAME}"', self.workflow)

    def test_commit_scope_is_limited_to_meteorology_outputs(self) -> None:
        for path in (
            "meteorology_evidence.json", "meteorology_cache.json",
            "meteorology_timeseries.json", "meteorology_trends.json",
            "meteorology_trends.md",
        ):
            self.assertEqual(self.workflow.count(f"git add cczps_lite/output/{path}"), 1)
        self.assertIn("Refusing to commit unexpected files", self.workflow)
        self.assertNotIn("git add .", self.workflow)
        self.assertNotIn("git add -A", self.workflow)

    def test_main_push_can_trigger_dashboard_deployment(self) -> None:
        deployment = (REPO_ROOT / ".github" / "workflows" / "deploy-dashboard-pages.yml").read_text(encoding="utf-8")
        self.assertIn("push:", deployment)
        self.assertIn("branches:\n      - main", deployment)


if __name__ == "__main__":
    unittest.main()
