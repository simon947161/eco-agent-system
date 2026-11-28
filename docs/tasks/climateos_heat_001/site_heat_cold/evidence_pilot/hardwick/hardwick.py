"""Replay two published Hardwick operating summaries and emit a JSON evidence record."""
import argparse
import csv
import hashlib
import io
import json
import sys
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = "https://arena.gov.au/assets/2025/08/Hardwick-Meatworks-Heat-Pump-Installation-and-Power-Upgrade-Demonstration-Final-Report.pdf"
COLUMNS = (
    "period pdf_page runtime_logged_h runtime_annualized_h thermal_total_kw "
    "thermal_pump_kw thermal_oil_kw savings_total_gj_y savings_pump_gj_y savings_oil_gj_y"
).split()
EXPECTED = [("2023-10/2024-09", "3"), ("2024-10/2025-05", "4")]


def replay(raw):
    reader = csv.DictReader(io.StringIO(raw.decode("utf-8-sig")))
    if reader.fieldnames != COLUMNS:
        raise ValueError("invalid or duplicate column names")
    rows = list(reader)
    if [(r["period"], r["pdf_page"]) for r in rows] != EXPECTED:
        raise ValueError("missing, duplicate or out-of-order reporting periods")

    records = []
    hours, powers, heat = [], [], []
    for row in rows:
        if None in row or any(not (row[key] or "").isascii() or
                              not row[key].isdecimal() for key in COLUMNS[2:]):
            raise ValueError("expected complete unsigned integer values in published units")
        v = {k: int(row[k]) for k in COLUMNS[2:]}
        hours_y = v["runtime_annualized_h"]
        power = v["thermal_total_kw"]
        if not 0 < v["runtime_logged_h"] <= hours_y <= 8784 or not power:
            raise ValueError("impossible hours or zero power")
        if power != v["thermal_pump_kw"] + v["thermal_oil_kw"]:
            raise ValueError("power components disagree with total")
        hours.append(hours_y)
        powers.append(power)
        heat_mwh = Decimal(power * hours_y) / 1000
        heat.append(heat_mwh)
        residual = v["savings_pump_gj_y"] + v["savings_oil_gj_y"] - v["savings_total_gj_y"]
        records.append({
            "period": row["period"],
            "annualized_reconstructed_source_heat_mwh": heat_mwh,
            "annualized_reconstructed_source_heat_gj": heat_mwh * Decimal("3.6"),
            "reported_annualized_fuel_savings_total_gj": v["savings_total_gj_y"],
            "fuel_component_sum_minus_reported_total_gj": residual,
            "fuel_split_quality": "unreconciled" if residual else "reconciled",
        })

    delta = heat[1] - heat[0]
    hours_term = Decimal((hours[1] - hours[0]) * sum(powers)) / 2000
    power_term = Decimal((powers[1] - powers[0]) * sum(hours)) / 2000
    if hours_term + power_term != delta:
        raise ValueError("energy decomposition failed to close")

    return {
        "schema": "hardwick.aggregate.v1", "source_url": SOURCE,
        "source_pdf_sha256": "e1203d5c64cc1eafc027987248fc481176ed3b4f3a997822007d40eaab2a33d1", "input_csv_sha256": hashlib.sha256(raw).hexdigest(),
        "source_granularity": "two published period aggregates manually transcribed",
        "periods": records, "change_in_annualized_source_heat_mwh": delta,
        "runtime_contribution_mwh": hours_term, "power_contribution_mwh": power_term,
        "same_service_causal_comparison": "DATA_NOT_READY",
        "field_dispatch_decision": "DATA_NOT_READY",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=HERE / "hardwick_periods.csv")
    args = parser.parse_args()
    try:
        result = replay(args.input.read_bytes())
    except (ValueError, OSError, csv.Error) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2
    print(json.dumps(result, default=str, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
