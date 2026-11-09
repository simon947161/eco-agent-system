"""Run scoped tests plus frozen-core regressions; archive actual output."""
from pathlib import Path
import argparse,hashlib,json,platform,subprocess,sys
from datetime import datetime,timezone
T=Path(__file__).resolve().parent
ROOT=T.parents[2]
P=T.relative_to(ROOT).as_posix()

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--record',action='store_true'); args=parser.parse_args()
    logdir=T/'evidence' if args.record else ROOT/'runtime_data/global_method_review_validation'
    logdir.mkdir(parents=True,exist_ok=True)
    commands=[['-m','unittest','discover','-s',P+'/tests','-v'],
      ['-m','unittest','discover','-s','docs/tasks/climateos_au_landfill_methane_methods_001','-p','test_mass_balance.py','-v'],
      ['-m','unittest','tests.test_physics_validation.GasTests','tests.test_methane_knowledge_engine','-v']]
    logs=[datetime.now(timezone.utc).isoformat(),'Python '+platform.python_version()]
    for command in commands:
        p=subprocess.run([sys.executable,*command],cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        logs+=['COMMAND: python '+' '.join(command),p.stdout,'EXIT_CODE: '+str(p.returncode)]
        (logdir/'tests.txt').write_text('\n'.join(logs),encoding='utf-8',newline='\n')
        if p.returncode: raise SystemExit(p.returncode)
    snapshots=[]
    for _ in range(2):
        for name in ['reviewer.py','check_open_fragment.py']:
            subprocess.run([sys.executable,str(T/name)],cwd=ROOT,check=True)
        snapshots.append({n:hashlib.sha256((T/'evidence'/n).read_bytes().replace(b'\r\n',b'\n')).hexdigest() for n in ['review-results.json','chain-a-replay.json','open-fragment-results.json']})
    assert snapshots[0]==snapshots[1]
    report={'status':'BYTE_IDENTICAL','runs':2,'hash_basis':'UTF8 text LF-normalized; input ZIP exact bytes','sha256':snapshots[0]}
    if not args.record:
        assert report==json.loads((T/'evidence/replay.json').read_text(encoding='utf-8')),'FROZEN_REPLAY_CHANGED'
    (logdir/'replay.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('Scoped tests and deterministic replay passed; inspect tests.txt for counts')

if __name__=='__main__': main()
