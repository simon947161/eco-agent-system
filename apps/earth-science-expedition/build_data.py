"""One reproducible source bundle for the offline learning UI; no downloads."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[2]
DOC=ROOT/'docs/research/world-science-expedition'
APP=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def bundle():
    parts=[read(p) for p in sorted((DOC/'research_parts').glob('*.json'))]
    sources=[s for p in parts for s in p['sources']]
    stations=[s for p in parts for s in p['stations']]
    claims=[dict(c,revision=1,checked_at='2026-11-11',supersedes=None) for p in parts for c in p['claims']]
    for s in sources:s.setdefault('last_checked',s['access_date'])
    order=['wesr','geo','wis2','ecmwf','esmf','bmi'];stations.sort(key=lambda s:order.index(s['id']))
    assert len(sources)<=25 and len(stations)==6
    assert len({s['id'] for s in sources})==len(sources)
    assert len({s['canonical_url'] for s in sources})==len(sources)
    ids={s['id'] for s in sources}
    for s in stations:assert set(s['source_ids'])<=ids
    for c in claims:assert set(c['source_ids'])<=ids
    docs={name:(DOC/name).read_text(encoding='utf-8') for name in [
        'FOUNDER_VISION_AND_DIALOGUE_20261111_ZH.md','FOUNDER_LEARNING_NOTES_ZH.md',
        'MECHANISM_COMPARISONS.md','RESEARCH_QUESTIONS.md','RIGHTS_AND_ACCESS.md',
        'CRP_HANDOFF.md','NEXT_SESSION.md','RECOVERY_AND_BASELINE.md',
        'research_parts/un_wmo.md','research_parts/interfaces.md']}
    return {'version':'expedition/1.0','checked_at':'2026-11-11','science':'PENDING',
            'sources':sources,'stations':stations,'claims':claims,'routes':read(DOC/'LEARNING_ROUTES.json'),
            'experiment':read(DOC/'evidence/interface-results.json'),'documents':docs,
            'revisions':[{'id':'v1','date':'2026-11-11','status':'SOURCE_READ / TECHNICALLY_TESTED_SUBSET',
                'change':'从统一函数名即相容，修订为审查库存提交语义。云端旧工件不可恢复，本轮重建并留痕。','counterevidence':'单端口时钟推进但库存未提交的实际反例。'}]}
if __name__=='__main__':
    d=bundle();write(DOC/'SOURCE_REGISTER.json',d['sources']);write(DOC/'CLAIM_LEDGER.json',d['claims']);write(DOC/'STATION_REGISTER.json',d['stations'])
    payload=json.dumps(d,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
    (APP/'data.js').write_text('window.EXPEDITION_DATA = '+payload+';\n',encoding='utf-8')
    print(f"{len(d['stations'])} stations / {len(d['sources'])} source targets / {len(d['claims'])} claims")
