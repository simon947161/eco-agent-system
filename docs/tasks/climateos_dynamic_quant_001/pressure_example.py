"""Hypothetical dry ideal-gas arithmetic, not a site or radiation model."""
import json
import math


def example():
    x, temperature = 2e-6, 293.15
    gas_constant, methane_molar_mass, air_molar_mass = 8.31446261815324, 0.016043, 0.028965
    rows = []
    for pressure in (101325, 80000):
        rows.append({'pressure_pa': pressure, 'temperature_k': temperature,
                     'dry_mole_fraction_ppm': x * 1e6,
                     'methane_mg_per_actual_m3': x * pressure * methane_molar_mass / (gas_constant * temperature) * 1e6,
                     'mass_mixing_ratio_mg_per_kg_dry_air': x * methane_molar_mass / air_molar_mass * 1e6})
    assert math.isclose(rows[1]['methane_mg_per_actual_m3'] / rows[0]['methane_mg_per_actual_m3'], 80000/101325)
    assert rows[0]['mass_mixing_ratio_mg_per_kg_dry_air'] == rows[1]['mass_mixing_ratio_mg_per_kg_dry_air']
    return {'evidence_class': 'HYPOTHETICAL_ARITHMETIC_NOT_OBSERVATION',
            'assumptions': 'Dry ideal gas; same mole fraction and temperature; no source/sink/mixing; no altitude assigned',
            'constants': {'R_J_per_mol_K': gas_constant, 'M_CH4_kg_per_mol': methane_molar_mass, 'M_dry_air_kg_per_mol_assumed': air_molar_mass},
            'cases': rows, 'emissions': 'NOT_COMPUTED', 'radiative_forcing': 'NOT_COMPUTED', 'warming': 'NOT_COMPUTED'}


if __name__ == '__main__':
    print(json.dumps(example(), indent=2, allow_nan=False))
