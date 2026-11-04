from pathlib import Path
import json,re,hashlib,datetime
B=Path(__file__).resolve().parent
def j(p):return json.loads((B/p).read_text(encoding='utf-8'))
r=j('EVENT_QUALITY_REGISTER.json');assert len(r)==2 and {x['station_id'] for x in r}=={'070217','039083'}
for x in r:
 for f in ['raw_daily_records','raw_file_sha256','observed_row_count','day_quality_flags','window_completeness','utc_start','utc_end']:assert x[f] is None
 assert x['value_status']=='PUBLISHED_SUMMARY_NOT_REVERIFIED_RAW' and x['science']=='PENDING'
 t=datetime.date.fromisoformat(x['event_label'])
 assert datetime.date.fromisoformat(x['requested_window_start'])==t-datetime.timedelta(days=7)
 assert datetime.date.fromisoformat(x['requested_window_end'])==t+datetime.timedelta(days=30)
m=j('MEASUREMENT_READINESS.json');assert len(m)==12 and len({x['id'] for x in m})==12
assert all(x['available_measurements'] is None and x['status']=='REQUIRED_NOT_ACQUIRED' for x in m)
a=j('ACCESS_ATTEMPTS.json');assert len(a)==8 and all(x['result']!='SUCCESS_RAW_DATA' for x in a)
s=j('EXECUTION_STATE.json');assert s['science']=='PENDING' and not s['numerical_experiments'] and not s['emission_calculation']
q=j('evidence/browser_qa.json');assert q['status']=='PASS' and not q['errors'] and not q['external_requests']
t=(B/'index.html').read_text(encoding='utf-8');assert len(re.findall('<section class="page"',t))==10
for link in re.findall(r'href="([^"]+)"',t):
 if not link.startswith(('https:','#')):assert (B/link).exists(),link
result={'status':'LOCAL_VERIFIED_STRUCTURAL_UI_ONLY','event_exemplars':2,'raw_daily_records_acquired':0,'raw_data_quality_validation':'NOT_PERFORMED_NO_DATA','measurement_requirements':12,'browser_viewport_page_checks':20,'science':'PENDING','note':'Date-window tests validate protocol labels only; not weather analysis, threshold execution or model simulation.'}
(B/'evidence/validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
(B/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(B).as_posix()+'\n' for p in sorted(B.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.txt' and p.suffix!='.png' and '__pycache__' not in p.parts),encoding='utf-8',newline='\n')
print(json.dumps(result))
