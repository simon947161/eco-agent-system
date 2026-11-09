"""Offline package manifest/link/budget/frozen-core audit; no remote claims."""
from pathlib import Path
import argparse,hashlib,json,re,subprocess
T=Path(__file__).resolve().parent
ROOT=T.parents[2]
PREFIX=T.relative_to(ROOT).as_posix()+'/'
BASE='77a35e2723372a290579e4549a86781e2be65c04'
INTAKE='32c56125e19ffa1f00f7937bcba67729b16e7203'
EXCLUDED={'manifest.json','REVIEW_REQUEST.json','HANDOFF_STATUS.json'}

def raw(path):
    b=path.read_bytes()
    return b if path.suffix=='.zip' else b.replace(b'\r\n',b'\n')

def git(*args):
    return subprocess.check_output(['git',*args],cwd=ROOT)

def snapshot():
    return {p.relative_to(T).as_posix():hashlib.sha256(raw(p)).hexdigest() for p in sorted(T.rglob('*'))
            if p.is_file() and '__pycache__' not in p.parts and p.name not in EXCLUDED}

def check(creating_manifest=False):
    files=snapshot(); links=0
    for p in T.rglob('*.md'):
        txt=p.read_text(encoding='utf-8')
        for target in re.findall(r'\]\(([^)]+)\)',txt):
            if '://' in target or target.startswith('#'):continue
            path=target.split('#')[0]
            target_path=(p.parent/path).resolve()
            assert target_path.exists() or (creating_manifest and target_path==T/'manifest.json'), (str(p),target)
            links+=1
    secret=re.compile(r'(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)')
    for p in T.rglob('*'):
        if p.is_file() and p.suffix in {'.md','.json','.py','.txt'}:
            assert not secret.search(p.read_text(encoding='utf-8')),p
    for name in ['TASKBOOK_ZH.md','ECOCHAIN_GOVERNANCE_MEMO_2026-11-09.md']:
        assert raw(T/name)==git('show',INTAKE+':'+PREFIX+name).replace(b'\r\n',b'\n'),name
    changed=git('diff','--name-only',BASE,'--').decode().splitlines()
    assert all(p.startswith(PREFIX) for p in changed),changed
    budgets=json.loads((T/'evidence/source-review-receipts.json').read_text(encoding='utf-8'))
    assert budgets['new_theme_count']==len(budgets['sources'])==9 and len(budgets['deep_comparison_jurisdictions'])<=4
    assert budgets['open_candidates']==1 and budgets['synthetic_packages']==3
    results=json.loads((T/'evidence/review-results.json').read_text(encoding='utf-8'))
    assert {k:v['status'] for k,v in results.items()}=={'A':'METHOD_ALIGNED','B':'MATERIAL_CONTRADICTION','C':'EVIDENCE_INSUFFICIENT'}
    assert all(v['REGULATORY_CERTIFICATION']=='NOT_PROVIDED' and v['human_review']=='PENDING' for v in results.values())
    logs=(T/'evidence/tests.txt').read_text(encoding='utf-8')
    counts=[int(x) for x in re.findall(r'Ran (\d+) tests',logs)]
    assert counts==[47,11,19] and logs.count('EXIT_CODE: 0')==3,counts
    # All paths outside the new task, including PR144 core and CCZPS, must be unchanged.
    assert git('diff',BASE,'--','cczps_lite','tests','docs/tasks/climateos_au_landfill_methane_methods_001','docs/tasks/climateos_methane_physics_knowledge_engine_001')==b''
    return files,links

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true'); args=parser.parse_args()
    files,links=check(creating_manifest=args.write)
    if args.write:
        (T/'manifest.json').write_text(json.dumps({'algorithm':'SHA256; UTF8 text LF-normalized; ZIP exact bytes',
          'exclusions':sorted(EXCLUDED),'files':files},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    else:
        assert files==json.loads((T/'manifest.json').read_text(encoding='utf-8'))['files'],'MANIFEST_MISMATCH'
    print(f'PASS: {len(files)} artifact hashes; {links} local links; 77 tests logged; frozen scope; bounded sources; narrow credential scan')

if __name__=='__main__':main()
