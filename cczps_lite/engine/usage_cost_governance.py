"""Usage and cost governance rules for CCZPS-Lite."""

from __future__ import annotations

import csv
import json
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = PROJECT_DIR.parent
PROFILE_PATH = PROJECT_DIR / "input" / "usage_cost_profiles.json"
OUTPUT_DIR = PROJECT_DIR / "output"

USAGE_MODES = {
    "idea_mode",
    "research_mode",
    "project_mode",
    "agent_mode",
    "enterprise_mode",
}
SERVICE_MODELS = {
    "open_source",
    "service_fee",
    "enterprise_support",
    "data_asset_service",
}
FEE_MODELS = {
    "none",
    "fixed",
    "percentage",
    "percentage_plus_fixed",
    "enterprise_agreement",
}
GOVERNANCE_FIELDS = [
    "usage_mode",
    "external_resource_owner",
    "external_cost_bearer",
    "platform_service_recipient",
    "estimated_cost_level",
    "estimated_external_resource_cost",
    "budget_warning",
    "requires_user_approval",
    "platform_service_model",
    "platform_service_fee_model",
    "platform_service_fee_estimate",
    "agentic_risk_level",
    "agentic_consumption_risk",
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
    external_cost_bearer: str | None = None,
    platform_service_recipient: str = "user",
    external_resource_count: int = 0,
    external_resource_types: list[str] | None = None,
    repeated_external_calls: bool = False,
    continuous_execution: bool = False,
    agent_count: int = 0,
    budget_controlled: bool = True,
    platform_service_model: str = "open_source",
    platform_service_fee_model: str = "none",
) -> dict:
    """Classify declared resource use without executing or billing anything."""
    if usage_mode not in USAGE_MODES:
        raise ValueError(f"unsupported usage mode: {usage_mode}")
    if platform_service_model not in SERVICE_MODELS:
        raise ValueError(
            f"unsupported platform service model: {platform_service_model}"
        )
    if platform_service_fee_model not in FEE_MODELS:
        raise ValueError(
            f"unsupported platform service fee model: {platform_service_fee_model}"
        )

    resource_count = max(0, int(external_resource_count))
    resource_types = sorted(set(external_resource_types or []))
    resource_count = max(resource_count, len(resource_types))
    agents = max(0, int(agent_count))
    uses_external = resource_count > 0
    cost_bearer = external_cost_bearer or external_resource_owner
    uncontrolled_multi_agent = agents > 1 and uses_external and not budget_controlled

    if uncontrolled_multi_agent:
        cost_level = risk_level = "very_high"
    elif usage_mode == "enterprise_mode" or (
        usage_mode == "agent_mode" and continuous_execution
    ):
        cost_level = risk_level = "high"
    elif usage_mode == "research_mode" or repeated_external_calls or uses_external:
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
    if platform_service_fee_model == "none":
        fee_estimate = "none"
    elif platform_service_fee_model == "fixed" and cost_level == "low":
        fee_estimate = "low"
    else:
        fee_estimate = cost_level
    resource_type_text = (
        f" Resource classes: {', '.join(resource_types)}."
        if resource_types
        else ""
    )
    resource_text = (
        "No external resource consumption is proposed."
        if not uses_external
        else (
            f"{resource_count} external resource class(es) are proposed, owned by "
            f"{external_resource_owner}; external costs belong to {cost_bearer}."
            f"{resource_type_text}"
        )
    )
    approval_text = (
        "Explicit user approval is required before execution."
        if requires_approval
        else "No additional approval is triggered by the current profile."
    )

    return {
        "usage_mode": usage_mode,
        "external_resource_owner": external_resource_owner,
        "external_cost_bearer": cost_bearer,
        "platform_service_recipient": platform_service_recipient,
        "estimated_cost_level": cost_level,
        "estimated_external_resource_cost": cost_level,
        "budget_warning": budget_warning,
        "requires_user_approval": requires_approval,
        "platform_service_model": platform_service_model,
        "platform_service_fee_model": platform_service_fee_model,
        "platform_service_fee_estimate": fee_estimate,
        "agentic_risk_level": risk_level,
        "agentic_consumption_risk": risk_level,
        "governance_summary": (
            f"{usage_mode} is classified at {cost_level} estimated cost and "
            f"{risk_level} agentic risk. {resource_text} {approval_text} "
            f"Platform services are provided to {platform_service_recipient} "
            f"under the {platform_service_fee_model} fee classification. "
            "This is a governance estimate only; no billing, payment, "
            "subscription, invoice, or resource call is performed."
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
                f"- External cost bearer: {row['external_cost_bearer']}",
                f"- Platform service recipient: {row['platform_service_recipient']}",
                f"- Estimated cost level: {row['estimated_cost_level']}",
                f"- Estimated external resource cost: {row['estimated_external_resource_cost']}",
                f"- Budget warning: {row['budget_warning']}",
                f"- Requires user approval: {row['requires_user_approval']}",
                f"- Platform service model: {row['platform_service_model']}",
                f"- Platform service fee model: {row['platform_service_fee_model']}",
                f"- Platform service fee estimate: {row['platform_service_fee_estimate']}",
                f"- Agentic risk level: {row['agentic_risk_level']}",
                f"- Agentic consumption risk: {row['agentic_consumption_risk']}",
                f"- Governance summary: {row['governance_summary']}",
            ]
        )
    _append_report_section(
        OUTPUT_DIR / "scenario_report.md",
        "\n## Usage & Cost Governance Reading\n",
        scenario_lines,
    )
    transparency_lines = [
        "## Cost Transparency Reading",
        "",
        "External costs belong to the declared resource consumer. Values below are qualitative classifications only.",
    ]
    for row in rows:
        transparency_lines.extend(
            [
                "",
                f"### {row['scenario_name']}",
                "",
                f"- External resource owner: {row['external_resource_owner']}",
                f"- External cost bearer: {row['external_cost_bearer']}",
                f"- Estimated external resource intensity: {row['estimated_external_resource_cost']}",
                f"- Platform governance service: {row['platform_service_model']}",
                f"- Platform service recipient: {row['platform_service_recipient']}",
                f"- Platform service fee model: {row['platform_service_fee_model']}",
                f"- Platform service fee estimate: {row['platform_service_fee_estimate']}",
                f"- Approval required: {row['requires_user_approval']}",
                f"- Agentic consumption risk: {row['agentic_consumption_risk']}",
            ]
        )
    _append_report_section(
        OUTPUT_DIR / "scenario_report.md",
        "\n## Cost Transparency Reading\n",
        transparency_lines,
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
        "- External resource costs belong to the declared external cost bearer; the platform does not silently absorb them.",
        "- Boundary: qualitative governance only; no external call, billing, payment, subscription, or invoice is performed.",
        "",
        "## Cost Transparency Reading",
        "",
        f"- Highest external resource intensity: {highest['estimated_external_resource_cost']} ({highest['scenario_name']}).",
        f"- Highest agentic consumption risk: {highest['agentic_consumption_risk']} ({highest['scenario_name']}).",
        "- Platform fee models and estimates are classifications only, not financial calculations.",
    ]
    _append_report_section(
        OUTPUT_DIR / "governance_summary.md",
        "\n## Usage & Cost Governance Reading\n",
        governance_lines,
    )
    system_lines = [
        "## Task 19 Usage and Cost Governance Validation",
        "",
        "Task 19 adds a deterministic pre-execution governance layer. It exposes usage mode, resource ownership, external cost bearer, platform service recipient, qualitative external cost, budget warnings, approval requirements, service and fee models, agentic consumption risk, and a governance summary for every scenario.",
        "",
        "The profiles are declared fixtures, not measured consumption. Cost levels are qualitative rather than currency prices. A true approval flag is an advisory stop condition for a future execution layer; it does not grant or record approval.",
        "",
        "The provider-agnostic structure can classify future NASA POWER, NOAA, ERA5, BOM, OpenAI, GIS, satellite, and sensor-network consumption without changing the governance schema.",
        "",
        "The runtime does not call external services, meter usage, calculate provider charges, enforce budgets, process billing, collect payments, create subscriptions, issue invoices, use crypto payments, operate token or RWA systems, or create resource marketplaces.",
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
