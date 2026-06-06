"""Structural regression tests for the static CCZPS-Lite dashboard."""

from __future__ import annotations

import unittest
from html.parser import HTMLParser
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_DIR = REPO_ROOT / "cczps_lite" / "dashboard"


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
        for path in (index_path, styles_path, script_path):
            self.assertTrue(path.is_file(), path)

        parser = DashboardHTMLParser()
        parser.feed(index_path.read_text(encoding="utf-8"))
        self.assertEqual(parser.scripts, ["dashboard.js"])
        self.assertEqual(parser.stylesheets, ["styles.css"])
        for section_id in (
            "overview",
            "comparison",
            "runtime-chain",
            "scenario-detail",
            "validation-report",
            "capability-map",
        ):
            self.assertIn(section_id, parser.ids)

    def test_dashboard_reads_existing_outputs_without_external_services(self) -> None:
        script = (DASHBOARD_DIR / "dashboard.js").read_text(encoding="utf-8")
        for path in (
            "../output/comparison_matrix.csv",
            "../../docs/CCZPS_LITE_SYSTEM_VALIDATION_REPORT.md",
            "../output/runtime_capability_map.md",
        ):
            self.assertIn(path, script)
        for forbidden in ("https://", "http://", "XMLHttpRequest", "WebSocket"):
            self.assertNotIn(forbidden, script)
        for scenario in ("batlow", "kunlun", "iraq", "baiyangdian"):
            self.assertIn(f"{scenario}:", script)


if __name__ == "__main__":
    unittest.main()
