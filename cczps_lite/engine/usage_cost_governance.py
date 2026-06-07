"""Usage and cost governance rules for CCZPS-Lite."""

from __future__ import annotations

import csv
import json
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = PROJECT_DIR.parent
PROFILE_PATH = PROJECT_DIR / "input" / "usage_cost_profiles.json"
OUTPUT_DIR = PROJECT_DIR / "output"

USAGE_MODES = {"idea_mode", "project_mode", "agent_mode", "enterprise_mode"}
SERVICE_MODELS = {
    "open_source",
    "service_fee",
    "enterprise_support",
    "data_asset_service",
}
GOVERNANCE_FIELDS = [
    "usage_mode",
    "external_resource_owner",
    "estimated_cost_level",
    "budget_warning",
    "requires_user_approval",
    "platform_service_model",
    "agentic_risk_level",
    "governance_summary",
]


def load_usage_profiles(path: Path = PROFILE_PATH) -> dict:
    with path.open("r", encoding="utf-8") as file_obj:
        profiles = json.load(file_obj)
    if not isinstance(profiles.get("default"), dict):
        raise ValueError("usage cost profiles require a default profile")
    if not isinstance(profiles.get("scenarios"), dict):
        raise ValueError("usage cost profiles require scenario mappings")
    return profiles


def derive_usage_cost_governance(
    usage_mode: str,
    external_resource_owner: str,
    external_resource_count: int = 0,
    repeated_external_calls: bool = False,
    continuous_execution: bool = False,
    agent_count: int = 0,
    budget_controlled: bool = True,
    platform_service_model: str = "open_source",
) -> dict:
    """Classify declared resource use without executing or billing anything."""
    if usage_mode not in USAGE_MODES:
        raise ValueError(f"unsupported usage mode: {usage_mode}")
    if platform_service_model not in SERVICE_MODELS:
        raise ValueError(
            f"unsupported platform service model: {platform_service_model}"
        )

    resource_count = max(0, int(external_resource_count))
    agents = max(0, int(agent_count))
    uses_external = resource_count > 0
    uncontrolled_multi_agent = agents > 1 and uses_external and not budget_controlled

    if uncontrolled_multi_agent:
        cost_level = risk_level = "very_high"
    elif usage_mode == "enterprise_mode" or (
        usage_mode == "agent_mode" and continuous_execution
    ):
        cost_level = risk_level = "high"
    elif repeated_external_calls or uses_external:
        cost_level = risk_level = "medium"
    else:
        cost_level = risk_level = "low"

    budget_warning = cost_level in {"high", "very_high"} or (
        repeated_external_calls and uses_external
    )
    requires_approval = uses_external and (
        repeated_external_calls
        or continuous_execution
        or agents > 0
        or cost_level in {"high", "very_high"}
    )
    resource_text = (
        "No external resource consumption is proposed."
        if not uses_external
        else f"{resource_count} external resource class(es) are proposed, owned by {external_resource_owner}."
    )
    approval_text = (
        "Explicit user approval is required before execution."
        if requires_approval
        else "No additional approval is triggered by the current profile."
    )

    return {
        "usage_mode": usage_mode,
        "external_resource_owner": external_resource_owner,
        "estimated_cost_level": cost_level,
        "budget_warning": budget_warning,
        "requires_user_approval": requires_approval,
        "platform_service_model": platform_service_model,
        "agentic_risk_level": risk_level,
        "governance_summary": (
            f"{usage_mode} is classified at {cost_level} estimated cost and "
            f"{risk_level} agentic risk. {resource_text} {approval_text} "
            "This is a governance estimate only; no billing, payment, "
            "subscription, or resource call is performed."
        ),
    }


def governance_for_scenario(scenario_id: str, profiles: dict | None = None) -> dict:
    profiles = profiles or load_usage_profiles()
    profile = {
        **profiles["default"],
        **profiles.get("scenarios", {}).get(scenario_id, {}),
    }
    return derive_usage_cost_governance(**profile)


def _append_report_section(path: Path, marker: str, lines: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    text = text.split(marker, 1)[0].rstrip()
    path.write_text(text + "\n\n" + "\n".join(lines) + "\n", encoding="utf-8")


def augment_runtime_outputs() -> list[dict]:
    """Add governance readings to generated CSV and Markdown reports."""
    matrix_path = OUTPUT_DIR / "comparison_matrix.csv"
    with matrix_path.open("r", encoding="utf-8", newline="") as file_obj:
        reader = csv.DictReader(file_obj)
        base_fields = [
            field for field in (reader.fieldnames or []) if field not in GOVERNANCE_FIELDS
        ]
        rows = list(reader)

    for row in rows:
        row.update(governance_for_scenario(row["scenario_id"]))

    with matrix_path.open("w", encoding="utf-8", newline="") as file_obj:
        writer = csv.DictWriter(
            file_obj, fieldnames=base_fields + GOVERNANCE_FIELDS, lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)

    scenario_lines = [
        "## Usage & Cost Governance Reading",
        "",
        "These are pre-execution governance classifications. They do not measure actual consumption or perform billing.",
    ]
    for row in rows:
        scenario_lines.extend(
            [
                "",
                f"### {row['scenario_name']}",
                "",
                f"- Usage mode: {row['usage_mode']}",
                f"- External resource owner: {row['external_resource_owner']}",
                f"- Estimated cost level: {row['estimated_cost_level']}",
                f"- Budget warning: {row['budget_warning']}",
                f"- Requires user approval: {row['requires_user_approval']}",
                f"- Platform service model: {row['platform_service_model']}",
                f"- Agentic risk level: {row['agentic_risk_level']}",
                f"- Governance summary: {row['governance_summary']}",
            ]
        )
    _append_report_section(
        OUTPUT_DIR / "scenario_report.md",
        "\n## Usage & Cost Governance Reading\n",
        scenario_lines,
    )

    approvals = [
        row["scenario_name"]
        for row in rows
        if str(row["requires_user_approval"]).lower() == "true"
    ]
    warnings = [
        row["scenario_name"]
        for row in rows
        if str(row["budget_warning"]).lower() == "true"
    ]
    cost_rank = {"low": 1, "medium": 2, "high": 3, "very_high": 4}
    highest = max(rows, key=lambda row: cost_rank[row["estimated_cost_level"]])
    governance_lines = [
        "## Usage & Cost Governance Reading",
        "",
        f"- Scenarios requiring explicit approval: {', '.join(approvals) or 'None'}.",
        f"- Scenarios carrying budget warnings: {', '.join(warnings) or 'None'}.",
        f"- Highest estimated cost level: {highest['estimated_cost_level']} ({highest['scenario_name']}).",
        "- Resource owners and service models remain visible in the comparison matrix.",
        "- Boundary: qualitative governance only; no external call, billing, payment, subscription, or invoice is performed.",
    ]
    _append_report_section(
        OUTPUT_DIR / "governance_summary.md",
        "\n## Usage & Cost Governance Reading\n",
        governance_lines,
    )
    system_lines = [
        "## Task 19 Usage and Cost Governance Validation",
        "",
        "Task 19 adds a deterministic pre-execution governance layer. It exposes usage mode, resource ownership, qualitative cost, budget warnings, approval requirements, service model, agentic risk, and a governance summary for every scenario.",
        "",
        "The profiles are declared fixtures, not measured consumption. Cost levels are qualitative rather than currency prices. A true approval flag is an advisory stop condition for a future execution layer; it does not grant or record approval.",
        "",
        "The runtime does not call external services, meter usage, calculate provider charges, enforce budgets, process billing, collect payments, create subscriptions, issue invoices, use crypto payments, operate token systems, or create resource marketplaces.",
    ]
    _append_report_section(
        REPO_ROOT / "docs" / "CCZPS_LITE_SYSTEM_VALIDATION_REPORT.md",
        "\n## Task 19 Usage and Cost Governance Validation\n",
        system_lines,
    )
    return rows


def main() -> None:
    augment_runtime_outputs()
    print("Added usage and cost governance readings to CCZPS-Lite outputs")


if __name__ == "__main__":
    main()
