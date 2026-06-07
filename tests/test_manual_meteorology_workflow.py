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
        for name in ("observation_date:", "manual_approval:", "force_refresh:", "commit_outputs:"):
            self.assertIn(name, self.workflow)

    def test_workflow_calls_guarded_runtime(self) -> None:
        self.assertIn("python cczps_lite/engine/meteorology_runtime.py", self.workflow)
        self.assertIn("--live", self.workflow)
        self.assertIn("--manual-approval", self.workflow)
        self.assertIn("--force-refresh", self.workflow)
        self.assertIn("python -m unittest discover", self.workflow)

    def test_artifact_fallback_contains_both_outputs(self) -> None:
        self.assertIn("actions/upload-artifact@v4", self.workflow)
        self.assertIn("name: meteorology-refresh-output", self.workflow)
        self.assertIn("cczps_lite/output/meteorology_evidence.json", self.workflow)
        self.assertIn("cczps_lite/output/meteorology_cache.json", self.workflow)

    def test_commit_is_conditional_and_avoids_empty_commit(self) -> None:
        self.assertIn("if: ${{ inputs.commit_outputs }}", self.workflow)
        self.assertIn("git diff --cached --quiet", self.workflow)
        self.assertIn('git commit -m "Refresh meteorology evidence for $OBSERVATION_DATE"', self.workflow)


if __name__ == "__main__":
    unittest.main()
