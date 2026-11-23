"""Verify sealed authored package and inherited code, without network or writes."""
import hashlib
import json
from pathlib import Path
import re
import sys
import engine as e

T=e.HERE
def file_hash(path):
    b=path.read_bytes()
    if path.suffix!='.png': b=b.replace(b'\r\n',b'\n')
    return hashlib.sha256(b).hexdigest()

def paths():
    local=[p for p in T.rglob('*') if p.is_file() and '__pycache__' not in p.parts
           and p.name not in ['manifest.json','package-validation.json']]
    return sorted(local+[e.ROOT/'tests/test_awt_claims.py',e.ROOT/'.github/workflows/cczps-lite-tests.yml'],key=str)

def verify():
    manifest=e.read('manifest.json')
    actual={p.relative_to(e.ROOT).as_posix():file_hash(p) for p in paths()}
    if actual!=manifest['files']: raise ValueError('MANIFEST_MISMATCH')
    for p,h in e.read('evidence/reuse-hashes.json')['files'].items():
        if file_hash(e.ROOT/p)!=h: raise ValueError('FROZEN_DEPENDENCY_CHANGED:'+p)
    for s in 'ABCD':
        e.validate(e.read('examples/'+s+'.json'))
        if e.assess(e.read('examples/'+s+'.json'))!=e.read('evidence/results.json')[s]:
            raise ValueError('RESULT_REPLAY_MISMATCH')
    # All reported JSON-pointer links must resolve to actual saved result fields.
    results=e.read('evidence/results.json')
    for s in 'ABCD':
        for entity in e.read('examples/'+s+'.json')['entities']:
            value=results
            for part in entity['result_pointer'].split('#/')[1].split('/'):
                value=value[part]
    html=(T/'index.html').read_text(encoding='utf-8')
    local_links=0
    for link in re.findall(r'href="([^"]+)"',html):
        if not link.startswith(('http:','https:','#')):
            if not (T/link).is_file():raise ValueError('BROKEN_HTML_LINK:'+link)
            local_links+=1
    text_files=[p for p in paths() if p.suffix!='.png']
    # Conservative public-output scans; not a substitute for manual scope review.
    patterns=[r'gh[pousr]_[A-Za-z0-9]{20,}',r'github_pat_[A-Za-z0-9_]{20,}',
              r'AKIA[0-9A-Z]{16}',r'-----BEGIN [A-Z ]*PRIVATE KEY-----',
              r'(?i)D:[\\/]eco_engine_v200[\\/]',r'(?i)D:[\\/]EcoEngine[\\/]']
    for p in text_files:
        body=p.read_text(encoding='utf-8')
        if any(re.search(pattern,body) for pattern in patterns):
            raise ValueError('PUBLIC_EXPORT_SCAN:'+p.name)
    return dict(status='PASS',files=len(actual),inherited_code_hashes=5,local_html_links=local_links,
                passport_and_result_replay=4,public_export_patterns='NO_MATCH',science='PENDING')

if __name__=='__main__':
    if '--seal' in sys.argv:
        manifest={'algorithm':'SHA256; authored text normalized LF; PNG exact bytes; external raw hashes separate',
            'baseline':'ae1050a621ac794e447f9ac047865d90b2f04b03',
            'files':{p.relative_to(e.ROOT).as_posix():file_hash(p) for p in paths()}}
        (T/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8',newline='\n')
    result=verify()
    if '--seal' in sys.argv:
        (T/'evidence/package-validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(result))
