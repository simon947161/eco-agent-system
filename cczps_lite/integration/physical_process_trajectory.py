"""Thin offline research projection on the frozen Atlas, NOT a climate solver.

Only frozen examples may enter evaluate(); helper equations are bounded research
functions. No networking, external tools, certification or global influence score.
"""
from __future__ import annotations
import argparse
from collections import Counter
from datetime import date, timedelta
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import random
import statistics
from . import global_natural_systems_atlas as atlas
from . import methane_knowledge_engine as methane

ROOT=Path(__file__).resolve().parents[2]
TASK=ROOT/'docs/tasks/climateos_physical_process_trajectory_001'
VERSION='physical-trajectory/1'
STATUSES={'EXACT_PHYSICS_CALCULABLE','OPEN_DATA_RECALCULATED','SYNTHETIC_TESTED',
          'CONDITIONAL_STATISTICAL_ESTIMATE','STRUCTURAL_QC_ONLY','BLOCKED_MISSING_DATA',
          'BLOCKED_MODEL_VALIDATION','NOT_INFERABLE'}
FIELDS={'PROCESS_ID','NODE_ID','EDGE_ID','physical_quantity','unit','medium/phase','spatial_domain',
        'temporal_support','mechanism','equation_id','assumptions','boundary','inputs','observed_or_derived',
        'source_version_locator','data_rights','uncertainty','calibration','counterevidence','model_validation',
        'numerical_output','residual','status','next_missing_input','edge_type','from_node'}
EDGES={'CONSERVATION_LAW','PHYSICAL_MECHANISM','EMPIRICAL_RELATION','STATISTICAL_TELECONNECTION',
       'MODEL_ASSUMPTION','HYPOTHESIS','GOVERNANCE_CONTEXT'}

def read(path): return json.loads(path.read_text(encoding='utf-8-sig'))
def require(ok, reason):
    if not ok: raise ValueError(reason)

def verify():
    manifest=read(TASK/'evidence/manifest.json')
    for rel, expected in manifest['files'].items():
        p=(ROOT/rel).resolve()
        require(p.is_relative_to(ROOT) and p.is_file(),'MANIFEST_PATH')
        raw=p.read_bytes()
        if rel not in manifest['byte_exact']: raw=raw.replace(b'\r\n',b'\n')
        require(hashlib.sha256(raw).hexdigest()==expected, 'HASH_MISMATCH:'+rel)
    return len(manifest['files'])

def load(verify_hashes=True):
    if verify_hashes: verify()
    data=read(TASK/'TRAJECTORIES.json'); sources=read(TASK/'SOURCES.json')
    ids={s['id']:s for s in sources}
    require(len(ids)==len(sources),'DUPLICATE_SOURCE')
    require(len({s['theme'] for s in sources if s['theme']!='INHERITED'})<=12,'SOURCE_BUDGET')
    seen=set()
    for r in data:
        require(set(r)==FIELDS,'SEGMENT_SCHEMA')
        require(r['NODE_ID'] not in seen,'DUPLICATE_NODE'); seen.add(r['NODE_ID'])
        require(r['status'] in STATUSES and r['edge_type'] in EDGES,'SEGMENT_STATE')
        require(r['PROCESS_ID'] in ('CH4','ENSO','HYDRO'),'PROCESS_BUDGET')
        require(bool(r['counterevidence']) and bool(r['assumptions']),'EVIDENCE_CONTEXT')
        for source in r['source_version_locator']:
            require(source['id'] in ids and source['version']==ids[source['id']]['version'],'SOURCE_VERSION')
            require(bool(source['locator']),'LOCATOR')
        require(bool(r['source_version_locator']),'MISSING_SOURCE')
        if r['status'].startswith('BLOCKED') or r['status']=='NOT_INFERABLE':
            require(r['numerical_output'] is None and bool(r['next_missing_input']),'FALSE_NUMERIC_COMPLETION')
    require(all(r['from_node'] is None or r['from_node'] in seen for r in data),'BROKEN_EDGE')
    return data

def query(process):
    require(process in ('CH4','ENSO','HYDRO'),'UNKNOWN_PROCESS')
    return [r for r in load() if r['PROCESS_ID']==process]

def trace(process):
    paths={'CH4':'methane','ENSO':'enso','HYDRO':'nile_flow'}
    require(process in paths,'UNKNOWN_PROCESS')
    data=atlas.load_atlas(); edges=data['graph']['paths'][paths[process]]
    by_id={e['id']:e for e in data['graph']['edges']}
    old_path=atlas.trace(data,by_id[edges[0]]['from_id'],by_id[edges[-1]]['to_id'])
    old_query=atlas.query(data,process=paths[process])
    # Existing Atlas topology is context, not a calculation dependency claim.
    return {'atlas_qualitative_path':old_path,'atlas_evidence_ids':[e['claim_id'] for e in old_query['evidence']],
            'trajectory':query(process),
            'scientific_admission':'PENDING','whole_chain_calculable':False}

def ch4_erf(M,N, *, unit='ppb_dry_global_mean', phase='gas_dry_air_mole_fraction'):
    require(unit=='ppb_dry_global_mean','UNIT_GLOBAL_BASIS')
    require(phase=='gas_dry_air_mole_fraction','PHASE')
    require(all(type(v) in (int,float) and math.isfinite(v) for v in (M,N)), 'NONFINITE')
    # This projection is bounded to the published baseline/current neighbourhood,
    # not claimed as the entire domain of the underlying radiative-transfer fit.
    require(729.2<=M<=2000 and 270<=N<=350,'FORMULA_DOMAIN')
    f=read(TASK/'evidence/aggi-facts.json')
    s,t,s0=math.sqrt(M),math.sqrt(N),math.sqrt(f['M0_ppb'])
    k=f['a']*s+f['b']*t+f['d']
    return {'ERF_W_m2':f['e']*k*(s-s0),
            'dF_dM':f['e']*(f['a']*(s-s0)+k)/(2*s),
            'dF_dN':f['e']*f['b']*(s-s0)/(2*t)}

def radiation():
    f=read(TASK/'evidence/aggi-facts.json'); out=ch4_erf(f['M_ppb'],f['N_ppb'])
    uM=out['dF_dM']*f['M_reported_uncertainty_ppb']; uN=out['dF_dN']*f['N_reported_uncertainty_ppb']
    out.update(reported_2025_ERF_W_m2=f['published_2025_ERF_W_m2'],
        rounding_residual_W_m2=out['ERF_W_m2']-f['published_2025_ERF_W_m2'],
        rounded_match=round(out['ERF_W_m2'],3)==f['published_2025_ERF_W_m2'],
        propagated_abundance_u_if_independent_W_m2=math.hypot(uM,uN),
        covariance_extreme_u_range_W_m2=[abs(abs(uM)-abs(uN)),abs(uM)+abs(uN)],
        uncertainty_interpretation=f['uncertainty_definition'],
        formula_10_percent_scale_W_m2=abs(out['ERF_W_m2'])*.10,
        model_scale_not_CI=True,temperature_K=None,status='OPEN_DATA_RECALCULATED',
        scope='NOAA 2025 global methane ERF relative to 1750; not emissions attribution, indirect ozone forcing or surface temperature')
    return out

def energy_residual(power_in, power_out, seconds, stored_change, *, units=('W','s','J')):
    """Synthetic first-law dimensional check only; supplies no temperature law."""
    require(units==('W','s','J'),'ENERGY_UNITS')
    require(all(type(v) in (int,float) and math.isfinite(v) for v in (power_in,power_out,seconds,stored_change)) and seconds>0,'ENERGY_INPUT')
    return (power_in-power_out)*seconds-stored_change

def phase(x): return 'warm' if x>=.5 else ('cold' if x<=-.5 else 'neutral')

def parse_roni(raw):
    lines=raw.decode('ascii').splitlines(); require(lines[0].split()==['SEAS','YR','ANOM'],'HEADER')
    rows={}; seasons={'DJF','JFM','FMA','MAM','AMJ','MJJ','JJA','JAS','ASO','SON','OND','NDJ'}
    for line in lines[1:]:
        if not line.strip(): continue
        s,y,v=line.split(); y=int(y); v=float(v)
        require(s in seasons and math.isfinite(v) and abs(v)<10,'INDEX_QC')
        require((y,s) not in rows,'DUPLICATE_TIME'); rows[y,s]=v
    require(all((y,s) in rows for y in range(1961,2021) for s in seasons),'MISSING_ANALYSIS_SEASON')
    return rows

def wilson(k,n):
    require(0<=k<=n and n>0,'BINOMIAL_SUPPORT')
    z=1.959963984540054; p=k/n; den=1+z*z/n
    center=(p+z*z/(2*n))/den; half=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return [center-half,center+half]

def correlation(x,y):
    mx,my=statistics.mean(x),statistics.mean(y)
    vx=sum((a-mx)**2 for a in x); vy=sum((b-my)**2 for b in y)
    return sum((a-mx)*(b-my) for a,b in zip(x,y))/math.sqrt(vx*vy) if vx*vy else None

def quantile(values,p):
    vals=sorted(values); pos=(len(vals)-1)*p; lo=int(pos); hi=min(lo+1,len(vals)-1)
    return vals[lo]+(vals[hi]-vals[lo])*(pos-lo)

def paired_stat(pairs,target):
    group=[b==target for a,b in pairs if a==target]; other=[b==target for a,b in pairs if a!=target]
    if not group or not other: return None
    return sum(group)/len(group),sum(group)/len(group)-sum(other)/len(other)

def block_intervals(pairs,target,length):
    rng=random.Random(131146); values=[]; differences=[]; n=len(pairs)
    for _ in range(2000):
        sample=[]
        while len(sample)<n:
            start=rng.randrange(n-length+1); sample.extend(pairs[start:start+length])
        ans=paired_stat(sample[:n],target)
        if ans is not None: values.append(ans[0]); differences.append(ans[1])
    require(len(values)>1900,'BOOTSTRAP_SUPPORT')
    return {'block_years':length,'valid':len(values),'replicates':2000,
            'p_interval':[quantile(values,.025),quantile(values,.975)],
            'difference_interval':[quantile(differences,.025),quantile(differences,.975)]}

def enso():
    raw=(TASK/'evidence/RONI.ascii.txt').read_bytes(); meta=read(TASK/'evidence/roni-metadata.json')
    require(hashlib.sha256(raw).hexdigest()==meta['sha256'],'INDEX_VERSION_HASH')
    rows=parse_roni(raw); years=list(range(1961,2021))
    strata={}
    for season in ('DJF','MAM','JJA','SON'):
        vals=[rows[y,season] for y in years]
        strata[season]={'n':len(vals),'counts':dict(Counter(map(phase,vals))),
            'mean_degC':statistics.mean(vals),'lag1_annual_correlation':correlation(vals[:-1],vals[1:]),
            'early_1961_1990':{'mean':statistics.mean(vals[:30]),'counts':dict(Counter(map(phase,vals[:30])))},
            'late_1991_2020':{'mean':statistics.mean(vals[30:]),'counts':dict(Counter(map(phase,vals[30:])))}}
    pairs=[(phase(rows[y,'JJA']),phase(rows[y,'SON'])) for y in years]
    persistence={}
    for target in ('warm','cold'):
        eligible=[(y,a,b) for y,(a,b) in zip(years,pairs) if a==target]
        k=sum(b==target for _,_,b in eligible); n=len(eligible); prob,diff=paired_stat(pairs,target)
        persistence[target]={'k':k,'n':n,'p_SON_same_given_JJA':prob,
            'difference_vs_JJA_not_target':diff,'nominal_iid_Wilson95':wilson(k,n),
            'block_bootstrap':[block_intervals(pairs,target,b) for b in (3,5)],
            'years':[y for y,_,_ in eligible],'counterexample_years':[y for y,_,b in eligible if b!=target],
            'split':{label:{'n':sum(a==target for a,b in sub),'k':sum(a==target and b==target for a,b in sub)}
                     for label,sub in [('1961-1990',pairs[:30]),('1991-2020',pairs[30:])]}}
    return {'status':'CONDITIONAL_STATISTICAL_ESTIMATE','source_rows':len(rows),
        'selected_rows':720,'years':[1961,2020],'QC':'No missing or duplicate selected seasons; no per-row quality flag supplied',
        'season_strata':strata,'JJA_to_SON_persistence':persistence,
        'weather_probability':None,'weather_status':'DATA_NOT_READY',
        'interpretation':'Index persistence only; 3-month nonoverlapping seasons, not independent events, not a regional rainfall model or causal test. Moving blocks assume within-window approximate stationarity; split results are diagnostics, not proof of stationarity.',
        'classification':'single-season threshold, not the CPC five-consecutive-season event rule'}

def water_balance(nodes,values,sd):
    require(len(nodes) in (2,3,4),'NODE_BUDGET')
    total={}; out=[]
    for node in nodes:
        coefs=node['coefficients']
        require(node['interval']=='SYNTHETIC_UTC_DAY_86400S','TIME_SUPPORT')
        require(node['unit']=='m3/interval','WATER_UNIT')
        require(set(coefs)<=set(values) and set(coefs)<=set(sd),'MISSING_TERM')
        if any(values[k] is None or sd[k] is None for k in coefs):
            return {'status':'BLOCKED_MISSING_DATA','residual_m3':None,'attribution':None,'missing':[k for k in coefs if values[k] is None or sd[k] is None]}
        require(all(math.isfinite(values[k]) and math.isfinite(sd[k]) and sd[k]>=0 for k in coefs),'INVALID_WATER_VALUE')
        residual=math.fsum(coefs[k]*values[k] for k in coefs)
        u=math.sqrt(sum((coefs[k]*sd[k])**2 for k in coefs))
        out.append({'node':node['id'],'residual_m3':residual,'synthetic_u_m3':u})
        for k,c in coefs.items(): total[k]=total.get(k,0)+c
    return {'status':'SYNTHETIC_TESTED','nodes':out,'residual_m3':math.fsum(c*values[k] for k,c in total.items()),
        'whole_chain_u_m3':math.sqrt(sum((c*sd[k])**2 for k,c in total.items())),
        'incorrect_independent_node_u_m3':math.sqrt(sum(r['synthetic_u_m3']**2 for r in out)),
        'global_coefficients':total,'cancelled_internal_terms':[k for k,c in total.items() if c==0],
        'attribution':None,'uncertainty':'Authored independent primitive standard deviations; shared inter-node variables correlated exactly and cancelled; no field calibration'}

def water_fixture():
    values={'q0':10*86400,'q12':11*86400,'q23':12*86400,'q3':12*86400,
            'l1':2*86400,'l2':3*86400,'l3':1*86400,'a1':1*86400,'a2':2*86400,'a3':1*86400,
            'p1':1000,'p2':2000,'p3':500,'e1':500,'e2':1000,'e3':500,'s1':500,'s2':1000,'s3':0}
    sd={k:8640 if k[0] in 'qla' else 100 for k in values}
    nodes=[]
    for i,qi,qo in [(1,'q0','q12'),(2,'q12','q23'),(3,'q23','q3')]:
        nodes.append({'id':f'CV{i}','unit':'m3/interval','interval':'SYNTHETIC_UTC_DAY_86400S',
                      'coefficients':{qi:1,'l'+str(i):1,'p'+str(i):1,qo:-1,'a'+str(i):-1,'e'+str(i):-1,'s'+str(i):-1}})
    return nodes,values,sd

def hydro():
    nodes,values,sd=water_fixture(); synthetic=water_balance(nodes,values,sd)
    missing=values.copy(); missing['l2']=None
    fragment=read(TASK/'evidence/hrs-january-2020.json'); rows=fragment['rows']; dates=[r['date'] for r in rows]
    expected={(date(2020,1,1)+timedelta(days=i)).isoformat() for i in range(31)}
    return {'synthetic':synthetic,'synthetic_inputs':{'nodes':nodes,'volumes_m3':values,'std_m3':sd},
        'unknown_lateral_example':water_balance(nodes,missing,sd),
        'real_fragment':{'status':'STRUCTURAL_QC_ONLY','rows':len(rows),'duplicate_dates':len(dates)-len(set(dates)),
            'absent_dates':sorted(expected-set(dates)),'quality_counts':dict(Counter(r['quality'] for r in rows)),
            'missing_values':sum(r['value'] is None for r in rows),'physical_volume_sum':None,
            'balance_status':'BLOCKED_MISSING_DATA','scope':'Cooma HRS audit; not Nile',
            'gaps':['E quality unreliable','ML column versus ML/day header','09:00 local UTC/DST and interval convention','matched upstream/downstream, lateral and storage observations absent']}}

def scorecard():
    f=read(TASK/'evidence/scorecard-audit-facts.json')
    diagnostic=sum(x=='Yes' for x in f['responses'])*20
    return {'status':'STRUCTURAL_QC_ONLY','diagnostic_assumption':'Each Yes=20, each No=0; no partial credits',
        'diagnostic_score':diagnostic,'published_historical_label':f['published_label'],
        'difference':diagnostic-f['published_label'],'official_score_reproduced':False,
        'baseline_conflict':{'card_visible':2030,'act':f['law']['baseline_year']},
        'effect_of_baseline_correction_on_binary_Q2':'43 remains below 50; no demonstrated score change',
        'score_wrong_proven':False,'current_page_direct_access':'403_STOPPED','contact_status':'NOT_SENT'}

def legacy():
    request=read(TASK.parent/'climateos_methane_physics_knowledge_engine_001/input.json')
    spec=importlib.util.spec_from_file_location('trajectory_frozen_ledger',TASK.parent/'climateos_au_landfill_methane_methods_001/mass_balance.py')
    ledger=importlib.util.module_from_spec(spec); spec.loader.exec_module(ledger)
    return {'PR143':methane.execute(request),'PR144':{name:ledger.evaluate(ledger.fixture(name)) for name in ('uncaptured','capture_flare','oxidation_leaks')}}

def evaluate(request):
    require(set(request)=={'version','example','authority','scope'},'REQUEST_SCHEMA_NO_EXTRA_INPUTS')
    require(request['version']==VERSION,'VERSION')
    require(request['authority']=='BOUNDED_RESEARCH_ONLY','UNAUTHORIZED_CERTIFICATION')
    require(request['scope']=='FROZEN_EVIDENCE_NO_CAUSAL_EXTRAPOLATION','SCOPE_CAUSALITY')
    require(request['example'] in ('CH4','ENSO','HYDRO','CROSS','SCORECARD'),'UNKNOWN_EXAMPLE')
    verify(); load()
    key=request['example']
    if key=='CH4': result={'published_radiation':radiation(),'legacy_replay':legacy(),
                          'synthetic_energy_check':{'Pin_W':10,'Pout_W':8,'dt_s':60,'dU_J':120,
                              'residual_J':energy_residual(10,8,60,120),'temperature_K':None}}
    elif key=='ENSO': result=enso()
    elif key=='HYDRO': result=hydro()
    elif key=='CROSS': result=read(TASK/'CROSS_RELATIONS.json')
    else: result=scorecard()
    return {'example':key,'result':result,'scientific_admission':'PENDING','certification':False,'deployed':False}

def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('action',choices=['query','trace','evaluate']); p.add_argument('process')
    args=p.parse_args()
    if args.action=='query': out=query(args.process)
    elif args.action=='trace': out=trace(args.process)
    else: out=evaluate({'version':VERSION,'example':args.process,'authority':'BOUNDED_RESEARCH_ONLY','scope':'FROZEN_EVIDENCE_NO_CAUSAL_EXTRAPOLATION'})
    print(json.dumps(out,ensure_ascii=False,indent=2,allow_nan=False))

if __name__=='__main__': main()
