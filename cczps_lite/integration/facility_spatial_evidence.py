"""Offline GA point intake for spatial orientation, never emissions inference."""
import hashlib
import json
import math
from pathlib import Path

from cczps_lite.qgis_local_spatial_foundation.hydrology_contract import AUTHORIZED_LONGITUDE_LATITUDE_EXTENT as EXTENT

EVIDENCE = Path(__file__).resolve().parents[2] / 'docs/tasks/climateos_dynamic_quant_001/facility_evidence'


def parse_points(payload, kind):
    if kind not in ('waste', 'wastewater'):
        raise ValueError('UNKNOWN_FACILITY_SOURCE')
    if not isinstance(payload, dict) or 'error' in payload or payload.get('exceededTransferLimit'):
        raise ValueError('PROVIDER_ERROR_OR_TRUNCATION')
    if payload.get('geometryType') != 'esriGeometryPoint' or payload.get('spatialReference', {}).get('wkid') != 7844:
        raise ValueError('GEOMETRY_OR_CRS_MISMATCH')
    features = payload.get('features')
    if not isinstance(features, list) or len(features) > 100:
        raise ValueError('INVALID_FEATURE_SET')
    records, seen = [], set()
    for f in features:
        a, g = f.get('attributes', {}), f.get('geometry', {})
        oid = a.get('objectid')
        if not isinstance(oid, int) or isinstance(oid, bool) or oid in seen:
            raise ValueError('INVALID_OR_DUPLICATE_ID')
        seen.add(oid)
        xy = [g.get('x'), g.get('y')]
        if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in xy):
            raise ValueError('INVALID_COORDINATES')
        # Broad envelope validation only: GDA2020 and WGS84 differ. Exact study
        # polygon membership is checked after a recorded CRS transformation.
        if not (EXTENT['west']-.001 <= xy[0] <= EXTENT['east']+.001 and EXTENT['south']-.001 <= xy[1] <= EXTENT['north']+.001):
            raise ValueError('OUTSIDE_QUERY_ENVELOPE')
        name = a.get('facility_name' if kind == 'waste' else 'feature_name')
        category = a.get('facility_infrastructure_type' if kind == 'waste' else 'feature_subtype')
        if not isinstance(name, str) or not name.strip() or not isinstance(category, str):
            raise ValueError('MISSING_IDENTITY')
        records.append({'source': kind, 'objectid': oid, 'name': name, 'category': category,
                        'coordinates': xy, 'crs': 'EPSG:7844', 'provider_attributes': a,
                        'evidence_class': 'FACILITY_REGISTER_POINT_NOT_MEASUREMENT'})
    return sorted(records, key=lambda r: r['objectid'])


def replay(folder=EVIDENCE):
    folder = Path(folder)
    receipts = json.loads((folder/'receipts.json').read_text(encoding='utf-8'))
    expected = {f'{kind}-{part}.json' for kind in ('waste', 'wastewater') for part in ('points', 'metadata')}
    if len(receipts) != 4 or {r['file'] for r in receipts} != expected:
        raise ValueError('INCOMPLETE_RECEIPTS')
    for r in receipts:
        if hashlib.sha256((folder/r['file']).read_bytes()).hexdigest() != r['sha256']:
            raise ValueError('HASH_MISMATCH')
    records = [r for kind in ('waste', 'wastewater') for r in parse_points(json.loads((folder/f'{kind}-points.json').read_bytes()), kind)]
    groups = {}
    for r in records:
        groups.setdefault(tuple(r['coordinates']), []).append(f"{r['source']}:{r['objectid']}")
    return {'status': 'SPATIAL_ORIENTATION_ONLY', 'records': records,
            'coincident_register_points': [v for v in groups.values() if len(v) > 1],
            'temporal_comparison': 'NOT_ADMITTED_NO_COMMON_OBSERVATION_INTERVAL',
            'methane': 'DATA_NOT_READY', 'environmental_conclusion': 'NOT_ESTABLISHED'}


if __name__ == '__main__':
    print(json.dumps(replay(), ensure_ascii=False, indent=2, allow_nan=False))
