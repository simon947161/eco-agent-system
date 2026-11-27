"""Check the archived QA artifact hashes and link them to the tested checkout."""
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
APP=HERE.parents[1]

def load(path):
    return json.loads(path.read_text())

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

report=load(HERE/'acceptance.json')
for filename,expected in report['artifactSha256'].items():
    if sha(HERE/filename)!=expected:
        raise SystemExit('QA_ARTIFACT_MISMATCH '+filename)
for filename,expected in report['sourceSha256'].items():
    if sha(APP/filename)!=expected:
        raise SystemExit('TESTED_FILE_HAS_CHANGED '+filename)
native=load(HERE/'native.json')
browser=load(HERE/'system/browser-e10.json')
if native['total']!=len(native['files']) or native['failed'] or native['passed']!=native['total']:
    raise SystemExit('NATIVE_REPORT_INCOMPLETE')
if not browser['allSuitesExecutedThisInvocation'] or len(browser['results'])!=6 or any(
    r['exitCode']!=0 or r['status']!='PASS_TESTED_HERE' for r in browser['results']
):
    raise SystemExit('BROWSER_REPORT_INCOMPLETE')
print('PASS archived evidence matches the recorded source files,',native['total'],'native files and six system browser suites. This check does not rerun those tests.')
