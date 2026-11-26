"""Non-physical workload resource probe; emits no L2 case values."""
import csv
import json
import pathlib
import sys
import time
import tracemalloc

OUT = pathlib.Path(__file__).with_name("resource_profile_output.csv")
NOPS = 10_000_000
NCELLS = 76
buf = [float(i) / NCELLS for i in range(NCELLS)]
start = time.perf_counter()
for n in range(NOPS):
    i = n % NCELLS
    j = i - 1 if i else NCELLS - 1
    buf[i] += (buf[j] - buf[i]) * 0.125
elapsed = time.perf_counter() - start

tracemalloc.start()
state_arrays = [[12.0] * NCELLS for _ in range(8)]
inventory = [0.0] * 16
with OUT.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["tag", "hour", *["metric_" + str(i) for i in range(24)]])
    for h in range(8760):
        w.writerow(["SYNTHETIC_RESOURCE_ONLY", h, *([0.0] * 24)])
current_bytes, peak_bytes = tracemalloc.get_traced_memory()
tracemalloc.stop()

print(json.dumps({
    "tag": "SYNTHETIC_RESOURCE_ONLY_NOT_MODEL_OUTPUT",
    "python": sys.version,
    "sample_operations": NOPS,
    "sample_cells": NCELLS,
    "sample_seconds": elapsed,
    "planned_time_refinement_cell_updates": 139_809_600,
    "planned_space_refinement_cell_updates": 136_656_000,
    "planned_total_cell_updates": 276_465_600,
    "projected_seconds_2x_margin": 2 * elapsed * 276_465_600 / NOPS,
    "csv_rows": 8760,
    "csv_bytes": OUT.stat().st_size,
    "buffer_bytes": sys.getsizeof(buf) + sum(sys.getsizeof(x) for x in buf),
    "representative_state_bytes": sum(sys.getsizeof(a) + sum(sys.getsizeof(x) for x in a) for a in state_arrays) + sys.getsizeof(inventory) + sum(sys.getsizeof(x) for x in inventory),
    "representative_tracemalloc_peak_bytes": peak_bytes,
}, sort_keys=True))

