"""Bounded one-shot public source acquisition. Never retry a recorded attempt.

Run inventory, select, archive, indices separately. No credentials or mirrors.
Large raw files stay in ignored runtime_data; evidence stores receipts.
"""
import argparse, hashlib, json, math, time, urllib.request
from datetime import datetime, timezone
from pathlib import Path

TASK = Path(__file__).resolve().parents[1]
ROOT = TASK.parents[2]
CACHE = ROOT / 'runtime_data/enso_regional_weather'
EVIDENCE = TASK / 'evidence'
BASE = 'https://www.ncei.noaa.gov/data/ghcnm/v4/precipitation/'
FILES = {
 'inventory': (BASE+'doc/ghcn-m_v4_prcp_inventory.txt',16_000_000),
 'archive': (BASE+'archive/ghcn-m_v4.00.00_prcp_s16970101_e20260930_c20261004.tar.gz',260_000_000),
 'dmi': ('https://psl.noaa.gov/data/timeseries/month/data/dmi.had.long.data',100_000),
 'aao': ('https://www.cpc.ncep.noaa.gov/products/precip/CWlink/daily_ao_index/aao/monthly.aao.index.b79.current.ascii',100_000)
}
def write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj,indent=2,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf-8',newline='\n')
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def acquire(key):
    receipt=EVIDENCE/(key+'-receipt.json')
    if receipt.exists(): raise SystemExit('ALREADY_ATTEMPTED: '+key)
    url, cap=FILES[key]; CACHE.mkdir(parents=True,exist_ok=True)
    state={'url':url,'started_utc':datetime.now(timezone.utc).isoformat(), 'status':'ATTEMPT_STARTED',
           'max_bytes':cap,'attempt':1,'plan_sha256':sha(TASK/'PLAN.json'),
           'preregistration_sha256':sha(TASK/'PRE_REGISTERED_ANALYSIS_PLAN.md')}
    write(receipt,state); start=time.monotonic(); count=0; digest=hashlib.sha256()
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'ClimateOS-bounded-research/1'}),timeout=35) as response:
            state.update(http_status=response.status, final_url=response.url,content_type=response.headers.get('Content-Type'),last_modified=response.headers.get('Last-Modified'))
            if response.status!=200: raise ValueError('NON_200')
            with (CACHE/key).open('wb') as out:
                while True:
                    chunk=response.read(1024*1024)
                    if not chunk: break
                    count+=len(chunk)
                    if count>cap or time.monotonic()-start>300: raise ValueError('BOUNDED_LIMIT')
                    out.write(chunk);digest.update(chunk)
            state.update(status='DOWNLOADED',bytes=count,sha256=digest.hexdigest())
    except Exception as exc:
        state.update(status='BLOCKED_NO_RETRY',bytes_received=count,error_type=type(exc).__name__,error=str(exc))
    state['completed_utc']=datetime.now(timezone.utc).isoformat(); write(receipt,state); print(json.dumps(state))
def distance(lat,lon,centre):
    a,b=map(math.radians,[lat,centre[0]]); dl=math.radians(lon-centre[1]);da=a-b
    return 6371*2*math.asin(min(1,math.sqrt(math.sin(da/2)**2+math.cos(a)*math.cos(b)*math.sin(dl/2)**2)))
def select():
    target=TASK/'REGIONS.json'
    if target.exists(): raise SystemExit('SELECTION_ALREADY_FROZEN')
    plan=json.loads((TASK/'PLAN.json').read_text()); stations=[]
    for line in (CACHE/'inventory').read_text().splitlines():
        # GHCN uses FIPS, not ISO alpha-2: AS=Australia, AU=Austria.
        if not line.startswith('AS'): continue
        stations.append(dict(id=line[:11],latitude=float(line[12:20]),longitude=float(line[21:30]),
            elevation=float(line[31:37]),name=line[41:79].strip(),wmo=line[80:85].strip(),first=int(line[86:90]),last=int(line[91:95]),inventory_line=line))
    result=[]
    for region in plan['regions']:
        a,b,c,d=region['box']; eligible=[]
        for s in stations:
            dist=distance(s['latitude'],s['longitude'],region['centre'])
            if s['first']<=1961 and s['last']>=2020 and a<=s['latitude']<=b and c<=s['longitude']<=d and dist<=plan['radius_km']:
                eligible.append(dict(s,distance_km=dist))
        eligible.sort(key=lambda s:(s['distance_km'],s['id'])); chosen=[]
        for s in eligible:
            if any((s['wmo'] not in ('','99999') and s['wmo']==t['wmo']) or distance(s['latitude'],s['longitude'],[t['latitude'],t['longitude']])<1 for t in chosen): continue
            chosen.append(s)
            if len(chosen)==plan['stations_per_region']:break
        result.append(dict(region,stations=chosen,eligible_count=len(eligible),weight=1/len(chosen) if chosen else None))
    write(target,{'selected_utc':datetime.now(timezone.utc).isoformat(),'before_rain_values':not (EVIDENCE/'archive-receipt.json').exists(),
        'inventory_sha256':sha(CACHE/'inventory'),'plan_sha256':sha(TASK/'PLAN.json'),'regions':result})
    print(json.dumps(result,indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=[*FILES,'select']);a=p.parse_args()
    select() if a.action=='select' else acquire(a.action)
