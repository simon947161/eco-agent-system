"""Offline orientation overlay using the existing local Geofabric archive.

Run with the pre-existing D:/apps/Python312/python.exe (Shapely/PyProj).
Copies of prior local public layers belong in runtime_data/facility_spatial;
this script does not retrieve data, alter a QGIS project or infer transport.
"""
import hashlib
import json
from pathlib import Path
import pyproj
import shapely
from pyproj import Transformer
from shapely.geometry import Point, shape
from shapely.ops import transform, unary_union
from cczps_lite.integration.facility_spatial_evidence import EVIDENCE, replay

ROOT = Path('runtime_data/facility_spatial')
STREAM = ROOT/'geofabric_v3_3_network_stream_all_cooma_10km_epsg4283.geojson'
SCOPE = ROOT/'cooma_locality_buffer_10km_epsg7855.geojson'
PINNED_LOCAL = {
    STREAM.name: 'cb2bf376e8ec948a5b7ddea57d08707eeb6cea58464d1f050a31e8d7dd87b44b',
    SCOPE.name: '9948a0f19bb427d065d21a6e2c08374e88933c36f6b31da4489bc3d3dfe8ef88',
}


def load(path, epsg):
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != PINNED_LOCAL[path.name]:
        raise ValueError('LOCAL_LAYER_HASH_MISMATCH')
    data = json.loads(raw)
    name = data.get('crs', {}).get('properties', {}).get('name')
    if name is None or pyproj.CRS.from_user_input(name) != pyproj.CRS.from_epsg(epsg):
        raise ValueError('LOCAL_LAYER_CRS_MISMATCH')
    geometries = [shape(f['geometry']) for f in data['features']]
    if not geometries or any(g.is_empty or not g.is_valid for g in geometries):
        raise ValueError('INVALID_LOCAL_GEOMETRY')
    return geometries, {'file': path.name, 'sha256': hashlib.sha256(raw).hexdigest(), 'crs': f'EPSG:{epsg}', 'features': len(geometries)}


def main():
    archive = replay()
    streams, stream_receipt = load(STREAM, 4283)
    scope, scope_receipt = load(SCOPE, 7855)
    if any(g.geom_type not in ('LineString', 'MultiLineString') for g in streams):
        raise ValueError('EXPECTED_STREAM_LINES')
    boundary = unary_union(scope)
    to_grid = Transformer.from_crs(7844, 7855, always_xy=True, allow_ballpark=False)
    stream_grid = Transformer.from_crs(4283, 7855, always_xy=True, allow_ballpark=False)
    lines = [transform(stream_grid.transform, g) for g in streams]
    rows = []
    for r in archive['records']:
        p = Point(*to_grid.transform(*r['coordinates']))
        rows.append({'source': r['source'], 'objectid': r['objectid'], 'name': r['name'],
                     'inside_existing_study_polygon': boundary.covers(p),
                     'distance_to_nearest_archived_stream_line_m': round(min(p.distance(g) for g in lines)),
                     'interpretation': 'MAP_PROXIMITY_ONLY_NOT_HYDROLOGICAL_CONNECTION'})
    result = {'status': 'OFFLINE_SPATIAL_OVERLAY_EXECUTED',
              'method': 'Euclidean point-to-line distance in EPSG:7855; nearest among archived lines only; rounded to metres, not accuracy',
              'versions': {'pyproj': pyproj.__version__, 'proj': pyproj.proj_version_str, 'shapely': shapely.__version__},
              'local_inputs': [stream_receipt, scope_receipt],
              'transformations': [{'from': 7844, 'to': 7855, 'description': to_grid.description, 'accuracy_m': to_grid.accuracy},
                                  {'from': 4283, 'to': 7855, 'description': stream_grid.description, 'accuracy_m': stream_grid.accuracy}],
              'records': rows, 'temporal_alignment': 'NOT_ESTABLISHED_REGISTER_VS_STATIC_CARTOGRAPHY',
              'environmental_conclusion': 'NOT_ESTABLISHED', 'methane': 'DATA_NOT_READY'}
    (EVIDENCE/'spatial-comparison.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    (EVIDENCE/'actual-facility-replay.json').write_text(json.dumps(archive, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
