"""Reconstruct bounded LSPS2020 factual research from its registered temporary original.
No original body/images are redistributed. Source occurrences and source conflicts remain distinct.
"""
import argparse,collections,csv,datetime,hashlib,json,re
from pathlib import Path
import pdfplumber,pypdf
APP=Path(__file__).resolve().parents[1]
SOURCE='csoi:smrc-lsps-2020:20261030';RAW='sha256:9bf75ec6fb98f1d03bad47f5b9cda44e6ffadce3bf452eb5a343b394322f8f47'
PREFIX='csoi:knowledge:lsps2020:'
PARSER='pypdf-'+pypdf.__version__+'-layout-whitespace-1'
# Authored short descriptions; none is an asserted current Council duty or completed work.
DESCRIPTIONS={
'1.1':('Aboriginal heritage study','Study regional Aboriginal heritage with Ngarigo and local land-council participation, then pursue the study actions.'),
'1.2':('Bombala and Delegate heritage controls','Review development controls for Bombala and Delegate, addressing streetscape, built form, heritage significance and visual amenity.'),
'1.3':('Cooma conservation controls','Re-examine controls applying to Cooma heritage conservation areas.'),
'1.4':('Regional heritage strategy','Prepare a region-wide heritage strategy.'),
'1.5':('Bundian Way collaboration','Advance Bundian Way with Eden Aboriginal Land Council, Ngarigo representatives and Delegate Progress Association.'),
'1.6':('Maybe Street conservation area','Establish a heritage conservation area for Maybe Street, informed by the heritage study.'),
'1.7':('Delegate main-street heritage','Use a heritage conservation area to retain Delegate main-street character.'),
'1.8':('Nimmitabel heritage and reuse','Review Nimmitabel heritage controls for compatible development and encourage restoration and adaptive reuse of heritage items.'),
'2.1':('Significant landscape protection','Identify valued scenic areas for protection through the LEP and DCP.'),
'2.2':('Rural landscape strategy','Prepare rural land-use strategy work that addresses the visual importance of the regional landscape.'),
'2.3':('Rural development form and scale','Implement planning controls governing the form and scale of permissible rural development.'),
'3.1':('Biodiversity evidence for the LEP','Use rural-land and biodiversity studies to inform zones and local LEP provisions.'),
'3.2':('Koala management plan','Complete and put a comprehensive koala management plan into operation as a historical planning intention.'),
'3.3':('Waterway pollution controls','Prepare planning controls intended to protect rivers and other waterways against pollution.'),
'3.4':('Jindabyne domestic animals','Explore local domestic-animal management options for Jindabyne.'),
'3.5':('Koala policy coordination','Coordinate with the NSW Government on a koala management plan under the then-described Koala SEPP.'),
'4.1':('Council emissions audit','Examine Council greenhouse-gas emissions to identify improvement opportunities; no resulting inventory is supplied here.'),
'4.2':('Sustainable subdivision controls','Review and update DCP provisions to improve subdivision sustainability, considering solar orientation, active transport, stormwater management and open space.'),
'4.3':('Public planting diversity','Expand the amount and variety of planting in public streets, parks and spaces.'),
'4.4':('New-development stormwater practice','Implementation wording calls for best-practice stormwater design, including tanks for non-potable reuse; narrative wording is less mandatory.'),
'4.5':('Agroforestry investigation','Explore agroforestry and its possible carbon-offset role without treating a potential benefit as measured reduction.'),
'4.6':('Renewable-energy exclusion study','Map areas considered unsuitable for large renewable-energy development because of ecological or scenic values.'),
'5.1':('Detailed rural-land strategy','Prepare a detailed regional rural land-use strategy.'),
'5.2':('Agriculture in the consolidated LEP','Prepare a consolidated LEP intended to prevent fragmentation of agricultural and resource land while facilitating compatible rural development and value-adding agriculture.'),
'5.3':('Agri-tourism corridor study','Investigate agri-tourism opportunities near the corridors shown in figures19 and28 and recommend land uses supporting farm innovation and diversification.'),
'5.4':('Intensive agriculture precincts','Investigate locations and planning controls for productive intensive-agriculture precincts.'),
'5.5':('Rural purchaser information','Use section10.7 planning certificates to inform prospective rural purchasers about agricultural priorities.'),
'6.1':('Employment land requirements','Analyse how much industrial and employment land is needed for prospective growth.'),
'6.2':('Flexible shared workspaces','Revisit controls for shared offices and collaboration suited to a mobile, flexible workforce.'),
'6.3':('Polo Flat improvement plan','Plan upgrades in Polo Flat, Cooma, intended to support further industrial investment.'),
'6.4':('Government-owned investment sites','Identify public sites in major towns that could accommodate business or industry investment.'),
'6.5':('Cooma centre masterplan','Prepare a masterplan to guide the future of the Cooma central business district.'),
'6.6':('Large-floor-area business locations','Locate candidate Cooma sites suitable for businesses or industries needing large floor areas.'),
'6.7':('Berridale centre amenity','Investigate options for Berridale town-centre amenity and appearance through settlement-strategy work.'),
'7.1':('Alpine Way tourism access corridor','Assess current and potential uses of the Alpine Way corridor through KNP and the suitability of tourism planning controls.'),
'7.2':('Tourism funding options','Investigate ways of funding tourism, including possible levies.'),
'7.3':('Tourism planning reform','Identify control changes supporting varied tourism development and propose a planning-reform lead.'),
'7.4':('Year-round alpine tourism','Broaden tourism activities in Jindabyne and the Snowy Mountains across the year.'),
'7.5':('Regional trails planning','Develop a regional masterplan for trails.'),
'8.1':('Locally responsive LEP','Prepare the LEP and supporting documents around differing community, locality and landscape needs.'),
'8.2':('Review proposed State instruments','Review State environmental-planning proposals and provide feedback or seek exclusions where warranted.'),
'8.3':('Town and village settlement strategy','Prepare settlement direction for distinct towns and villages using the stated planning priorities and objectives.'),
'8.4':('Jindabyne alpine architecture','Use controls to support varied alpine design and environmental performance in Jindabyne.'),
'8.5':('Berridale zoning and growth','Examine Berridale zoning and potential surrounding growth.'),
'8.6':('Michelago structure plan','Prepare a structure plan to guide future Michelago growth.'),
'8.7':('Diverse rural landscapes','Prepare rural-land strategy direction responsive to different landscapes.'),
'8.8':('Village-specific DCP chapters','Prepare tailored DCP chapters for maintaining and enhancing village character.'),
'8.9':('Recreation needs strategy','Plan for future community recreation needs through a recreation strategy.'),
'8.10':('Therry Street pocket park','The plan proposes completing the final Stronger Communities Fund stage at Therry Street Pocket Park; completion is unverified.'),
'9.1':('Staged greenfield rezoning','Rezone greenfield land following settlement-strategy staging and sequencing.'),
'9.2':('Monitor housing provision','Review and update settlement planning against community housing needs and demand.'),
'9.3':('Jindabyne housing and the SAP','Consider the final Snowy Mountains SAP with government and community participation to widen housing options around Jindabyne.'),
'9.4':('Adaptable housing','Support adaptable housing through relevant planning instruments and controls.'),
'9.5':('Appropriate rural-residential sites','Plan rural-residential locations consistently with land-use strategies and the regional plan.'),
'9.6':('Rural land-use conflict','Use controls to reduce conflicts between rural housing and primary production.'),
'10.1':('Regional transport and access strategy','Develop integrated regional transport and access planning.'),
'10.2':('Walking and shared paths','Develop and implement a strategy for footpaths and shared paths.'),
'10.3':('Pedestrian access plan','Develop and implement pedestrian access and mobility planning.'),
'10.4':('Rail corridor reuse options','Explore a Monaro rail trail on the Bombala rail corridor and retain rail reinstatement as a conditional option if viable.'),
'10.5':('Intergovernmental road improvements','Engage NSW and ACT authorities on improvements to the nine named road corridors.'),
'10.6':('Jindabyne traffic and parking','Work with NSW and the Snowy Mountains SAP team on Jindabyne traffic and parking problems.'),
'10.7':('Heavy-vehicle alternatives','Investigate heavy-vehicle alternatives for Cooma, Bombala and Berridale; the core narrative also mentions a Jindabyne bypass investigation.'),
'10.8':('Cooma centre movement','Explore safer, more accessible pedestrian movement and better traffic permeability in central Cooma.'),
'10.9':('Maybe Street amenity','Improve amenity along Maybe Street as a published intention.'),
'10.10':('Regional contributions plan','Prepare a development-contributions plan for roads, recreation, active transport and community infrastructure.'),
'10.11':('Michelago contribution-funded works','Include the identified causeway and road upgrades in a Michelago development-contributions plan.'),
'11.1':('Bushfire-prone land mapping','Update mapping to represent bushfire exposure, including grassland risk.'),
'11.2':('Flood planning controls','Translate flood-risk management plans for five named settlements into planning controls.'),
'11.3':('Sensitive uses and natural hazards','Assess land-use compatibility with hazards, giving specific consideration to hospitals, schools and aged-care facilities.'),
'11.4':('Snowy Hydro flood evidence','Use Snowy Hydro flood information for planning near lakes Jindabyne and Eucumbene.'),
'11.5':('Integrated water-cycle strategy','Develop integrated water-cycle management planning.'),
'11.6':('Drought and water-efficiency controls','Review and update development controls, policies, guidelines and public-domain projects to improve water efficiency in response to drought and water availability.'),
'11.7':('Landslide-risk planning','Map landslide exposure and develop associated planning controls.'),
'11.8':('Shade-sensitive design','Review DCP design provisions in light of shade guidance.'),
'11.9':('Healthy ageing controls','Review development controls against Heart Foundation themes for healthy active ageing.'),
'12.1':('Population scenarios','Prepare a policy setting out alternative regional population-change scenarios.'),
'12.2':('Michelago water and wastewater options','Investigate Michelago water and wastewater options; the core narrative names water only.'),
'12.3':('Infrastructure for growing towns','Assess infrastructure needs in places including Jindabyne and Berridale and work with NSW on provision.'),
'12.4':('Growth where capacity exists','Direct and encourage growth toward existing infrastructure capacity through strategic plans.'),
'12.5':('Business and resident attraction','Prepare a business-investment portfolio and a policy aimed at long-term residents.'),
'12.6':('Berridale electricity capacity','Investigate with electricity providers effective ways to expand Berridale system capacity.'),
'12.7':('Berridale sewage treatment options','Investigate sewage-treatment upgrades against anticipated Berridale growth.'),
'12.8':('Old Adaminaby potable supply','Investigate potable-water options for Old Adaminaby.')}
PRIORITIES={1:'Cultural and built heritage',2:'Scenic landscape protection',3:'Environmental values and restoration',4:'A lower-carbon future',5:'Agriculture and related industry',6:'Business growth and efficiency',7:'Year-round alpine destination',8:'Locally responsive planning and recreation',9:'Housing choice',10:'Transport and development coordination',11:'Resilient communities and hazard planning',12:'Growth, business and population change'}
# Distinct intentions printed under reused or additional codes; do not silently merge by code.
SUPPLEMENTAL={
(27,'3.2'):('Terrestrial and aquatic ecosystems','The core narrative associates code3.2 with protection of high-value land and aquatic ecosystems; the implementation table uses that code for koala planning.'),
(27,'3.3'):('Koala plan under narrative code3.3','The narrative assigns koala-plan completion to3.3, whereas the implementation table assigns it to3.2.'),
(27,'3.4'):('Waterway protection under narrative code3.4','The narrative uses3.4 for waterway-pollution controls; implementation3.4 instead concerns domestic animals in Jindabyne.'),
(34,'5.4'):('Agriculture and rural tourism','Narrative5.4 concerns links between agriculture and suitable rural tourism; implementation5.4 concerns intensive-agriculture precincts.'),
(42,'8.1'):('Rural-land strategy under narrative code8.1','Narrative8.1 calls for a rural-land strategy tailored to different landscapes; implementation8.1 refers to an LEP and supporting planning documents.'),
(59,'6.4'):('Polo Flat under local code6.4','The Cooma chapter labels the Polo Flat upgrade plan6.4; implementation6.4 instead identifies government sites and6.3 covers Polo Flat.'),
(59,'6.6'):('Cooma centre plan under local code6.6','The Cooma chapter uses6.6 for its CBD masterplan; implementation6.6 instead concerns large-floor-area sites.'),
(59,'6.7'):('Cooma business sites under local code6.7','The Cooma chapter labels large-floor-area business sites6.7; implementation6.7 instead concerns Berridale centre amenity.'),
(64,'7.1'):('Jindabyne and KNP congestion','The Jindabyne chapter uses7.1 for congestion coordination with NSW; implementation7.1 concerns the Alpine Way tourism corridor.'),
(64,'7.2'):('Alpine Way under local code7.2','The Jindabyne chapter labels the Alpine Way corridor review7.2; implementation7.2 concerns tourism funding.'),
(64,'8.5'):('Alpine architecture under local code8.5','The Jindabyne chapter uses8.5 for alpine architecture controls; implementation8.5 concerns Berridale zoning.'),
(64,'12.6'):('SAP infrastructure under local code12.6','The Jindabyne chapter uses12.6 for masterplan/SAP infrastructure coordination; implementation12.6 concerns Berridale electricity.'),
(71,'6.8'):('Berridale road-reserve amenity','The Berridale chapter labels investigation of highway-services road-reserve amenity options6.8, a code absent from the implementation table; related town-centre work appears there as6.7.'),
(71,'8.6'):('Berridale zoning under local code8.6','The Berridale chapter labels zoning/growth review8.6; implementation8.6 is a Michelago structure plan.'),
(74,'8.7'):('Michelago structure plan under local code8.7','The Michelago chapter labels its structure plan8.7; implementation8.7 instead concerns rural-land strategy.'),
(74,'10.10'):('Michelago roads under local code10.10','The Michelago chapter labels specific road/causeway contributions10.10; implementation10.10 is the regional plan and10.11 carries the Michelago works.'),
(83,'8.9'):('Village DCP chapters under local code8.9','The village chapter labels local-character DCP chapters8.9; implementation8.9 concerns recreation and8.8 covers village chapters.'),
(89,'5.7'):('Rural housing conflict under local code5.7','The rural chapter labels conflict controls5.7, a code absent from the implementation table; the corresponding general action is listed there as9.6.')}
ANOMALIES={
'2.1':['Implementation timing is printed Medium/ with no following timing label; do not complete the missing value.'],
'3.1':['Implementation Who cell ends SMRC & without identifying the additional party. Narrative calls the study Rural Lands Study; implementation says Rural Land Use Strategy; rural chapter says Rural Lands Analysis.'],
'4.2':['Narrative action has a shorter sustainability statement; implementation explicitly lists solar orientation, active transport, stormwater and open space.'],
'4.4':['Narrative PDF31 says encourage while implementation PDF93 says require; neither wording is promoted to a current legal obligation.'],
'5.3':['Narrative PDF34 points to figure19, rural PDF89 to figure28, and implementation PDF94 names both; geographic interpretation remains unverified.'],
'6.4':['Narrative PDF37 additionally calls for suitable planning controls on the identified sites.'],
'6.5':['Narrative PDF37 expands on commercial guidance and a vibrant regional commercial core.'],
'6.7':['Narrative PDF37 specifies the Berridale highway-services road reserve; implementation PDF95 uses town centre.'],
'7.2':['Narrative PDF39 additionally describes accommodation/business levies and regional/NSW investment; these are not approved charges.'],
'7.3':['Narrative PDF39 describes a regional reform lead; implementation PDF96 says across the state.'],
'8.9':['Narrative PDF42 includes recreation-needs analysis and long-term management, beyond the implementation synopsis.'],
'9.3':['Narrative PDF45 ends with government/community collaboration; implementation PDF98–99 explicitly adds diverse housing for Jindabyne and surrounds.'],
'9.6':['Narrative PDF45 uses a generic land-use-conflict statement; implementation PDF99 identifies rural housing and primary production.'],
'10.7':['Narrative PDF50 additionally names investigation of an alternative route/bypass for Jindabyne; implementation PDF101 omits that extension.'],
'12.2':['Narrative PDF55 names a water-options study; local PDF74 and implementation PDF103 name both water and wastewater.'],
'12.5':['Implementation PDF103 has the source spelling buisness; authored label uses standard spelling without altering intent.']}
TIMEFRAMES={'Immediate':{'minimumYearsAfterAdoption':0,'maximumYearsAfterAdoption':1},'Short':{'minimumYearsAfterAdoption':1,'maximumYearsAfterAdoption':5},'Medium':{'minimumYearsAfterAdoption':5,'maximumYearsAfterAdoption':10},'Long':{'minimumYearsAfterAdoption':10,'maximumYearsAfterAdoption':20},'Ongoing':{'basis':'WHEN_ITEM_ARISES'}}
def norm(s):return ' '.join(s.split())
def digest(s):return 'sha256:'+hashlib.sha256(s.encode()).hexdigest()
def words_text(ws):return norm(' '.join(w['text']for w in sorted(ws,key=lambda x:(round(x['top']/2)*2,x['x0']))))
def header(p):
 ws=p.extract_words();row=next(w['top']for w in ws if w['text']=='No.'and 80<w['top']<350);h={k:next(w for w in ws if w['text']==k and abs(w['top']-row)<2)for k in ['No.','Action','Timing','Who','Funded','CSP','DCP','LEP','CP','Strategy','Other']}
 y=h['No.']['top'];bottom=max(w['bottom']for w in ws if y-2<=w['top']<y+30)
 return ws,h,bottom

def table(pdf):
 rows=[];priorities={}
 for pn in range(90,105):
  p=pdf.pages[pn-1];ws,h,ht=header(p);starts=sorted([w for w in ws if w['x0']<100 and w['top']>ht and re.fullmatch(r'\d{1,2}\.\d{1,2}',w['text'])],key=lambda w:w['top'])
  headings=[w for w in ws if w['text']=='Planning'and w['x0']<100 and w['top']>ht]
  last=min([w['top']for w in ws if w['text'].startswith('*Please')]+[525.0])
  events=sorted([(w['top']-2,'action',w)for w in starts]+[(w['top']-2,'priority',w)for w in headings]+[(last,'end',None)])
  names=['Action','Timing','Who','Funded','CSP','DCP','LEP','CP','Strategy','Other'];bounds=[h[k]['x0']-5 for k in names]+[780]
  def segment(y0,y1):
   columns={key:words_text([w for w in ws if bounds[i]<=w['x0']<bounds[i+1]and y0<=w['top']<y1])for i,key in enumerate(names)}
   tick=[]
   for im in p.images:
    if y0<=im['top']+3<y1:
     c=next((key for i,key in enumerate(names)if bounds[i]<=im['x0']<bounds[i+1]),None)
     if c in ['DCP','LEP','CP','Strategy','Other']:tick.append({'category':c,'imageDigest':'sha256:'+hashlib.sha256(im['stream'].get_data()).hexdigest(),'bbox':[round(im[k],3)for k in ['x0','top','x1','bottom']]})
   relevant=[w for w in ws if 70<=w['x0']<780 and y0<=w['top']<y1];bottom=min(y1,max([w['bottom']for w in relevant]+[y0+2])+2)
   return {'pdfPage':pn,'bbox':[70,round(y0,3),780,round(bottom,3)],'columns':columns,'ticks':tick}
  if events and events[0][0]>ht+3:
   cont=segment(ht+2,events[0][0]);
   if cont['columns']['Action']:
    assert rows,(pn,cont);rows[-1]['segments'].append(cont)
  for i,(y,kind,w)in enumerate(events[:-1]):
   if kind=='priority':
    txt=words_text([x for x in ws if 70<=x['x0']<780 and y<=x['top']<events[i+1][0]])
    code=int(re.search(r'Priority\s+(\d+)',txt)[1]);priorities[code]={'pdfPage':pn,'bbox':[70,round(y,3),780,round(events[i+1][0],3)],'title':txt}
   else:rows.append({'code':w['text'],'segments':[segment(y,events[i+1][0])]})
 return rows,priorities

def narratives(pdf):
 out=[]
 for pn in range(23,90):
  p=pdf.pages[pn-1];ws=p.extract_words();starts=[]
  for w in ws:
   if w['x0']>290 and re.fullmatch(r'\d{1,2}\.\d{1,2}',w['text'])and any(v['text']==''and abs(v['top']-w['top'])<4 and 0<w['x0']-v['x0']<35 for v in ws):starts.append(w)
  for i,w in enumerate(starts):
   end=starts[i+1]['top']-1 if i+1<len(starts)else min(775,p.height-55)
   selected=[v for v in ws if v['x0']>=w['x0']-1 and w['top']-1<=v['top']<end]
   out.append({'code':w['text'],'pdfPage':pn,'bbox':[round(w['x0']-1,3),round(w['top']-1,3),round(p.width-35,3),round(max(v['bottom']for v in selected)+1,3)],'text':words_text(selected)})
 return out

def make(pdfpath):
 body=pdfpath.read_bytes();assert 'sha256:'+hashlib.sha256(body).hexdigest()==RAW
 reader=pypdf.PdfReader(pdfpath);assert len(reader.pages)==118
 hashes={n:digest(norm(reader.pages[n-1].extract_text(extraction_mode='layout')or''))for n in range(1,119)}
 def anchor(p,bbox=None):
  a={'pdfPage':p,'normalizedPageDigest':hashes[p],'parserVersion':PARSER}
  if bbox:a['bbox']=bbox
  return a
 with pdfplumber.open(pdfpath)as pdf:rows,priorities=table(pdf);mentions=narratives(pdf)
 assert len(rows)==len({r['code']for r in rows})==83 and set(r['code']for r in rows)==set(DESCRIPTIONS)
 assert set(priorities)==set(range(1,13));assert set(SUPPLEMENTAL).issubset({(m['pdfPage'],m['code'])for m in mentions})
 records=[];doc={'id':PREFIX+'document','kind':'DocumentRevision','category':'DOCUMENT','code':'LSPS2020','parentId':None,'title':'LSPS2020 — historical priorities and action evidence','summary':'Research index of twelve planning priorities, the full numbered implementation table, and separately identified conflicting narrative/local action occurrences. Maps and other narrative evidence remain outside complete structured coverage.','locator':'PDF1 / printed0; adoption line; implementation PDF90–104 / printed89–103','anchor':anchor(1),'facts':{'documentTitle':'Snowy Monaro Local Strategic Planning Statement2020','printedAdoptionDate':'21 May 2020','totalPages':118,'prioritiesExpected':12,'prioritiesStructured':12,'implementationActionsExpected':83,'implementationActionsStructured':83,'actionCensusScope':'83 unique rows in implementation PDF90–104; supplemental narrative/local occurrences separately identified; duplicate codes are not presumed identical intents.','timeframeDefinitions':TIMEFRAMES,'timeframeDefinitionAnchor':anchor(90,[65,130,385,268]),'agencyNameDateBasis':'PDF104 states listed government agency names are as of2019 and may change.','currentLaw':'UNKNOWN','officialAdmission':'PENDING','wholeDocumentCoverage':'PARTIAL_CORE_CENSUS_WITH_SEPARATE_CONFLICT_OCCURRENCES_NOT_FULL_MAP_OR_NARRATIVE_EXTRACTION'},'relations':[]};records.append(doc)
 perpriority=collections.defaultdict(list)
 for r in rows:perpriority[int(r['code'].split('.')[0])].append(r)
 for num,p in priorities.items():
  group=perpriority[num]
  records.append({'id':PREFIX+'priority:'+str(num),'kind':'PlanningPriority','category':'PRIORITY','code':str(num),'parentId':doc['id'],'title':f'LSPS priority{num} — {PRIORITIES[num]}','summary':f'Historical planning priority about {PRIORITIES[num].lower()}, with {len(group)} implementation-table actions. Publication does not establish delivery or current statutory authority.','locator':f'PDF{p["pdfPage"]} / printed{p["pdfPage"]-1}; implementation priority heading','anchor':anchor(p['pdfPage'],p['bbox']),'facts':{'priorityNumber':num,'printedTitle':p['title'],'implementationActionCodes':[r['code']for r in group],'implementationActionCount':len(group),'printedResponsibleLabels':sorted({norm(' '.join(s['columns']['Who']for s in r['segments']))for r in group}),'printedTimingLabels':sorted({norm(' '.join(s['columns']['Timing']for s in r['segments']))for r in group}),'timingBasis':'Relative to2020 adoption, not a fresh due date','titleBasis':'Implementation-table heading; descriptive narrative and local variants retained separately','actualExecution':'UNKNOWN','actualOutcome':'UNKNOWN','currentBudget':'UNKNOWN','officialAdmission':'PENDING'},'relations':[]})
  for r in group:
   code=r['code'];segs=r['segments'];a=segs[0];cols={k:norm(' '.join(s['columns'][k]for s in segs))for k in a['columns']};title,description=DESCRIPTIONS[code];same=[m for m in mentions if m['code']==code and(m['pdfPage'],code)not in SUPPLEMENTAL];conflicts=[m for m in mentions if m['code']==code and(m['pdfPage'],code)in SUPPLEMENTAL]
   anomalies=list(ANOMALIES.get(code,[]))+[f'Distinct intention under the same printed code on PDF{m["pdfPage"]}; retained as '+PREFIX+f'narrative-action:p{m["pdfPage"]}:{code}'for m in conflicts]
   ticks=[{'pdfPage':s['pdfPage'],**t}for s in segs for t in s['ticks']];categories=sorted({t['category']for t in ticks})
   evidence=[{'role':'IMPLEMENTATION_ROW','anchor':anchor(s['pdfPage'],s['bbox']),'sourceCellDigests':{k:digest(v)for k,v in s['columns'].items()}}for s in segs]+[{'role':'RELATED_NARRATIVE_OR_LOCAL_OCCURRENCE','anchor':anchor(m['pdfPage'],m['bbox']),'occurrenceTextDigest':digest(m['text'])}for m in same]
   facts={'actionCode':code,'actionDescription':description,'priorityNumber':num,'sourceSection':'IMPLEMENTATION_TABLE','printedTiming':cols['Timing'],'printedWho':cols['Who'],'who':cols['Who'],'printedFunded':cols['Funded'],'funded':cols['Funded'],'fundingMeaning':'Historical published Yes/No/Part classification; no current budget, amount or expenditure established.','relativeTimeDefinitions':TIMEFRAMES,'timingBasis':'Years after LSPS adoption; not converted into a new deadline or current execution state.','timingDefinitionPdfPage':90,'timingDefinitionAnchor':anchor(90,[65,130,385,268]),'agencyNameBasis':'Agency labels are the source2019 naming, not current assigned officers.','responsibilityMeaning':'Historical published institutional attribution; no current person or Council assignment created.','relatedPolicyReferences':[{'printedCode':cols['CSP'],'column':'CSP Delivery Program','meaning':'Historical source reference; referenced document version unverified, not automatically mapped to CSP2035.'}],'printedRelatedDocumentCategories':categories,'untickedRelatedDocumentCategories':[x for x in ['DCP','LEP','CP','Strategy','Other']if x not in categories],'relatedDocumentCategoryMeaning':'Embedded tick image in named category; does not identify an operative document version or prove current legal implementation.','relatedDocumentTickEvidence':ticks,'evidenceAnchors':evidence,'sourceAnomalies':anomalies,'workState':'HISTORICAL_PUBLISHED_PLAN','actualCouncilAssignment':'NOT_CREATED','actualExecution':'UNKNOWN','actualOutcome':'UNKNOWN','actualSpend':'UNKNOWN','currentBudget':'UNKNOWN','currentLegalApplicability':'UNKNOWN','officialAdmission':'PENDING'}
   if code in ['1.2','1.8','6.7']:facts['namedLocations']={'1.2':['Bombala','Delegate'],'1.8':['Nimmitabel'],'6.7':['Berridale']}[code]
   if code=='10.5':facts['namedRoads']=['Monaro Hwy','Kosciuszko Road','Delegate Road','Polo Flat Road','Smiths Road','Bobeyan Road','Black Lake Road','Springfield Road','Imlay Road']
   if code=='10.11':facts['namedRoads']=['Ryrie Street','Tinderry road','Burra','Micalago','Tinderry Roads']
   if code=='11.2':facts['namedLocations']=['Berridale','Bombala','Bredbo','Cooma','Michelago']
   if code=='11.3':facts['sensitiveUses']=['hospitals','schools','aged care facilities']
   records.append({'id':PREFIX+'action:'+code,'kind':'Task','category':'ACTION','code':code,'parentId':PREFIX+'priority:'+str(num),'title':f'LSPS{code} — {title}','summary':description,'locator':'; '.join(f'PDF{s["pdfPage"]} / printed{s["pdfPage"]-1}'for s in segs)+f'; implementation action{code}','anchor':anchor(a['pdfPage'],a['bbox']),'facts':facts,'relations':[]})
 for (pn,code),(title,description)in SUPPLEMENTAL.items():
  m=next(m for m in mentions if m['pdfPage']==pn and m['code']==code);num=int(code.split('.')[0]);section='CORE_NARRATIVE_CONFLICT'if pn<56 else'LOCAL_ACTION_CONFLICT'
  records.append({'id':PREFIX+f'narrative-action:p{pn}:{code}','kind':'Task','category':'ACTION','code':code,'parentId':PREFIX+'priority:'+str(num),'title':f'LSPS{code} · PDF{pn} — {title}','summary':description,'locator':f'PDF{pn} / printed{pn-1}; separate {section.lower()} occurrence of{code}','anchor':anchor(pn,m['bbox']),'facts':{'actionCode':code,'actionDescription':description,'priorityNumber':num,'sourceSection':section,'printedTiming':'UNKNOWN_NOT_STATED_IN_THIS_OCCURRENCE','printedWho':'UNKNOWN_NOT_STATED_IN_THIS_OCCURRENCE','who':'UNKNOWN_NOT_STATED_IN_THIS_OCCURRENCE','printedFunded':'UNKNOWN_NOT_STATED_IN_THIS_OCCURRENCE','funded':'UNKNOWN_NOT_STATED_IN_THIS_OCCURRENCE','fundingMeaning':'No timing/funding value copied from a different-intent row with the same code.','relatedPolicyReferences':[],'relatedDocumentCategoryMeaning':'No implementation-table tick set borrowed for this separate occurrence.','evidenceAnchors':[{'role':section,'anchor':anchor(pn,m['bbox']),'occurrenceTextDigest':digest(m['text'])}],'sourceAnomalies':[description],'workState':'HISTORICAL_PUBLISHED_PLAN','actualCouncilAssignment':'NOT_CREATED','actualExecution':'UNKNOWN','actualOutcome':'UNKNOWN','actualSpend':'UNKNOWN','currentBudget':'UNKNOWN','currentLegalApplicability':'UNKNOWN','officialAdmission':'PENDING'},'relations':[]})
 bundle={'format':'csoi-public-knowledge-1','sourceId':SOURCE,'sourceRevision':RAW,'sourcePageCount':118,'rights':'UNKNOWN','currentVersion':'UNKNOWN','officialAdmission':'PENDING','originalBytesCommitted':False,'records':records}
 return bundle,rows,mentions,hashes

def evidence(bundle,rows,mentions,hashes,out):
 out.mkdir(parents=True,exist_ok=True);records=bundle['records'];bycode={r['code']:r for r in records if r['category']=='ACTION'and r['facts']['sourceSection']=='IMPLEMENTATION_TABLE'}
 coverage=[]
 for r in records:
  coverage.append({'recordId':r['id'],'category':r['category'],'code':r['code'],'sourceId':SOURCE,'sourceVersion':'LSPS2020; adoption printed21May2020; currentVersionUNKNOWN','sourceRevision':RAW,'pdfPage':r['anchor']['pdfPage'],'printedPage':r['anchor']['pdfPage']-1,'anchorDigest':r['anchor']['normalizedPageDigest'],'extraction':'STRUCTURED_AUTHORED_RESEARCH','implementation':'PENDING_PARENT_INTEGRATION','verification':'PENDING_INDEPENDENT_ORIGINAL_CHECK','scope':r['facts'].get('sourceSection',r['category']),'gaps':'Current law, actual execution, budget and official admission unverified; source-internal conflicts retained.'})
 occurrences=[]
 for m in mentions:
  separate=(m['pdfPage'],m['code'])in SUPPLEMENTAL;rid=PREFIX+f'narrative-action:p{m["pdfPage"]}:{m["code"]}'if separate else bycode[m['code']]['id']
  occurrences.append({'pdfPage':m['pdfPage'],'printedPage':m['pdfPage']-1,'code':m['code'],'recordId':rid,'disposition':'SEPARATE_CONFLICTING_INTENT'if separate else'RELATED_REPEATED_OCCURRENCE_WITH_EXPLICIT_DIFFERENCES_WHERE_IDENTIFIED','pageDigest':hashes[m['pdfPage']],'bbox':m['bbox'],'occurrenceTextDigest':digest(m['text']),'fullTextRedistributed':False})
 maps={8,16,17,21,28,44,48,57,60,61,65,66,69,72,75,76,88,105,106,107,108,109,110,111,112,113,114,115,116}
 sectionranges=[(1,1,'Cover and adoption'),(2,2,'Acknowledgement'),(3,4,'Contents'),(5,5,'Glossary'),(6,11,'Regional setting and subregions'),(12,17,'Planning framework and historical strategy alignment'),(18,21,'Consultation, growth and vision'),(22,31,'Environment and heritage priorities'),(32,39,'Economic priorities'),(40,45,'Place and housing priorities'),(46,55,'Infrastructure, hazards and growth priorities'),(56,57,'Local planning overview'),(58,61,'Cooma local chapter'),(62,66,'Jindabyne local chapter'),(67,69,'Bombala local chapter'),(70,72,'Berridale local chapter'),(73,75,'Michelago local chapter'),(76,83,'Village chapters'),(84,89,'Rural-land chapter'),(90,104,'Implementation and monitoring table'),(105,116,'Mapping appendix'),(117,118,'Bibliography')]
 inventory=[]
 for p in range(1,119):
  linked=[r['id']for r in records if r['anchor']['pdfPage']==p or any(e['anchor']['pdfPage']==p for e in r['facts'].get('evidenceAnchors',[]))];tablepage=90<=p<=104;hasmentions=any(x['pdfPage']==p for x in mentions)
  inventory.append({'pdfPage':p,'printedPage':p-1,'sourceRevision':RAW,'normalizedPageDigest':hashes[p],'section':next(title for a,b,title in sectionranges if a<=p<=b),'review':'IMPLEMENTATION_ALL_ROWS_COLUMNS_AND_TICKS'if tablepage else'NUMBERED_ACTION_OCCURRENCES_COMPARED'if hasmentions else'PAGE_INVENTORIED_NOT_FULL_SEMANTIC_EXTRACTION','linkedRecordIds':linked,'structuredItems':len(linked),'containsMapOrFigure':p in maps,'gap':'Map geometry/legend and parcel applicability NOT_VERIFIED; non-action prose/figures not fully structured.'if p in maps else'Non-action prose, references and current applicability not fully structured; no whole-document completeness claim.'})
 for name,data in [('coverage-matrix.json',coverage),('narrative-occurrence-matrix.json',occurrences),('page-inventory.json',inventory)]: (out/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 for name,data in [('coverage-matrix.csv',coverage),('narrative-occurrence-matrix.csv',occurrences),('page-inventory.csv',inventory)]:
  with(out/name).open('w',newline='')as f:
   w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows({k:json.dumps(v,ensure_ascii=False)if isinstance(v,(list,dict))else v for k,v in r.items()}for r in data)
 counts={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sourcePages':118,'implementationPages':list(range(90,105)),'implementationActions':len(rows),'implementationUniqueCodes':len({r['code']for r in rows}),'priorities':12,'supplementalConflictRecords':len(SUPPLEMENTAL),'allActionRecords':len([r for r in records if r['category']=='ACTION']),'narrativeLocalOccurrencesCompared':len(mentions),'uniqueCodesAcrossTableAndNarrative':len(set(r['code']for r in rows)|set(m['code']for m in mentions)),'narrativeCodesAbsentFromImplementation':sorted(set(m['code']for m in mentions)-set(r['code']for r in rows)),'totalBundleRecords':len(records),'wholeDocumentKnowledgeCoverage':'PARTIAL','sourceCurrentVersion':'UNKNOWN','currentLegalApplicability':'UNKNOWN','officialAdmission':'PENDING','reconstruction':'NEW_OFFICIAL_SOURCE_RESEARCH_NOT_RECOVERED_UNCOMMITTED_FILES','originalBytesCommitted':False}
 (out/'census-summary.json').write_text(json.dumps(counts,indent=2)+'\n');print(json.dumps(counts,indent=2))
if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('pdf',type=Path);ap.add_argument('--out',type=Path,default=APP/'sources/lsps-public-knowledge.json');ap.add_argument('--evidence',type=Path,default=APP/'qa/strategy-completion/lsps');args=ap.parse_args();bundle,rows,mentions,hashes=make(args.pdf);args.out.write_text(json.dumps(bundle,ensure_ascii=False,indent=2)+'\n');evidence(bundle,rows,mentions,hashes,args.evidence)
