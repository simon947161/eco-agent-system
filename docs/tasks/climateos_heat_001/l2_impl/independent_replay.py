#!/usr/bin/env python3
"""Independent stored-row checks; does not import the L2 solver."""
import csv, gzip, hashlib, json, pathlib, sys

ROOT=pathlib.Path(__file__).resolve().parent
FIX=ROOT/"fixtures"/"paired_hours.csv.gz"
OUT=ROOT/"outputs"

def replay(layout,dt,dx):
    stem=f"L2_V3_{layout}_dt{dt}_dx{dx}"
    compressed=OUT/(stem+"_hourly.csv.gz")
    plain=OUT/(stem+"_hourly.csv")
    if compressed.exists():
        with gzip.open(compressed,"rt",encoding="utf-8",newline="") as stream: rows=list(csv.DictReader(stream))
        output_path=compressed
    else:
        rows=list(csv.DictReader(plain.open(encoding="utf-8",newline="")))
        output_path=plain
    with gzip.open(FIX,"rt",encoding="utf-8",newline="") as f: demand=list(csv.DictReader(f))
    if len(rows)!=8760 or len(demand)!=8760: raise ValueError("row count is not 8760")
    if any(r.get("tag")!="SYNTHETIC" or r.get("layout")!=layout for r in rows): raise ValueError("provenance tag/layout mismatch")
    total={k:sum(float(r[k]) for r in rows) for k in rows[0] if k.endswith("_kwh") and k!="tank_end_kwh"}
    expected=sum(float(r["space_kw"])+float(r["dhw_kw"]) for r in demand)
    service=sum(float(r["qualified_network_kwh"])+float(r["tank_discharge_kwh"])+float(r["backup_kwh"]) for r in rows)
    tank_balance=total["tank_charge_kwh"]-total["tank_discharge_kwh"]-total["tank_loss_kwh"]-total["terminal_dump_kwh"]
    pipe_balance=total["hp_heat_kwh"]-total["network_delivery_kwh"]-total["pipe_ground_loss_kwh"]
    if abs(expected-total["demand_kwh"])>1e-6: raise ValueError("hourly demand does not replay")
    if abs(service-expected)>1e-6: raise ValueError("served service does not equal demand")
    if abs(tank_balance)>1e-5: raise ValueError("tank stock balance fails")
    if abs(pipe_balance)>1e-5: raise ValueError("annual pipe energy balance fails")
    return {"tag":"SYNTHETIC","rows":8760,"demand_kwh":expected,"service_kwh":service,"tank_residual_kwh":tank_balance,"pipe_residual_kwh":pipe_balance,"row_file_sha256":hashlib.sha256(output_path.read_bytes()).hexdigest(),"output_file":output_path.name,"independent_path":"csv/gzip + scalar Python summation; no solver import"}

if __name__=="__main__": print(json.dumps(replay(sys.argv[1],int(sys.argv[2]),float(sys.argv[3])),sort_keys=True))
