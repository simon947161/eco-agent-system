#!/usr/bin/env python3
"""Bounded localhost-only OpenAPI/MCP adapter for GGG synthetic handoffs."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

ADAPTER_VERSION = "ggg-loopback-adapter-v0.3"
CONTRACT_VERSION = "ggg-transport-v0.2"
MAX_BODY_BYTES = 262_144
SYSTEMS = {"MISSION_CONTROL", "CLIMATEOS", "CARBONOS", "BUILDINGOS", "ECOCHAIN", "GEGG"}
ROUTES = {
    ("CLIMATEOS", "BUILDINGOS", "EvidenceObject"),
    ("BUILDINGOS", "ECOCHAIN", "DomainClaim"),
    ("ECOCHAIN", "MISSION_CONTROL", "RegistrySubmission"),
}
REQUIRED = {
    "contract_version", "handoff_id", "correlation_id", "object_id", "object_type",
    "source_system", "target_system", "evidence_state", "synthetic", "authority",
    "provenance", "boundaries", "measurement", "transformations", "uncertainty",
    "limitations", "permitted_use", "governance", "privacy_boundary", "payload",
}


def canonical_bytes(doc: dict[str, Any]) -> bytes:
    return json.dumps(doc, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def validate_envelope(doc: Any) -> list[str]:
    if not isinstance(doc, dict):
        return ["ENVELOPE_MUST_BE_OBJECT"]
    errors: list[str] = []
    missing = REQUIRED - set(doc)
    if missing:
        return ["MISSING_REQUIRED_FIELDS:" + ",".join(sorted(missing))]
    if set(doc) - REQUIRED:
        errors.append("UNDECLARED_TOP_LEVEL_FIELDS")
    if doc["contract_version"] != CONTRACT_VERSION:
        errors.append("INVALID_CONTRACT_VERSION")
    if not isinstance(doc["handoff_id"], str) or not re.fullmatch(r"HO-[A-Z0-9-]{3,80}", doc["handoff_id"]):
        errors.append("INVALID_HANDOFF_ID")
    if doc["source_system"] not in SYSTEMS or doc["target_system"] not in SYSTEMS:
        errors.append("INVALID_SYSTEM")
    if doc["evidence_state"] != "SYNTHETIC" or doc.get("synthetic") is not True:
        errors.append("REAL_DATA_NOT_AUTHORIZED")
    if (doc["source_system"], doc["target_system"], doc["object_type"]) not in ROUTES:
        errors.append("ROUTE_OR_OBJECT_AUTHORITY_MISMATCH")
    authority = doc.get("authority", {})
    if authority.get("decision_authorized") is not False:
        errors.append("DECISION_AUTHORITY_NOT_BOUNDED")
    provenance = doc.get("provenance", {})
    if not re.fullmatch(r"[a-f0-9]{64}", provenance.get("sha256", "")):
        errors.append("INVALID_SOURCE_HASH")
    if not doc.get("limitations") or not doc.get("uncertainty"):
        errors.append("UNCERTAINTY_OR_LIMITATIONS_REMOVED")
    governance = doc.get("governance", {})
    if not set(governance.get("child_capabilities", [])) <= set(governance.get("parent_capabilities", [])):
        errors.append("CHILD_CAPABILITY_ESCALATION")
    if governance.get("protected_write_requested") and not governance.get("protected_write_approval_present"):
        errors.append("PROTECTED_WRITE_APPROVAL_MISSING")
    if governance.get("external_action_authorized") is not False:
        errors.append("EXTERNAL_ACTION_NOT_BOUNDED")
    privacy = doc.get("privacy_boundary", {})
    if any(privacy.get(k) is not False for k in (
        "private_person_assets_included", "biometric_assets_included", "personal_os_connected"
    )):
        errors.append("PRIVATE_ASSET_BOUNDARY_BREACH")
    if doc["source_system"] == "ECOCHAIN" and doc.get("payload", {}).get("truth_status_upgraded") is not False:
        errors.append("REGISTRY_TRUTH_UPGRADE_FORBIDDEN")
    return sorted(set(errors))


class AdapterState:
    def __init__(self) -> None:
        self.receipts: dict[str, tuple[str, dict[str, Any]]] = {}

    def handoff(self, doc: dict[str, Any]) -> tuple[int, dict[str, Any]]:
        errors = validate_envelope(doc)
        digest = hashlib.sha256(canonical_bytes(doc)).hexdigest()
        handoff_id = doc.get("handoff_id", "HO-INVALID")
        prior = self.receipts.get(handoff_id)
        if prior and prior[0] != digest:
            errors = sorted(set(errors + ["IDEMPOTENCY_CONFLICT"]))
        receipt = {
            "receipt_version": "ggg-receipt-v0.3",
            "adapter_version": ADAPTER_VERSION,
            "handoff_id": handoff_id,
            "correlation_id": doc.get("correlation_id"),
            "receiver": doc.get("target_system"),
            "status": "REJECTED" if errors else "ACCEPTED",
            "envelope_sha256": digest,
            "evidence_state_preserved": doc.get("evidence_state") == "SYNTHETIC",
            "authority_preserved": not any(e in errors for e in (
                "ROUTE_OR_OBJECT_AUTHORITY_MISMATCH", "DECISION_AUTHORITY_NOT_BOUNDED",
                "CHILD_CAPABILITY_ESCALATION", "PRIVATE_ASSET_BOUNDARY_BREACH",
            )),
            "external_action": False,
            "mainline_write": False,
            "network_scope": "LOOPBACK_ONLY",
            "reasons": errors,
        }
        if not errors and prior is None:
            self.receipts[handoff_id] = (digest, receipt)
        return (409 if "IDEMPOTENCY_CONFLICT" in errors else 200), receipt


class LoopbackHandler(BaseHTTPRequestHandler):
    server_version = ADAPTER_VERSION

    def log_message(self, _format: str, *_args: Any) -> None:
        return

    def _json(self, status: int, body: dict[str, Any]) -> None:
        encoded = json.dumps(body, ensure_ascii=False, sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(encoded)

    def _body(self) -> tuple[Any | None, str | None]:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            return None, "INVALID_CONTENT_LENGTH"
        if length <= 0 or length > MAX_BODY_BYTES:
            return None, "BODY_SIZE_NOT_ALLOWED"
        try:
            return json.loads(self.rfile.read(length).decode("utf-8")), None
        except (UnicodeDecodeError, json.JSONDecodeError):
            return None, "INVALID_JSON"

    def do_GET(self) -> None:
        if self.path == "/health":
            self._json(200, {"status": "ok", "adapter_version": ADAPTER_VERSION, "network_scope": "LOOPBACK_ONLY"})
        elif self.path == "/capabilities":
            self._json(200, {
                "interfaces": ["OPENAPI_HTTP", "MCP_JSON_RPC"],
                "contract_version": CONTRACT_VERSION,
                "synthetic_only": True,
                "external_action": False,
                "mainline_write": False,
                "private_person_assets": False,
            })
        else:
            self._json(404, {"error": "NOT_FOUND"})

    def do_POST(self) -> None:
        content_type = self.headers.get("Content-Type", "").split(";", 1)[0].strip()
        if content_type != "application/json":
            self._json(415, {"error": "CONTENT_TYPE_NOT_ALLOWED"})
            return
        body, error = self._body()
        if error:
            self._json(400, {"error": error})
            return
        state: AdapterState = self.server.adapter_state  # type: ignore[attr-defined]
        if self.path == "/v0.3/handoffs":
            status, receipt = state.handoff(body)
            self._json(status, receipt)
        elif self.path == "/mcp":
            self._mcp(body, state)
        else:
            self._json(404, {"error": "NOT_FOUND"})

    def _mcp(self, request: dict[str, Any], state: AdapterState) -> None:
        request_id = request.get("id")
        method = request.get("method")
        if request.get("jsonrpc") != "2.0":
            self._json(200, {"jsonrpc": "2.0", "id": request_id, "error": {"code": -32600, "message": "Invalid Request"}})
            return
        if method == "tools/list":
            result = {"tools": [{
                "name": "ggg.handoff_evidence.v0_3",
                "description": "Validate one bounded synthetic cross-OS handoff on localhost.",
                "inputSchema": {"type": "object"},
            }]}
        elif method == "tools/call" and request.get("params", {}).get("name") == "ggg.handoff_evidence.v0_3":
            _status, receipt = state.handoff(request.get("params", {}).get("arguments", {}))
            result = {"content": [{"type": "text", "text": json.dumps(receipt, sort_keys=True)}], "structuredContent": receipt, "isError": receipt["status"] == "REJECTED"}
        else:
            self._json(200, {"jsonrpc": "2.0", "id": request_id, "error": {"code": -32601, "message": "Method not found"}})
            return
        self._json(200, {"jsonrpc": "2.0", "id": request_id, "result": result})


def build_server(port: int = 8787) -> ThreadingHTTPServer:
    server = ThreadingHTTPServer(("127.0.0.1", port), LoopbackHandler)
    server.adapter_state = AdapterState()  # type: ignore[attr-defined]
    return server


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8787)
    args = parser.parse_args()
    server = build_server(args.port)
    print(json.dumps({"status": "ready", "url": f"http://127.0.0.1:{server.server_port}", "adapter_version": ADAPTER_VERSION}))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
