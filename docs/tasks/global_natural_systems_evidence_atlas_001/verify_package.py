"""Offline package integrity, local links, source receipts and publication boundaries."""
import ast
import json
import re
import sys
from pathlib import Path
T=Path(__file__).resolve().parent; ROOT=T.parents[2]
sys.path.insert(0,str(ROOT))
from cczps_lite.integration import global_natural_systems_atlas as atlas

def main():
    checked=atlas.verify_manifest(); links=0; json_count=0
    for path in T.rglob('*'):
        if not path.is_file() or '__pycache__' in path.parts: continue
        if path.suffix=='.json': json.loads(path.read_text(encoding='utf-8'));json_count+=1
        if path.suffix=='.py': ast.parse(path.read_text(encoding='utf-8'),filename=str(path))
        if path.suffix not in ('.md','.json','.py','.txt'): raise ValueError('UNEXPECTED_PUBLISHED_FORMAT:'+path.name)
        text=path.read_text(encoding='utf-8')
        if re.search(r'gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',text):
            raise ValueError('POSSIBLE_SECRET:'+path.name)
        if path.suffix=='.md':
            for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)',text):
                if link.startswith(('https://','http://','#','mailto:')): continue
                relative=link.split('#')[0]
                if not (path.parent/relative).exists(): raise ValueError('BROKEN_LOCAL_LINK:'+str(path)+':'+link)
                links+=1
    data=atlas.load_atlas()
    raw=[]
    for receipt in atlas.read(T/'evidence/acquisition.json'):
        path=ROOT/f"runtime_data/global_natural_atlas_metadata/{receipt['id']}.html"
        if path.exists():
            import hashlib
            assert hashlib.sha256(path.read_bytes()).hexdigest()==receipt['sha256']
            assert path.stat().st_size==receipt['bytes']
            raw.append(receipt['id'])
    print(json.dumps({'status':'PACKAGE_VERIFIED','manifest_files':checked,'local_links':links,
       'json_files':json_count,'raw_cache_matches_if_present':raw,'geometry_coverage':0,'scientific_admission':'PENDING'}))

if __name__=='__main__': main()
