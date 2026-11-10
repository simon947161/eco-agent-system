"""Small offline source admission and ENSO evidence calculation, no forecasting.

Reuses PR147 statistics/Atlas, PR148 QC and EcoEngine evidence. No networking
in this module. Acquisition is a separately invoked, bounded research script.
"""
from __future__ import annotations
import csv, hashlib, io, json, math, random, statistics
from collections import Counter
from pathlib import Path
from . import enso_regional_weather as previous
from . import physical_process_trajectory as trajectory
from ..engine.evidence_layer import meteorology_evidence_record
from ..engine.scenario_comparison import _record as scenario_record
from ..engine.evidence_traceability import _record as trace_record

ROOT=Path(__file__).resolve().parents[2]
TASK=ROOT/'docs/tasks/climateos_multisource_data_admission_001'
VERSION='multisource/1'
SOURCE='GHCNM_V4_PRCP_20261105_WAGGA'
SUPPORT='NSW_WAGGA_PANEL_PR148_THREE_STATIONS'
INDEX='RONI_ERSSTv6_1991-2020_PR147'
STATIONS=('ASN00072150','ASN00074104','ASN00072008')
PHASES=('warm','cold','neutral')
MODES=(('JJA','JJA'),('SON','SON'),('JJA','SON'))
read=previous.read
require=previous.require
canonical=previous.canonical
def sha(raw):return hashlib.sha256(raw).hexdigest()
def source_gate(source):
    """Provider country does not determine coverage; spatial support does."""
    if source.get('http_status')==404:return 'NOT_FOUND_404'
    if source.get('http_status') in (401,403,499):return 'ACCESS_RESTRICTED'
    if source.get('auth_required'):return 'AUTH_REQUIRED'
    if not source.get('research_use_permitted'):return 'LICENCE_UNCLEAR'
    if 'Australia' not in source.get('geographic_coverage',[]):return 'TIME_SUPPORT_MISMATCH'
    if source.get('baseline_years_available',0)<24:return 'TIME_SUPPORT_MISMATCH'
    if not source.get('payload_available'):return 'PAYLOAD_INVALID'
    return 'CANDIDATE_FOR_QC'
def fallback(sources):
    """Decision trace only. Never retries, obtains credentials or claims a GET."""
    trace=[]
    for s in sources:
        status=source_gate(s);trace.append({'source_id':s['source_id'],'decision':status,'network_executed':False})
        if status=='CANDIDATE_FOR_QC':return {'candidate':s['source_id'],'trace':trace}
    return {'candidate':None,'trace':trace}
def contract(r):
    expected={'source_id':SOURCE,'method_version':VERSION,'data_support':SUPPORT,
              'index_version':INDEX,'time_basis':'calendar_month_not_UTC_instant',
              'unit':'tenth_mm','data_kind':'observational_monthly_compilation',
              'authorship':'OFFICIAL_SOURCE_BYTES','claim':'DESCRIPTIVE_CONDITIONAL_ASSOCIATION',
              'authority':'BOUNDED_RESEARCH_ONLY','missing_policy':'EXCLUDE_NO_ZERO'}
    require(r==expected,'SOURCE_OR_SCIENCE_CONTRACT')
    return r
def request():
    return {'source_id':SOURCE,'method_version':VERSION,'data_support':SUPPORT,'index_version':INDEX,
            'time_basis':'calendar_month_not_UTC_instant','unit':'tenth_mm','data_kind':'observational_monthly_compilation',
            'authorship':'OFFICIAL_SOURCE_BYTES','claim':'DESCRIPTIVE_CONDITIONAL_ASSOCIATION',
            'authority':'BOUNDED_RESEARCH_ONLY','missing_policy':'EXCLUDE_NO_ZERO'}
def parse_station(raw,station):
    require(station in STATIONS,'STATION_ID')
    rows={}; flags=Counter(); pos=set(); rejected=[]; all_months=[]
    for line_number,row in enumerate(csv.reader(io.StringIO(raw.decode('ascii')),skipinitialspace=True),1):
        require(len(row)==11,'CSV_SCHEMA')
        row=[v.strip() for v in row]
        require(row[0]==station and row[0].startswith('AS'),'FIPS_AS_NOT_ISO_AU')
        require(len(row[5])==6 and row[5].isdigit(),'MONTH_FORMAT')
        y,m=int(row[5][:4]),int(row[5][4:]);require(1<=m<=12,'MONTH_RANGE')
        require((y,m) not in rows,'DUPLICATE_STATION_MONTH')
        lat,lon,elev=map(float,row[2:5]); require(all(math.isfinite(v) for v in (lat,lon,elev)),'COORDINATES')
        # Frozen Wagga region. Point positions are compiled metadata, not proof
        # of no historical relocation; source may repeat latest coordinates.
        require(-36<=lat<=-34 and 146<=lon<=149,'AUSTRALIAN_REGION_SUPPORT')
        a,b=map(math.radians,(lat,-35.12)); dl=math.radians(lon-147.37)
        dist=12742*math.asin(min(1,math.sqrt(math.sin((a-b)/2)**2+math.cos(a)*math.cos(b)*math.sin(dl/2)**2)))
        require(dist<=75,'REGION_RADIUS')
        value=float(row[6]);require(value.is_integer(),'TENTH_MM_INTEGER')
        q=previous.monthly_qc(value,row[7],row[8],row[9])
        rows[y,m]={'station':station,'year':y,'month':m,'rain_mm':q['mm'],'raw_tenth_mm':int(value),
                   'M':row[7],'Q':row[8],'S':row[9],'source_index':row[10],
                   'quality':q,'source_line':line_number,'latitude':lat,'longitude':lon}
        all_months.append(y*100+m)
        if 1961<=y<=2020:
            flags['M:'+row[7]]+=1;flags['Q:'+row[8]]+=1;flags['S:'+row[9]]+=1;pos.add((lat,lon,elev))
            if not q['eligible']:rejected.append({'year':y,'month':m,'reasons':q['reasons']})
    window=[(y,m) for y in range(1961,2021) for m in range(1,13)]
    missing=[{'year':y,'month':m} for y,m in window if (y,m) not in rows]
    valid=sum(rows.get(k,{}).get('rain_mm') is not None for k in window)
    return rows,{'station':station,'raw_rows':len(rows),'coverage':[min(all_months),max(all_months)],
        'window_expected_months':720,'present_months':720-len(missing),'valid_months':valid,
        'missing_months':missing,'rejected_months':rejected,'flags':dict(sorted(flags.items())),
        'reported_positions':sorted(pos),'historical_relocation':'UNKNOWN_latest_metadata_may_be_repeated',
        'daily_completeness':'UNKNOWN_for_blank_M','calibration':'UNKNOWN_no_instrument_record'}
def panel(station_rows):
    require(set(station_rows)==set(STATIONS),'FIXED_THREE_STATION_SUPPORT')
    monthly=[]
    for y in range(1961,2021):
        for m in range(1,13):
            values=[station_rows[s].get((y,m),{}).get('rain_mm') for s in STATIONS]
            monthly.append({'year':y,'month':m,'rain_mm':previous.fixed_panel(values,3),
                            'missing_or_rejected_stations':[s for s,v in zip(STATIONS,values) if v is None]})
    seasons={}
    by_month={(r['year'],r['month']):r['rain_mm'] for r in monthly}
    for s,months in (('JJA',(6,7,8)),('SON',(9,10,11))):
        seasons[s]=[{'year':y,'season':s,'rain_mm':previous.seasonal_total({m:by_month[y,m] for m in months},s)} for y in range(1961,2021)]
    return monthly,seasons
def quality_gate(rows):
    baseline=[r for r in rows if r['year']<=1990 and r['rain_mm'] is not None]
    valid=[r for r in rows if r['rain_mm'] is not None]
    return {'status':'DATA_ADMITTED' if len(baseline)>=24 and len(valid)>=40 else 'QC_INSUFFICIENT',
            'valid_baseline_seasons':len(baseline),'valid_analysis_seasons':len(valid),
            'missing_years':[r['year'] for r in rows if r['rain_mm'] is None]}
def event_number(value,threshold,event):
    return int(value<threshold) if event in ('dry','extreme_dry') else int(value>threshold)
def summary(rows,threshold,event):
    valid=[r for r in rows if r['rain_mm'] is not None];result={}
    total=sum(event_number(r['rain_mm'],threshold,event) for r in valid)
    for p in PHASES:
        group=[r for r in valid if r['phase']==p];others=[r for r in valid if r['phase']!=p]
        k=sum(event_number(r['rain_mm'],threshold,event) for r in group);n=len(group)
        other=sum(event_number(r['rain_mm'],threshold,event) for r in others)
        prob=k/n if n else None;op=other/len(others) if others else None;bp=total/len(valid) if valid else None
        result[p]={'k':k,'n':n,'p':prob,'wilson95':trajectory.wilson(k,n) if n else None,
                   'other_k':other,'other_n':len(others),'difference_nonphase':prob-op if n and others else None,
                   'baseline_k':total,'baseline_n':len(valid),'difference_unconditional':prob-bp if n else None,
                   'sample_warning':'LOW_N' if n<5 else 'DEPENDENT_SMALL_HISTORICAL_SAMPLE'}
    w,c=result['warm']['p'],result['cold']['p']
    return {'event':event,'threshold_mm':threshold,'phase':result,'warm_minus_cold':w-c if w is not None and c is not None else None}
def block_samples(n,length,repeats=2000):
    rng=random.Random(147148);out=[]
    for _ in range(repeats):
        idx=[]
        while len(idx)<n:
            start=rng.randrange(n);idx.extend((start+j)%n for j in range(length))
        out.append(idx[:n])
    return out
def interval(values,repeats):
    return {'valid_replicates':len(values),'replicates':repeats,
            'percentile95':[trajectory.quantile(values,.025),trajectory.quantile(values,.975)] if values else None,
            'status':'NOMINAL_BLOCK_INTERVAL' if len(values)>=.9*repeats else 'UNSTABLE_SUPPORT',
            'degenerate':bool(values) and min(values)==max(values)}
def bootstrap(rows,threshold,event,length,reestimate=False,repeats=2000):
    buffers={p:{'p':[],'difference_nonphase':[],'difference_unconditional':[]} for p in PHASES};diff=[]
    for idx in block_samples(len(rows),length,repeats):
        sample=[rows[i] for i in idx];t=threshold
        if reestimate:
            base=[r['rain_mm'] for r in sample if r['year']<=1990 and r['rain_mm'] is not None]
            if len(base)<15:continue
            t=statistics.median(base)
        res=summary(sample,t,event)
        for p in PHASES:
            for k in buffers[p]:
                v=res['phase'][p][k]
                if v is not None:buffers[p][k].append(v)
        if res['warm_minus_cold'] is not None:diff.append(res['warm_minus_cold'])
    return {'block_years':length,'circular':True,'threshold_reestimated':reestimate,
            'phase':{p:{k:interval(v,repeats) for k,v in vals.items()} for p,vals in buffers.items()},
            'warm_minus_cold':interval(diff,repeats)}
def holdout(rows):
    train=[r for r in rows if r['year']<=1990 and r['rain_mm'] is not None]
    test=[r for r in rows if r['year']>=1991 and r['rain_mm'] is not None]
    require(len(train)>=24,'TRAINING_BASELINE_TOO_SHORT')
    threshold=statistics.median(r['rain_mm'] for r in train);out={}
    for event in ('dry','wet'):
        base=(sum(event_number(r['rain_mm'],threshold,event) for r in train)+.5)/(len(train)+1)
        phase_prob={};training_n={}
        for p in PHASES:
            g=[r for r in train if r['phase']==p];training_n[p]=len(g)
            phase_prob[p]=(sum(event_number(r['rain_mm'],threshold,event) for r in g)+.5)/(len(g)+1) if g else None
        predictions=[]
        for r in test:
            p=phase_prob[r['phase']]
            if p is not None:predictions.append({'year':r['year'],'phase':r['phase'],'event':event_number(r['rain_mm'],threshold,event),'p':p,'baseline_p':base})
        bs=statistics.mean((r['p']-r['event'])**2 for r in predictions) if predictions else None
        b0=statistics.mean((r['baseline_p']-r['event'])**2 for r in predictions) if predictions else None
        out[event]={'training_n':training_n,'training_probability':phase_prob,'training_unconditional':base,
                    'test_n':len(predictions),'brier_phase':bs,'brier_baseline':b0,'difference':bs-b0 if bs is not None else None,'predictions':predictions}
    return {'train':[1961,1990],'test':[1991,2020],'threshold_mm':threshold,'events':out,
            'interpretation':'RETROSPECTIVE_HOLDOUT_NOT_REALTIME_HINDCAST; no tuning; small sample, no skill certification'}
def analyse(seasons,roni,*,repeats=2000):
    require(set(seasons)=={'JJA','SON'},'SEASON_SUPPORT')
    for season, records in seasons.items():
        require([r['year'] for r in records]==list(range(1961,2021)),'ANNUAL_ALIGNMENT')
        require(all(r['season']==season for r in records),'SEASON_ALIGNMENT')
        require(all(r['rain_mm'] is None or (math.isfinite(r['rain_mm']) and r['rain_mm']>=0) for r in records),'RAIN_VALUE')
        require(all((y,season) in roni and math.isfinite(roni[y,season]) for y in range(1961,2021)),'RONI_ALIGNMENT')
    paired=[];results=[];counter=[]
    for predictor,response in MODES:
        rain=seasons[response];gate=quality_gate(rain)
        rows=[dict(r,phase=trajectory.phase(roni[r['year'],predictor]),roni=roni[r['year'],predictor],
                   predictor_season=predictor,response_season=response,source_id=SOURCE,data_support=SUPPORT) for r in rain]
        mode=predictor+'_'+response
        if gate['status']!='DATA_ADMITTED':results.append({'mode':mode,'gate':gate,'probabilities':None});continue
        base=[r['rain_mm'] for r in rows if r['year']<=1990 and r['rain_mm'] is not None]
        med=statistics.median(base);lo=trajectory.quantile(base,.2);hi=trajectory.quantile(base,.8)
        for r in rows:
            r.update(mode=mode,event=previous.event(r['rain_mm'],med),threshold_mm=med,
                     extreme_dry=None if r['rain_mm'] is None else r['rain_mm']<lo,
                     extreme_wet=None if r['rain_mm'] is None else r['rain_mm']>hi)
            paired.append(r)
            if (r['phase'],r['event']) in (('warm','wet'),('cold','dry')):counter.append(r.copy())
        adjacent=[(a['rain_mm'],b['rain_mm']) for a,b in zip(rows,rows[1:]) if a['rain_mm'] is not None and b['rain_mm'] is not None]
        late=[r['rain_mm'] for r in rows if r['year']>=1991 and r['rain_mm'] is not None]
        event_results={}
        for ev in ('dry','wet'):
            event_results[ev]={'primary':summary(rows,med,ev),
                'blocks':[bootstrap(rows,med,ev,b,False,repeats) for b in (3,5)],
                'threshold_uncertainty_block3':bootstrap(rows,med,ev,3,True,repeats),
                'early':summary([r for r in rows if r['year']<=1990],med,ev),
                'late_fixed_threshold':summary([r for r in rows if r['year']>=1991],med,ev),
                'late_rebased_retrospective':summary([r for r in rows if r['year']>=1991],statistics.median(late),ev) if late else None}
        results.append({'mode':mode,'gate':gate,'events':event_results,'extreme_dry':summary(rows,lo,'extreme_dry'),
            'extreme_wet':summary(rows,hi,'extreme_wet'),'holdout':holdout(rows),
            'rain_lag1_correlation':trajectory.correlation([v[0] for v in adjacent],[v[1] for v in adjacent]) if len(adjacent)>1 else None,
            'adjacent_pairs_n':len(adjacent),'thresholds_mm':{'median_1961_1990':med,'p20':lo,'p80':hi},
            'missingness_by_phase':{p:{'total':sum(r['phase']==p for r in rows),'valid':sum(r['phase']==p and r['rain_mm'] is not None for r in rows)} for p in PHASES}})
    return paired,results,counter
def verify():
    manifest=read(TASK/'evidence/manifest.json')
    for rel,d in manifest['files'].items():
        p=(ROOT/rel).resolve();require(p.is_relative_to(ROOT) and p.is_file(),'MANIFEST_PATH')
        b=p.read_bytes();b=b if rel in manifest['byte_exact'] else b.replace(b'\r\n',b'\n')
        require(sha(b)==d,'HASH_MISMATCH:'+rel)
    return len(manifest['files'])
def intake():
    receipts=read(TASK/'DOWNLOAD_RECEIPTS.json');plan=sha((TASK/'PRE_ACCESS_PLAN.md').read_bytes())
    require(len(receipts)<=6 and len({r['product_id'] for r in receipts})<=3,'NETWORK_BUDGET')
    require(sum(r.get('bytes',0) for r in receipts)<=75_000_000,'BYTE_BUDGET')
    require(all(0<r.get('bytes',0)<=25_000_000 for r in receipts),'PER_FILE_BUDGET')
    selected={r['id']:r for r in receipts if r.get('status')=='DOWNLOADED_PENDING_ADMISSION'}
    require(set(selected)==set(STATIONS),'THREE_RAW_FILES_REQUIRED')
    sources=read(TASK/'SOURCE_REGISTRY.json');source=next(s for s in sources if s['source_id']==SOURCE)
    require(source_gate(source)=='CANDIDATE_FOR_QC','SOURCE_NOT_ADMISSIBLE')
    data={};qc=[]
    for station in STATIONS:
        receipt=selected[station];require(receipt['plan_sha256']==plan,'PREREGISTRATION_DRIFT')
        require(receipt['product_id']=='GHCNM_V4_PRCP' and receipt['http_status']==200,'RECEIPT_PRODUCT')
        require(source['raw_bytes_sha256'][station]==receipt['sha256'],'REGISTRY_HASH')
        path=(TASK/receipt['local_path']).resolve();require(path.is_relative_to(TASK/'evidence/raw'),'RAW_PATH')
        raw=path.read_bytes();require(sha(raw)==receipt['sha256'] and len(raw)==receipt['bytes'],'RAW_HASH_OR_BYTES')
        data[station],q=parse_station(raw,station);qc.append(q)
    monthly,seasons=panel(data)
    raw=(trajectory.TASK/'evidence/RONI.ascii.txt').read_bytes()
    require(sha(raw)==read(previous.TASK/'PLAN.json')['roni_sha256'],'RONI_HASH')
    return qc,monthly,seasons,trajectory.parse_roni(raw)
def evaluate(r,*,verify_hashes=True,repeats=2000):
    contract(r)
    if verify_hashes:verify()
    qc,monthly,seasons,roni=intake();paired,results,counter=analyse(seasons,roni,repeats=repeats)
    admitted=[v for v in results if v['gate']['status']=='DATA_ADMITTED']
    status='OPEN_DATA_RECALCULATED' if admitted else 'DATA_NOT_READY'
    # Reuse the existing comparator's pure record builder for a NEW named
    # Wagga evidence scenario. No mutation of its four production fixtures.
    last=next((v for v in reversed(seasons['SON']) if v['rain_mm'] is not None),None)
    eco=meteorology_evidence_record({'retrieval_status':'success' if admitted else 'unavailable','confidence':'low',
        'rainfall_mm':last['rain_mm'] if admitted else None,'source_id':SOURCE,'source_version':'2026-11-05',
        'temporal_support':'SON '+str(last['year']) if admitted else None,'data_support':SUPPORT,
        'statistical_result_id':'ENSO_REGION_WEATHER_MULTISOURCE','not_recent_weather':True})
    # The reused generic builder labels all rain as 'recent rainfall'. This
    # adapter must narrow that label to the actual historical temporal support.
    eco['indicators']=['historical seasonal rainfall','historical ENSO association'] if admitted else []
    traces=[trace_record('wagga_enso_research','historical_conditional_probability',SOURCE,
        'Historical ENSO rainfall association; no causal or future-weather claim',[SOURCE],
        'docs/tasks/climateos_multisource_data_admission_001/PAIRED_DATA.json',
        'observational_monthly_derived_statistics','low','uncertainty_requires_review','PENDING',[],
        ['fixed three-station support','CONFOUNDER_NOT_CONTROLLED','not statutory or forecast validation'])]
    cc=scenario_record('wagga_enso_research',{'name':'Wagga historical ENSO evidence','meteorology_ids':['wagga_enso_research']},
                       {'traceability':{'records':traces if admitted else []}})
    return {'process_id':'ENSO_REGION_WEATHER','method_version':VERSION,'source_id':SOURCE,'data_support':SUPPORT,
        'status':status,'station_qc':qc,'monthly':monthly,'paired_rows':paired,'results':results,'counterexamples':counter,
        'regions_not_acquired':['QLD_ROCKHAMPTON_PANEL','WA_PERTH_PANEL'],'hot':'NOT_ASSESSED',
        'confounders':'CONFOUNDER_NOT_CONTROLLED','scientific_admission':'PENDING','forecast_validation':'PENDING',
        'causal_identification':'NOT_ESTABLISHED','ecoengine':eco,'cczps':cc,'traceability':traces,
        'atlas_context':trajectory.trace('ENSO')['atlas_qualitative_path'],
        'ecochain':'PROPOSAL_ONLY_ECOCHAIN_CANONICAL_NOT_FOUND','enotebook':'PENDING_INTEGRATION',
        'deployed':False,'certified':False,'source_expansion_stopped':bool(admitted)}
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path);a=p.parse_args();v=evaluate(request())
    if a.out:a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(canonical(v),encoding='utf-8',newline='\n')
    else:print(canonical({'status':v['status'],'results':[{'mode':r['mode'],'gate':r['gate'],'dry':r.get('events',{}).get('dry',{}).get('primary')} for r in v['results']]}))
