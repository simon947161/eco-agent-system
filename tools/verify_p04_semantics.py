"""Offline metadata acceptance only. Does not load or join physical arrays."""
import hashlib
import json
from datetime import date, timedelta
from pathlib import Path

EVIDENCE = Path(__file__).resolve().parents[1] / 'docs/tasks/climateos_regional_public_os_001/evidence/p04_semantics_20261027'


def load_verified(directory=EVIDENCE):
    directory = Path(directory)
    manifest = json.loads((directory / 'manifest.json').read_text(encoding='utf-8'))
    for item in manifest['files']:
        path = directory / item['file']
        if path.parent.resolve() != directory.resolve():
            raise ValueError('Nonlocal evidence path')
        if hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
            raise ValueError('Evidence checksum mismatch: ' + item['file'])
    return {v: json.loads((directory / (v + '-native-header.json')).read_text())
            for v in ('rain_day', 'sm_pct')}


def inspect_semantics(headers):
    result = {'status': 'BLOCKED_NUMERIC_JOIN', 'variables': {}, 'physical_values_read': False}
    for name, header in headers.items():
        variables = header['variables']
        time = variables['time']['attributes']
        if time.get('calendar') != 'gregorian' or time.get('units') != 'days since 1900-01-01' or time.get('bounds') != 'time_bounds':
            raise ValueError('Unreviewed time contract')
        attrs = variables[name]['attributes']
        expected = {'rain_day': 'mm', 'sm_pct': 'fraction of fullness'}[name]
        if attrs.get('units') != expected:
            raise ValueError('Unreviewed unit; no automatic conversion')
        sample = header['coordinate_sample']
        labels = sample['time'] + sample['last_time']
        bounds = sample['time_bounds'] + sample['last_time_bounds']
        if len(labels) != len(bounds):
            raise ValueError('Coordinate length mismatch')
        decoded = []
        for label, (lower, upper) in zip(labels, bounds):
            start, end, point = [date(1900, 1, 1) + timedelta(days=n) for n in (lower, upper, label)]
            next_month = date(start.year + (start.month == 12), start.month % 12 + 1, 1)
            if start.day != 1 or end != next_month or point != end - timedelta(days=1):
                raise ValueError('Unexpected monthly bounds or label')
            decoded.append({'label': point.isoformat(), 'start': start.isoformat(), 'end_boundary': end.isoformat(), 'days': (end-start).days})
        result['variables'][name] = {
            'units': attrs['units'], 'dtype': variables[name]['dtype'],
            'absent_attributes': [key for key in ('scale_factor', 'add_offset', 'missing_value', 'valid_range', 'cell_methods') if key not in attrs],
            'fill_value': attrs.get('_FillValue'), 'sampled_months': decoded,
            'aggregation': 'UNRESOLVED', 'numeric_completeness': 'NOT_TESTED',
            'time_zone_alignment_to_hrs': 'UNRESOLVED',
        }
    return result


if __name__ == '__main__':
    print(json.dumps(inspect_semantics(load_verified()), indent=2))
