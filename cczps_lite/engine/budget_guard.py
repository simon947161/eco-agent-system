"""Pre-execution budget guard rules for CCZPS-Lite."""

from __future__ import annotations

import csv
import json
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
PROFILE_PATH = PROJECT_DIR / "input" / "budget_profile.json"
OUTPUT_DIR = PROJECT_DIR / "output"

COST_RANK = {"low": 1, "medium": 2, "high": 3, "very_high": 4}
BUDGET_GUARD_FIELDS = [
    "monthly_budget_limit", "daily_call_limit", "agent_run_limit",
    "estimated_calls", "estimated_cost_level", "budget_status",
    "budget_warning", "requires_manual_confirmation",
    "stop_if_budget_exceeded", "budget_guard_summary",
]


def load_budget_profile(path: Path = PROFILE_PATH) -> dict:
    with path.open("r", encoding="utf-8") as file_obj:
        profile = json.load(file_obj)
    if not isinstance(profile.get("default"), dict):
        raise ValueError("budget profile requires a default object")
    if not isinstance(profile.get("scenarios"), dict):
        raise ValueError("budget profile requires scenario request mappings")
    return profile


def classify_budget_status(
    monthly_budget_limit: str,
    daily_call_limit: int,
    agent_run_limit: int,
    estimated_calls: int,
    estimated_monthly_cost: str = "low",
    agent_run_count: int = 0,
) -> str:
    """Classify declared limits without metering or executing resources."""
    if monthly_budget_limit not in COST_RANK:
        raise ValueError(f"unsupported monthly budget limit: {monthly_budget_limit}")
    if estimated_monthly_cost not in COST_RANK:
        raise ValueError(f"unsupported estimated monthly cost: {estimated_monthly_cost}")
    if (
        estimated_calls > daily_call_limit
        or agent_run_count > agent_run_limit
        or COST_RANK[estimated_monthly_cost] > COST_RANK[monthly_budget_limit]
    ):
        return "stop_required"
    close_to_limit = daily_call_limit > 0 and estimated_calls >= daily_call_limit * 0.8
    if close_to_limit or estimated_monthly_cost in {"medium", "high", "very_high"}:
        return "warning"
    return "within_budget"


def requires_manual_confirmation(
    usage_cost_governance: dict, resource_request: dict
) -> bool:
    resource_classes = resource_request.get("resource_classes", [])
    has_external_resources = bool(resource_classes)
    approval_granted = bool(resource_request.get("manual_approval_granted", False))
    approval_trigger = (
        bool(usage_cost_governance.get("requires_user_approval"))
        or usage_cost_governance.get("agentic_consumption_risk")
        in {"medium", "high", "very_high"}
        or bool(resource_request.get("repeated_external_calls"))
        or bool(resource_request.get("continuous_execution"))
        or (
            usage_cost_governance.get("usage_mode") == "agent_mode"
            and has_external_resources
        )
    )
    return has_external_resources and approval_trigger and not approval_granted


def should_stop_if_budget_exceeded(budget_status: str) -> bool:
    return budget_status == "stop_required"


def summarize_budget_guard(budget_guard_result: dict) -> str:
    status = budget_guard_result["budget_status"]
    if status == "stop_required":
        action = "Stop before execution; a declared hard limit or risk condition is exceeded."
    elif status == "approval_required":
        action = "Do not proceed until manual confirmation is recorded."
    elif status == "warning":
        action = "Proceed only with caution and review the declared limits."
    else:
        action = "The declared activity is within the current local guard profile."
    return (
        f"Budget status is {status}. Estimated calls are "
        f"{budget_guard_result['estimated_calls']} against a daily limit of "
        f"{budget_guard_result['daily_call_limit']}; the agent-run limit is "
        f"{budget_guard_result['agent_run_limit']}. {action} This is a "
        "pre-execution governance check only; no metering, billing, payment, "
        "or external resource call is performed."
    )


def derive_budget_guard(
    usage_cost_governance: dict, resource_request: dict, budget_profile: dict | None = None
) -> dict:
    profile = budget_profile or load_budget_profile()["default"]
    monthly_budget_limit = profile["monthly_budget_limit"]
    daily_call_limit = int(profile["daily_call_limit"])
    agent_run_limit = int(profile["agent_run_limit"])
    estimated_calls = max(0, int(resource_request.get("estimated_calls", 0)))
    estimated_cost_level = resource_request.get(
        "estimated_monthly_cost",
        usage_cost_governance.get("estimated_external_resource_cost", "low"),
    )
    agent_run_count = max(0, int(resource_request.get("agent_run_count", 0)))
    approval_granted = bool(resource_request.get("manual_approval_granted", False))
    status = classify_budget_status(
        monthly_budget_limit, daily_call_limit, agent_run_limit, estimated_calls,
        estimated_cost_level, agent_run_count,
    )
    if (
        usage_cost_governance.get("agentic_consumption_risk") == "very_high"
        and not approval_granted
    ):
        status = "stop_required"
    manual_confirmation = requires_manual_confirmation(
        usage_cost_governance, resource_request
    )
    if status != "stop_required":
        if manual_confirmation:
            status = "approval_required"
        elif status == "within_budget" and (
            usage_cost_governance.get("estimated_external_resource_cost")
            in {"medium", "high", "very_high"}
            or usage_cost_governance.get("agentic_consumption_risk")
            in {"medium", "high", "very_high"}
        ):
            status = "warning"
    result = {
        "monthly_budget_limit": monthly_budget_limit,
        "daily_call_limit": daily_call_limit,
        "agent_run_limit": agent_run_limit,
        "estimated_calls": estimated_calls,
        "estimated_cost_level": estimated_cost_level,
        "budget_status": status,
        "budget_warning": status in {"warning", "approval_required", "stop_required"},
        "requires_manual_confirmation": manual_confirmation,
        "stop_if_budget_exceeded": (
            bool(profile.get("stop_if_budget_exceeded", True))
            and should_stop_if_budget_exceeded(status)
        ),
    }
    result["budget_guard_summary"] = summarize_budget_guard(result)
    return result


def _append_report_section(path: Path, marker: str, lines: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    text = text.split(marker, 1)[0].rstrip()
    path.write_text(text + "\n\n" + "\n".join(lines) + "\n", encoding="utf-8")


def augment_runtime_outputs() -> list[dict]:
    profile = load_budget_profile()
    matrix_path = OUTPUT_DIR / "comparison_matrix.csv"
    with matrix_path.open("r", encoding="utf-8", newline="") as file_obj:
        reader = csv.DictReader(file_obj)
        base_fields = [
            field for field in (reader.fieldnames or [])
            if field not in BUDGET_GUARD_FIELDS
        ]
        rows = list(reader)
    for row in rows:
        request = profile["scenarios"].get(row["scenario_id"], {})
        row.update(derive_budget_guard(row, request, profile["default"]))
    with matrix_path.open("w", encoding="utf-8", newline="") as file_obj:
        writer = csv.DictWriter(
            file_obj, fieldnames=base_fields + BUDGET_GUARD_FIELDS,
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)
    report_lines = [
        "## Budget Guard Reading", "",
        "These are local pre-execution guard classifications, not measured usage or financial calculations.",
    ]
    for row in rows:
        report_lines.extend([
            "", f"### {row['scenario_name']}", "",
            f"- Budget status: {row['budget_status']}",
            f"- Estimated calls: {row['estimated_calls']}",
            f"- Daily call limit: {row['daily_call_limit']}",
            f"- Agent run limit: {row['agent_run_limit']}",
            f"- Manual confirmation required: {row['requires_manual_confirmation']}",
            f"- Stop if budget exceeded: {row['stop_if_budget_exceeded']}",
            f"- Budget guard summary: {row['budget_guard_summary']}",
        ])
    _append_report_section(
        OUTPUT_DIR / "scenario_report.md", "\n## Budget Guard Reading\n", report_lines
    )
    stopped = [row["scenario_name"] for row in rows if row["budget_status"] == "stop_required"]
    approvals = [row["scenario_name"] for row in rows if row["budget_status"] == "approval_required"]
    governance_lines = [
        "## Budget Guard Reading", "",
        f"- Stop required before execution: {', '.join(stopped) or 'None'}.",
        f"- Manual confirmation required: {', '.join(approvals) or 'None'}.",
        "- Hard call, monthly-cost, and agent-run limits cannot be overridden by manual approval.",
        "- Boundary: no live metering, billing, payment, subscription, invoice, or external execution is performed.",
    ]
    _append_report_section(
        OUTPUT_DIR / "governance_summary.md", "\n## Budget Guard Reading\n",
        governance_lines,
    )
    return rows


def main() -> None:
    augment_runtime_outputs()
    print("Added budget guard readings to CCZPS-Lite outputs")


if __name__ == "__main__":
    main()
