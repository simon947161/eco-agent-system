"""Bounded offline SYNTHETIC_METHOD_TEST; not a facility or regulatory calculator.

Inventory entries are interval-integrated kg CH4, including gas+dissolved stock.
Reuses frozen PR143 conservation checks and PR138 gas-state functions. No solver,
network, credit calculation, real-data ingestion, or scientific admission route.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from cczps_lite.integration import physics_validation as p
from cczps_lite.integration.methane_knowledge_engine import conserve, require

VERSION = 'AUTHOR_LEDGER_V1_NOT_NGER_NOT_ACCU'
FLOW_KEYS = {'stock_start', 'generated', 'inflow', 'stock_end', 'collected',
             'cover_in', 'lateral_out', 'pipe_leak', 'pipe_stock_change',
             'device_in', 'device_slip', 'destroyed', 'oxidized', 'surface'}
META_KEYS = {'mode', 'version', 'gas', 'phase', 'unit', 'interval', 'source_id',
             'licence', 'calibration', 'uncertainty', 'flows'}


def evaluate(request):
    """Validate independent interface readings before computing global residuals.

No optional zero. Unknown quantities fail. This arithmetic harness deliberately
rejects real observations. It cannot certify whether a user-labelled synthetic
number is truly synthetic; reviewer/source checks remain necessary.
"""
    require(set(request) == META_KEYS, 'REQUEST_SCHEMA')
    for key, expected in [('mode', 'SYNTHETIC_METHOD_TEST'), ('version', VERSION),
                          ('gas', 'CH4'), ('phase', 'total_CH4_gas_plus_dissolved'),
                          ('unit', 'kg_CH4/interval'),
                          ('licence', 'AUTHOR_SYNTHETIC_CC0'),
                          ('calibration', 'SYNTHETIC_NOT_FIELD')]:
        require(request[key] == expected, key.upper() + '_NOT_ADMITTED')
    require(request['source_id'] == 'SYNTHETIC_TASKBOOK_LEDGER', 'UNSOURCED')
    require(request['uncertainty'] == 'EXACT_ARITHMETIC_FIXTURE_NOT_FIELD_UNCERTAINTY',
            'UNCERTAINTY_NOT_DECLARED')
    require(request['interval'] == 'SYNTHETIC_DAY_001', 'TIME_SUPPORT')
    flows = request['flows']
    require(set(flows) == FLOW_KEYS, 'MISSING_OR_EXTRA_FLOW')
    f = {}
    for key, entry in flows.items():
        require(set(entry) == {'value', 'unit', 'interval'}, 'ENTRY_SCHEMA')
        require(entry['unit'] == request['unit'], 'UNIT_MISMATCH')
        require(entry['interval'] == request['interval'], 'TIME_MISMATCH')
        # This bounded three-case harness allows positive accumulation only.
        f[key] = p.number(entry['value'], key)
    residuals = {
        'body': conserve(f['stock_start'] + f['generated'] + f['inflow'],
                         f['stock_end'] + f['collected'] + f['cover_in'] + f['lateral_out']),
        'pipe': conserve(f['collected'], f['device_in'] + f['pipe_leak'] + f['pipe_stock_change']),
        'device': conserve(f['device_in'], f['destroyed'] + f['device_slip']),
        'cover': conserve(f['cover_in'], f['oxidized'] + f['surface']),
    }
    emitted = f['surface'] + f['pipe_leak'] + f['device_slip']
    consumed = f['destroyed'] + f['oxidized']
    start = f['stock_start'] + f['generated'] + f['inflow']
    end_ch4 = f['stock_end'] + f['pipe_stock_change'] + emitted + f['lateral_out']
    residuals['CH4'] = conserve(start, end_ch4 + consumed)
    # Declared integer stoichiometric convention, distinct from ideal-gas M_CH4.
    co2 = consumed * 44 / 16
    residuals['carbon'] = conserve(start * 12 / 16, end_ch4 * 12 / 16 + co2 * 12 / 44)
    return {'status': 'SYNTHETIC_METHOD_TEST', 'version': VERSION,
            'emitted_kg_CH4': emitted, 'consumed_kg_CH4': consumed,
            'co2_from_CH4_reaction_kg': co2,
            'carbon_in_kg_C': start * 12 / 16,
            'carbon_out_plus_stock_kg_C': end_ch4 * 12 / 16 + co2 * 12 / 44,
            'residuals': residuals,
            'unknown_field_uncertainty': True, 'regulatory_admission': 'NOT_APPLICABLE'}


def generation_from_decomposed_carbon(kg_c, methane_carbon_fraction):
    """IPCC 2006 Eq3.6 conversion only; no FOD simulation/default k."""
    return p.number(kg_c, 'decomposed carbon') * p.number(methane_carbon_fraction, 'F', high=1) * p.IPCC_CH4_C_RATIO


def flow_mass(*, volume, unit, x_dry, pressure_pa, temperature_k, vapour_pa,
              gas='CH4', phase='gas', source='SYNTHETIC', calibration='SYNTHETIC_NOT_FIELD'):
    """Known enclosed gas quantity only: never an ambient plume source inversion."""
    require(unit == 'm3_wet_actual', 'EXPLICIT_ACTUAL_VOLUME_REQUIRED')
    require(gas == 'CH4' and phase == 'gas', 'WRONG_GAS_OR_PHASE')
    require(source == 'SYNTHETIC' and calibration == 'SYNTHETIC_NOT_FIELD', 'PROVENANCE')
    v = p.number(volume, 'volume')
    density = p.gas_properties(x_dry, pressure_pa, temperature_k, vapour_pa)['mass_concentration_kg_per_m3']
    # NGER dry standard conditions are 15 C, not the P1 function's default 0 C.
    v15 = p.reference_dry_volume(v, pressure_pa, temperature_k, vapour_pa,
                               p_ref_pa=101325, t_ref_k=288.15)
    m15 = v15 * p.gas_properties(x_dry, 101325, 288.15, 0)['mass_concentration_kg_per_m3']
    conserve(v * density, m15)
    return {'kg_CH4': v * density, 'm3_dry_15C_101325Pa': v15,
            'scope': 'ideal-gas physics; not statutory NGER gamma factor'}


def flux_chamber(*, volume_m3, area_m2, slope_mg_m3_s):
    """NGER s5.17H algebra/units demonstration, synthetic only, not a field fit."""
    return p.number(volume_m3, 'V', strict_low=True) / p.number(area_m2, 'A', strict_low=True) * p.number(slope_mg_m3_s, 'dc/dt')


def operation_hour(minutes, volume_interval, operation_interval):
    """ACCU s78 item2 Eq11 coverage contract, NOT a credit/combustion calculator."""
    require(volume_interval == operation_interval, 'PAIRING_MISMATCH')
    require(len(minutes) == 60 and all(type(x) is bool for x in minutes), 'MONITORING_GAP')
    return int(all(minutes))


def validate_graph(nodes, edges):
    require(len(nodes) == len(set(nodes)), 'DUPLICATE_NODE')
    require(all(a in nodes and b in nodes for a, b in edges), 'BROKEN_LINK')
    return True


def fixture(name):
    # All inputs are invented analytical fixtures, no case-study measurements.
    common = dict(stock_start=10, generated=100, inflow=0, stock_end=15,
                  collected=0, cover_in=95, lateral_out=0, pipe_leak=0,
                  pipe_stock_change=0, device_in=0, device_slip=0,
                  destroyed=0, oxidized=0, surface=95)
    if name == 'capture_flare':
        common.update(collected=60, cover_in=35, device_in=60, device_slip=1.2,
                      destroyed=58.8, oxidized=3.5, surface=31.5)
    elif name == 'oxidation_leaks':
        common.update(collected=60, cover_in=30, lateral_out=5, pipe_leak=6,
                      device_in=54, device_slip=1.08, destroyed=52.92,
                      oxidized=6, surface=24)
    else:
        require(name == 'uncaptured', 'UNKNOWN_FIXTURE')
    return dict(mode='SYNTHETIC_METHOD_TEST', version=VERSION, gas='CH4',
                phase='total_CH4_gas_plus_dissolved', unit='kg_CH4/interval',
                interval='SYNTHETIC_DAY_001', source_id='SYNTHETIC_TASKBOOK_LEDGER',
                licence='AUTHOR_SYNTHETIC_CC0', calibration='SYNTHETIC_NOT_FIELD',
                uncertainty='EXACT_ARITHMETIC_FIXTURE_NOT_FIELD_UNCERTAINTY',
                flows={k: {'value': v, 'unit': 'kg_CH4/interval', 'interval': 'SYNTHETIC_DAY_001'} for k, v in common.items()})
