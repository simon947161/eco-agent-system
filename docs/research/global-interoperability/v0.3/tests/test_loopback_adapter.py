#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
import threading
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "adapter"))
from loopback_adapter import build_server  # noqa: E402

FIXTURE = json.loads((ROOT / "fixtures" / "synthetic_climateos_to_buildingos.json").read_text(encoding="utf-8"))


def request(base: str, path: str, body=None, content_type="application/json"):
    data = None if body is None else json.dumps(body).encode("utf-8")
    req = urllib.request.Request(base + path, data=data, headers={"Content-Type": content_type})
    try:
        with urllib.request.urlopen(req, timeout=3) as response:
            return response.status, json.loads(response.read())
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read())


def mutate(path: str, value, suffix: str | None = None):
    doc = copy.deepcopy(FIXTURE)
    node = doc
    parts = path.split(".")
    for part in parts[:-1]:
        node = node[part]
    node[parts[-1]] = value
    if suffix:
        doc["handoff_id"] = f"HO-SYN-NEG-{suffix}"
    return doc


def main() -> int:
    server = build_server(0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_port}"
    cases = []
    try:
        status, body = request(base, "/health")
        cases.append({"case": "health", "passed": status == 200 and body["network_scope"] == "LOOPBACK_ONLY"})
        status, body = request(base, "/capabilities")
        cases.append({"case": "capabilities", "passed": status == 200 and body["synthetic_only"] is True})
        status, openapi_receipt = request(base, "/v0.3/handoffs", FIXTURE)
        cases.append({"case": "openapi_handoff", "passed": status == 200 and openapi_receipt["status"] == "ACCEPTED"})
        mcp = {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "ggg.handoff_evidence.v0_3", "arguments": FIXTURE}}
        status, mcp_body = request(base, "/mcp", mcp)
        mcp_receipt = mcp_body.get("result", {}).get("structuredContent", {})
        cases.append({"case": "mcp_same_contract", "passed": status == 200 and mcp_receipt.get("envelope_sha256") == openapi_receipt["envelope_sha256"]})
        status, body = request(base, "/v0.3/handoffs", mutate("evidence_state", "OBSERVED", "REAL"))
        cases.append({"case": "block_real_state", "passed": "REAL_DATA_NOT_AUTHORIZED" in body.get("reasons", [])})
        status, body = request(base, "/v0.3/handoffs", mutate("authority.decision_authorized", True, "AUTH"))
        cases.append({"case": "block_decision_authority", "passed": "DECISION_AUTHORITY_NOT_BOUNDED" in body.get("reasons", [])})
        status, body = request(base, "/v0.3/handoffs", mutate("privacy_boundary.private_person_assets_included", True, "PRIVACY"))
        cases.append({"case": "block_private_assets", "passed": "PRIVATE_ASSET_BOUNDARY_BREACH" in body.get("reasons", [])})
        status, body = request(base, "/v0.3/handoffs", mutate("governance.child_capabilities", ["read_fixture", "send_external_message"], "CAP"))
        cases.append({"case": "block_capability_escalation", "passed": "CHILD_CAPABILITY_ESCALATION" in body.get("reasons", [])})
        protected = mutate("governance.protected_write_requested", True, "WRITE")
        status, body = request(base, "/v0.3/handoffs", protected)
        cases.append({"case": "block_unapproved_protected_write", "passed": "PROTECTED_WRITE_APPROVAL_MISSING" in body.get("reasons", [])})
        conflict = mutate("payload.confidence", "CHANGED")
        status, body = request(base, "/v0.3/handoffs", conflict)
        cases.append({"case": "block_idempotency_conflict", "passed": status == 409 and "IDEMPOTENCY_CONFLICT" in body.get("reasons", [])})
        status, body = request(base, "/v0.3/handoffs", FIXTURE, "text/plain")
        cases.append({"case": "block_wrong_content_type", "passed": status == 415 and body.get("error") == "CONTENT_TYPE_NOT_ALLOWED"})
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=3)
    passed = sum(case["passed"] for case in cases)
    report = {
        "prototype": "GGG local loopback adapter v0.3",
        "binding": "127.0.0.1 only",
        "interfaces": ["OpenAPI HTTP", "MCP JSON-RPC"],
        "total_cases": len(cases),
        "passed": passed,
        "failed": len(cases) - passed,
        "result": "PASS" if passed == len(cases) else "FAIL",
        "real_data": False,
        "external_action": False,
        "mainline_write": False,
        "private_person_assets": False,
        "cases": cases,
    }
    output = ROOT / "evidence" / "LOOPBACK_TEST_RESULT_v0.3.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
