"""Reconstruct bounded CSP public research from the registered original; never infer current duties.
Original PDF/full extracted text are temporary inputs, never an output. Authored summaries
and tabular factual metadata are not a republication of the source's prose.
"""
import argparse,csv,hashlib,json,re
from pathlib import Path
import pdfplumber,pypdf
from pypdf import PdfReader
APP=Path(__file__).resolve().parents[1]
SHA='sha256:dc4fe1fca1d860b3389ea1e5ddca3826efaf5d02a7d029242a45ec20666cf743'
SID='csoi:smrc-csp-full-2025:20261030';PREFIX='csoi:knowledge:csp2035:'
PILLARS=[('community',18,19,'Community health, inclusion and resilience'),('economy',20,21,'Employment, economic resilience and affordability'),('environment',22,23,'Environmental protection with development safeguards'),('infrastructure',24,25,'Infrastructure for services, movement and daily life'),('civic',26,27,'Responsive leadership and accountable planning')]
OBJECTIVES={
1:'Health services and facilities for an enjoyable life',2:'Respect and share cultural identity',3:'Community safety, care and resilience',4:'Work opportunities supported by innovation',5:'More affordable regional living',6:'Protect natural assets and public enjoyment',7:'Land-use controls for environmental and landscape protection',8:'Infrastructure that supports health',9:'Reliable transport within and beyond the region',10:'Digital connectivity where and when needed',11:'Infrastructure that enables local lifestyles',12:'Public confidence in leadership',13:'Informed participation and transparent decisions',14:'Effective strategies for the community vision'}
STRATEGIES={
'1.1':('Accessible care throughout life','Seek quality, accessible aged, disability and health services across different life stages.'),'1.2':('Facilities for healthier lifestyles','Support facilities that enable healthier ways of living.'),
'2.1':('Aboriginal and cultural history','Maintain the region’s Aboriginal and wider cultural heritage.'),'2.2':('Historically important places','Protect significant historic places, including museum settings.'),'2.3':('Cultural exchange and inclusion','Encourage people to share and participate in diverse cultures.'),'2.4':('Support the arts','Assist arts activity across the region.'),'2.5':('Community and cultural events','Support a varied programme of cultural and community events.'),
'3.1':('Inclusive and safe organisations','Encourage organisations to strengthen inclusion, respect and safety.'),'3.2':('Prevent crime proactively','Promote preventive work against crime.'),'3.3':('Volunteers helping people in need','Support volunteering programmes that assist people needing help.'),'3.4':('Opportunities for younger residents','Use jobs, education and social opportunities to help young people settle or remain locally.'),'3.5':('Policing for community safety','Support policing activity that protects community safety.'),
'4.1':('More value from tourism','Improve the economic value of tourism.'),'4.2':('Encourage manufacturing','Identify ways to expand manufacturing activity.'),'4.3':('Resilient local enterprise','Help local businesses and industries remain successful and resilient.'),'4.4':('Education and vocational routes','Support good education choices and vocational pathways.'),
'5.1':('Build on regional economic strengths','Use regional strengths and opportunities to improve economic stability and development.'),'5.2':('Housing diversity through land-use planning','Plan for a range of housing types that responds to demand.'),'5.3':('Higher-value employment','Encourage jobs that add greater economic value.'),
'6.1':('Monitor air, land and waterways','Observe environmental assets so protection needs can be identified; this is not a carbon-calculation rule.'),'6.2':('Prevent and repair environmental damage','Prevent degradation, restore damaged places and manage pressures on vulnerable environments, including invasive species, to preserve biodiversity.'),'6.3':('Shared environmental stewardship','Encourage collective environmental care and sustainable practices.'),
'7.1':('Development that respects nature and heritage','Use land-use plans to guide development sensitive to environmental and heritage values.'),'7.2':('Lower-impact open space and recreation','Plan recreation and open spaces to limit harm and improve environmental sustainability.'),'7.3':('Balanced town, village and rural development','Use planning to sustain local lifestyles while balancing development.'),'7.4':('Retain productive farming and forestry land','Identify important agricultural and forestry land and support its continued productive use.'),
'8.1':('Suitable hospitals and medical centres','Advocate modern, equipped medical facilities that meet community needs.'),'8.2':('Maintain water and wastewater capacity','Maintain water and wastewater infrastructure and its ability to accommodate regional growth.'),'8.3':('Manage community waste effectively','Use facilities, services and programmes to manage waste streams efficiently.'),
'9.1':('Safe and maintained transport assets','Maintain transport infrastructure so travel needs can be met safely.'),'9.2':('Transport services for future demand','Align future transport services with changing regional demand.'),'9.3':('Investment in transport connections','Improve existing transport assets to support sustainable growth and connectivity.'),
'10.1':('Resilient digital connections','Develop digital networks for changing needs and growth, with resilience and security.'),
'11.1':('Accessible public facilities','Make public buildings and facilities usable by all people.'),'11.2':('Identify future infrastructure needs','Plan the infrastructure needed to support communities.'),'11.3':('Connected trails and shared paths','Develop regional trails and accessible shared pathways.'),'11.4':('Maintain sport and leisure facilities','Keep sporting and leisure facilities in good condition.'),
'12.1':('Visible and accessible leadership','Make leadership visible and accessible to the community.'),'12.2':('Agreed standards for public services','Establish and apply agreed public-service standards.'),'12.3':('Govern resources and systems well','Manage Council resources, systems and processes with sound governance.'),
'13.1':('Effective stakeholder engagement','Use engagement strategies to consult stakeholders effectively.'),'13.2':('Multiple ways to contribute','Offer different consultation mechanisms so stakeholders can provide input.'),'13.3':('Relevant and timely communication','Communicate relevant information about matters affecting stakeholders in time to be useful.'),
'14.1':('Keep major-issue strategies current','Maintain up-to-date strategies for major community issues.')}
COLS={29:[56.693,235.35,409.606,460.63,537.165],30:[57.443,244.779,411.079,462.103,538.637],31:[56.443,243.78,410.079,461.103,537.637]}
GROUPS=[(29,'community',168.662,767.74),(30,'economy',158.56,447.70),(30,'environment',481.709,714.20),(31,'infrastructure',158.56,476.04),(31,'civic',512.89,702.82)]
SHORT_NAMES={
'community':['Personal wellbeing','Community wellbeing','Belonging','Weekly median household income','Socioeconomic disadvantage','Equity and inclusion','Childhood developmental vulnerability','Life expectancy','Long-term health conditions','Mental health conditions','Organised volunteering','Psychological distress','Crime and safety','Mortgage burden','Rental burden','General healthcare access','Specialist healthcare access','Mental healthcare access','Community spirit','Health, education and childcare access','Community-event participation','Public transport access: community table','Drinking-water guideline compliance','Major-offence rate'],
'economy':['Regional product share','GST-registered businesses','Tourism sales share','Certificate III or higher qualification','No non-school qualification','Local school quality','Unemployment','Employment relative to regional NSW','Household savings relative to regional NSW','Agricultural production value','Visitor expenditure'],
'environment':['Landscape and aesthetics','Perceived environmental health','Per-person greenhouse emissions','DA lodgement time','DA assessment time','Development/community-value balance','Waste diverted from landfill','Age of land-use strategies'],
'infrastructure':['Road length per resident','Local road quality','Public transport access: infrastructure table','Water and sewer main breaks','Water and sewer greenhouse emissions','Recycling rate','Telecommunications access','Public halls','Public libraries','Public open space','Public swimming pools','Infrastructure repair-cost estimate'],
'civic':['Operating performance ratio','Residential rates','Residential water/sewer bill','Infrastructure backlog ratio','Community leadership and collaboration','Voice and participation','Leadership satisfaction','Strategies kept current']}
def norm(s):return ' '.join(s.split())
def digest(s):return 'sha256:'+hashlib.sha256(s.encode()).hexdigest()
def crop(words,bbox):
 x0,y0,x1,y1=bbox
 return norm(' '.join(w['text']for w in words if x0<=w['x0']<x1 and y0<=w['top']<y1))
def build(pdfpath):
 assert 'sha256:'+hashlib.sha256(pdfpath.read_bytes()).hexdigest()==SHA,'ORIGINAL_BYTE_MISMATCH'
 reader=PdfReader(pdfpath);assert len(reader.pages)==36
 texts={n:norm(reader.pages[n-1].extract_text(extraction_mode='layout')or'')for n in range(1,37)}
 parser='pypdf-'+pypdf.__version__+'-layout-whitespace-1'
 def anch(n,bbox):return {'pdfPage':n,'normalizedPageDigest':digest(texts[n]),'parserVersion':parser,'bbox':[round(x,3)for x in bbox]}
 records=[];rows=[]
 def add(category,code,parent,title,summary,page,bbox,facts):
  kind={'CSP_DOCUMENT':'DocumentRevision','CSP_PILLAR':'StrategicOutcome','CSP_OBJECTIVE':'Objective','CSP_STRATEGY':'ContentBlock','CSP_INDICATOR':'QuantifiedObservation'}[category]
  tail={'CSP_DOCUMENT':'document','CSP_PILLAR':'pillar:'+code,'CSP_OBJECTIVE':'objective:'+code,'CSP_STRATEGY':'strategy:'+code,'CSP_INDICATOR':'indicator:'+code.removeprefix('CSP-KPI-')}[category]
  n={'id':PREFIX+tail,'kind':kind,'category':category,'code':code,'parentId':parent,'title':title,'summary':summary,'locator':f'CSP 2035 2025 revision; PDF/printed page {page}; '+('published measure row '+code if category=='CSP_INDICATOR'else category.replace('CSP_','').lower()+' '+code),'anchor':anch(page,bbox),'facts':facts,'relations':[]};records.append(n);return n
 def boundary(pillar=None):return {'actualOutcome':'UNKNOWN','councilRoles':'NOT_ASSIGNED_AT_THIS_LEVEL','partners':'SEE_SOURCE_STRATEGY_ROWS','responsibleRole':'UNKNOWN_LOCAL_ASSIGNMENT','timeframe':'2035 plan horizon; no item execution dates established',**({'pillar':pillar}if pillar else{})}
 add('CSP_DOCUMENT','CSP2035',None,'CSP 2035: 2025 published revision','Community-wide strategic direction, supporting partners and published baseline measures. It is not a record of completed Council work.',1,[0,0,595.276,841.89],{**boundary(),'planningHorizon':'2035; introductory page 3 also says next 18 years, an unreconciled source wording conflict','versionLabel':'Cover: 2025 Revision; version table PDF35: v3.0, 1 May 2025, resolution73/25; current controlled version UNKNOWN','totalPages':36})
 with pdfplumber.open(pdfpath)as pdf:
  for pillar,start,last,title in PILLARS:
   q=pdf.pages[last-1];words=q.extract_words();begin=next(w['top']for w in words if w['text']=='Supporting');lines=q.crop((50,begin+12,550,790)).extract_text().splitlines();support=[]
   for line in lines:
    line=norm(line)
    if line and not line.startswith('Supporting documents')and not re.fullmatch(r'\d+',line):support.append({'title':line,'pdfPage':last,'normalizedPageDigest':digest(texts[last]),'relationship':'SOURCE_LISTED_SUPPORTING_DOCUMENT','version':'UNKNOWN','implementation':'UNKNOWN'})
   add('CSP_PILLAR',pillar,PREFIX+'document',title,{'community':'Support health and wellbeing through suitable services, including aged care.','economy':'Sustain a varied economy spanning agriculture, energy, timber, services and tourism, with growth and innovation.','environment':'Protect and improve natural and heritage values while balancing regional development needs.','infrastructure':'Improve roads and regional services so infrastructure supports diverse communities, the economy and daily life.','civic':'Seek transparent, open leadership that responds to the local community.'}[pillar],start,[50,85,550,270],{**boundary(pillar),'supportingDocuments':support})
  seenobjectives=set()
  for page in [18,19,21,22,23,24,25,26,27]:
   q=pdf.pages[page-1];words=q.extract_words();codes=[w for w in words if re.fullmatch(r'\d{1,2}\.\d',w['text'])and 170<w['x0']<220]
   end=next((w['top']for w in words if w['text']=='Supporting'and w['top']>codes[-1]['top']),790)-4
   role_x=min(w['x0']for w in words if w['text']in ['Provide','Collaborate','Advocate']and w['x0']>300 and w['top']>codes[0]['top']-2)
   head=next(w for w in words if w['text']=='Council’s');partner_x=next(w['x0']for w in words if w['text']=='Our'and abs(w['top']-head['top'])<2)-6
   for i,codeword in enumerate(codes):
    code=codeword['text'];number=int(code.split('.')[0]);pillar='community'if number<=3 else'economy'if number<=5 else'environment'if number<=7 else'infrastructure'if number<=11 else'civic'
    top=codeword['top']-2;bottom=codes[i+1]['top']-2 if i+1<len(codes)else end
    if number not in seenobjectives:
     nextobjective=next((w['top']-2 for w in codes[i+1:]if int(w['text'].split('.')[0])!=number),end)
     add('CSP_OBJECTIVE',str(number),PREFIX+'pillar:'+pillar,f'{number} · {OBJECTIVES[number]}','Published strategic objective concerning '+OBJECTIVES[number].lower()+'. Individual strategy roles and partners are recorded below.',page,[50,top,codeword['x0']-3,nextobjective],{**boundary(pillar),'printedCode':str(number)})
     seenobjectives.add(number)
    roles=crop(words,[role_x-2,top,partner_x,bottom]).split();assert all(r in ['Provide','Collaborate','Advocate']for r in roles),(code,roles)
    partners=crop(words,[partner_x,top,550,bottom]);assert partners
    title,summary=STRATEGIES[code]
    n=add('CSP_STRATEGY',code,PREFIX+'objective:'+str(number),code+' · '+title,summary,page,[codeword['x0']-2,top,550,bottom],{**boundary(pillar),'printedCode':code,'councilRoles':roles,'partners':{'printedColumnText':partners,'meaning':'Listed collaborators in this historical source; not current assignments','columnBounds':[round(x,3)for x in [partner_x,top,550,bottom]]}})
  actualstrategies={n['code']for n in records if n['category']=='CSP_STRATEGY'};assert actualstrategies==set(STRATEGIES)and len(seenobjectives)==14
  for page,pillar,start,end in GROUPS:
   q=pdf.pages[page-1];words=q.extract_words();columns=COLS[page]
   horizontal=sorted({round(e['top'],3)for e in q.edges if e['orientation']=='h' and 450<e['x0']<470 and e['x1']>530 and start+0.5<e['top']<end-0.5})
   bounds=[start]+horizontal+[end];assert len(bounds)-1==len(SHORT_NAMES[pillar]),(pillar,bounds)
   for row,(top,bottom)in enumerate(zip(bounds,bounds[1:]),1):
    cells=[crop(words,[columns[i],top,columns[i+1],bottom])for i in range(4)];label,source,baseline,trend=cells;assert all(cells),(pillar,row,cells)
    code=f'CSP-KPI-{page}-{pillar}-{row:02d}';num=re.search(r'-?\d[\d,]*(?:\.\d+)?',baseline);assert num;value=float(num.group().replace(',',''));value=int(value)if value.is_integer()else value;scale=1000000 if re.search(r'\dM\b',baseline)else 1
    unit='UNKNOWN';printedunit=re.sub(r'^\s*[-$]?\d[\d,]*(?:\.\d+)?\s*','',baseline).strip();currency='UNKNOWN'
    if '%'in baseline:unit='%'
    elif baseline.startswith('$'):unit='$';currency='UNKNOWN_DOLLAR_CURRENCY_NOT_STATED_IN_ROW';printedunit='$'+('M'if scale==1000000 else'')
    elif 'tonnes'in baseline:unit='tonnes CO2e/person';printedunit='tonnes'
    elif 'years'in baseline:unit='years'
    elif 'days'in baseline:unit='days'
    elif ' ha'in baseline:unit='ha'
    elif re.search(r'\dm$',baseline):unit='m/person'
    elif '100kms'in baseline:unit='breaks/100 km of main'
    elif re.search(r'Number of |Total GST registered',label):unit='count'
    yearmatches=re.findall(r'20\d\d(?:[-–]\d{2,4})?',source);sourceyear=yearmatches[-1]if yearmatches else'UNKNOWN'
    measureyears=re.findall(r'20\d\d(?:[-–]\d{2,4})?',label);measureyear=measureyears[-1]if measureyears else'UNKNOWN_NOT_STATED_IN_MEASURE_LABEL'
    definition=SHORT_NAMES[pillar][row-1];denom='NOT_STATED_IN_ROW'
    if '%'in baseline or 'percentage'in label.lower():denom='Population or total named in the measure; matched raw denominator not ingested'
    if 'capita'in label:denom='Corresponding source population; matching year/boundary not independently established'
    if '100'in label:denom='Source-specific 100-unit normalisation, not a raw observed denominator'
    if 'Index'in label or 'Ratio'in label:denom='Index/ratio construction and reference series not ingested'
    expression='UNKNOWN_FROM_PUBLISHED_TABLE';formulaBasis='Source publishes a baseline, not the complete calculation specification'
    inputs=['Underlying source observations','Same-period and same-boundary denominator or method','Source methodology and revision','Units and measurement precision']
    boundaries={'geographic':'Snowy Monaro regional context; exact underlying geography not independently reconciled','organisation':'UNKNOWN_NOT_A_COUNCIL_PERFORMANCE_RESULT','accounting':'Underlying inventory/method not ingested'}
    if pillar=='environment'and row==3:
     expression='same-boundary emissions / corresponding population';formulaBasis='Conceptual per-person identity, not an independently reproduced CSP result';inputs=['Raw regional emissions total for2021–22','Corresponding population, boundary and year','Inventory sectors, scopes and methodology','Unrounded values and GWP basis'];boundaries['organisation']='Regional/community context; not a Council operations inventory'
    if pillar=='infrastructure'and row==5:
     inputs=['Underlying NSW Water2022–23 inventory','Full unit, gas/scopes and GWP convention','Operational activity and emission factors','Matched organisation and accounting boundary'];boundaries['organisation']='Water and sewer aggregate named by table; precise operational boundary unverified'
    conflicts=[]
    if (pillar,row)in [('community',22),('infrastructure',3)]:conflicts=['CSP-KPI-29-community-22','CSP-KPI-31-infrastructure-03']
    facts={'actualValue':'UNKNOWN','baseline':{'value':value,'scale':scale,'normalisedValue':value*scale,'normalisation':'M suffix denotes million; otherwise scale1; printed value retained','unit':unit,'printedUnit':printedunit or'NOT_STATED','unitStatus':'UNKNOWN_FULL_UNIT'if unit=='UNKNOWN'else'OBSERVED_OR_NAMED_IN_MEASURE','role':'PUBLISHED_BASELINE_NOT_CURRENT_ACTUAL','currency':currency},'boundaries':boundaries,'computability':'NOT_COMPUTABLE','definition':definition+'; published baseline observation, not verified current performance.','denominator':{'label':denom,'value':'UNKNOWN','normalisationReference':'Named measure only; no matched raw denominator supplied','status':'NOT_INDEPENDENTLY_VALIDATED'},'desiredTrend':trend,'formula':{'expression':expression,'basis':formulaBasis,'requiredInputs':inputs},'humanReview':'PENDING','measurementYearLabel':measureyear,'officialRelationship':'UNKNOWN_NOT_ADMITTED','originalCensusId':code,'originalColumnBounds':{key:[round(x,3)for x in [columns[i],top,columns[i+1],bottom]]for i,key in enumerate(['measure','source','baseline','trend'])},'pillar':pillar,'printedBaseline':baseline,'printedDesiredTrend':trend,'printedLabel':label,'printedSource':source,'quantityRole':'PUBLISHED_BASELINE_NOT_CURRENT_ACTUAL','referencePeriod':{'label':measureyear if measureyears else sourceyear,'basis':'Printed measure year if stated, otherwise source label; precise period not inferred'},'responsibleRole':'UNKNOWN','sourceConflictIds':conflicts,'sourceYear':sourceyear,'tableRow':row,'timeInterval':{'from':'UNKNOWN','to':'UNKNOWN','basis':'Printed year label retained; exact start/end dates not independently confirmed'},'timeframe':'Historical published baseline; not a current measurement'}
    summary=f'Published {definition.lower()} baseline: {baseline}; source label {source}; desired trend {trend}. Raw inputs and current performance are unverified.'
    add('CSP_INDICATOR',code,PREFIX+'pillar:'+pillar,definition,summary,page,[columns[0],top,columns[-1],bottom],facts)
 return {'format':'csoi-public-knowledge-1','sourceId':SID,'sourceRevision':SHA,'sourcePageCount':36,'rights':'UNKNOWN','currentVersion':'UNKNOWN','officialAdmission':'PENDING','originalBytesCommitted':False,'records':records},texts

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('pdf',type=Path);p.add_argument('--out',type=Path,default=APP/'sources/csp-public-knowledge.json');a=p.parse_args();bundle,_=build(a.pdf);a.out.write_text(json.dumps(bundle,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'records':len(bundle['records']),'categories':{k:sum(n['category']==k for n in bundle['records'])for k in sorted({n['category']for n in bundle['records']})}}))
if __name__=='__main__':main()
