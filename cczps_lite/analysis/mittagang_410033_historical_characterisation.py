"""L2 historical characterisation for BoM HRS gauge 410033.

The module intentionally uses only the Python standard library.  It derives
descriptive indicators from the exact official product admitted by the
Task2091–2100 intake.  It does not estimate current flow, water availability,
causality, engineering performance, or public safety.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any, Iterable, Sequence

from cczps_lite.integration.mittagang_410033_flow_intake import (
    SOURCE_URL,
    parse_daily_flow,
)

SCHEMA_ID = "climateos.mittagang_410033_historical_characterisation.v0.1"
ANSWER_SCHEMA_ID = "climateos.time_bounded_environmental_answer.v0.1"
PASSPORT_SCHEMA_ID = "climateos.environmental_evidence_passport.v0.1"
RUN_ID = "MITTAGANG-410033-HISTORICAL-CHARACTERISATION-V0.1"
METHOD_VERSION = "0.1.0"
CONCLUSION_LEVELS = {"L0", "L1", "L2", "L3", "L4"}
EVIDENCE_STAGES = {f"S{index}" for index in range(8)}
QUALITY_CODES = ("A", "B", "C", "E", "G")
SCREENED_QUALITY_CODES = {"A", "B"}
MONTH_NAMES = (
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
)
SEASONS = {
    12: "Summer (DJF)",
    1: "Summer (DJF)",
    2: "Summer (DJF)",
    3: "Autumn (MAM)",
    4: "Autumn (MAM)",
    5: "Autumn (MAM)",
    6: "Winter (JJA)",
    7: "Winter (JJA)",
    8: "Winter (JJA)",
    9: "Spring (SON)",
    10: "Spring (SON)",
    11: "Spring (SON)",
}
REQUIRED_ANSWER_FIELDS = {
    "answer_id",
    "question",
    "decision_use",
    "place",
    "spatial_boundary",
    "assessment_period",
    "evidence_cutoff",
    "issued_at",
    "valid_until",
    "conclusion_level",
    "evidence_maturity",
    "answer",
    "confidence",
    "supporting_evidence",
    "conflicting_evidence",
    "missing_critical_evidence",
    "local_translation_path",
    "alternative_explanations",
    "consequence_if_true",
    "consequence_if_false",
    "intervention_window",
    "permitted_actions",
    "prohibited_actions",
    "update_triggers",
    "demotion_triggers",
    "stop_conditions",
    "human_review",
    "official_confirmation",
    "retrospective_validation",
}


class HistoricalCharacterisationError(ValueError):
    """Raised when the L2 method boundary or input contract is violated."""


@dataclass(frozen=True)
class FlowObservation:
    observation_date: date
    flow_ml_per_day: float
    quality_code: str


def _sha256_bytes(body: bytes) -> str:
    return "sha256:" + hashlib.sha256(body).hexdigest()


def _sha256_text(text: str) -> str:
    return _sha256_bytes(text.encode("utf-8"))


def _is_leap_year(year: int) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def _expected_days(year: int) -> int:
    return 366 if _is_leap_year(year) else 365


def _quantile(values: Sequence[float], probability: float) -> float:
    if not values:
        raise HistoricalCharacterisationError("Cannot calculate an empty quantile")
    if not 0 <= probability <= 1:
        raise HistoricalCharacterisationError("Quantile probability is outside 0–1")
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] + (ordered[upper] - ordered[lower]) * fraction


def _rounded(value: float | None, digits: int = 3) -> float | None:
    return None if value is None else round(value, digits)


def _distribution(values: Sequence[float]) -> dict[str, Any]:
    if not values:
        return {
            "count": 0,
            "mean_ml_per_day": None,
            "p10_ml_per_day": None,
            "p25_ml_per_day": None,
            "median_ml_per_day": None,
            "p75_ml_per_day": None,
            "p90_ml_per_day": None,
            "p95_ml_per_day": None,
            "maximum_ml_per_day": None,
        }
    return {
        "count": len(values),
        "mean_ml_per_day": _rounded(sum(values) / len(values)),
        "p10_ml_per_day": _rounded(_quantile(values, 0.10)),
        "p25_ml_per_day": _rounded(_quantile(values, 0.25)),
        "median_ml_per_day": _rounded(_quantile(values, 0.50)),
        "p75_ml_per_day": _rounded(_quantile(values, 0.75)),
        "p90_ml_per_day": _rounded(_quantile(values, 0.90)),
        "p95_ml_per_day": _rounded(_quantile(values, 0.95)),
        "maximum_ml_per_day": _rounded(max(values)),
    }


def parse_observations(body: bytes) -> tuple[list[FlowObservation], dict[str, Any]]:
    """Return validated observations plus the L1 intake metadata."""
    metadata = parse_daily_flow(body)
    rows = list(csv.reader(body.decode("utf-8-sig").splitlines()))
    try:
        header_index = rows.index(["Date", "Flow (ML)", "Bureau QCode"])
    except ValueError as exc:  # pragma: no cover - guarded by intake parser
        raise HistoricalCharacterisationError("Expected flow header is missing") from exc
    observations: list[FlowObservation] = []
    for row in rows[header_index + 1 :]:
        if len(row) != 3:
            raise HistoricalCharacterisationError("Invalid observation row")
        observation = FlowObservation(
            observation_date=date.fromisoformat(row[0]),
            flow_ml_per_day=float(row[1]),
            quality_code=row[2],
        )
        if observation.flow_ml_per_day < 0:
            raise HistoricalCharacterisationError("Negative daily flow is unsupported")
        observations.append(observation)
    if len(observations) != metadata["row_count"]:
        raise HistoricalCharacterisationError("Observation count changed after intake")
    return observations, metadata


def _group_distribution(
    observations: Iterable[FlowObservation],
) -> dict[str, Any]:
    rows = list(observations)
    all_values = [row.flow_ml_per_day for row in rows]
    screened_values = [
        row.flow_ml_per_day
        for row in rows
        if row.quality_code in SCREENED_QUALITY_CODES
    ]
    return {
        "all_published": _distribution(all_values),
        "quality_screen_a_b": _distribution(screened_values),
        "quality_screen_a_b_share": _rounded(
            len(screened_values) / len(all_values) if all_values else None, 6
        ),
    }


def _monthly_profile(
    observations: Sequence[FlowObservation],
) -> list[dict[str, Any]]:
    grouped: dict[int, list[FlowObservation]] = defaultdict(list)
    for observation in observations:
        grouped[observation.observation_date.month].append(observation)
    return [
        {
            "month": month,
            "month_name": MONTH_NAMES[month - 1],
            **_group_distribution(grouped[month]),
        }
        for month in range(1, 13)
    ]


def _seasonal_profile(
    observations: Sequence[FlowObservation],
) -> list[dict[str, Any]]:
    grouped: dict[str, list[FlowObservation]] = defaultdict(list)
    for observation in observations:
        grouped[SEASONS[observation.observation_date.month]].append(observation)
    order = ("Summer (DJF)", "Autumn (MAM)", "Winter (JJA)", "Spring (SON)")
    return [
        {"season": season, **_group_distribution(grouped[season])}
        for season in order
    ]


def _annual_profile(
    observations: Sequence[FlowObservation],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    grouped: dict[int, list[FlowObservation]] = defaultdict(list)
    for observation in observations:
        grouped[observation.observation_date.year].append(observation)
    all_years: list[dict[str, Any]] = []
    complete_years: list[dict[str, Any]] = []
    for year in sorted(grouped):
        rows = grouped[year]
        quality_counts = Counter(row.quality_code for row in rows)
        record = {
            "year": year,
            "calendar_day_count": len(rows),
            "complete_calendar_year": len(rows) == _expected_days(year),
            "quality_code_counts": {
                code: quality_counts.get(code, 0) for code in QUALITY_CODES
            },
            **_group_distribution(rows),
        }
        all_years.append(record)
        if record["complete_calendar_year"]:
            complete_years.append(record)
    return all_years, complete_years


def _decadal_profile(
    observations: Sequence[FlowObservation],
) -> list[dict[str, Any]]:
    grouped: dict[int, list[FlowObservation]] = defaultdict(list)
    for observation in observations:
        decade = (observation.observation_date.year // 10) * 10
        grouped[decade].append(observation)
    output = []
    for decade in sorted(grouped):
        rows = grouped[decade]
        counts = Counter(row.quality_code for row in rows)
        output.append(
            {
                "decade": decade,
                "period": (
                    f"{min(row.observation_date for row in rows).isoformat()}/"
                    f"{max(row.observation_date for row in rows).isoformat()}"
                ),
                "quality_code_counts": {
                    code: counts.get(code, 0) for code in QUALITY_CODES
                },
                **_group_distribution(rows),
            }
        )
    return output


def characterise(
    body: bytes,
    *,
    issued_at: str,
    retrieval_receipt_digest: str | None = None,
) -> dict[str, Any]:
    """Calculate bounded L2 historical indicators."""
    observations, metadata = parse_observations(body)
    quality_counts = Counter(row.quality_code for row in observations)
    overall = _group_distribution(observations)
    annual_all, annual_complete = _annual_profile(observations)
    all_median = overall["all_published"]["median_ml_per_day"]
    screened_median = overall["quality_screen_a_b"]["median_ml_per_day"]
    median_sensitivity_percent = (
        None
        if all_median in (None, 0) or screened_median is None
        else _rounded((screened_median - all_median) / all_median * 100, 2)
    )
    return {
        "schema_id": SCHEMA_ID,
        "run_id": RUN_ID,
        "method_version": METHOD_VERSION,
        "issued_at": issued_at,
        "source": {
            "publisher": metadata["publisher"],
            "product_family": metadata["product_family"],
            "station_id": metadata["station_id"],
            "station_name": metadata["station_name"],
            "url": SOURCE_URL,
            "content_digest": _sha256_bytes(body),
            "retrieval_receipt_digest": retrieval_receipt_digest,
            "dataset_version": metadata["dataset_version"],
            "data_extraction_date": metadata["data_extraction_date"],
        },
        "boundary": {
            "spatial": "BoM HRS gauge 410033 record; no catchment-wide inference",
            "measurement": "daily streamflow",
            "unit": "ML/day",
            "coverage_start": metadata["coverage_start"],
            "coverage_end": metadata["coverage_end"],
            "day_boundary": "09:00 source-local time for previous 24 hours",
            "iana_timezone": None,
        },
        "quality_profile": {
            "row_count": len(observations),
            "missing_calendar_date_count": metadata["missing_calendar_date_count"],
            "blank_flow_value_count": metadata["blank_flow_value_count"],
            "duplicate_date_count": metadata["duplicate_date_count"],
            "quality_code_counts": {
                code: quality_counts.get(code, 0) for code in QUALITY_CODES
            },
            "quality_code_shares": {
                code: _rounded(quality_counts.get(code, 0) / len(observations), 6)
                for code in QUALITY_CODES
            },
            "source_definitions": {
                "A": "Best available data",
                "B": "Good data",
                "C": "Poor data",
                "E": "Unreliable data",
                "G": "Gap filled data",
            },
            "primary_published_series": "All source-published rows, with quality visible",
            "sensitivity_screen": "A+B only; not treated as a replacement dataset",
        },
        "overall_distribution": overall,
        "monthly_profile": _monthly_profile(observations),
        "seasonal_profile": _seasonal_profile(observations),
        "annual_profile_all": annual_all,
        "annual_profile_complete_years": annual_complete,
        "decadal_profile": _decadal_profile(observations),
        "sensitivity": {
            "all_published_median_ml_per_day": all_median,
            "a_b_screen_median_ml_per_day": screened_median,
            "a_b_minus_all_median_percent": median_sensitivity_percent,
            "interpretation": (
                "A difference between the all-published and A+B-screened "
                "summaries demonstrates method sensitivity; it is not an "
                "estimate of measurement error."
            ),
        },
        "trend_assessment": {
            "status": "NOT_PERFORMED_IN_V0_1",
            "reason": (
                "Quality-code composition changes materially through the record. "
                "A trend or change-point claim requires a separately reviewed "
                "method that addresses quality, serial dependence, seasonality "
                "and multiple testing."
            ),
        },
        "maximum_conclusion_level": "L2",
        "evidence_maturity": "S0",
        "prohibited_conclusions": [
            "current 2026 flow",
            "Cooma drinking-water sufficiency or safety",
            "reservoir storage or demand balance",
            "causal attribution",
            "engineering, wastewater or public-safety status",
            "catchment-wide behaviour",
        ],
    }


def validate_time_bounded_answer(answer: dict[str, Any]) -> None:
    missing = sorted(REQUIRED_ANSWER_FIELDS - answer.keys())
    if missing:
        raise HistoricalCharacterisationError(
            f"Time-bounded answer fields are missing: {missing}"
        )
    if answer.get("schema_id") != ANSWER_SCHEMA_ID:
        raise HistoricalCharacterisationError("Unexpected answer schema")
    if answer["conclusion_level"] not in CONCLUSION_LEVELS:
        raise HistoricalCharacterisationError("Invalid conclusion level")
    if answer["evidence_maturity"] not in EVIDENCE_STAGES:
        raise HistoricalCharacterisationError("Invalid evidence maturity")
    if not answer["valid_until"]:
        raise HistoricalCharacterisationError("Answer validity is required")
    if answer["conclusion_level"] != "L2":
        raise HistoricalCharacterisationError("This method can issue L2 only")
    if answer["evidence_maturity"] != "S0":
        raise HistoricalCharacterisationError(
            "Historical baseline characterisation must remain S0"
        )


def build_time_bounded_answer(
    result: dict[str, Any],
    *,
    issued_at: str,
) -> dict[str, Any]:
    overall = result["overall_distribution"]["all_published"]
    quality = result["quality_profile"]
    answer = {
        "schema_id": ANSWER_SCHEMA_ID,
        "answer_id": "MITTAGANG-410033-HISTORICAL-ANSWER-V0.1",
        "question": (
            "What does the admitted 1964-03-01 to 2024-02-29 daily streamflow "
            "record for Murrumbidgee River at Mittagang Crossing show about "
            "historical coverage, seasonality, variability and source quality?"
        ),
        "decision_use": (
            "Historical baseline and method foundation for later, separately "
            "admitted near-current comparison"
        ),
        "place": "Murrumbidgee River at Mittagang Crossing, gauge 410033",
        "spatial_boundary": result["boundary"]["spatial"],
        "assessment_period": "1964-03-01/2024-02-29",
        "evidence_cutoff": "2024-02-29",
        "issued_at": issued_at,
        "valid_until": (
            "Until the source digest, source quality definitions, station "
            "identity or method version changes"
        ),
        "conclusion_level": "L2",
        "evidence_maturity": "S0",
        "answer": (
            f"For the declared gauge record and method, {quality['row_count']:,} "
            "daily values cover every calendar date from 1964-03-01 to "
            f"2024-02-29. The all-published daily median is "
            f"{overall['median_ml_per_day']:,.3f} ML/day and the central "
            f"80% spans {overall['p10_ml_per_day']:,.3f} to "
            f"{overall['p90_ml_per_day']:,.3f} ML/day. Monthly and annual "
            "distributions vary substantially. These are historical descriptive "
            "indicators, not a statement of current conditions."
        ),
        "confidence": (
            "High for computational reproducibility and calendar coverage; "
            "limited for treating all values as equivalent observations because "
            "source quality categories include C and E."
        ),
        "supporting_evidence": [
            result["source"]["content_digest"],
            "BoM HRS station identity and source quality codes",
            "complete daily calendar coverage in the admitted record",
            "reproducible standard-library method and tests",
        ],
        "conflicting_evidence": [
            (
                "All-published and A+B-screened summaries differ; the sensitivity "
                "is recorded rather than averaged away."
            )
        ],
        "missing_critical_evidence": [
            "equivalent-method observations after 2024-02-29",
            "qualified hydrology review",
            "uncertainty model beyond source quality categories",
            "storage, extraction, demand, rainfall and snow evidence",
        ],
        "local_translation_path": [
            "official gauge record",
            "quality-aware historical distributions",
            "future equivalent-method near-current comparison",
        ],
        "alternative_explanations": [
            (
                "Differences across years or decades may reflect hydrology, "
                "quality classification, gauging or source-processing changes."
            )
        ],
        "consequence_if_true": (
            "A lawful reproducible historical baseline is available for bounded "
            "future comparison."
        ),
        "consequence_if_false": (
            "If source identity, digest or method checks fail, the derived "
            "indicators must be withdrawn and recomputed."
        ),
        "intervention_window": (
            "No environmental intervention is supported; the current window is "
            "for method review and evidence preparation only."
        ),
        "permitted_actions": [
            "review the method and quality sensitivity",
            "prepare an equivalent-method near-current evidence gate",
            "request qualified hydrology review",
        ],
        "prohibited_actions": [
            "represent the result as current 2026 flow",
            "infer water sufficiency, safety, causality or engineering status",
            "issue a public warning",
        ],
        "update_triggers": [
            "source digest or dataset version changes",
            "new equivalent-method flow record is lawfully admitted",
            "quality-code definitions or station identity change",
            "method version changes",
        ],
        "demotion_triggers": [
            "source correction",
            "calculation error",
            "licence or provenance failure",
            "qualified review identifies a material method defect",
        ],
        "stop_conditions": [
            "attempted use for current conditions or public safety",
            "unresolved source identity mismatch",
            "silent exclusion or relabelling of quality categories",
        ],
        "human_review": {
            "status": "FOUNDER_EVIDENCE_REVIEW_PENDING",
            "qualified_hydrology_review": "REQUIRED_BEFORE_L3",
            "review_questions": [
                "Is the A+B sensitivity framing defensible?",
                "Which uncertainty treatment is required before trend analysis?",
                "Is the gauge boundary fit for a proposed later local question?",
            ],
        },
        "official_confirmation": {
            "issuer": "Australian Bureau of Meteorology",
            "scope": "official HRS source record and quality classification",
            "relationship_to_answer": (
                "Supports source identity and L1 facts; does not itself confirm "
                "the L2 calculations or any current local condition."
            ),
        },
        "retrospective_validation": {
            "plan": (
                "On source or method update, rerun from the exact admitted bytes, "
                "compare output digests and indicators, explain differences, and "
                "preserve the prior version."
            ),
            "status": "PLANNED",
        },
    }
    validate_time_bounded_answer(answer)
    return answer


def build_evidence_passport(
    result: dict[str, Any], answer: dict[str, Any]
) -> dict[str, Any]:
    return {
        "schema_id": PASSPORT_SCHEMA_ID,
        "passport_id": "MITTAGANG-410033-HISTORICAL-PASSPORT-V0.1",
        "subject": "Historical daily streamflow characterisation",
        "source_identity": result["source"],
        "method": {
            "run_id": result["run_id"],
            "version": result["method_version"],
            "unit": "ML/day",
            "calendar_basis": "source-local daily record",
            "quality_treatment": result["quality_profile"][
                "sensitivity_screen"
            ],
        },
        "derived_claim": {
            "answer_id": answer["answer_id"],
            "conclusion_level": answer["conclusion_level"],
            "evidence_maturity": answer["evidence_maturity"],
            "evidence_cutoff": answer["evidence_cutoff"],
        },
        "limitations": {
            "missing_critical_evidence": answer["missing_critical_evidence"],
            "prohibited_actions": answer["prohibited_actions"],
            "trend_status": result["trend_assessment"]["status"],
        },
        "review": answer["human_review"],
        "retrospective_validation": answer["retrospective_validation"],
    }


def _write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field) for field in fields})


def _svg_escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _line_chart_svg(
    *,
    title: str,
    subtitle: str,
    labels: Sequence[str],
    series: Sequence[tuple[str, Sequence[float | None], str]],
    y_label: str,
    width: int = 1120,
    height: int = 620,
) -> str:
    margin_left, margin_right, margin_top, margin_bottom = 90, 40, 100, 90
    plot_width = width - margin_left - margin_right
    plot_height = height - margin_top - margin_bottom
    numeric = [
        value
        for _, values, _ in series
        for value in values
        if value is not None and math.isfinite(value)
    ]
    y_min = 0.0
    y_max = max(numeric) if numeric else 1.0
    y_max = max(1.0, y_max * 1.08)

    def x_position(index: int) -> float:
        return margin_left + (
            plot_width * index / max(1, len(labels) - 1)
        )

    def y_position(value: float) -> float:
        return margin_top + plot_height * (1 - (value - y_min) / (y_max - y_min))

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
        f'height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#fbfcfa"/>',
        f'<text x="{margin_left}" y="38" font-family="Arial, sans-serif" '
        f'font-size="24" font-weight="700" fill="#183a2d">{_svg_escape(title)}</text>',
        f'<text x="{margin_left}" y="66" font-family="Arial, sans-serif" '
        f'font-size="14" fill="#53645d">{_svg_escape(subtitle)}</text>',
    ]
    for tick in range(6):
        value = y_max * tick / 5
        y = y_position(value)
        lines.extend(
            [
                f'<line x1="{margin_left}" y1="{y:.2f}" x2="{width-margin_right}" '
                'y2="{:.2f}" stroke="#dce5e0" stroke-width="1"/>'.format(y),
                f'<text x="{margin_left-12}" y="{y+5:.2f}" text-anchor="end" '
                'font-family="Arial, sans-serif" font-size="12" fill="#53645d">'
                f"{value:,.0f}</text>",
            ]
        )
    for index, label in enumerate(labels):
        x = x_position(index)
        lines.append(
            f'<text x="{x:.2f}" y="{height-margin_bottom+28}" text-anchor="middle" '
            'font-family="Arial, sans-serif" font-size="11" fill="#53645d">'
            f"{_svg_escape(label)}</text>"
        )
    for name, values, colour in series:
        segments: list[list[str]] = []
        current_segment: list[str] = []
        for index, value in enumerate(values):
            if value is None:
                if current_segment:
                    segments.append(current_segment)
                    current_segment = []
                continue
            current_segment.append(
                f"{x_position(index):.2f},{y_position(value):.2f}"
            )
        if current_segment:
            segments.append(current_segment)
        for points in segments:
            lines.append(
                f'<polyline points="{" ".join(points)}" fill="none" '
                f'stroke="{colour}" stroke-width="3" stroke-linejoin="round" '
                'stroke-linecap="round"/>'
            )
    lines.append(
        f'<text x="24" y="{margin_top + plot_height/2:.2f}" '
        'transform="rotate(-90 24 {:.2f})" text-anchor="middle" '
        'font-family="Arial, sans-serif" font-size="13" fill="#374c43">'
        f"{_svg_escape(y_label)}</text>".format(margin_top + plot_height / 2)
    )
    legend_x = margin_left
    legend_y = height - 22
    for name, _, colour in series:
        lines.extend(
            [
                f'<line x1="{legend_x}" y1="{legend_y-5}" x2="{legend_x+26}" '
                f'y2="{legend_y-5}" stroke="{colour}" stroke-width="4"/>',
                f'<text x="{legend_x+34}" y="{legend_y}" '
                'font-family="Arial, sans-serif" font-size="12" fill="#374c43">'
                f"{_svg_escape(name)}</text>",
            ]
        )
        legend_x += 230
    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def _quality_chart_svg(result: dict[str, Any]) -> str:
    decades = result["decadal_profile"]
    width, height = 1120, 620
    left, right, top, bottom = 90, 40, 105, 95
    plot_width = width - left - right
    plot_height = height - top - bottom
    colours = {
        "A": "#146c43",
        "B": "#55a868",
        "C": "#e5a84b",
        "E": "#c95d63",
        "G": "#6f7c91",
    }
    bar_width = plot_width / max(1, len(decades)) * 0.64
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
        f'height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#fbfcfa"/>',
        f'<text x="{left}" y="38" font-family="Arial, sans-serif" '
        'font-size="24" font-weight="700" fill="#183a2d">'
        "Source quality-code composition by decade</text>",
        f'<text x="{left}" y="66" font-family="Arial, sans-serif" '
        'font-size="14" fill="#53645d">'
        "Shares describe source classifications; they are not uncertainty estimates."
        "</text>",
    ]
    for tick in range(6):
        share = tick / 5
        y = top + plot_height * (1 - share)
        lines.extend(
            [
                f'<line x1="{left}" y1="{y:.2f}" x2="{width-right}" y2="{y:.2f}" '
                'stroke="#dce5e0" stroke-width="1"/>',
                f'<text x="{left-12}" y="{y+5:.2f}" text-anchor="end" '
                'font-family="Arial, sans-serif" font-size="12" fill="#53645d">'
                f"{share:.0%}</text>",
            ]
        )
    for index, decade in enumerate(decades):
        counts = decade["quality_code_counts"]
        total = sum(counts.values())
        x = left + plot_width * (index + 0.5) / len(decades) - bar_width / 2
        y_cursor = top + plot_height
        for code in QUALITY_CODES:
            segment_height = plot_height * counts[code] / total if total else 0
            y_cursor -= segment_height
            lines.append(
                f'<rect x="{x:.2f}" y="{y_cursor:.2f}" width="{bar_width:.2f}" '
                f'height="{segment_height:.2f}" fill="{colours[code]}"/>'
            )
        lines.append(
            f'<text x="{x+bar_width/2:.2f}" y="{height-bottom+28}" '
            'text-anchor="middle" font-family="Arial, sans-serif" '
            f'font-size="12" fill="#53645d">{decade["decade"]}s</text>'
        )
    legend_x, legend_y = left, height - 24
    for code in QUALITY_CODES:
        lines.extend(
            [
                f'<rect x="{legend_x}" y="{legend_y-12}" width="16" height="12" '
                f'fill="{colours[code]}"/>',
                f'<text x="{legend_x+23}" y="{legend_y}" '
                'font-family="Arial, sans-serif" font-size="12" fill="#374c43">'
                f"{code}</text>",
            ]
        )
        legend_x += 95
    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def _method_note(
    result: dict[str, Any],
    answer: dict[str, Any],
    output_digests: dict[str, str],
) -> str:
    def display(value: float | None) -> str:
        return "N/A" if value is None else f"{value:,.3f}"

    quality = result["quality_profile"]
    all_dist = result["overall_distribution"]["all_published"]
    screened = result["overall_distribution"]["quality_screen_a_b"]
    monthly_rows = "\n".join(
        "| {month_name} | {a} | {b} | {p10} | {p90} |".format(
            month_name=row["month_name"],
            a=display(row["all_published"]["median_ml_per_day"]),
            b=display(row["quality_screen_a_b"]["median_ml_per_day"]),
            p10=display(row["all_published"]["p10_ml_per_day"]),
            p90=display(row["all_published"]["p90_ml_per_day"]),
        )
        for row in result["monthly_profile"]
    )
    return f"""# Mittagang 410033 Historical Daily Streamflow Characterisation v0.1

## Bounded answer

{answer["answer"]}

**State:** `S0 BASELINE_MONITORING / L2 DESCRIPTIVE_INDICATOR`  
**Evidence cut-off:** `2024-02-29`  
**Current-condition conclusion:** `NOT SUPPORTED`

## Dataset and grain

- Publisher: Australian Bureau of Meteorology, Hydrologic Reference Stations.
- Gauge: 410033, Murrumbidgee River at Mittagang Crossing.
- Grain: one source-local daily streamflow value, `ML/day`.
- Coverage: `{result["boundary"]["coverage_start"]}` to
  `{result["boundary"]["coverage_end"]}`.
- Rows: `{quality["row_count"]:,}`; missing dates:
  `{quality["missing_calendar_date_count"]}`; blank values:
  `{quality["blank_flow_value_count"]}`; duplicate dates:
  `{quality["duplicate_date_count"]}`.
- Exact source digest: `{result["source"]["content_digest"]}`.

## Quality treatment

The primary description retains every source-published value and keeps its
quality code visible. A separate A+B-only sensitivity screen is reported; it
does not silently replace the official series.

| Code | Source meaning | Count | Share |
|---|---|---:|---:|
| A | Best available data | {quality["quality_code_counts"]["A"]:,} | {quality["quality_code_shares"]["A"]:.1%} |
| B | Good data | {quality["quality_code_counts"]["B"]:,} | {quality["quality_code_shares"]["B"]:.1%} |
| C | Poor data | {quality["quality_code_counts"]["C"]:,} | {quality["quality_code_shares"]["C"]:.1%} |
| E | Unreliable data | {quality["quality_code_counts"]["E"]:,} | {quality["quality_code_shares"]["E"]:.1%} |
| G | Gap filled data | {quality["quality_code_counts"]["G"]:,} | {quality["quality_code_shares"]["G"]:.1%} |

The source header also states that data gaps were filled with a daily
rainfall-runoff model, while the published rows contain no `G` code. This
apparent tension is preserved as a method limitation and requires hydrology
review; ClimateOS does not relabel rows.

## Overall distribution

| Method | Count | P10 | Median | P90 | Maximum |
|---|---:|---:|---:|---:|---:|
| All published | {all_dist["count"]:,} | {all_dist["p10_ml_per_day"]:,.3f} | {all_dist["median_ml_per_day"]:,.3f} | {all_dist["p90_ml_per_day"]:,.3f} | {all_dist["maximum_ml_per_day"]:,.3f} |
| A+B screen | {screened["count"]:,} | {screened["p10_ml_per_day"]:,.3f} | {screened["median_ml_per_day"]:,.3f} | {screened["p90_ml_per_day"]:,.3f} | {screened["maximum_ml_per_day"]:,.3f} |

The A+B-screened median differs from the all-published median by
`{result["sensitivity"]["a_b_minus_all_median_percent"]:+.2f}%`. This is method
sensitivity, not an estimate of measurement error.

## Monthly distribution

| Month | All median | A+B median | All P10 | All P90 |
|---|---:|---:|---:|---:|
{monthly_rows}

All values are `ML/day`.

![Monthly historical distribution](monthly_distribution.svg)

![Source quality composition](quality_composition_by_decade.svg)

## Annual and trend boundary

Annual distributions are published for all years, but cross-year comparison
uses only complete calendar years. The partial 1964 and 2024 years remain in
the daily and monthly record but are not treated as complete annual periods.

![Complete-year annual medians](annual_medians.svg)

No formal trend or change-point result is issued in v0.1. Source quality
composition changes materially through time; a later method must address
quality, serial dependence, seasonality and multiple testing before trend
language is permitted.

## What this establishes

- a reproducible historical distribution for this admitted gauge record;
- calendar coverage and source quality composition;
- monthly, seasonal, complete-year and decadal descriptive summaries;
- sensitivity to an explicit A+B quality screen.

## What this does not establish

- current 2026 flow;
- Cooma drinking-water sufficiency or safety;
- storage, extraction, demand or water balance;
- causes of historical variation;
- engineering, wastewater or public-safety status;
- catchment-wide behaviour.

## Human review and retrospective plan

Founder evidence review is the current gate. A qualified hydrology review is
required before any L3 promotion or formal trend method. If the source or
method changes, ClimateOS must preserve this version, rerun from exact admitted
bytes, compare output digests and indicators, and explain the differences.

## Output identity

```json
{json.dumps(output_digests, indent=2, ensure_ascii=False)}
```
"""


def write_outputs(
    result: dict[str, Any],
    output_root: str | Path,
    *,
    issued_at: str,
) -> dict[str, str]:
    root = Path(output_root)
    root.mkdir(parents=True, exist_ok=True)
    answer = build_time_bounded_answer(result, issued_at=issued_at)
    passport = build_evidence_passport(result, answer)

    result_path = root / "characterisation_receipt.json"
    answer_path = root / "time_bounded_environmental_answer.json"
    passport_path = root / "evidence_passport.json"
    result_path.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    answer_path.write_text(
        json.dumps(answer, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    passport_path.write_text(
        json.dumps(passport, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    monthly_rows = []
    for row in result["monthly_profile"]:
        monthly_rows.append(
            {
                "month": row["month"],
                "month_name": row["month_name"],
                "all_count": row["all_published"]["count"],
                "all_p10_ml_per_day": row["all_published"]["p10_ml_per_day"],
                "all_median_ml_per_day": row["all_published"]["median_ml_per_day"],
                "all_p90_ml_per_day": row["all_published"]["p90_ml_per_day"],
                "ab_count": row["quality_screen_a_b"]["count"],
                "ab_median_ml_per_day": row["quality_screen_a_b"][
                    "median_ml_per_day"
                ],
            }
        )
    _write_csv(
        root / "monthly_profile.csv",
        monthly_rows,
        list(monthly_rows[0]),
    )
    annual_rows = []
    for row in result["annual_profile_complete_years"]:
        annual_rows.append(
            {
                "year": row["year"],
                "all_count": row["all_published"]["count"],
                "all_median_ml_per_day": row["all_published"]["median_ml_per_day"],
                "all_p10_ml_per_day": row["all_published"]["p10_ml_per_day"],
                "all_p90_ml_per_day": row["all_published"]["p90_ml_per_day"],
                "ab_count": row["quality_screen_a_b"]["count"],
                "ab_median_ml_per_day": row["quality_screen_a_b"][
                    "median_ml_per_day"
                ],
                "quality_a": row["quality_code_counts"]["A"],
                "quality_b": row["quality_code_counts"]["B"],
                "quality_c": row["quality_code_counts"]["C"],
                "quality_e": row["quality_code_counts"]["E"],
                "quality_g": row["quality_code_counts"]["G"],
            }
        )
    annual_fields = [
        "year",
        "all_count",
        "all_median_ml_per_day",
        "all_p10_ml_per_day",
        "all_p90_ml_per_day",
        "ab_count",
        "ab_median_ml_per_day",
        "quality_a",
        "quality_b",
        "quality_c",
        "quality_e",
        "quality_g",
    ]
    _write_csv(
        root / "annual_complete_year_profile.csv",
        annual_rows,
        annual_fields,
    )

    monthly = result["monthly_profile"]
    (root / "monthly_distribution.svg").write_text(
        _line_chart_svg(
            title="Historical daily streamflow distribution by month",
            subtitle=(
                "Gauge 410033, 1964-03-01 to 2024-02-29; medians and "
                "all-published P10/P90"
            ),
            labels=[row["month_name"] for row in monthly],
            series=[
                (
                    "All-published median",
                    [row["all_published"]["median_ml_per_day"] for row in monthly],
                    "#146c43",
                ),
                (
                    "A+B-screen median",
                    [
                        row["quality_screen_a_b"]["median_ml_per_day"]
                        for row in monthly
                    ],
                    "#3f7cac",
                ),
                (
                    "All-published P10",
                    [row["all_published"]["p10_ml_per_day"] for row in monthly],
                    "#9cb8aa",
                ),
                (
                    "All-published P90",
                    [row["all_published"]["p90_ml_per_day"] for row in monthly],
                    "#d49b50",
                ),
            ],
            y_label="Daily streamflow (ML/day)",
        ),
        encoding="utf-8",
    )
    complete_years = result["annual_profile_complete_years"]
    annual_labels = [
        str(row["year"]) if row["year"] % 5 == 0 else ""
        for row in complete_years
    ]
    (root / "annual_medians.svg").write_text(
        _line_chart_svg(
            title="Complete-year daily streamflow medians",
            subtitle=(
                "Partial 1964 and 2024 years excluded; lines are descriptive, "
                "not a formal trend test"
            ),
            labels=annual_labels,
            series=[
                (
                    "All-published median",
                    [
                        row["all_published"]["median_ml_per_day"]
                        for row in complete_years
                    ],
                    "#146c43",
                ),
                (
                    "A+B-screen median",
                    [
                        row["quality_screen_a_b"]["median_ml_per_day"]
                        for row in complete_years
                    ],
                    "#3f7cac",
                ),
            ],
            y_label="Annual median daily streamflow (ML/day)",
        ),
        encoding="utf-8",
    )
    (root / "quality_composition_by_decade.svg").write_text(
        _quality_chart_svg(result), encoding="utf-8"
    )

    digest_paths = [
        result_path,
        answer_path,
        passport_path,
        root / "monthly_profile.csv",
        root / "annual_complete_year_profile.csv",
        root / "monthly_distribution.svg",
        root / "annual_medians.svg",
        root / "quality_composition_by_decade.svg",
    ]
    output_digests = {
        path.name: _sha256_bytes(path.read_bytes()) for path in digest_paths
    }
    method_note = _method_note(result, answer, output_digests)
    (root / "METHOD_AND_RESULTS.md").write_text(method_note, encoding="utf-8")
    output_digests["METHOD_AND_RESULTS.md"] = _sha256_text(method_note)
    (root / "run_receipt.json").write_text(
        json.dumps(
            {
                "schema_id": SCHEMA_ID,
                "run_id": RUN_ID,
                "method_version": METHOD_VERSION,
                "issued_at": issued_at,
                "source_digest": result["source"]["content_digest"],
                "conclusion_level": "L2",
                "evidence_maturity": "S0",
                "output_digests": output_digests,
                "human_review": answer["human_review"],
                "public_warning_issued": False,
                "current_condition_conclusion": None,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    return output_digests


def run_characterisation(
    raw_csv_path: str | Path,
    output_root: str | Path,
    *,
    issued_at: str | None = None,
    retrieval_receipt_path: str | Path | None = None,
) -> tuple[dict[str, Any], dict[str, str]]:
    timestamp = issued_at or (
        datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    )
    body = Path(raw_csv_path).read_bytes()
    receipt_digest = None
    if retrieval_receipt_path is not None:
        receipt_digest = _sha256_bytes(Path(retrieval_receipt_path).read_bytes())
    result = characterise(
        body,
        issued_at=timestamp,
        retrieval_receipt_digest=receipt_digest,
    )
    digests = write_outputs(result, output_root, issued_at=timestamp)
    return result, digests
