import http.client
import json
import tempfile
import threading
import unittest
from pathlib import Path

from cczps_lite.environmental_question_runtime.server import create_server
from tests.test_environmental_question_runtime import QUESTION


class EnvironmentalQuestionRuntimeServerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.server = create_server(Path(self.temp.name) / "web.sqlite3", port=0)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True); self.thread.start()
        self.addCleanup(self._stop); self.port = self.server.server_address[1]

    def _stop(self):
        self.server.shutdown(); self.server.server_close(); self.thread.join(timeout=2)

    def request(self, method, path, body=None):
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=2)
        payload = None if body is None else json.dumps(body)
        conn.request(method, path, payload, {"Host": "127.0.0.1", "Content-Type": "application/json"})
        response = conn.getresponse(); raw = response.read(); kind = response.getheader("Content-Type", ""); conn.close()
        return response.status, json.loads(raw) if "json" in kind else raw.decode()

    def test_page_explains_real_plan_and_synthetic_run_boundary(self):
        status, html = self.request("GET", "/")
        self.assertEqual(status, 200)
        for text in ("question you actually care about", "Real-world evidence plan", "Human approval gate", "Run Receipt", "Evidence Passport"):
            self.assertIn(text, html)
        source = "".join((Path(__file__).parents[1] / "cczps_lite/environmental_question_runtime/static" / name).read_text() for name in ("index.html", "app.js", "styles.css"))
        for blocked in ("https://", "http://", "openai", "GraphCast", "WebSocket"):
            self.assertNotIn(blocked, source)

        program_source = "".join(
            (Path(__file__).parents[1] / "cczps_lite/environmental_question_runtime/static" / name).read_text()
            for name in ("program.html", "program.js")
        )
        self.assertIn("refreshStatus", program_source)
        self.assertIn('applyRefreshGate("REFRESH_IN_PROGRESS")', program_source)
        self.assertIn('$("compile").disabled=inProgress||retry', program_source)

    def test_health_truthfully_reports_manual_allowlisted_network_capability(self):
        status, health = self.request("GET", "/api/health")
        self.assertEqual(status, 200)
        self.assertTrue(health["network_egress"])
        self.assertEqual(health["network_egress_mode"], "manual_allowlisted_https_only")
        self.assertFalse(health["automatic_network_egress"])
        self.assertTrue(health["live_refresh_requires_human_approval"])
        self.assertFalse(health["raw_source_content_retained"])
        self.assertEqual(health["cost_aud"], 0)

    def test_http_flow_to_quarantined_result(self):
        status, session = self.request("POST", "/api/questions", {"question": QUESTION}); self.assertEqual(status, 201)
        sid = session["session_id"]
        status, session = self.request("POST", f"/api/sessions/{sid}/rehearsal", {}); self.assertEqual(status, 200)
        status, session = self.request("POST", f"/api/sessions/{sid}/decision", {"decision":"APPROVE","reviewer":"Human","reason":"Approve this exact fictional rehearsal only."}); self.assertEqual(status, 200)
        status, session = self.request("POST", f"/api/sessions/{sid}/run", {}); self.assertEqual(status, 200)
        self.assertEqual(session["passport"]["state"], "SUPPORTED_SYNTHETIC_ONLY")

    def test_persistent_program_http_flow_without_network(self):
        status, program = self.request("GET", "/api/programs/COOMA-WATER-FIRE-WASTEWATER-WATCH")
        self.assertEqual(status, 200)
        self.assertEqual(program["current_hypothesis_version"], 0)
        status, cycle = self.request("POST", "/api/programs/COOMA-WATER-FIRE-WASTEWATER-WATCH/cycles", {"year_month":"2026-07","trigger":"MONTHLY"})
        self.assertEqual(status, 201)
        cycle_id = cycle["cycle_id"]
        status, _ = self.request("POST", f"/api/cycles/{cycle_id}/observations", {
            "category":"WATER", "observed_on":"2026-07-18",
            "note":"The river appeared low from a public location; no measurement was taken.",
            "location_scope":"Cooma public area", "public_safe_confirmation":True,
        })
        self.assertEqual(status, 200)
        status, cycle = self.request("POST", f"/api/cycles/{cycle_id}/compile", {})
        self.assertEqual(status, 200)
        self.assertIsNone(cycle["hypothesis_version"]["environmental_conclusion"])
        status, reviewed = self.request("POST", f"/api/cycles/{cycle_id}/review", {
            "decision":"ACCEPT_CYCLE", "reviewer":"Founder reviewer",
            "reason":"Accept this as a monthly research record without an environmental signoff.",
        })
        self.assertEqual(status, 200)
        self.assertFalse(reviewed["human_review"]["environmental_signoff"])


if __name__ == "__main__":
    unittest.main()
