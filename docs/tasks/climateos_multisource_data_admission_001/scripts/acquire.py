"""Six-file, 75 MB bounded acquisition for approved public candidates. No retries."""
import argparse,hashlib,json,time,urllib.request,urllib.error
from datetime import datetime,timezone
from pathlib import Path
T=Path(__file__).resolve().parents[1]
BASE='https://www.ncei.noaa.gov/data/global-historical-climatology-network-monthly/v4/precipitation/access/'
URLS={s:BASE+s+'.csv' for s in ('ASN00072150','ASN00074104','ASN00072008')}
def save(v):
    (T/'DOWNLOAD_RECEIPTS.json').write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def get(key):
    f=T/'DOWNLOAD_RECEIPTS.json';rows=json.loads(f.read_text()) if f.exists() else []
    if any(r['id']==key for r in rows):raise SystemExit('ALREADY_ATTEMPTED_NO_RETRY')
    if len(rows)>=6 or sum(r.get('bytes',r.get('bytes_received',0)) for r in rows)>=75_000_000:raise SystemExit('BUDGET_EXHAUSTED')
    cap=min(25_000_000,75_000_000-sum(r.get('bytes',r.get('bytes_received',0)) for r in rows))
    rec={'id':key,'url':URLS[key],'product_id':'GHCNM_V4_PRCP','started_utc':datetime.now(timezone.utc).isoformat(),'status':'ATTEMPT_STARTED',
         'plan_sha256':hashlib.sha256((T/'PRE_ACCESS_PLAN.md').read_bytes()).hexdigest(),'max_bytes':cap,'attempt':1}
    rows.append(rec);save(rows);h=hashlib.sha256();n=0;start=time.monotonic()
    rawdir=T/'evidence/raw';rawdir.mkdir(parents=True,exist_ok=True);out=rawdir/(key+'.csv')
    try:
        with urllib.request.urlopen(urllib.request.Request(URLS[key],headers={'User-Agent':'ClimateOS-bounded-research/1'}),timeout=30) as r:
            rec.update(http_status=r.status,final_url=r.url,content_type=r.headers.get('Content-Type'),last_modified=r.headers.get('Last-Modified'))
            if r.status!=200:raise ValueError('NON_200')
            with out.open('wb') as w:
                while True:
                    b=r.read(65536)
                    if not b:break
                    n+=len(b)
                    if n>cap or time.monotonic()-start>90:raise ValueError('SIZE_OR_TIME_BUDGET')
                    w.write(b);h.update(b)
            rec.update(status='DOWNLOADED_PENDING_ADMISSION',bytes=n,sha256=h.hexdigest(),local_path=out.relative_to(T).as_posix())
    except Exception as e:
        code=getattr(e,'code',None)
        rec.update(status='NOT_FOUND_404' if code==404 else 'ACCESS_RESTRICTED' if code in (401,403,499) else 'ACCESS_FAILED',http_status=code,error=str(e),bytes_received=n)
    rec['completed_utc']=datetime.now(timezone.utc).isoformat();save(rows);print(json.dumps(rec))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('id',choices=URLS);get(p.parse_args().id)
