"""Conservation-first idealised surface / mixed-layer models.

All transfer coefficients/capacities are ASSUMED_NOT_VALIDATED. The FAO56
saturation equation is reused, but this is NOT the FAO crop ET model.
"""
from __future__ import annotations
from dataclasses import replace
from datetime import datetime,timedelta,timezone
from functools import lru_cache
import copy, math
from pathlib import Path
from . import VERSION
from .state import CATALOG,Field,Grid,State,TimeSupport,Rejection,need,digest
from .. import physical_process_trajectory as old

ROOT=Path(__file__).resolve().parents[3]
TASK=ROOT/'docs/tasks/climateos_earth_system_coupling_lab_001'
LV=2.45e6;RD=287.05;CP=1004.
STRATEGIES=('independent','one_way','two_way')

def saturation(T,p):
    need(243.15<=T<=333.15 and 70000<=p<=110000,'FORMULA_DOMAIN','water-only idealised saturation range')
    tc=T-273.15;e=610.8*math.exp(17.27*tc/(tc+237.3))
    return .622*e/(p-.378*e)
def time_window(seconds,dt):
    t=datetime(2000,1,1,tzinfo=timezone.utc)+timedelta(seconds=seconds)
    return TimeSupport(t.isoformat(),(t+timedelta(seconds=dt)).isoformat(),local_clock='UTC synthetic clock; no real site or local observation day')
def default_config():
    return {'grid_n':2,'length_m':2000.,'dt_s':900.,'steps':24,'ta_k':302.,'ts_offset_k':2.,'q_kgkg':.009,
        'pressure_pa':100000.,'wind_m_s':3.,'rain_kg_m2_s':2e-5,'radiation_w_m2':220.,
        'water_kg_m2':50.,'capacity_kg_m2':150.,'surface_heat_capacity':2e6,'mixing_height_m':100.,
        'transfer_coefficient':.002,'relaxation_time_s':14400.,'diffusivity_m2_s':.5,
        'relaxation':.5,'max_iterations':60,'tolerance':1e-8,'lag_steps':0,'fault':None}
def validate_config(c):
    need(set(c)==set(default_config()),'CONFIG_FIELDS')
    for key,value in c.items():
        if key!='fault':need(type(value) in (int,float) and math.isfinite(value),'CONFIG_NONFINITE',key)
    need(type(c['steps']) is int and 1<=c['steps']<=96,'STEP_BUDGET')
    need(type(c['grid_n']) is int and 1<=c['grid_n']<=16,'GRID_BUDGET')
    need(type(c['max_iterations']) is int and 1<=c['max_iterations']<=80,'ITERATION_BUDGET')
    need(type(c['lag_steps']) is int and 0<=c['lag_steps']<=4,'LAG_RANGE')
    need(0<c['dt_s']<=86400 and c['steps']*c['dt_s']<=7*86400,'CLOCK_BUDGET')
    need(.05<=c['relaxation']<=1 and 1e-10<=c['tolerance']<=1e-5,'SOLVER_CONTROL')
    need(c['length_m']>0 and c['capacity_kg_m2']>0 and c['surface_heat_capacity']>0 and c['mixing_height_m']>0 and c['relaxation_time_s']>0,'POSITIVE_PARAMETER')
    need(0<=c['water_kg_m2']<=c['capacity_kg_m2'] and 0<=c['rain_kg_m2_s']<=.01,'WATER_DOMAIN')
    need(0<=c['wind_m_s']<=50 and 0<=c['diffusivity_m2_s'] and 0<=c['transfer_coefficient']<=.02,'PARAMETER_DOMAIN')
    need(0<=c['q_kgkg']<=.04 and -100<=c['radiation_w_m2']<=1000,'FORCING_DOMAIN')
    saturation(c['ta_k'],c['pressure_pa']);return c
def field(name,values,grid,time,config_hash,**kw):
    return Field(name,tuple(values),grid,time,CATALOG[name][0],kw.pop('kind','SIMULATED_STATE'),
                 kw.pop('source_id','SYNTHETIC_CONFIG'),VERSION,config_hash,'MIT repository-authored synthetic fixture',
                 'SYNTHETIC_NOT_OBSERVATIONS',(None,)*len(values),lineage=('declared_config',),**kw)
def initial_state(c):
    validate_config(c);g=Grid.strip(c['grid_n'],c['length_m']);t=time_window(0,c['dt_s']);h=digest(c)
    values={'ta':[c['ta_k']]*c['grid_n'],'ts':[c['ta_k']+c['ts_offset_k']+math.cos(math.pi*(i+.5)/c['grid_n']) for i in range(c['grid_n'])],
        'q':[c['q_kgkg']]*c['grid_n'],'pressure':[c['pressure_pa']]*c['grid_n'],'u':[c['wind_m_s']]*c['grid_n'],'v':[0.]*c['grid_n'],
        'rain':[c['rain_kg_m2_s']]*c['grid_n'],'rn':[c['radiation_w_m2']]*c['grid_n'],'water':[c['water_kg_m2']]*c['grid_n'],
        'evap':[0.]*c['grid_n'],'runoff':[0.]*c['grid_n']}
    state=State(field(k,v,g,t,h) for k,v in values.items())
    if c['fault']=='missing_q':state.put(replace(state.fields['q'],values=(None,)*c['grid_n']))
    if c['fault']=='unit':state.put(replace(state.fields['rain'],unit='mm/month'))
    if c['fault']=='time':state.put(replace(state.fields['rain'],time=time_window(3600,c['dt_s'])))
    if c['fault']=='synthetic_as_observed':state.put(replace(state.fields['ta'],kind='OBSERVED_STATE'))
    if c['fault']=='global_to_local':state.put(replace(state.fields['rn'],grid=Grid('GLOBAL','spherical_global',((0.,1.,0.,1.),),'global'),values=(.569344413968403,),uncertainty=(None,)))
    for f in context_state()[0].fields.values():state.put(f)
    return state

class Component:
    name='component';required_fields=();provided_fields=();clock='local'
    def initialize(self,state):
        self.current_time=0.;self.grid=state.fields[self.required_fields[0]].grid;self._initial=state.checkpoint();return self
    @property
    def units(self):return {k:CATALOG[k][0] for k in self.required_fields+self.provided_fields}
    def inspect(self):return {'name':self.name,'required_fields':self.required_fields,'provided_fields':self.provided_fields,'units':self.units,'current_time':getattr(self,'current_time',None),'clock':self.clock,'evidence':self.evidence()}
    def checkpoint(self):return getattr(self,'current_time',0.)
    def reset(self,checkpoint=0.):self.current_time=checkpoint
    def evidence(self):return {'model_version':VERSION,'status':'ASSUMED_NOT_VALIDATED','scope':'synthetic local slab; no forecasting'}

class Atmosphere(Component):
    name='atmospheric_exchange_and_column';required_fields=('ta','q','pressure','u','v','ts','water');provided_fields=('ta','q','evap');clock='2 fast substeps per land interval'
    def fluxes(self,guess,c,old_values,dt,lag_values=None):
        e=[];h=[];rho=[]
        for i,T in enumerate(guess['ta']):
            p=old_values['pressure'][i];density=p/(RD*T);rho.append(density)
            U=math.hypot(old_values['u'][i],old_values['v'][i]);coef=c['transfer_coefficient']
            q=guess['q'][i] if lag_values is None else lag_values['q'][i]
            moisture=max(0,min(1,guess['water'][i]/c['capacity_kg_m2']))
            demand=density*coef*U*max(0,saturation(guess['ts'][i],p)-q)*moisture
            available=old_values['water'][i]/dt+old_values['rain'][i]
            e.append(min(demand,available));h.append(density*CP*coef*U*(guess['ts'][i]-T))
        return {'evap':e,'sensible':h,'density':rho}
    def step(self,old_values,flux,c,dt):
        ta=list(old_values['ta']);q=list(old_values['q']);n=len(ta);mass=c['pressure_pa']/(RD*c['ta_k'])*c['mixing_height_m'];cap=mass*CP
        boundary_heat=[0.]*n;vented_water=[0.]*n
        for _ in range(2):
            for i in range(n):
                B=-cap*(ta[i]-c['ta_k'])/c['relaxation_time_s'];V=mass*(q[i]-c['q_kgkg'])/c['relaxation_time_s']
                ta[i]+=(flux['sensible'][i]+B)*(dt/2)/cap;q[i]+=(flux['evap'][i]-V)*(dt/2)/mass
                boundary_heat[i]+=B*dt/2;vented_water[i]+=V*dt/2
        return {'ta':ta,'q':q,'boundary_heat':boundary_heat,'vented_water':vented_water,'air_mass':mass,'air_capacity':cap}

class Surface(Component):
    name='surface_water_and_energy';required_fields=('ts','water','rain','rn');provided_fields=('ts','water','runoff');clock='land interval'
    def step(self,old_values,flux,c,dt):
        ts=old_values['ts'];n=len(ts);dx=c['length_m']/n;water=[];newt=[];runoff=[];diffusion=[]
        for i in range(n):
            lap=(ts[max(0,i-1)]-2*ts[i]+ts[min(n-1,i+1)])/dx**2
            diff=c['surface_heat_capacity']*c['diffusivity_m2_s']*lap
            available=old_values['water'][i]+(old_values['rain'][i]-flux['evap'][i])*dt
            out=max(0,available-c['capacity_kg_m2']);water.append(available-out);runoff.append(out/dt)
            newt.append(ts[i]+dt*(old_values['rn'][i]-flux['sensible'][i]-LV*flux['evap'][i]+diff)/c['surface_heat_capacity']);diffusion.append(diff)
        return {'ts':newt,'water':water,'runoff':runoff,'diffusion':diffusion}

@lru_cache(maxsize=1)
def public_baseline():
    """Read existing frozen derived evidence only; never acquire or copy CSVs."""
    from .. import multisource_data_admission as m
    m.verify();old.verify();data=m.read(m.TASK/'evidence/results.json');facts=old.read(old.TASK/'evidence/aggi-facts.json')
    return {'RONI':old.parse_roni((old.TASK/'evidence/RONI.ascii.txt').read_bytes())[2012,'SON'],
        'warm_dry':data['results'][1]['events']['dry']['primary']['phase']['warm'],
        'valid_SON':46,'last_valid_year':2012,'source_result_hash':m.sha((m.TASK/'evidence/results.json').read_bytes().replace(b'\r\n',b'\n')),
        'ch4_facts_hash':m.sha((old.TASK/'evidence/aggi-facts.json').read_bytes().replace(b'\r\n',b'\n')),
        'roni_hash':m.sha((old.TASK/'evidence/RONI.ascii.txt').read_bytes()),
        'M':facts['M_ppb'],'N':facts['N_ppb'],'radiation':old.radiation(),
        'status':'CONDITIONAL_ACCEPTED_WITH_GAPS; scientific_admission PENDING','local_forcing_connection':'FORBIDDEN_UNVALIDATED_SCALE_LINK'}

class ENSOContext(Component):
    name='seasonal_enso_context';required_fields=('roni',);provided_fields=('enso_phase',);clock='seasonal; diagnostic only'
    def step(self,state,dt):
        f=state.fields['roni'];need(dt==f.time.seconds(),'SLOW_CLOCK_MISMATCH')
        phase={'warm':1.,'cold':-1.,'neutral':0.}[old.phase(f.values[0])]
        state.put(replace(f,id='enso_phase',values=(phase,),unit='1',kind='CONSTRAINED_ESTIMATE',uncertainty=(None,),lineage=f.lineage+('PR147.phase; no local precipitation equation',)))
        self.current_time=dt;return {'phase':phase,'local_numeric_forcing':None,'historical_association':public_baseline()['warm_dry']}
    def evidence(self):return {'model_version':'PR147/149 frozen','status':'OBSERVATION_DERIVED_HISTORICAL_ASSOCIATION','causal_link':False}

class MethaneERF(Component):
    name='global_methane_erf';required_fields=('ch4','n2o');provided_fields=('erf',);clock='annual; independent global diagnostic'
    def step(self,state,dt):
        f=state.fields['ch4'];need(f.grid.support=='global' and f.time==state.fields['n2o'].time,'GLOBAL_SUPPORT')
        need(dt==f.time.seconds(),'SLOW_CLOCK_MISMATCH')
        result=old.ch4_erf(f.values[0],state.fields['n2o'].values[0])
        state.put(replace(f,id='erf',unit='W m-2',values=(result['ERF_W_m2'],),kind='CONSTRAINED_ESTIMATE',uncertainty=(None,),lineage=f.lineage+('PR147.ch4_erf; no local temperature conversion',)))
        self.current_time=dt;return result
    def evidence(self):return {'model_version':'PR147 published NOAA function','status':'OPEN_DATA_RECALCULATED','scope':'global annual CH4 ERF, not regional forcing'}

@lru_cache(maxsize=1)
def context_state():
    b=public_baseline();g=Grid('global','GLOBAL_MEAN',((0.,1.,0.,1.),),'global');index=Grid('RONI','NINO34_INDEX',((0.,1.,0.,1.),),'index_region')
    year=TimeSupport('2025-01-01T00:00:00Z','2026-01-01T00:00:00Z',local_clock='calendar annual support; not instantaneous timestamp')
    season=TimeSupport('2012-09-01T00:00:00Z','2012-12-01T00:00:00Z',local_clock='calendar SON support; not observation UTC boundary')
    fields=[]
    for name,value,grid,t in [('ch4',b['M'],g,year),('n2o',b['N'],g,year),('roni',b['RONI'],index,season)]:
        fields.append(Field(name,(value,),grid,t,CATALOG[name][0],'CONSTRAINED_ESTIMATE','FROZEN_PUBLIC_PR147','PR147_D',b['roni_hash' if name=='roni' else 'ch4_facts_hash'],
            'existing research evidence rights; no new raw redistribution','DERIVED_SOURCE_FACT',(None,),evidence_level='OPEN_DATA_RECALCULATED',reference_conditions='original global/seasonal domain'))
    state=State(fields);a=ENSOContext().initialize(state);m=MethaneERF().initialize(state)
    outputs={a.name:a.step(state,season.seconds()),m.name:m.step(state,year.seconds())}
    return state,outputs,[a.inspect(),m.inspect()]

@lru_cache(maxsize=1)
def context_snapshot():
    state,outputs,comps=context_state()
    return {'state':state.inspect(),'outputs':outputs,'components':comps,'scientific_admission':'PENDING'}

def components():return [x().inspect() for x in (Atmosphere,Surface,ENSOContext,MethaneERF)]

def mapped_step(oldv,guess,c,strategy,lag_values=None):
    dt=c['dt_s'];n=c['grid_n'];atm=Atmosphere();land=Surface()
    if strategy=='independent':flux={'evap':[0.]*n,'sensible':[0.]*n}
    else:flux=atm.fluxes(guess,c,oldv,dt,lag_values)
    surface=land.step(oldv,flux,c,dt)
    if strategy=='two_way':air=atm.step(oldv,flux,c,dt)
    else:air={'ta':oldv['ta'],'q':oldv['q'],'boundary_heat':[0.]*n,'vented_water':[0.]*n,'air_mass':0.,'air_capacity':0.}
    new={k:surface[k] for k in ('ts','water')};new.update(ta=air['ta'],q=air['q'])
    return new,flux,surface,air

def advance(state,c,strategy,lag_values=None):
    need(strategy in STRATEGIES,'COUPLING_STRATEGY');dt=c['dt_s'];cp=state.checkpoint();g=state.fields['ts'].grid;t=state.fields['ts'].time
    required=Surface.required_fields if strategy=='independent' else tuple(set(Surface.required_fields+Atmosphere.required_fields))
    state.require(required,grid=g,time=t);oldv={k:list(f.values) for k,f in state.fields.items()}
    dx=c['length_m']/c['grid_n'];need(c['diffusivity_m2_s']*dt/dx**2<=.5,'DIFFUSION_CFL')
    need(dt/2/c['relaxation_time_s']<=1,'ATMOSPHERE_CLOCK_STABILITY')
    guess={k:list(oldv[k]) for k in ('ts','water','ta','q')};scale={'ts':1.,'water':100.,'ta':1.,'q':.01};iterations=0;error=0.
    try:
        for iteration in range(c['max_iterations'] if strategy=='two_way' else 1):
            new,flux,surface,air=mapped_step(oldv,guess,c,strategy,lag_values);iterations=iteration+1
            need(all(243.15<=v<=333.15 for k in ('ts','ta') for v in new[k]),'TEMPERATURE_DOMAIN')
            if strategy!='independent':need(all(0<=v<=.05 for v in new['q']),'HUMIDITY_DOMAIN')
            need(all(-1e-10<=v<=c['capacity_kg_m2']+1e-10 for v in new['water']),'WATER_DOMAIN')
            if strategy!='two_way':break
            error=max(abs(a-b)/scale[k] for k in scale for a,b in zip(new[k],guess[k]))
            if error<=c['tolerance']:break
            guess={k:[a+c['relaxation']*(b-a) for a,b in zip(guess[k],new[k])] for k in scale}
        else:raise Rejection('NON_CONVERGENCE',f'iterations={iterations}, normalized_error={error}')
        # Water and enthalpy: same exchanged flux enters both components.
        water_res=[];energy_res=[]
        for i in range(c['grid_n']):
            water_change=new['water'][i]-oldv['water'][i]
            energy_change=c['surface_heat_capacity']*(new['ts'][i]-oldv['ts'][i])
            if strategy=='two_way':
                water_change+=air['air_mass']*(new['q'][i]-oldv['q'][i]);water_expected=(oldv['rain'][i]-surface['runoff'][i])*dt-air['vented_water'][i]
                energy_change+=air['air_capacity']*(new['ta'][i]-oldv['ta'][i])+LV*air['air_mass']*(new['q'][i]-oldv['q'][i])
                energy_expected=(oldv['rn'][i]+surface['diffusion'][i])*dt+air['boundary_heat'][i]-LV*air['vented_water'][i]
            else:
                water_expected=(oldv['rain'][i]-flux['evap'][i]-surface['runoff'][i])*dt
                energy_expected=(oldv['rn'][i]-flux['sensible'][i]-LV*flux['evap'][i]+surface['diffusion'][i])*dt
            water_res.append(water_change-water_expected);energy_res.append(energy_change-energy_expected)
        need(max(map(abs,water_res))<1e-8,'WATER_CONSERVATION')
        need(max(map(abs,energy_res))<1e-5,'ENERGY_CONSERVATION')
        need(abs(sum(d*a for d,a in zip(surface['diffusion'],g.areas)))<1e-6,'LATERAL_BOUNDARY_FLUX')
        for k in ('ts','water','ta','q'):state.put(replace(state.fields[k],values=tuple(new[k]),lineage=('synthetic_initial_state',VERSION+':'+strategy)))
        for k,vals in [('evap',flux['evap']),('runoff',surface['runoff'])]:state.put(replace(state.fields[k],values=tuple(vals),lineage=(VERSION+':'+strategy,)))
        return {'iterations':iterations,'fixed_point_error':error,'water_residual_kg_m2':max(map(abs,water_res)),
            'energy_residual_j_m2':max(map(abs,energy_res)),'evap_kg_m2':sum(flux['evap'])/len(flux['evap'])*dt,'runoff_kg_m2':sum(surface['runoff'])/len(surface['runoff'])*dt,
            'closure':'surface_plus_atmosphere_enthalpy_and_water' if strategy=='two_way' else 'surface_open_boundary_fluxes',
            'boundary_heat_j_m2':air['boundary_heat'],'vented_water_kg_m2':air['vented_water']}
    except Rejection:
        state.reset(cp);raise

def simulate(config=None,strategy='two_way',capture=True):
    c=copy.deepcopy(default_config() if config is None else config);config_hash=digest({'config':c,'strategy':strategy,'version':VERSION})
    # Slow, disjoint components still produce diagnostics when the fast edge fails.
    context=context_snapshot();state=None;history=[];trace=[];water_error=energy_error=0.;evap=runoff=0.;iters=0;flags=[];diagnostic_on=False
    status='COMPLETED';failure=None;completed=0;initial_hash=None
    try:
        state=initial_state(c);initial_hash=state.hash();atm=Atmosphere().initialize(state);land=Surface().initialize(state)
        history.append({k:list(state.fields[k].values) for k in ('ta','q','ts','water')})
        if capture:trace.append({'elapsed_s':0.,'values':history[-1]})
        for step in range(c['steps']):
            lag=history[max(0,len(history)-1-c['lag_steps'])] if c['lag_steps'] else None
            cp=state.checkpoint();old_clock=(atm.checkpoint(),land.checkpoint())
            try:info=advance(state,c,strategy,lag)
            except Rejection:state.reset(cp);atm.reset(old_clock[0]);land.reset(old_clock[1]);raise
            completed+=1;atm.current_time+=c['dt_s'];land.current_time+=c['dt_s']
            water_error=max(water_error,info['water_residual_kg_m2']);energy_error=max(energy_error,info['energy_residual_j_m2']);iters+=info['iterations'];evap+=info['evap_kg_m2'];runoff+=info['runoff_kg_m2']
            current={k:list(state.fields[k].values) for k in ('ta','q','ts','water')};history.append(current)
            hotdry=any(T>303.15 and W/c['capacity_kg_m2']<.25 for T,W in zip(current['ta'],current['water']))
            release=all(T<301.15 or W/c['capacity_kg_m2']>.30 for T,W in zip(current['ta'],current['water']))
            if hotdry:diagnostic_on=True
            elif release:diagnostic_on=False
            flags.append(hotdry)
            if capture:trace.append({'elapsed_s':completed*c['dt_s'],'values':current,'hot_dry':hotdry,'decision_memory_flag':diagnostic_on,'ledger':info})
            # Advance local clocks only; no resampling of seasonal/global fields.
            for k,f in list(state.fields.items()):
                if f.grid.support=='area' and k not in ('evap','runoff'):
                    state.put(replace(f,time=time_window(completed*c['dt_s'],c['dt_s'])))
        clocks=[atm.inspect(),land.inspect()]
    except Rejection as e:
        status='REJECTED';failure={'code':e.code,'detail':e.detail,'rolled_back_failed_step':state is not None,
                                 'stage':'INITIALIZATION' if state is None else 'STEP'};clocks=[]
    values={} if state is None else {k:list(state.fields[k].values) for k in ('ta','ts','q','water')}
    return {'model_version':VERSION,'config_hash':config_hash,'config':c,'strategy':strategy,'status':status,'failure':failure,
        'completed_steps':completed,'requested_steps':c['steps'],'iterations':iters,'max_water_residual_kg_m2':water_error,'max_energy_residual_j_m2':energy_error,
        'evaporation_kg_m2':evap,'runoff_kg_m2':runoff,'hot_dry_exceeded':any(flags) if completed else None,
        'decision_memory_flag':diagnostic_on if completed else None,'final_values':values,'initial_state_hash':initial_hash,'final_state_hash':state.hash() if state else None,
        'evidence_class':'SYNTHETIC_MODEL_EXPERIMENT','parameters_status':'ASSUMED_NOT_VALIDATED','scientific_admission':'PENDING',
        'trace':trace if capture else None,'final_shared_state':state.inspect() if capture and state else None,
        'components':clocks+context['components'] if capture else None,'independent_slow_context':context if capture else {'status':'AVAILABLE_INDEPENDENTLY','ERF':context['outputs']['global_methane_erf']['ERF_W_m2']},
        'forecast_skill':None,'causal_real_world_validation':False}
