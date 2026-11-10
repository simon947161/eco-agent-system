"""Finite differences, counterfactuals and numerical controls, not causal estimators."""
import math,statistics,random
from dataclasses import replace
from .state import need,State,difference,apply_difference,remap,Grid
from .models import default_config,simulate,initial_state,mapped_step,STRATEGIES

def gradient(values,dx):
    need(len(values)>=3 and dx>0,'DERIVATIVE_SUPPORT')
    return [(values[1]-values[0])/dx]+[(values[i+1]-values[i-1])/(2*dx) for i in range(1,len(values)-1)]+[(values[-1]-values[-2])/dx]
def divergence(faces,dx):
    need(len(faces)>=2 and dx>0,'DERIVATIVE_SUPPORT');return [(b-a)/dx for a,b in zip(faces,faces[1:])]
def tendency(a,b,dt):
    need(len(a)==len(b) and dt>0,'DERIVATIVE_SUPPORT');return [(y-x)/dt for x,y in zip(a,b)]
def diffusion(n,dt,horizon=100.,kappa=1.,length=100.):
    """Manufactured cosine with homogeneous Neumann walls; cell-centred FV."""
    dx=length/n;need(kappa*dt/dx**2<=.5,'DIFFUSION_CFL');steps=round(horizon/dt)
    need(abs(steps*dt-horizon)<1e-8,'CLOCK_ALIGNMENT')
    x=[(i+.5)*dx for i in range(n)];v=[math.cos(math.pi*t/length) for t in x]
    for _ in range(steps):v=[a+kappa*dt*((v[max(i-1,0)]-2*a+v[min(i+1,n-1)])/dx**2) for i,a in enumerate(v)]
    exact=[math.cos(math.pi*t/length)*math.exp(-kappa*(math.pi/length)**2*horizon) for t in x]
    return {'n':n,'dx_m':dx,'dt_s':dt,'rms_error':math.sqrt(statistics.mean((a-b)**2 for a,b in zip(v,exact))),
            'sum_integral':sum(v)*dx,'values':v,'exact':exact}
def final_mean(run,key):
    need(run['status']=='COMPLETED','DIAGNOSTIC_RUN_FAILED',str(run['failure']))
    return statistics.mean(run['final_values'][key])
def sparse_rank_example():
    c=default_config();a=simulate(c,capture=False);c2=dict(c,wind_m_s=c['wind_m_s']*2,transfer_coefficient=c['transfer_coefficient']/2);b=simulate(c2,capture=False)
    return {'description':'Only transfer_coefficient*wind is identifiable from this idealised trajectory when wind has no other dynamics',
        'configs':[c,c2],'max_final_difference':max(abs(x-y) for k in a['final_values'] for x,y in zip(a['final_values'][k],b['final_values'][k])),
        'inference':'NON_IDENTIFIABLE_PARAMETERS; identical trajectories do not establish correct mechanism'}
def jacobian_bound(c):
    state=initial_state(c);v={k:list(f.values) for k,f in state.fields.items()};keys=('ta','ts','q','water');scale={'ta':1.,'ts':1.,'q':.01,'water':100.}
    z={k:v[k][:] for k in keys};base=mapped_step(v,z,c,'two_way')[0];rows=[]
    entries=[(k,i) for k in keys for i in range(c['grid_n'])]
    for k,i in entries:
        row=[]
        for col,j in entries:
            pert={key:val[:] for key,val in z.items()};eps=1e-5*scale[col];pert[col][j]+=eps
            out=mapped_step(v,pert,c,'two_way')[0];row.append((out[k][i]-base[k][i])/eps*scale[col]/scale[k])
        rows.append(row)
    norm=max(sum(map(abs,row)) for row in rows)
    return {'dimensionless_scaled_jacobian':rows,'variables':entries,'infinity_norm_bound':norm,
        'relaxed_bound':1-c['relaxation']+c['relaxation']*norm,
        'interpretation':'local finite-difference sufficient contraction bound only; >=1 does not prove divergence; not observed feedback gain'}
def compare():
    c=default_config();runs={s:simulate(c,s) for s in STRATEGIES};base=runs['independent']
    deltas={s:{k:[b-a for a,b in zip(base['final_values'][k],r['final_values'][k])] for k in base['final_values']} for s,r in runs.items()}
    single=[]
    for key,h in [('ta_k',.5),('q_kgkg',.001),('wind_m_s',.5),('water_kg_m2',5.)]:
        minus=simulate(dict(c,**{key:c[key]-h}),capture=False);plus=simulate(dict(c,**{key:c[key]+h}),capture=False)
        single.append({'parameter':key,'perturbation':h,'d_final_ts_d_parameter':(final_mean(plus,'ts')-final_mean(minus,'ts'))/(2*h),
                       'd_final_water_d_parameter':(final_mean(plus,'water')-final_mean(minus,'water'))/(2*h),'status':'MODEL_SENSITIVITY_NOT_CAUSAL_EFFECT'})
    scenarios={}
    for label,ta,water in [('baseline',298.,50.),('heat_only',305.,50.),('dry_only',298.,25.),('joint_heat_dry',305.,25.)]:
        scenarios[label]=simulate(dict(c,ta_k=ta,water_kg_m2=water))
    joint={k:final_mean(scenarios['joint_heat_dry'],k)-final_mean(scenarios['heat_only'],k)-final_mean(scenarios['dry_only'],k)+final_mean(scenarios['baseline'],k) for k in ('ts','water','q')}
    heatmap=[]
    for temp in (-2.,0.,2.):
        for wind in (-1.,0.,1.):
            r=simulate(dict(c,ta_k=c['ta_k']+temp,wind_m_s=c['wind_m_s']+wind),capture=False)
            heatmap.append({'delta_temperature_K':temp,'delta_wind_m_s':wind,'final_ts_K':final_mean(r,'ts'),'final_water_kg_m2':final_mean(r,'water')})
    temporal=[]
    for dt in (1200.,600.,300.):
        r=simulate(dict(c,dt_s=dt,steps=int(21600/dt)),capture=False);temporal.append({'dt_s':dt,'final_ts_K':final_mean(r,'ts'),'final_water_kg_m2':final_mean(r,'water')})
    spatial=[]
    for n in (2,4,8):
        r=simulate(dict(c,grid_n=n),capture=False);spatial.append({'n':n,'dx_m':2000/n,'final_ts_K':r['final_values']['ts'],'mean_water_kg_m2':final_mean(r,'water')})
    delays=[simulate(dict(c,lag_steps=k),capture=False) for k in (0,1,4)]
    dspace=[diffusion(n,.01) for n in (8,16,32)]
    # Fixed space: compare temporal error against exact semidiscrete eigenmode,
    # so spatial truncation cannot masquerade as temporal convergence.
    temporal_exact=[];n=8;dx=100/n;lam=-4*math.sin(math.pi/(2*n))**2/dx**2
    for dt in (2.,1.,.5):
        amp=(1+lam*dt)**round(100/dt);exact=math.exp(lam*100);temporal_exact.append({'dt_s':dt,'amplitude_error':abs(amp-exact)})
    initial=initial_state(c);modified=State(initial.fields.values());modified.put(replace(modified.fields['ts'],values=tuple(x+1 for x in modified.fields['ts'].values)))
    patch=difference(initial,modified);restored=apply_difference(apply_difference(initial,patch),patch,reverse=True)
    measured=replace(initial.fields['water'],values=(40.,60.),uncertainty=(2.,3.),covariance=((4.,3.),(3.,9.)))
    mapped=remap(measured,Grid.strip(4));g4=simulate(dict(c,grid_n=4));last=g4['trace'][-1];prev=g4['trace'][-2]
    mediation={'before':measured.metadata(),'after':mapped.metadata(),'area_integral_before':sum(v*a for v,a in zip(measured.values,measured.grid.areas)),
        'area_integral_after':sum(v*a for v,a in zip(mapped.values,mapped.grid.areas)),'reversible_difference':patch,'round_trip_hash_equal':restored.hash()==initial.hash(),
        'temperature_gradient_K_m':gradient(last['values']['ts'],500.),'temperature_tendency_K_s':tendency(prev['values']['ts'],last['values']['ts'],c['dt_s']),
        'synthetic_face_flux_W_m': [0.,10.,0.,-10.,0.],'flux_divergence_W_m2':divergence([0.,10.,0.,-10.,0.],500.)}
    ensembles=[]
    for rho in (-.6,0.):
        rng=random.Random(20261112);rows=[]
        for i in range(60):
            z=rng.gauss(0,1);qz=rho*z+math.sqrt(1-rho*rho)*rng.gauss(0,1)
            cfg=dict(c,ta_k=302+z,q_kgkg=.009+.001*qz);r=simulate(cfg,capture=False)
            rows.append({'id':i,'ta_k':cfg['ta_k'],'q':cfg['q_kgkg'],'status':r['status'],'final_ts_K':final_mean(r,'ts'),'evap_kg_m2':r['evaporation_kg_m2']})
        ensembles.append({'seed':20261112,'rho':rho,'n':60,'rows':rows,'sd_final_ts_K':statistics.stdev(x['final_ts_K'] for x in rows),
                          'sd_evap_kg_m2':statistics.stdev(x['evap_kg_m2'] for x in rows),'status':'ASSUMED_INPUT_COVARIANCE_NOT_PREDICTIVE_INTERVAL'})
    return {'evidence_class':'SYNTHETIC_MODEL_EXPERIMENT','runs':runs,'difference_from_independent':deltas,'single_sensitivity':single,
        'joint_scenarios':scenarios,'joint_interaction':joint,'heatmap':heatmap,'dt_halving':temporal,'dx_halving':spatial,
        'space_manufactured':dspace,'time_semidiscrete':temporal_exact,'lag_diagnostics':delays,'local_feedback_bound':jacobian_bound(c),
        'identifiability':sparse_rank_example(),'mediation':mediation,'uncertainty_ensembles':ensembles,'counterexample':'joint heat plus dry can cross a declared threshold when either perturbation alone does not',
        'threshold_status':'ASSUMED_NOT_VALIDATED; hysteresis flag is decision memory, not physical multistability proof'}
