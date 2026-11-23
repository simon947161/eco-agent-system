"""Issue162 bounded author-synthetic review. Offline, no credit or field solver.

Reuses PR144 methane ledger and PR145 hashes/schema primitives/event history.
All numerical outputs are conditional on supplied synthetic assumptions.
"""
from copy import deepcopy
from datetime import date
import hashlib
import importlib.util
import itertools
import json
import math
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
spec = importlib.util.spec_from_file_location('awt_existing_review', HERE.parent / 'climateos_global_method_evidence_ecochain_001/reviewer.py')
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)
ledger = prior.ledger
VERSION = 'awt-teaching-envelope/1'
INTERVAL = 'COHORT_100_YEARS_INTEGRATED_NOT_ANNUAL'
TYPES = {'OBSERVATION', 'PHYSICAL_ESTIMATE', 'BASELINE_COUNTERFACTUAL',
         'PROJECT_EMISSIONS', 'LEAKAGE', 'NET_ABATEMENT_ESTIMATE',
         'ADDITIONALITY_AND_ELIGIBILITY', 'CLAIM_AND_CREDIT_RIGHTS', 'ASSURANCE_STATUS'}


def read(name):
    return json.loads((HERE / name).read_text(encoding='utf-8'))


def sha_bytes(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def schema_validate(value, schema):
    """Closed JSON Schema subset actually used here; no claim of general support.

    PR145 enforces basic leaf types and finite numbers. This extension implements
    nullable values, const/enum/ranges/patterns and required/extra-field checking.
    """
    allowed = {'$schema', '$id', 'title', 'description', 'type', 'properties',
               'required', 'additionalProperties', 'items', 'minItems', 'const',
               'enum', 'minimum', 'maximum', 'pattern'}
    if set(schema) - allowed:
        raise ValueError('UNSUPPORTED_SCHEMA_KEYWORD')
    types = schema['type'] if isinstance(schema['type'], list) else [schema['type']]
    if value is None and 'null' in types:
        return
    typ = next((t for t in types if t != 'null'), None)
    if typ == 'object':
        if not isinstance(value, dict) or set(value) != set(schema['required']):
            raise ValueError('SCHEMA_FIELDS')
        for key, item in value.items():
            schema_validate(item, schema['properties'][key])
    elif typ == 'array':
        if not isinstance(value, list) or len(value) < schema.get('minItems', 0):
            raise ValueError('SCHEMA_ARRAY')
        for item in value:
            schema_validate(item, schema['items'])
    else:
        prior.schema_check(value, {'type': typ})
    if 'const' in schema and value != schema['const']:
        raise ValueError('SCHEMA_CONST')
    if 'enum' in schema and value not in schema['enum']:
        raise ValueError('SCHEMA_ENUM')
    if 'minimum' in schema and value < schema['minimum']:
        raise ValueError('SCHEMA_MIN')
    if 'maximum' in schema and value > schema['maximum']:
        raise ValueError('SCHEMA_MAX')
    if 'pattern' in schema and not re.fullmatch(schema['pattern'], value):
        raise ValueError('SCHEMA_PATTERN')


def validate(passport):
    schema_validate(passport, read('CLAIM_PASSPORT_SCHEMA.json'))
    ids = [x['id'] for x in passport['entities']]
    if len(ids) != len(set(ids)) or {x['type'] for x in passport['entities']} != TYPES:
        raise ValueError('ENTITY_ID_OR_TYPE_COVERAGE')
    for entity in passport['entities']:
        if any(ref not in ids for ref in entity['depends_on']):
            raise ValueError('DANGLING_ENTITY')
    edges = {x['id']: x['depends_on'] for x in passport['entities']}
    def walk(key, chain):
        if key in chain:
            raise ValueError('CYCLIC_EVIDENCE')
        for dep in edges[key]:
            walk(dep, chain | {key})
    for key in ids:
        walk(key, set())
    # Only tracked local synthetic fixtures may enter this pilot. No paths from callers.
    expected = read('fixtures/' + passport['scenario'] + '.json')
    if passport['dataset']['sha256'] != sha_bytes(HERE / ('fixtures/' + passport['scenario'] + '.json')):
        raise ValueError('DATASET_BYTE_HASH')
    if passport['input_sha256'] != prior.digest(expected):
        raise ValueError('INPUT_HASH')
    if passport['claim_id'] != 'AWT-' + passport['scenario']:
        raise ValueError('CLAIM_SCENARIO_MISMATCH')
    actual_code = hashlib.sha256((HERE/'engine.py').read_bytes().replace(b'\r\n',b'\n')).hexdigest()
    if passport['output_provenance']['engine_sha256'] != actual_code:
        raise ValueError('CODE_HASH')
    if any(passport['observation'][k] is not None for k in ['instrument','unit','time','location','uncertainty']):
        raise ValueError('NO_OBSERVATION_MUST_REMAIN_NULL')
    numeric = {k for k,v in expected.items() if type(v) in (int,float)}
    assumptions = passport['assumptions']
    if len(assumptions) != len(numeric) or {a['input_pointer'] for a in assumptions} != {'/'+k for k in numeric}:
        raise ValueError('ASSUMPTION_COVERAGE')
    units = {'waste_t':'t_wet','residue_N2O_kg':'kg_N2O','import_kWh':'kWh',
             'grid_kg_CO2e_per_kWh':'kg_CO2e/kWh'}
    for a in assumptions:
        k = a['input_pointer'][1:]
        if a['unit'] != units.get(k, 'fraction' if k.endswith('_fraction') else 't_fossil_CO2'):
            raise ValueError('PARAMETER_UNIT')
    for row in passport['rights_links']:
        if row['period'] != INTERVAL:
            raise ValueError('RIGHTS_TIME_MISMATCH')
    if passport['revision'] != int(passport['revision']):
        raise ValueError('REVISION_INTEGER')
    date.fromisoformat(passport['legal']['assessment_date'])
    return expected


def bounded(value, name, upper=None):
    return ledger.p.number(value, name, high=math.inf if upper is None else upper)


def methane_path(generated, capture, oxidation, pipe_loss, destruction):
    """Integrated methane interfaces only, evaluated by the frozen PR144 core.

    Its day label is internal to that arithmetic harness. Never export that label
    as this cohort's time support. No rates, kinetics or day/year scaling here.
    """
    g = bounded(generated, 'generated')
    c, o, p, d = [bounded(v, n, 1) for v, n in zip(
        [capture, oxidation, pipe_loss, destruction], ['capture', 'oxidation', 'pipe', 'destruction'])]
    collected = g * c
    cover = g - collected
    leak = collected * p
    device = collected - leak
    f = dict(stock_start=0, generated=g, inflow=0, stock_end=0,
             collected=collected, cover_in=cover, lateral_out=0,
             pipe_leak=leak, pipe_stock_change=0, device_in=device,
             device_slip=device * (1 - d), destroyed=device * d,
             oxidized=cover * o, surface=cover * (1 - o))
    req = ledger.fixture('uncaptured')
    for key, value in f.items():
        req['flows'][key]['value'] = value
    checked = ledger.evaluate(req)
    return dict(interval=INTERVAL, unit='kg_CH4', flows=f,
                emitted_kg_CH4=checked['emitted_kg_CH4'],
                reaction_biogenic_CO2_kg=checked['co2_from_CH4_reaction_kg'],
                residuals=checked['residuals'], kernel=ledger.VERSION,
                kernel_scope='INTERNAL_FIXTURE_REPLAY_ONLY; integral algebra adapter')


def calculate(f):
    if f['mode'] != 'SYNTHETIC' or f['interval'] != INTERVAL or f['waste_unit'] != 't_wet':
        raise ValueError('MODE_UNIT_TIME_NOT_ADMITTED')
    if f['waste_t'] != 1000:
        raise ValueError('ONLY_1000T_AUTHORIZED')
    if set(f) != set(read('fixtures/A.json')):
        raise ValueError('INPUT_FIELDS')
    for key, expected in read('fixtures/A.json').items():
        if type(expected) in (float, int):
            bounded(f[key], key, 1 if key.endswith('_fraction') else None)
    for key in ['residue_CH4_known','residue_N2O_known','leakage_known']:
        if f[key] not in ['YES_SYNTHETIC','UNKNOWN']:
            raise ValueError('UNKNOWN_QUALITY_STATE')
    if f['ad_decomposed_fraction'] + f['residue_decomposed_fraction'] > 1:
        raise ValueError('ORGANIC_CARBON_DOUBLE_USE')
    doc = f['waste_t'] * 1000 * f['doc_fraction']
    def gas(frac):
        return ledger.generation_from_decomposed_carbon(doc * frac, .5)
    baseline = methane_path(gas(f['landfill_decomposed_fraction']), f['capture_fraction'],
                            .1, .01, .98)
    ch4_gwp, n2o_gwp = 27.2, 273.0
    b = baseline['emitted_kg_CH4'] / 1000 * ch4_gwp + f['baseline_fossil_CO2_t']
    out = dict(mode='SYNTHETIC', interval=INTERVAL, waste_t=1000,
               physical_coherence='COHERENT_WITHIN_SYNTHETIC_CH4_BOUNDARY',
               physical_ledger={'landfill': baseline, 'organic_carbon_kg': doc,
                  'carbon_scope':'CH4-path carbon conserved; no full waste LCA',
                  'dispersion':'NOT_COMPUTED_NO_CONCENTRATION_INVERSION'},
               baseline_t_CO2e=b, project_t_CO2e=None, leakage_t_CO2e=None,
               estimated_net_abatement_t_CO2e=None, credit_quantity='NOT_DETERMINED',
               gwp={'CH4_nonfossil':ch4_gwp,'N2O':n2o_gwp,'source':'IPCC_AR6_WGI_TABLE_7_15',
                    'basis':'GWP100 research metric, not NGER/ACCU factor'},
               real_data='DATA_NOT_READY', science='PENDING', unknowns=[])
    if f['route'] == 'LANDFILL_IDENTITY':
        out.update(project_t_CO2e=b, leakage_t_CO2e=0, estimated_net_abatement_t_CO2e=0,
                   accounting_status='SYNTHETIC_IDENTITY_CONTROL')
        out['physical_ledger']['project'] = deepcopy(baseline)
        return out
    if f['route'] != 'AD_WITH_RESIDUE_LANDFILL':
        raise ValueError('UNKNOWN_ROUTE')
    ad = methane_path(gas(f['ad_decomposed_fraction']), f['ad_capture_fraction'], 0,
                      f['ad_pipe_loss_fraction'], .98)
    out['physical_ledger']['AD'] = ad
    required = ['residue_CH4_known', 'residue_N2O_known', 'leakage_known']
    if any(f[k] != 'YES_SYNTHETIC' for k in required):
        out.update(accounting_status='INSUFFICIENT_EVIDENCE',
                   unknowns=[k for k in required if f[k] != 'YES_SYNTHETIC'])
        return out  # unknown residue/leakage is never zero or an apparently complete net
    residue = methane_path(gas(f['residue_decomposed_fraction']), .2, .1, .01, .98)
    out['physical_ledger']['residue_landfill'] = residue
    energy = f['import_kWh'] * f['grid_kg_CO2e_per_kWh'] / 1000
    project = ((ad['emitted_kg_CH4'] + residue['emitted_kg_CH4']) / 1000 * ch4_gwp
               + f['residue_N2O_kg'] / 1000 * n2o_gwp + energy
               + f['project_fossil_CO2_t'] + f['transport_fossil_CO2_t'])
    leakage = f['offsite_leakage_fossil_CO2_t']
    out.update(project_t_CO2e=project, leakage_t_CO2e=leakage,
               estimated_net_abatement_t_CO2e=b - project - leakage,
               accounting_status='CONDITIONAL_SYNTHETIC_NOT_STATUTORY',
               component_t_CO2e={'import_electricity':energy,
                    'residue_N2O':f['residue_N2O_kg']/1000*n2o_gwp,
                    'AD_CH4':ad['emitted_kg_CH4']/1000*ch4_gwp,
                    'residue_CH4':residue['emitted_kg_CH4']/1000*ch4_gwp,
                    'fuel':f['project_fossil_CO2_t'], 'transport':f['transport_fossil_CO2_t'],
                    'offsite_only_leakage':leakage},
               energy_export_credit_t_CO2e=0,
               energy_export_policy='EXCLUDED_NO_DISPLACEMENT_EVIDENCE_NO_DOUBLE_SUBTRACTION')
    return out


def legal_screen(x):
    """Dated, deliberately incomplete screening; never a statutory determination."""
    day = date.fromisoformat(x['assessment_date'])
    if x['jurisdiction'] != 'AU-NSW' or x['premises'] != 'HOUSEHOLD_COUNCIL_RED_BIN':
        collection = 'UNKNOWN_OUTSIDE_IMPLEMENTED_SCOPE'
    elif day < date(2030, 7, 1):
        collection = 'NOT_YET_DUE_UNDER_REVIEWED_HOUSEHOLD_RULE'
    elif x['exemption'] != 'NO_SYNTHETIC_ASSUMPTION':
        collection = 'UNKNOWN_EXEMPTION_NOT_VERIFIED'
    else:
        collection = 'CONDITIONALLY_IN_SCOPE_REVERIFY_LAW_AT_EVENT_DATE'
    method = 'INSUFFICIENT_EVIDENCE'
    reason = 'REGISTRATION_AND_TRANSITION_NOT_VERIFIED'
    if x['method'] == 'AWT_2015' and x['registration'] == 'NEW' and day > date(2025, 3, 31):
        method, reason = 'NOT_ELIGIBLE', 'EXPIRED_METHOD_NEW_REGISTRATION_ONLY'
    elif x['method'] == 'AWT_2026_PROPOSAL':
        reason = 'CONSULTATION_IS_NOT_ENACTED_METHOD'
    return dict(collection=collection,
                required_processing_pathway='AD_SPECIFIC_REQUIREMENT_NOT_ESTABLISHED',
                additionality='INSUFFICIENT_EVIDENCE', eligibility=method, reason=reason,
                source_ids=['DCCEEW_AWT','FRL_AWT2015','EPA_FOGO','EPA_EXEMPTIONS'],
                formal_legal_determination=False,
                as_of='2026-11-23', transition='LEGACY_PROJECT_CREDITING_PERIOD_REQUIRES_EVIDENCE')


def overlap(links):
    seen = {}
    risks = []
    for row in links:
        key = (row['batch'], row['period'], row['quantity_boundary'])
        if key in seen:
            risks.append({'batch':row['batch'], 'mechanisms':[seen[key],row['mechanism']],
                          'status':'POTENTIAL_OVERLAP_NOT_PROVEN_DOUBLE_ISSUANCE'})
        seen[key] = row['mechanism']
    return risks


def assess(passport):
    result = dict(science='PENDING', human_review='PENDING', real_data='DATA_NOT_READY',
                  credit_quantity='NOT_DETERMINED', assurance='INSUFFICIENT_EVIDENCE',
                  calculation=None, reasons=[], legal=None, duplicate_risks=[])
    try:
        fixture = validate(passport)
        result['calculation'] = calculate(fixture)
    except (ValueError, TypeError, KeyError) as exc:
        result.update(assurance='CONDITIONS_NOT_MET', reasons=[str(exc)])
        return result
    result['legal'] = legal_screen(passport['legal'])
    result['observation'] = deepcopy(passport['observation'])
    result['duplicate_risks'] = overlap(passport['rights_links'])
    result['reasons'] = ['SYNTHETIC_NOT_SITE_EVIDENCE', 'INDEPENDENT_REVIEW_PENDING',
                         'PARAMETER_INTERVALS_NOT_EMPIRICAL_CONFIDENCE']
    if passport['baseline_evidence'] != 'SYNTHETIC_ASSUMPTIONS_ONLY':
        result['reasons'].append('BASELINE_EVIDENCE_MISSING')
    result['reasons'] += result['calculation']['unknowns']
    if result['duplicate_risks']:
        result['reasons'].append('MATERIAL_BATCH_RIGHTS_RECONCILIATION_REQUIRED')
    if passport['scenario'] == 'C':
        result['reasons'].append('LANDFILL_COUNTERFACTUAL_UNDER_MANDATE_UNPROVEN')
    result['reasons'].append(result['legal']['reason'])
    return result


RANGES = {'capture_fraction':[.24,.75], 'landfill_decomposed_fraction':[.4,.6],
          'ad_capture_fraction':[.90,.99], 'ad_pipe_loss_fraction':[.005,.03],
          'residue_decomposed_fraction':[.05,.2], 'residue_N2O_kg':[50,300],
          'grid_kg_CO2e_per_kWh':[.4,.9]}


def sensitivity(f):
    # Common assumptions shared across baseline/project; A cancels identically.
    if calculate(f)['estimated_net_abatement_t_CO2e'] is None:
        return {'status':'NOT_BOUNDED_MISSING_RESIDUE', 'bounds':None, 'runs':0}
    runs = []
    for values in itertools.product(*RANGES.values()):
        case = dict(f, **dict(zip(RANGES, values)))
        result = calculate(case)
        runs.append({'parameters':dict(zip(RANGES, values)), 'net_t_CO2e':result['estimated_net_abatement_t_CO2e']})
    return {'status':'SYNTHETIC_CORNER_ENVELOPE_NOT_CONFIDENCE_INTERVAL',
            'bounds':[min(r['net_t_CO2e'] for r in runs),max(r['net_t_CO2e'] for r in runs)],
            'runs':len(runs), 'cases':runs,
            'limits':'Fixed GWP and all unlisted inputs. No probability distribution or whole-system uncertainty.'}


def revision(previous, changed):
    """Immutable append preparation; history externally anchored by Git, not signature."""
    if changed['claim_id'] != previous['claim_id']:
        raise ValueError('CLAIM_ID_CHANGED')
    updated = deepcopy(changed)
    updated['revision'] = previous['revision'] + 1
    updated['previous_revision_sha256'] = prior.digest(previous)
    validate(updated)
    return updated


def main():
    results = {s:assess(read('examples/'+s+'.json')) for s in 'ABCD'}
    ranges = {s:sensitivity(read('fixtures/'+s+'.json')) for s in 'ABCD'}
    events = prior.append_event([], 'SUBMITTED', 'SYNTHETIC_SUBMITTER', prior.digest(read('examples/A.json')))
    # No fabricated human REVIEWED event. Submission chain only.
    outputs = {'results.json':results, 'sensitivities.json':ranges, 'submission-events.json':events}
    for name, value in outputs.items():
        (HERE/'evidence'/name).write_text(json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({s:{'net_t_CO2e':r['calculation']['estimated_net_abatement_t_CO2e'] if r['calculation'] else None,
                         'assurance':r['assurance']} for s,r in results.items()},ensure_ascii=False))


if __name__ == '__main__':
    main()
