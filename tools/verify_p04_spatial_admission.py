"""Offline, fail-closed verification of pinned public P04 metadata/geometry.

Optional GIS dependencies are isolated; this tool never fetches or joins data.
"""
import argparse
import calendar
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'docs/tasks/climateos_regional_public_os_001/evidence/p04_case001'


def load_verified(directory):
    directory = Path(directory)
    manifest = json.loads((directory / 'manifest.json').read_bytes())
    result = {}
    for entry in manifest['files']:
        name = entry['file']
        if Path(name).name != name:
            raise ValueError('Evidence must be a direct child file')
        raw = (directory / name).read_bytes()
        if hashlib.sha256(raw).hexdigest() != entry['sha256']:
            raise ValueError('Evidence checksum mismatch: ' + name)
        result[name] = json.loads(raw)
    return result


def spatial_check(catchment, station):
    from shapely.geometry import shape, Point
    from shapely.ops import transform
    from pyproj import Transformer
    if catchment.get('exceededTransferLimit') or station.get('exceededTransferLimit'):
        raise ValueError('Truncated evidence')
    if len(catchment['features']) != 1 or len(station['features']) != 1:
        raise ValueError('Exactly one station and catchment required')
    feature, node = catchment['features'][0], station['features'][0]
    props, attrs = feature['properties'], node['attributes']
    if props['stationno'] != '410033' or attrs['stationno'] != '410033':
        raise ValueError('Wrong station')
    if props['netnodeid'] != attrs['hydroid']:
        raise ValueError('Station/network identity mismatch')
    if catchment['crs']['properties']['name'] != 'EPSG:4283' or station['spatialReference']['wkid'] != 4326:
        raise ValueError('Unexpected CRS')
    if props['confidence'] not in (1, 2, 3, 4) or attrs['confidence'] not in (1, 2, 3, 4):
        raise ValueError('Low or unknown publisher confidence')
    geom = shape(feature['geometry'])
    if geom.geom_type != 'MultiPolygon' or geom.is_empty or not geom.is_valid:
        raise ValueError('Invalid polygon; no automatic repair allowed')
    project = Transformer.from_crs(4283, 3577, always_xy=True)
    projected = transform(project.transform, geom)
    station_project = Transformer.from_crs(4326, 3577, always_xy=True)
    point = Point(*station_project.transform(node['geometry']['x'], node['geometry']['y']))
    if not projected.covers(point):
        raise ValueError('Published network node is outside station polygon')
    area = projected.area / 1e6
    return {
        'status': 'VERIFIED_PUBLISHER_GEOMETRY_NOT_SCIENTIFIC_EQUIVALENCE',
        'station_id': '410033', 'network_node_id': attrs['hydroid'],
        'catchment_hydroid': props['hydroid'], 'publisher_confidence_code': props['confidence'],
        'source_crs': 'EPSG:4283', 'area_crs': 'EPSG:3577',
        'topology_valid': True, 'parts': len(geom.geoms),
        'holes': sum(len(p.interiors) for p in geom.geoms),
        'computed_area_km2': area, 'publisher_area_km2': props['albersareakm2'],
        'hrs_reference_area_km2': 1889.8,
        'difference_from_hrs_percent': (area / 1889.8 - 1) * 100,
        'network_node_covered': True, 'node_boundary_distance_m': projected.boundary.distance(point),
        'publisher_near_dist_raw': attrs['near_dist'],
        'snap_method': 'Exact stationno and netnodeid join; no new snapping or geometry repair',
        'new_snap_tolerance_m': None,
        'original_publisher_snap_tolerance': 'NOT_DOCUMENTED_IN_RETURNED_METADATA',
        'scientific_equivalence_to_hrs_polygon': 'PENDING_VERSION_AND_AREA_REVIEW',
    }


def variable_check(metadata):
    variables = metadata['multidimensionalInfo']['variables']
    results = {}
    expected = {f'{y:04}-{m:02}' for y in range(2000, 2026) for m in range(1, 13)}
    for name, unit in [('rain_day', 'mm'), ('sm_pct', 'fraction of fullness')]:
        matches = [v for v in variables if v['name'] == name]
        if len(matches) != 1 or matches[0]['unit'] != unit:
            raise ValueError('Missing or changed variable/unit: ' + name)
        var = matches[0]
        dims = [d for d in var['dimensions'] if d['name'] == 'StdTime']
        if len(dims) != 1:
            raise ValueError('Missing/ambiguous time dimension')
        dates = [datetime.fromtimestamp(v / 1000, timezone.utc) for v in dims[0]['values']]
        if len(dates) != len(set(dates)) or any(d.day != calendar.monthrange(d.year, d.month)[1] for d in dates):
            raise ValueError('Duplicate or non-month-end labels')
        months = {d.strftime('%Y-%m') for d in dates}
        if not expected <= months:
            raise ValueError('Study-period dimension labels missing')
        results[name] = {'description': var['description'], 'raw_unit': unit,
                         'study_month_labels': len(expected), 'all_labels': len(dates),
                         'latest_label_utc': max(dates).isoformat(),
                         'numeric_cell_completeness_verified': False}
    return results


def verify(directory=EVIDENCE):
    evidence = load_verified(directory)
    return {'case_id': 'P04-WATER-SOIL-CLIMATE-001',
            'geometry': spatial_check(evidence['catchment410033.geojson'], evidence['station410033.json']),
            'awra_variables': variable_check(evidence['awra-dimensions.json']),
            'status': 'BLOCKED_NUMERIC_JOIN',
            'blockers': ['HRS daily interval/DST/month assignment and header-unit interpretation unresolved',
                         'AWRA raw fraction versus percent encoding and full-month soil statistic need product contract',
                         'Exact grid revision, basin mask/completeness and scientific QC review pending'],
            'numeric_subset_prepared': False, 'environmental_conclusion': None,
            'waternsw_credential_dependency': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--evidence', type=Path, default=EVIDENCE)
    parser.add_argument('--output', type=Path, default=Path('.local/p04-spatial-admission.json'))
    args = parser.parse_args()
    result = verify(args.evidence)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': result['status'], 'geometry': result['geometry']['status']}))
