"""Structural regression tests for the static CCZPS-Lite dashboard."""

from __future__ import annotations

import unittest
from html.parser import HTMLParser
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_DIR = REPO_ROOT / "cczps_lite" / "dashboard"
PAGES_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "deploy-dashboard-pages.yml"


class DashboardHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.scripts: list[str] = []
        self.stylesheets: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if attributes.get("id"):
            self.ids.add(str(attributes["id"]))
        if tag == "script" and attributes.get("src"):
            self.scripts.append(str(attributes["src"]))
        if tag == "link" and attributes.get("rel") == "stylesheet":
            self.stylesheets.append(str(attributes.get("href", "")))


class DemonstrationDashboardTests(unittest.TestCase):
    def test_dashboard_assets_and_sections_exist(self) -> None:
        index_path = DASHBOARD_DIR / "index.html"
        styles_path = DASHBOARD_DIR / "styles.css"
        script_path = DASHBOARD_DIR / "dashboard.js"
        usage_script_path = DASHBOARD_DIR / "usage-cost-dashboard.js"
        budget_script_path = DASHBOARD_DIR / "budget-guard-dashboard.js"
        for path in (index_path, styles_path, script_path, usage_script_path, budget_script_path):
            self.assertTrue(path.is_file(), path)
        parser = DashboardHTMLParser()
        parser.feed(index_path.read_text(encoding="utf-8"))
        self.assertEqual(parser.scripts, ["dashboard.js", "usage-cost-dashboard.js", "budget-guard-dashboard.js"])
        self.assertEqual(parser.stylesheets, ["styles.css"])
        for section_id in ("overview", "comparison", "runtime-chain", "scenario-detail", "usage-cost", "budget-guard", "validation-report", "capability-map"):
            self.assertIn(section_id, parser.ids)

    def test_dashboard_reads_existing_outputs_without_external_services(self) -> None:
        script = (DASHBOARD_DIR / "dashboard.js").read_text(encoding="utf-8")
        for path in ("../output/comparison_matrix.csv", "../../docs/CCZPS_LITE_SYSTEM_VALIDATION_REPORT.md", "../output/runtime_capability_map.md"):
            self.assertIn(path, script)
        for forbidden in ("https://", "http://", "XMLHttpRequest", "WebSocket"):
            self.assertNotIn(forbidden, script)
        for scenario in ("batlow", "kunlun", "iraq", "baiyangdian"):
            self.assertIn(f"{scenario}:", script)
        usage_script = (DASHBOARD_DIR / "usage-cost-dashboard.js").read_text(encoding="utf-8")
        for field in ("usage_mode", "external_resource_owner", "external_cost_bearer", "platform_service_recipient", "estimated_external_resource_cost", "platform_service_fee_model", "platform_service_fee_estimate", "budget_warning", "requires_user_approval", "agentic_consumption_risk"):
            self.assertIn(field, usage_script)
        budget_script = (DASHBOARD_DIR / "budget-guard-dashboard.js").read_text(encoding="utf-8")
        for field in ("budget_status", "daily_call_limit", "estimated_calls", "agent_run_limit", "requires_manual_confirmation", "stop_if_budget_exceeded"):
            self.assertIn(field, budget_script)

    def test_github_pages_workflow_stages_a_self_contained_site(self) -> None:
        self.assertTrue(PAGES_WORKFLOW.is_file())
        workflow = PAGES_WORKFLOW.read_text(encoding="utf-8")
        for expected in ("branches:\n      - main", "contents: read", "pages: write", "id-token: write", "actions/checkout@v4", "actions/configure-pages@v5", "actions/upload-pages-artifact@v4", "actions/deploy-pages@v4", "name: github-pages", "url: ${{ steps.deployment.outputs.page_url }}", "cp -R cczps_lite/dashboard/. _site/", "data/comparison_matrix.csv", "data/system_validation_report.md", "data/runtime_capability_map.md", "python cczps_lite/engine/usage_cost_governance.py", "_site/usage-cost-dashboard.js", "python cczps_lite/engine/budget_guard.py", "_site/budget-guard-dashboard.js"):
            self.assertIn(expected, workflow)


if __name__ == "__main__":
    unittest.main()
