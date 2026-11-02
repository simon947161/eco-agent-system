#!/usr/bin/env python3
"""After all browser processes finish, retain verified large exports outside Git."""
import datetime,hashlib,json,shutil
from pathlib import Path
HERE=Path(__file__).resolve().parent;APP=HERE.parents[2]
DEST=Path('/tmp/csoi-closure-exports-20261102')
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()
report=json.loads((HERE/'browser-results.json').read_text())
assert len(report['results'])==4 and all(r['status']=='PASS_ACTUALLY_TESTED' for r in report['results'])
assert json.loads((HERE/'browser/linear-accessibility/results.json').read_text())['status']=='PASS_BOUNDED_BROWSER_CHECKS'
rows=[]
for p in sorted((HERE/'browser').rglob('*.json')):
    if p.stat().st_size<=1024*1024:continue
    assert 'snapshot' in p.name or p.name.startswith('atlas-discovery-'),p
    relative=p.relative_to(HERE);target=DEST/relative;target.parent.mkdir(parents=True,exist_ok=True)
    payload=json.loads(p.read_text());assert payload['format']=='atlas-public-snapshot-1'
    size=p.stat().st_size;digest=sha(p);width=1440 if '1440' in p.name else 390
    log=p.parent/'execution.log';logtext=log.read_text()
    if 'paths' in p.parent.name:
        expected='"integrity":true,"current":true'
        assert logtext.count(expected)>=(1 if width==1440 else 2)
        result={'verifier':'verify-paths.cjs','result':{'integrity':True,'current':True,'officialUse':'REJECTED_UNKNOWN_ADMISSION'},'proof':str((p.parent/f'csoi-path-proof-{width}.json').relative_to(HERE))}
    else:
        expected='PASS: dataset, linked history and content-root receipts match.'
        assert logtext.count(expected)>=(1 if width==1440 else 2)
        result={'verifier':'verify-snapshot.cjs','result':'PASS_DATASET_LINKED_HISTORY_CONTENT_ROOT_RECEIPTS'}
    if target.exists():assert sha(target)==digest,('Existing different archive',target)
    shutil.move(str(p),str(target));assert sha(target)==digest and target.stat().st_size==size
    rows.append({'originalRelativePath':str(relative),'bytes':size,'sha256':digest,'newLocalPath':str(target),'datasetEntities':len(payload['dataset']['domain']['entities']),'offlineVerification':{**result,'status':'PASS_ACTUALLY_EXECUTED_BY_BROWSER_SUITE','evidenceLog':str(log.relative_to(HERE)),'evidenceLogSHA256':sha(log),'verificationScope':'Exact exported snapshot; signature/legal truth/official authority not established.'},'moveDigestMatched':True,'committedToGit':False})
receipt={'format':'csoi-large-browser-export-archive-1','at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'movedAfterBrowserProcessCompleted':True,'files':rows,'fileCount':len(rows),'totalBytes':sum(x['bytes'] for x in rows),'reason':'Preserve regenerable public/synthetic whole-history exports locally without committing five duplicate histories to Git. Proofs, smaller JSON, logs and screenshots remain in QA.','newOfflineVerificationExecutedDuringMove':False,'verificationBasis':'Retained actual CLI results from the completed browser suites, associated by exact viewport/output file and suite iteration order; file SHA and byte count rechecked during move.'}
(HERE/'large-export-receipts.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'fileCount':receipt['fileCount'],'totalBytes':receipt['totalBytes'],'allMovesHashMatched':all(x['moveDigestMatched'] for x in rows)},ensure_ascii=False))
