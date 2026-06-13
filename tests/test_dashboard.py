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
        super().__init__(); self.ids=set(); self.scripts=[]; self.stylesheets=[]
    def handle_starttag(self, tag, attrs) -> None:
        attributes=dict(attrs)
        if attributes.get("id"): self.ids.add(str(attributes["id"]))
        if tag=="script" and attributes.get("src"): self.scripts.append(str(attributes["src"]))
        if tag=="link" and attributes.get("rel")=="stylesheet": self.stylesheets.append(str(attributes.get("href", "")))


class DemonstrationDashboardTests(unittest.TestCase):
    def test_dashboard_assets_and_sections_exist(self) -> None:
        assets=[DASHBOARD_DIR/name for name in ("index.html","styles.css","planning-hypothesis-dashboard.css","dashboard.js","usage-cost-dashboard.js","budget-guard-dashboard.js","meteorology-dashboard.js","planning-hypothesis-dashboard.js","governance-decision-dashboard.js")]
        for path in assets: self.assertTrue(path.is_file(), path)
        parser=DashboardHTMLParser(); parser.feed(assets[0].read_text(encoding="utf-8"))
        self.assertEqual(parser.scripts,["dashboard.js","usage-cost-dashboard.js","budget-guard-dashboard.js","meteorology-dashboard.js","planning-hypothesis-dashboard.js","governance-decision-dashboard.js"])
        self.assertEqual(parser.stylesheets,["styles.css","planning-hypothesis-dashboard.css"])
        for section_id in ("overview","comparison","runtime-chain","scenario-detail","usage-cost","budget-guard","meteorology","planning-hypothesis","planning-hypotheses","governance-decision","governance-decision-support","validation-report","capability-map"):
            self.assertIn(section_id,parser.ids)
        self.assertIn("meteorology-trends", parser.ids)

    def test_dashboard_reads_existing_outputs_without_external_services(self) -> None:
        script=(DASHBOARD_DIR/"dashboard.js").read_text(encoding="utf-8")
        for path in ("../output/comparison_matrix.csv","../../docs/CCZPS_LITE_SYSTEM_VALIDATION_REPORT.md","../output/runtime_capability_map.md"): self.assertIn(path,script)
        for forbidden in ("https://","http://","XMLHttpRequest","WebSocket"): self.assertNotIn(forbidden,script)
        usage=(DASHBOARD_DIR/"usage-cost-dashboard.js").read_text(encoding="utf-8")
        for field in ("usage_mode","external_resource_owner","estimated_external_resource_cost","agentic_consumption_risk"): self.assertIn(field,usage)
        budget=(DASHBOARD_DIR/"budget-guard-dashboard.js").read_text(encoding="utf-8")
        for field in ("budget_status","daily_call_limit","estimated_calls","requires_manual_confirmation"): self.assertIn(field,budget)
        meteorology=(DASHBOARD_DIR/"meteorology-dashboard.js").read_text(encoding="utf-8")
        self.assertIn("../output/meteorology_evidence.json",meteorology)
        self.assertIn("../output/meteorology_trends.json",meteorology)
        self.assertNotIn("power.larc.nasa.gov",meteorology)
        for forbidden in ("https://", "http://", "XMLHttpRequest", "WebSocket"):
            self.assertNotIn(forbidden, meteorology)
        hypotheses=(DASHBOARD_DIR/"planning-hypothesis-dashboard.js").read_text(encoding="utf-8")
        self.assertIn("../output/planning_hypotheses.json", hypotheses)
        for field in ("hypothesis_status", "problem_statement", "planning_assumption", "intervention_logic", "expected_effect", "validation_indicators", "failure_conditions", "human_review_required"):
            self.assertIn(field, hypotheses)
        for forbidden in ("https://", "http://", "XMLHttpRequest", "WebSocket", "OpenAI", "anthropic", "power.larc.nasa.gov"):
            self.assertNotIn(forbidden, hypotheses)
        governance=(DASHBOARD_DIR/"governance-decision-dashboard.js").read_text(encoding="utf-8")
        self.assertIn("../output/governance_decision_records.json", governance)
        for field in ("internal_decision_status", "external_approval_status", "evidence_trace_ids", "human_review_required", "professional_review_required"):
            self.assertIn(field, governance)
        for forbidden in ("https://", "http://", "XMLHttpRequest", "WebSocket", "OpenAI", "anthropic"):
            self.assertNotIn(forbidden, governance)

    def test_meteorology_panel_exposes_observation_and_governance_fields(self) -> None:
        meteorology=(DASHBOARD_DIR/"meteorology-dashboard.js").read_text(encoding="utf-8")
        for field in ("temperature_c", "rainfall_mm", "humidity_percent", "wind_speed_kmh", "wind_direction_degrees", "solar_radiation_mj_m2", "from_cache", "budget_guard_status", "observation_date"):
            self.assertIn(field, meteorology)
        for status in ("success", "blocked_by_budget_guard", "missing_data", "retrieval_failed", "not_retrieved"):
            self.assertIn(status, meteorology)
        self.assertIn("Not available", meteorology)
        for field in ("trend_classification", "sample_count", "observation_window"):
            self.assertIn(field, meteorology)

    def test_github_pages_workflow_stages_a_self_contained_site(self) -> None:
        workflow=PAGES_WORKFLOW.read_text(encoding="utf-8")
        for expected in ("python cczps_lite/engine/meteorology_runtime.py","python cczps_lite/engine/planning_hypothesis.py","python cczps_lite/engine/evidence_traceability.py","python cczps_lite/engine/governance_decision_support.py","data/meteorology_evidence.json","data/meteorology_trends.json","data/planning_hypotheses.json","data/governance_decision_records.json","_site/meteorology-dashboard.js","_site/planning-hypothesis-dashboard.js","_site/governance-decision-dashboard.js","actions/deploy-pages@v4"):
            self.assertIn(expected,workflow)


if __name__ == "__main__": unittest.main()
