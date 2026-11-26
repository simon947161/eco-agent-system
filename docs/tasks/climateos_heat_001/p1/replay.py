"""Replay paired annual cases from the canonical fixture. Python standard library."""
import argparse
from collections import defaultdict
import csv
import gzip
import hashlib
import io
import json
from pathlib import Path
from datetime import timedelta

from ledger import (ARMS, EDGES, ELECTRIC, HERE, NODES, START, TOL, VERSION, audit_hour,
                    conditions, dispatch, exergy, load_inputs, require)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_json(path, data):
    path.write_bytes((json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode())


class ClockAudit:
    """Unique interval keys and continuity imply unique case/arm/hour/edge meter IDs."""
    def __init__(self):
        self.next_hour = 0
        self.end = 0.0

    def accept(self, hour, start, end):
        require(hour == self.next_hour, "DUPLICATE_OR_MISSING_HOUR")
        require(abs(start-self.end) <= TOL, "SOC_CONTINUITY")
        self.next_hour += 1
        self.end = end

    def close(self):
        require(self.next_hour == 8760 and abs(self.end) <= TOL, "TERMINAL_STOCK_OR_CLOCK")


def impacts(flows, p, arm, length):
    electricity = sum(flows[k] for k in ELECTRIC)
    fuel = flows["fuel"]
    useful = flows["space"] + flows["dhw"]
    net = arm in ("L", "T")
    hp_cap = p["network_hp_capex"] if net else p["air_hp_capex"] if arm == "R1" else 0
    hp_emb = p["hp_embodied"] if net else p["air_hp_embodied"] if arm == "R1" else 0
    capex = {"boiler": p["boiler_capex"], "hp": hp_cap,
             "route": length*p["trench_capex"], "tank": p["tank_kwh"]*p["tank_capex"] if net else 0}
    fixed = sum(capex.values()) * p["fixed_om"]
    annual_power = electricity*p["electricity_price"]
    annual_fuel = fuel*p["fuel_price"]
    life, rate = p["life"], p["rate"]
    pv_years = sum((1+rate)**-y for y in range(1, int(life)+1))
    pv = sum(capex.values()) + pv_years*(fixed+annual_power+annual_fuel)
    embodied = (p["boiler_embodied"] + hp_emb + length*p["pipe_embodied"]
                + (p["tank_kwh"]*p["tank_embodied"] if net else 0))
    carbon = electricity*p["grid_ef"] + fuel*p["fuel_ef"]
    return {"service_kWh": useful, "electricity_kWh": electricity, "fuel_kWh_LHV": fuel,
            "primary_kWh": electricity*p["grid_pe"] + fuel*p["fuel_pe"],
            "operation_kgCO2e": carbon, "optional_embodied_kgCO2e": embodied,
            "partial_life_kgCO2e": life*carbon+embodied,
            "partial_life_kgCO2e_per_MWh": (life*carbon+embodied)/(life*useful/1000),
            "capital_AUD": capex, "annual_opex_AUD": {"fixed":fixed,"electricity":annual_power,"fuel":annual_fuel},
            "PV_cost_AUD": pv, "LCOH_AUD_per_MWh": pv/(pv_years*useful/1000)}


def run_arm(case, p, routes, arm, writer=None):
    clock = ClockAudit()
    flows = dict.fromkeys(EDGES, 0.0)
    ex = defaultdict(float)
    worst = dict.fromkeys((*NODES, "system"), 0.0)
    annual_residual = dict.fromkeys(worst, 0.0)
    seasonal = defaultdict(lambda: defaultdict(float))
    peaks = {"stock_max_kWh": 0.0, "stock_min_kWh": 0.0, "backup_hours": 0, "full_tank_hours": 0}
    for h in range(8760):
        demand = conditions(h, p)
        start = clock.end
        f, end, hp = dispatch(arm, h, start, demand, p, routes)
        residual = audit_hour(f, start, end, demand, hp, p, 1, arm)
        clock.accept(h, start, end)
        quality = exergy(f, hp, p)
        for k, v in quality.items():
            ex[k] += v
        for k, v in f.items():
            flows[k] += v
        for k, v in residual.items():
            worst[k] = max(worst[k], abs(v))
            annual_residual[k] += v
        peaks["stock_max_kWh"] = max(peaks["stock_max_kWh"], end)
        peaks["stock_min_kWh"] = min(peaks["stock_min_kWh"], end)
        peaks["backup_hours"] += int(arm != "R0" and f["boiler_service"] > TOL)
        peaks["full_tank_hours"] += int(p["tank_kwh"] > 0 and abs(end-p["tank_kwh"]) <= TOL)
        timestamp = START + timedelta(hours=h)
        monthly = seasonal[str(timestamp.month)]
        for k in ("space", "dhw", "gross", "bypass", "charge", "discharge", "tank_loss", "boiler_service"):
            monthly[k] += f[k]
        if writer:
            row = ["SYNTHETIC", case, arm, timestamp.strftime("%Y-%m-%dT%H:00Z"), h,
                   demand[0], demand[1], p["heat_supply_C"], p["dhw_C"], start, end,
                   hp[0] if f["compressor"] else "", hp[1] if f["compressor"] else "",
                   *f.values(), *quality.values(), *residual.values()]
            writer.writerow([format(v, ".12g") if type(v) is float else v for v in row])
    clock.close()
    require(max(map(abs, annual_residual.values())) < 1e-5, "ANNUAL_RESIDUAL")
    length = sum(routes[arm]) if arm in routes else 0
    return {"tag": "SYNTHETIC", "annual_edges_kWh": flows, "annual_exergy_kWh_ex":dict(ex),
            "annual_metrics":impacts(flows, p, arm, length), "hourly_max_abs_residual_kWh":worst,
            "annual_residual_kWh":annual_residual, "stock_end_kWh":clock.end, **peaks,
            "monthly_edges_kWh":dict(seasonal)}


def run_case(name, p, routes, writer=None):
    arms = {a:run_arm(name, p, routes, a, writer) for a in ARMS}
    metrics = ("primary_kWh", "operation_kgCO2e", "partial_life_kgCO2e",
               "partial_life_kgCO2e_per_MWh", "PV_cost_AUD", "LCOH_AUD_per_MWh")
    diffs = {}
    for arm, ref in (("L","R0"),("T","R0"),("L","R1"),("T","R1"),("T","L")):
        lhs, rhs = (arms[a]["annual_metrics"] for a in (arm, ref))
        require(abs(lhs["service_kWh"]-rhs["service_kWh"]) < TOL, "PAIRED_SERVICE")
        diffs[arm+"-"+ref] = {k:lhs[k]-rhs[k] for k in metrics}
    return {"tag":"SYNTHETIC","routes_one_way_m":routes,"arms":arms,"delta_intervention_minus_reference":diffs,
            "receptor_effect":"UNKNOWN","global_cooling":"NOT_TESTABLE"}


def write_outputs(out, detail="central"):
    out.mkdir(parents=True, exist_ok=True)
    cases = load_inputs()
    require(detail in cases, "UNKNOWN_DETAIL_CASE")
    name = "P1_HOURLY_"+detail+".csv.gz"
    ledger = {"tag":"SYNTHETIC","formula_version":VERSION, "review":"FOUNDER_ACCEPTANCE_PENDING",
              "clock":"2001 synthetic non-leap UTC; 8760 one-hour intervals per arm",
              "edge_id":"scenario/arm/UTC interval start/column; transfers in kWh",
              "edge_ports":EDGES, "cases":{}}
    with (out/name).open("wb") as binary, gzip.GzipFile(filename="", fileobj=binary, mode="wb", mtime=0) as gz:
        with io.TextIOWrapper(gz, encoding="utf-8", newline="") as stream:
            writer = csv.writer(stream, lineterminator="\n")
            writer.writerow(["tag","case","arm","UTC","hour","space_request_kW","dhw_request_kW",
                             "space_supply_C","dhw_supply_C","start_kWh","end_kWh","COP","Carnot_COP",
                             *EDGES, "hp_cold_ex","hp_hot_ex","hp_destroyed_ex","minimum_work","service_ex",
                             "intercept_ex", *("res_"+n for n in (*NODES,"system"))])
            for case, (p, routes) in cases.items():
                ledger["cases"][case] = run_case(case, p, routes, writer if case == detail else None)
    result = out/"P1_ENERGY_EXERGY_CARBON_LEDGER.json"
    save_json(result, ledger)
    with gzip.open(out/name, "rb") as csvfile:
        csv_digest = hashlib.sha256(csvfile.read()).hexdigest()
    input_files = ["P1_SYNTHETIC_INPUTS.json", "P1_SYNTHETIC_INPUTS.schema.json",
                   "ledger.py", "replay.py", "test_ledger.py"]
    save_json(out/"P1_RUN_PASSPORT.json", {"tag":"SYNTHETIC","version":VERSION,
              "review":"FOUNDER_ACCEPTANCE_PENDING","inputs_and_code_sha256":{k:sha(HERE/k) for k in input_files},
              "outputs_sha256":{k:sha(out/k) for k in (result.name,name)},
              "decompressed_hourly_csv_sha256":csv_digest, "hourly_detail_case":detail,
              "hours_per_arm":8760,"arms":ARMS,"case_count":len(cases),
              "validated_arm_hours":len(cases)*len(ARMS)*8760, "hourly_tolerance_kWh":TOL,
              "annual_tolerance_kWh":1e-5,"data_rights":"Author-created synthetic fixtures only"})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--hourly", default="central", help="case with exported hourly meters; all cases audited")
    args = parser.parse_args()
    write_outputs(args.out, args.hourly)
