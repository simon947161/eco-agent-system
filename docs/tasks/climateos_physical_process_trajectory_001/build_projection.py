"""Build task-local typed projections; never change frozen Atlas or science gates."""
from pathlib import Path
import json

T=Path(__file__).resolve().parent
def write(name,obj): (T/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8',newline='\n')
def read(name): return json.loads((T/name).read_text(encoding='utf-8'))

def main():
    sources=[]
    def src(id,theme,version,url,locator,rights,access,limitations):
        sources.append(dict(id=id,theme=theme,version=version,url=url,locator=locator,rights=rights,access=access,limitations=limitations))
    src('GML_AGGI','01_GML','AGGI2025','https://gml.noaa.gov/aggi/aggi.html','Observations; Table1 CH4 and footnotes; Table2 2025',
        'NOAA GML public-domain numerical facts; disclaimer https://gml.noaa.gov/about/disclaimer.html','DIRECT_BYTES_HASHED',
        'Published aggregate derived from remote marine boundary-layer measurements; rounded inputs and model fit; no surface-temperature response or site attribution')
    src('CPC_RONI','02_CPC','ERSSTv6_1991-2020_2026-11-03','https://www.cpc.ncep.noaa.gov/data/indices/RONI.ascii.txt',
        'SEAS YR ANOM; method https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/enso/roni/',
        'NOAA/NWS public-domain product; https://www.weather.gov/disclaimer; attribution, no endorsement','DIRECT_BYTES_HASHED',
        'Retrospective derived SST index; no per-row QC/uncertainty. No regional weather series or operational forecast')
    src('NOAA_ENSO','03_NOAA_MECHANISM','web_2026-11-10','https://www.noaa.gov/understanding-el-nino','Ocean-atmosphere coupling; additional NOAA upwelling source https://oceanservice.noaa.gov/facts/ninonina.html updated2026-09-23',
        'Public reading, own summary only; no images redistributed','WEB_READER', 'Educational mechanism, no fitted local weather response')
    src('BOM_RAIN','04_BOM','web_2026-11-10','https://www.bom.gov.au/climate/change/about/rain_timeseries.shtml',
        'Rainfall data; Data format; Data use and copyright','Product-specific study/research permission; unrestricted raw redistribution NOT established; https://www.bom.gov.au/copyright',
        'METADATA_ONLY; PARAMETERIZED_RAIN_PAGE_INACCESSIBLE_TO_WEB_READER; NO_RETRY','Study/research allowed, not treated as illegal. No raw payload obtained. AGCD area average since 1900; preliminary recent months; 1961-1990 anomaly baseline. Do not inherit maps/graphs CC BY4.0 onto raw series')
    src('BOM_COUNTER','04_BOM','updated_2026-09-28','https://www.bom.gov.au/news-and-media/el-nino-strength-doesnt-always-match-impact-on-australia',
        'How will a strong El Niño impact Australia; Why is it raining during El Niño','Own paraphrase; no figures or full text redistributed','WEB_READER',
        'Historical 2023-24 and winter 2026 examples distinct from forecast portions; not a downloaded rainfall time series')
    src('NBI','05_NBI','web_2026-11-10','https://nilebasin.org/hydromet/map','Station table Eldeim, Khartoum, Halfaya Bridge, Dongola',
        'Public metadata facts only; no raw flow licence inferred','WEB_READER','Topology metadata only; no same-window measured flows, storages or travel times')
    src('NILE_STUDY','06_NILE_RESEARCH','Siam_Eltahir_2015','https://doi.org/10.5194/hess-19-1181-2015','Published abstract; twentieth-century datasets',
        'CC BY3.0 article; author paraphrase, no dataset imported','PUBLISHER_ABSTRACT_READ',
        'ENSO and southern Indian Ocean have distinct explanatory roles; published explained variance not independently replayed, not current regulated-flow calibration')
    src('WET_SUPPORT','07_WETLAND_SUPPORT','NatureCommunications_2024_15_10894','https://www.nature.com/articles/s41467-024-55266-y',
        'Indexed publisher abstract and Results/Discussion excerpt','Bibliographic facts and own summary only; no raw file redistributed',
        'INDEXED_PUBLISHER_EXCERPT; FULL_PAGE_IDP_REDIRECT_STOPPED',
        'Inversion ensemble links 2020-21 surges to inundated regions; model-based attribution, regional heterogeneity; full text not obtained this task')
    src('WET_COUNTER','08_WETLAND_COUNTER','CommunicationsEarthEnvironment_2025_s43247-025-02438-3','https://www.nature.com/articles/s43247-025-02438-3',
        'Indexed publisher Discussion excerpt','Bibliographic facts and own summary only; no raw file redistributed',
        'INDEXED_PUBLISHER_EXCERPT; FULL_PAGE_IDP_REDIRECT_STOPPED',
        'Alternate inundation/forcing/model evidence finds limited support for tropical wetland explanation. Baseline, domain and inference design differ; not a controlled same-input comparison')
    src('AU_ACT','09_LAW','C2025C00153_Compilation2','https://www.legislation.gov.au/C2022A00037/2025-02-20/2025-02-20/text/original/epub/OEBPS/document_1/document_1.html',
        's10(1)(a), s10(1)(b); latest details https://www.legislation.gov.au/C2022A00037/latest/details',
        'Statutory facts and short excerpt only; HTML not redistributed','DIRECT_BYTES_HASHED',
        'Compilation effective2025-02-20, registered2025-02-27; not legal advice or a new target review')
    src('SCORECARD_AU','10_SCORECARD','PR146_snapshot_plus_web_reader_2026-11-10','https://www.climatescorecard.org/scorecard/',
        'Australia accordion Q2; five question method; old CSS fifty label','Short quotation only; full HTML not redistributed','DIRECT403_STOPPED; PREEXISTING_WEB_READER_AND_PR146_RECEIPT',
        'Current byte snapshot unavailable. Page-wide publication/modification dates do not date the Australian card; item-level partial-credit rubric unresolved')
    src('HRS_INHERITED','INHERITED','PR129_987cc1d_HRS_Sep2026','https://github.com/simon947161/eco-agent-system/blob/987cc1dc7170204e5eab3d1750590ba463ea9d08/apps/regional-public-os/data/index.json',
        'index metadata, manifest, 2020 shard; fixed January subset','CC BY3.0 AU © WaterNSW; BoM HRS; inherited licence evidence 2026-10-26; unchanged values selected',
        'PINNED_GIT_ARTIFACT_HASH_VERIFIED_NO_NETWORK_RETRY','Public derived fragment, not independently reacquired raw. E unreliable; unit/time/header date conflicts retained')
    src('PR143','INHERITED','746825e65b8ddbd0f518709c94d9476df107208b','https://github.com/simon947161/eco-agent-system/pull/143',
        'methane_knowledge_engine.py; input.json; E01-E14','Repository synthetic reference, no field inputs','LOCAL_PURE_FUNCTION_REPLAY','ChainA synthetic only; ChainB BLOCKED')
    src('PR144','INHERITED','77a35e2723372a290579e4549a86781e2be65c04','https://github.com/simon947161/eco-agent-system/pull/144',
        'mass_balance.py three fixtures; review6735839200','AUTHOR_SYNTHETIC_CC0','LOCAL_PURE_FUNCTION_REPLAY','Species conversion vs carbon conservation; lateral fate UNKNOWN; not NGER/ACCU statutory calculation')
    src('PR145','INHERITED','ae1050a621ac794e447f9ac047865d90b2f04b03','https://github.com/simon947161/eco-agent-system/pull/145',
        'reviewer.py A/B/C; review6736737730','Repository fixtures','REUSED_VIA_ATLAS_E2E','B arithmetic INTERNAL_FIXTURE_REPLAY_ONLY; no external trust anchor or real appointed reviewers')
    src('PR146','INHERITED','1e6b13e2b80c50e6d20e05a4e88819eb0de93488','https://github.com/simon947161/eco-agent-system/pull/146#issuecomment-6750846921',
        'Atlas query/trace; latest ChatGPT ACCEPT_WITH_CONDITIONS','Repository metadata projection','FROZEN_MANIFEST_VERIFIED','METADATA_AND_QUALITATIVE_RELATION_ATLAS; 0 geometry; not a calculable complete physical chain')
    src('AUTHOR','INHERITED','trajectory-protocol/1','ANALYSIS_PROTOCOL.json','Frozen protocol; taskbook; author synthetic derivations',
        'Repository authored synthetic fixtures and analysis; no observation claim','LOCAL_COMPUTATION','No field calibration, causal identification, certification or scientific admission')
    write('SOURCES.json',sources); byid={s['id']:s for s in sources}
    A=read('evidence/computed-A.json'); B=read('evidence/computed-B.json'); C=read('evidence/computed-C.json'); L=read('evidence/computed-legacy.json')
    rows=[]
    def node(process,id,prev,quantity,unit,phase,space,time,mechanism,eq,assumptions,boundary,inputs,origin,ss,u,cal,ce,validation,value,residual,status,gaps,edge):
        rows.append({'PROCESS_ID':process,'NODE_ID':id,'EDGE_ID':f'{prev or "START"}->{id}','from_node':prev,
            'physical_quantity':quantity,'unit':unit,'medium/phase':phase,'spatial_domain':space,'temporal_support':time,
            'mechanism':mechanism,'equation_id':eq,'assumptions':assumptions,'boundary':boundary,'inputs':inputs,
            'observed_or_derived':origin,'source_version_locator':[{'id':s,'version':byid[s]['version'],'locator':byid[s]['locator']} for s in ss],
            'data_rights':[byid[s]['rights'] for s in ss],'uncertainty':u,'calibration':cal,'counterevidence':ce,
            'model_validation':validation,'numerical_output':value,'residual':residual,'status':status,'next_missing_input':gaps,'edge_type':edge})
    node('CH4','A1',None,'CH4 stocks, emissions, oxidation/destruction','kg_CH4/interval','gas plus explicitly dissolved total','synthetic landfill control volumes','synthetic day',
        'species inventory; converted carbon conserved','PR144 ledger', ['fixed boundary, no measured facility claim'],'body / pipe / device / cover',
        'PR144 fixture values, re-executed','SYNTHETIC',['PR144','PR143'],'exact authored arithmetic, not measurement uncertainty','not applicable synthetic',['CE01','CE02'],
        'legacy arithmetic replay only', {k:v['emitted_kg_CH4'] for k,v in L['PR144'].items()},'old four-interface checks retained','SYNTHETIC_TESTED',
        ['same-window site sources, storage, capture/leak measurements with uncertainty'],'CONSERVATION_LAW')
    node('CH4','A2','A1','local concentration and reference gas mass','kg/m3; kg','dry fraction in wet gas','same homogeneous synthetic parcel','instantaneous same parcel',
        'ideal gas, dry/wet reference-volume conversion','PR143 E01-E05',['ideal gas at admitted P,T,e; no global representativeness'],'same parcel before/after standardization',
        'PR143 input.json','SYNTHETIC',['PR143'],'P/e covariance retained','not applicable synthetic',['CE01'],
        'analytical equality replay',{'replay':'evidence/computed-legacy.json#PR143'},'mass residual in replay','SYNTHETIC_TESTED',
        ['global representativeness, atmospheric mass profile, transport/chemistry inversion for emission inference'],'CONSERVATION_LAW')
    node('CH4','A3','A2','global mole fraction to methane ERF','W/m2','dry-air mole fraction','global remote marine boundary-layer annual abundance','2025 minus1750 baseline',
        'published radiative-transfer fit plus rapid adjustment','AGGI_Table1_CH4',['published global means admitted independently of A2; no local-to-global scaling'],'methane direct ERF contribution excluding indirect ozone/water and surface response',
        read('evidence/aggi-facts.json'),'PUBLISHED_OBSERVATION_AGGREGATE_PLUS_EMPIRICAL_RELATION',['GML_AGGI'],
        'propagated reported abundance uncertainty conditional on its interpretation; separate ~10% formula scale, not CI','NOAA published network; no independent instrument recalibration',['CE03'],
        'rounded published result reproduced; not independent validation of radiation physics',A,A['rounding_residual_W_m2'],'OPEN_DATA_RECALCULATED',
        ['validated response kernel, other forcings, time series, feedbacks and ocean heat uptake'],'EMPIRICAL_RELATION')
    node('CH4','A4','A3','global surface-temperature response','K','coupled atmosphere/ocean','global energy balance','explicit response history required',
        'energy accumulation and feedback','C*dT/dt=F-lambda*T; T(t)=integral G(t-s)F(s)ds',
        ['equation is a model form, not admitted parameterization'],'planetary energy budget','F fragment only; C,lambda,G and other forcings missing','MODEL_FORM',['PR143','GML_AGGI'],
        'structural/parameter uncertainty unquantified','no response calibration',['CE03'],'not validated',None,None,'BLOCKED_MODEL_VALIDATION',
        ['source-backed C,lambda or response kernel, initial state, forcing histories and independent observations'],'MODEL_ASSUMPTION')
    node('CH4','A5','A4','regional climate or release-height impact','K or impact metric','transport/chemistry/region','not defined','not defined',
        'transport, chemistry, regional circulation and vulnerability','NONE_EXECUTABLE',['no arbitrary height GWP'],'no admitted source-region counterfactual','missing','HYPOTHESIS',['PR143','PR146'],
        'unidentified','missing',['CE03'],'not validated',None,None,'NOT_INFERABLE',['validated transport/chemistry, comparable counterfactual and exposure/response boundary'],'HYPOTHESIS')
    node('ENSO','B1',None,'SST, wind, thermocline and convection','K; m/s; m','ocean-atmosphere','equatorial Pacific','seasonal coupled evolution',
        'weak trades -> reduced eastern upwelling/shallow cold-water influence -> warmer east -> weaker SST gradient/trades; Bjerknes positive feedback with delayed ocean recharge/discharge',
        'conceptual coupled heat/momentum balances',['feedback direction is mechanism, not a one-equation forecast'],'Pacific coupled system','no wind or heat-content series admitted','LITERATURE_MECHANISM',['NOAA_ENSO'],
        'no model parameters','not calibrated',['CE04'],'qualitative',None,None,'BLOCKED_MODEL_VALIDATION',['wind stress, thermocline/heat-content and validated coupled model'],'PHYSICAL_MECHANISM')
    node('ENSO','B2','B1','relative SST index','degC_anomaly','sea surface','Niño3.4 relative to tropical20N-20S','3month means,1991-2020base;1961-2020analysis',
        'area-average anomaly difference and variance rescaling','RONI_ER SSTv6'.replace(' ',''),['not spliced with ONI or SOI; not five-season event classifier'],'index reconstruction',
        'evidence/RONI.ascii.txt','PUBLISHED_DERIVED_INDEX',['CPC_RONI'],'no row uncertainty/quality flags; retrospective revisions possible','official reconstructed index, not local sensor validation',['CE04'],
        'raw hash, fields, duplicates and coverage checked',{'selected_seasons':720,'missing':0},None,'STRUCTURAL_QC_ONLY',[],'EMPIRICAL_RELATION')
    node('ENSO','B3','B2','conditional same-phase index persistence','probability','statistical index','same Pacific index; no region-weather response','JJA -> SON same year; 60years',
        'conditional counts and paired-year resampling','p=k/n; Wilson; moving-block percentile',
        ['single-season threshold; fixed selection; block approximate stationarity; finite small conditional samples'],'1961-2020 closed historical sample',
        '720 selected seasonal index values','DERIVED_HISTORICAL_STATISTIC',['CPC_RONI','AUTHOR'],
        'nominal Wilson plus3/5year blocks; cold bootstrap[1,1] degenerates, NOT certainty','not a weather forecast',['CE05','CE06'],
        'independent arithmetic/count checks; no held-out forecast validation',B,None,'CONDITIONAL_STATISTICAL_ESTIMATE',
        ['same-window licensed area rainfall and QC before weather probability'],'STATISTICAL_TELECONNECTION')
    node('ENSO','B4','B3','regional seasonal dry probability','probability','regional atmosphere','Australian area average candidate','SON1961-2020; dry threshold1961-1990median',
        'circulation teleconnection conditional on season/IOD/SAM etc.','P(dry|phase)',
        ['index persistence cannot substitute rainfall outcomes'],'not facility, not Indonesia, not Nile','rainfall payload not admitted','UNAVAILABLE',['BOM_RAIN','BOM_COUNTER'],
        'unknown','missing',['CE04','CE06'],'no estimate',None,None,'BLOCKED_MISSING_DATA',
        ['product-specific reproducible-use rights and complete QC rainfall series; confounder protocol'],'STATISTICAL_TELECONNECTION')
    node('ENSO','B5','B4','environmental risk or facility CH4 response','risk / kg_CH4','catchment or facility','not calibrated','lags undefined',
        'weather -> hydrology/process -> vulnerability','NONE_EXECUTABLE',['no deterministic drought or methane causality'],'requires exposure/process evidence','missing','HYPOTHESIS',['BOM_COUNTER','WET_COUNTER'],
        'unidentified','missing',['CE07'],'not validated',None,None,'NOT_INFERABLE',['same-site hydro/temperature/flux covariates and independent process validation'],'HYPOTHESIS')
    node('HYDRO','C1',None,'flow direction and tributary topology','directed links','surface water','Nile: Eldeim -> Khartoum -> Halfaya -> Dongola','station metadata, not synchronized flows',
        'Blue Nile joins White Nile before Halfaya; intervening tributaries/storage remain','control-volume topology',['no numeric travel-time inferred'],'NBI station context','NBI station table','OFFICIAL_METADATA',['NBI','PR146'],
        'locations/timing not field-validated here','not applicable to metadata',['CE08'],'topology only',{'geometry_count':0},None,'STRUCTURAL_QC_ONLY',
        ['licensed simultaneous stage-discharge, rating uncertainty and tributary/storage terms'],'PHYSICAL_MECHANISM')
    node('HYDRO','C2','C1','water-volume balance and propagated residual uncertainty','m3/day_interval','incompressible freshwater','three abstract control volumes, not real Nile reaches','same synthetic86400s UTC interval',
        'Qin+lateral+Parea-Qout-abstraction-evap-dS','HYDRO_CV1',
        ['constant density; identical internal-flow variable reused, no travel lag in this fixture'],'three nested/joined ledgers',
        C['synthetic_inputs'],'SYNTHETIC',['AUTHOR','NBI'],C['synthetic']['uncertainty'],'not applicable synthetic',['CE08','CE09'],
        'exact fixture and perturbation tests',C['synthetic'],0,'SYNTHETIC_TESTED',['measured same-window terms, rating curves, lag/storage model'],'CONSERVATION_LAW')
    node('HYDRO','C3','C2','public daily river-record quality','rows; quality flags','surface water','Cooma410033 ONLY; not Nile proxy','2020-01-01 through01-31; source09:00local unspecified offset',
        'source lineage and structural QC','HRS_QC_ONLY',['no unreliable E flow used as quantitative balance input'],'single gauging station',
        'evidence/hrs-january-2020.json','INHERITED_DERIVED_PUBLIC_RECORDS',['HRS_INHERITED'],
        'E unreliable plus interval/unit ambiguity','no independent gauge calibration',['CE10'],'structural check',C['real_fragment'],None,'STRUCTURAL_QC_ONLY',
        ['verified good-quality same-window records; reconcile ML/MLday, day/UTC and source extraction date'],'EMPIRICAL_RELATION')
    node('HYDRO','C4','C3','real river balance and residual attribution','m3/interval','surface + groundwater','no admitted matched control-volume boundary','no matched time/lag support',
        'missing terms prevent unique allocation of residual','HYDRO_CV1',['unknown lateral/storage is not zero; residual is not automatically evaporation'],'unresolved',
        'single unreliable station cannot close system','UNAVAILABLE',['HRS_INHERITED','NBI','AUTHOR'],
        'unidentified','missing',['CE08','CE09','CE10'],'blocked',None,None,'BLOCKED_MISSING_DATA',
        ['upstream/downstream + lateral + storage + abstraction + P/evap + groundwater terms and uncertainties'],'CONSERVATION_LAW')
    write('TRAJECTORIES.json',rows)
    cross=[]
    for a,b,state,source,counter,claim in [
        ('CH4','CH4','KNOWN_MECHANISM',['GML_AGGI'],['CE03'],'Global abundance-to-ERF fragment replayed; response/emissions attribution blocked'),
        ('CH4','ENSO','NOT_IDENTIFIED',['GML_AGGI','NOAA_ENSO'],['CE03','CE07'],'Long-lived forcing and internal variability differ; no CH4-specific causal coefficient for ENSO identified'),
        ('CH4','HYDRO','BLOCKED',['GML_AGGI','WET_COUNTER'],['CE03','CE07'],'No global mole-fraction-to-local-flow conversion; climate/hydrological intermediate models missing'),
        ('ENSO','CH4','CONDITIONAL',['WET_SUPPORT','WET_COUNTER'],['CE07'],'Possible wetland/chemistry modulation; attribution disputed, no numeric transfer function'),
        ('ENSO','ENSO','OBSERVED_ASSOCIATION',['CPC_RONI'],['CE05','CE06'],'Historical index persistence; no causal identification or future guarantee'),
        ('ENSO','HYDRO','CONDITIONAL',['NILE_STUDY','BOM_COUNTER'],['CE04','CE11'],'Published Nile-specific ENSO and Indian Ocean association; not reproduced here or transferable from Australia'),
        ('HYDRO','CH4','CONDITIONAL',['WET_SUPPORT','WET_COUNTER'],['CE07'],'Inundation/water conditions affect anaerobic habitat but magnitude depends on process and disputed data/models'),
        ('HYDRO','ENSO','NOT_IDENTIFIED',['NOAA_ENSO','NILE_STUDY'],['CE11'],'No identified river-flow-to-ENSO causal model in this evidence package'),
        ('HYDRO','HYDRO','KNOWN_MECHANISM',['NBI','AUTHOR'],['CE08','CE09'],'Water conservation applies; zero synthetic residual does not validate real Nile balance')]:
        cross.append({'from':a,'to':b,'status':state,'sources':source,'counterevidence':counter,'claim':claim,'numeric_coefficient':None})
    write('CROSS_RELATIONS.json',cross)
    print(len(sources),'source records; 10 new themes;',len(rows),'segments;',len(cross),'cross-relations')

if __name__=='__main__': main()
