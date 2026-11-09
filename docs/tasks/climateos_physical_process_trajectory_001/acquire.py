"""One request per URL, no retries, no credential or protection bypass.

Raw HTML stays ignored. Only public-domain RONI numerical bytes are published.
Re-running reuses receipts, including failures. Other source facts are manually
checked against the snapshot and never treated as independently measured data.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, urllib.request, urllib.error

TASK = Path(__file__).resolve().parent
ROOT = TASK.parents[2]
CACHE = ROOT/'runtime_data/physical-process-trajectory'
URLS = {
    'aggi': 'https://gml.noaa.gov/aggi/aggi.html',
    'gml-rights': 'https://gml.noaa.gov/about/disclaimer.html',
    'roni': 'https://www.cpc.ncep.noaa.gov/data/indices/RONI.ascii.txt',
    'roni-method': 'https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/enso/roni/',
    'nws-rights': 'https://www.weather.gov/disclaimer',
    'scorecard': 'https://www.climatescorecard.org/scorecard/',
    'au-act': 'https://www.legislation.gov.au/C2022A00037/2025-02-20/2025-02-20/text/original/epub/OEBPS/document_1/document_1.html',
}

def main():
    CACHE.mkdir(parents=True, exist_ok=True)
    out = TASK/'evidence/acquisition.json'
    out.parent.mkdir(exist_ok=True)
    records = json.loads(out.read_text()) if out.exists() else {}
    for key, url in URLS.items():
        if key in records:
            print(key, 'ALREADY_ATTEMPTED'); continue
        row = {'url': url, 'retrieved_at': datetime.now(timezone.utc).isoformat(), 'attempts': 1}
        # Persist BEFORE request; an interrupted attempt is not silently retried.
        records[key] = row | {'status': 'ATTEMPT_STARTED'}
        out.write_text(json.dumps(records, indent=2), encoding='utf-8')
        try:
            request = urllib.request.Request(url, headers={'User-Agent': 'ClimateOS bounded public research; no periodic harvesting'})
            with urllib.request.urlopen(request, timeout=35) as response:
                raw = response.read(3_000_001)
                if len(raw) > 3_000_000: raise ValueError('SIZE_BUDGET')
                if b'cf-chl-' in raw or b'captcha' in raw.lower(): raise ValueError('CHALLENGE_STOP')
                row.update(status='ACQUIRED', http_status=response.status, final_url=response.url,
                           bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(),
                           last_modified=response.headers.get('Last-Modified'),
                           content_type=response.headers.get('Content-Type'))
                (CACHE/(key+'.raw')).write_bytes(raw)
                if key == 'roni':
                    if not raw.lstrip().startswith(b'SEAS'): raise ValueError('RONI_HEADER')
                    (TASK/'evidence/RONI.ascii.txt').write_bytes(raw)
        except (urllib.error.URLError, TimeoutError, ValueError) as exc:
            row.update(status='STOP_NO_RETRY', error=str(exc))
        records[key] = row
        out.write_text(json.dumps(records, indent=2), encoding='utf-8')
        print(key, row['status'], row.get('bytes'), row.get('sha256'))

if __name__ == '__main__': main()
