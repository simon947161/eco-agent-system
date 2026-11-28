"""Check exported CSV meters independently and exercise failure/zero-effect cases."""
import csv
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

from site_balance import HERE, run_day


def check(a, b):
    if not math.isclose(a, b, abs_tol=1e-7, rel_tol=1e-10):
        raise ValueError(f"Independent audit: {a} != {b}")


def main():
    cfg = json.loads((HERE / "fixture.json").read_text(encoding="utf-8"))
    output = Path(sys.argv[1])
    with (output / "hourly.csv").open(encoding="utf-8") as f:
        hours = list(csv.DictReader(f))
    with (output / "daily.csv").open(encoding="utf-8") as f:
        summary = list(csv.DictReader(f))
    cases = defaultdict(list)
    for row in hours:
        key = (row["season"], row["shift"], row["arm"])
        cases[key].append({k: float(v) for k, v in row.items() if k not in ("season", "shift", "arm")})
    check(len(cases), 24)
    check(len(summary), 24)
    for day in summary:
        key = (day["season"], day["shift"], day["arm"])
        rows = cases[key]
        if [r["hour"] for r in rows] != list(range(24)):
            raise ValueError("Incomplete clock")
        prev = 0.0
        for r in rows:
            check(r["opening_kWh"], prev)
            prev = r["closing_kWh"]
            check(r["gas_kWh"] * cfg["boiler_efficiency"] + r["recovered_kWh"], r["wash_demand_kWh"])
            check(r["wash_demand_kWh"], r["wash_kg"] * cfg["water_cp_kJ_kgK"] * (cfg["wash_target_C"] - r["mains_C"]) / 3600)
            check(r["cold_delivered_kWh"], r["cold_kWh"])
            check(r["cold_kWh"] + r["electricity_kWh"] + r["gas_kWh"] + r["opening_kWh"],
                  r["wash_demand_kWh"] + r["site_reject_kWh"] + r["closing_kWh"])
        check(prev, 0)
        check(sum(r["product_kg"] for r in rows), 8000)
        check(sum(r["wash_kg"] for r in rows), 3200)
        check(float(day["emissions_kg"]), cfg["gas_kgCO2e_per_kWh_fuel"] * sum(r["gas_kWh"] for r in rows)
              + cfg["grid_kgCO2e_per_kWh"] * sum(r["electricity_kWh"] for r in rows))
        check(float(day["peak_electric_kW"]), max(r["electricity_kWh"] for r in rows))
    for name, value in (("tank_capacity_kWh", 0), ("hot_stream_C", 15)):
        altered = dict(cfg, **{name: value})
        for s in cfg["seasons"]:
            pair = [run_day(altered, s, "later", arm) for arm in ("independent", "storage")]
            for base, intervention in zip(*pair):
                check(base["emissions_kg"], intervention["emissions_kg"])
    for field in ("cold_capacity_kW", "boiler_useful_capacity_kW"):
        try:
            run_day(dict(cfg, **{field: 1}), "winter", "aligned", "independent")
        except ValueError as exc:
            if "service" not in str(exc):
                raise
        else:
            raise ValueError("Under-capacity service accepted")
    print("CSV re-audit passed: 576 hourly/24 daily rows; 2 zero-effect sweeps and 2 capacity rejection controls passed")


if __name__ == "__main__":
    main()
