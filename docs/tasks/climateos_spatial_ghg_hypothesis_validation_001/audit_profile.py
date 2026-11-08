"""Offline, structural audit only. Does not import a physical or climate model."""
import argparse
import csv
import hashlib
import io
import json
import math
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def digest(data):
    return hashlib.sha256(data).hexdigest()


def finite(value):
    try:
        v = float(value)
        return v if math.isfinite(v) else None
    except (ValueError, TypeError):
        return None


def rows(path):
    reader = csv.DictReader(io.StringIO(path.read_text(encoding='utf-8')),
                            skipinitialspace=True)
    return [{k.strip(): v.strip() for k, v in row.items()} for row in reader]


def summary(values):
    vals = [finite(x) for x in values]
    good = [x for x in vals if x is not None]
    return {'finite': len(good), 'missing_or_nonfinite': len(vals)-len(good),
            'min': min(good) if good else None, 'max': max(good) if good else None}


def audit(root=ROOT):
    manifest = json.loads((root/'INPUT_MANIFEST.json').read_text(encoding='utf-8'))
    for entry in manifest['files']:
        raw = (root/entry['path']).read_bytes()
        if digest(raw) != entry['sha256'] or len(raw) != entry['bytes']:
            raise ValueError('Input identity mismatch: '+entry['path'])
    profile = rows(root/manifest['profile_path'])
    met = rows(root/manifest['met_path'])
    protocol = json.loads((root/'PROFILE_PROTOCOL.json').read_text(encoding='utf-8'))
    metadata = json.loads((root/'METADATA_GATES.json').read_text(encoding='utf-8'))
    blocked = [k for k in protocol['required_global_evidence']
               if metadata.get(k, {}).get('status') != 'VERIFIED']
    reasons = Counter()
    structurally_usable = []
    for i, row in enumerate(profile):
        issues = []
        for key in ('Pressure(mb)', 'T(C)', 'CH4(ppb)', 'ch4_err', 'RH(%)',
                    'Alt(m)', 'Lat(N)', 'Lon(E)', 'alt_err_ch4-(m)', 'alt_err_ch4+(m)'):
            if finite(row[key]) is None:
                issues.append('missing_or_nonfinite:'+key)
        if not issues:
            if float(row['Pressure(mb)']) <= 0: issues.append('nonpositive_pressure')
            if float(row['T(C)']) <= -273.15: issues.append('nonpositive_absolute_temperature')
            if float(row['CH4(ppb)']) < 0: issues.append('negative_ch4')
            if float(row['ch4_err']) < 0: issues.append('negative_uncertainty')
            if not 0 <= float(row['RH(%)']) <= 100: issues.append('rh_outside_0_100')
            if not -90 <= float(row['Lat(N)']) <= 90: issues.append('invalid_latitude')
            if not -180 <= float(row['Lon(E)']) <= 180: issues.append('invalid_longitude')
            if any(float(row[k]) < 0 for k in ('alt_err_ch4-(m)', 'alt_err_ch4+(m)')):
                issues.append('negative_diffusion_span')
        reasons.update(issues)
        if not issues: structurally_usable.append(i)
    layers = []
    for low, high in protocol['proposed_layers_m']:
        in_layer = [i for i in structurally_usable if low <= float(profile[i]['Alt(m)']) < high]
        contained = [i for i in in_layer
                     if float(profile[i]['Alt(m)'])-float(profile[i]['alt_err_ch4-(m)']) >= low
                     and float(profile[i]['Alt(m)'])+float(profile[i]['alt_err_ch4+(m)']) < high]
        layers.append({'nominal_altitude_bounds_m': [low, high],
                       'rows_with_centres': len(in_layer),
                       'rows_with_ch4_diffusion_support_inside_band': len(contained),
                       'independent_samples': None, 'quantitative_comparison_admitted': False})
    times = [datetime.strptime(r['DateTime(yyyy-mm-dd HH:MM:SS)'], '%Y-%m-%d %H:%M:%S') for r in profile]
    clock_delta = [abs((t-t.replace(hour=0, minute=0, second=0)).total_seconds()
                       - float(r['SecondsFromMidnight(s)'])) for t, r in zip(times, profile)]
    return {'audit_version': '1.0', 'scope': 'one original profile; structural QC, no concentration conversion',
            'global_metadata_blockers': blocked,
            'stage2_status': 'NO_VALID_VERTICAL_PROFILE' if blocked else 'REQUIRES_SEPARATE_SCIENTIFIC_REVIEW',
            'profile_rows': len(profile), 'met_rows': len(met),
            'field_summary': {k: summary([r[k] for r in profile]) for k in profile[0] if not k.startswith('DateTime')},
            'row_structural_failures': dict(reasons),
            'structurally_usable_rows': len(structurally_usable),
            'globally_admitted_comparison_rows': 0,
            'time_utc_start': min(times).isoformat()+'Z', 'time_utc_end': max(times).isoformat()+'Z',
            'duplicate_formatted_timestamps': len(times)-len(set(times)),
            'duplicate_fractional_seconds': len(profile)-len({r['SecondsFromMidnight(s)'] for r in profile}),
            'time_reversals': sum(b < a for a,b in zip(times,times[1:])),
            'maximum_formatted_clock_difference_seconds': max(clock_delta),
            'met_flight_flags': dict(Counter(r['Flight'] for r in met)),
            'layers': layers, 'p1_executed': False, 'counterfactual_executed': False,
            'missing_code_note': 'NaN present; finite sentinels remain under provider QC uncertainty. No new QC flag invented.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', help='Compare with committed deterministic QC result')
    args = parser.parse_args()
    result = audit()
    target = ROOT/'PROFILE_QC.json'
    if args.check:
        assert result == json.loads(target.read_text(encoding='utf-8')), 'QC output differs'
        print('PASS: input hashes and deterministic structural QC')
    else:
        target.write_text(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False)+'\n', encoding='utf-8')
        print(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False))
