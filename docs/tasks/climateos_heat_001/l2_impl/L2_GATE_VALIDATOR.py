"""Deterministic pre-run gate check. Reads frozen SYNTHETIC fixtures only."""
import csv
import gzip
import hashlib
import json
import math
from datetime import datetime, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CONTRACT = ROOT / "L2_FROZEN_SYNTHETIC_CONTRACT.json"
P1_INPUTS = ROOT / "fixtures" / "P1_SYNTHETIC_INPUTS.json"
HOURS = ROOT / "fixtures" / "paired_hours.csv.gz"


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
p1 = json.loads(P1_INPUTS.read_text(encoding="utf-8"))
assert contract["status"] == "GATE_PASS"
assert contract["pre_run_gate"]["status"] == "PASS"
assert contract["authorization"]["issue"] == 183
assert contract["l2_geometry"]["topology"].startswith("A stable synthetic waste-heat source")
assert contract["l2_geometry"]["no_third_A_B_pipe"] is True
for key in ("l2_geometry", "l2_fluid_properties", "l2_pipe_properties",
            "l2_flow_and_pumps", "l2_heat_pump_and_tank"):
    assert contract[key]["tag"] == "SYNTHETIC", key
assert p1["tag"] == "SYNTHETIC"
assert p1["version"] == "HEAT-P1/1.0.0"
assert p1["clock"]["hours"] == 8760
assert sha256(P1_INPUTS) == contract["provenance"]["p1_input_sha256"]
assert sha256(HOURS) == contract["provenance"]["p1_hour_fixture_gzip_sha256"]

count = 0
first = last = None
with gzip.open(HOURS, "rt", encoding="utf-8", newline="") as stream:
    reader = csv.DictReader(stream)
    assert tuple(reader.fieldnames) == tuple(contract["time_and_service"]["fixture_columns"])
    for i, row in enumerate(reader):
        assert row["origin"] == "SYNTHETIC"
        assert int(row["hour"]) == i
        stamp = datetime.fromisoformat(row["utc"].replace("Z", "+00:00"))
        if last is not None:
            assert stamp - last == timedelta(hours=1)
        else:
            first = stamp
        last = stamp
        assert float(row["space_kw"]) >= 0 and float(row["dhw_kw"]) >= 0
        count += 1
assert count == 8760
assert first.isoformat() == "2001-01-01T00:00:00+00:00"
assert contract["p1_reference_metrics"]["R0"]["service_kWh"] == contract["p1_reference_metrics"]["R1"]["service_kWh"]
assert contract["resource_gate"]["resource_probe"]["projected_runtime_with_2x_margin_seconds"] < contract["resource_gate"]["resource_probe"]["projected_runtime_budget_seconds"]
assert contract["resource_gate"]["resource_probe"]["output_disk_budget_bytes"] < contract["resource_gate"]["disk_C_available_bytes"]
assert contract["security_and_prohibitions"]["network_during_runs"] is False
assert contract["security_and_prohibitions"]["real_site_or_council_data"] is False

# Deterministic static closure checks, not L2 case calculations.
flow = contract["l2_flow_and_pumps"]["low_loop_design_mass_flow_kg_s"]
rho = contract["l2_fluid_properties"]["density_kg_m3"]
diameter = contract["l2_pipe_properties"]["inside_diameter_m"]
velocity = flow / rho / (math.pi * diameter * diameter / 4)
shortest_segment_m = 40.0
coarse_cell_m = shortest_segment_m / math.ceil(shortest_segment_m / 25.0)
worst_cfl = velocity * 60.0 / coarse_cell_m
assert worst_cfl <= contract["preregistered_acceptance_thresholds"]["courant_number_max"]
highest_elevation_m = 6.0
reference_pressure_pa = contract["l2_flow_and_pumps"]["max_abs_pressure_reference_Pa"]
static_highpoint_pa = reference_pressure_pa - rho * contract["l2_fluid_properties"]["gravity_m_s2"] * highest_elevation_m
minimum_safe_pa = max(contract["l2_flow_and_pumps"]["minimum_absolute_pressure_Pa"], 80000 + 50000)
assert static_highpoint_pa > minimum_safe_pa

print(json.dumps({
    "status": "GATE_PASS",
    "formal_l2_case_outputs_present": False,
    "contract_sha256": sha256(CONTRACT),
    "p1_input_sha256": sha256(P1_INPUTS),
    "p1_hour_fixture_gzip_sha256": sha256(HOURS),
    "hour_rows_verified": count,
    "first_utc": first.isoformat(),
    "last_utc": last.isoformat(),
    "worst_static_cfl": worst_cfl,
    "minimum_T_highpoint_static_pressure_Pa": static_highpoint_pa,
}, sort_keys=True))
