"""Run the authorized deterministic synthetic/reference batch and real charts.

From repository root: D:/apps/Python312/python.exe run_physics_validation.py
No networking. Inputs, formulas, test records and outputs are separate files.
"""
import csv
import hashlib
import importlib.metadata
import json
import math
import platform
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from cczps_lite.integration import physics_validation as p

ROOT = Path(__file__).resolve().parent
TASK = ROOT/'docs/tasks/climateos_physics_validation_001'


def write_json(name, data):
    (TASK/name).write_text(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')


def write_csv(name, rows):
    keys=[k for k in rows[0] if not isinstance(rows[0][k],dict)]
    with (TASK/name).open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,keys,extrasaction='ignore');writer.writeheader();writer.writerows(rows)


def chart(name, series, xlabel, ylabel, title, extra=None):
    fig,ax=plt.subplots(figsize=(9.5,4.2),layout='constrained')
    for label,x,y in series:ax.plot(x,y,label=label,linewidth=2)
    ax.set(xlabel=xlabel,ylabel=ylabel,title=title)
    ax.grid(alpha=.2);ax.legend(fontsize=9)
    if extra:extra(ax)
    fig.savefig(TASK/'charts'/f'{name}.svg',metadata={'Date':None})
    plt.close(fig)


def main():
    cfg=json.loads((TASK/'inputs.json').read_text())
    (TASK/'charts').mkdir(exist_ok=True)
    matplotlib.rcParams.update({'svg.hashsalt':'CLIMATEOS-PHYSICS-VALIDATION-001','font.size':11})
    c1=cfg['P1'];gas=[]
    for pressure in c1['pressures_pa']:
        for water in c1['water_vapour_pa']:
            r=p.gas_properties(c1['x_dry'],pressure,c1['temperature_k'],water)
            r.update(pressure_pa=pressure,vapour_pa=water,temperature_k=c1['temperature_k'],
                     reference_dry_volume_per_actual_wet_m3=p.reference_dry_volume(1,pressure,c1['temperature_k'],water))
            gas.append(r)
    write_json('p1.json',{'class':'HYPOTHETICAL_IDEAL_GAS','rows':gas});write_csv('p1.csv',gas)
    pressures=list(range(70000,105001,1000))
    chart('p1-pressure',[(f'{t} K',pressures,[p.gas_properties(2e-6,x,t)['mass_concentration_kg_per_m3']*1e6 for x in pressures]) for t in [283.15,293.15,303.15]],'Absolute pressure (Pa)','CH4 (mg / actual m3)','P1 synthetic: fixed dry 2 ppm')
    waters=list(range(0,2001,100))
    chart('p1-water',[(f'{pr} Pa',waters,[p.gas_properties(2e-6,pr,293.15,e)['mass_concentration_kg_per_m3']*1e6 for e in waters]) for pr in [80000,101325]],'Water-vapour partial pressure (Pa)','CH4 (mg / actual wet m3)','P1 dry fraction fixed, water displaces dry air')
    c2=cfg['P2'];kwargs={k:c2[k] for k in ['duration_h','dt_h','conductance_kg_h_pa','generation_kg_h','volume_m3','temperature_k','external_initial_pa','initial_overpressure_pa']}
    storage={name:p.storage_run(slope_pa_h=s,**kwargs) for name,s in c2['slope_scenarios_pa_h'].items()}
    storage['sealed']=p.storage_run(**{**kwargs,'conductance_kg_h_pa':0})
    storage['zero_generation']=p.storage_run(slope_pa_h=-100,**{**kwargs,'generation_kg_h':0})
    storage['underpressure']=p.storage_run(**{**kwargs,'generation_kg_h':0,'initial_overpressure_pa':-1000})
    convergence=[]
    for dt in c2['convergence_dt_h']:
        r=p.storage_run(slope_pa_h=-100,**{**kwargs,'dt_h':dt})
        a=r['pressure_per_mass_pa_kg'];lam=kwargs['conductance_kg_h_pa']*a
        delta_eq=(a*kwargs['generation_kg_h']+100)/lam
        delta=delta_eq+(kwargs['initial_overpressure_pa']-delta_eq)*math.exp(-lam*kwargs['duration_h'])
        exact=(kwargs['external_initial_pa']-100*kwargs['duration_h']+delta)/a
        convergence.append({'dt_h':dt,'final_kg':r['final_kg'],'analytic_final_kg':exact,'absolute_error_kg':abs(r['final_kg']-exact),'mass_residual_kg':r['residual_kg']})
    write_json('p2.json',{'runs':storage,'convergence':convergence})
    write_csv('p2-convergence.csv',convergence)
    for name,r in storage.items():write_csv(f'p2-{name}.csv',r['rows'])
    chart('p2-vent',[(name,[x['time_h'] for x in r['rows']],[x['vent_kg_h']*1000 for x in r['rows']]) for name,r in storage.items() if name in ['falling','steady','rising']],'Time (h)','Venting (g CH4 / h)','P2 hypothetical one-way pure-CH4 box')
    chart('p2-convergence',[('Euler vs analytic',[x['dt_h'] for x in convergence],[x['absolute_error_kg'] for x in convergence])],'Step size (h)','Final-stock absolute error (kg)','P2 analytic ramp oracle',lambda ax:(ax.set_xscale('log'),ax.set_yscale('log')))
    c3=cfg['P3'];baseargs={k:c3[k] for k in ['waste_gg','k_per_year','doc','docf','mcf','methane_fraction','recovered_fraction','oxidation_fraction','initial_ddoc_gg_c']}
    base=p.fod_run(**baseargs);write_json('p3.json',base);write_csv('p3.csv',base['rows'])
    years=[r['year_index'] for r in base['rows']]
    chart('p3-stock',[(label,years,[r[key] for r in base['rows']]) for label,key in [('DDOC stock (Gg C)','end_DDOC_Gg_C'),('New DDOC (Gg C)','deposit_Gg_C'),('Decomposed (Gg C)','decomposed_Gg_C')]],'Inventory year index','Gg carbon','P3 IPCC 2006 formula, SYNTHETIC inputs')
    chart('p3-partition',[(label,years,[r[key] for r in base['rows']]) for label,key in [('Generated','generated_CH4_Gg'),('Recovered','recovered_CH4_Gg'),('Oxidised','oxidised_CH4_Gg'),('Emitted','emitted_CH4_Gg')]],'Inventory year index','Gg CH4 per annual interval','P3 generated = recovered + oxidised + emitted')
    c4=cfg['P4'];tf=[p.temperature_multiplier(t,c4['activation_j_mol'],c4['reference_temperature_k']) for t in c4['temperature_by_year_k']]
    mf=[p.moisture_multiplier(x,c4['reference_moisture']) for x in c4['normalized_moisture_by_year']]
    neutral_t=p.fod_run(**baseargs,rate_multipliers=[p.temperature_multiplier(c4['reference_temperature_k'])]*len(years))
    neutral_m=p.fod_run(**baseargs,rate_multipliers=[p.moisture_multiplier(c4['reference_moisture'])]*len(years))
    temp=p.fod_run(**baseargs,rate_multipliers=tf);moist=p.fod_run(**baseargs,rate_multipliers=mf)
    assert neutral_t==base and neutral_m==base
    sensitivity=[]
    sensitivity_runs=[]
    for k in c4['uncertainty_grid_k_per_year']:
        for ea in c4['uncertainty_grid_activation_j_mol']:
            fac=[p.temperature_multiplier(t,ea) for t in c4['temperature_by_year_k']]
            result=p.fod_run(**{**baseargs,'k_per_year':k},rate_multipliers=fac)
            sensitivity_runs.append(result)
            sensitivity.append({'k_per_year':k,'activation_j_mol':ea,'annual_emitted_Gg':[r['emitted_CH4_Gg'] for r in result['rows']],'total_emitted_CH4_Gg':result['total_emitted_CH4_Gg'],'carbon_residual_Gg_C':result['carbon_residual_Gg_C']})
    moisture_sensitivity=[]
    for reference in c4['moisture_reference_sensitivity']:
        run=p.fod_run(**baseargs,rate_multipliers=[p.moisture_multiplier(x,reference) for x in c4['normalized_moisture_by_year']])
        sensitivity_runs.append(run)
        moisture_sensitivity.append({'reference_moisture':reference,'total_emitted_CH4_Gg':run['total_emitted_CH4_Gg'],'carbon_residual_Gg_C':run['carbon_residual_Gg_C']})
    write_json('p4.json',{'class':'HYPOTHETICAL_UNCALIBRATED_RESPONSE','C0':base,'neutral_temperature':neutral_t,'neutral_moisture':neutral_m,'C1_temperature_only':temp,'C1_moisture_only':moist,'temperature_multipliers':tf,'moisture_multipliers':mf,'temperature_parameter_grid':sensitivity,'moisture_reference_sensitivity':moisture_sensitivity,'neutral_max_abs_error_Gg':0,'response_step':'annual piecewise constant only; no claimed subannual prediction'})
    for name,r in [('temperature',temp),('moisture',moist)]:write_csv(f'p4-{name}.csv',r['rows'])
    baseline=[r['emitted_CH4_Gg'] for r in base['rows']]
    chart('p4-neutral',[(name,years,[a['emitted_CH4_Gg']-b for a,b in zip(run['rows'],baseline)]) for name,run in [('Temperature neutral',neutral_t),('Moisture neutral',neutral_m)]],'Inventory year index','C1 - C0 (Gg CH4)','P4 exact neutrality in the same annual model')
    for name,run,mult in [('temperature',temp,tf),('moisture',moist,mf)]:
        chart(f'p4-{name}',[('C0',years,baseline),(f'C1 {name} only',years,[r['emitted_CH4_Gg'] for r in run['rows']])],'Inventory year index','Gg CH4 per annual interval',f'P4 hypothetical {name} response, other mechanisms fixed')
        chart(f'p4-{name}-input',[('Declared rate multiplier',years,mult)],'Inventory year index','Dimensionless rate multiplier',f'Synthetic {name} driver / annual constant multiplier')
    chart('p4-sensitivity',[(f"k={s['k_per_year']}, Ea={s['activation_j_mol']/1000:g} kJ/mol",years,s['annual_emitted_Gg']) for s in sensitivity],'Inventory year index','Gg CH4 per annual interval','P4 deterministic parameter grid (not confidence intervals)')
    all_response_runs=[temp,moist,neutral_t,neutral_m]+sensitivity_runs
    balance={'P2_max_absolute_residual_kg':max(abs(r['residual_kg']) for r in storage.values()),'P2_minimum_stock_kg':min(r['minimum_stock_kg'] for r in storage.values()),'P3_absolute_carbon_residual_Gg_C':abs(base['carbon_residual_Gg_C']),'P3_max_methane_partition_residual_Gg':max(abs(r['methane_partition_residual_Gg']) for r in base['rows']),'P4_max_absolute_carbon_residual_Gg_C':max(abs(r['carbon_residual_Gg_C']) for r in all_response_runs),'P4_max_methane_partition_residual_Gg':max(abs(row['methane_partition_residual_Gg']) for r in all_response_runs for row in r['rows']),'P4_minimum_DDOC_Gg_C':min(row['end_DDOC_Gg_C'] for r in all_response_runs for row in r['rows']),'P4_neutral_max_absolute_difference_Gg_CH4':0,'absolute_tolerance_kg':1e-12,'absolute_tolerance_Gg_C':1e-12,'observational_validation':'NOT_PERFORMED','D3':'DATA_NOT_READY','P1_A':'SCIENCE_PENDING'}
    assert balance['P2_max_absolute_residual_kg']<1e-12 and balance['P3_absolute_carbon_residual_Gg_C']<1e-12
    assert balance['P4_max_absolute_carbon_residual_Gg_C']<1e-12 and balance['P4_max_methane_partition_residual_Gg']<1e-12 and balance['P4_minimum_DDOC_Gg_C']>=0
    write_json('conservation.json',balance)
    packages=['numpy','matplotlib','contourpy','cycler','fonttools','kiwisolver','packaging','Pillow','pyparsing','python-dateutil','six']
    versions={name:importlib.metadata.version(name) for name in packages}
    write_json('runtime.json',{'python':platform.python_version(),'core':'stdlib only, Python 3.12-3.14 compatible; executed runtime shown here','plot_dependencies':versions,'browser_qa':'tools/physics_qa/package-lock.json','deterministic':'No randomness; SVG fixed hash salt and no date metadata'})
    (TASK/'requirements-plot.lock.txt').write_text('\n'.join(f'{k}=={v}' for k,v in versions.items())+'\n',encoding='utf-8')
    print(json.dumps(balance,indent=2))


if __name__=='__main__':main()
