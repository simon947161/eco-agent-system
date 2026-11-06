"""One-shot documented public files only; legal/source gates checked first.

No retry/fallback. Originals remain in git-ignored runtime_data. Never execute
downloaded scripts. Re-running refuses existing destinations.
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'runtime_data/local_case_method_intake'
LOG=Path(__file__).parent/'evidence/acquisition.json'
FILES=[
 {'candidate':'A-FOGO','name':'cooma-fogo-2018.pdf','url':'https://www.epa.nsw.gov.au/sites/default/files/18p0747_snowymonaro-cooma-fogo-case-study.pdf','licence':'EPA CC BY4 current policy for EPA-owned text/data; excluded third-party photos not republished','kind':'OFFICIAL_HISTORICAL_CONTEXT_NOT_GAS_OBSERVATIONS'},
 {'candidate':'B2','name':'Data for Network SL1.zip','url':'https://zenodo.org/records/17718964/files/Data%20for%20Network%20SL1.zip?download=1','md5':'111905ec94e77b483048b974c38564e9','licence':'CC BY 4.0 verified in publisher embedded metadata; Li,Jiuling, Sewer CH4 v1, DOI10.5281/zenodo.17718964','kind':'DATASET_FILE_NOT_YET_QC_ADMITTED'},
 {'candidate':'B2','name':'Fig2_S2.zip','url':'https://zenodo.org/records/17718964/files/Fig2_S2.zip?download=1','md5':'9efacaa75f34959249f509727ac6350c','licence':'CC BY 4.0, same verified record','kind':'SOURCE_DATA_AND_CODE_NOT_YET_QC_ADMITTED'},
]


def main():
    OUT.mkdir(exist_ok=True);records=[];stopped=set();total=0
    if LOG.exists():raise SystemExit('One-shot ledger exists; do not reacquire')
    for item in FILES:
        r={**item,'retrieved_at_utc':datetime.now(timezone.utc).isoformat()}
        destination=OUT/item['name']
        if item['candidate'] in stopped:r['status']='SKIPPED_CANDIDATE_STOP'
        elif destination.exists():raise SystemExit('Existing original, refusing overwrite')
        else:
            try:
                with urlopen(item['url'],timeout=40) as response:
                    size=int(response.headers.get('Content-Length','0'))
                    if size>50_000_000 or total+size>100_000_000:raise ValueError('SIZE_GATE')
                    raw=response.read(min(50_000_001,100_000_001-total))
                    r.update(http_status=response.status,mime=response.headers.get('Content-Type'),final_url=response.url)
                if len(raw)>50_000_000 or total+len(raw)>100_000_000:raise ValueError('SIZE_GATE')
                if 'md5' in item and hashlib.md5(raw).hexdigest()!=item['md5']:raise ValueError('PROVIDER_MD5_MISMATCH')
                if item['name'].endswith('.pdf') and not raw.startswith(b'%PDF'):raise ValueError('NOT_PDF')
                if item['name'].endswith('.zip') and not raw.startswith(b'PK'):raise ValueError('NOT_ZIP')
                destination.write_bytes(raw);total+=len(raw)
                r.update(status='ACQUIRED_NOT_YET_ADMITTED',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),local_original=destination.relative_to(ROOT).as_posix())
            except Exception as exc:
                r.update(status='BLOCKED_STOPPED_NO_RETRY',error=f'{type(exc).__name__}: {exc}');stopped.add(item['candidate'])
        records.append(r)
        LOG.write_text(json.dumps({'records':records,'acquired_total_bytes':total,'cap_total_bytes':100000000,'cap_single_bytes':50000000},indent=2)+'\n',encoding='utf-8')
        print(item['name'],r['status'],r.get('bytes',r.get('error')))


if __name__=='__main__':main()
