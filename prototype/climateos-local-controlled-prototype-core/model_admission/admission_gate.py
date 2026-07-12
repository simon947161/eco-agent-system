"""Deterministic structural gate for Task1290-1299.

This module validates records and blockers. It never decides a real model.
"""

ALLOWED_STATES = {
    "ADMITTED_FOR_RESEARCH",
    "ADMITTED_WITH_LIMITATIONS",
    "REQUIRES_FURTHER_EVIDENCE",
    "NOT_ADMITTED",
    "LICENCE_OR_PROVENANCE_BLOCKED",
}

REQUIRED_SCOPE = {
    "model_id", "model_version", "source_revision", "purpose", "variables",
    "region", "forecast_horizons", "evidence_snapshot_id", "licence_status",
    "review_date", "expiry_date",
}

REQUIRED_EVIDENCE = {
    "model_registry", "statistical_evaluation", "physical_consistency",
    "extreme_event", "regional_fitness", "ood_nonstationarity",
    "licence_provenance_cost_dependency_exit", "disputes_counter_evidence",
}


def assess_completeness(record):
    """Return blockers and missing fields without assigning an admission state."""
    blockers = []
    missing_scope = sorted(k for k in REQUIRED_SCOPE if not record.get(k))
    if missing_scope:
        blockers.append({"code": "missing_scope", "fields": missing_scope})

    evidence = record.get("evidence", {})
    missing_evidence = sorted(k for k in REQUIRED_EVIDENCE if k not in evidence)
    if missing_evidence:
        blockers.append({"code": "missing_evidence", "fields": missing_evidence})

    if record.get("licence_status") in {"blocked", "unknown"}:
        blockers.append({"code": "licence_or_provenance_blocked"})

    return {"complete": not blockers, "blockers": blockers}


def record_human_decision(record, decision):
    """Validate and append an explicit human decision.

    Real records cannot receive a decision unless the human supplies all
    authority metadata. No state is inferred from evidence.
    """
    if not decision.get("responsible_human"):
        raise ValueError("responsible_human is required")
    if decision.get("state") not in ALLOWED_STATES:
        raise ValueError("invalid admission state")
    if not decision.get("reason"):
        raise ValueError("decision reason is required")
    if not decision.get("evidence_snapshot_id"):
        raise ValueError("evidence_snapshot_id is required")
    if decision["evidence_snapshot_id"] != record.get("evidence_snapshot_id"):
        raise ValueError("decision evidence snapshot must match the record")
    if not decision.get("decided_at"):
        raise ValueError("decided_at is required")

    assessment = assess_completeness(record)
    favourable = decision["state"] in {
        "ADMITTED_FOR_RESEARCH", "ADMITTED_WITH_LIMITATIONS"
    }
    if favourable and not assessment["complete"]:
        raise ValueError("blocked or incomplete evidence cannot be admitted")

    history = list(record.get("decision_history", []))
    history.append(dict(decision))
    result = dict(record)
    result["decision_history"] = history
    result["current_human_decision"] = dict(decision)
    return result


def automatic_real_model_decision(*_args, **_kwargs):
    """Hard refusal path required by Founder authorization."""
    raise PermissionError("automatic real-model admission is prohibited")
