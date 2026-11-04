from pathlib import Path
import json, hashlib, re
B=Path(__file__).resolve().parent
rows=json.loads((B/'IDENTITY_RECONCILIATION.json').read_text(encoding='utf-8'))
assert len(rows)==3 and len({r['candidate_id'] for r in rows})==3
assert sum(r['kind']=='multi_function_site_with_landfill' for r in rows)==1
for r in rows:
 assert r['science_admission']=='PENDING' and r['identity_status']=='PARTIAL'
 assert not r['current_status_verified'] and r['current_status']=='UNKNOWN'
 for f in ['latitude','longitude','crs','accuracy_m','official_site_id','permit_id','operator_id','current_methane_management']: assert r[f] is None
sources=json.loads((B/'SOURCES.json').read_text(encoding='utf-8'))
assert all(s['url'].startswith('https://www.rockhamptonregion.qld.gov.au/') for s in sources)
ids={s['source_id'] for s in sources}
assert all(set(r['current_evidence'])<=ids for r in rows)
assert rows[0]['monitoring_point']=='RP1' and rows[1]['monitoring_point'] is None
assert len(rows[2]['process_units'])==5 and rows[2]['methane_historical']['electricity_generation'] is None
q=json.loads((B/'evidence/browser_qa.json').read_text(encoding='utf-8'))
assert q['status']=='PASS' and not q['errors'] and not q['external_requests']
t=(B/'index.html').read_text(encoding='utf-8')
assert len(re.findall(r'<section class="page"',t))==10
for link in re.findall(r'href="([^"]+)"',t):
 if not link.startswith(('https:','#')): assert (B/link).exists(),link
state=json.loads((B/'EXECUTION_STATE.json').read_text(encoding='utf-8'))
assert state['p1a_scientific_admission']=='PENDING' and not state['numerical_experiments_run']
assert state['national_facility_count'] is None and state['national_emissions'] is None
result={'status':'LOCAL_VERIFIED_STRUCTURAL_AND_UI_ONLY','identity':'PARTIAL','science':'PENDING','candidates':3,'new_landfill_containing_candidates':1,'browser_combinations':20,'source_http_body_hashes':False,'note':'No source correctness or current operating status certified by these checks.'}
(B/'evidence/validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
(B/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(B).as_posix()+'\n' for p in sorted(B.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.txt' and p.suffix!='.png' and '__pycache__' not in p.parts),encoding='utf-8',newline='\n')
print(json.dumps(result))
