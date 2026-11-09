"""Bounded offline analytical CH4 chain; no eval, network or field-data models."""
from __future__ import annotations
import json
import math
from pathlib import Path
from cczps_lite.integration import physics_validation as p

TASK = Path(__file__).resolve().parents[2] / 'docs/tasks/climateos_methane_physics_knowledge_engine_001'
QUESTIONS = {'给定条件下空气甲烷浓度多少': 'chain_a', '填埋场释放多少': 'landfill',
             '同吨数不同高度气候效应是否一样': 'altitude', '现有观测可否直接用于计算': 'observations'}
ALLOWED = {'E01', 'E02', 'E03', 'E04', 'E05'}
UNITS = {'x_ppm': 'ppm_dry', 'P': 'Pa', 'T': 'K', 'e': 'Pa', 'V': 'm3_wet_actual',
         'P_ref': 'Pa', 'T_ref': 'K'}
KEYS = {'question','gas','phase','mode','source_id','licence','calibration','temporal_support',
        'spatial_support','model_id','values','units','uncertainty','parameter_provenance'}


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def plan(registry, targets):
    """Only computation dependencies enter this DAG; conceptual feedback never does."""
    nodes = {n['equation_id']: n for n in registry['equations']}
    require(len(nodes) == len(registry['equations']), 'DUPLICATE_NODE')
    order, active = [], set()
    def visit(key):
        require(key in nodes, 'BROKEN_DEPENDENCY')
        require(key not in active, 'DEPENDENCY_CYCLE')
        if key in order:
            return
        node = nodes[key]
        require(key in ALLOWED and node['permission'] == 'SYNTHETIC_ONLY', 'MODEL_NOT_AUTHORIZED')
        require(node['source_id'] and node['parameter_provenance'], 'UNSOURCED_EQUATION')
        require(node['validation_status'] == 'ANALYTICAL_REFERENCE', 'VALIDATION_HOLD')
        active.add(key)
        for parent in node['dependencies']:
            visit(parent)
        active.remove(key); order.append(key)
    for target in targets:
        visit(target)
    return order


def conserve(actual, reference):
    require(math.isfinite(actual) and math.isfinite(reference), 'NONFINITE_MASS')
    residual = actual-reference
    require(abs(residual) <= 1e-15 + 1e-12*max(abs(actual),abs(reference)), 'MASS_NOT_CONSERVED')
    return residual


def execute(request):
    try:
        require(isinstance(request, dict) and set(request) == KEYS, 'REQUEST_SCHEMA')
        require(isinstance(request['question'],str) and request['question'] in QUESTIONS, 'UNKNOWN_QUESTION')
        route = QUESTIONS[request['question']]
        if route != 'chain_a':
            gaps = {'landfill':['waste history and DOC','site k and oxidation/capture','flow and boundary validation'],
                    'altitude':['gas-specific counterfactual and metric/horizon','transport chemistry and response validation'],
                    'observations':['PR140/141 global metadata and calibration gates remain open']}[route]
            return {'status':'STRUCTURAL_QC_ONLY' if route=='observations' else 'BLOCKED',
                    'route':route,'missing':gaps,'numerical_output':None}
        require(request['gas']=='CH4' and request['phase']=='gas_dry_fraction_in_wet_air','GAS_OR_PHASE')
        require(request['mode']=='SYNTHETIC_REFERENCE','REAL_DATA_NOT_AUTHORIZED')
        require(request['source_id']=='TASKBOOK_SYNTHETIC_A1' and request['licence']=='REPOSITORY_AUTHORED_SYNTHETIC','SOURCE_OR_LICENCE')
        require(request['calibration']=='NOT_APPLICABLE_SYNTHETIC','CALIBRATION_REQUIRED')
        require(request['temporal_support']=='instantaneous_same_parcel' and request['spatial_support']=='homogeneous_parcel_no_height_inference','SUPPORT_MISMATCH')
        require(request['model_id']=='p1_chain/1','MODEL_NOT_AUTHORIZED')
        require(request['units']==UNITS,'UNIT_OR_BASIS')
        vals=request['values']; require(isinstance(vals,dict) and set(vals)==set(UNITS),'VARIABLE_SCHEMA')
        require(request['parameter_provenance']=={'inputs':'TASKBOOK_SYNTHETIC_A1','constants':'FROZEN_P1_PR138','uncertainty':'DECLARED_SYNTHETIC_SMALL_ERROR'},'PARAMETER_SOURCE')
        ranges={'x_ppm':(0,100),'P':(50000,110000),'T':(230,330),'e':(0,10000),'V':(0,100),'P_ref':(50000,110000),'T_ref':(230,330)}
        v={k:p.number(vals[k],k,low=lo,high=hi) for k,(lo,hi) in ranges.items()}
        require(v['e'] < v['P'], 'INVALID_PARTIAL_PRESSURE')
        u=request['uncertainty']
        require(isinstance(u,dict) and set(u)=={'std','rho_P_e','assumption'},'UNCERTAINTY_SCHEMA')
        require(u['assumption']=='only_P_e_covariance;constants_exact;model_error_excluded','COVARIANCE_REQUIRED')
        require(isinstance(u['std'],dict) and set(u['std'])=={'x_ppm','P','T','e'},'UNCERTAINTY_SCHEMA')
        sd={k:p.number(value,k) for k,value in u['std'].items()}
        require(all(sd[k] <= lim for k,lim in {'x_ppm':1,'P':1000,'T':2,'e':200}.items()),'LINEARIZATION_DOMAIN')
        rho=p.number(u['rho_P_e'],'rho',low=-1,high=1)
        registry=json.loads((TASK/'EQUATION_REGISTRY.json').read_text(encoding='utf-8'))
        order=plan(registry,['E04','E05'])
        x=v['x_ppm']*1e-6
        gas=p.gas_properties(x,v['P'],v['T'],v['e'])
        ref=p.reference_dry_volume(v['V'],v['P'],v['T'],v['e'],v['P_ref'],v['T_ref'])
        cref=p.gas_properties(x,v['P_ref'],v['T_ref'],0.0)['mass_concentration_kg_per_m3']
        c=gas['mass_concentration_kg_per_m3']; mass=c*v['V']; refmass=cref*ref
        residual=conserve(mass,refmass)
        # Jacobian in declared input units, including x in ppm, not mol/mol.
        j={'x_ppm':1e-6*(v['P']-v['e'])*p.M_CH4/(p.R*v['T']),
           'P':x*p.M_CH4/(p.R*v['T']),'e':-x*p.M_CH4/(p.R*v['T']),'T':-c/v['T']}
        terms={k:(j[k]*sd[k])**2 for k in j}
        cross=2*j['P']*j['e']*rho*sd['P']*sd['e']
        variance=math.fsum([*terms.values(),cross]); require(variance>=0,'INVALID_COVARIANCE')
        by_id={n['equation_id']:n for n in registry['equations']}
        return {'status':'SYNTHETIC_ONLY','execution_status':'IMPLEMENTED_SYNTHETIC_TESTED',
                'classification':'SYNTHETIC_REFERENCE / ANALYTICAL_TEST','input':request,
                'path':order,'steps':[{'equation_id':k,'formula':by_id[k]['formula'],'source_id':by_id[k]['source_id'],
                                     'input_units':by_id[k]['input_units'],'output_units':by_id[k]['output_units']} for k in order],
                'conversion':{'ppm_to_mol_per_mol':1e-6,'x_dry':x,'dry_pressure_Pa':v['P']-v['e'],
                              'kg_m3_to_mg_m3':1e6,'reference_water_pressure_Pa':0.0,'reference_basis':'explicitly dry'},
                'constants':{'R_J_mol_K':p.R,'M_CH4_kg_mol':p.M_CH4},
                'output':{'concentration_kg_m3':c,'concentration_mg_m3':c*1e6,'x_wet_mol_mol':gas['x_wet_mol_per_mol'],
                          'reference_dry_volume_m3':ref,'mass_actual_kg':mass,'mass_reference_kg':refmass,'mass_residual_kg':residual},
                'uncertainty':{'jacobian_per_declared_unit':j,'diagonal_variance_terms':terms,'covariance_term':cross,
                               'u_c_kg_m3':math.sqrt(variance),'scope':'first-order concentration only; assumed errors; no field confidence interval'},
                'sensitivity':{'x_elasticity':1 if x>0 else None,'P_elasticity':v['P']/(v['P']-v['e']),
                               'e_elasticity':-v['e']/(v['P']-v['e']),'T_elasticity':-1},
                'explanation_zh':'同一份空气的体积会随温压变化，单位体积甲烷质量因而改变。换算成同一干气参考体积后，甲烷总质量守恒。这不是排放量或气候效应。',
                'holds':['no real source rate','no climate coefficient','synthetic uncertainties only','scientific admission unchanged']}
    except (ValueError,KeyError,TypeError,OSError) as exc:
        return {'status':'BLOCKED','reason':str(exc),'numerical_output':None}
