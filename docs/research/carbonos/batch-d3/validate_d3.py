"""Offline package/metadata integrity checks only; no observation or model computation."""
from pathlib import Path
import hashlib,json,re,subprocess,stat
B=Path(__file__).resolve().parent;R=B.parents[3]
def j(n):return json.loads((B/n).read_text(encoding='utf-8'))
c=j('DATASET_CANDIDATES.json');s=j('EXECUTION_STATE.json');f=j('FAILURES_AND_STOPS.json')
assert len(c)==3 and len({x['id'] for x in c})==3
assert all(x['decision']=='REJECTED' and x['actual_observation_bytes']==0 for x in c)
assert f['candidate_limit']==3 and f['stop']=='HARD_STOP_REACHED' and f['no_retry']
assert len(f['attempts'])==2 and all(x['status']==403 for x in f['attempts'])
urls=[x['url'] for x in f['attempts']]
assert len(set(urls))==len(urls) and not set(urls)&set(f['excluded_known_blocked_urls'])
assert s['science']=='PENDING' and s['status']=='DATA_NOT_READY'
for k in ['numerical_experiments','regression','emission_calculation','flux_inversion','simulation','weather_replay','calculator','merged','deployed','external_contact']:
 assert s[k] is False,k
m=j('LICENCE_AND_SHA256_MANIFEST.json')
assert m['observation_files']==[] and not m['original_observation_bytes_obtained']
assert all(x is None for x in m['raw_data_hashes'].values())
# The only successful provider bytes are explicitly metadata, not data.
p=R.parent/'.local/d3-data-admission/ny-landing.html'
if p.exists():
 b=p.read_bytes();r=m['metadata_files'][0]
 assert len(b)==r['size'] and hashlib.sha256(b).hexdigest()==r['sha256']
 assert r['kind']=='PROVIDER_LANDING_HTML_NOT_OBSERVATION_DATA'
 assert not p.stat().st_mode & stat.S_IWRITE
 assert b'Creative Commons Zero v1.0 Universal' in b and b'/downloads/file_stream/4623494' in b
 metadata='MATCHED_LOCAL_METADATA_BYTES_READONLY'
else:metadata='LOCAL_METADATA_NOT_AVAILABLE_ON_THIS_MACHINE'
for a in j('SCHEMA_AND_TIME_AUDIT.json'):
 assert a['inspection']=='NOT_PERFORMED_NO_RAW_DATA'
 for k in ['native_columns','row_count','clock_timezone_DST','QC_flag_counts','missing_dates','sample_coverage','spatial_extent_from_raw']:
  assert a[k] is None,k
t=(B/'index.html').read_text(encoding='utf-8')
assert len(re.findall('<section class="page"',t))==12
for u in re.findall(r'href="([^"]+)"',t):
 if not u.startswith(('https:','#')) and u!='evidence/validation.json':assert (B/u).is_file(),u
q=j('evidence/browser_qa.json')
assert q['status']=='PASS' and not q['errors'] and not q['external_requests']
assert sum(len(v['pages']) for v in q['viewports'])==24
folders=['p1a','batch-b','batch-b2','batch-b3','batch-c','batch-c2','batch-d']
paths=['docs/research/carbonos/'+x for x in folders]
assert subprocess.run(['git','diff','--exit-code',s['parent_sha'],'--',*paths],cwd=R,capture_output=True).returncode==0
tracked=subprocess.check_output(['git','ls-tree','-r','--name-only',s['parent_sha'],'--',*paths],cwd=R,text=True).splitlines()
result={'status':'LOCAL_VERIFIED_PACKAGE_ONLY','candidate_count':3,'original_observation_files':0,'observation_quality_check':'NOT_PERFORMED_NO_DATA','metadata_integrity':metadata,'browser_checks':24,'prior_tracked_files_unchanged':len(tracked),'science':'PENDING','CI':'NOT_ASSERTED','numerical_experiments':False}
(B/'evidence/validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
manifest=''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(B).as_posix()+'\n' for p in sorted(B.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.txt' and p.suffix!='.png' and '__pycache__' not in p.parts)
(B/'SHA256SUMS.txt').write_text(manifest,encoding='utf-8',newline='\n')
print(json.dumps(result))
