"""HEAT-001 P1. Offline synthetic heat accounting; energies are interval kWh."""
from datetime import datetime, timedelta, timezone
import json
import math
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
VERSION = "HEAT-P1/1.0.0"
TOL = 1e-7  # kWh per interval, plus separate relative checks on annual sums
ARMS = ("R0", "R1", "L", "T")
START = datetime(2001, 1, 1, tzinfo=timezone.utc)

# One physical transfer per key. Both adjacent control volumes use the same edge.
EDGES = {
    "gross": ("process", "A"), "bypass": ("A", "original_outfall"),
    "intercept": ("A", "AC"), "low_loss": ("AC", "soil"),
    "evap": ("AC", "HP"), "ambient": ("outdoor_air", "HP"),
    "compressor": ("grid", "HP"), "condenser": ("HP", "header"),
    "charge": ("header", "tank"), "discharge": ("tank", "header"),
    "tank_loss": ("tank", "tank_room"), "terminal_dump": ("tank", "tank_room"),
    "send": ("header", "CB"), "high_loss": ("CB", "soil"),
    "network_service": ("CB", "B"), "local_hp": ("header", "B"),
    "fuel": ("fuel_supply", "boiler"), "boiler_service": ("boiler", "B"),
    "flue": ("boiler", "flue_sink"), "space": ("B", "space_meter"),
    "dhw": ("B", "hot_water_meter"), "low_pump": ("grid", "motor"),
    "high_pump": ("grid", "motor"), "motor_loss": ("motor", "equipment_room"),
}
NODES = ("A", "AC", "HP", "header", "tank", "CB", "boiler", "B", "motor")
INTERNAL = set(NODES)
IN_EDGES = {node: [k for k, (_, end) in EDGES.items() if end == node] for node in NODES}
OUT_EDGES = {node: [k for k, (start, _) in EDGES.items() if start == node] for node in NODES}
IMPORTS = [k for k, (a, b) in EDGES.items() if a not in INTERNAL and b in INTERNAL]
EXPORTS = [k for k, (a, b) in EDGES.items() if a in INTERNAL and b not in INTERNAL]
ELECTRIC = [k for k, (a, _) in EDGES.items() if a == "grid"]


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def number(value, label):
    require(type(value) in (int, float) and math.isfinite(value), "MISSING_OR_NONFINITE:" + label)
    return value


def read_json(path):
    def unique(pairs):
        obj = {}
        for key, value in pairs:
            require(key not in obj, "DUPLICATE_KEY:" + key)
            obj[key] = value
        return obj
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique)


def load_inputs():
    manifest = read_json(HERE / "P1_SYNTHETIC_INPUTS.json")
    schema = read_json(HERE / "P1_SYNTHETIC_INPUTS.schema.json")
    require(set(manifest) == set(schema["required"]), "MANIFEST_FIELDS")
    require(manifest["tag"] == "SYNTHETIC" and manifest["version"] == VERSION, "MANIFEST_VERSION")
    require(manifest["review"] == "FOUNDER_ACCEPTANCE_PENDING", "REVIEW_STATE")
    require(manifest["clock"] == {"tag": "SYNTHETIC", "start": "2001-01-01T00:00:00Z",
                                   "step_h": 1, "hours": 8760}, "CLOCK")
    spec = schema["properties"]["parameters"]
    units = {k: schema["$defs"][v["$ref"].split("/")[-1]]["properties"]["unit"]["const"]
             for k, v in spec["properties"].items()}

    def values(records):
        result = {}
        for k, item in records.items():
            require(k in units and set(item) == {"tag", "value", "unit"}, "METER_FIELDS:" + k)
            require(item["tag"] == "SYNTHETIC" and item["unit"] == units[k], "UNIT_OR_ORIGIN:" + k)
            result[k] = number(item["value"], k)
        return result

    base = values(manifest["parameters"])
    require(set(base) == set(units), "MISSING_METER")
    profile = manifest["profile"]
    profile_spec = schema["properties"]["profile"]
    require(set(profile) == set(profile_spec["required"]) and profile["tag"] == "SYNTHETIC", "PROFILE")
    for k, field in profile_spec["properties"].items():
        if field.get("type") != "array":
            continue
        seq = profile[k]
        require(type(seq) is list and field["minItems"] <= len(seq) <= field["maxItems"], "PROFILE:" + k)
        rule = field["items"]
        for v in seq:
            require(rule["minimum"] <= number(v, k) <= rule.get("maximum", math.inf), "PROFILE_RANGE:" + k)
            require(rule["type"] != "integer" or type(v) is int, "PROFILE_CLOCK:" + k)
        require(not field.get("uniqueItems") or len(set(seq)) == len(seq), "PROFILE_DUPLICATE:" + k)
    require(number(profile["space_offpeak_multiplier"], "offpeak") >= 0
            and set(profile["summer_months"]).isdisjoint(profile["winter_months"]), "PROFILE_SEASON")
    require(set(manifest["layouts"]) == {"L", "T"}, "ROUTES")
    routes = {}
    for arm, route in manifest["layouts"].items():
        require(set(route) == {"tag", "ac_m", "cb_m"} and route["tag"] == "SYNTHETIC", "ROUTE_TAG")
        routes[arm] = [route["ac_m"], route["cb_m"]]
    cases = {}
    for scenario in manifest["scenarios"]:
        name = scenario["id"]
        require(set(scenario) == {"tag", "id", "overrides", "routes"}
                and scenario["tag"] == "SYNTHETIC" and re.fullmatch(r"[a-z][a-z0-9_]*", name)
                and name not in cases, "DUPLICATE_OR_INVALID_SCENARIO")
        p = dict(base, **values(scenario["overrides"]))
        lengths = {**routes, **scenario["routes"]}
        require(set(lengths) == {"L", "T"}, "ROUTES")
        for pair in lengths.values():
            require(len(pair) == 2 and all(number(x, "length") >= 0 for x in pair), "ROUTE_LENGTH")
        validate_parameters(p)
        p["profile"] = profile
        cases[name] = (p, lengths)
    require("central" in cases, "MISSING_CENTRAL")
    return cases


def validate_parameters(p):
    for k, value in p.items():
        if k == "profile":
            continue
        number(value, k)
        if not k.endswith("_C"):
            require(value >= 0, "NEGATIVE:" + k)
    for k in ("carnot_fraction", "air_carnot_fraction", "pump_eff", "boiler_eff"):
        require(0 < p[k] <= 1, "EFFICIENCY:" + k)
    require(p["T0_K"] > 0 and p["life"] >= 1 and int(p["life"]) == p["life"], "REFERENCE_OR_LIFE")
    require(0 <= p["tank_frac_loss"] < 1 and int(p["shift_hours"]) == p["shift_hours"], "TANK_OR_CLOCK")
    for k in ("water_cp", "water_density", "source_drop_K", "approach_K", "backup_kw"):
        require(p[k] > 0, "NONPOSITIVE:" + k)
    require(p["source_C"] - p["source_drop_K"] > p["ground_C"]
            and p["hot_C"] > p["return_C"] > p["ground_C"], "PIPE_TEMPERATURE")
    require(p["hot_C"] >= max(p["dhw_C"], p["heat_supply_C"]) + p["approach_K"]
            and p["heat_supply_C"] > p["heat_return_C"] and p["dhw_C"] > p["inlet_C"], "SERVICE_TEMPERATURE")


def conditions(hour, p):
    """Fixed calendar and prescribed synthetic loads. No weather data or forecasting."""
    month = (START + timedelta(hours=hour)).month
    profile = p["profile"]
    season = profile["month_heating_fraction"][month-1]
    air = profile["month_air_C"][month-1]
    clock = hour % 24
    multiplier = p["morning_gain"] if clock in profile["space_peak_UTC"] else profile["space_offpeak_multiplier"]
    space = p["heating_peak_kw"] * season * multiplier
    tap_clock = (clock - p["shift_hours"]) % 24
    dhw = p["dhw_base_kw"] + (p["dhw_peak_kw"] if tap_clock in profile["dhw_peak_UTC"] else 0)
    factor = p["winter_load_factor"] if month in profile["winter_months"] else (
        p["summer_load_factor"] if month in profile["summer_months"] else 1)
    return space * factor, dhw * factor, air


def heat_pump(p, air, local):
    cold_c = air if local else p["source_C"] - p["source_drop_K"]
    cold = cold_c + 273.15 - p["approach_K"]
    hot = p["hot_C"] + 273.15 + p["approach_K"]
    require(0 < cold < hot, "LIFT")
    reversible = hot / (hot - cold)
    efficiency = p["air_carnot_fraction"] if local else p["carnot_fraction"]
    cop = reversible * efficiency
    require(1 < cop <= reversible, "COP_BOUND")
    return cop, reversible, cold, hot


def line_loss(length, supply, ret, p, dt):
    return p["pipe_U"] * length * (supply + ret - 2*p["ground_C"]) * dt / 1000


def pump_work(heat, delta_T, length, p):
    # kWh_th * 3600 / [kJ/(kg K) * K * kg/m3] gives circulating m3.
    volume = heat * 3600 / (p["water_cp"] * delta_T * p["water_density"])
    pressure = p["pump_fixed_dp"] + 2*length*p["pump_dp"]
    return pressure * volume / (3_600_000 * p["pump_eff"])


def dispatch(arm, hour, stock, demand, p, lengths, dt=1.0):
    require(arm in ARMS and number(dt, "hours") > 0, "ARM_OR_STEP")
    space_kw, dhw_kw, air = demand
    require(min(number(space_kw, "space_kw"), number(dhw_kw, "dhw_kw")) >= 0, "NEGATIVE_DEMAND")
    number(air, "air_C")
    f = dict.fromkeys(EDGES, 0.0)
    f["gross"] = p["source_kw"] * dt
    f["space"], f["dhw"] = space_kw * dt, dhw_kw * dt
    need = f["space"] + f["dhw"]
    cop, reversible, cold, hot = heat_pump(p, air, arm == "R1")
    end = stock
    if arm == "R1":
        f["local_hp"] = min(need, p["air_hp_kw"] * dt)
        f["condenser"] = f["local_hp"]
        f["compressor"] = f["condenser"] / cop
        f["ambient"] = f["condenser"] - f["compressor"]
    if arm in ("L", "T"):
        low, high = lengths[arm]
        cold_loss = line_loss(low, p["source_C"], p["source_C"]-p["source_drop_K"], p, dt)
        hot_loss = line_loss(high, p["hot_C"], p["return_C"], p, dt)
        hp_limit = min(p["hp_kw"] * dt, max(0, f["gross"]-cold_loss)/(1-1/cop))
        f["tank_loss"] = stock * (1 - (1-p["tank_frac_loss"])**dt)
        available = stock - f["tank_loss"]
        discharge_limit = min(available, p["tank_rate"]*dt)
        charge_limit = min(p["tank_kwh"]-available, p["tank_rate"]*dt)
        desired = need + hot_loss if need > 0 else 0
        if desired and hp_limit + discharge_limit > hot_loss:
            # Last day: use the tank first and disable charging to restore the start state.
            if hour >= 8736:
                f["discharge"] = min(desired, discharge_limit)
            hp_to_load = min(desired - f["discharge"], hp_limit)
            f["discharge"] += min(desired - hp_to_load - f["discharge"],
                                  discharge_limit - f["discharge"])
            f["send"] = hp_to_load + f["discharge"]
            f["high_loss"] = hot_loss
            f["network_service"] = f["send"] - hot_loss
        else:
            hp_to_load = 0
        if hour < 8736 and f["discharge"] == 0:
            f["charge"] = min(charge_limit, hp_limit - hp_to_load)
        f["condenser"] = hp_to_load + f["charge"]
        f["compressor"] = f["condenser"] / cop
        f["evap"] = f["condenser"] - f["compressor"]
        f["low_loss"] = cold_loss if f["condenser"] > 0 else 0
        f["intercept"] = f["evap"] + f["low_loss"]
        f["low_pump"] = pump_work(f["intercept"], p["source_drop_K"], low, p)
        f["high_pump"] = pump_work(f["send"], p["hot_C"]-p["return_C"], high, p)
        end = available + f["charge"] - f["discharge"]
        if hour == 8759:
            f["terminal_dump"], end = end, 0.0
    f["bypass"] = f["gross"] - f["intercept"]
    f["boiler_service"] = max(0.0, need - f["network_service"] - f["local_hp"])
    require(f["boiler_service"] <= p["backup_kw"]*dt + TOL, "UNMET_SERVICE")
    f["fuel"] = f["boiler_service"] / p["boiler_eff"]
    f["flue"] = f["fuel"] - f["boiler_service"]
    f["motor_loss"] = f["low_pump"] + f["high_pump"]
    return f, end, (cop, reversible, cold, hot)


def audit_hour(f, start, end, demand, hp, p, dt, arm):
    require(f.keys() == EDGES.keys(), "MISSING_OR_DUPLICATE_EDGE")
    for k, v in f.items():
        require(number(v, k) >= -TOL, "NEGATIVE_FLOW:" + k)
    capacity = p["tank_kwh"] if arm in ("L", "T") else 0
    require(all(-TOL <= number(v, "stock") <= capacity+TOL for v in (start, end)), "SOC_BOUNDS")
    require(min(f["charge"], f["discharge"]) <= TOL and
            max(f["charge"], f["discharge"]) <= p["tank_rate"]*dt+TOL, "SOC_DISPATCH")
    for key, kw in zip(("space", "dhw"), demand):
        require(abs(f[key] - kw * dt) <= TOL, "HOURLY_SERVICE:" + key)
    require(abs(f["gross"] - p["source_kw"] * dt) <= TOL, "POWER_ENERGY_MISMATCH")
    cop, reversible, cold, hot = hp
    require(0 < cold < hot and 1 < cop <= hot/(hot-cold)+1e-12
            and abs(reversible-hot/(hot-cold)) < 1e-10, "COP_BOUND")
    require(abs(f["condenser"] - cop*f["compressor"]) <= TOL, "COP_METER")
    residual = {n: sum(f[k] for k in IN_EDGES[n]) - sum(f[k] for k in OUT_EDGES[n]) for n in NODES}
    residual["tank"] -= end-start
    residual["system"] = sum(f[k] for k in IMPORTS)-sum(f[k] for k in EXPORTS)-(end-start)
    for key, value in residual.items():
        require(abs(value) <= TOL, "ENERGY_RESIDUAL:" + key)
    return residual


def stream_grade(supply_c, return_c, t0):
    hot, cold = supply_c + 273.15, return_c + 273.15
    return 1 - t0*math.log(hot/cold)/(hot-cold)


def exergy(f, hp, p):
    cop, reversible, cold, hot = hp
    t0 = p["T0_K"]
    cold_ex = (f["evap"] + f["ambient"]) * (1 - t0/cold)
    hot_ex = f["condenser"] * (1 - t0/hot)
    destroyed = cold_ex + f["compressor"] - hot_ex
    require(destroyed >= -TOL, "NEGATIVE_EXERGY_DESTRUCTION")
    useful = (f["space"] * stream_grade(p["heat_supply_C"], p["heat_return_C"], t0)
              + f["dhw"] * stream_grade(p["dhw_C"], p["inlet_C"], t0))
    return {"hp_cold_ex": cold_ex, "hp_hot_ex": hot_ex, "hp_destroyed_ex": destroyed,
            "minimum_work": f["condenser"] / reversible, "service_ex": useful,
            "intercept_ex": f["intercept"] * stream_grade(p["source_C"], p["source_C"]-p["source_drop_K"], t0)}
