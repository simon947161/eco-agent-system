"""Record real local test commands and deterministic replay evidence."""
from pathlib import Path
import hashlib
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone

T=Path(__file__).resolve().parent
ROOT=T.parents[2]
PREFIX=T.relative_to(ROOT).as_posix()

def main():
    commands=[['-m','unittest','discover','-s',PREFIX,'-p','test_mass_balance.py','-v'],
              ['-m','unittest','tests.test_physics_validation.GasTests','tests.test_methane_knowledge_engine','-v']]
    logs=['Executed UTC: '+datetime.now(timezone.utc).isoformat(), 'Python: '+platform.python_version()]
    for command in commands:
        result=subprocess.run([sys.executable,*command],cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        logs.extend(['COMMAND: python '+' '.join(command),result.stdout,'EXIT_CODE: '+str(result.returncode)])
        if result.returncode:
            (T/'evidence/tests.txt').write_text('\n'.join(logs),encoding='utf-8')
            raise SystemExit(result.returncode)
    names=['synthetic-inputs.json','synthetic-results.json','worked-examples.json']
    snapshots=[]
    for _ in range(2):
        subprocess.run([sys.executable,str(T/'run_synthetic.py')],cwd=ROOT,check=True)
        snapshots.append({n:hashlib.sha256((T/'evidence'/n).read_bytes()).hexdigest() for n in names})
    assert snapshots[0]==snapshots[1]
    (T/'evidence/replay.json').write_text(json.dumps({'status':'BYTE_IDENTICAL','runs':2,'outputs':snapshots[0],'scope':'synthetic ledger, unit examples only'},indent=2)+'\n',encoding='utf-8')
    (T/'evidence/tests.txt').write_text('\n'.join(logs),encoding='utf-8')
    print('30 tests passed; two deterministic runs; logs saved')

if __name__=='__main__':main()
