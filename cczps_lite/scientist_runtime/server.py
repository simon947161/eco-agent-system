"""Dependency-free localhost Web adapter for the minimum runtime."""

from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Lock
from urllib.parse import urlparse

from .contracts import ContractError
from .runtime import RuntimeBoundaryError, RuntimeStateError, ScientistRuntime

STATIC_ROOT = Path(__file__).resolve().parent / "static"
MAX_REQUEST_BYTES = 64 * 1024
ALLOWED_HOSTS = {"127.0.0.1", "localhost"}


def build_handler(runtime: ScientistRuntime):
    class RuntimeHandler(BaseHTTPRequestHandler):
        server_version = "ClimateOSMinimumRuntime/0.1"

        def _headers(self, status: int, content_type: str) -> None:
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("X-Frame-Options", "DENY")
            self.send_header("Referrer-Policy", "no-referrer")
            self.end_headers()

        def _json(self, status: int, value: object) -> None:
            payload = json.dumps(value, ensure_ascii=False, sort_keys=True).encode("utf-8")
            self._headers(status, "application/json; charset=utf-8")
            self.wfile.write(payload)

        def _body(self) -> dict:
            raw_length = self.headers.get("Content-Length", "0")
            try:
                length = int(raw_length)
            except ValueError as exc:
                raise ContractError("invalid Content-Length") from exc
            if length <= 0 or length > MAX_REQUEST_BYTES:
                raise ContractError("request body size is outside 1..65536 bytes")
            try:
                value = json.loads(self.rfile.read(length).decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise ContractError("request body must be UTF-8 JSON") from exc
            if not isinstance(value, dict):
                raise ContractError("request body must be a JSON object")
            return value

        def _safe_host(self) -> bool:
            host = self.headers.get("Host", "").split(":", 1)[0].casefold()
            return host in ALLOWED_HOSTS

        def _segments(self) -> list[str]:
            return [item for item in urlparse(self.path).path.split("/") if item]

        def _error(self, exc: Exception) -> None:
            status = HTTPStatus.CONFLICT if isinstance(exc, RuntimeStateError) else HTTPStatus.BAD_REQUEST
            self._json(status, {"error": type(exc).__name__, "detail": str(exc)})

        def do_GET(self) -> None:
            if not self._safe_host():
                self._json(HTTPStatus.BAD_REQUEST, {"error": "localhost_only"})
                return
            parts = self._segments()
            if not parts:
                self._serve_file("index.html", "text/html; charset=utf-8")
            elif parts == ["app.js"]:
                self._serve_file("app.js", "text/javascript; charset=utf-8")
            elif parts == ["styles.css"]:
                self._serve_file("styles.css", "text/css; charset=utf-8")
            elif parts == ["api", "health"]:
                self._json(HTTPStatus.OK, {
                    "status": "ready",
                    "localhost_only": True,
                    "network_egress": False,
                    "cost_aud": 0,
                    "scientific_authority": False,
                })
            elif len(parts) == 3 and parts[:2] == ["api", "sessions"]:
                try:
                    self._json(HTTPStatus.OK, runtime.get_session(parts[2]))
                except KeyError:
                    self._json(HTTPStatus.NOT_FOUND, {"error": "session_not_found"})
            else:
                self._json(HTTPStatus.NOT_FOUND, {"error": "not_found"})

        def _serve_file(self, name: str, content_type: str) -> None:
            path = STATIC_ROOT / name
            if not path.is_file():
                self._json(HTTPStatus.NOT_FOUND, {"error": "asset_not_found"})
                return
            self._headers(HTTPStatus.OK, content_type)
            self.wfile.write(path.read_bytes())

        def do_POST(self) -> None:
            if not self._safe_host():
                self._json(HTTPStatus.BAD_REQUEST, {"error": "localhost_only"})
                return
            try:
                body = self._body()
                parts = self._segments()
                if parts == ["api", "sessions"]:
                    allowed = {"question", "session_label"}
                    if not set(body) <= allowed or "question" not in body:
                        raise ContractError("session fields are closed")
                    result = runtime.create_session(body["question"], session_label=body.get("session_label", "founder-web-demo"))
                    status = HTTPStatus.CREATED
                elif len(parts) == 4 and parts[:2] == ["api", "sessions"]:
                    session_id, action = parts[2], parts[3]
                    if action == "propose":
                        if body:
                            raise ContractError("propose accepts an empty JSON object")
                        result = runtime.propose_hypothesis(session_id)
                    elif action == "revise":
                        if set(body) != {"hypothesis", "reviewer_label", "reason"}:
                            raise ContractError("revision fields are closed")
                        result = runtime.revise_hypothesis(session_id, **body)
                    elif action == "decision":
                        if set(body) != {"decision", "reviewer_label", "reason"}:
                            raise ContractError("decision fields are closed")
                        result = runtime.decide_before_run(session_id, **body)
                    elif action == "run":
                        if body:
                            raise ContractError("run accepts an empty JSON object")
                        result = runtime.run(session_id)
                    elif action == "review":
                        if set(body) != {"decision", "reviewer_label", "reason"}:
                            raise ContractError("review fields are closed")
                        result = runtime.review(session_id, **body)
                    else:
                        self._json(HTTPStatus.NOT_FOUND, {"error": "not_found"})
                        return
                    status = HTTPStatus.OK
                else:
                    self._json(HTTPStatus.NOT_FOUND, {"error": "not_found"})
                    return
                self._json(status, result)
            except KeyError:
                self._json(HTTPStatus.NOT_FOUND, {"error": "session_not_found"})
            except (ContractError, RuntimeStateError, RuntimeBoundaryError) as exc:
                self._error(exc)

        def log_message(self, format: str, *args) -> None:
            return

    return RuntimeHandler


class ScientistHTTPServer(ThreadingHTTPServer):
    """Threaded localhost server with explicit, idempotent resource shutdown."""

    def __init__(self, address, handler, runtime) -> None:
        self.runtime = runtime
        self._lifecycle_lock = Lock()
        self._shutdown_requested = False
        self._server_closed = False
        self._resources_closed = False
        super().__init__(address, handler)

    def shutdown(self) -> None:
        with self._lifecycle_lock:
            if self._shutdown_requested:
                return
            self._shutdown_requested = True
        super().shutdown()

    def close_runtime_resources(self) -> None:
        with self._lifecycle_lock:
            if self._resources_closed:
                return
            self._resources_closed = True
        self.runtime.close()

    def server_close(self) -> None:
        with self._lifecycle_lock:
            if self._server_closed:
                return
            self._server_closed = True
        try:
            super().server_close()
        finally:
            self.close_runtime_resources()


def create_server(db_path: str | Path, host: str = "127.0.0.1", port: int = 8765) -> ScientistHTTPServer:
    if host not in ALLOWED_HOSTS:
        raise RuntimeBoundaryError("server may bind only to localhost")
    if port != 0 and not 1024 <= port <= 65535:
        raise RuntimeBoundaryError("port must be 0 for an ephemeral test port or in 1024..65535")
    runtime = ScientistRuntime(db_path)
    return ScientistHTTPServer((host, port), build_handler(runtime), runtime)


def serve(db_path: str | Path, host: str = "127.0.0.1", port: int = 8765) -> None:
    server = create_server(db_path, host, port)
    print(f"ClimateOS minimum scientist runtime: http://{host}:{port}")
    print("Local fictional tiny-synthetic demonstration only. Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
