"""Public synthetic contract + frozen PR152 side only. No legacy loader."""
from pathlib import Path
from dataclasses import replace
import copy,hashlib,json,math,sys,time
TASK=Path(__file__).resolve().parents[1];ROOT=TASK.parents[2]
sys.path.insert(0,str(ROOT))
from cczps_lite.integration.earth_system_coupling import models as m
from cczps_lite.integration.earth_system_coupling.state import State,Grid,Rejection,digest
from cczps_lite.integration.earth_system_coupling.ports import ModelPort

BASELINE='cf91e4a061341bc33d16400bcf4c6a2c2817aa65'

def design():
    base={'id':'P01','fault':'none','temperature_c':20.,'wind_m_s':3.,'rain_mm_day':0.,
          'temperature_unit':'degC','temperature_offset_s':0,'history_days':14,
          'background':{'et0_mm_day':4.,'latitude':-35.,'longitude':149.,'target_altitude_m':800.,'reference_altitude_m':800.,'coastal':False,'rainfall_season':'cool-season'},
          'reference':'ALLOW','comparison_class':'NUMERIC_INPUT_GOVERNANCE'}
    cases=[]
    changes=[{}, {'id':'P02','fault':'missing_temperature','temperature_c':'MISSING','reference':'REFUSE'},
      {'id':'P03','fault':'nonfinite_wind','wind_m_s':'NONFINITE_NAN','reference':'REFUSE'},
      {'id':'P04','fault':'missing_rain','rain_mm_day':'MISSING','reference':'REFUSE'},
      {'id':'P05','fault':'wrong_unit','temperature_unit':'degF','reference':'REFUSE','comparison_class':'METADATA_CAPABILITY_ATTEMPT'},
      {'id':'P06','fault':'wrong_time','temperature_offset_s':900,'reference':'REFUSE','comparison_class':'METADATA_CAPABILITY_ATTEMPT'}]
    for change in changes:cases.append(dict(copy.deepcopy(base),**change))
    return {'protocol':'ISSUE151_PAIRED_INPUT_GOVERNANCE_V1','baseline_sha':BASELINE,'groups':6,'repeats_per_side':2,
      'task':'May the declared downstream computation consume these required inputs and return a native result?',
      'reference_rule':'ALLOW iff shared required quantities are present and finite, declared temperature unit is degC and field clock equals consumer clock; otherwise REFUSE.',
      'reference_is':'predeclared interface requirement, not observed environmental truth',
      'common_outputs':['RETURNED','STRUCTURED_REFUSAL','UNCONTROLLED_ERROR','ADAPTER_INCOMPATIBLE'],
      'missing_representation':'MISSING maps to None; NONFINITE_NAN maps to IEEE NaN on both sides; never impute.',
      'information_budget':'Constant synthetic quantities; legacy uses 14 identical daily numeric samples; new side uses two identical cells and one 900-second step. This represents numeric eligibility only, not equal physical time/space support.',
      'metadata_rule':'If a native interface cannot represent a metadata field, record capability loss. Do not add a validation gate on its behalf, silently convert bad units, or score it as a native metadata refusal.',
      'new_side':'Actual Field/State.require, Atmosphere/Surface.required_fields and ModelPort.step from frozen PR152; proposals only, not a full coupled trajectory.',
      'legacy_side':'Existing local entry and original rules; private representation-only adapter; no algorithm transplant.',
      'correctness':'Outcome matching the independent admission rule; native return is not scientific approval. Uncontrolled errors are not structured refusals.',
      'replay':'Exact within each side after excluding wall-clock cost and private traceback paths. Compare decisions, not incompatible physical/diagnostic output magnitudes.',
      'cost':'Record end-to-end adapter/native seconds separately; different work and instrumentation forbid a speed-winner claim.',
      'stop':'At most six groups, two repetitions per side; preserve failures; no tuning after outcome inspection.',
      'prediction_accuracy_comparisons':0,'science':'PENDING','cases':cases}

def decode(v):
    if v=='MISSING':return None
    if v=='NONFINITE_NAN':return float('nan')
    return v

def reference(case):
    vals=[decode(case[k]) for k in ('temperature_c','wind_m_s','rain_mm_day')]
    valid=all(type(v) in (int,float) and math.isfinite(v) for v in vals)
    return 'ALLOW' if valid and case['temperature_unit']=='degC' and case['temperature_offset_s']==0 else 'REFUSE'

def verify_sources():
    frozen=json.loads((ROOT/'docs/tasks/climateos_earth_system_coupling_lab_001/EXPERIMENT_RESULTS.json').read_text(encoding='utf-8'))
    hashes={}
    for name,h in frozen['source_hashes'].items():
        actual=hashlib.sha256((ROOT/name).read_bytes().replace(b'\r\n',b'\n')).hexdigest()
        assert actual==h,'FROZEN_SOURCE_CHANGED';hashes[name]=h
    return hashes

def run_case(case):
    start=time.perf_counter();stage='field_construction';ports={};kernel_started=[];cp=None
    row={'id':case['id'],'canonical_input_sha256':digest(case),'reference':reference(case),
         'status':None,'code':None,'stage':None,'native_nodes_started':kernel_started,
         'contract_metadata_supported':True,'native_output':None,'new_trajectory_runs':0}
    try:
        c=m.default_config();c.update(ta_k=293.15,wind_m_s=3.,rain_kg_m2_s=0.)
        grid=Grid.strip(2,c['length_m']);clock=m.time_window(0,c['dt_s']);h=digest(case)
        T=decode(case['temperature_c']);wind=decode(case['wind_m_s']);rain=decode(case['rain_mm_day'])
        temp=(T+273.15) if T is not None and case['temperature_unit']=='degC' else T
        rain=None if rain is None else rain/86400.
        values={'ta':temp,'ts':295.15,'q':c['q_kgkg'],'pressure':c['pressure_pa'],'u':wind,'v':0.,
                'rain':rain,'rn':c['radiation_w_m2'],'water':c['water_kg_m2'],'evap':0.,'runoff':0.}
        fields=[]
        for key,value in values.items():
            f=m.field(key,[value,value],grid,clock,h,source_id='SYNTHETIC_ISSUE151_PAIRWISE')
            if key=='ta':
                f=replace(f,unit='K' if case['temperature_unit']=='degC' else case['temperature_unit'],
                          time=m.time_window(case['temperature_offset_s'],c['dt_s']))
            fields.append(f)
        state=State(fields);cp=state.checkpoint()
        ports={'atmosphere':ModelPort(m.Atmosphere()).initialize(state,c),'surface':ModelPort(m.Surface()).initialize(state,c)}
        stage='dependency_gate'
        for port in ports.values():state.require(port.required_fields,grid=grid,time=clock)
        old_values={k:list(f.values) for k,f in state.fields.items()}
        stage='native_exchange';flux=m.Atmosphere().fluxes(old_values,c,old_values,c['dt_s'])
        output={};stage='native_steps'
        for label,port in ports.items():
            port.exchange=flux;kernel_started.append(label);output[label]=port.step(c['dt_s'])
        assert state.checkpoint()==cp,'UNEXPECTED_SHARED_COMMIT'
        row.update(status='RETURNED',native_output=output,state_unmodified=True)
    except Rejection as exc:row.update(status='STRUCTURED_REFUSAL',code=exc.code)
    except Exception as exc:row.update(status='UNCONTROLLED_ERROR',code=type(exc).__name__)
    row['stage']=stage;row['seconds']=time.perf_counter()-start
    return row

def stable(row):return {k:v for k,v in row.items() if k!='seconds'}

def run():
    protocol=json.loads((TASK/'PAIRWISE_PROTOCOL.json').read_text(encoding='utf-8'));assert protocol==design()
    hashes=verify_sources();rows=[]
    for case in protocol['cases']:
        assert reference(case)==case['reference']
        a=run_case(case);b=run_case(case);assert stable(a)==stable(b),'REPLAY_MISMATCH'
        rows.append({'id':case['id'],'canonical_input_sha256':digest(case),'reference':reference(case),'replay_equal':True,'new':a,'repeat_seconds':b['seconds']})
    return {'scope':'PUBLIC_NEW_SIDE_OF_ACTUAL_LOCAL_PAIRING','protocol_sha256':digest(protocol),'baseline_sha':BASELINE,
            'case_groups':6,'native_attempts':12,'source_hashes':hashes,'rows':rows,'trajectory_runs':0,'science':'PENDING'}

if __name__=='__main__':
    if '--prepare' in sys.argv:
        (TASK/'PAIRWISE_PROTOCOL.json').write_text(json.dumps(design(),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PAIR_PROTOCOL_FIXED_BEFORE_EXECUTION')
    else:
        result=run();out=ROOT/'runtime_data/issue151_pairwise_new.json';out.parent.mkdir(exist_ok=True)
        out.write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
        print(json.dumps({'groups':6,'new_attempts':12,'outcomes':[{ 'id':r['id'],'status':r['new']['status'],'code':r['new']['code']} for r in result['rows']]}))
