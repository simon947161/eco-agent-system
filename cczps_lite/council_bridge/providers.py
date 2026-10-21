"""Provider protocol and deterministic, no-network simulation."""
from typing import Protocol

from .contracts import BridgeError


class Provider(Protocol):
    provider_id: str

    def capabilities(self) -> dict: ...
    def submit(self, request: dict) -> dict: ...
    def status(self, request: dict, mode: str) -> dict: ...
    def cancel(self, request: dict) -> dict: ...


class MockProvider:
    provider_id = "mock-local"

    def capabilities(self):
        return {"provider_id": self.provider_id, "model_version": "fixed-fixture-v1", "variable": "fixture_resource_index", "unit": "1", "network": False, "cost_aud": 0}

    def submit(self, request):
        return {"status": "QUEUED", "provider_id": self.provider_id}

    def cancel(self, request):
        return {"status": "CANCELLED"}

    def status(self, request, mode="success"):
        if mode not in {"success", "timeout", "failure", "incompatible"}:
            raise BridgeError("unknown simulation mode")
        if mode in {"timeout", "failure"}:
            return {"status": "TIMED_OUT" if mode == "timeout" else "FAILED", "error": "SIMULATED_" + mode.upper()}
        return {"status": "COMPLETED_QUARANTINED", "result": {
            "classification": "SYNTHETIC_ONLY", "request_id": request["request_id"],
            "input_digest": request["input_digest"], "model_version": "fixed-fixture-v1",
            "variable": request["variable"], "unit": "K" if mode == "incompatible" else "1",
            "period_start": request["period_start"], "period_end": request["period_end"],
            "spatial_ids": request["spatial_ids"], "diagnostic": 1,
            "uncertainty": "Fictional diagnostic; no environmental confidence", "network_used": False, "cost_aud": 0}}


class AlternateMockProvider(MockProvider):
    provider_id = "mock-alternate"


class MatrixOneAdapter:
    provider_id = "matrix-one-unverified"

    def capabilities(self):
        return {"provider_id": self.provider_id, "status": "IDENTITY_API_LICENCE_COST_UNVERIFIED", "executable": False}

    def submit(self, request):
        raise BridgeError("Matrix One real service is not verified or admitted")

    def status(self, request, mode="success"):
        raise BridgeError("no admitted Matrix One job")

    def cancel(self, request):
        raise BridgeError("no admitted Matrix One job")
