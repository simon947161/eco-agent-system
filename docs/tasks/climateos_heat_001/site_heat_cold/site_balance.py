"""SYNTHETIC site ledger. Run with Python 3, standard library only."""
import argparse
import csv
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARMS = ("independent", "direct", "storage")


def active(hour, interval):
    return interval[0] <= hour < interval[1]


def require_close(a, b, label):
    if not math.isclose(a, b, abs_tol=1e-8, rel_tol=1e-10):
        raise ValueError(f"{label}: {a} != {b}")


def run_day(cfg, season, shift, arm):
    climate = cfg["seasons"][season]
    ambient = climate["ambient_C"]
    mains = climate["mains_C"]
    wash_window = cfg["wash_shifts"][shift]
    water_cp = cfg["water_cp_kJ_kgK"] / 3600
    # Indirect recovery only from an already hot stream at production load.
    # Two minimum approaches allow charging and subsequent delivery at grade.
    preheat_temp = min(cfg["preheat_limit_C"], cfg["wash_target_C"],
                       cfg["hot_stream_C"] - 2 * cfg["minimum_approach_K"])
    state = 0.0
    records = []
    for hour in range(24):
        production = active(hour, cfg["production"])
        mass = cfg["line_kg_h"] if production else 0
        water = cfg["wash_kg_h"] if active(hour, wash_window) else 0
        product_cold = mass * cfg["product_cp_kJ_kgK"] * (cfg["product_inlet_C"] - cfg["product_outlet_C"]) / 3600
        cold = product_cold + cfg["room_internal_kW"] + cfg["room_UA_kW_K"] * max(0, ambient - cfg["room_target_C"])
        cold_delivered = min(cold, cfg["cold_capacity_kW"])
        require_close(cold_delivered, cold, "cold service capacity")
        compressor = cold_delivered / climate["cold_COP"]
        condenser = cold_delivered + compressor
        grade = condenser * cfg["high_grade_fraction_on_shift"] if production and preheat_temp > mains else 0.0
        hot = water * water_cp * (cfg["wash_target_C"] - mains)
        preheat_load = water * water_cp * max(0, preheat_temp - mains)
        direct = min(grade, preheat_load) if arm != "independent" else 0.0
        opening = state
        loss = opening * cfg["tank_loss_fraction_h"]
        discharge = min(opening - loss, cfg["tank_discharge_limit_kW"], preheat_load - direct)
        state = opening - loss - discharge
        charge = 0.0
        # Daily schedule known to the operator: store surplus only before the
        # next wash shift. No simultaneous charge/discharge or overnight credit.
        if arm == "storage" and hour < wash_window[0]:
            charge = min(grade - direct, cfg["tank_charge_limit_kW"], cfg["tank_capacity_kWh"] - state)
        state += charge
        dump = state if hour == 23 else 0.0
        state -= dump
        recovered = direct + discharge
        backup = min(hot - recovered, cfg["boiler_useful_capacity_kW"])
        unmet = hot - recovered - backup
        gas = backup / cfg["boiler_efficiency"]
        pump = (direct + charge) * cfg["source_pump_kWh_per_kWh"] + discharge * cfg["tank_delivery_pump_kWh_per_kWh"]
        power = compressor + pump
        reject = condenser - direct - charge
        boiler_flue = gas - backup
        remaining_heat = reject + loss + dump + pump + boiler_flue
        emissions = power * cfg["grid_kgCO2e_per_kWh"] + gas * cfg["gas_kgCO2e_per_kWh_fuel"]
        row = dict(season=season, shift=shift, arm=arm, hour=hour, ambient_C=ambient, mains_C=mains,
                   product_kg=mass, room_target_C=cfg["room_target_C"], wash_kg=water,
                   cold_kWh=cold, cold_delivered_kWh=cold_delivered, unmet_cold_kWh=cold-cold_delivered, wash_demand_kWh=hot,
                   preheat_cap_kWh=preheat_load, grade_available_kWh=grade,
                   compressor_kWh=compressor, condenser_kWh=condenser, direct_kWh=direct,
                   opening_kWh=opening, charge_kWh=charge, discharge_kWh=discharge,
                   tank_loss_kWh=loss, end_dump_kWh=dump, closing_kWh=state, recovered_kWh=recovered,
                   condenser_reject_kWh=reject, boiler_useful_kWh=backup, gas_kWh=gas,
                   pump_kWh=pump, electricity_kWh=power, emissions_kg=emissions, unmet_heat_kWh=unmet,
                   boiler_loss_kWh=boiler_flue, site_reject_kWh=remaining_heat)
        require_close(condenser, direct + charge + reject, "source")
        require_close(opening + charge, state + discharge + loss + dump, "tank")
        require_close(hot, recovered + backup, "hot service")
        require_close(cold_delivered + power + gas, hot + remaining_heat + state - opening, "site boundary")
        if min(reject, state, recovered, grade - direct - charge, preheat_load - recovered) < -1e-8:
            raise ValueError("negative flow or temperature-grade exceedance")
        records.append(row)
    require_close(state, 0, "terminal condition")
    return records


def summarize(rows):
    sums = ("product_kg", "cold_kWh", "wash_kg", "wash_demand_kWh", "grade_available_kWh",
            "recovered_kWh", "tank_loss_kWh", "end_dump_kWh", "condenser_reject_kWh", "gas_kWh",
            "electricity_kWh", "pump_kWh", "emissions_kg", "unmet_heat_kWh", "unmet_cold_kWh", "site_reject_kWh")
    result = {k: rows[0][k] for k in ("season", "shift", "arm")}
    result.update({k: sum(row[k] for row in rows) for k in sums})
    result["peak_electric_kW"] = max(row["electricity_kWh"] for row in rows)
    tonnes = result["product_kg"] / 1000
    for key in ("gas_kWh", "electricity_kWh", "recovered_kWh", "condenser_reject_kWh", "emissions_kg"):
        result[key + "_per_t"] = result[key] / tonnes
    return result


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0], lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: format(v, ".10f") if isinstance(v, float) else v for k, v in row.items()})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    destination = parser.parse_args().out
    destination.mkdir(parents=True, exist_ok=True)
    cfg = json.loads((HERE / "fixture.json").read_text(encoding="utf-8"))
    hourly, daily = [], []
    for season in cfg["seasons"]:
        for shift in cfg["wash_shifts"]:
            cases = [run_day(cfg, season, shift, arm) for arm in ARMS]
            reference = cases[0]
            for rows in cases:
                for actual, baseline in zip(rows, reference):
                    for key in ("hour", "product_kg", "wash_kg", "cold_kWh", "cold_delivered_kWh",
                                "wash_demand_kWh", "room_target_C", "ambient_C", "mains_C", "compressor_kWh"):
                        require_close(actual[key], baseline[key], "paired " + key)
                hourly.extend(rows)
                daily.append(summarize(rows))
            if shift == "aligned":
                require_close(daily[-1]["emissions_kg"], daily[-2]["emissions_kg"], "aligned tank null")
            if shift == "later":
                require_close(daily[-3]["emissions_kg"], daily[-2]["emissions_kg"], "later direct null")
    write_csv(destination / "daily.csv", daily)
    write_csv(destination / "hourly.csv", hourly)
    print(f"SYNTHETIC {len(daily)} arm-days, {len(hourly)} arm-hours; paired service, source, storage, terminal and null checks passed")


if __name__ == "__main__":
    main()
