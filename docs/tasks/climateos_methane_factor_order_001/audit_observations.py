"""Offline structural audit only. No concentration conversion or attribution."""
import argparse
from collections import Counter
from datetime import datetime, timedelta, timezone
import hashlib
import json
import math
from pathlib import Path
import zipfile

HERE = Path(__file__).resolve().parent
ZIP_SHA = '2fcf772a81598f5fcfcde63af56e822905f518a24d4efd681cfc5b3e564b0cce'
MET_SHA = '38150a86d6f95a375757fc39173036b1f75950ed29f265f03bfa4404ee77fbe1'
MEMBER = 'brw/ch4_brw_surface-insitu_1_ccgg_HourlyData.txt'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def valid(value, minimum=0):
    x = float(value)
    return math.isfinite(x) and x >= minimum

def unique(rows):
    result = {}
    for key, row in rows:
        if key in result:
            raise ValueError('Duplicate UTC timestamp: ' + key)
        dt = datetime.fromisoformat(key.replace('Z', '+00:00'))
        if dt.utcoffset() != timedelta(0) or dt.minute or dt.second:
            raise ValueError('Not a UTC hour start')
        result[key] = row
    return result

def precision_gate(metadata):
    required = ('pressure_uncertainty', 'temperature_uncertainty', 'humidity_uncertainty',
                'humidity_reference', 'sensor_heights', 'representativeness_budget')
    return all(metadata.get(k) is not None for k in required)

def audit(ch4_text, met_text):
    lines = ch4_text.splitlines()
    header = next(line.split() for line in lines if line.startswith('site_code '))
    records = [dict(zip(header, line.split(), strict=True)) for line in lines
               if line.startswith('BRW 2024 ')]
    ch4 = unique((r['datetime'], r) for r in records)
    met_records = []
    for line in met_text.splitlines():
        if not line.strip() or line.startswith('#'):
            continue
        fields = line.split()
        if len(fields) != 14 or fields[0] != 'BRW' or fields[1] != '2024':
            raise ValueError('Unexpected meteorology schema/site/year')
        dt = datetime(*(int(v) for v in fields[1:5]), tzinfo=timezone.utc)
        met_records.append((dt.isoformat().replace('+00:00', 'Z'), fields))
    met = unique(met_records)
    expected = {(datetime(2024, 1, 1, tzinfo=timezone.utc) + timedelta(hours=h)).isoformat().replace('+00:00', 'Z') for h in range(8784)}
    if (set(ch4) | set(met)) - expected:
        raise ValueError('Unexpected timestamp outside 2024')
    overlap = sorted(set(ch4) & set(met))
    losses = Counter()
    retained = []
    for key in overlap:
        c, m = ch4[key], met[key]
        # Exclusive waterfall. Non-background is not equivalent to invalid measurement.
        if not valid(c['value']) or not valid(c['value_unc']):
            losses['ch4_value_or_uncertainty_missing'] += 1
        elif c['qcflag'] != '...':
            losses['conservative_background_qc_exclusion'] += 1
        elif not (valid(m[8], 1) and valid(m[9], -273.14) and valid(m[11], -273.14)
                  and valid(m[12]) and float(m[12]) <= 100):
            losses['pressure_temperature_humidity_missing'] += 1
        else:
            retained.append(key)
    return {
        'status': 'NO_VALID_PAIR', 'audit_scope': 'structural quality checks; no P1 numerical comparison',
        'year': 2024, 'expected_hours': 8784, 'ch4_rows': len(ch4), 'met_rows': len(met),
        'ch4_absent_hours': len(expected-set(ch4)), 'met_absent_hours': len(expected-set(met)),
        'exact_utc_overlap': len(overlap), 'exclusive_losses': dict(losses),
        'complete_background_timestamp_matches': len(retained),
        'precision_and_height_gate_exclusions': len(retained), 'science_eligible_pairs': 0,
        'qc_counts_all_ch4_rows': dict(Counter(r['qcflag'] for r in records)),
        'intake_heights_m': sorted({r['intake_height'] for r in records}),
        'instruments': sorted({r['instrument'] for r in records}),
        'monthly_overlap_counts': dict(Counter(k[:7] for k in overlap)),
        'missing_counts_met_all_rows': {name: sum(not valid(r[i], low) or (i==12 and float(r[i])>100) for r in met.values())
            for name, i, low in [('station_pressure',8,1),('T2m',9,-273.14),('T10m',10,-273.14),('Ttower',11,-273.14),('RH',12,0),('wind_speed',6,0),('wind_direction',5,0),('precipitation',13,0)]},
        'first_complete_example': {'utc': retained[0], 'ch4': ch4[retained[0]], 'met_original_fields': met[retained[0]]} if retained else None,
        'missing_precision_metadata': ['pressure_uncertainty','temperature_uncertainty','humidity_uncertainty','humidity_reference','sensor_heights','representativeness_budget'],
        'numerical_comparison_run': False, 'fixed_2ppm_run': False,
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-dir', type=Path)
    args = parser.parse_args()
    evidence = HERE/'evidence'
    evidence.mkdir(exist_ok=True)
    if args.source_dir:
        src = args.source_dir
        raw = (src/'ch4_brw_surface-insitu_ccgg_text.zip').read_bytes()
        met_raw = (src/'met_brw_insitu_1_obop_hour_2024.txt').read_bytes()
        if sha(raw) != ZIP_SHA or sha(met_raw) != MET_SHA:
            raise ValueError('Original file checksum mismatch')
        if (src/'ch4_brw_surface-insitu_ccgg_text.zip.sha256').read_text().split()[0] != ZIP_SHA:
            raise ValueError('Publisher checksum mismatch')
        with zipfile.ZipFile(src/'ch4_brw_surface-insitu_ccgg_text.zip') as z:
            text = z.read(MEMBER).decode('utf-8')
        # Exact retained lines, original ordering and newline normalization documented.
        selected = [line for line in text.splitlines() if line.startswith('#') or line.startswith('site_code ') or line.startswith('BRW 2024 ')]
        (evidence/'ch4_brw_2024_subset.txt').write_bytes(('\n'.join(selected)+'\n').encode())
        (evidence/'met_brw_2024.txt').write_bytes(met_raw)
    ch4_raw = (evidence/'ch4_brw_2024_subset.txt').read_bytes()
    met_raw = (evidence/'met_brw_2024.txt').read_bytes()
    if sha(ch4_raw) != '152357dd30ca8ce5e80ec3d51ce4414405b783e1b2bb8a6f04bcd95be729edb3' or sha(met_raw) != MET_SHA:
        raise ValueError('Committed audit inputs changed; stop and review provenance')
    result = audit(ch4_raw.decode(), met_raw.decode())
    result['file_hashes'] = {'original_zip': ZIP_SHA, 'original_met': MET_SHA,
        'committed_ch4_subset': sha(ch4_raw), 'committed_met': sha(met_raw)}
    (evidence/'quality_audit.json').write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='first_complete_example'}, indent=2))

if __name__ == '__main__':
    main()
