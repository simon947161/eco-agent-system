"""Rebuild authored CC0 synthetic examples and closed schema. No network."""
import json
from pathlib import Path
import hashlib
import engine as e

T = Path(__file__).resolve().parent
def save(name, value):
    p = T/name
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8',newline='\n')

def string(**kw): return dict(type='string',**kw)
def fixed(value): return dict(type='boolean' if isinstance(value,bool) else 'string',const=value)
def obj(**props): return dict(type='object',additionalProperties=False,required=list(props),properties=props)
def array(item, minimum=0): return dict(type='array',minItems=minimum,items=item)
def nullable(typ='string'): return dict(type=[typ,'null'])
sha=string(pattern='[0-9a-f]{64}')
types = ['OBSERVATION','PHYSICAL_ESTIMATE','BASELINE_COUNTERFACTUAL','PROJECT_EMISSIONS',
         'LEAKAGE','NET_ABATEMENT_ESTIMATE','ADDITIONALITY_AND_ELIGIBILITY',
         'CLAIM_AND_CREDIT_RIGHTS','ASSURANCE_STATUS']
schema=obj(schema_version=fixed('awt-claim-passport/1'),claim_id=string(pattern='AWT-[A-D]'),
    scenario=string(enum=list('ABCD')),revision=dict(type='number',minimum=1),
    previous_revision_sha256=dict(type=['string','null'],pattern='[0-9a-f]{64}'),mode=fixed('SYNTHETIC'),input_sha256=sha,
    dataset=obj(source=fixed('AUTHOR_SYNTHETIC_FIXTURE'),licence=fixed('CC0-1.0_AUTHOR_INPUT_ONLY'),
        sha256=sha,byte_scope=fixed('EXACT_UTF8_LF_FIXTURE_BYTES'),time_support=fixed(e.INTERVAL),
        timezone=fixed('NOT_APPLICABLE_SYNTHETIC_NO_CIVIL_TIME'),qc=fixed('ARITHMETIC_FIXTURE_NOT_INSTRUMENT_QC'),
        spatial_scope=fixed('FICTIONAL_NSW_NO_SITE_OR_COORDINATES')),
    observation=obj(status=fixed('NO_OBSERVATION'),instrument=nullable(),unit=nullable(),time=nullable(),
        location=nullable(),uncertainty=nullable('number'),qc=fixed('NOT_APPLICABLE_SYNTHETIC')),
    baseline_evidence=string(enum=['SYNTHETIC_ASSUMPTIONS_ONLY','MISSING']),
    formula=obj(id=fixed('AUTHOR_COHORT_COUNTERFACTUAL_V1'),source_version=fixed('PR144_LEDGER_V1_AND_IPCC_AR6_GWP100'),
        statutory_solver=fixed(False),unit=fixed('t_CO2e/1000_t_wet_cohort')),
    assumptions=array(obj(input_pointer=string(),owner=fixed('CODEX_AUTHOR_SYNTHETIC'),unit=string(),uncertainty=string()),1),
    entities=array(obj(id=string(),type=string(enum=types),depends_on=array(string()),
        evidence_state=string(enum=['SYNTHETIC','UNKNOWN','OFFICIAL_CONTEXT_ONLY']),result_pointer=string()),1),
    legal=obj(jurisdiction=string(enum=['AU-NSW','OTHER']),assessment_date=string(pattern='[0-9]{4}-[0-9]{2}-[0-9]{2}'),
        premises=string(enum=['HOUSEHOLD_COUNCIL_RED_BIN','UNKNOWN']),
        exemption=string(enum=['UNKNOWN','NO_SYNTHETIC_ASSUMPTION']),method=string(enum=['AWT_2015','AWT_2026_PROPOSAL','UNKNOWN']),
        registration=string(enum=['NEW','LEGACY_UNVERIFIED','UNKNOWN']),source_verified_at=fixed('2026-11-23'),
        legal_effective_date=fixed('AWT_EXPIRED_2025-03-31;FOGO_HOUSEHOLD_DUE_2030-07-01'),
        source_status=fixed('OFFICIAL_WEB_SCREENING_NSW_PRIMARY_TEXT_BLOCKED')),
    rights_links=array(obj(batch=string(),period=string(),quantity_boundary=string(),mechanism=string(),
        project_registry_id=fixed('NOT_REGISTERED_SYNTHETIC'),right_verified=fixed(False))),
    output_provenance=obj(engine=fixed('engine.py'),engine_sha256=sha,kernel=fixed('PR144_LEDGER'),
        result_file=fixed('evidence/results.json'),hash_scope=fixed('SOURCE_LF_NORMALIZED;GIT_HEAD_EXTERNAL_ANCHOR')),
    review=obj(gate=fixed('PENDING'),human_reviewer=nullable(),human_notes=array(string(),1),
        scientifically_admitted=fixed(False),regulatory_certification=fixed('NOT_PROVIDED'),credit_quantity=fixed('NOT_DETERMINED')))
schema.update({'$schema':'https://json-schema.org/draft/2020-12/schema','$id':'climateos.awt.claim-passport.v1',
               'title':'Issue162 PR145-compatible claim passport extension; synthetic pilot only'})
save('CLAIM_PASSPORT_SCHEMA.json',schema)

base = dict(mode='SYNTHETIC', interval=e.INTERVAL, waste_unit='t_wet', waste_t=1000,
    route='AD_WITH_RESIDUE_LANDFILL', doc_fraction=.15, landfill_decomposed_fraction=.5,
    capture_fraction=.37, ad_decomposed_fraction=.6, residue_decomposed_fraction=.1,
    ad_capture_fraction=.98, ad_pipe_loss_fraction=.01, residue_N2O_kg=100,
    import_kWh=18000, grid_kg_CO2e_per_kWh=.65, baseline_fossil_CO2_t=20,
    project_fossil_CO2_t=5, transport_fossil_CO2_t=10, offsite_leakage_fossil_CO2_t=5,
    residue_CH4_known='YES_SYNTHETIC', residue_N2O_known='YES_SYNTHETIC', leakage_known='YES_SYNTHETIC')
units = {'waste_t':'t_wet','residue_N2O_kg':'kg_N2O','import_kWh':'kWh',
         'grid_kg_CO2e_per_kWh':'kg_CO2e/kWh'}
deps = [[],['OBSERVATION'],['PHYSICAL_ESTIMATE'],['PHYSICAL_ESTIMATE'],[],
        ['BASELINE_COUNTERFACTUAL','PROJECT_EMISSIONS','LEAKAGE'],[],[],
        ['NET_ABATEMENT_ESTIMATE','ADDITIONALITY_AND_ELIGIBILITY','CLAIM_AND_CREDIT_RIGHTS']]
pointers=['observation','calculation/physical_ledger','calculation/baseline_t_CO2e','calculation/project_t_CO2e',
          'calculation/leakage_t_CO2e','calculation/estimated_net_abatement_t_CO2e','legal','duplicate_risks','assurance']
for s in 'ABCD':
    f = dict(base)
    if s=='A': f['route']='LANDFILL_IDENTITY'
    if s=='D': f.update(residue_CH4_known='UNKNOWN',residue_N2O_known='UNKNOWN')
    save('fixtures/'+s+'.json',f)
    legal = dict(jurisdiction='AU-NSW',assessment_date='2026-11-23',premises='HOUSEHOLD_COUNCIL_RED_BIN',
        exemption='UNKNOWN',method='AWT_2015',registration='NEW',source_verified_at='2026-11-23',
        legal_effective_date='AWT_EXPIRED_2025-03-31;FOGO_HOUSEHOLD_DUE_2030-07-01',
        source_status='OFFICIAL_WEB_SCREENING_NSW_PRIMARY_TEXT_BLOCKED')
    if s=='C': legal.update(assessment_date='2030-07-01',method='AWT_2026_PROPOSAL',exemption='NO_SYNTHETIC_ASSUMPTION')
    if s=='D': legal.update(registration='LEGACY_UNVERIFIED')
    rights = [dict(batch='SYNTHETIC_BATCH_1000T',period=e.INTERVAL,quantity_boundary='AVOIDED_LANDFILL_CH4',
                   mechanism='AWT_CANDIDATE',project_registry_id='NOT_REGISTERED_SYNTHETIC',right_verified=False)]
    if s=='D': rights.append(dict(rights[0],mechanism='SAFEGUARD_CANDIDATE'))
    p = dict(schema_version='awt-claim-passport/1',claim_id='AWT-'+s,scenario=s,revision=1,
        previous_revision_sha256=None,mode='SYNTHETIC',input_sha256=e.prior.digest(f),
        dataset=dict(source='AUTHOR_SYNTHETIC_FIXTURE',licence='CC0-1.0_AUTHOR_INPUT_ONLY',
            sha256=e.sha_bytes(T/('fixtures/'+s+'.json')),byte_scope='EXACT_UTF8_LF_FIXTURE_BYTES',
            time_support=e.INTERVAL,timezone='NOT_APPLICABLE_SYNTHETIC_NO_CIVIL_TIME',
            qc='ARITHMETIC_FIXTURE_NOT_INSTRUMENT_QC',spatial_scope='FICTIONAL_NSW_NO_SITE_OR_COORDINATES'),
        observation=dict(status='NO_OBSERVATION',instrument=None,unit=None,time=None,location=None,
                         uncertainty=None,qc='NOT_APPLICABLE_SYNTHETIC'),
        baseline_evidence='MISSING' if s=='D' else 'SYNTHETIC_ASSUMPTIONS_ONLY',
        formula=dict(id='AUTHOR_COHORT_COUNTERFACTUAL_V1',source_version='PR144_LEDGER_V1_AND_IPCC_AR6_GWP100',
                     statutory_solver=False,unit='t_CO2e/1000_t_wet_cohort'),
        assumptions=[dict(input_pointer='/'+k,owner='CODEX_AUTHOR_SYNTHETIC',
            unit=units.get(k,'fraction' if k.endswith('_fraction') else 't_fossil_CO2'),
            uncertainty=('BOUND_'+str(e.RANGES[k])+'_NOT_CI') if k in e.RANGES else 'FIXED_SYNTHETIC_NOT_CALIBRATED')
            for k,v in f.items() if isinstance(v,(float,int))],
        entities=[dict(id=typ,type=typ,depends_on=dep,
            evidence_state='UNKNOWN' if typ=='OBSERVATION' else ('OFFICIAL_CONTEXT_ONLY' if typ=='ADDITIONALITY_AND_ELIGIBILITY' else 'SYNTHETIC'),
            result_pointer='evidence/results.json#/'+s+'/'+pointer) for typ,dep,pointer in zip(types,deps,pointers)],
        legal=legal,rights_links=rights,
        output_provenance=dict(engine='engine.py',engine_sha256=hashlib.sha256((T/'engine.py').read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
            kernel='PR144_LEDGER',result_file='evidence/results.json',hash_scope='SOURCE_LF_NORMALIZED;GIT_HEAD_EXTERNAL_ANCHOR'),
        review=dict(gate='PENDING',human_reviewer=None,human_notes=['No independent reviewer has signed this synthetic teaching package.'],
            scientifically_admitted=False,regulatory_certification='NOT_PROVIDED',credit_quantity='NOT_DETERMINED'))
    save('examples/'+s+'.json',p)
print('Four synthetic fixtures and compatible claim passports generated.')
