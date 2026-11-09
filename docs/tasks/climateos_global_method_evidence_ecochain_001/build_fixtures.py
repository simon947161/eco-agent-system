"""Author three synthetic examples and a frozen proposal registry; not admission."""
import copy, hashlib, json
from reviewer import T, ledger, digest

def save(name,value):
    p=T/name; p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def contract(value):
    if isinstance(value,dict): return {'type':'object','additionalProperties':False,'required':list(value),'properties':{k:contract(v) for k,v in value.items()}}
    if isinstance(value,list): return {'type':'array','minItems':1,'items':contract(value[0])}
    return {'type':'boolean' if isinstance(value,bool) else 'number' if isinstance(value,(int,float)) else 'string'}

def main():
    names=['uncaptured','capture_flare','oxidation_leaks']
    payload={'origin':'AUTHOR_SYNTHETIC','cases':[{'fixture':n,'flows':ledger.fixture(n)['flows']} for n in names]}
    source={'evidence_id':'AUTHOR_LEDGER_FIXTURES','origin':'AUTHOR_SYNTHETIC','licence':'AUTHOR_SYNTHETIC_CC0','sha256':digest(payload),'payload':payload}
    code_sha=hashlib.sha256((T.parent/'climateos_au_landfill_methane_methods_001/mass_balance.py').read_bytes().replace(b'\r\n',b'\n')).hexdigest()
    package={'schema_version':'claim-evidence-proposal/1','package_id':'A','revision':'1',
      'CLAIM':[{'claim_id':'A-'+n,'scope':'SYNTHETIC_ARITHMETIC_ONLY','fixture':n,
                'supporting_evidence_ids':['AUTHOR_LEDGER_FIXTURES'],'flows':ledger.fixture(n)['flows'],
                'reported_emitted_kg_CH4':v} for n,v in zip(names,[95,32.7,31.08])],
      'METHOD':{'id':ledger.VERSION,'jurisdiction':'AUTHOR_SYNTHETIC_ONLY','version':'1','reporting_year':'SYNTHETIC_NOT_A_REPORTING_YEAR','formula_id':'FOUR_INTERFACE_CH4_C_LEDGER'},
      'SOURCE_LICENCE':[source],
      'DATA':{'gas':'CH4','phase':'total_CH4_gas_plus_dissolved','unit':'kg_CH4/interval',
        'wet_dry':'NOT_APPLICABLE_INTEGRATED_MASS','volume_reference':'NOT_APPLICABLE_MASS',
        'time_window':'SYNTHETIC_DAY_001','timezone':'SYNTHETIC_NO_CIVIL_TIME',
        'spatial_boundary':'SYNTHETIC_BODY_PIPE_DEVICE_COVER;LATERAL_UNKNOWN',
        'crs':'NOT_APPLICABLE_SYNTHETIC','coordinates':'NOT_A_REAL_SITE',
        'instrument':'SYNTHETIC_NOT_FIELD','calibration':'SYNTHETIC_NOT_FIELD',
        'uncertainty':'EXACT_ARITHMETIC_FIXTURE_NOT_FIELD_UNCERTAINTY',
        'raw_flow_evidence':'SYNTHETIC_FIXTURE_ONLY','missing_policy':'REJECT_UNKNOWN_NO_IMPUTATION'},
      'CALCULATION':{'code_sha256':code_sha,'oxidation_applications':1,'lateral_fate':'UNKNOWN_NOT_AVOIDED'},
      'REVIEW':{'submitter_id':'SYNTHETIC_SUBMITTER','reviewer_id':'TECHNICAL_REVIEW_FIXTURE','authority':'ROLE_SIMULATION_NO_HUMAN_APPROVAL'},
      'OUTCOME':{'requested_effect':'NOT_ASSESSED','regulatory_certification':'NOT_PROVIDED'}}
    schema=contract(package); schema.update({'$schema':'https://json-schema.org/draft/2020-12/schema','$id':'urn:climateos:claim-evidence-proposal:1','title':'Bounded offline synthetic technical review; not ECOChain canonical'})
    save('CLAIM_EVIDENCE_SCHEMA.json',schema)
    save('examples/A.json',package)
    wrong=copy.deepcopy(package); wrong['package_id']='B'
    for c in wrong['CLAIM']: c['claim_id']=c['claim_id'].replace('A-','B-')
    wrong['DATA']['phase']='ambient_air'; wrong['DATA']['unit']='ppm'
    wrong['CALCULATION']['oxidation_applications']=2
    wrong['CALCULATION']['lateral_fate']='AVOIDED_EMISSION'
    wrong['CLAIM'][2]['flows']['lateral_out']['value']=0
    save('examples/B.json',wrong)
    missing=copy.deepcopy(package); missing['package_id']='C'
    for c in missing['CLAIM']: c['claim_id']=c['claim_id'].replace('A-','C-')
    missing['DATA']['raw_flow_evidence']='UNKNOWN'; missing['DATA']['calibration']='UNKNOWN'
    missing['SOURCE_LICENCE'][0]['licence']='UNKNOWN'
    save('examples/C.json',missing)
    registry={'status':'AUTHOR_FIXTURE_REGISTRY_NOT_IDENTITY_AUTHORITY','sources':{'AUTHOR_LEDGER_FIXTURES':{k:source[k] for k in ['origin','licence','sha256']}},'core_sha256':code_sha,
      'roles':{'SYNTHETIC_SUBMITTER':{'role':'submitter_fixture','organization':'FIXTURE_ORG_A','conflict_of_interest':False},
               'TECHNICAL_REVIEW_FIXTURE':{'role':'technical_reviewer_fixture','organization':'FIXTURE_ORG_B','conflict_of_interest':False}}}
    save('evidence/trusted-registry.json',registry)

if __name__=='__main__': main()
