"""Risk-oriented Bridge verification using only isolated temporary fixtures."""
import copy
import http.client
import json
import sqlite3
import tempfile
import threading
import unittest
from pathlib import Path

from cczps_lite.council_bridge.contracts import BridgeError, digest
from cczps_lite.council_bridge.fixtures import council_fixture
from cczps_lite.council_bridge.runtime import CouncilBridge, Principal, ALL_PERMISSIONS
from cczps_lite.council_bridge.server import make_server


class CouncilBridgeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.now = "2026-10-21T00:00:00Z"
        self.configs = [council_fixture(), council_fixture("other-council", "Fictional other Council")]
        self.bridge = CouncilBridge(self.tmp.name, self.configs, clock=lambda: self.now)
        self.a = Principal(self.configs[0]["council_id"], ALL_PERMISSIONS)
        self.b = Principal(self.configs[1]["council_id"], ALL_PERMISSIONS)

    def tearDown(self):
        self.tmp.cleanup()

    def completed(self, provider="mock-local"):
        request = self.bridge.prepare_request(self.a)
        self.bridge.submit(self.a, request, provider)
        self.bridge.progress(self.a, request["request_id"])
        return request

    def release(self):
        preview = self.bridge.preview(self.a)
        self.bridge.approve_release(self.a, preview["digest"])
        return preview

    def test_end_to_end_existing_answer_shape_and_synthetic_ceiling(self):
        request = self.completed()
        answer = self.bridge.assess(self.a, request["request_id"])
        schema = json.loads((Path(__file__).parents[1] / "schemas/climateos_v2/time_bounded_environmental_answer.schema.json").read_text())
        self.assertTrue(set(schema["required"]) <= answer.keys())
        self.assertEqual((answer["conclusion_level"], answer["evidence_maturity"]), ("L0", "S0"))
        self.assertEqual(answer["human_review"]["status"], "PENDING_HUMAN_REVIEW")
        self.bridge.review(self.a, answer["answer_id"], "ACCEPT_DEMO")
        self.bridge.observe(self.a, answer["answer_id"])
        snapshot = self.bridge.snapshot(self.a)
        self.assertTrue(snapshot["audit_consistent"])
        self.assertFalse(snapshot["assessments"][0]["human_review"]["scientific_signoff"])
        self.assertEqual(len(snapshot["outcomes"]), 1)
        self.assertEqual(len(snapshot["assessments"]), 1)

    def test_node_isolation_and_scope_permissions(self):
        request = self.completed()
        with self.assertRaises(BridgeError):
            self.bridge.progress(self.b, request["request_id"])
        with self.assertRaises(BridgeError):
            self.bridge.submit(self.b, request)
        with self.assertRaises(BridgeError):
            self.bridge.prepare_request(Principal(self.a.council_id, frozenset({"read"})))
        with self.assertRaises(BridgeError):
            self.bridge.snapshot(Principal("../escape", ALL_PERMISSIONS))
        self.assertFalse(self.bridge.snapshot(self.b)["jobs"])
        self.assertEqual(len(list(Path(self.tmp.name).glob("*/bridge.sqlite3"))), 2)

    def test_compute_contract_rejects_mismatch_and_unbound_approval(self):
        request = self.bridge.prepare_request(self.a)
        for key, value in [("unit", "K"), ("period_end", request["period_start"]), ("model_version", "real-model"),
                           ("budget_aud", 10), ("budget_aud", True), ("data_classification", "OBSERVATION"),
                           ("spatial_ids", ["external-place"]), ("input_digest", "fake")]:
            bad = copy.deepcopy(request)
            bad[key] = value
            bad["approval_digest"] = digest({k: v for k, v in bad.items() if k != "approval_digest"})
            with self.subTest(field=key, value=value), self.assertRaises(BridgeError):
                self.bridge.submit(self.a, bad)
        bad = copy.deepcopy(request)
        bad["period_end"] = "2026-10-30T00:00:00Z"
        with self.assertRaises(BridgeError):
            self.bridge.submit(self.a, bad)
        self.assertFalse(self.bridge.snapshot(self.a)["jobs"])

    def test_idempotence_and_collision(self):
        request = self.bridge.prepare_request(self.a)
        first = self.bridge.submit(self.a, request)
        self.assertEqual(first, self.bridge.submit(self.a, request))
        bad = copy.deepcopy(request)
        bad["request_id"] += "-new"
        bad["approval_digest"] = digest({k: v for k, v in bad.items() if k != "approval_digest"})
        with self.assertRaises(BridgeError):
            self.bridge.submit(self.a, bad)
        self.assertEqual(len(self.bridge.snapshot(self.a)["jobs"]), 1)

    def test_timeout_retry_cap_failure_cancel_and_duplicate_response(self):
        request = self.bridge.prepare_request(self.a)
        rid = request["request_id"]
        self.bridge.submit(self.a, request)
        self.assertEqual(self.bridge.progress(self.a, rid, mode="timeout")["status"], "TIMED_OUT")
        self.bridge.progress(self.a, rid, action="retry")
        self.assertEqual(self.bridge.progress(self.a, rid, mode="failure")["status"], "FAILED")
        self.bridge.progress(self.a, rid, action="retry")
        final = self.bridge.progress(self.a, rid)
        self.assertEqual(self.bridge.progress(self.a, rid), final)
        self.assertEqual(final["attempts"], 3)
        with self.assertRaises(BridgeError):
            self.bridge.progress(self.a, rid, action="retry")
        second = self.bridge.prepare_request(self.a)
        self.bridge.submit(self.a, second)
        self.assertEqual(self.bridge.progress(self.a, second["request_id"], action="cancel")["status"], "CANCELLED")
        with self.assertRaises(BridgeError):
            self.bridge.progress(self.a, second["request_id"])

    def test_incompatible_result_rolls_back_and_can_recover(self):
        request = self.bridge.prepare_request(self.a)
        self.bridge.submit(self.a, request)
        with self.assertRaises(BridgeError):
            self.bridge.progress(self.a, request["request_id"], mode="incompatible")
        job = self.bridge.snapshot(self.a)["jobs"][request["request_id"]]
        self.assertEqual(job["status"], "QUEUED")
        self.assertIsNone(job["result"])
        self.bridge.progress(self.a, request["request_id"])

    def test_supplier_replacement_and_matrix_one_denial(self):
        request = self.completed("mock-alternate")
        self.assertEqual(self.bridge.snapshot(self.a)["jobs"][request["request_id"]]["provider_id"], "mock-alternate")
        with self.assertRaises(BridgeError):
            self.bridge.submit(self.a, self.bridge.prepare_request(self.a), "matrix-one-unverified")

    def test_review_permission_and_no_scientific_promotion(self):
        request = self.completed()
        answer = self.bridge.assess(self.a, request["request_id"])
        with self.assertRaises(BridgeError):
            self.bridge.review(Principal(self.a.council_id, frozenset({"read"})), answer["answer_id"], "ACCEPT_DEMO")
        with self.assertRaises(BridgeError):
            self.bridge.review(self.a, answer["answer_id"], "SCIENTIFIC_SIGNOFF")
        self.bridge.review(self.a, answer["answer_id"], "REJECT_DEMO")
        with self.assertRaises(BridgeError):
            self.bridge.observe(self.a, answer["answer_id"])

    def test_expiry_blocks_compute_review_export_and_marks_import(self):
        request = self.completed()
        answer = self.bridge.assess(self.a, request["request_id"])
        release = self.release()
        self.bridge.import_release(self.b, self.a, release["digest"])
        self.now = "2026-11-01T00:00:00Z"
        with self.assertRaises(BridgeError):
            self.bridge.submit(self.a, self.bridge.prepare_request(self.a))
        with self.assertRaises(BridgeError):
            self.bridge.review(self.a, answer["answer_id"], "ACCEPT_DEMO")
        with self.assertRaises(BridgeError):
            self.bridge.export(self.a, release["digest"])
        self.assertEqual(self.bridge.snapshot(self.a)["assessments"][0]["display_state"], "EXPIRED")
        self.assertEqual(self.bridge.sync_imports(self.b)[release["digest"]]["status"], "EXPIRED")

    def test_preview_approval_export_and_no_private_content(self):
        preview = self.bridge.preview(self.a)
        with self.assertRaises(BridgeError):
            self.bridge.export(self.a, preview["digest"])
        with self.assertRaises(BridgeError):
            self.bridge.approve_release(self.a, "wrong-preview")
        self.bridge.approve_release(self.a, preview["digest"])
        exported = self.bridge.export(self.a, preview["digest"])
        encoded = json.dumps(exported)
        for forbidden in ("private_notes", "LOCAL ONLY", '"value"', '"geometry"', '"source"'):
            self.assertNotIn(forbidden, encoded)
        self.assertEqual(digest(exported), preview["digest"])

    def test_withdrawal_propagates_without_rewriting_old_answer(self):
        request = self.completed()
        answer = self.bridge.assess(self.a, request["request_id"])
        release = self.release()
        self.bridge.import_release(self.b, self.a, release["digest"])
        self.bridge.import_release(self.b, self.a, release["digest"])
        self.assertEqual(len(self.bridge.snapshot(self.b)["imports"]), 1)
        self.bridge.withdraw(self.a, self.a.council_id + "-e1")
        self.assertEqual(self.bridge.sync_imports(self.b)[release["digest"]]["status"], "WITHDRAWN_AT_SOURCE")
        self.assertEqual(self.bridge.snapshot(self.a)["assessments"][0]["answer"], answer["answer"])
        self.assertEqual(self.bridge.snapshot(self.a)["assessments"][0]["display_state"], "WITHDRAWN_EVIDENCE_REVIEW_REQUIRED")
        with self.assertRaises(BridgeError):
            self.bridge.export(self.a, release["digest"])
        with self.assertRaises(BridgeError):
            self.bridge.approve_release(self.a, release["digest"])

    def test_restart_preserves_state_and_detects_tampering(self):
        request = self.completed()
        restarted = CouncilBridge(self.tmp.name, self.configs, clock=lambda: self.now)
        self.assertIn(request["request_id"], restarted.snapshot(self.a)["jobs"])
        db = Path(self.tmp.name) / self.a.council_id / "bridge.sqlite3"
        with sqlite3.connect(db) as con:
            body = json.loads(con.execute("SELECT body FROM state").fetchone()[0])
            body["evidence"][0]["value"] = 999
            con.execute("UPDATE state SET body=?", (json.dumps(body),))
        con.close()
        self.assertFalse(restarted.snapshot(self.a)["audit_consistent"])
        with self.assertRaises(BridgeError):
            restarted.submit(self.a, restarted.prepare_request(self.a))

    def test_config_keeps_boundary_and_resources_distinct(self):
        config = self.configs[0]
        kinds = {o["kind"] for o in config["objects"]}
        self.assertTrue({"ADMINISTRATIVE", "CATCHMENT", "SITE", "SERVICE_AREA", "CLIMATE_GRID"} <= kinds)
        self.assertIsNone(config["boundary"]["geometry"])
        self.assertTrue(any(o["id"].endswith("-farm") for o in config["objects"]))


class BridgeHTTPTests(unittest.TestCase):
    setUp = CouncilBridgeTests.setUp
    tearDown = CouncilBridgeTests.tearDown

    def test_session_host_origin_and_unknown_scope(self):
        server, token = make_server(self.bridge, 0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        port = server.server_port
        def request(method, path, body=None, **headers):
            con = http.client.HTTPConnection("127.0.0.1", port, timeout=3)
            con.request(method, path, body=body, headers=headers)
            response = con.getresponse()
            data = response.read()
            result = (response.status, data, dict(response.getheaders()))
            con.close()
            return result
        try:
            self.assertEqual(request("GET", "/api/state")[0], 401)
            self.assertEqual(request("GET", "/", Host="evil.example")[0], 400)
            headers = {"Authorization": "Bearer " + token, "X-Council-ID": self.a.council_id, "Content-Type": "application/json"}
            self.assertEqual(request("POST", "/api/prepare", "{}", **headers)[0], 403)
            headers["Origin"] = f"http://127.0.0.1:{port}"
            self.assertEqual(request("POST", "/api/prepare", "{}", **headers)[0], 200)
            headers["X-Council-ID"] = "../escape"
            self.assertEqual(request("GET", "/api/state", **headers)[0], 400)
            headers["X-Council-ID"] = self.a.council_id
            self.assertEqual(request("POST", "/api/prepare", "[]", **headers)[0], 400)
            status, html, response_headers = request("GET", "/")
            self.assertEqual(status, 200)
            self.assertNotIn(token.encode(), html)
            self.assertIn("frame-ancestors 'none'", response_headers["Content-Security-Policy"])
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=3)


if __name__ == "__main__":
    unittest.main()
