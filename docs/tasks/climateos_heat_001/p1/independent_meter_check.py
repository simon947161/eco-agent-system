"""Reconstruct center-case balances directly from exported meters; no dispatch import."""
import argparse
import csv
from datetime import datetime, timedelta, timezone
import gzip
import json
import math
from pathlib import Path


def close(a, b, label, hourly=False):
    limit = 1e-7 if hourly else 1e-6 + 1e-10 * max(abs(a), abs(b))
    if not (math.isfinite(a) and math.isfinite(b) and abs(a - b) <= limit):
        raise ValueError(f"{label}: {a} vs {b}")


def independent(root):
    inputs = json.loads((root/"P1_SYNTHETIC_INPUTS.json").read_text("utf-8"))
    p = {k:v["value"] for k,v in inputs["parameters"].items()}
    main = json.loads((root/"results/P1_ENERGY_EXERGY_CARBON_LEDGER.json").read_text("utf-8"))
    control = json.loads((root/"controls/P1_PAIRED_SPATIAL_CONTROLS.json").read_text("utf-8"))
    source = root/"results/P1_HOURLY_central.csv.gz"
    with gzip.open(root/"controls/paired_hours.csv.gz","rt",encoding="utf-8",newline="") as stream:
        inputs_by_hour = list(csv.DictReader(stream))
    ports = main["edge_ports"]
    sums = {}
    next_hour, stock, worst = {}, {}, {}
    with gzip.open(source,"rt",encoding="utf-8",newline="") as stream:
        reader = csv.DictReader(stream)
        if len(reader.fieldnames) != len(set(reader.fieldnames)):
            raise ValueError("duplicate meter column")
        for row in reader:
            arm, hour = row["arm"], int(row["hour"])
            expected = (datetime(2001,1,1,tzinfo=timezone.utc)+timedelta(hours=hour)).strftime("%Y-%m-%dT%H:00Z")
            if (row["UTC"],row["tag"],row["case"],hour) != (expected,"SYNTHETIC","central",next_hour.get(arm,0)):
                raise ValueError("clock / tag / duplicate key")
            next_hour[arm] = hour+1
            v = {k:float(row[k]) for k in ports}
            if not all(math.isfinite(x) and x >= -1e-7 for x in v.values()):
                raise ValueError("invalid meter")
            start,end = float(row["start_kWh"]),float(row["end_kWh"])
            close(start,stock.get(arm,0),"continuity",True)
            stock[arm] = end
            need = inputs_by_hour[hour]
            close(v["space"],float(need["space_kw"]),"space",True)
            close(v["dhw"],float(need["dhw_kw"]),"dhw",True)
            close(float(row["space_supply_C"]),p["heat_supply_C"],"space temperature",True)
            close(float(row["dhw_supply_C"]),p["dhw_C"],"DHW temperature",True)
            cap = p["tank_kwh"] if arm in ("L","T") else 0
            if not -1e-7 <= end <= cap+1e-7:
                raise ValueError("SOC bounds")
            balances = {
                "A":v["gross"]-v["bypass"]-v["intercept"],
                "AC":v["intercept"]-v["evap"]-v["low_loss"],
                "HP":v["evap"]+v["ambient"]+v["compressor"]-v["condenser"],
                "header":v["condenser"]+v["discharge"]-v["charge"]-v["send"]-v["local_hp"],
                "CB":v["send"]-v["high_loss"]-v["network_service"],
                "tank":start+v["charge"]-v["discharge"]-v["tank_loss"]-v["terminal_dump"]-end,
                "boiler":v["fuel"]-v["boiler_service"]-v["flue"],
                "B":v["network_service"]+v["local_hp"]+v["boiler_service"]-v["space"]-v["dhw"],
                "motor":v["low_pump"]+v["high_pump"]-v["motor_loss"],
                "system":(v["gross"]+v["ambient"]+v["fuel"]+v["compressor"]+v["low_pump"]+v["high_pump"]
                          -v["bypass"]-v["low_loss"]-v["high_loss"]-v["tank_loss"]-v["terminal_dump"]
                          -v["motor_loss"]-v["flue"]-v["space"]-v["dhw"]-(end-start))}
            for label, res in balances.items():
                close(res,0,arm+"/"+label,True)
                close(res,float(row["res_"+label]),"archived residual",True)
            largest=max(abs(x) for x in balances.values())
            worst[arm]=max(worst.get(arm,0),largest)
            heat_k = p["hot_C"]+p["approach_K"]+273.15
            cold_c = float(need["air_C"]) if arm=="R1" else p["source_C"]-p["source_drop_K"]
            cold_k = cold_c-p["approach_K"]+273.15
            hp_ex = (v["evap"]+v["ambient"])*(1-p["T0_K"]/cold_k)+v["compressor"]-v["condenser"]*(1-p["T0_K"]/heat_k)
            close(hp_ex,float(row["hp_destroyed_ex"]),"HP exergy",True)
            if v["compressor"]>0:
                close(v["condenser"]/v["compressor"],float(row["COP"]),"COP",True)
            annual = sums.setdefault(arm, {k:0.0 for k in ports})
            for k,x in v.items():
                annual[k]+=x
    if next_hour!={arm:8760 for arm in ("R0","R1","L","T")}:
        raise ValueError("incomplete arms")
    for arm,v in sums.items():
        close(stock[arm],0,"terminal",True)
        annual=main["cases"]["central"]["arms"][arm]
        more=control["cases"]["canonical"][arm]
        for k,x in v.items():
            close(x,annual["annual_edges_kWh"][k],"annual archived/"+k)
            close(x,more["edges_kWh"][k],"annual supplemental/"+k)
        elec=v["compressor"]+v["low_pump"]+v["high_pump"]
        net=arm in ("L","T")
        length=sum((inputs["layouts"][arm][k] for k in ("ac_m","cb_m"))) if net else 0
        capex=p["boiler_capex"]+length*p["trench_capex"]
        built=p["boiler_embodied"]+length*p["pipe_embodied"]
        if net:
            capex+=p["network_hp_capex"]+p["tank_kwh"]*p["tank_capex"]
            built+=p["hp_embodied"]+p["tank_kwh"]*p["tank_embodied"]
        if arm=="R1":
            capex+=p["air_hp_capex"]
            built+=p["air_hp_embodied"]
        annuity=(1-(1+p["rate"])**(-p["life"]))/p["rate"] if p["rate"] else p["life"]
        s=v["space"]+v["dhw"]
        carbon=elec*p["grid_ef"]+v["fuel"]*p["fuel_ef"]
        cost=capex/annuity+capex*p["fixed_om"]+elec*p["electricity_price"]+v["fuel"]*p["fuel_price"]
        hand={"service_kWh":s,"electricity_kWh":elec,"fuel_kWh_LHV":v["fuel"],
              "primary_kWh":elec*p["grid_pe"]+v["fuel"]*p["fuel_pe"], "operation_kgCO2e":carbon,
              "partial_life_kgCO2e":carbon*p["life"]+built, "LCOH_AUD_per_MWh":cost/(s/1000)}
        for k,x in hand.items():
            close(x,annual["annual_metrics"][k],k)
            close(x,more["metrics"][k],k)
    return {"origin":"SYNTHETIC", "hourly_rows_checked":sum(next_hour.values()),"edges_per_row":len(ports),
            "control_volumes_per_hour":10,"largest_reconstructed_residual_kWh":worst,
            "center_annual_metrics_per_arm":len(hand),"review":"COMPUTATIONAL_CROSSCHECK_ONLY"}


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root",type=Path,default=Path(__file__).resolve().parent)
    args=parser.parse_args()
    print(json.dumps(independent(args.root),indent=2,allow_nan=False))
