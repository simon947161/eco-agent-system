from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
r=json.loads((B/'IDENTITY_CANDIDATES.json').read_text(encoding='utf-8'))
assert 0<len(r)<=10
assert len({x['candidate_id'] for x in r})==len(r)
assert len({x['source_url'] for x in r})==len(r)
for x in r:
 assert x['latitude'] is None and x['longitude'] is None and x['accuracy_m'] is None
 assert x['operator_id'] is None and x['instrument_id'] is None
 assert x['process_description']=='Sewage Treatment'
 assert x['science_admission']=='PENDING' and not x['current_status_verified']
assert r[0]['approval_holder']==r[1]['approval_holder'] and r[0]['physical_site_name']!=r[1]['physical_site_name']
assert r[0]['monitoring_point_id']=='RP1' and r[1]['monitoring_point_id'] is None
q=json.loads((B/'evidence/browser_qa.json').read_text(encoding='utf-8'));assert q['status']=='PASS' and not q['external_requests'] and not q['errors']
schema={'record_type':'facility_candidate_not_confirmed_asset','required_fields':list(r[0]),'nullable':['site_id_official','process_unit_id_official','operator_id','operator_name','instrument_id','latitude','longitude','crs','accuracy_m','actual_throughput','gas_capture'],'keys':'candidate_id is local research identifier, never official site ID','relationships':'approval_holder, operator, instrument and monitoring point distinct; point ID scoped to facility','time':'source_updated differs from checked_on; current_status_verified independent','prohibition':'no null-to-zero conversion; no landfill reclassification; no operator-only merge'}
(B/'ENTITY_SCHEMA.json').write_text(json.dumps(schema,indent=2),encoding='utf-8',newline='\n')
(B/'evidence/validation.json').write_text(json.dumps({'status':'PASS_LOCAL_STRUCTURAL_ONLY','candidates':len(r),'identity_verification':'PARTIAL','no_operator_only_merge':True,'no_monitor_point_as_facility':True,'unknown_ids_and_coordinates_preserved':True,'browser':'20 viewport/page combinations PASS','independent_scientific_review':'PENDING','raw_http_body_capture':False},indent=2),encoding='utf-8',newline='\n')
(B/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(B).as_posix()+'\n' for p in sorted(B.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.txt' and p.suffix!='.png' and '__pycache__' not in p.parts),encoding='utf-8',newline='\n')
print('PASS: bounded candidates, null semantics, entity separation, UI receipt; science PENDING')
