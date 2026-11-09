"""Reproduce the three explicitly authorized offline ledger fixtures."""
import json
from pathlib import Path
from mass_balance import evaluate, fixture, flow_mass, flux_chamber, operation_hour, generation_from_decomposed_carbon

TASK = Path(__file__).resolve().parent

def main():
    out = TASK / 'evidence'; out.mkdir(exist_ok=True)
    inputs = {n: fixture(n) for n in ['uncaptured','capture_flare','oxidation_leaks']}
    results = {n: evaluate(r) for n,r in inputs.items()}
    examples = {'classification':'AUTHOR_DERIVED_SYNTHETIC_EXAMPLE',
                'IPCC2006_Eq3_6_12kgC_F0_5_kgCH4':generation_from_decomposed_carbon(12,.5),
                'NGER_5_17H_mgCH4_m2_s':flux_chamber(volume_m3=.1,area_m2=.2,slope_mg_m3_s=2),
                'ACCU_78_item2_60_valid_minutes':operation_hour([True]*60,'h1','h1'),
                'ACCU_78_item2_one_invalid_minute':operation_hour([True]*59+[False],'h1','h1'),
                'P1_known_enclosed_gas':flow_mass(volume=100,unit='m3_wet_actual',x_dry=.5,pressure_pa=101325,temperature_k=293.15,vapour_pa=2000)}
    for name, data in [('synthetic-inputs.json',inputs),('synthetic-results.json',results),('worked-examples.json',examples)]:
        (out/name).write_text(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps({'status':'SYNTHETIC_METHOD_TEST','cases':list(results),'actual_facility_estimates':0}))

if __name__ == '__main__': main()
