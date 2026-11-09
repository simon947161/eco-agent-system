"""One bounded public candidate; no retry, no authentication, no models."""
from pathlib import Path
import hashlib, json, re, urllib.request
from datetime import datetime, timezone

T = Path(__file__).resolve().parent
URL = 'https://zenodo.org/records/17718964'
FILE = URL + '/files/Data%20for%20Network%20SL1.zip?download=1'
EXPECTED = 'd559b1c81e31090c7563accea4091b215c4a0d533d0a23d79b251dd83b9cb589'

def main():
    out = T/'evidence/open-case-acquisition.json'
    if out.exists():
        raise SystemExit('Already attempted: inspect receipt, do not repeat addresses')
    receipt = {'candidate_count':1, 'attempted_at_utc':datetime.now(timezone.utc).isoformat(),
               'record':URL, 'url':FILE, 'author':'Jiuling Li', 'version':'v1, 2025-11-26',
               'doi':'10.5281/zenodo.17718964', 'attempts':[]}
    try:
        bodies=[]
        for url in [URL, FILE]:
            receipt['attempts'].append({'url':url, 'status':'STARTED'})
            with urllib.request.urlopen(url,timeout=45) as response:
                body=response.read(1000001)
                assert len(body)<=1000000, 'SIZE_LIMIT'
                receipt['attempts'][-1].update(status=response.status,bytes=len(body),sha256=hashlib.sha256(body).hexdigest())
                bodies.append(body)
        html=bodies[0].decode('utf-8')
        assert 'creativecommons.org/licenses/by/4.0' in html or '"id": "cc-by-4.0"' in html, 'LICENCE_NOT_CONFIRMED'
        assert hashlib.sha256(bodies[1]).hexdigest()==EXPECTED, 'RAW_SHA_MISMATCH'
        assert hashlib.md5(bodies[1]).hexdigest()=='111905ec94e77b483048b974c38564e9', 'PUBLISHER_MD5'
        raw=T/'evidence/raw/SL1.zip'; raw.parent.mkdir(exist_ok=True)
        raw.write_bytes(bodies[1])
        receipt.update(status='RAW_BYTES_VERIFIED',licence='CC-BY-4.0',licence_locator='record HTML rights / Creative Commons Attribution 4.0',
                       licence_url='https://creativecommons.org/licenses/by/4.0/',raw='evidence/raw/SL1.zip',
                       sha256=EXPECTED, redistribution='CC-BY-4.0 attribution; ZIP unmodified; derived conversion explicitly marked')
    except Exception as exc:
        receipt.update(status='OPEN_CASE_DATA_NOT_READY',reason=str(exc))
    out.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(receipt['status'])

if __name__=='__main__': main()
