"""Author-only integrity manifest; not an external signature or science approval."""
import hashlib, json
from pathlib import Path
T=Path(__file__).resolve().parent
ROOT=T.parents[2]

def main():
    excluded={'manifest.json','tests.txt','validation.json','REVIEW_REQUEST.json','HANDOFF_STATUS.json'}
    files=[p for p in T.rglob('*') if p.is_file() and p.suffix in ('.md','.json','.py','.txt') and p.name not in excluded and '__pycache__' not in p.parts]
    files += [ROOT/'cczps_lite/integration/physical_process_trajectory.py',ROOT/'tests/test_physical_process_trajectory.py',T/'.gitattributes']
    exact={(T/'evidence/RONI.ascii.txt').relative_to(ROOT).as_posix()}
    hashes={}
    for p in sorted(set(files)):
        rel=p.relative_to(ROOT).as_posix(); raw=p.read_bytes()
        if rel not in exact: raw=raw.replace(b'\r\n',b'\n')
        hashes[rel]=hashlib.sha256(raw).hexdigest()
    (T/'evidence/manifest.json').write_text(json.dumps({'basis':'LF-normalized text except byte_exact files; HTTP raw SHA in acquisition.json',
        'trust':'Reviewed Git tree; not external signature. R/D handoff metadata and execution logs excluded.',
        'byte_exact':sorted(exact),'files':hashes},indent=2)+'\n',encoding='utf-8',newline='\n')
    print('Frozen',len(hashes),'files')

if __name__=='__main__': main()
