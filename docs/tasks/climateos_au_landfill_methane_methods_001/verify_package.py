"""Offline artifact, provenance and frozen-scope checks; not scientific admission."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess
import sys
from mass_balance import validate_graph

TASK=Path(__file__).resolve().parent
ROOT=TASK.parents[2]
BASE='746825e65b8ddbd0f518709c94d9476df107208b'
PREFIX=TASK.relative_to(ROOT).as_posix()+'/'
EXCLUDED={'manifest.json','evidence/package-validation.json','REVIEW_REQUEST.json','HANDOFF_STATUS.json'}
REQUIRED=['README.md','FOUNDER_REPORT_ZH.md','SOURCE_REGISTER.md','REGULATORY_VERSION_MATRIX.md',
 'SECTION_AND_EQUATION_CROSSWALK.md','AU_LANDFILL_METHOD_COMPARISON.md','LANDFILL_PHYSICS_AND_MASS_BALANCE.md',
 'MEASUREMENT_AND_MODEL_CALIBRATION.md','PR143_E06_E07_BRIDGE_AUDIT.md','SYNTHETIC_MASS_BALANCE_RESULTS.md',
 'OPEN_DATA_FEASIBILITY.md','METHOD_KNOWLEDGE_INDEX.md','LEARNING_PATH_ZH.md','FUTURE_MODULES_INDEX.md',
 'QA_AND_VALIDATION.md','NEXT_SESSION.md','CRP_HANDOFF.md','REVIEW_REQUEST.json','HANDOFF_STATUS.json']

def digest(data): return hashlib.sha256(data).hexdigest()
def git(*args): return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
def package_files():
    return [p for p in sorted(TASK.rglob('*')) if p.is_file() and '__pycache__' not in p.parts
            and p.suffix in {'.md','.json','.py','.txt'} and p.relative_to(TASK).as_posix() not in EXCLUDED]
def canonical(p): return p.read_bytes().replace(b'\r\n',b'\n')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write-manifest',action='store_true');args=parser.parse_args()
    for name in REQUIRED: assert (TASK/name).is_file(), name
    for p in TASK.rglob('*.json'): json.loads(p.read_text(encoding='utf-8'))
    catalog=json.loads((TASK/'knowledge/catalog.json').read_text(encoding='utf-8'))
    assert len(catalog['sources'])==8 and catalog['integration']=='PENDING_INTEGRATION'
    source_ids=[s['id'] for s in catalog['sources']];edges=[];exercises=0
    for s in catalog['sources']:
        pkg=json.loads((TASK/'knowledge'/s['package']).read_text(encoding='utf-8'))
        for key in ['SOURCE_MASTER','KNOWLEDGE_CORE','SKILL_PROCEDURE','CASE_EVIDENCE','CONNECTIONS','LEARNING_PATH_ZH','UPDATE_LEDGER']: assert pkg[key]
        ex=pkg['LEARNING_PATH_ZH']['exercises'];assert len(ex)>=3 and all(x['question'] and x['reference_answer'] for x in ex);exercises+=len(ex)
        for e in pkg['KNOWLEDGE_CORE']['equations']:
            assert all(e[k] for k in ['id','locator','expression','variables','scope'])
        edges.append((s['id'],'INDEX'))
    validate_graph(source_ids+['INDEX'],edges)
    links=0
    for p in TASK.rglob('*.md'):
        prose=re.sub(r'`[^`]*`','',p.read_text(encoding='utf-8'))
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',prose):
            if target.startswith(('https://','http://','#','mailto:')):continue
            if args.write_manifest and (p.parent/target).resolve() in {TASK/'manifest.json',TASK/'evidence/package-validation.json'}:
                continue  # Bootstrap only; normal verification must check the generated files.
            assert (p.parent/target.split('#')[0]).is_file(),(p,target)
            links+=1
    sources=json.loads((TASK/'source_receipts/download-list.json').read_text())
    assert len(sources)==12 and len({s['url'] for s in sources})==12
    raw=[]
    for s in sources:
        r=json.loads((TASK/'source_receipts'/f"{s['id']}.json").read_text())
        assert r['url']==s['url']
        if r['status']=='ACQUIRED':
            assert re.fullmatch('[a-f0-9]{64}',r['sha256']) and r['bytes']>0
            path=ROOT/r['cache_path']
            if path.exists():
                data=path.read_bytes();assert len(data)==r['bytes'] and digest(data)==r['sha256'];status='RAW_BYTES_MATCH'
            else:status='RAW_NOT_CACHED'
        else:
            assert r['status']=='BLOCKED' and '403' in r['reason'] and 'sha256' not in r
            status='BLOCKED_NO_HASH'
        raw.append({'id':s['id'],'status':status})
    old_changes=git('diff','--name-only',BASE,'--','.').splitlines()
    assert all(p.startswith(PREFIX) for p in old_changes),old_changes
    assert git('hash-object',str(TASK/'TASKBOOK_ZH.md'))=='25b2b93a09176c829773cc9022d0f6ef118fa8aa'
    for h in ['REVIEW_REQUEST.json','HANDOFF_STATUS.json']:
        data=json.loads((TASK/h).read_text(encoding='utf-8'))
        assert data['scientific_gates']=={'D3':'DATA_NOT_READY','P1-A':'PENDING','PR140':'NO_VALID_PAIR','PR141':'NO_VALID_VERTICAL_PROFILE','PR143_ChainB':'BLOCKED','Stage3':'METHOD_READY_NOT_VALIDATED'}
        assert data['reviewed_head_sha'] is None and data['deployed'] is False
    files={p.relative_to(TASK).as_posix():digest(canonical(p)) for p in package_files()}
    manifest={'algorithm':'SHA-256','text_normalization':'CRLF to LF only; raw originals use exact-byte receipts',
              'excluded':sorted(EXCLUDED),'files':files}
    if args.write_manifest:
        (TASK/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    else:
        assert json.loads((TASK/'manifest.json').read_text())==manifest,'MANIFEST_MISMATCH'
    suspects=[]
    for p in package_files():
        # Narrow secret signatures; this is not a guarantee against all sensitive content.
        if re.search(r'gh[pousr]_[A-Za-z0-9]{20,}|AKIA[A-Z0-9]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----',p.read_text(encoding='utf-8')):suspects.append(str(p))
    assert not suspects,'SECRET_PATTERN'
    report={'status':'LOCAL_VERIFIED_WITH_SOURCE_GAPS','files_hashed':len(files),'local_links':links,
            'knowledge_sources':len(source_ids),'knowledge_exercises':exercises,'raw_sources':raw,
            'frozen_taskbook_blob':'25b2b93a09176c829773cc9022d0f6ef118fa8aa',
            'diff_scope':'ONLY_NEW_TASK_DIRECTORY','narrow_secret_signatures':0,
            'scientific_admission':'PENDING','raw_redistribution':False}
    (TASK/'evidence/package-validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__':main()
