"""Verify frozen package hashes, local links, and deterministic public replay."""
from pathlib import Path
import hashlib
import json
import re
import sys

TASK = Path(__file__).resolve().parent
ROOT = TASK.parents[2]
sys.path.insert(0, str(ROOT))
from cczps_lite.integration.client_ai_evidence import execute


def main():
    manifest = json.loads((TASK/'evidence/manifest.json').read_text(encoding='utf-8'))
    for item in manifest['files']:
        path = ROOT / item['path']
        if not path.resolve().is_relative_to(ROOT.resolve()):
            raise AssertionError('MANIFEST_PATH_ESCAPE')
        raw=path.read_bytes()
        if item['hash_basis']=='repository_text_LF':
            raw=raw.replace(b'\r\n',b'\n')
        assert hashlib.sha256(raw).hexdigest() == item['sha256'], item['path']
    links=0
    for path in TASK.glob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)',path.read_text(encoding='utf-8')):
            if '://' in target or target.startswith('#'):
                continue
            assert (path.parent/target.split('#')[0]).exists(), (path.name,target)
            links+=1
    request=json.loads((TASK/'request.json').read_text(encoding='utf-8'))
    actual=execute(request)
    assert actual == json.loads((TASK/'evidence/audit.json').read_text(encoding='utf-8'))
    assert actual['spatial_result'] == json.loads((TASK/'evidence/station.geojson').read_text(encoding='utf-8'))
    print(json.dumps({'status':'PASS','hashes':len(manifest['files']),'local_links':links,
                      'deterministic_replay':'MATCH','scope':'integrity and local QA; not independent science validation'}))


if __name__=='__main__':
    main()
