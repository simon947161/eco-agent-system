"""Audit the published paired electricity readings; stdout is the JSON receipt."""
import csv
import hashlib
import io
import json
import sys
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / 'source/04_hourly_energy_data.txt'
FILE_HASH = 'c5753f3b888c4f92e14bac9684f76f0f68b87fa22cf9bb0a146a80bdc41d4b37'
SCHEMA = ['date (dd.mm.yyyy)', 'time (hh:mm)', 'ref_sys_1 (kW)', 'el_boiler (kW)']


def parse(raw):
    reader = csv.reader(io.StringIO(raw.decode('ascii')), delimiter='\t')
    if [name.strip() for name in next(reader)] != SCHEMA:
        raise ValueError('Unexpected meter fields or units')
    rows = []
    for day, hour, ref, boiler in reader:
        stamp = datetime.strptime(day + ' ' + hour, '%d.%m.%Y %H:%M')
        if rows and stamp - rows[-1][0] != timedelta(hours=1):
            raise ValueError('Gap, duplicate or disorder at ' + str(stamp))
        powers = [Decimal(s.replace(',', '.')) for s in (ref, boiler)]
        if any(not x.is_finite() or x < 0 for x in powers):
            raise ValueError('Invalid meter value')
        rows.append((stamp, *powers))
    if len(rows) != 240 or rows[0][0] != datetime(2021, 1, 5):
        raise ValueError('Window differs from source README')
    return rows


def summarize(group):
    return {
        'hours': len(group),
        'ref_kw_range': [float(min(r[1] for r in group)), float(max(r[1] for r in group))],
        'mean_boiler_kw': round(float(sum(r[2] for r in group) / len(group)), 6),
    }


def calculate(raw):
    rows = parse(raw)
    sha = hashlib.sha256(raw).hexdigest()
    if sha != FILE_HASH:
        raise ValueError('Input differs from admitted source')
    ranked = sorted(rows, key=lambda r: (r[1], r[0]))
    quarter = len(rows) // 4
    cleaned = io.StringIO()
    writer = csv.writer(cleaned, lineterminator='\n')
    writer.writerow(['timestamp_source_clock', 'ref_system_1_electric_kw', 'electric_boiler_kw'])
    for t, ref, boiler in rows:
        writer.writerow([t.isoformat(timespec='minutes'), ref, boiler])
    normalized = cleaned.getvalue().encode('utf-8')
    audit = {
        'source': '10.5281/zenodo.6563580', 'input_sha256': sha,
        'clean_sha256': hashlib.sha256(normalized).hexdigest(),
        'measurement': 'hourly electrical power readings, original clock, timezone unspecified',
        'full_window': summarize(rows),
        'lowest_quarter_by_refrigeration_kw': summarize(ranked[:quarter]),
        'highest_quarter_by_refrigeration_kw': summarize(ranked[-quarter:]),
        'site_heat_saved_kwh': None, 'three_arm_causal_effect': 'DATA_NOT_READY',
    }
    return normalized, audit


if __name__ == '__main__':
    data, audit = calculate(INPUT.read_bytes())
    if len(sys.argv) == 2:
        Path(sys.argv[1]).write_bytes(data)
    elif len(sys.argv) != 1:
        raise SystemExit('usage: python replay.py [output_clean_csv]')
    print(json.dumps(audit, indent=2, allow_nan=False))
