import http.client
import json
import tempfile
import threading
import unittest
from pathlib import Path

from cczps_lite.scientist_runtime import RuntimeBoundaryError
from cczps_lite.scientist_runtime.server import create_server

ROOT = Path(__file__).resolve().parents[1]
STATIC = ROOT / "cczps_lite" / "scientist_runtime" / "static"


class ScientistRuntimeServerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.server = create_server(Path(self.temp.name) / "web.sqlite3", port=0)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self._stop)
        self.port = self.server.server_address[1]

    def _stop(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)

    def request(self, method, path, body=None, host="127.0.0.1"):
        connection = http.client.HTTPConnection("127.0.0.1", self.port, timeout=2)
        payload = None if body is None else json.dumps(body)
        headers = {"Host": host}
        if payload is not None:
            headers["Content-Type"] = "application/json"
        connection.request(method, path, payload, headers)
        response = connection.getresponse()
        data = response.read()
        connection.close()
        content_type = response.getheader("Content-Type", "")
        parsed = json.loads(data) if "application/json" in content_type else data.decode("utf-8")
        return response.status, parsed, response

    def test_health_and_html_are_local_and_explain_boundaries(self):
        status, health, response = self.request("GET", "/api/health")
        self.assertEqual(status, 200)
        self.assertTrue(health["localhost_only"])
        self.assertFalse(health["network_egress"])
        self.assertEqual(health["cost_aud"], 0)
        self.assertEqual(response.getheader("X-Frame-Options"), "DENY")
        status, html, _ = self.request("GET", "/")
        self.assertEqual(status, 200)
        for text in (
            "Human question", "AI-structured hypothesis", "Human approval gate",
            "Run receipt", "Human review", "Reject plan", "Save bounded revision",
            "Start revised session",
        ):
            self.assertIn(text, html)

    def test_http_hypothesis_revision_is_bounded_and_audited(self):
        question = "In this fictional offline test box, does a higher input produce a higher output score than baseline?"
        status, session, _ = self.request("POST", "/api/sessions", {"question": question})
        self.assertEqual(status, 201)
        session_id = session["session_id"]
        status, session, _ = self.request("POST", f"/api/sessions/{session_id}/propose", {})
        self.assertEqual(status, 200)
        hypothesis = session["object_graph"]["hypothesis"]
        hypothesis["revision_id"] = f'{hypothesis["hypothesis_id"]}-R2'
        hypothesis["hypothesis_statement"] = "For this fictional offline box, the higher fixed test input will produce a higher output score."
        status, revised, _ = self.request("POST", f"/api/sessions/{session_id}/revise", {
            "hypothesis": hypothesis,
            "reviewer_label": "Founder reviewer",
            "reason": "Clarify the statement without changing the fixed executor or fixture.",
        })
        self.assertEqual(status, 200)
        self.assertEqual(revised["state"], "HYPOTHESIS_PROPOSED")
        self.assertEqual(revised["object_graph"]["hypothesis"]["revision_id"], hypothesis["revision_id"])
        self.assertEqual(revised["audit_events"][-1]["event_type"], "HUMAN_HYPOTHESIS_REVISED")
        self.assertEqual(revised["object_graph"]["resource_ceiling"]["cost_aud"], 0)

    def test_complete_http_workflow(self):
        question = "In the fictional sealed scalar box, does the fixed perturbation increase the response index compared with baseline?"
        status, session, _ = self.request("POST", "/api/sessions", {"question": question, "session_label": "http-test"})
        self.assertEqual(status, 201)
        session_id = session["session_id"]
        for action, body, expected_state in (
            ("propose", {}, "HYPOTHESIS_PROPOSED"),
            ("decision", {"decision":"APPROVE","reviewer_label":"Human reviewer","reason":"Approve this exact local fictional fixture for HTTP workflow testing."}, "APPROVED_TO_RUN"),
            ("run", {}, "RUN_COMPLETED_QUARANTINED"),
            ("review", {"decision":"ACCEPT_RUNTIME_DEMO","reviewer_label":"Human reviewer","reason":"The HTTP workflow completed and remains non-environmental evidence."}, "REVIEWED_DEMO_ACCEPTED"),
        ):
            status, session, _ = self.request("POST", f"/api/sessions/{session_id}/{action}", body)
            self.assertEqual(status, 200)
            self.assertEqual(session["state"], expected_state)
        self.assertTrue(session["audit_chain_valid"])

    def test_host_body_and_transition_controls_refuse_invalid_requests(self):
        status, result, _ = self.request("GET", "/api/health", host="example.com")
        self.assertEqual(status, 400)
        self.assertEqual(result["error"], "localhost_only")
        status, result, _ = self.request("POST", "/api/sessions", {"unexpected": True})
        self.assertEqual(status, 400)
        self.assertEqual(result["error"], "ContractError")

    def test_server_refuses_non_local_bind(self):
        with self.assertRaises(RuntimeBoundaryError):
            create_server(Path(self.temp.name) / "bad.sqlite3", host="0.0.0.0", port=8765)

    def test_static_assets_do_not_call_external_services(self):
        source = "\n".join(path.read_text(encoding="utf-8") for path in STATIC.iterdir())
        for prohibited in ("https://", "http://", "WebSocket", "EventSource", "openai", "GraphCast"):
            self.assertNotIn(prohibited, source)


if __name__ == "__main__":
    unittest.main()
