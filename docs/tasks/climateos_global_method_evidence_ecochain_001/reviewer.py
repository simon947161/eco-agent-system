"""Offline technical-review proposal. No certification, network or field solver.

Trusted files belong to the reviewed Git tree, never to the submitting package.
They are not signatures or a production identity/access-control system.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import math
import sys

T = Path(__file__).resolve().parent
ROOT = T.parents[2]
sys.path.insert(0, str(ROOT))
from cczps_lite.integration import methane_knowledge_engine as core

SPEC = importlib.util.spec_from_file_location('frozen_ledger', T.parent/'climateos_au_landfill_methane_methods_001/mass_balance.py')
ledger = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ledger)
VERSION = 'technical-review-proposal/1'

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')

def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()

def load(name):
    return json.loads((T/name).read_text(encoding='utf-8'))

def schema_check(value, schema, path='$'):
    """Deliberately closed subset of JSON Schema used by the published contract."""
    typ = schema['type']
    types = {'object':dict, 'array':list, 'string':str, 'boolean':bool, 'number':(float,int)}
    if not isinstance(value, types[typ]) or (typ=='number' and (isinstance(value,bool) or not math.isfinite(value))):
        raise ValueError('SCHEMA_TYPE:'+path)
    if typ=='object':
        if set(value)!=set(schema['required']): raise ValueError('SCHEMA_FIELDS:'+path)
        for k,v in value.items(): schema_check(v,schema['properties'][k],path+'.'+k)
    elif typ=='array':
        if len(value)<schema.get('minItems',0): raise ValueError('SCHEMA_EMPTY:'+path)
        for i,v in enumerate(value): schema_check(v,schema['items'],path+f'[{i}]')
    elif typ=='string' and not value:
        raise ValueError('SCHEMA_EMPTY:'+path)

def check_sources(package):
    registry=load('evidence/trusted-registry.json')
    problems=[]
    for source in package['SOURCE_LICENCE']:
        entry=registry['sources'].get(source['evidence_id'])
        if not entry:
            problems.append(('EVIDENCE_INSUFFICIENT','SOURCE_NOT_REGISTERED',source['evidence_id']))
            continue
        if source['sha256']!=entry['sha256'] or digest(source['payload'])!=entry['sha256']:
            problems.append(('MATERIAL_CONTRADICTION','HASH_TAMPER',source['evidence_id']))
        if source['origin']!=entry['origin'] or source['payload']['origin']!=entry['origin']:
            problems.append(('MATERIAL_CONTRADICTION','SYNTHETIC_AS_REAL',source['evidence_id']))
        if source['licence']!=entry['licence']:
            problems.append(('EVIDENCE_INSUFFICIENT','LICENCE_UNVERIFIED',source['evidence_id']))
    return registry,problems

def review(package):
    """Separate method, arithmetic, evidence and governance outcomes per claim."""
    result={'rules_version':VERSION,'package_sha256':None,'claims':[],
            'REGULATORY_CERTIFICATION':'NOT_PROVIDED','effect':'NOT_ASSESSED',
            'human_review':'PENDING','reviewer':'OFFLINE_RULE_ENGINE; role fixtures only'}
    try:
        schema_check(package,load('CLAIM_EVIDENCE_SCHEMA.json'))
        result['package_sha256']=digest(package)
    except (ValueError,TypeError) as exc:
        result.update(status='MATERIAL_CONTRADICTION',failures=[str(exc)])
        return result
    registry,common=check_sources(package)
    def flag(state,reason,pointer): common.append((state,reason,pointer))
    if package['schema_version']!='claim-evidence-proposal/1': flag('MATERIAL_CONTRADICTION','SCHEMA_VERSION','schema_version')
    data=package['DATA']; method=package['METHOD']; calc=package['CALCULATION']; role=package['REVIEW']
    expected_method={'id':ledger.VERSION,'jurisdiction':'AUTHOR_SYNTHETIC_ONLY','version':'1','reporting_year':'SYNTHETIC_NOT_A_REPORTING_YEAR','formula_id':'FOUR_INTERFACE_CH4_C_LEDGER'}
    aligned=method==expected_method
    if not aligned: flag('MATERIAL_CONTRADICTION','JURISDICTION_VERSION_REPORTING_YEAR','METHOD')
    expected_data={'gas':'CH4','phase':'total_CH4_gas_plus_dissolved','unit':'kg_CH4/interval',
        'wet_dry':'NOT_APPLICABLE_INTEGRATED_MASS','volume_reference':'NOT_APPLICABLE_MASS',
        'time_window':'SYNTHETIC_DAY_001','timezone':'SYNTHETIC_NO_CIVIL_TIME',
        'spatial_boundary':'SYNTHETIC_BODY_PIPE_DEVICE_COVER;LATERAL_UNKNOWN',
        'crs':'NOT_APPLICABLE_SYNTHETIC','coordinates':'NOT_A_REAL_SITE',
        'instrument':'SYNTHETIC_NOT_FIELD','calibration':'SYNTHETIC_NOT_FIELD',
        'uncertainty':'EXACT_ARITHMETIC_FIXTURE_NOT_FIELD_UNCERTAINTY',
        'raw_flow_evidence':'SYNTHETIC_FIXTURE_ONLY','missing_policy':'REJECT_UNKNOWN_NO_IMPUTATION'}
    for key,expected in expected_data.items():
        if data[key]!=expected:
            state='EVIDENCE_INSUFFICIENT' if data[key]=='UNKNOWN' else 'MATERIAL_CONTRADICTION'
            flag(state,'DATA_'+key.upper(), 'DATA.'+key)
    if calc['code_sha256']!=registry['core_sha256'] or hashlib.sha256((T.parent/'climateos_au_landfill_methane_methods_001/mass_balance.py').read_bytes().replace(b'\r\n',b'\n')).hexdigest()!=registry['core_sha256']:
        flag('MATERIAL_CONTRADICTION','CODE_HASH','CALCULATION.code_sha256')
    if calc['oxidation_applications']!=1: flag('MATERIAL_CONTRADICTION','DOUBLE_OXIDATION','CALCULATION')
    if calc['lateral_fate']!='UNKNOWN_NOT_AVOIDED': flag('MATERIAL_CONTRADICTION','BOUNDARY_OMISSION','CALCULATION')
    roles=registry['roles']
    submitter=roles.get(role['submitter_id']); reviewer=roles.get(role['reviewer_id'])
    if not submitter or not reviewer:
        flag('EVIDENCE_INSUFFICIENT','ROLE_UNKNOWN','REVIEW')
    elif (reviewer['role']!='technical_reviewer_fixture' or submitter['role']!='submitter_fixture'
          or role['submitter_id']==role['reviewer_id'] or reviewer['organization']==submitter['organization'] or reviewer['conflict_of_interest']):
        flag('MATERIAL_CONTRADICTION','ROLE_CONFLICT','REVIEW')
    if role['authority']!='ROLE_SIMULATION_NO_HUMAN_APPROVAL': flag('MATERIAL_CONTRADICTION','UNAUTHORIZED_APPROVAL','REVIEW')
    if package['OUTCOME']['requested_effect']!='NOT_ASSESSED' or package['OUTCOME']['regulatory_certification']!='NOT_PROVIDED':
        flag('MATERIAL_CONTRADICTION','UNAUTHORIZED_CERTIFICATION','OUTCOME')
    ids=[s['evidence_id'] for s in package['SOURCE_LICENCE']]
    if len(ids)!=len(set(ids)): flag('MATERIAL_CONTRADICTION','DUPLICATE_EVIDENCE','SOURCE_LICENCE')
    claimids=[c['claim_id'] for c in package['CLAIM']]
    if len(claimids)!=len(set(claimids)): flag('MATERIAL_CONTRADICTION','DUPLICATE_CLAIM','CLAIM')
    for claim in package['CLAIM']:
        problems=list(common); answer=None
        if claim['scope']!='SYNTHETIC_ARITHMETIC_ONLY':
            problems.append(('MATERIAL_CONTRADICTION','SCOPE_EXPANSION','CLAIM.scope'))
        if not claim['supporting_evidence_ids'] or any(e not in ids for e in claim['supporting_evidence_ids']):
            problems.append(('EVIDENCE_INSUFFICIENT','MISSING_CLAIM_EVIDENCE','CLAIM.supporting_evidence_ids'))
        matching=[case for source in package['SOURCE_LICENCE'] if source['evidence_id'] in claim['supporting_evidence_ids'] for case in source['payload']['cases'] if case['fixture']==claim['fixture']]
        if len(matching)!=1:
            problems.append(('EVIDENCE_INSUFFICIENT','RAW_INPUT_LINK','CLAIM.flows'))
        elif matching[0]['flows']!=claim['flows']:
            problems.append(('MATERIAL_CONTRADICTION','RAW_INPUT_MISMATCH','CLAIM.flows'))
        try:
            # Arithmetic is explicitly on authored synthetic fixtures, even for missing-evidence C.
            request=ledger.fixture(claim['fixture'])
            request['flows']=claim['flows']
            answer=ledger.evaluate(request)
            if not math.isclose(answer['emitted_kg_CH4'],claim['reported_emitted_kg_CH4'],rel_tol=1e-12,abs_tol=1e-12):
                raise ValueError('OUTPUT_MISMATCH')
        except (ValueError,KeyError,TypeError) as exc:
            problems.append(('MATERIAL_CONTRADICTION',str(exc),'CLAIM.flows_or_output'))
            answer=None
        states={p[0] for p in problems}
        state='MATERIAL_CONTRADICTION' if 'MATERIAL_CONTRADICTION' in states else ('EVIDENCE_INSUFFICIENT' if states else 'METHOD_ALIGNED')
        result['claims'].append({'claim_id':claim['claim_id'],'status':state,
            'method':'METHOD_ALIGNED' if aligned else 'NOT_ASSESSED',
            'arithmetic':'RECALCULATED' if answer is not None else 'NOT_ASSESSED',
            'evidence':'EVIDENCE_INSUFFICIENT' if any(p[0]=='EVIDENCE_INSUFFICIENT' for p in problems) else ('MATERIAL_CONTRADICTION' if problems else 'SYNTHETIC_ONLY'),
            'failures':[{'classification':s,'reason':r,'pointer':p,'remedy':'Correct identified mismatch or supply independently reviewable original evidence; append new revision.'} for s,r,p in problems],
            'supporting_evidence_ids':claim['supporting_evidence_ids'],'scope':claim['scope'],
            'reviewer':result['reviewer'],'calculation':answer,'effect':'NOT_ASSESSED'})
    result['status']='MATERIAL_CONTRADICTION' if any(c['status']=='MATERIAL_CONTRADICTION' for c in result['claims']) else ('EVIDENCE_INSUFFICIENT' if any(c['status']=='EVIDENCE_INSUFFICIENT' for c in result['claims']) else 'METHOD_ALIGNED')
    return result

def verify_events(events, expected_head):
    prev='0'*64
    transitions={'START':{'SUBMITTED'},'SUBMITTED':{'REVIEWED','WITHDRAWN'},'REVIEWED':{'OBJECTED','WITHDRAWN'},
                 'OBJECTED':{'CORRECTED','WITHDRAWN'},'CORRECTED':{'REREVIEWED','WITHDRAWN'},'REREVIEWED':{'OBJECTED','WITHDRAWN'},'WITHDRAWN':set()}
    stage='START'; package_sha=None
    for i,event in enumerate(events):
        core.require(set(event)=={'sequence','action','actor','package_sha256','previous','event_sha256'},'EVENT_SCHEMA')
        body={k:v for k,v in event.items() if k!='event_sha256'}
        core.require(event['previous']==prev and event['sequence']==i,'CHAIN_ORDER')
        core.require(digest(body)==event['event_sha256'],'EVENT_TAMPER')
        core.require(event['action'] in transitions[stage],'LIFECYCLE')
        required='TECHNICAL_REVIEW_FIXTURE' if event['action'] in {'REVIEWED','REREVIEWED'} else 'SYNTHETIC_SUBMITTER'
        core.require(event['actor']==required,'EVENT_ROLE')
        core.require(len(event['package_sha256'])==64 and all(c in '0123456789abcdef' for c in event['package_sha256']),'EVENT_PACKAGE_SHA')
        if stage!='START':
            core.require((event['package_sha256']!=package_sha) if event['action']=='CORRECTED' else (event['package_sha256']==package_sha),'REVISION_LINK')
        package_sha=event['package_sha256']; stage=event['action']; prev=event['event_sha256']
    core.require(prev==expected_head,'EXTERNAL_HEAD_MISMATCH')
    return stage

def append_event(events,action,actor,package_sha):
    # Return a new list. Original history is never rewritten by this function.
    body={'sequence':len(events),'action':action,'actor':actor,'package_sha256':package_sha,
          'previous':events[-1]['event_sha256'] if events else '0'*64}
    result=events+[dict(body,event_sha256=digest(body))]
    verify_events(result,result[-1]['event_sha256'])
    return result

def main():
    outputs={name:review(load('examples/'+name+'.json')) for name in ['A','B','C']}
    (T/'evidence/review-results.json').write_text(json.dumps(outputs,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8',newline='\n')
    request=json.loads((T.parent/'climateos_methane_physics_knowledge_engine_001/input.json').read_text(encoding='utf-8'))
    result=core.execute(request)
    core.require(result['status']=='SYNTHETIC_ONLY','FROZEN_CHAIN_A')
    (T/'evidence/chain-a-replay.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print({k:v['status'] for k,v in outputs.items()})

if __name__=='__main__': main()
