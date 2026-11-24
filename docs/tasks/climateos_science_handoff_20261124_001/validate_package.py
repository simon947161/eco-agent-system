"""Offline document/metadata QA only. No downloads, models or conversions."""
from pathlib import Path
import ast
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from urllib.parse import urlparse, unquote

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
BASE = '9eb7577e145e76161f9f1cd8509348b19c2904cc'
TASK_SHA = '7926373d975a16b59fb508b127216fd953893a9bc0fa351892d8b84f705606f3'
checks = []

def check(name, condition):
    checks.append({'check': name, 'result': 'PASS' if condition else 'FAIL'})
    if not condition:
        raise AssertionError(name)

def site_label_allowed(direction_status, coordinates_verified):
    return direction_status == 'CONFIRMED' and coordinates_verified is True

def measurement_join_allowed(left, right):
    # Conservative equality check; this validator deliberately has no unit converter.
    keys = ('analyte', 'unit', 'matrix', 'fraction', 'basis')
    return all(left.get(k) not in (None, '', 'UNKNOWN') and left.get(k) == right.get(k) for k in keys)

def main():
    candidates = json.loads((ROOT/'whh_candidates.json').read_text(encoding='utf-8'))
    lit = json.loads((ROOT/'literature_register.json').read_text(encoding='utf-8'))
    reuse = json.loads((ROOT/'reuse_manifest.json').read_text(encoding='utf-8'))
    check('candidate and detailed budgets', len(candidates['candidates']) <= 10 and sum(c['depth']=='DETAILED' for c in candidates['candidates']) <= 5)
    check('publication budget and unique ids', len(lit['publications']) <= 18 and len({x['id'] for x in lit['publications']}) == len(lit['publications']))
    check('term-resolution query budgets', all(x['github_queries'] <= 2 for x in reuse['term_resolution'].values()))
    check('independent science/data gates', candidates['gates'] == {'science':'PENDING','real_data':'DATA_NOT_READY','health_inference':'NOT_AUTHORIZED','calculation':'NOT_AUTHORIZED'})
    required = {'id','depth','source_url','owner','licence_status','licence_text_url','access_outcome','temporal_extent','variables_and_format','raw_sha256','sample_count','coordinates','crs','timezone','lod_loq','missing_codes','calibration','disposition'}
    check('candidate structure and no raw/admission claims', all(required <= c.keys() and c['raw_sha256'] is None and c['sample_count'] is None and c['raw_data_downloaded'] is False and c['disposition']=='NO_DATA_ADMITTED' for c in candidates['candidates']))
    check('open-grant assertions have source URL', all(c['licence_text_url'] for c in candidates['candidates'] if c['id'] in ('D03','D05')))
    check('taskbook exact bytes', hashlib.sha256((ROOT/'UNIFIED_CODEX_TASKBOOK.md').read_bytes()).hexdigest()==TASK_SHA)
    check('12 canonical screens', len(re.findall(r'^## \d\d｜', (ROOT/'FOUNDER_ACCEPTANCE_CN.md').read_text(encoding='utf-8'), re.M)) == 12)
    preview = (ROOT/'index.html').read_text(encoding='utf-8')
    check('12 preview screens and local assets only', len(re.findall(r'class="slide"',preview))==12 and not re.search(r'<(?:script|img|link)[^>]+(?:src|href)=["\x27]https?://',preview))
    check('negative: unresolved or reversed COO300 order rejected', not site_label_allowed('CONFLICT_OPEN', True) and not site_label_allowed('REVERSED', True))
    check('negative: unknown geometry rejected', not site_label_allowed('CONFIRMED', False))
    check('control: hypothetical confirmed metadata label accepted', site_label_allowed('CONFIRMED', True))
    a={'analyte':'NO3-','unit':'mg/L','matrix':'water','fraction':'dissolved','basis':'ion_mass'}
    b={**a,'analyte':'NO3-N','basis':'nitrogen_mass'}
    check('negative: NO3- versus NO3-N rejected without conversion', not measurement_join_allowed(a,b))
    check('negative: mg/L versus ug/L rejected without conversion', not measurement_join_allowed(a,{**a,'unit':'ug/L'}))
    check('negative: unknown basis rejected', not measurement_join_allowed({**a,'basis':None},{**a,'basis':None}))
    check('control: identical fully specified measurement metadata accepted', measurement_join_allowed(a, a))
    check('no raw file types in new package', all(p.suffix in {'.md','.json','.py','.html','.cjs'} or p.name in ('.gitattributes','preview-desktop.png','preview-mobile.png') for p in ROOT.rglob('*') if p.is_file()))
    external=set(); internal=[]
    for p in ROOT.glob('*'):
        if p.suffix=='.json':
            json.loads(p.read_text(encoding='utf-8'))
        if p.suffix=='.py':
            ast.parse(p.read_text(encoding='utf-8'))
        if p.suffix not in ('.md','.html'):
            continue
        text=p.read_text(encoding='utf-8')
        links=re.findall(r'\[[^\]]*\]\(([^)]+)\)',text) if p.suffix=='.md' else re.findall(r'href="([^"]+)"',text)
        for link in links:
            url=urlparse(link)
            if url.scheme:
                check_name = None
                if url.scheme not in ('https','http') or not url.netloc:
                    raise AssertionError('invalid URL '+link)
                external.add(link)
            elif not link.startswith('#'):
                target=(p.parent/unquote(url.path)).resolve()
                generated_here = target.parent == ROOT and target.name in ('validation_results.json','artifact_manifest.json')
                internal.append((str(p.name),link,target.exists() or generated_here))
    check('internal links exist', all(x[2] for x in internal))
    check('JSON syntax and Python AST parsed', True)
    frozen=[]
    for f in reuse['files']:
        actual=subprocess.check_output(['git','show',f["commit"]+':'+f['path']],cwd=REPO)
        frozen.append(hashlib.sha256(actual).hexdigest()==f['sha256'])
    check('16 exact existing source blobs unchanged', len(frozen)==16 and all(frozen))
    changed=subprocess.check_output(['git','diff','--name-only',BASE],cwd=REPO,text=True).splitlines()
    untracked=subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=REPO,text=True).splitlines()
    prefix=ROOT.relative_to(REPO).as_posix()+'/'
    check('diff only isolated task package', all(p.startswith(prefix) for p in changed+untracked))
    artifact_manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(ROOT.iterdir()) if p.is_file() and p.name not in ('artifact_manifest.json','validation_results.json')}
    (ROOT/'artifact_manifest.json').write_text(json.dumps(artifact_manifest,indent=2)+'\n',encoding='utf-8',newline='\n')
    result={'status':'LOCAL_METADATA_QA_PASS','run_utc':datetime.now(timezone.utc).isoformat(),'baseline':BASE,'checked_head_before_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),'checks':checks,'counts':{'publications':len(lit['publications']),'portals':len(candidates['candidates']),'detailed':sum(c['depth']=='DETAILED' for c in candidates['candidates']),'internal_link_occurrences':len(internal),'unique_external_urls':len(external),'frozen_blob_checks':len(frozen)},'scientific_runs':0,'raw_files_downloaded':0,'scope_limitation':'Metadata QA, not source-server availability, independent scientific validation, or an exhaustive audit of host network history','ci':'NOT_TRIGGERED_UNTIL_SEPARATELY_VERIFIED_REMOTE'}
    (ROOT/'validation_results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    assert (ROOT/'artifact_manifest.json').is_file() and (ROOT/'validation_results.json').is_file()
    print(json.dumps({'status':result['status'],'checks_passed':len(checks),'counts':result['counts']},ensure_ascii=False))

if __name__ == '__main__':
    main()
