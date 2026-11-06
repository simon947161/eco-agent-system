"""Write actual unittest records; --full runs the existing complete suite."""
import argparse
import io
import json
import platform
from pathlib import Path
import unittest


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--full',action='store_true');args=parser.parse_args()
    suite=(unittest.defaultTestLoader.discover('tests') if args.full else unittest.defaultTestLoader.loadTestsFromName('tests.test_physics_validation'))
    stream=io.StringIO();result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    folder=Path('docs/tasks/climateos_physics_validation_001');name='full-suite' if args.full else 'physics-tests'
    (folder/f'{name}.log').write_text(stream.getvalue(),encoding='utf-8')
    report={'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),'skips':[{'test':str(t),'reason':r} for t,r in result.skipped],'successful':result.wasSuccessful(),'python':platform.python_version(),'scope':'implementation/unit verification; no observational validation'}
    (folder/f'{name}.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report));raise SystemExit(0 if result.wasSuccessful() else 1)


if __name__=='__main__':main()
