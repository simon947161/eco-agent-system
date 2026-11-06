"""CLIMATEOS-PHYSICS-VALIDATION-001, synthetic/reference verification only.

Stdlib numerical core. No network, site-data reader, statutory calculation or
changes to the historical no-run gates. Units are SI except explicit Gg/years.
"""
from __future__ import annotations

import math

R = 8.31446261815324  # J mol-1 K-1
M_CH4 = 0.016043  # kg mol-1, P1/P2 ideal gas convention
M_AIR = 0.028965  # kg mol-1, declared assumed dry-air mean
GG_TO_KG = 1_000_000
IPCC_CH4_C_RATIO = 16 / 12  # IPCC 2006 convention, distinct from gas molar mass


def number(value, name, low=0.0, high=math.inf, strict_low=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f'{name}: finite real required')
    if value > high or value < low or (strict_low and value == low):
        raise ValueError(f'{name}: outside declared domain')
    return float(value)


def gas_properties(x_dry, pressure_pa, temperature_k, vapour_pa=0.0):
    """c=x_dry(P-e)M/RT; x_wet=x_dry(P-e)/P; r=x_dry M/Mair."""
    x = number(x_dry, 'x_dry', high=1)
    p = number(pressure_pa, 'pressure_pa', strict_low=True)
    t = number(temperature_k, 'temperature_k', strict_low=True)
    e = number(vapour_pa, 'vapour_pa')
    if e >= p:
        raise ValueError('vapour pressure must be below total pressure')
    return {'x_dry_mol_per_mol': x, 'x_wet_mol_per_mol': x * (p-e)/p,
            'mass_concentration_kg_per_m3': x * (p-e)*M_CH4/(R*t),
            'mass_mixing_ratio_kg_per_kg_dry_air': x*M_CH4/M_AIR}


def dry_fraction_from_concentration(c_kg_m3, p_pa, t_k, e_pa=0):
    gas_properties(0, p_pa, t_k, e_pa)
    c = number(c_kg_m3, 'concentration')
    x = c*R*t_k/((p_pa-e_pa)*M_CH4)
    return number(x, 'derived_x_dry', high=1)


def dry_fraction_from_wet(x_wet, p_pa, e_pa=0):
    gas_properties(0, p_pa, 293.15, e_pa)
    return number(number(x_wet, 'x_wet', high=1)*p_pa/(p_pa-e_pa), 'derived_x_dry', high=1)


def reference_dry_volume(actual_wet_m3, p_pa, t_k, e_pa=0, p_ref_pa=101325, t_ref_k=273.15):
    """Same dry gas amount: Vref=V(P-e)/Pref*Tref/T. CH4 mass conserved."""
    gas_properties(0, p_pa, t_k, e_pa)
    gas_properties(0, p_ref_pa, t_ref_k)
    return number(actual_wet_m3, 'actual_wet_volume')*(p_pa-e_pa)/p_ref_pa*t_ref_k/t_k


def storage_run(*, slope_pa_h=0, duration_h=24, dt_h=.125, conductance_kg_h_pa=2e-6,
                generation_kg_h=.001, volume_m3=1, temperature_k=293.15,
                external_initial_pa=101325, initial_overpressure_pa=500):
    """Pure-CH4 surrogate box: Pi=a*m; v=C*max(Pi-Pe,0); m'=g-v.

    Explicit Euler, left-end flux integral. C*a*dt<=1 ensures positivity for
    g>=0 and Pe>0, without clipping stock or hiding a mass residual. The valve
    forbids inflow. Synthetic parameters are not a porous landfill constitutive
    law and pure CH4 is not an ambient-air assumption.
    """
    number(slope_pa_h, 'slope', low=-math.inf)
    duration = number(duration_h, 'duration', strict_low=True)
    dt = number(dt_h, 'dt', strict_low=True)
    c = number(conductance_kg_h_pa, 'conductance')
    g = number(generation_kg_h, 'generation')
    v = number(volume_m3, 'volume', strict_low=True)
    t = number(temperature_k, 'temperature', strict_low=True)
    p0 = number(external_initial_pa, 'external_initial', strict_low=True)
    delta0 = number(initial_overpressure_pa, 'initial_overpressure', low=-math.inf)
    if min(p0, p0+slope_pa_h*duration) <= 0 or p0+delta0 < 0:
        raise ValueError('nonpositive boundary pressure or negative initial inventory')
    a = R*t/(M_CH4*v)  # Pa/kg
    if c*a*dt > 1:
        raise ValueError('positivity/stability bound C*a*dt<=1 exceeded')
    n = round(duration/dt)
    if n < 1 or not math.isclose(n*dt, duration, abs_tol=1e-10):
        raise ValueError('duration must be an integral number of timesteps')
    initial = (p0+delta0)/a
    mass, integrated_out = initial, 0.0
    rows = []
    for i in range(n):
        time = i*dt
        pe = p0+slope_pa_h*time
        pi = a*mass
        vent = c*max(pi-pe, 0)
        next_mass = mass+(g-vent)*dt
        rows.append({'time_h': time, 'external_pa': pe, 'internal_pa': pi,
                     'differential_pa': pi-pe, 'pressure_tendency_pa_h': slope_pa_h,
                     'stock_kg_start': mass, 'generation_kg_h': g, 'vent_kg_h': vent,
                     'stock_kg_end': next_mass})
        mass = next_mass
        integrated_out += vent*dt
    residual = math.fsum([initial, g*duration, -math.fsum(r['vent_kg_h']*dt for r in rows), -mass])
    return {'class': 'HYPOTHETICAL_UNCALIBRATED_PURE_CH4_BOX', 'rows': rows,
            'initial_kg': initial, 'final_kg': mass, 'input_kg': g*duration,
            'vented_kg': integrated_out, 'residual_kg': residual, 'dt_h': dt,
            'stability_number': c*a*dt, 'pressure_per_mass_pa_kg': a,
            'minimum_stock_kg': min([initial]+[r['stock_kg_end'] for r in rows])}


def fod_run(waste_gg, k_per_year=.1, doc=.15, docf=.5, mcf=1,
            methane_fraction=.5, recovered_fraction=.4, oxidation_fraction=.1,
            initial_ddoc_gg_c=.5, rate_multipliers=None):
    """IPCC 2006 annual Eqs 3.1,3.2,3.4-3.6; synthetic parameters.

    A_T=D_T+A_(T-1)*exp(-k_T); decomp=A_(T-1)*(1-exp(-k_T)).
    Annual deposition is added AFTER decay (next-Jan-1 start, average 6-month
    delay). Each annual input and inherited stock is separately tracked.
    Recovery is a declared synthetic fraction of generation, then oxidation of
    the unrecovered remainder. No additional gas-storage state or P2 coupling.
    """
    if not isinstance(waste_gg, (list, tuple)) or not waste_gg:
        raise ValueError('nonempty annual history required')
    k = number(k_per_year, 'k_per_year')
    fractions = [number(x, name, high=1) for x,name in [(doc,'DOC'),(docf,'DOCf'),(mcf,'MCF'),
                 (methane_fraction,'F'),(recovered_fraction,'recovery'),(oxidation_fraction,'OX')]]
    doc, docf, mcf, methane_fraction, recovered_fraction, oxidation_fraction = fractions
    initial = number(initial_ddoc_gg_c, 'initial_ddoc')
    multipliers = [1.0]*len(waste_gg) if rate_multipliers is None else rate_multipliers
    if len(multipliers) != len(waste_gg):
        raise ValueError('annual multiplier length mismatch')
    cohorts = {-1: initial}
    rows = []
    for year, (w, factor) in enumerate(zip(waste_gg, multipliers)):
        deposit = number(w, 'waste_Gg')*doc*docf*mcf
        effective_k = k*number(factor, 'rate_multiplier')
        start = math.fsum(cohorts.values())
        decomp = start*(-math.expm1(-effective_k))
        cohorts = {cid: stock*math.exp(-effective_k) for cid,stock in cohorts.items()}
        cohorts[year] = deposit
        end = math.fsum(cohorts.values())
        generation = decomp*methane_fraction*IPCC_CH4_C_RATIO
        recovered = generation*recovered_fraction
        oxidised = (generation-recovered)*oxidation_fraction
        emitted = (generation-recovered)*(1-oxidation_fraction)
        rows.append({'year_index': year, 'waste_Gg': w, 'deposit_Gg_C': deposit,
                     'start_DDOC_Gg_C': start, 'end_DDOC_Gg_C': end,
                     'decomposed_Gg_C': decomp, 'effective_k_per_year': effective_k,
                     'generated_CH4_Gg': generation, 'recovered_CH4_Gg': recovered,
                     'oxidised_CH4_Gg': oxidised, 'emitted_CH4_Gg': emitted,
                     'carbon_residual_Gg_C': math.fsum([start, deposit, -decomp, -end]),
                     'methane_partition_residual_Gg': math.fsum([generation,-recovered,-oxidised,-emitted]),
                     'cohorts_end_Gg_C': {str(cid):stock for cid,stock in cohorts.items()}})
    total_deposit = math.fsum(row['deposit_Gg_C'] for row in rows)
    return {'class':'IPCC_2006_ANNUAL_FORMULA_SYNTHETIC_INPUTS_NOT_OFFICIAL_REFERENCE_RESULT',
            'rows':rows, 'total_emitted_CH4_Gg':math.fsum(r['emitted_CH4_Gg'] for r in rows),
            'total_generated_CH4_Gg':math.fsum(r['generated_CH4_Gg'] for r in rows),
            'final_DDOC_Gg_C':rows[-1]['end_DDOC_Gg_C'],
            'carbon_residual_Gg_C':math.fsum([initial,total_deposit,-math.fsum(r['decomposed_Gg_C'] for r in rows),-rows[-1]['end_DDOC_Gg_C']]),
            'delay_convention':'deposition year no decay; next January 1 onset; average six-month delay',
            'temporal_step':'one year, exactly integrated first-order loss for piecewise-constant annual k'}


def temperature_multiplier(temperature_k, activation_j_mol=30000, reference_k=293.15):
    """Normalized Arrhenius family; synthetic Ea, no inferred site kinetics."""
    t = number(temperature_k, 'temperature_k', strict_low=True)
    ref = number(reference_k, 'reference_k', strict_low=True)
    ea = number(activation_j_mol, 'activation_J_mol', high=100000)
    if not 250 <= t <= 330 or not 250 <= ref <= 330:
        raise ValueError('outside illustrative 250-330K response domain')
    return math.exp(-ea/R*(1/t-1/ref))


def moisture_multiplier(theta, reference=.5):
    """Own bounded linear hypothesis, no empirical methane response claimed.

    theta is a dimensionless normalized moisture index, NOT rainfall or a
    measured volumetric water content. Family is linear interpolation through
    (0,0),(reference,1),(1,2), with a distinct slope after the reference point.
    """
    x = number(theta, 'normalized_moisture', high=1)
    ref = number(reference, 'reference_moisture', high=1, strict_low=True)
    if ref == 1:
        raise ValueError('moisture reference must be strictly below 1')
    return x/ref if x <= ref else 1+(x-ref)/(1-ref)
