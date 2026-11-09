"""Bounded one-attempt official-file acquisition; existing receipts are never retried."""
from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

TASK=Path(__file__).resolve().parent
ROOT=TASK.parents[2]
CACHE=ROOT/'runtime_data/au_landfill_methods'

def main():
    CACHE.mkdir(parents=True,exist_ok=True)
    for item in json.loads((TASK/'source_receipts/download-list.json').read_text()):
        receipt=TASK/'source_receipts'/f"{item['id']}.json"
        if receipt.exists():
            print(item['id'],'EXISTING_RECEIPT_NO_RETRY');continue
        record={**item,'attempted_at_utc':datetime.now(timezone.utc).isoformat(),
                'redistribution':'NOT_REPUBLISHED; original in ignored local cache; rights reviewed in source master',
                'reading_scope':'targeted sections, not assertion of full document reading'}
        try:
            with urlopen(item['url'],timeout=35) as response:
                data=response.read(20_000_001)
                if len(data)>20_000_000:raise ValueError('SIZE_LIMIT')
                if item['format']=='pdf' and not data.startswith(b'%PDF'):raise ValueError('NOT_PDF')
                path=CACHE/f"{item['id']}.{item['format']}";path.write_bytes(data)
                record.update(status='ACQUIRED',resolved_url=response.url,sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),cache_path=path.relative_to(ROOT).as_posix())
        except (HTTPError,URLError,TimeoutError,ValueError,OSError) as exc:
            record.update(status='BLOCKED',reason=str(exc))
        receipt.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
        print(item['id'],record['status'],record.get('bytes',record.get('reason')))

if __name__=='__main__':main()
