from .schemas import CandidateStatus


class InvalidTransitionError(ValueError):
    pass


TERMINAL_STATUSES = {"Archived", "Superseded"}

ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    "Draft Candidate": {
        "Needs Source Verification",
        "Needs Translation Review",
        "Needs Human Review",
        "Blocked",
        "Founder Gate Required",
        "Archived",
        "Superseded",
    },
    "Needs Source Verification": {
        "Needs Translation Review",
        "Needs Human Review",
        "Blocked",
        "Founder Gate Required",
        "Archived",
        "Superseded",
    },
    "Needs Translation Review": {
        "Needs Human Review",
        "Blocked",
        "Founder Gate Required",
        "Archived",
        "Superseded",
    },
    "Needs Human Review": {
        "Human-Reviewed Candidate",
        "Blocked",
        "Founder Gate Required",
        "Archived",
        "Superseded",
    },
    "Human-Reviewed Candidate": {
        "Needs Human Review",
        "Blocked",
        "Founder Gate Required",
        "Archived",
        "Superseded",
    },
    "Blocked": {
        "Needs Human Review",
        "Founder Gate Required",
        "Archived",
        "Superseded",
    },
    "Founder Gate Required": {
        "Needs Human Review",
        "Human-Reviewed Candidate",
        "Blocked",
        "Archived",
        "Superseded",
    },
    "Archived": set(),
    "Superseded": set(),
}


def validate_transition(
    current_status: str,
    new_status: CandidateStatus,
    linked_risk_flags: list[str],
    founder_gate_trigger: str,
) -> None:
    if current_status == new_status:
        raise InvalidTransitionError("Status transition must change the candidate status.")
    if current_status in TERMINAL_STATUSES:
        raise InvalidTransitionError(f"{current_status} records are terminal in this prototype.")
    if new_status not in ALLOWED_TRANSITIONS.get(current_status, set()):
        raise InvalidTransitionError(f"Transition from {current_status} to {new_status} is not permitted.")
    if new_status in {"Blocked", "Founder Gate Required"} and not linked_risk_flags:
        raise InvalidTransitionError(f"Transition to {new_status} requires at least one linked risk flag.")
    if new_status == "Founder Gate Required" and not founder_gate_trigger:
        raise InvalidTransitionError("Founder Gate Required transition requires a Founder Gate trigger.")
    if current_status == "Human-Reviewed Candidate" and new_status == "Needs Human Review" and not linked_risk_flags:
        raise InvalidTransitionError("Revoking Human-Reviewed Candidate status requires a linked risk flag.")
