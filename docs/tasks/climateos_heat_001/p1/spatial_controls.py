"""Additional pre-registered P1 controls. Offline, Python standard library."""
import argparse
from collections import Counter
from contextlib import nullcontext
import csv
import gzip
from pathlib import Path

from ledger import (EDGES, TOL, audit_hour, dispatch, exergy, heat_pump, line_loss,
                    load_inputs, pump_work, require)
from paired_inputs import FIXTURE, verify
from replay import ClockAudit, impacts, save_json


def dispatch_load_side(arm, hour, stock, demand, p, routes):
    """Only move the same vessel. Charge after CB and discharge directly at B."""
    space, dhw, air = demand
    need = space + dhw
    ac, cb = routes[arm]
    hp = heat_pump(p, air, False)
    cop = hp[0]
    loss_ac = line_loss(ac, p["source_C"], p["source_C"] - p["source_drop_K"], p, 1)
    loss_cb = line_loss(cb, p["hot_C"], p["return_C"], p, 1)
    capacity = min(p["hp_kw"], max(0, p["source_kw"] - loss_ac) / (1 - 1/cop))
    available_supply = max(0, capacity - loss_cb)
    f = dict.fromkeys(EDGES, 0.0)
    f.update(gross=p["source_kw"], space=space, dhw=dhw)
    f["tank_loss"] = stock * p["tank_frac_loss"]
    available = stock - f["tank_loss"]
    draw_cap = min(available, p["tank_rate"])
    last_day = hour >= 8736
    prior_draw = min(need, draw_cap) if last_day else 0
    direct = min(need - prior_draw, available_supply)
    f["discharge"] = min(draw_cap, need - direct)
    if not last_day and f["discharge"] == 0:
        f["charge"] = min(p["tank_kwh"] - available, p["tank_rate"], available_supply - direct)
    # The hot-pipe outlet supplies both direct demand and tank charging.
    f["network_service"] = direct + f["charge"]
    if f["network_service"] > 0:
        f["high_loss"] = loss_cb
        f["send"] = f["network_service"] + f["high_loss"]
    f["condenser"] = f["send"]
    f["compressor"] = f["condenser"] / cop
    f["evap"] = f["condenser"] - f["compressor"]
    f["low_loss"] = loss_ac if f["condenser"] else 0
    f["intercept"] = f["evap"] + f["low_loss"]
    f["bypass"] = f["gross"] - f["intercept"]
    f["boiler_service"] = max(0, need - direct - f["discharge"])
    require(f["boiler_service"] <= p["backup_kw"] + TOL, "UNMET_SERVICE")
    f["fuel"] = f["boiler_service"] / p["boiler_eff"]
    f["flue"] = f["fuel"] - f["boiler_service"]
    f["low_pump"] = pump_work(f["intercept"], p["source_drop_K"], ac, p)
    f["high_pump"] = pump_work(f["send"], p["hot_C"] - p["return_C"], cb, p)
    f["motor_loss"] = f["low_pump"] + f["high_pump"]
    end = available + f["charge"] - f["discharge"]
    if hour == 8759:
        f["terminal_dump"], end = end, 0.0
    return f, end, hp


def check(arm, h, start, demand, p, routes, moved):
    if not moved:
        flows, end, hp = dispatch(arm, h, start, demand, p, routes)
        return flows, end, hp, audit_hour(flows, start, end, demand, hp, p, 1, arm)
    f, end, hp = dispatch_load_side(arm, h, start, demand, p, routes)
    # Reuse all common device, meters, SOC, service and full-system checks. Map only
    # the two internal pipe-edge readings to the canonical C-header convention.
    delta = f["discharge"] - f["charge"]
    canonical = dict(f, send=f["send"] + delta, network_service=f["network_service"] + delta)
    residuals = audit_hour(canonical, start, end, demand, hp, p, 1, arm)
    actual = {
        "header": f["condenser"] - f["send"],
        "CB": f["send"] - f["high_loss"] - f["network_service"],
        "B": (f["network_service"] + f["discharge"] + f["boiler_service"]
              - f["charge"] - f["space"] - f["dhw"]),
    }
    require(max(map(abs, actual.values())) <= TOL, "MOVED_CONTROL_VOLUME")
    residuals.update(actual)
    return f, end, hp, residuals


def run_arm(case, arm, base, routes, rows, *, profile="central", outage="", moved=False,
            writer=None):
    totals, seasonal, quality = Counter(), Counter(), Counter()
    clock = ClockAudit()
    peaks = Counter()
    for row in rows:
        h = int(row["hour"])
        outage_now = outage == "always" or bool(outage and not int(row[outage]))
        p = dict(base, hp_kw=0) if outage_now and arm in ("L", "T") else base
        prefix = "" if profile == "central" else profile + "_"
        d = (float(row[prefix+"space_kw"]), float(row[prefix+"dhw_kw"]), float(row["air_C"]))
        start = clock.end
        f, end, hp, residuals = check(arm, h, start, d, p, routes, moved)
        clock.accept(h, start, end)
        require(abs(f["gross"] - float(row["gross_kw"])) <= TOL, "GROSS_PROCESS_DRIFT")
        require(not (outage_now and f["intercept"] > TOL), "UNAUTHORIZED_SOURCE_EXTRACTION")
        peaks["max_abs_residual_kWh"] = max(peaks["max_abs_residual_kWh"], *map(abs, residuals.values()))
        peaks["peak_send_kW"] = max(peaks["peak_send_kW"], f["send"])
        peaks["peak_inventory_kWh"] = max(peaks["peak_inventory_kWh"], end)
        peaks["full_h"] += int(p["tank_kwh"] > 0 and abs(end-p["tank_kwh"]) <= TOL)
        peaks["empty_h"] += int(abs(end) <= TOL)
        month = int(row["utc"][5:7])
        if month in (12, 1, 2):
            seasonal["summer_bypass_kWh"] += f["bypass"]
        if month in (6, 7, 8):
            seasonal["winter_backup_kWh"] += f["boiler_service"]
        totals.update(f)
        quality.update(exergy(f, hp, p))
        if writer:
            writer.writerow(["SYNTHETIC", case, arm, row["utc"], h, start, end,
                             *f.values(), max(map(abs, residuals.values()))])
    clock.close()
    return {"edges_kWh": dict(totals), "exergy_kWh_ex": dict(quality),
            "metrics": impacts(totals, base, arm, sum(routes.get(arm, ()))),
            "diagnostics": dict(peaks), "seasonal": dict(seasonal), "terminal_kWh": clock.end}


def recipes(cases):
    center, standard = cases["central"]
    cold, _ = cases["cold_source"]
    mismatch, _ = cases["seasonal_mismatch"]
    _, long_routes = cases["long_pipes"]
    return {
        "canonical": (center, standard, {}),
        "tank_at_B": (center, standard, {"moved": True}),
        "cold_only": (dict(center, source_C=25), standard, {}),
        "hot_only": (dict(center, source_C=60), standard, {}),
        "cold_inefficient_long": (cold, long_routes, {}),
        "mismatch_no_store": (dict(mismatch, tank_kwh=0), standard, {"profile":"mismatch"}),
        "mismatch_store": (mismatch, standard, {"profile":"mismatch"}),
        "mismatch_large_store": (dict(mismatch, tank_kwh=1280), standard, {"profile":"mismatch"}),
        "nonextracting_installed": (center, standard, {"outage":"always"}),
        "winter_week_out": (center, standard, {"outage":"july_maintenance_source_available"}),
        "owner_exit_july": (center, standard, {"outage":"july_source_available"}),
        "equal_physical_inputs": (center, cases["equal_length"][1], {}),
    }


def control_site_status(receptor_exceeded=None, route_available=None):
    if receptor_exceeded is True or route_available is False:
        return "REJECT_SYNTHETIC_FLAG"
    return "UNKNOWN"


def run(out, detail=None):
    digest = verify()
    cases = load_inputs()
    with gzip.open(FIXTURE, "rt", newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    require(len(rows) == 8760 and all(r["origin"] == "SYNTHETIC" for r in rows), "INPUT_GRID")
    out.mkdir(parents=True, exist_ok=True)
    experiments = recipes(cases)
    require(detail is None or detail in experiments, "UNKNOWN_DETAIL_CASE")
    notes = {"tag": "SYNTHETIC", "input_csv_sha256": digest,
             "review": "FOUNDER_ACCEPTANCE_PENDING",
             "moved_edge_overrides": {"charge":["B","tank"], "discharge":["tank","B"]},
             "H2": control_site_status(), "H3":"NOT_TESTABLE", "cases": {}}
    for name, (p, routes, flags) in experiments.items():
        sink = nullcontext(None)
        if name == detail:
            sink = (out / ("hourly_"+name+".csv")).open("w", newline="", encoding="utf-8")
        with sink as stream:
            writer = csv.writer(stream, lineterminator="\n") if stream else None
            if writer:
                writer.writerow(["origin","case","arm","utc","hour","start_kWh","end_kWh",
                                 *EDGES,"max_abs_residual_kWh"])
            arms = {}
            for arm in ("R0", "R1", "L", "T"):
                options = dict(flags, moved=bool(flags.get("moved") and arm in ("L","T")))
                arms[arm] = run_arm(name, arm, p, routes, rows, writer=writer, **options)
            for arm in ("R1","L","T"):
                for k in ("space","dhw"):
                    require(abs(arms[arm]["edges_kWh"][k] - arms["R0"]["edges_kWh"][k]) <= TOL, "PAIRED_SERVICE")
            notes["cases"][name] = arms
    require(notes["cases"]["equal_physical_inputs"]["L"] == notes["cases"]["equal_physical_inputs"]["T"], "LABEL_EFFECT")
    for arm in ("L","T"):
        n = notes["cases"]["nonextracting_installed"]
        require(n[arm]["metrics"]["primary_kWh"] == n["R0"]["metrics"]["primary_kWh"], "NONEXTRACTION")
        require(n[arm]["metrics"]["PV_cost_AUD"] > n["R0"]["metrics"]["PV_cost_AUD"], "LOST_ASSETS")
    center, standard = cases["central"]
    stamp = 24 * 181 + 7  # 1 July 07:00 UTC, winter failure
    demand = tuple(float(rows[stamp][k]) for k in ("space_kw","dhw_kw","air_C"))
    try:
        check("L", stamp, 0, demand, dict(center,hp_kw=0,backup_kw=1), standard, False)
    except ValueError as exc:
        require(str(exc) == "UNMET_SERVICE", "UNEXPECTED_REJECTION")
    else:
        raise ValueError("UNDETECTED_UNDERSERVICE")
    notes["negative_controls"] = {"incapable_backup":"UNMET_SERVICE",
        "blocked_corridor":control_site_status(route_available=False),
        "hot_receptor":control_site_status(receptor_exceeded=True), "site_without_observations":control_site_status()}
    save_json(out/"P1_PAIRED_SPATIAL_CONTROLS.json", notes)
    print(f"{len(experiments)} paired cases; {len(experiments)*4*8760} arm-hours; input CSV {digest}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--hourly", choices=tuple(recipes(load_inputs())), help="also export detailed hourly edge matrix for one case")
    args = parser.parse_args()
    run(args.out, args.hourly)
