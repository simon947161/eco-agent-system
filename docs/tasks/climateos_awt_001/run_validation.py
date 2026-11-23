"""Execute actual local tests/replay; record evidence without touching old outputs."""
import contextlib
import hashlib
import importlib.util
import io
import json
import platform
import sys
import unittest
from pathlib import Path
import engine as e

T=e.HERE
def save(name,v):
    (T/'evidence'/name).write_text(json.dumps(v,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8',newline='\n')

def main():
    old={p.name:e.sha_bytes(p) for p in (T/'evidence').glob('*.json') if p.name in ['results.json','sensitivities.json','submission-events.json']}
    e.main()
    new={name:e.sha_bytes(T/'evidence'/name) for name in old}
    if old!=new: raise ValueError('NONDETERMINISTIC_REPLAY')
    save('replay.json',dict(equal=True,algorithm='SHA256_EXACT_BYTES',outputs=new))
    sys.path.insert(0,str(e.ROOT))
    suite=unittest.defaultTestLoader.loadTestsFromName('tests.test_awt_claims')
    stream=io.StringIO()
    result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    (T/'evidence'/'unit-tests.txt').write_text(stream.getvalue(),encoding='utf-8',newline='\n')
    save('unit-tests.json',dict(command='python -m unittest tests.test_awt_claims -v',
        python=platform.python_version(),platform=platform.system(),tests=result.testsRun,
        failures=len(result.failures),errors=len(result.errors),skipped=len(result.skipped),passed=result.wasSuccessful()))
    cases={s:e.assess(e.read('examples/'+s+'.json')) for s in 'ABCD'}
    p=e.read('examples/B.json');p['baseline_evidence']='MISSING'
    cases['missing_baseline']=e.assess(p)
    p=e.read('examples/B.json');p['dataset']['sha256']='0'*64
    cases['tampered_source']=e.assess(p)
    f=e.read('fixtures/B.json');f['capture_fraction']=1.2
    try:
        e.calculate(f)
        raise AssertionError('INVALID_PHYSICS_NOT_REJECTED')
    except ValueError as exc:
        cases['physically_inconsistent']={'status':'CONDITIONS_NOT_MET','reason':str(exc),'net':None}
    cases['unknown_exemption']=e.legal_screen(dict(e.read('examples/C.json')['legal'],exemption='UNKNOWN'))
    save('decision-cases.json',cases)
    paths=['cczps_lite/integration/physics_validation.py','cczps_lite/integration/methane_knowledge_engine.py',
        'docs/tasks/climateos_au_landfill_methane_methods_001/mass_balance.py',
        'docs/tasks/climateos_global_method_evidence_ecochain_001/reviewer.py',
        'cczps_lite/contracts/bondo_evidence_passport.schema.json']
    save('reuse-hashes.json',{'baseline':'ae1050a621ac794e447f9ac047865d90b2f04b03',
        'normalization':'TEXT_LF', 'files':{p:hashlib.sha256((e.ROOT/p).read_bytes().replace(b'\r\n',b'\n')).hexdigest() for p in paths}})
    print(json.dumps({'tests':result.testsRun,'passed':result.wasSuccessful(),'replay_equal':True,'decision_cases':len(cases)}))
    if not result.wasSuccessful():sys.exit(1)

if __name__=='__main__':main()
