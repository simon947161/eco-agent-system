"""Author bounded research records from frozen factual extracts, not a crawler.

No geometry, emissions model or policy-to-physics parameter conversion.
Run only to deliberately regenerate this version; ordinary queries are read-only.
"""
from pathlib import Path
import hashlib
import json

T = Path(__file__).resolve().parent
ROOT = T.parents[2]
VERSION = 'atlas-research-1/2026-11-09'

def write(name, obj):
    (T/name).write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n',encoding='utf-8',newline='\n')

def digest(path):
    return hashlib.sha256(path.read_bytes().replace(b'\r\n',b'\n')).hexdigest()

def build():
    receipts = {r['id']:r for r in json.loads((T/'evidence/acquisition.json').read_text())}
    source_specs = [
      ('M49','UN statistics','https://unstats.un.org/unsd/methodology/m49/overview/','English downloadTableEN','snapshot 2026-11-09','PUBLIC_FACTUAL_METADATA_ONLY','m49','SOURCE_VERIFIED','M49 online snapshot; no full HTML redistribution or implied sovereignty'),
      ('SCORE','Climate Scorecard','https://www.climatescorecard.org/scorecard/','rubric; country toggle + CSS; JSON-LD','published 2021-03-29; modified 2025-09-25','ALL_RIGHTS_RESERVED_FACTS_LINKS_ONLY','scorecard','SOURCE_VERIFIED','Modification date is not a per-country policy validity date'),
      ('REPORTS','Climate Scorecard','https://www.climatescorecard.org/reports/','report index; Report 80; Australia forecast article','snapshot 2026-11-09','ALL_RIGHTS_RESERVED_FACTS_LINKS_ONLY','reports','SOURCE_VERIFIED','Report narratives and predictions are not independently verified outcomes'),
      ('SC_AU_REPORT','Climate Scorecard / Jessica Gregory','https://www.climatescorecard.org/2026/03/australia-2026-emissions-forecast/','title, byline, publication/update line and engagement resources','2026-03-25 published; 2026-05-08 updated','ALL_RIGHTS_RESERVED_FACTS_LINKS_ONLY',None,'SOURCE_VERIFIED','A forecast article; underlying inventory references were not independently reanalysed'),
      ('SC_FOREST','Climate Scorecard / country managers','https://www.climatescorecard.org/project/report-80/','Report 80 introduction and country article index','country posts dated 2024-11-25','ALL_RIGHTS_RESERVED_FACTS_LINKS_ONLY',None,'SOURCE_VERIFIED','Country narrative does not constitute a harmonised independently measured ecological outcome'),
      ('NE','Natural Earth','https://www.naturalearthdata.com/about/terms-of-use/','terms of use','product version UNKNOWN; terms snapshot 2026-11-09','PUBLIC_DOMAIN',None,'SOURCE_VERIFIED','Only licence metadata verified; no geometry or exact product acquired'),
      ('KG','Beck et al. / GloH2O','https://www.gloh2o.org/koppen/','V3 landing; DOI 10.1038/s41597-023-02549-6','V3 landing / 2023 paper','CC_BY_4_0_INDEXED_NOT_PAYLOAD_VERIFIED',None,'EVIDENCE_INSUFFICIENT','Indexed metadata only; direct request timed out; past classifications and future projections differ'),
      ('HYDRO','HydroSHEDS','https://www.hydrosheds.org/products/hydrobasins','product description and licence section','HydroBASINS version 1','CUSTOM_HYDROSHEDS_TERMS_NOT_FULLY_AUDITED',None,'SOURCE_VERIFIED','12 nested levels; 15 arc-second parent grid; Antarctica excluded; polygons not acquired'),
      ('IUCN','IUCN','https://iucn.org/resources/conservation-tool/iucn-global-ecosystem-typology','GET tool; 2020 publication','GET 2.0 (2020), intentionally frozen','UNKNOWN_METADATA_LINKS_ONLY',None,'SOURCE_VERIFIED','Six hierarchical levels; not claiming latest version or redistributed boundaries'),
      ('NBI','Nile Basin Initiative','https://nilebasin.org/hydromet/map','Eldeim, Khartoum, Halfaya Bridge, Dongola station rows','undated page snapshot 2026-11-09','UNKNOWN_METADATA_LINKS_ONLY',None,'SOURCE_VERIFIED','Station purpose supports qualitative connectivity, not measured discharge, rights or attribution'),
      ('ENSO','NOAA','https://www.noaa.gov/understanding-el-nino','Impacts; Forecasting; RONI transition paragraph','snapshot 2026-11-09; RONI transition 2026-02-01','PUBLIC_FACTUAL_METADATA_ONLY',None,'SOURCE_VERIFIED','Teleconnections likely not certain; third-party images not copied'),
      ('IPCC','IPCC','https://www.ipcc.ch/report/ar6/wg1/chapter/chapter-6/','AR6 WGI Chapter 6 Table 6.2 indexed reference','2021','UNKNOWN_METADATA_LINKS_ONLY',None,'BLOCKED','403; no retries; no downloaded full-text verification this batch'),
      ('GML','NOAA GML','https://gml.noaa.gov/ccgg/trends_ch4/','monthly marine surface means; uncertainty; citation','2026-10','PUBLIC_FACTUAL_METADATA_ONLY',None,'SOURCE_VERIFIED','Derived global product, latest year provisional; not local emissions'),
      ('AGGI','NOAA GML','https://gml.noaa.gov/aggi/aggi.html','Radiative Forcing Calculations; Table 1','2025 AGGI update, retrieved 2026-11-09','PUBLIC_FACTUAL_METADATA_ONLY',None,'SOURCE_VERIFIED','Global abundances to effective forcing; excludes slower surface-temperature feedbacks'),
      ('NDC','UNFCCC','https://unfccc.int/NDCREG','party/version/submission-date rows','web excerpt snapshot 2026-11-09','UNKNOWN_METADATA_LINKS_ONLY','ndc','EVIDENCE_INSUFFICIENT','Local HTTP200 was a 212-byte challenge; only independent web-rendered registry metadata read; no PDF targets admitted'),
      ('AU_ACT','Federal Register of Legislation','https://www.legislation.gov.au/C2022A00037/2025-02-20/2025-02-20/text/original/epub/OEBPS/document_1/document_1.html','Climate Change Act 2022 section 10(1)(a)','Compilation 2 / 2025-02-20 / C2025C00153','PUBLIC_FACTUAL_METADATA_ONLY',None,'SOURCE_VERIFIED','Fixed historical compilation, not certification or full legal advice'),
    ]
    sources = []
    for sid,publisher,url,locator,version,rights,raw,state,limit in source_specs:
        # Same organisation/product family is one source theme, with explicit children.
        theme = {'REPORTS':'SCORE','SC_AU_REPORT':'SCORE','SC_FOREST':'SCORE','AGGI':'GML'}.get(sid,sid)
        sources.append(dict(source_id=sid,theme_id=theme,publisher=publisher,url=url,locator=locator,version=version,
          rights=rights,review_state=state,sha_if_downloaded=receipts[raw]['sha256'] if raw else None,
          raw_receipt_id=raw,publication_mode='FACTS_LINKS_OWN_ANALYSIS_ONLY',raw_redistributed=False,
          retrieved_date='2026-11-09',limitations=limit))
    inherited = [
      ('PR140','climateos_methane_factor_order_001/evidence/ch4_brw_2024_subset.txt','77a35e2723372a290579e4549a86781e2be65c04','NOAA original subset inherited; no new statistical experiment'),
      ('PR143','climateos_methane_physics_knowledge_engine_001/EQUATION_REGISTRY.json','746825e65b8ddbd0f518709c94d9476df107208b','Existing formula and physical boundary registry; Chain B still BLOCKED'),
      ('PR145','climateos_global_method_evidence_ecochain_001/reviewer.py','ae1050a621ac794e447f9ac047865d90b2f04b03','Internal synthetic arithmetic only, no external trust anchor or actual role appointments'),
      ('TASK','global_natural_systems_evidence_atlas_001/TASKBOOK_ZH.md','a5c479b07b4a3a7e654e188505657f5715d39b1c','Founder bounded prototype authorization; not scientific admission'),
    ]
    for sid,p,rev,limit in inherited:
        path=ROOT/'docs/tasks'/p
        sources.append(dict(source_id=sid,theme_id='INHERITED',publisher='existing reviewed repository',
          url=f'https://github.com/simon947161/eco-agent-system/blob/{rev}/docs/tasks/{p}',locator='docs/tasks/'+p,
          version=rev,rights='INHERITED_REFERENCE_ONLY',review_state='SOURCE_VERIFIED',
          sha_if_downloaded=digest(path),hash_basis='LF-normalized inherited text',raw_receipt_id=None,
          publication_mode='REFERENCE_ONLY',raw_redistributed=False,retrieved_date='2026-11-09',limitations=limit))
    write('SOURCES.json',sources)
    bysource={s['source_id']:s for s in sources}
    unitspec=[
      ('ATM_GLOBAL','大气全球混合库','atmosphere','GML','global; not a uniform local field'),
      ('ATM_WALKER','Walker 环流研究单元','atmosphere','ENSO','tropical Pacific atmosphere'),
      ('ATM_BOUNDARY','边界层观测支持域','atmosphere','PR140','BRW point sampling, no global spatial interpolation'),
      ('CLIMATE_ZONES','Köppen-Geiger 分类接口','atmosphere','KG','1 km product metadata; no zone assignment'),
      ('PACIFIC','热带太平洋','ocean','ENSO','basin context, not EEZ sovereignty'),
      ('HIGH_SEAS','公海外部索引','ocean','NE','legal boundaries UNKNOWN; no country owner'),
      ('COASTAL','珊瑚与沿岸生态接口','ocean','IUCN','ecosystem class only; no habitat polygons'),
      ('BLUE_UPPER','埃塞俄比亚青尼罗河上游','hydrology','NBI','upstream reach context'),
      ('BLUE_LOWER','苏丹青尼罗河下游','hydrology','NBI','Eldeim to Khartoum context'),
      ('MAIN_NILE','尼罗河干流苏丹—埃及','hydrology','NBI','confluence to Aswan context'),
      ('BASIN_NILE','尼罗河跨境流域','hydrology','NBI','drainage basin; not main-stem passage through every country'),
      ('HYDROBASINS','全球嵌套流域分类接口','hydrology','HYDRO','metadata only, Antarctica excluded'),
      ('TERRESTRIAL','陆地生物群区分类接口','terrestrial','IUCN','forest/wetland/peatland/dryland/agroecosystem classes'),
      ('AMAZON_CONTEXT','亚马孙研究候选背景','terrestrial','IUCN','author context label; no authoritative boundary acquired'),
      ('BOREAL_CONTEXT','北方森林与冻土候选背景','terrestrial','IUCN','author context label; no measured permafrost fraction'),
      ('CRYOSPHERE','冰川/海冰/积雪/冻土接口','cryosphere','IUCN','class registration; extent and epoch UNKNOWN'),
      ('POLAR','极地独立研究索引','cryosphere','NE','no national assignment; polar geometry absent'),
      ('REGIONAL_RAIN','区域降雨风险支持域','atmosphere','ENSO','Australia/Indonesia contextual association, not forecasts'),
      ('CH4_SOURCE','甲烷源项研究接口','human','PR143','waste/energy/agriculture; no real facility rate'),
      ('LAND_USE','土地利用及农业接口','human','IUCN','system class only; no activity inventory'),
      ('SUPPLY_CHAIN','贸易与供应链接口','human','TASK','unpopulated research class; no embodied emissions'),
      ('FORCING','全球辐射强迫接口','atmosphere','AGGI','global effective forcing, W m-2; not local temperature'),
      ('CLIMATE_RESPONSE','气候响应未运行接口','atmosphere','IPCC','response kernel, feedbacks and attribution NOT_ADMITTED'),
      ('POLICY_CONTEXT','政策承诺与评价层','governance','SCORE','country assessments; never physical parameters'),
      ('TREATY_METHOD','条约/许可/核算方法接口','governance','PR145','jurisdiction-version reporting period required'),
    ]
    units=[]
    for uid,name,system,source,scale in unitspec:
        units.append(dict(id=uid,name=name,system=system,source=source,version=bysource[source]['version'],
          geometry_ref=None,CRS='NOT_APPLICABLE_NO_GEOMETRY',valid_time='UNKNOWN',scale=scale,
          coverage='METADATA_OR_QUALITATIVE_CONTEXT_ONLY',confidence='NOT_QUANTIFIED',
          uncertainty='No geometry, area fraction, numerical influence or local calibration admitted',
          license=bysource[source]['rights'],status='METADATA_ONLY'))
    # Country selection is mechanism/biome/vulnerability based, not an ordering of sizes.
    cases=[
      ('156','China',['CLIMATE_ZONES','CH4_SOURCE'],'东亚/季风、能源农业与区域差异'),
      ('643','Russia',['BOREAL_CONTEXT','CRYOSPHERE','CH4_SOURCE'],'北方生态与冻土；内部70%/30%政策文字冲突'),
      ('356','India',['CLIMATE_ZONES','CH4_SOURCE'],'南亚季风/农业；强度承诺不能替代绝对排放'),
      ('458','Malaysia',['TERRESTRIAL','COASTAL'],'海洋大陆、湿热生态；评分覆盖缺口'),
      ('360','Indonesia',['REGIONAL_RAIN','TERRESTRIAL','CH4_SOURCE'],'海洋大陆与ENSO条件降雨关联'),
      ('076','Brazil',['AMAZON_CONTEXT','LAND_USE'],'热带森林/土地利用；不能以国家等同亚马孙'),
      ('036','Australia',['REGIONAL_RAIN','CH4_SOURCE','POLICY_CONTEXT'],'ENSO条件关联；既有Batlow与甲烷审查接口'),
      ('840','United States',['ATM_BOUNDARY','CH4_SOURCE'],'复用BRW点观测；点位不代表全国'),
      ('276','Germany',['TERRESTRIAL','POLICY_CONTEXT'],'欧洲制度代表；欧盟评分不能复制为成员国效果'),
      ('231','Ethiopia',['BLUE_UPPER','BASIN_NILE'],'跨境上游；官方NDC登记替补政策背景'),
      ('818','Egypt',['MAIN_NILE','BASIN_NILE'],'跨境下游/干旱区；不推出分水权利'),
      ('242','Fiji',['PACIFIC','COASTAL'],'小岛屿/沿岸暴露；不外推某次灾害归因'),
    ]
    facts=json.loads((T/'evidence/m49-facts.json').read_text(encoding='utf-8'))
    score=json.loads((T/'evidence/scorecard-facts.json').read_text(encoding='utf-8'))
    scoreby={r['name']:r for r in score['records']}
    deep={c[0]:c for c in cases}
    countries=[]
    for row in facts['rows']:
        code=row['M49 Code']; case=deep.get(code)
        countries.append(dict(id='M49:'+code,m49=code,name=row['Country or Area'],iso2=row['ISO-alpha2 Code'],iso3=row['ISO-alpha3 Code'],
          region=row['Region Name'],subregion=row['Sub-region Name'],source='M49',version=VERSION,
          geometry_ref=None,CRS='NOT_APPLICABLE_NO_GEOMETRY',valid_time='2026-11-09 snapshot, validity interval UNKNOWN',
          scale='country-or-area statistical identity, not natural boundary',coverage='DEEP_METADATA_CASE' if case else 'REGISTER_ONLY_UNKNOWN',
          confidence='IDENTIFIER_EXTRACT_VERIFIED',uncertainty='No global scientific or geometry coverage implied',
          license=bysource['M49']['rights'],status='SOURCE_VERIFIED' if case else 'NOT_ASSESSED',
          natural_units=case[2] if case else [],geometry_status='NOT_ACQUIRED',science_status='PENDING',
          scorecard_coverage=('COVERED_STALE_ASSESSMENT' if case[1] in scoreby else 'NOT_COVERED_ON_AUDITED_SCORECARD') if case else 'NOT_ASSESSED'))
    write('GLOBAL_COVERAGE_REGISTER.json',dict(version=VERSION,standard='UN M49 English online snapshot',
      source_sha256=facts['source_sha256'],count=len(countries),countries=countries,
      beyond_country_units=['PACIFIC','HIGH_SEAS','POLAR','BASIN_NILE','ATM_GLOBAL'],
      geometry_acquired_count=0,geometry_coverage_fraction=0,deep_case_count=len(cases)))
    policies=[]; links=[]
    ndc_dates={'458':'2025-10-24','231':'2025-09-26','818':'2026-11-08','242':'2025-11-06'}
    for code,name,uids,reason in cases:
        published=scoreby.get(name)
        policies.append(dict(id='POLICY:'+code,country_id='M49:'+code,display_name=name,
          type='COUNTRY_POLICY_SCORE' if published else 'POLICY_COMMITMENT',
          evidence_type='POLICY_ASSESSMENT' if published else 'POLICY_COMMITMENT',
          source_id='SCORE' if published else 'NDC',source_locator=name+' card' if published else name+' NDC 3.0 registry row',
          score=published['published_percent_label'] if published else None,unit='published_policy_percent_label' if published else 'not_applicable',
          category=published['category'] if published else 'NOT_COVERED_ON_AUDITED_SCORECARD',
          version=score['dateModified'] if published else 'NDC 3.0 registry metadata',
          valid_time='UNKNOWN' if published else ndc_dates[code],time_semantics='ASSESSMENT_VALIDITY_UNKNOWN' if published else 'SUBMISSION_DATE_ONLY',
          review_state='MATERIAL_CONTRADICTION' if code=='036' else ('SOURCE_VERIFIED' if published else 'EVIDENCE_INSUFFICIENT'),
          selection_reason=reason,source_fact=published if published else None,not_inferable='observed reduction, emissions factor, warming benefit or current legal compliance',
          contradictions=['AU card base year 2030 versus AU_ACT s10 base year 2005'] if code=='036' else (['Russia 70% reduction wording conflicts with 30% below 1990 wording; not adjudicated'] if code=='643' else [])))
        for uid in uids:
            supported=uid in ('REGIONAL_RAIN','BLUE_UPPER','MAIN_NILE','BASIN_NILE','ATM_BOUNDARY')
            links.append(dict(country_id='M49:'+code,unit_id=uid,relation='RESEARCH_CONTEXT_NOT_GEOMETRIC_OVERLAY',
              mapping_basis='SOURCE_QUALITATIVE_CONTEXT' if supported else 'AUTHOR_RESEARCH_SELECTION',
              source_id=next(u['source'] for u in units if u['id']==uid),fraction=None,
              status='SOURCE_VERIFIED' if supported else 'NOT_ASSESSED',version=VERSION))
    # Sudan is route context only; it is not a thirteenth deep policy case.
    for uid in ('BLUE_LOWER','MAIN_NILE','BASIN_NILE'):
        links.append(dict(country_id='M49:729',unit_id=uid,relation='RESEARCH_CONTEXT_NOT_GEOMETRIC_OVERLAY',
          mapping_basis='SOURCE_QUALITATIVE_CONTEXT',source_id='NBI',fraction=None,status='SOURCE_VERIFIED',version=VERSION))
    write('POLICIES.json',policies)
    evidence=[]
    def ev(cid,typ,src,claim,nodes,unit='not_applicable',state='SOURCE_VERIFIED',start=None,end=None,method='qualitative_source_audit',origin='PUBLIC_METADATA',value=None,limit='No numerical magnitude or causal attribution established'):
        s=bysource[src]
        evidence.append(dict(claim_id=cid,evidence_type=typ,source_id=src,version=s['version'],source_locator=s['locator'],
          claim=claim,rights=s['rights'],sha_if_downloaded=s['sha_if_downloaded'],geographic_support=nodes,
          time_support=dict(start=start,end=end,timezone='UTC' if start else 'UNKNOWN',semantics='OBSERVATION_WINDOW' if start else 'UNKNOWN_NOT_INFERRED_FROM_RETRIEVAL'),
          method_id=method,unit=unit,value=value,uncertainty=limit,calibration_QA='Inherited instrument QA not revalidated' if typ=='PHYSICAL_OBSERVATION' else 'Metadata structure checked; no instrument calibration implied',
          review_state=state,contradictions=[],not_inferable_from=[limit],origin=origin))
    ev('NILE_CONNECT','SCIENTIFIC_LITERATURE','NBI','NBI technical station descriptions identify directional cross-border monitoring context',['BLUE_UPPER','BLUE_LOWER','MAIN_NILE','BASIN_NILE'])
    ev('ENSO_MECHANISM','SCIENTIFIC_LITERATURE','ENSO','Coupled Pacific ocean-atmosphere process with conditional regional rainfall associations',['PACIFIC','ATM_WALKER','REGIONAL_RAIN'],limit='No deterministic regional drought, methane or event attribution')
    ev('CH4_PHYSICS','SCIENTIFIC_LITERATURE','PR143','Existing methane mass and transport/chemistry distinctions retained',['CH4_SOURCE','ATM_GLOBAL'],limit='No admitted facility flow, global emissions or vertical correction')
    ev('GML_GLOBAL','DERIVED_DATA','GML','Marine surface observations are aggregated into a global mean product',['ATM_GLOBAL'],unit='nmol mol-1',method='NOAA marine surface aggregation metadata',limit='No numerical series imported; latest year preliminary; cannot invert a site flux')
    ev('AGGI_METHOD','MODEL_OUTPUT','AGGI','Metadata for effective forcing derived from global abundances; no output array imported',['ATM_GLOBAL','FORCING'],unit='W m-2',state='NOT_ASSESSED',method='AGGI 2025 effective forcing metadata',limit='Model output type registered as metadata only; not a newly computed result or temperature response')
    ev('RESPONSE_GAP','SCIENTIFIC_LITERATURE','IPCC','Climate response evidence locator retained; this batch full-text access blocked',['FORCING','CLIMATE_RESPONSE'],state='BLOCKED',limit='403; no climate response calculation, local benefit or exact kernel admitted')
    ev('BRW_EXISTING','PHYSICAL_OBSERVATION','PR140','Previously archived NOAA BRW CH4 observation subset, referred to without reanalysis',['ATM_BOUNDARY'],unit='nmol mol-1',start='2024-01-01T00:00:00Z',end='2025-01-01T00:00:00Z',method='inherited NOAA BRW surface in-situ observation',origin='INHERITED_OBSERVATION',limit='Subset-specific completeness/QA retained in PR140; no valid paired flux or vertical profile')
    ev('AU_TARGET','LEGAL_METHOD','AU_ACT','Section 10(1)(a) target uses a 2005 reference year',['POLICY_CONTEXT'],method='AU/C2025C00153/s10',limit='Policy target is not achieved outcome and not an emissions estimation method')
    for p in policies:
        ev('EV:'+p['id'],p['evidence_type'],p['source_id'],'Published policy label or registry submission metadata for '+p['display_name'],
           ['M49:'+p['country_id'].split(':')[1]],unit=p['unit'],state=p['review_state'],method=p['type'],limit=p['not_inferable'])
        evidence[-1]['contradictions']=p['contradictions']
    ev('AU_COUNTRY_REPORT','POLICY_ASSESSMENT','SC_AU_REPORT','Australian forecast article metadata, author Jessica Gregory; not an observed future outcome',['M49:036'],method='COUNTRY_REPORT',limit='Forecast narrative cannot become 2026 observed emissions or ecological benefit')
    ev('OUTCOME_GAP','ECOLOGICAL_OUTCOME','SC_FOREST','Forest report is a pointer for independent ecological outcome verification, not measured outcome evidence',['TERRESTRIAL'],state='EVIDENCE_INSUFFICIENT',method='OBSERVED_OUTCOME_NOT_ADMITTED',limit='No harmonised forest-change observations or counterfactual admitted')
    ev('FOUNDER_SCOPE','GOVERNANCE_DECISION','TASK','Bounded Atlas implementation authorized; scientific admission unchanged',['POLICY_CONTEXT'],method='task scope authorization',limit='No human scientific acceptance, statutory certificate or deployment permission')
    ev('INTERNAL_REPLAY','SYNTHETIC_TEST','PR145','Existing A/B/C internal methane-ledger replay through original reviewer',['CH4_SOURCE'],unit='kg_CH4/interval',state='RECALCULATED',origin='SYNTHETIC',method='INTERNAL_FIXTURE_REPLAY_ONLY',limit='Not submitted-data validity, field validation, external approval or real mitigation')
    write('EVIDENCE.json',evidence)
    edges=[]
    def edge(eid,a,b,typ,process,evs,causal,space,time,assumptions,counter,limit):
        edges.append(dict(id=eid,from_id=a,to_id=b,type=typ,process=process,direction='from_to',spatial_scale=space,
          temporal_scale=time,evidence_ids=evs,causality=causal,assumptions=assumptions,counterevidence=counter,
          applicability=limit,version=VERSION,status='BLOCKED' if eid=='M3' else 'SOURCE_VERIFIED',
          unit='not_applicable_qualitative',numeric_weight=None))
    edge('N1','BLUE_UPPER','BLUE_LOWER','PHYSICAL_TRANSPORT','nile_flow',['NILE_CONNECT'],'MECHANISM_SUPPORTED','cross-border river reaches','travel time UNKNOWN; daily/seasonal storage matters',
      'Direction from reach topology, not nationality','Reservoir releases, abstraction, lateral tributaries and storage prevent equal upstream/downstream instantaneous flow','No quantified downstream effect or allocation rights')
    edge('N2','BLUE_LOWER','MAIN_NILE','PHYSICAL_TRANSPORT','nile_flow',['NILE_CONNECT'],'MECHANISM_SUPPORTED','confluence to downstream reach','routing time UNKNOWN',
      'White Nile and Atbara contributions must be included','A closure residual requires storage/tributaries before attributing upstream responsibility','Topology only, no gauges or geometry loaded')
    edge('E1','PACIFIC','ATM_WALKER','CLIMATE_TELECONNECTION','enso',['ENSO_MECHANISM'],'COUPLED_MECHANISM','tropical Pacific ocean-atmosphere','seasonal/interannual',
      'Displayed arrow is an explanatory path; feedback is bidirectional','Warm SST alone without atmospheric coupling does not establish coupled ENSO','No one-way mass transport or deterministic country effect')
    edge('E2','ATM_WALKER','REGIONAL_RAIN','CLIMATE_TELECONNECTION','enso',['ENSO_MECHANISM'],'CONDITIONAL_ASSOCIATION','Australia/Indonesia context','season and event dependent',
      'Other modes, trend and regional heterogeneity confound the relation','A wet regional event during El Nino refutes a deterministic drought rule, not the probabilistic mechanism','No particular event attribution, rainfall amount or CH4 response')
    edge('M1','CH4_SOURCE','ATM_GLOBAL','BIOGEOCHEMICAL_CYCLE','methane',['CH4_PHYSICS','GML_GLOBAL'],'MECHANISM_SUPPORTED','local sources to global burden','transport and chemical loss times differ',
      'All source/sink terms and air mass needed for any quantitative budget','Concentration changes also reflect transport and sink variation','Local ppm is not flux, global burden or responsibility share')
    edge('M2','ATM_GLOBAL','FORCING','BIOGEOCHEMICAL_CYCLE','methane',['AGGI_METHOD'],'MECHANISM_SUPPORTED','global mean radiation','annual forcing product; no new run',
      'Global abundance, background gases and formula version required','AGGI excludes slow feedbacks and cannot validate local temperatures','Existing methodology linkage only, no GWP altitude adjustment')
    edge('M3','FORCING','CLIMATE_RESPONSE','HYPOTHESIS_ONLY','methane',['RESPONSE_GAP'],'NOT_VALIDATED_HERE','global to regional response unresolved','response times/kernel UNKNOWN',
      'A separately admitted response model and observational validation would be needed','Internal variability and other forcings prevent local causal inference','Boundary is research gap; not denial of established greenhouse mechanism')
    write('RELATION_GRAPH.json',dict(schema_version=VERSION,units=units,country_links=links,edges=edges,
      paths={'nile_flow':['N1','N2'],'enso':['E1','E2'],'methane':['M1','M2','M3']}))
    write('BUDGET.json',dict(new_source_themes=len({s['theme_id'] for s in sources if s['theme_id']!='INHERITED'}),
      deep_cases=len(cases),deep_mechanisms=3,new_GIS_datasets=0,geometry_acquired_count=0,
      limits=dict(new_source_themes=15,deep_cases=12,deep_mechanisms=3,new_GIS_datasets=3)))
    print('Built bounded Atlas data; metadata only, no geometry or emissions calculations')

if __name__=='__main__': build()
