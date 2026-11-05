"""One-shot bounded public acquisition; no credentials or paid APIs."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen
from cczps_lite.qgis_local_spatial_foundation.hydrology_contract import AUTHORIZED_LONGITUDE_LATITUDE_EXTENT as E

OUT = Path('docs/tasks/climateos_dynamic_quant_001/facility_evidence')

def main():
    OUT.mkdir(exist_ok=True)
    receipts = []
    for kind, service in [('waste', 'Waste_Management_Facilities'), ('wastewater', 'Wastewater_Treatment_Facilities')]:
        base = f'https://services.ga.gov.au/gis/rest/services/{service}/MapServer/0'
        fields = ('objectid,facility_name,facility_infrastructure_type,operational_status,spatial_confidence'
                  if kind == 'waste' else 'objectid,feature_name,feature_subtype,status,spatial_confidence,feature_source_date,attribute_source_date')
        params = dict(f='json', where='1=1', geometry=','.join(str(E[k]) for k in ['west','south','east','north']),
                      geometryType='esriGeometryEnvelope', inSR=4326, outSR=7844,
                      spatialRel='esriSpatialRelIntersects', outFields=fields,
                      returnGeometry='true', resultRecordCount=100, orderByFields='objectid')
        for suffix, url in [('metadata', base+'?f=pjson'), ('points', base+'/query?'+urlencode(params))]:
            target = OUT / f'{kind}-{suffix}.json'
            if target.exists():
                raise SystemExit(f'Overwrite refused: {target}')
            with urlopen(url, timeout=40) as response:
                raw = response.read(1_000_001)
            if len(raw) > 1_000_000:
                raise ValueError('Response too large')
            payload = json.loads(raw)
            if 'error' in payload or payload.get('exceededTransferLimit'):
                raise ValueError('Provider error or truncated result')
            target.write_bytes(raw)
            receipts.append(dict(file=target.name, url=url, sha256=hashlib.sha256(raw).hexdigest(),
                                 retrieved_at_utc=datetime.now(timezone.utc).isoformat(), bytes=len(raw)))
    (OUT/'receipts.json').write_text(json.dumps(receipts, indent=2)+'\n', encoding='utf-8')
    print('Archived', len(receipts), 'bounded public responses')

if __name__ == '__main__':
    main()
