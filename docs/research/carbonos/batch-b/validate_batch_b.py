from pathlib import Path
import json,csv,re,hashlib
B=Path(__file__).resolve().parent
rows=json.loads((B/'AU_WASTE_FACILITY_SOURCE_REGISTER.json').read_text(encoding='utf-8'))
schema=json.loads((B/'SOURCE_SCHEMA.json').read_text(encoding='utf-8'))
assert {r['jurisdiction'] for r in rows}=={'Commonwealth','NSW','VIC','QLD','WA','SA','TAS','NT','ACT'}
assert len({r['source_id'] for r in rows})==len(rows)==20
assert len({r['canonical_url'].rstrip('/') for r in rows})==len(rows)
assert all(set(r)==set(schema['items']['required']) for r in rows)
assert all(r['evidence_tier'] in ['B','C'] and r['science_admission']=='PENDING' and r['coordinate_accuracy_m'] is None and r['facility_records_extracted']==0 for r in rows)
csvrows=list(csv.DictReader((B/'AU_WASTE_FACILITY_SOURCE_REGISTER.csv').open(encoding='utf-8')))
assert [r['source_id'] for r in csvrows]==[r['source_id'] for r in rows]
observations=json.loads((B/'evidence/source_observations.json').read_text(encoding='utf-8'))
assert {r['source_id'] for r in observations}=={r['source_id'] for r in rows}
qa=json.loads((B/'evidence/browser_qa.json').read_text(encoding='utf-8'))
assert qa['status']=='PASS' and not qa['errors'] and not qa['external_requests']
for p in list(B.glob('*.md'))+[B/'index.html']:
 text=p.read_text(encoding='utf-8')
 targets=re.findall(r'href="([^"]+)"',text) if p.suffix=='.html' else re.findall(r'\]\(([^)]+)\)',text)
 for target in targets:
  if not target.startswith(('http:','https:','#')):assert (p.parent/target).exists(),target
 assert not re.search(r'ghp_|github_pat_|BEGIN .*PRIVATE KEY|C:\\Users\\',text)
result={'status':'PASS','jurisdiction_levels':9,'unique_source_entries':20,'facility_records':0,'source_url_dedup':'PASS','facility_entity_dedup':'NOT_EXECUTED_NO_RECORDS','coordinates_accuracy':'UNKNOWN_NULL_PRESERVED','licence_validation':'PENDING','p1a_science_admission':'PENDING','scientific_experiment':False,'browser_viewports':2,'pages_per_viewport':10,'source_body_hashes':'NOT_CAPTURED_NOT_CLAIMED','visual_review':['mobile-page-1.png'],'limits':'Source catalogue only; no facility census or numerical model; manual schema fields check, not full JSON Schema engine'}
(B/'evidence/validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8',newline='\n')
print(json.dumps(result))
