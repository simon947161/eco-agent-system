"""Offline blocked-data handoff and bounded QC helpers, not a weather forecaster.

No rain payload was acquired in this run. No statistical engine is claimed as
executed or validated on observations. Reuses PR147/Atlas and EcoEngine gates.
"""
from __future__ import annotations
import hashlib
import json
import math
from pathlib import Path
from . import physical_process_trajectory as trajectory
from ..engine.evidence_layer import meteorology_evidence_record
from ..engine.scenario_comparison import build_scenario_comparison

ROOT = Path(__file__).resolve().parents[2]
TASK = ROOT/'docs/tasks/climateos_enso_regional_weather_probability_001'
VERSION = 'enso-regional-weather/1'
def read(path): return json.loads(path.read_text(encoding='utf-8-sig'))
def require(ok, reason):
    if not ok: raise ValueError(reason)
def canonical(obj):
    return json.dumps(obj,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+'\n'
def verify():
    manifest=read(TASK/'evidence/manifest.json')
    for rel,digest in manifest['files'].items():
        p=(ROOT/rel).resolve()
        require(p.is_relative_to(ROOT) and p.is_file(),'MANIFEST_PATH')
        raw=p.read_bytes().replace(b'\r\n',b'\n')
        require(hashlib.sha256(raw).hexdigest()==digest,'HASH_MISMATCH:'+rel)
    return len(manifest['files'])
def inventory_row(line):
    require(len(line)>=95,'INVENTORY_LENGTH')
    require(line[:2]=='AS','COUNTRY_FIPS_NOT_ISO')
    lat,lon=float(line[12:20]),float(line[21:30])
    require(math.isfinite(lat) and math.isfinite(lon) and -90<=lat<=90 and -180<=lon<=180,'COORDINATES')
    return {'id':line[:11],'latitude':lat,'longitude':lon,'first':int(line[86:90]),'last':int(line[91:95])}
def monthly_qc(value,measurement='',quality='',source='D',unit='tenth_mm'):
    """Fixture-tested only: do not silently interpret blank M as daily completeness."""
    require(unit=='tenth_mm','RAIN_UNIT')
    require(type(value) in (int,float) and math.isfinite(value),'RAIN_VALUE')
    require(measurement in ('','A','B','C','D','E'),'UNKNOWN_MEASUREMENT_FLAG')
    require(quality in ('','D','K','L','O','R','S','T','W'),'UNKNOWN_QUALITY_FLAG')
    require(source in ('D','H','M','R','S','W','Z'),'UNKNOWN_SOURCE_FLAG')
    reasons=[]
    if quality: reasons.append('QC_'+quality)
    if measurement: reasons.append('MISSING_DAYS_'+measurement)
    if value==-1: reasons.append('TRACE_NO_DOCUMENTED_UPPER_BOUND')
    elif value<0: reasons.append('NEGATIVE_OR_MISSING_SENTINEL')
    return {'mm':None if reasons else value/10,'eligible':not reasons,'reasons':reasons,
            'daily_completeness':'UNKNOWN' if not measurement else 'INCOMPLETE','source':source}
def fixed_panel(values,expected_count):
    require(expected_count in (1,2,3) and len(values)==expected_count,'STATION_SUPPORT')
    if any(v is None for v in values): return None
    require(all(type(v) in (int,float) and math.isfinite(v) and v>=0 for v in values),'RAIN_VALUE')
    return sum(values)/expected_count
def seasonal_total(months,season):
    require(season in ('JJA','SON'),'SEASON')
    expected=(6,7,8) if season=='JJA' else (9,10,11)
    require(tuple(sorted(months))==expected,'MONTH_SEASON_MISMATCH')
    if any(v is None for v in months.values()): return None
    require(all(type(v) in (int,float) and math.isfinite(v) and v>=0 for v in months.values()),'RAIN_VALUE')
    return sum(months.values())
def event(value,median):
    if value is None: return None
    require(all(type(v) in (int,float) and math.isfinite(v) and v>=0 for v in (value,median)),'EVENT_VALUE')
    return 'dry' if value<median else 'wet' if value>median else 'neither'
def request():
    return {'version':VERSION,'process':'ENSO_REGION_WEATHER','index_version':'RONI_ERSSTv6_1991-2020_PR147',
            'mode':['JJA','SON'],'unit':'mm','spatial_support':'fixed_equal_weight_station_panel',
            'temporal_support':'calendar_month_not_UTC_instant','missing_policy':'EXCLUDE_NO_ZERO_IMPUTATION',
            'claim':'HISTORICAL_CONDITIONAL_ASSOCIATION','authority':'BOUNDED_RESEARCH_ONLY'}
def validate_request(r):
    require(set(r)==set(request()),'REQUEST_FIELDS')
    for key,expected in request().items():
        if key!='mode': require(r[key]==expected,'REQUEST_'+key.upper())
    require(r['mode'] in [['JJA','JJA'],['SON','SON'],['JJA','SON']],'WRONG_SEASON_OR_LAG')
def evaluate(r, *, verify_hashes=True):
    validate_request(r)
    if verify_hashes: verify()
    plan=read(TASK/'PLAN.json'); selection=read(TASK/'REGIONS.json')
    digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    require(digest(trajectory.TASK/'evidence/RONI.ascii.txt')==plan['roni_sha256'],'RONI_RAW_HASH')
    inventory=read(TASK/'evidence/inventory-receipt.json'); rain=read(TASK/'evidence/archive-receipt.json')
    require(all(x['plan_sha256']==digest(TASK/'PLAN.json') and x['preregistration_sha256']==digest(TASK/'PRE_REGISTERED_ANALYSIS_PLAN.md') for x in (inventory,rain)),'PREREGISTRATION_DRIFT')
    require(selection['before_rain_values'] and selection['selected_utc']<rain['started_utc'],'POST_OUTCOME_SELECTION')
    require(selection['inventory_sha256']==inventory['sha256'],'INVENTORY_SOURCE_HASH')
    require(inventory['status']=='DOWNLOADED' and rain['status']=='BLOCKED_NO_RETRY','FROZEN_ACQUISITION_STATE')
    require(rain['bytes_received']==0,'UNEXPECTED_RAIN_PAYLOAD')
    paired=read(TASK/'PAIRED_ENSO_WEATHER_DATA.json')
    require(paired['rows']==[] and paired['status']=='DATA_NOT_READY','FABRICATED_WEATHER_PAIRS')
    ids=[]
    for region in selection['regions']:
        for s in region['stations']:
            parsed=inventory_row(s['inventory_line']); require(parsed['id']==s['id'],'STATION_ID')
            ids.append(s['id'])
    require(len(ids)==len(set(ids))==9,'DUPLICATE_STATION')
    old=trajectory.trace('ENSO')
    eco=meteorology_evidence_record({'retrieval_status':'unavailable','rainfall_mm':None,'confidence':'low',
                                   'source':'NOAA GHCN-M v4 archive attempt','status':'DATA_NOT_READY'})
    comparison=build_scenario_comparison({'traceability':{'records':[]}})
    return {'PROCESS_ID':'ENSO_REGION_WEATHER','version':VERSION,'status':'DATA_NOT_READY',
      'paired_years':0,'numerical_output':None,'probabilities':[], 'hot':'NOT_ASSESSED',
      'inventory_candidates':ids,'selected_stations_are_not_rain_observations':True,
      'blocker':{'source':rain['url'],'error':rain['error'],'weather_attempted_files':2,
                 'budget_interpretation':'conservatively includes station inventory; no more downloads'},
      'statistics_execution':'NOT_EXECUTED_MISSING_RAIN','confounder_analysis':'NOT_EXECUTED_NO_PAIRED_RESPONSE',
      'atlas_trace_context':{'path':old['atlas_qualitative_path'],'evidence_ids':old['atlas_evidence_ids'],
                             'does_not_supply_rain_probability':True},
      'ecoengine_evidence':eco,
      'cczps_comparison_adapter_check':{'existing_scenarios_not_the_selected_regions':True,
        'record_count':comparison['record_count'],'summary':comparison['cross_scenario_summary'],
        'statuses':{x['scenario_id']:x['comparison_status'] for x in comparison['records']}},
      'ecochain':'PROPOSAL_ONLY_ECOCHAIN_CANONICAL_NOT_FOUND','enotebook':'PENDING_INTEGRATION',
      'scientific_admission':'PENDING','causal_validation':'PENDING','forecast_validation':'PENDING',
      'deployed':False,'certified':False,'next_missing_input':'Founder-reviewed new acquisition scope for a current legal PRCP archive or offline lawful file; preserve registered regions and thresholds'}
if __name__=='__main__': print(canonical(evaluate(request())))
