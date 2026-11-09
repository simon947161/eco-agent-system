"""Check hashes, registry/graph references, local links and deterministic replay."""
from pathlib import Path
import hashlib
import json
import re
import sys
TASK=Path(__file__).resolve().parent
ROOT=TASK.parents[2]
sys.path.insert(0,str(ROOT))
from cczps_lite.integration import methane_knowledge_engine as m


def main():
    manifest=json.loads((TASK/'evidence/manifest.json').read_text(encoding='utf-8'))
    for item in manifest['files']:
        path=ROOT/item['path']
        assert path.resolve().is_relative_to(ROOT.resolve())
        assert hashlib.sha256(path.read_bytes().replace(b'\r\n',b'\n')).hexdigest()==item['sha256'],item['path']
    registry=json.loads((TASK/'EQUATION_REGISTRY.json').read_text(encoding='utf-8'))
    graph=json.loads((TASK/'MECHANISM_GRAPH.json').read_text(encoding='utf-8'))
    sources={x['source_id'] for x in json.loads((TASK/'sources.json').read_text(encoding='utf-8'))}
    factors={x['factor_id'] for x in graph['factors']}
    ids=factors|set(graph['equation_nodes'])
    for node in registry['equations']:
        assert set(node['source_id'])<=sources
        assert node['factor_id'] and set(node['factor_id'])<=factors
        assert set(node['dependencies'])<=set(graph['equation_nodes'])
    assert all(e['from'] in ids and e['to'] in ids for e in graph['edges'])
    links=0
    for path in TASK.glob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)',path.read_text(encoding='utf-8')):
            if '://' in target or target.startswith(('repository:','#')):continue
            assert (path.parent/target.split('#')[0]).exists(),(path.name,target)
            links+=1
    result=m.execute(json.loads((TASK/'input.json').read_text(encoding='utf-8')))
    assert result==json.loads((TASK/'evidence/chain-a.json').read_text(encoding='utf-8'))
    print(json.dumps({'status':'PASS','hashes':len(manifest['files']),'equation_nodes':len(registry['equations']),
                      'factor_nodes':len(factors),'local_links':links,'replay':'MATCH'}))


if __name__=='__main__':main()
