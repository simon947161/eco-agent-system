"""Read-only evidence index adapter for CCZPS; no GIS overlay or climate solver.

This task-local research contract does not replace Public Strategy Atlas atlas-domain-1.
All external content is inert JSON. Numeric scores never enter the scenario engine.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from collections import deque
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TASK = ROOT/'docs/tasks/global_natural_systems_evidence_atlas_001'
DATA_FILES = ('GLOBAL_COVERAGE_REGISTER.json','RELATION_GRAPH.json','EVIDENCE.json','SOURCES.json','POLICIES.json','BUDGET.json')
EVIDENCE_TYPES = {'PHYSICAL_OBSERVATION','DERIVED_DATA','MODEL_OUTPUT','SCIENTIFIC_LITERATURE','LEGAL_METHOD',
                  'POLICY_COMMITMENT','POLICY_ASSESSMENT','ECOLOGICAL_OUTCOME','GOVERNANCE_DECISION','SYNTHETIC_TEST'}
EDGE_TYPES = {'PHYSICAL_TRANSPORT','BIOGEOCHEMICAL_CYCLE','ECOLOGICAL_DEPENDENCY','CLIMATE_TELECONNECTION',
              'SUPPLY_CHAIN_FLOW','EMISSION_RESPONSIBILITY','EXPOSURE_VULNERABILITY','POLICY_DEPENDENCY','OBSERVATION_SUPPORT','HYPOTHESIS_ONLY'}
STATES = {'SOURCE_VERIFIED','RECALCULATED','EVIDENCE_INSUFFICIENT','MATERIAL_CONTRADICTION','NOT_ASSESSED','BLOCKED'}
FIELDS = {'claim_id','evidence_type','source_id','version','source_locator','claim','rights','sha_if_downloaded',
          'geographic_support','time_support','method_id','unit','value','uncertainty','calibration_QA','review_state',
          'contradictions','not_inferable_from','origin'}

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def sha(path):
    return hashlib.sha256(path.read_bytes().replace(b'\r\n',b'\n')).hexdigest()

def verify_manifest(directory=TASK):
    manifest = read(directory/'evidence/manifest.json')
    for relative, expected in manifest['files'].items():
        path = (ROOT/relative).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file() or sha(path) != expected:
            raise ValueError('HASH_OR_PATH_MISMATCH:'+relative)
    # Trust is this reviewed Git tree, not an external signature or institutional endorsement.
    return len(manifest['files'])

def load_atlas(directory=TASK, verify=True):
    if verify: verify_manifest(directory)
    result = dict(zip(('coverage','graph','evidence','sources','policies','budget'),[read(directory/n) for n in DATA_FILES]))
    validate(result, directory)
    return result

def unique(items, key):
    values = [r[key] for r in items]
    if len(values) != len(set(values)): raise ValueError('DUPLICATE_ID:'+key)
    return {r[key]:r for r in items}

def timestamp(text):
    value=datetime.fromisoformat(text.replace('Z','+00:00'))
    if value.tzinfo is None: raise ValueError('TIMEZONE_REQUIRED')
    return value

def validate(data, directory=TASK):
    def require(ok, message):
        if not ok: raise ValueError(message)
    coverage, graph = data['coverage'], data['graph']
    countries=unique(coverage['countries'],'id'); units=unique(graph['units'],'id')
    sources=unique(data['sources'],'source_id'); evidence=unique(data['evidence'],'claim_id')
    policies=unique(data['policies'],'id'); edges=unique(graph['edges'],'id')
    facts=read(directory/'evidence/m49-facts.json')
    require(set(countries)=={'M49:'+r['M49 Code'] for r in facts['rows']},'GLOBAL_COVERAGE_MISMATCH')
    require(coverage['count']==len(countries)==len(facts['rows']),'COVERAGE_COUNT')
    for row in facts['rows']:
        c=countries['M49:'+row['M49 Code']]
        require((c['name'],c['iso2'],c['iso3'])==(row['Country or Area'],row['ISO-alpha2 Code'],row['ISO-alpha3 Code']),'M49_IDENTITY_CHANGED')
        require(c['science_status']=='PENDING','SCIENTIFIC_PROMOTION')
    require(len(data['policies'])<=12,'CASE_BUDGET')
    require(set(graph['paths'])=={'nile_flow','enso','methane'},'MECHANISM_BUDGET')
    require(len({s['theme_id'] for s in data['sources'] if s['theme_id']!='INHERITED'})<=15,'SOURCE_BUDGET')
    for key,limit in data['budget']['limits'].items(): require(data['budget'][key]<=limit,'BUDGET:'+key)
    for row in list(countries.values())+list(units.values()):
        require(row['source'] in sources,'UNKNOWN_UNIT_SOURCE')
        require(row['geometry_ref'] is None and row['CRS']=='NOT_APPLICABLE_NO_GEOMETRY','UNADMITTED_GEOMETRY_OR_CRS')
        require(row['license']==sources[row['source']]['rights'],'UNIT_RIGHTS_MISMATCH')
    require(coverage['geometry_acquired_count']==coverage['geometry_coverage_fraction']==0,'FABRICATED_GEOMETRY_COVERAGE')
    for s in sources.values():
        require(bool(s['rights']) and s['rights'] not in ('OPEN_ASSUMED','UNKNOWN_OPEN'),'LICENCE_REQUIRED')
        require(s['raw_redistributed'] is False,'UNAPPROVED_RAW_REDISTRIBUTION')
        require(s['review_state'] in STATES,'SOURCE_STATE')
    for link in graph['country_links']:
        require(link['country_id'] in countries and link['unit_id'] in units,'DANGLING_COUNTRY_UNIT')
        require(link['fraction'] is None and link['relation']=='RESEARCH_CONTEXT_NOT_GEOMETRIC_OVERLAY','UNVERIFIED_SPATIAL_OVERLAY')
    scorefacts={r['name']:r for r in read(directory/'evidence/scorecard-facts.json')['records']}
    for p in policies.values():
        require(p['country_id'] in countries and p['source_id'] in sources,'DANGLING_POLICY')
        if p['type']=='COUNTRY_POLICY_SCORE':
            expected=scorefacts.get(p['display_name'])
            require(expected is not None and p['source_id']=='SCORE' and p['source_fact']==expected,'SCORE_PROVENANCE')
            require(p['score']==expected['published_percent_label'],'FABRICATED_SCORE')
            require(p['unit']=='published_policy_percent_label' and p['evidence_type']=='POLICY_ASSESSMENT','POLICY_AS_PHYSICS')
            require(p['valid_time']=='UNKNOWN','FALSE_POLICY_VALIDITY')
        else:
            require(p['type']=='POLICY_COMMITMENT' and p['score'] is None,'SCORE_WITHOUT_COVERAGE')
    for e in evidence.values():
        require(set(e)==FIELDS,'EVIDENCE_FIELDS')
        require(e['evidence_type'] in EVIDENCE_TYPES and e['review_state'] in STATES,'EVIDENCE_ENUM')
        require(e['source_id'] in sources,'DANGLING_EVIDENCE_SOURCE')
        s=sources[e['source_id']]
        require(e['rights']==s['rights'] and e['version']==s['version'],'RIGHTS_OR_VERSION_MISMATCH')
        require(e['sha_if_downloaded']==s['sha_if_downloaded'],'PROVENANCE_HASH_MISMATCH')
        require(e['value'] is None,'NUMERIC_PAYLOAD_NOT_ADMITTED_THIS_BATCH')
        require(all(n in units or n in countries for n in e['geographic_support']),'EVIDENCE_GEOGRAPHY')
        if e['evidence_type']=='SYNTHETIC_TEST': require(e['origin']=='SYNTHETIC','SYNTHETIC_AS_REAL')
        if e['source_id'] in ('SCORE','NDC','SC_AU_REPORT'):
            require(e['evidence_type'] in ('POLICY_ASSESSMENT','POLICY_COMMITMENT'),'POLICY_AS_OBSERVATION')
            require(e['unit'] in ('published_policy_percent_label','not_applicable'),'POLICY_UNIT')
        if e['claim_id']=='OUTCOME_GAP': require(e['review_state']=='EVIDENCE_INSUFFICIENT','UNVERIFIED_OUTCOME_PROMOTION')
        if e['claim_id']=='BRW_EXISTING':
            require(e['unit']=='nmol mol-1' and e['origin']=='INHERITED_OBSERVATION','OBSERVATION_UNIT_OR_ORIGIN')
        expected_units={'GML_GLOBAL':'nmol mol-1','AGGI_METHOD':'W m-2','INTERNAL_REPLAY':'kg_CH4/interval'}
        if e['claim_id'] in expected_units: require(e['unit']==expected_units[e['claim_id']],'UNIT_BOUNDARY_MISMATCH')
        if e['claim_id']=='AU_TARGET': require(e['method_id']=='AU/C2025C00153/s10','WRONG_JURISDICTION_VERSION')
        t=e['time_support']
        if t['start'] is not None:
            require(t['end'] is not None and t['timezone']=='UTC','TIME_WINDOW_OR_ZONE')
            require(timestamp(t['end'])>timestamp(t['start']),'TIME_ORDER')
            require(timestamp(t['start']).utcoffset().total_seconds()==0 and timestamp(t['end']).utcoffset().total_seconds()==0,'UTC_OFFSET_CONFLICT')
        else: require(t['end'] is None and t['timezone']=='UNKNOWN','FABRICATED_TIME_SUPPORT')
    require(EVIDENCE_TYPES <= {e['evidence_type'] for e in evidence.values()},'MISSING_EVIDENCE_CLASS')
    expected_direction={'N1':('BLUE_UPPER','BLUE_LOWER'),'N2':('BLUE_LOWER','MAIN_NILE')}
    for edge in edges.values():
        require(edge['from_id'] in units and edge['to_id'] in units,'DANGLING_EDGE')
        require(edge['type'] in EDGE_TYPES and edge['direction']=='from_to','EDGE_TYPE_DIRECTION')
        require(edge['evidence_ids'] and all(e in evidence for e in edge['evidence_ids']),'MISSING_EDGE_EVIDENCE')
        require(edge['numeric_weight'] is None and edge['unit']=='not_applicable_qualitative','UNADMITTED_COEFFICIENT')
        require(edge['counterevidence'] and edge['assumptions'] and edge['applicability'],'MISSING_CAUSAL_LIMITS')
        if edge['id'] in expected_direction:
            require((edge['from_id'],edge['to_id'])==expected_direction[edge['id']],'RIVER_DIRECTION_REVERSED')
        if edge['type']=='CLIMATE_TELECONNECTION':
            require(edge['causality'] in ('COUPLED_MECHANISM','CONDITIONAL_ASSOCIATION'),'FALSE_DETERMINISTIC_CAUSALITY')
        if edge['type']=='HYPOTHESIS_ONLY': require(edge['causality']=='NOT_VALIDATED_HERE','HYPOTHESIS_AS_CAUSE')
        if edge['type'] in ('PHYSICAL_TRANSPORT','BIOGEOCHEMICAL_CYCLE','CLIMATE_TELECONNECTION'):
            require(all(evidence[i]['evidence_type'] not in ('POLICY_COMMITMENT','POLICY_ASSESSMENT') for i in edge['evidence_ids']),'POLICY_USED_AS_PHYSICAL_SUPPORT')
    for process, path in graph['paths'].items():
        require(all(e in edges and edges[e]['process']==process for e in path),'PATH_REFERENCE')
        require(all(edges[a]['to_id']==edges[b]['from_id'] for a,b in zip(path,path[1:])),'DISCONNECTED_PATH')
    return {'status':'LOCAL_VERIFIED','countries':len(countries),'units':len(units),'edges':len(edges),
            'evidence_records':len(evidence),'deep_cases':len(policies),'geometry_coverage_fraction':0,'scientific_admission':'PENDING'}

def query(data, *, country=None, system=None, process=None, at=None, evidence_type=None, text=None):
    """AND filters; time matches known observation support only, never retrieval date."""
    graph=data['graph']; units={u['id']:u for u in graph['units']}
    selected=set(units)
    country_ids=[]
    if country:
        match=[c for c in data['coverage']['countries'] if country.casefold() in {c['id'].casefold(),c['m49'],c['iso2'].casefold(),c['iso3'].casefold(),c['name'].casefold()}]
        country_ids=[c['id'] for c in match]
        selected &= {l['unit_id'] for l in graph['country_links'] if l['country_id'] in country_ids}
    if system: selected &= {u['id'] for u in units.values() if u['system']==system or u['id']==system}
    if process:
        selected &= {e[k] for e in graph['edges'] if e['process']==process for k in ('from_id','to_id')}
    if not country:
        country_ids = sorted({l['country_id'] for l in graph['country_links'] if l['unit_id'] in selected}) if (system or process) else [c['id'] for c in data['coverage']['countries']]
    elif system or process:
        linked = {l['country_id'] for l in graph['country_links'] if l['unit_id'] in selected}
        country_ids = [c for c in country_ids if c in linked]
    # With a country filter, unlinked global science is not silently assigned to it.
    ev=[]; when=timestamp(at) if at else None
    for e in data['evidence']:
        if not (set(e['geographic_support']) & (selected | set(country_ids))): continue
        if evidence_type and e['evidence_type']!=evidence_type: continue
        if text and text.casefold() not in json.dumps(e,ensure_ascii=False).casefold(): continue
        t=e['time_support']
        if when and (not t['start'] or not timestamp(t['start'])<=when<timestamp(t['end'])): continue
        ev.append(e)
    evid={e['claim_id'] for e in ev}
    edge_results=[e for e in graph['edges'] if (e['from_id'] in selected or e['to_id'] in selected)
                  and (not process or e['process']==process) and evid.intersection(e['evidence_ids'])]
    policy_results=[p for p in data['policies'] if (not country or p['country_id'] in country_ids)
                    and ('EV:'+p['id']) in evid]
    sourceids={e['source_id'] for e in ev}|{p['source_id'] for p in policy_results}
    return {'scope':'METADATA_AND_QUALITATIVE_LINKS; no geometry overlay','country_ids':country_ids,
      'units':[units[u] for u in sorted(selected)],'relations':edge_results,'evidence':ev,'policies':policy_results,
      'sources':[s for s in data['sources'] if s['source_id'] in sourceids],
      'unknown':['Unmatched or unknown time records are excluded from time-filtered results','No causal magnitude, admitted emissions or scientific promotion'],
      'scientific_admission':'PENDING'}

def trace(data, start, end):
    """Directed breadth-first search returning typed edges, not an influence score."""
    ids={u['id'] for u in data['graph']['units']}
    if start not in ids or end not in ids: raise ValueError('UNKNOWN_NODE')
    queue=deque([(start,[])]); seen={start}
    while queue:
        node,path=queue.popleft()
        if node==end: return path
        for edge in data['graph']['edges']:
            if edge['from_id']==node and edge['to_id'] not in seen:
                seen.add(edge['to_id']); queue.append((edge['to_id'],path+[edge]))
    return []

def end_to_end(data):
    from cczps_lite.engine.scenario_comparison import build_scenario_comparison
    physical=query(data,country='AU',process='methane')
    policy=query(data,country='AU',evidence_type='POLICY_ASSESSMENT')
    # Truthy explicit empty evidence prevents fallback to ambient local output files.
    scenarios=build_scenario_comparison({'traceability':{'records':[]}})
    base=ROOT/'docs/tasks/climateos_global_method_evidence_ecochain_001'
    spec=importlib.util.spec_from_file_location('atlas_frozen_reviewer',base/'reviewer.py')
    reviewer=importlib.util.module_from_spec(spec); spec.loader.exec_module(reviewer)
    results={}
    for name in ('A','B','C'):
        out=reviewer.review(read(base/'examples'/f'{name}.json'))
        out['arithmetic_interpretation']='INTERNAL_FIXTURE_REPLAY_ONLY'
        out['external_trust_anchor']='ABSENT_ROLE_FIXTURES_IN_SAME_GIT_TREE'
        results[name]=out
    return {'process':'methane','physical_evidence_ids':[e['claim_id'] for e in physical['evidence']],
      'policy_context':policy['policies'],'policy_sent_to_model':False,
      'scenario_interface':scenarios,'scenario_link':'Batlow is configured AU comparison context only; no new methane scenario implemented',
      'interface_mapping':{'natural_unit_id':'CH4_SOURCE','country_id':'M49:036','policy_id':'POLICY:036',
        'cczps_scenario_id':'batlow','technical_review_packages':['A','B','C'],
        'link_status':'SYNTHETIC_INTERFACE_REHEARSAL_ONLY_NOT_BATLOW_PHYSICS',
        'physical_source_ids':['PR143'],'review_source_id':'PR145','policy_source_id':'SCORE'},
      'review_results':results,'ecochain':'ECOCHAIN_CANONICAL_NOT_FOUND','enotebook':'PENDING_INTEGRATION',
      'scientific_admission':'PENDING','human_decision':'PENDING','deployed':False,
      'not_inferable':'Synthetic ledger review does not validate Batlow, Scorecard, physical effects or real roles'}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['validate','query','trace','e2e'])
    for arg in ('country','system','process','at','evidence-type','text','start','end'): parser.add_argument('--'+arg)
    args=parser.parse_args(); data=load_atlas()
    if args.action=='validate': result=validate(data)
    elif args.action=='e2e': result=end_to_end(data)
    elif args.action=='trace': result=trace(data,args.start,args.end)
    else: result=query(data,**{k:getattr(args,k) for k in ('country','system','process','at','evidence_type','text')})
    print(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False))

if __name__=='__main__': main()
