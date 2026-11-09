"""Local links, required artifacts, scope and accidental secret-pattern checks."""
from pathlib import Path
import json,re
T=Path(__file__).resolve().parent; ROOT=T.parents[2]
required='TASKBOOK_ZH README FOUNDER_REPORT_ZH TRAJECTORY_METHOD_AND_SCHEMA TRAJECTORY_CH4 TRAJECTORY_ENSO TRAJECTORY_HYDROLOGY CROSS_PROCESS_CAUSAL_MATRIX COUNTEREVIDENCE_REGISTER OPEN_DATA_AND_SOURCE_REGISTER QUANTITATIVE_RECALC_RESULTS MODEL_GAPS_AND_NEXT_INPUTS SCORECARD_AU_CORRECTION_BRIEF_ZH EDITOR_NOTE_EN_DRAFT CCZPS_ECOCHAIN_HANDOFF QA_AND_VALIDATION NEXT_SESSION CRP_HANDOFF'.split()
links=0
for name in required: assert (T/(name+'.md')).is_file(), name
for p in T.glob('*.md'):
    text=p.read_text(encoding='utf-8')
    for rel in re.findall(r'\]\(([^)]+)\)',text):
        if re.match(r'https?://|#',rel): continue
        target=(p.parent/rel.split('#')[0]).resolve()
        assert target.is_relative_to(ROOT) and target.is_file(),(p.name,rel)
        links+=1
files=[p for p in T.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
for p in files:
    assert p.suffix.lower() not in ('.sqlite','.sqlite3','.db','.html','.raw','.pem','.key'),p.name
    if p.name=='check_content.py': continue
    value=p.read_text(encoding='utf-8-sig')
    assert not re.search(r'gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----|AKIA[A-Z0-9]{16}',value),p.name
sources=json.loads((T/'SOURCES.json').read_text(encoding='utf-8'))
themes={s['theme'] for s in sources if s['theme']!='INHERITED'}
assert len(themes)<=12
data=json.loads((T/'TRAJECTORIES.json').read_text(encoding='utf-8'))
assert len(data)==14 and {x['PROCESS_ID'] for x in data}=={'CH4','ENSO','HYDRO'}
sourceids={s['id'] for s in sources}; ce={'CE'+str(i).zfill(2) for i in range(1,13)}
cross=json.loads((T/'CROSS_RELATIONS.json').read_text(encoding='utf-8'))
assert len(cross)==9 and len({(c['from'],c['to']) for c in cross})==9
for row in cross:
    assert set(row['sources'])<=sourceids and set(row['counterevidence'])<=ce
    assert row['numeric_coefficient'] is None
for row in data: assert set(row['counterevidence'])<=ce
report={'required_markdown':len(required),'local_links_checked':links,'source_records':len(sources),
    'new_source_themes':len(themes),'segments':len(data),'cross_relations':len(cross),
    'forbidden_artifact_or_obvious_secret_pattern_matches':0,'note':'Pattern scan is not a guarantee; publication set also manually reviewed'}
(T/'evidence/content-checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
print(report)
