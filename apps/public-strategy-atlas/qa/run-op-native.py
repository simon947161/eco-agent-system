"""Run all current application native tests, retaining exact executed file hashes."""
from pathlib import Path
import concurrent.futures,datetime,hashlib,json,os,subprocess,sys,time
APP=Path(__file__).resolve().parents[1];OUT=APP/os.environ.get('ATLAS_NATIVE_OUTPUT','qa/op-completion-20261102/native');OUT.mkdir(parents=True,exist_ok=True)
files=sorted(APP.glob('*.test.cjs'))
if sys.argv[1:]:files=[APP/x for x in sys.argv[1:]]
def run(file):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();before=hashlib.sha256(file.read_bytes()).hexdigest();begin=time.monotonic()
 with (OUT/(file.name+'.log')).open('w')as log:r=subprocess.run(['node',file.name],cwd=APP,stdout=log,stderr=subprocess.STDOUT)
 return {'file':file.name,'startedAt':start,'finishedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'seconds':round(time.monotonic()-begin,2),'sha256':before,'fileUnchanged':hashlib.sha256(file.read_bytes()).hexdigest()==before,'exitCode':r.returncode,'status':'PASS_TESTED_HERE'if r.returncode==0 else'FAIL','log':file.name+'.log'}
rows=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=int(os.environ.get('ATLAS_NATIVE_WORKERS','2')))as pool:
 for future in concurrent.futures.as_completed([pool.submit(run,f)for f in files]):
  row=future.result();rows.append(row);(OUT/'results.json').write_text(json.dumps({'testFiles':len(files),'completed':len(rows),'results':sorted(rows,key=lambda x:x['file'])},indent=2)+'\n');print(row['status'],row['file'],flush=True)
if any(r['status']!='PASS_TESTED_HERE'or not r['fileUnchanged']for r in rows):sys.exit(1)
