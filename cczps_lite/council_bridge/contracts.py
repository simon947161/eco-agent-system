"""Small closed exchange contracts layered over existing ClimateOS identities."""
from __future__ import annotations

import math
import re
from datetime import datetime, timezone

from cczps_lite.scientist_runtime.contracts import canonical_json, digest

VERSION = "climateos.council_bridge.v0.1"
LABEL = "SYNTHETIC_ONLY / NOT_ENVIRONMENTAL_EVIDENCE / LOCAL_REHEARSAL"
KINDS = {"ADMINISTRATIVE", "SETTLEMENT", "SITE", "CATCHMENT", "STATION", "SERVICE_AREA", "CLIMATE_GRID", "ASSET", "ECOSYSTEM"}
REQUEST_FIELDS = {"request_id", "council_id", "question_id", "spatial_ids", "variable", "unit", "period_start", "period_end", "input_digest", "data_classification", "licence", "model_version", "budget_aud", "approval_digest", "idempotency_key", "output_requirement"}


class BridgeError(ValueError):
    pass


def identifier(value):
    if not isinstance(value, str) or re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]{0,79}", value) is None:
        raise BridgeError("invalid identifier")
    return value


def instant(value):
    try:
        stamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if stamp.tzinfo is None:
            raise ValueError("timezone required")
        return stamp.astimezone(timezone.utc)
    except (ValueError, TypeError, AttributeError) as exc:
        raise BridgeError("timezone-aware ISO timestamp required") from exc


def utcnow():
    return datetime.now(timezone.utc).isoformat()


def require(condition, message):
    if not condition:
        raise BridgeError(message)


def validate_config(config):
    identifier(config["council_id"])
    require(config["boundary"]["geometry"] is None, "real boundary not admitted in rehearsal")
    require(config["boundary"]["status"] == "METADATA_ONLY_NOT_ADMITTED", "boundary status")
    objects = config["objects"]
    ids = [identifier(obj["id"]) for obj in objects]
    require(len(ids) == len(set(ids)), "duplicate spatial identity")
    for obj in objects:
        require(obj["kind"] in KINDS and obj["classification"] == "SYNTHETIC_ONLY", "spatial classification")
        require(0 <= obj["x"] <= 100 and 0 <= obj["y"] <= 100, "schematic coordinates")
    for relation in config["relations"]:
        require(relation["from"] in ids and relation["to"] in ids, "unresolved spatial relationship")
        require(relation["type"] in {"CONTAINS", "DEPENDS_ON", "OVERLAPS", "UPSTREAM_OF"}, "relationship type")
    return config


def validate_request(request, config, expected_input):
    require(isinstance(request, dict) and set(request) == REQUEST_FIELDS, "closed Compute Request fields required")
    for key in ("request_id", "council_id", "question_id", "idempotency_key"):
        identifier(request[key])
    require(request["council_id"] == config["council_id"], "Council mismatch")
    require(request["data_classification"] == "SYNTHETIC_ONLY", "only synthetic execution admitted")
    require(request["variable"] == "fixture_resource_index" and request["unit"] == "1", "variable/unit mismatch")
    require(request["model_version"] == "fixed-fixture-v1", "model not admitted")
    require(request["licence"] == "MIT_REPOSITORY_FIXTURE", "input licence not admitted")
    require(request["output_requirement"] == "SYNTHETIC_DIAGNOSTIC_ONLY", "output scope mismatch")
    require(isinstance(request["spatial_ids"], list) and len(set(request["spatial_ids"])) >= 2, "two spatial objects required")
    require(set(request["spatial_ids"]) <= {x["id"] for x in config["objects"]}, "unknown spatial scope")
    require(instant(request["period_start"]) < instant(request["period_end"]), "time range mismatch")
    require(request["input_digest"] == expected_input, "input changed")
    budget = request["budget_aud"]
    require(type(budget) in (int, float) and math.isfinite(budget) and budget == 0, "only zero cost admitted")
    require(request["approval_digest"] == digest({k: v for k, v in request.items() if k != "approval_digest"}), "approval scope changed")
    return request
