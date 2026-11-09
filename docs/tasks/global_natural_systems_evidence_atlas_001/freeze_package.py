"""Author-only manifest/schema freeze; no promotion or external trusted anchor."""
import json
import importlib.util
from pathlib import Path
import sys
T=Path(__file__).resolve().parent
ROOT=T.parents[2]
sys.path.insert(0,str(ROOT))
from cczps_lite.integration import global_natural_systems_atlas as atlas

def dump(name,value):
    (T/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')

def record_schema(record, enums=None):
    enums=enums or {}
    types={str:'string',list:'array',dict:'object',int:'integer',float:'number',bool:'boolean',type(None):'null'}
    properties={k:{'type':types[type(v)]} for k,v in record.items()}
    for k,vals in enums.items(): properties[k]={'enum':sorted(vals)}
    return {'type':'object','additionalProperties':False,'required':sorted(record),'properties':properties}

def main():
    data=atlas.load_atlas(verify=False)
    spec=importlib.util.spec_from_file_location('atlas_validation_author',T/'run_validation.py')
    replay=importlib.util.module_from_spec(spec);spec.loader.exec_module(replay)
    (T/'evidence/query-results.json').write_text(json.dumps(replay.snapshot(data),ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+'\n',encoding='utf-8',newline='\n')
    evidence=record_schema(data['evidence'][0],{'evidence_type':atlas.EVIDENCE_TYPES,'review_state':atlas.STATES})
    evidence['properties']['sha_if_downloaded']={'type':['string','null'],'pattern':'^[a-f0-9]{64}$'}
    evidence['properties']['time_support']={'type':'object','additionalProperties':False,
      'required':['start','end','timezone','semantics'],'properties':{'start':{'type':['string','null']},'end':{'type':['string','null']},'timezone':{'type':'string'},'semantics':{'type':'string'}}}
    dump('EVIDENCE_SCHEMA.json',{'$schema':'https://json-schema.org/draft/2020-12/schema','$id':'urn:climateos:atlas-research-1:evidence',
      'description':'Task-local additive research projection. Semantic checks in CCZPS adapter; not replacing Evidence Passport.', 'type':'array','items':evidence})
    graph=data['graph']
    dump('RELATION_SCHEMA.json',{'$schema':'https://json-schema.org/draft/2020-12/schema','$id':'urn:climateos:atlas-research-1:graph',
      'type':'object','required':['schema_version','units','country_links','edges','paths'],'additionalProperties':False,
      'properties':{'schema_version':{'const':graph['schema_version']},'units':{'type':'array','items':record_schema(graph['units'][0])},
       'country_links':{'type':'array','items':record_schema(graph['country_links'][0])},
       'edges':{'type':'array','items':record_schema(graph['edges'][0],{'type':atlas.EDGE_TYPES})},'paths':{'type':'object'}}})
    excluded={'manifest.json','tests.txt','validation.json','REVIEW_REQUEST.json','HANDOFF_STATUS.json'}
    files=[p for p in T.rglob('*') if p.is_file() and p.suffix in ('.md','.json','.py','.txt') and p.name not in excluded and '__pycache__' not in p.parts]
    files += [ROOT/'cczps_lite/integration/global_natural_systems_atlas.py',ROOT/'tests/test_global_natural_systems_atlas.py',
      ROOT/'cczps_lite/engine/scenario_comparison.py',ROOT/'cczps_lite/integration/methane_knowledge_engine.py',
      T.parent/'climateos_au_landfill_methane_methods_001/mass_balance.py']
    old=T.parent/'climateos_global_method_evidence_ecochain_001'
    files += [old/'reviewer.py',old/'CLAIM_EVIDENCE_SCHEMA.json',old/'evidence/trusted-registry.json',*sorted((old/'examples').glob('*.json'))]
    for source in data['sources']:
        if source['theme_id']=='INHERITED': files.append(ROOT/source['locator'])
    dump('evidence/manifest.json',{'hash_basis':'UTF-8/text LF-normalized SHA256; raw HTTP byte hashes in acquisition.json',
       'trust_boundary':'Reviewed Git tree only; not signed externally. R/D metadata and mutable execution logs excluded.',
       'files':{p.relative_to(ROOT).as_posix():atlas.sha(p) for p in sorted(set(files))}})
    print('Frozen',atlas.verify_manifest(),'file hashes')

if __name__=='__main__': main()
