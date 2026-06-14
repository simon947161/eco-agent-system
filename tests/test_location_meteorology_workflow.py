"""Structural tests for the manual Location Meteorology Refresh workflow."""
from __future__ import annotations

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "location-meteorology-refresh.yml"


class LocationMeteorologyWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.workflow = WORKFLOW.read_text(encoding="utf-8")

    def test_workflow_is_manual_only(self) -> None:
        self.assertIn("workflow_dispatch:", self.workflow)
        self.assertNotIn("schedule:", self.workflow)
        self.assertNotIn("cron:", self.workflow)
        self.assertNotIn("push:", self.workflow)

    def test_workflow_requires_manual_approval(self) -> None:
        self.assertIn("manual_approval:", self.workflow)
        self.assertIn('if [[ "$MANUAL_APPROVAL" != "true" ]]', self.workflow)
        self.assertIn("--manual-approval", self.workflow)

    def test_workflow_supports_dates_selection_and_cache_control(self) -> None:
        for expected in (
            "observation_dates:",
            "selected_intake_ids:",
            "force_refresh:",
            "commit_outputs:",
            "--selected-intake-ids",
            "--force-refresh",
        ):
            self.assertIn(expected, self.workflow)

    def test_commit_allowlist_and_empty_commit_guard_are_present(self) -> None:
        for path in (
            "cczps_lite/output/location_meteorology_evidence.json",
            "cczps_lite/output/location_meteorology_evidence.md",
            "cczps_lite/output/meteorology_cache.json",
        ):
            self.assertIn(path, self.workflow)
        self.assertIn("unexpected_files=", self.workflow)
        self.assertIn("git diff --cached --quiet", self.workflow)


if __name__ == "__main__":
    unittest.main()
