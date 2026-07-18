"""Localhost Web adapter for the meaningful environmental question Runtime."""

from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from .runtime import EnvironmentalQuestionRuntime, RuntimeBoundaryError, RuntimeStateError

STATIC = Path(__file__).resolve().parent / "static"
ALLOWED_HOSTS = {"127.0.0.1", "localhost"}


def build_handler(runtime: EnvironmentalQuestionRuntime):
    class Handler(BaseHTTPRequestHandler):
        def _send(self, status: int, payload: bytes, content_type: str) -> None:
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Frame-Options", "DENY")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(payload)

        def _json(self, status: int, value: object) -> None:
            self._send(status, json.dumps(value, ensure_ascii=False).encode(), "application/json; charset=utf-8")

        def _parts(self) -> list[str]:
            return [part for part in urlparse(self.path).path.split("/") if part]

        def _host_ok(self) -> bool:
            return self.headers.get("Host", "").split(":", 1)[0].casefold() in ALLOWED_HOSTS

        def _body(self) -> dict:
            try:
                length = int(self.headers.get("Content-Length", "0"))
            except ValueError as exc:
                raise RuntimeBoundaryError("invalid request length") from exc
            if not 1 <= length <= 65536:
                raise RuntimeBoundaryError("request body must be 1..65536 bytes")
            value = json.loads(self.rfile.read(length).decode())
            if not isinstance(value, dict):
                raise RuntimeBoundaryError("request body must be an object")
            return value

        def do_GET(self) -> None:
            if not self._host_ok():
                self._json(400, {"error": "localhost_only"}); return
            parts = self._parts()
            if not parts:
                name, kind = "index.html", "text/html; charset=utf-8"
            elif parts in (["app.js"], ["styles.css"]):
                name = parts[0]; kind = "text/javascript; charset=utf-8" if name.endswith(".js") else "text/css; charset=utf-8"
            elif parts == ["api", "health"]:
                self._json(200, {"status": "ready", "real_execution": "blocked", "synthetic_execution": "local_only", "network_egress": False, "cost_aud": 0}); return
            elif len(parts) == 3 and parts[:2] == ["api", "sessions"]:
                try: self._json(200, runtime.get_session(parts[2]))
                except KeyError: self._json(404, {"error": "session_not_found"})
                return
            else:
                self._json(404, {"error": "not_found"}); return
            path = STATIC / name
            self._send(200, path.read_bytes(), kind)

        def do_POST(self) -> None:
            if not self._host_ok():
                self._json(400, {"error": "localhost_only"}); return
            try:
                body, parts = self._body(), self._parts()
                if parts == ["api", "questions"] and set(body) == {"question"}:
                    result, status = runtime.create_question(body["question"]), HTTPStatus.CREATED
                elif len(parts) == 4 and parts[:2] == ["api", "sessions"]:
                    session_id, action = parts[2:]
                    if action == "rehearsal" and not body: result = runtime.create_rehearsal(session_id)
                    elif action == "decision" and set(body) == {"decision", "reviewer", "reason"}: result = runtime.decide(session_id, **body)
                    elif action == "run" and not body: result = runtime.run(session_id)
                    elif action == "review" and set(body) == {"decision", "reviewer", "reason"}: result = runtime.review(session_id, **body)
                    else: raise RuntimeBoundaryError("endpoint fields are closed")
                    status = HTTPStatus.OK
                else: raise RuntimeBoundaryError("unknown endpoint or fields")
                self._json(status, result)
            except KeyError:
                self._json(404, {"error": "session_not_found"})
            except (RuntimeBoundaryError, RuntimeStateError, json.JSONDecodeError, UnicodeDecodeError) as exc:
                self._json(409 if isinstance(exc, RuntimeStateError) else 400, {"error": type(exc).__name__, "detail": str(exc)})

        def log_message(self, format: str, *args) -> None:
            return
    return Handler


def create_server(db_path: str | Path, host: str = "127.0.0.1", port: int = 8766) -> ThreadingHTTPServer:
    if host not in ALLOWED_HOSTS:
        raise RuntimeBoundaryError("server may bind only to localhost")
    if port != 0 and not 1024 <= port <= 65535:
        raise RuntimeBoundaryError("invalid local port")
    return ThreadingHTTPServer((host, port), build_handler(EnvironmentalQuestionRuntime(db_path)))


def serve(db_path: str | Path, host: str = "127.0.0.1", port: int = 8766) -> None:
    server = create_server(db_path, host, port)
    print(f"ClimateOS meaningful environmental question Runtime: http://{host}:{port}")
    print("Real questions produce plans only; execution uses a fictional local fixture. Ctrl+C stops.")
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: server.server_close()
