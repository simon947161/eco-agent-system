from pathlib import Path
import json,re,hashlib,datetime
B=Path(__file__).resolve().parent
def read(p): return json.loads((B/p).read_text(encoding='utf-8'))
rows=read('CLIMATE_EVENT_REGISTER.json'); sources=read('SOURCES.json'); ids={s['source_id'] for s in sources}
assert len(rows)==6 and len({r['event_id'] for r in rows})==6
assert {r['region'] for r in rows}=={'Cooma','Rockhampton'}
for r in rows:
 assert r['source_id'] in ids and r['record_type']=='OBSERVATION_SUMMARY' and not r['forecast']
 assert datetime.date.fromisoformat(r['window_start_label'])<=datetime.date.fromisoformat(r['window_end_label'])
 assert r['facility_gas_effect'] is None and r['utc_start'] is None and r['utc_end'] is None
 assert r['unit'] in ('degC','mm') and r['station_id'] in ('070217','039083')
 assert r['station_qc_flags'] is None and r['completeness_fraction'] is None
assert rows[-1]['metric']=='monthly rainfall total' and 'NOT Debbie' in rows[-1]['window_basis']
f=read('FACILITY_FOLLOWUP.json'); prior=json.loads((B.parent/'batch-b3/IDENTITY_RECONCILIATION.json').read_text(encoding='utf-8'))
assert f['preserved_ids']==[r['candidate_id'] for r in prior]
c=f['new_candidate']; assert c['instrument_version']=='2017-03-15' and c['instrument_id_historical']=='6194'
assert c['current_permit_validity']=='UNKNOWN' and c['latitude'] is None and c['methane_measurements'] is None
state=read('EXECUTION_STATE.json');assert state['science_admission']=='PENDING' and not state['numerical_experiments'] and not state['emissions_calculated']
q=read('evidence/browser_qa.json');assert q['status']=='PASS' and not q['external_requests'] and not q['errors']
t=(B/'index.html').read_text(encoding='utf-8');assert len(re.findall('<section class="page"',t))==10
for link in re.findall(r'href="([^"]+)"',t):
 if not link.startswith(('https:','#')): assert (B/link).exists(),link
result={'status':'LOCAL_VERIFIED_STRUCTURAL_AND_UI_ONLY','climate_records':6,'preserved_facilities':3,'new_partial_candidate':1,'browser_page_viewport_checks':20,'science':'PENDING','raw_source_body_hashes':False,'limitations':'Validation does not independently certify BOM QC, current licence validity or scientific effects.'}
(B/'evidence/validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
(B/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(B).as_posix()+'\n' for p in sorted(B.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.txt' and p.suffix!='.png' and '__pycache__' not in p.parts),encoding='utf-8',newline='\n')
print(json.dumps(result))
