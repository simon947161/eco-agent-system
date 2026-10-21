"""Loopback-only, session-capability UI. Never a production Council endpoint."""
from __future__ import annotations

import json
import secrets
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from .contracts import BridgeError, canonical_json
from .runtime import Principal, ALL_PERMISSIONS

STATIC = Path(__file__).parent / "static"


def make_server(bridge, port=8767):
    token = secrets.token_urlsafe(32)

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass  # Do not log capability headers or request bodies.

        def send(self, status, data, kind="application/json; charset=utf-8"):
            body = data if isinstance(data, bytes) else canonical_json(data).encode()
            self.send_response(status)
            for k, v in {"Content-Type": kind, "Content-Length": str(len(body)), "Cache-Control": "no-store",
                         "X-Content-Type-Options": "nosniff", "X-Frame-Options": "DENY", "Referrer-Policy": "no-referrer",
                         "Content-Security-Policy": "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'"}.items():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(body)

        def host_ok(self):
            expected = {f"127.0.0.1:{self.server.server_port}", f"localhost:{self.server.server_port}"}
            return self.headers.get("Host") in expected

        def authorized(self):
            return secrets.compare_digest(self.headers.get("Authorization", ""), "Bearer " + token)

        def principal(self, permission):
            cid = self.headers.get("X-Council-ID", "")
            if cid not in bridge.configs:
                raise BridgeError("Council not configured")
            # The session capability represents this one local operator. Network
            # accounts, delegated reviewers and independent sign-off are absent.
            return Principal(cid, ALL_PERMISSIONS)

        def do_GET(self):
            if not self.host_ok():
                self.send(400, {"error": "invalid host"}); return
            path = urlsplit(self.path).path
            if path in {"/", "/app.js", "/styles.css"}:
                name = "index.html" if path == "/" else path[1:]
                kind = {"index.html": "text/html", "app.js": "text/javascript", "styles.css": "text/css"}[name]
                self.send(200, (STATIC / name).read_bytes(), kind + "; charset=utf-8"); return
            if not self.authorized():
                self.send(401, {"error": "local session capability required"}); return
            try:
                if path == "/api/councils":
                    data = [{"id": cid, "name": c["name"]} for cid, c in bridge.configs.items()]
                elif path == "/api/state":
                    data = bridge.snapshot(self.principal("read"))
                elif path == "/api/preview":
                    data = bridge.preview(self.principal("publish"))
                else:
                    self.send(404, {"error": "not found"}); return
                self.send(200, data)
            except BridgeError as exc:
                self.send(400, {"error": str(exc)})

        def do_POST(self):
            if not self.host_ok():
                self.send(400, {"error": "invalid host"}); return
            if not self.authorized():
                self.send(401, {"error": "local session capability required"}); return
            origin = self.headers.get("Origin")
            if origin not in {f"http://127.0.0.1:{self.server.server_port}", f"http://localhost:{self.server.server_port}"}:
                self.send(403, {"error": "same-origin request required"}); return
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if not 1 <= length <= 16384 or self.headers.get_content_type() != "application/json":
                    raise BridgeError("small JSON object required")
                payload = json.loads(self.rfile.read(length))
                if not isinstance(payload, dict):
                    raise BridgeError("JSON object required")
                action = urlsplit(self.path).path
                p = self.principal("read")
                if action == "/api/prepare":
                    result = bridge.prepare_request(p)
                elif action == "/api/submit":
                    result = bridge.submit(p, payload["request"], payload.get("provider", "mock-local"))
                elif action == "/api/progress":
                    result = bridge.progress(p, payload["request_id"], payload.get("action", "poll"), payload.get("mode", "success"))
                elif action == "/api/assess":
                    result = bridge.assess(p, payload["request_id"])
                elif action == "/api/review":
                    result = bridge.review(p, payload["answer_id"], payload["decision"])
                elif action == "/api/observe":
                    result = bridge.observe(p, payload["answer_id"])
                elif action == "/api/approve":
                    result = bridge.approve_release(p, payload["digest"])
                elif action == "/api/export":
                    result = bridge.export(p, payload["digest"])
                elif action == "/api/import":
                    source = Principal(payload["source_council"], ALL_PERMISSIONS)
                    result = bridge.import_release(p, source, payload["digest"])
                elif action == "/api/withdraw":
                    result = bridge.withdraw(p, payload["evidence_id"])
                elif action == "/api/sync":
                    result = bridge.sync_imports(p)
                else:
                    self.send(404, {"error": "unknown action"}); return
                self.send(200, result)
            except (BridgeError, ValueError, KeyError, TypeError) as exc:
                self.send(400, {"error": str(exc)})

    return ThreadingHTTPServer(("127.0.0.1", port), Handler), token
