"""Bounded public metadata snapshots. One attempt/address, no authentication.

Raw copyrighted web pages stay git-ignored; only factual extraction and hashes
are candidates for publication. No GIS download or source admission implied.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, urllib.request

T=Path(__file__).resolve().parent
ROOT=T.parents[2]
DEST=ROOT/'runtime_data/global_natural_atlas_metadata'
SOURCES={
 'm49':'https://unstats.un.org/unsd/methodology/m49/overview/',
 'scorecard':'https://www.climatescorecard.org/scorecard/',
 'reports':'https://www.climatescorecard.org/reports/',
 'ndc':'https://unfccc.int/NDCREG',
}

def main():
    DEST.mkdir(parents=True,exist_ok=True); (T/'evidence').mkdir(exist_ok=True)
    out=T/'evidence/acquisition.json'
    if out.exists(): raise SystemExit('ALREADY_ATTEMPTED; use local snapshots, do not retry')
    receipts=[]
    for key,url in SOURCES.items():
        r={'id':key,'url':url,'retrieved_at_utc':datetime.now(timezone.utc).isoformat(),'attempts':1,'raw_publication':'NOT_REDISTRIBUTED_HTML'}
        try:
            with urllib.request.urlopen(url,timeout=40) as response:
                body=response.read(3000001)
                assert len(body)<=3000000,'SIZE_LIMIT'
                r.update(status=response.status,bytes=len(body),sha256=hashlib.sha256(body).hexdigest())
                (DEST/(key+'.html')).write_bytes(body)
        except Exception as exc: r.update(status='BLOCKED',reason=str(exc))
        receipts.append(r)
        out.write_text(json.dumps(receipts,indent=2)+'\n',encoding='utf-8',newline='\n')
    print([(r['id'],r['status'],r.get('bytes')) for r in receipts])

if __name__=='__main__':main()
