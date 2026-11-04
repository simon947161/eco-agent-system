"""Package integrity only; never computes scientific/model results."""
from pathlib import Path
import json,re,hashlib,subprocess
B=Path(__file__).resolve().parent
R=B.parents[3]
def read(p):return json.loads((B/p).read_text(encoding='utf-8'))
s=read('EXECUTION_STATE.json')
assert s['science']=='PENDING'
assert all(s[k] is False for k in ['numerical_experiments','emission_calculation','deployed','merged','calculator'])
methods=read('METHOD_COMPARISON.json');data=read('DATA_READINESS.json');sources=read('SOURCES.json')
ids={x['id'] for x in sources}
assert len(methods)==6 and len(data)==4 and len(ids)==len(sources)
assert methods[0]['comparison_status']=='NOT_COMPARABLE'
assert all(d['raw_sha256'] is None and d['abc_status']=='DATA_NOT_READY' for d in data)
assert all(d['source_id'] in ids or d['source_id']=='LOCAL_C2' for d in data)
assert all(i in ids for m in methods for i in m['source_ids'])
assert all(x['raw_file_sha256'] is None for x in sources)
assert methods[1]['parameters'] is None and methods[-1]['parameters'] is None
for name in ['D0_COMPARISON_CONTRACT.md','D1_BASELINE_METHODS.md','D2_RESPONSE_MODEL_FAMILIES.md','D3_VALIDATION_DATA_DISCOVERY.md','D4_FALSIFICATION_PROTOCOL.md','LITERATURE_AUDIT_NOTES.md','EVIDENCE_MATRIX.md','NEXT_SESSION.md','README.md']:
 assert (B/name).is_file()
t=(B/'index.html').read_text(encoding='utf-8')
assert len(re.findall('<section class="page"',t))==12
assert 'connect-src \'none\'' in t
for link in re.findall(r'href="([^"]+)"',t):
 if not link.startswith(('https:','#')) and link!='evidence/validation.json':assert (B/link).exists(),link
q=read('evidence/browser_qa.json')
assert q['status']=='PASS' and not q['errors'] and not q['external_requests']
assert sum(len(v['pages']) for v in q['viewports'])==24
# Frozen records: compare bytes to exact preceding reviewed HEAD.
prior=s['parent_sha']
preserved=[]
for folder in ['p1a','batch-b','batch-b2','batch-b3','batch-c','batch-c2']:
 prefix='docs/research/carbonos/'+folder
 tracked=subprocess.check_output(['git','ls-tree','-r','--name-only',prior,'--',prefix],cwd=R,text=True).splitlines()
 for path in tracked:
  baseline=subprocess.check_output(['git','show',prior+':'+path],cwd=R)
  actual=(R/path).read_bytes()
  # Prior files use platform checkout newline conversion; compare normalized content,
  # and also require no git diff in protected directories.
  assert baseline.replace(b'\r\n',b'\n')==actual.replace(b'\r\n',b'\n'),path
 assert subprocess.run(['git','diff','--exit-code',prior,'--',prefix],cwd=R,capture_output=True).returncode==0
 preserved.append({'folder':folder,'tracked_files_checked':len(tracked),'status':'UNCHANGED'})
result={'status':'LOCAL_VERIFIED_STRUCTURAL_UI_ONLY','browser_viewport_page_checks':24,'source_records':len(sources),'method_entries':len(methods),'data_entries':len(data),'raw_files_acquired':0,'science':'PENDING','raw_observation_QC':'NOT_PERFORMED_NO_DATA','numeric_experiments':False,'preserved_prior_artifacts':preserved,'scope':'Authored package integrity/navigation only, not scientific validation or CI'}
(B/'evidence/validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
paths=[p for p in sorted(B.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.txt' and p.suffix!='.png' and '__pycache__' not in p.parts]
(B/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(B).as_posix()+'\n' for p in paths),encoding='utf-8',newline='\n')
print(json.dumps(result))
