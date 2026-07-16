"""Offline Environmental Coupling Relation contract for Task1661–1670.

This dependency-free prototype validates repository-authored static synthetic
graphs. It has no network client, data connector, model runner, scheduler,
monitor, scientific scorer, or decision recommender.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

SCHEMA_ID = "climateos.environmental_coupling_graph.v0.1"
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "input"
DOMAINS = {"CLIMATE", "REGIONAL_WEATHER", "WATER", "LAND", "LIFE", "GOVERNANCE"}
RELATIONSHIP_TYPES = {"observed_association", "lagged_signal", "model_inference", "causal_hypothesis"}
GOVERNANCE_STATES = {
    "SYNTHETIC_ONLY",
    "HYPOTHESIS_ONLY",
    "HUMAN_REVIEW_REQUIRED",
    "PROHIBITED_CONCLUSION",
    "ROUTE_TO_TASK1701_PLUS",
}
REQUIRED_SAFE_STATES = {
    "SYNTHETIC_ONLY",
    "HYPOTHESIS_ONLY",
    "HUMAN_REVIEW_REQUIRED",
    "PROHIBITED_CONCLUSION",
}


class CouplingContractError(ValueError):
    """Raised when a graph crosses the static, non-conclusion contract."""


def _strict(value: Any, fields: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise CouplingContractError(f"{label} must be an object")
    missing = fields - set(value)
    unknown = set(value) - fields
    if missing or unknown:
        raise CouplingContractError(
            f"{label} fields invalid; missing={sorted(missing)}, unknown={sorted(unknown)}"
        )
    return value


def _text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CouplingContractError(f"{label} must be a non-empty string")
    return value


def _unique_strings(value: Any, label: str, *, non_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or (non_empty and not value):
        raise CouplingContractError(f"{label} must be a{' non-empty' if non_empty else ''} list")
    values = [_text(item, label) for item in value]
    if len(values) != len(set(values)):
        raise CouplingContractError(f"{label} must contain unique values")
    return values


def load_static_coupling_graph(path: str | Path) -> dict[str, Any]:
    """Load a local fixture only from cczps_lite/input and validate it."""
    if isinstance(path, str) and "://" in path:
        raise CouplingContractError("URL and network graph sources are blocked")
    fixture = Path(path).resolve()
    try:
        fixture.relative_to(FIXTURE_ROOT.resolve())
    except ValueError as exc:
        raise CouplingContractError("Coupling fixtures must stay under cczps_lite/input") from exc
    with fixture.open("r", encoding="utf-8") as stream:
        graph = json.load(stream)
    validate_coupling_graph(graph)
    return graph


def validate_coupling_graph(value: Any) -> None:
    """Validate structure, cross-references, safe states and acyclic routing."""
    root = _strict(
        value,
        {"schema_id", "graph", "evidence_sources", "states", "relations", "boundaries"},
        "root",
    )
    if root["schema_id"] != SCHEMA_ID:
        raise CouplingContractError("Unsupported schema_id")
    _validate_header(root["graph"])
    boundaries = _validate_boundaries(root["boundaries"])

    sources = root["evidence_sources"]
    states = root["states"]
    relations = root["relations"]
    if not isinstance(sources, list) or not sources:
        raise CouplingContractError("evidence_sources must be a non-empty list")
    if not isinstance(states, list) or len(states) < 2:
        raise CouplingContractError("states must contain at least two entries")
    if not isinstance(relations, list) or not relations:
        raise CouplingContractError("relations must be a non-empty list")

    source_ids: set[str] = set()
    for source in sources:
        _validate_source(source)
        if source["source_id"] in source_ids:
            raise CouplingContractError(f"Duplicate source_id: {source['source_id']}")
        source_ids.add(source["source_id"])

    state_ids: set[str] = set()
    for state in states:
        _validate_state(state, source_ids)
        if state["state_id"] in state_ids:
            raise CouplingContractError(f"Duplicate state_id: {state['state_id']}")
        state_ids.add(state["state_id"])

    relation_ids: set[str] = set()
    edges: list[tuple[str, str]] = []
    for relation in relations:
        _validate_relation(relation, state_ids, source_ids, boundaries)
        if relation["relation_id"] in relation_ids:
            raise CouplingContractError(f"Duplicate relation_id: {relation['relation_id']}")
        relation_ids.add(relation["relation_id"])
        edges.append((relation["source_state_id"], relation["target_state_id"]))
    _validate_acyclic(state_ids, edges)


def _validate_header(header: Any) -> None:
    fields = {"graph_id", "title", "classification", "purpose", "geography", "time_scope"}
    record = _strict(header, fields, "graph")
    for field in ("graph_id", "title", "geography"):
        _text(record[field], field)
    if record["classification"] != "REPOSITORY_AUTHORED_STATIC_SYNTHETIC_ONLY":
        raise CouplingContractError("Only repository-authored static synthetic graphs are allowed")
    if record["purpose"] != "INTERFACE_AND_GOVERNANCE_VALIDATION_ONLY":
        raise CouplingContractError("Graph purpose exceeds interface and governance validation")
    if record["time_scope"] != "ILLUSTRATIVE_NOT_OBSERVED_OR_FORECAST":
        raise CouplingContractError("Observed or forecast time scopes are blocked")


def _validate_boundaries(value: Any) -> dict[str, Any]:
    fields = {
        "network_used", "real_data_accessed", "model_executed", "monitoring_active",
        "external_action", "scientific_conclusion_formed",
        "project_performance_conclusion_formed", "cost_aud", "human_review_required",
    }
    boundaries = _strict(value, fields, "boundaries")
    false_fields = fields - {"cost_aud", "human_review_required"}
    if any(boundaries[field] is not False for field in false_fields):
        raise CouplingContractError("Network, data, model, monitoring, action and conclusions must remain false")
    if boundaries["cost_aud"] != 0 or isinstance(boundaries["cost_aud"], bool):
        raise CouplingContractError("cost_aud must remain zero")
    if boundaries["human_review_required"] is not True:
        raise CouplingContractError("human_review_required must remain true")
    return boundaries


def _validate_source(source: Any) -> None:
    fields = {"source_id", "source_class", "description", "external_locator", "admission_state"}
    record = _strict(source, fields, "evidence source")
    _text(record["source_id"], "source_id")
    _text(record["description"], "source description")
    if record["source_class"] != "REPOSITORY_SYNTHETIC_FIXTURE":
        raise CouplingContractError("Only repository synthetic fixture sources are allowed")
    if record["external_locator"] is not None:
        raise CouplingContractError("External locators are blocked")
    if record["admission_state"] != "SYNTHETIC_INTERFACE_ONLY":
        raise CouplingContractError("Synthetic sources cannot be promoted to evidence")


def _validate_state(state: Any, source_ids: set[str]) -> None:
    fields = {
        "state_id", "domain", "label", "state_class", "geography", "time_scope",
        "evidence_source_ids", "uncertainty_state", "human_review_status",
    }
    record = _strict(state, fields, "state")
    for field in ("state_id", "label", "geography"):
        _text(record[field], field)
    if record["domain"] not in DOMAINS:
        raise CouplingContractError("Unsupported state domain")
    if record["state_class"] != "SYNTHETIC_HYPOTHESIS_STATE":
        raise CouplingContractError("State class must remain synthetic hypothesis")
    if record["time_scope"] != "ILLUSTRATIVE_ONLY":
        raise CouplingContractError("State time_scope must remain illustrative")
    refs = set(_unique_strings(record["evidence_source_ids"], "state evidence_source_ids", non_empty=True))
    if not refs <= source_ids:
        raise CouplingContractError("State references unknown synthetic sources")
    if record["uncertainty_state"] != "NOT_ASSESSED":
        raise CouplingContractError("Synthetic state uncertainty cannot be assessed")
    if record["human_review_status"] != "NOT_REVIEWED":
        raise CouplingContractError("No expert review is authorized")


def _validate_relation(
    relation: Any,
    state_ids: set[str],
    source_ids: set[str],
    boundaries: dict[str, Any],
) -> None:
    fields = {
        "relation_id", "source_state_id", "target_state_id", "relationship_type",
        "lead_lag_window", "geography", "time_period", "evidence_source_ids",
        "model_method", "confidence", "uncertainty_transformation", "stationarity_warning",
        "expert_review_status", "future_mechanism_test_id", "governance_states",
        "prohibited_inferences",
    }
    record = _strict(relation, fields, "relation")
    for field in ("relation_id", "source_state_id", "target_state_id", "geography"):
        _text(record[field], field)
    if record["source_state_id"] not in state_ids or record["target_state_id"] not in state_ids:
        raise CouplingContractError("Relation references unknown states")
    if record["source_state_id"] == record["target_state_id"]:
        raise CouplingContractError("Self-relations are blocked")
    relationship_type = record["relationship_type"]
    if relationship_type not in RELATIONSHIP_TYPES:
        raise CouplingContractError("Unsupported relationship_type")
    if relationship_type == "observed_association":
        raise CouplingContractError("Observed associations require a separately authorized evidence gate")
    if relationship_type == "model_inference" or boundaries["model_executed"] is not False:
        raise CouplingContractError("Model inference and execution are blocked")
    _validate_lead_lag(record["lead_lag_window"])
    if record["time_period"] != "ILLUSTRATIVE_NOT_OBSERVED":
        raise CouplingContractError("Relation time_period must remain illustrative")
    refs = set(_unique_strings(record["evidence_source_ids"], "relation evidence_source_ids", non_empty=True))
    if not refs <= source_ids:
        raise CouplingContractError("Relation references unknown synthetic sources")
    if record["model_method"] != "NONE_NO_MODEL_EXECUTION" or record["confidence"] != "NOT_ASSESSED":
        raise CouplingContractError("No model method or confidence assessment is authorized")
    _text(record["uncertainty_transformation"], "uncertainty_transformation")
    _text(record["stationarity_warning"], "stationarity_warning")
    if record["expert_review_status"] != "NOT_REVIEWED":
        raise CouplingContractError("No expert review is authorized")
    states = set(_unique_strings(record["governance_states"], "governance_states", non_empty=True))
    if not states <= GOVERNANCE_STATES or not REQUIRED_SAFE_STATES <= states:
        raise CouplingContractError("Relation must retain all synthetic, review and prohibition states")
    _unique_strings(record["prohibited_inferences"], "prohibited_inferences", non_empty=True)
    if relationship_type == "causal_hypothesis":
        mechanism_id = _text(record["future_mechanism_test_id"], "future_mechanism_test_id")
        if not mechanism_id.startswith("TASK1701-") or "ROUTE_TO_TASK1701_PLUS" not in states:
            raise CouplingContractError("Causal hypotheses must route to Task1701+")
    elif record["future_mechanism_test_id"] is not None:
        raise CouplingContractError("Only causal hypotheses may register mechanism tests")


def _validate_lead_lag(value: Any) -> None:
    record = _strict(value, {"minimum", "maximum", "unit", "status"}, "lead_lag_window")
    if record["minimum"] is not None or record["maximum"] is not None:
        raise CouplingContractError("No lead-lag value may be estimated in this batch")
    if record["unit"] != "NOT_ESTIMATED" or record["status"] != "ILLUSTRATIVE_ONLY":
        raise CouplingContractError("Lead-lag window must remain unestimated and illustrative")


def _validate_acyclic(state_ids: set[str], edges: list[tuple[str, str]]) -> None:
    adjacency = {state_id: [] for state_id in state_ids}
    for source, target in edges:
        adjacency[source].append(target)
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visiting:
            raise CouplingContractError("Coupling graph cycles are blocked in v0.1")
        if node in visited:
            return
        visiting.add(node)
        for target in adjacency[node]:
            visit(target)
        visiting.remove(node)
        visited.add(node)

    for state_id in sorted(state_ids):
        visit(state_id)


def build_internal_coupling_preview(graph: dict[str, Any]) -> dict[str, Any]:
    """Return a deterministic non-decision preview after strict validation."""
    validate_coupling_graph(graph)
    relation_types: dict[str, int] = {}
    mechanism_routes: list[str] = []
    for relation in graph["relations"]:
        relation_type = relation["relationship_type"]
        relation_types[relation_type] = relation_types.get(relation_type, 0) + 1
        if relation["future_mechanism_test_id"] is not None:
            mechanism_routes.append(relation["future_mechanism_test_id"])
    return {
        "graph_id": graph["graph"]["graph_id"],
        "classification": "STATIC_SYNTHETIC_INTERFACE_PREVIEW_ONLY",
        "state_count": len(graph["states"]),
        "relation_count": len(graph["relations"]),
        "relation_types": dict(sorted(relation_types.items())),
        "future_mechanism_test_ids": sorted(mechanism_routes),
        "scientific_conclusion": "NONE",
        "governance_recommendation": "NONE",
        "decision_support_status": "NOT_READY_FOR_DECISION",
        "human_review_required": True,
        "boundary_note": (
            "Repository-authored static synthetic interface only; no observation, forecast, "
            "model execution, causal finding, project conclusion, monitoring or external action."
        ),
    }
