"""One SYNTHETIC paired winter day; constant-rate two-pipe counterflow route."""
import csv
import json
import math
import sys
from pathlib import Path

PARENT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PARENT))
from site_balance import run_day, require_close

CFG = json.loads((PARENT / "fixture.json").read_text(encoding="utf-8"))
GROUND = 10.0                 # degC, independently assumed
RETURN_AT_USER = 35.0         # degC, process exchanger controlled outlet
SOURCE_LIFT = 20.0            # K, constant across clean-water source exchanger
LINE_U = 0.25                 # W/(m K), per pipe, includes insulation & ground
PRESSURE_GRADIENT = 200.0     # Pa/m, per pipe, constant flow during operation
PUMP_EFF = 0.60
RHO = 1000.0                  # kg/m3
DAY = run_day(CFG, "winter", "aligned", "independent")
LOCAL = run_day(CFG, "winter", "aligned", "direct")


def route(q, length):
    # q in kW; one-hour steps. Reuse local duty without extra compression.
    capacity_rate = q / SOURCE_LIFT                      # kW/K
    flow = capacity_rate / CFG["water_cp_kJ_kgK"] / RHO   # m3/s
    attenuation = math.exp(-LINE_U * length / (1000 * capacity_rate))
    return_source = GROUND + (RETURN_AT_USER - GROUND) * attenuation
    supply_source = return_source + SOURCE_LIFT
    supply_user = GROUND + (supply_source - GROUND) * attenuation
    delivered = capacity_rate * (supply_user - RETURN_AT_USER)
    line_loss = capacity_rate * ((supply_source - supply_user) + (RETURN_AT_USER - return_source))
    require_close(q, delivered + line_loss, "route heat")
    pump = 2 * PRESSURE_GRADIENT * length * flow / (1000 * PUMP_EFF)
    return delivered, line_loss, pump, supply_user, supply_source, return_source


def evaluate(length, state):
    gas = electricity = delivered_total = loss_total = route_pump_total = carbon = peak = 0.0
    h6 = {}
    for baseline, local in zip(DAY, LOCAL):
        q = local["direct_kWh"]
        recovered = loss = route_pump = extraction_pump = 0.0
        if q > 0 and state == "on":
            recovered, loss, route_pump, supply, origin, returning = route(q, length)
            if recovered < -1e-8:
                raise ValueError("Outside fixed-temperature forward-delivery envelope")
            recovered = max(0.0, recovered)
            outlet = baseline["mains_C"] + recovered * 3600 / (baseline["wash_kg"] * CFG["water_cp_kJ_kgK"])
            if (outlet > CFG["preheat_limit_C"] + 1e-8 or supply - outlet < CFG["minimum_approach_K"]
                    or RETURN_AT_USER - baseline["mains_C"] < CFG["minimum_approach_K"]
                    or CFG["hot_stream_C"] - origin < CFG["minimum_approach_K"] - 1e-8):
                raise ValueError("Temperature/approach violation")
            extraction_pump = q * CFG["source_pump_kWh_per_kWh"]
            if baseline["hour"] == 6:
                h6 = dict(supply_source_C=origin, supply_user_C=supply, return_source_C=returning,
                          preheated_water_C=outlet)
        backup = baseline["wash_demand_kWh"] - recovered
        if backup > CFG["boiler_useful_capacity_kW"] + 1e-8:
            raise ValueError("Hot service not met")
        gas_input = backup / CFG["boiler_efficiency"]
        elec = baseline["compressor_kWh"] + extraction_pump + route_pump
        require_close(gas_input * CFG["boiler_efficiency"] + recovered, baseline["wash_demand_kWh"], "service")
        require_close(local["cold_delivered_kWh"], baseline["cold_kWh"], "cold")
        require_close(q if state == "on" else 0, recovered + loss, "heat meters")
        gas += gas_input
        electricity += elec
        delivered_total += recovered
        loss_total += loss
        route_pump_total += route_pump
        carbon += gas_input * CFG["gas_kgCO2e_per_kWh_fuel"] + elec * CFG["grid_kgCO2e_per_kWh"]
        peak = max(peak, elec)
    return dict(length_m=length, state=state, useful_kWh=delivered_total, line_loss_kWh=loss_total,
                route_pump_kWh=route_pump_total, gas_kWh=gas, electricity_kWh=electricity,
                peak_kW=peak, emissions_kg=carbon, **h6)


def main():
    base = evaluate(0, "off")
    local = evaluate(0, "on")
    for field in ("gas_kWh", "electricity_kWh", "emissions_kg"):
        require_close(base[field], sum(r[field] for r in DAY), "independent " + field)
        require_close(local[field], sum(r[field] for r in LOCAL), "local " + field)
    q = max(r["direct_kWh"] for r in LOCAL)
    diff = RETURN_AT_USER - GROUND
    # Supply reaches controlled return when diff*x^2 + SOURCE_LIFT*x - diff = 0.
    x = 2 * diff / (math.sqrt(SOURCE_LIFT**2 + 4 * diff**2) + SOURCE_LIFT)
    max_length = -math.log(x) * 1000 * (q / SOURCE_LIFT) / LINE_U
    low, high = 0.0, max_length
    if not (local["emissions_kg"] < base["emissions_kg"] < evaluate(high, "on")["emissions_kg"]):
        raise ValueError("Carbon threshold is not bracketed")
    for _ in range(55):
        mid = (low + high) / 2
        if evaluate(mid, "on")["emissions_kg"] < base["emissions_kg"]:
            low = mid
        else:
            high = mid
    critical = (low + high) / 2
    require_close(evaluate(critical, "on")["emissions_kg"], base["emissions_kg"], "carbon root")
    longer = (max_length + critical) / 2
    if evaluate(longer, "on")["emissions_kg"] <= base["emissions_kg"]:
        raise ValueError("Expected sign reversal")
    cases = [base, local, evaluate(100, "on"), evaluate(critical, "on"),
             evaluate(longer, "on"), evaluate(longer, "off"), evaluate(max_length, "on")]
    columns = list(local) + ["delta_vs_boiler_kg", "delta_vs_local_kg"]
    writer = csv.DictWriter(sys.stdout, fieldnames=columns, lineterminator="\n")
    writer.writeheader()
    for case in cases:
        case["delta_vs_boiler_kg"] = case["emissions_kg"] - base["emissions_kg"]
        case["delta_vs_local_kg"] = case["emissions_kg"] - local["emissions_kg"]
        writer.writerow({k: f"{v:.8f}" if isinstance(v, float) else v for k, v in case.items()})


if __name__ == "__main__":
    main()
