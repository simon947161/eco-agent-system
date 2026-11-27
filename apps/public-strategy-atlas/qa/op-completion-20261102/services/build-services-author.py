#!/usr/bin/env python3
"""Reproduce bounded public OP author records from pinned original + authored readings.
Raw PDF/native original text/crops remain outside the repository. No network access.
"""
import argparse,collections,csv,hashlib,importlib.util,json,re,sys,unicodedata
from pathlib import Path
import fitz
HERE=Path(__file__).resolve().parent
APP=HERE.parents[2]
PDF_SHA='4e0b6440768c6bb902628ec36e43757366be470f583169834a4c7c3d4cf54fd2'
SOURCE='csoi:smrc-op-2026:20261030'
PARSER='pymupdf-1.26.6-text-nfkc-whitespace-v1'
RENDERER='pymupdf-1.26.6-rgb-100dpi-fresh-document-clip-v2'
PHOTO_PAGES={12,15,34,43,54,63,79,97,106}
def norm(t):return re.sub(r'\s+',' ',unicodedata.normalize('NFKC',t or '')).strip()
def digest(x):return 'sha256:'+hashlib.sha256(x if isinstance(x,bytes) else x.encode()).hexdigest()
def union(boxes):
 boxes=[b for b in boxes if b]
 return [min(b[0] for b in boxes),min(b[1] for b in boxes),max(b[2] for b in boxes),max(b[3] for b in boxes)]
def state(s):return 'MERGED_FROM_PRINTED_CELL' if s is None else 'BLANK' if not norm(s) else 'NOT_STATED_DASH' if norm(s)=='-' else 'NO_MEASURE' if norm(s).lower()=='no measure' else 'PRINTED_NIL' if norm(s).lower()=='nil' else 'PRINTED'
def dump(name,x):(HERE/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def extract_original(doc):
 """Read the pinned original directly; no unverified temporary extraction inputs."""
 pages=[];rows=[]
 for page_index in range(106):
  p=doc[page_index];pn=page_index+1
  out={'pdfPage':pn,'rect':list(p.rect),'text':p.get_text('text'),'blocks':[{'blockIndex':b[5],'bbox':list(b[:4]),'text':b[4]} for b in p.get_text('blocks') if b[6]==0 and b[4].strip()],'tables':[]}
  for ti,t in enumerate(p.find_tables().tables):
   tid=f'p{pn:03d}-t{ti:02d}';vals=t.extract();cells=[list(r.cells) for r in t.rows]
   out['tables'].append({'id':tid,'bbox':list(t.bbox),'rows':vals,'cells':cells,'rowCount':t.row_count,'columnCount':t.col_count})
   if pn!=11 and pn<13:continue
   header=vals[0] if vals else [];first=norm(header[0]) if header else ''
   typ='SERVICE' if first=='Action/Program Description' else 'PROJECT' if first=='Major Project/Infrastructure Delivery' else 'IMPROVEMENT' if first=='Action' and len(header)==2 else None
   if typ:
    for ri in range(1,len(vals)):rows.append({'id':f'{tid}-r{ri:02d}','pdfPage':pn,'type':typ,'headers':header,'cells':vals[ri],'bboxes':cells[ri]})
  pages.append(out)
 return pages,rows
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--pdf',default='/tmp/csoi-strategy-completion-20261101/op.pdf');args=ap.parse_args()
 pdf=Path(args.pdf);assert len(pdf.read_bytes())==37500187 and hashlib.sha256(pdf.read_bytes()).hexdigest()==PDF_SHA
 assert fitz.VersionBind=='1.26.6'
 doc=fitz.open(pdf);assert len(doc)==142
 sys.dont_write_bytecode=True
 spec=importlib.util.spec_from_file_location('context_author',HERE/'context-author.py');a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
 original,rows=extract_original(doc);page_by={p['pdfPage']:p for p in original}
 readings={r[0]:r[1:] for r in csv.reader((HERE/'row-readings.tsv').open(),delimiter='\t')};assert len(readings)==517
 assert set(readings)=={r['id'] for r in rows if r['pdfPage']>=13}
 readings.update(a.EXAMPLES)
 anchor_cache={}
 def anchor(p,bb,field):
  bb=list(bb);key=(p,tuple(bb));
  if key not in anchor_cache:anchor_cache[key]=digest(norm(doc[p-1].get_text('text',clip=fitz.Rect(bb))))
  return {'field':field,'pdfPage':p,'bbox':bb,'normalizedTextDigest':anchor_cache[key],'parserVersion':PARSER}
 def raster(p,bb,field='visual'):
  with fitz.open(pdf) as fresh:
   pix=fresh[p-1].get_pixmap(matrix=fitz.Matrix(100/72,100/72),clip=fitz.Rect(bb),colorspace=fitz.csRGB,alpha=False)
   dg=digest(f'RGB|{pix.width}x{pix.height}|'.encode()+pix.samples)
  return {'field':field,'pdfPage':p,'bbox':list(bb),'rasterDigest':dg,'renderer':RENDERER,'width':pix.width,'height':pix.height}
 boundaries={'currentVersion':'UNKNOWN','currentLegalApplicability':'UNKNOWN','actualOutput':'UNKNOWN','actualExecution':'UNKNOWN','actualSpend':'UNKNOWN','actualOutcome':'UNKNOWN','activityResourceAllocation':'UNKNOWN','officialAdmission':'PENDING','councilAssignmentCreated':False}
 csp=json.loads((APP/'sources/csp-public-knowledge.json').read_text())
 known={r['id'].rsplit(':',1)[-1]:r['id'] for r in csp['records'] if ':strategy:' in r['id']}
 def refs(value,an,row_id):
  result=[]
  for code in re.findall(r'(?<![\d.])\d{1,2}\.\d{1,2}(?![\d.])',norm(value)):
   result.append({'occurrenceId':row_id+':csp:'+code,'code':code,'pdfPage':an['pdfPage'],'physicalRowId':row_id,'field':'csp','sourceAnchor':an,'relationship':'PRINTED_SOURCE_REFERENCE_ONLY','targetId':known.get(code),'resolution':'RESOLVED_EXISTING_STRATEGY' if code in known else 'UNRESOLVED_PRINTED_CODE'})
  return result
 units=[];physical=[];all_refs={};resolved_by={};group=None;previous_table=None
 programme_starts={p[0]:p[1] for p in a.PROGRAMMES}
 def programme(p):return programme_starts[max(n for n in programme_starts if n<=p)] if p>=13 else 'Reading guide and example' if p==11 else 'Document front matter'
 legacy={'p073-t00-r01':'asset-maintenance','p073-t00-r02':'potable-water','p074-t00-r01':'daily-testing','p074-t01-r01':'service-requests','p074-t02-r01':'water-incidents','p074-t02-r03':'reactive-repairs','p074-t02-r04':'quality-complaints','p074-t03-r01':'sewer-maintenance'}
 section_by_table={};current_section='UNKNOWN'
 for p in original:
  events=[(t['bbox'][1],'table',t) for t in p['tables']]
  events += [(b['bbox'][1],'heading',norm(b['text'])) for b in p['blocks'] if re.match(r'^(Planned|Reactive|Major Project/Infrastructure Delivery|Actions)$|^(Planned|Reactive|Major Project/Infrastructure Delivery)\s+[–-]',norm(b['text']))]
  for _,kind,item in sorted(events,key=lambda e:e[0]):
   if kind=='heading':current_section=item
   else:section_by_table[item['id']]=current_section
 def new_unit(r,title):
  return {'id':'csoi:op-full:'+r['id'],'pdfPage':r['pdfPage'],'pages':[],'category':'GUIDE_EXAMPLE' if r['pdfPage']==11 else {'SERVICE':'SERVICE_ACTION','PROJECT':'PROJECT','IMPROVEMENT':'IMPROVEMENT_ACTION'}[r['type']],'section':programme(r['pdfPage']),'title':title,'summary':'','bbox':None,'sourceSegments':[],'sourceAnchors':[],'facts':{'sourceTableType':r['type'],'rows':[],'interpretation':dict(boundaries)},'conditions':[],'qualifiers':[],'cspReferences':[],'lspsReferences':[],'existingRecordIds':[],'physicalRowIds':[]}
 for r in rows:
  rid=r['id'];p=r['pdfPage'];table=rid.rsplit('-r',1)[0]
  fields=['action','kpi','regulatory','target','reportingFrequency','csp','otherPlans'] if r['type']=='SERVICE' and len(r['cells'])==7 else ['action','optimalVolume','fundedVolume','kpi','regulatory','target','reportingFrequency','csp','otherPlans'] if r['type']=='SERVICE' else ['projectTitle','description','annualBudget','resources','csp','otherPlans','start','end'] if r['type']=='PROJECT' else ['action','target']
  authored=readings[rid];assert len(authored)==3
  if table!=previous_table:resolved_by={}
  if r['cells'][0] is not None:
   if rid=='p030-t00-r01':
    group=next(x for x in units if x['id']=='csoi:op-full:p029-t00-r08');group['qualifiers'].append('原文cont.明确延续PDF29的环境投诉动作，合并逻辑动作但保留PDF29/30所有独立及相互不同的KPI子行。')
   else:group=new_unit(r,authored[0]);units.append(group)
  assert group is not None and (r['cells'][0] is not None or table==previous_table)
  row={'id':rid,'pdfPage':p,'tableId':table,'printedSection':section_by_table[table],'summary':authored[1],'conditions':[] if authored[2]=='-' else [authored[2]],'fields':{},'sourceAnchors':[]}
  for idx,field in enumerate(fields):
   val=r['cells'][idx];bb=r['bboxes'][idx];st=state(val)
   if bb is not None:
    an=anchor(p,bb,field);owner=rid;resolved_by[field]={'value':norm(val),'anchor':an,'owner':owner}
    row['sourceAnchors'].append(an);group['sourceAnchors'].append(an)
   else:
    assert field in resolved_by,(rid,field)
    an=resolved_by[field]['anchor'];owner=resolved_by[field]['owner']
   resolved=resolved_by[field];entry={'sourceState':st,'sourceCellOwnerRow':owner,'sourceAnchor':an}
   if field in ['action','projectTitle','description','kpi']:
    entry['summary']=authored[1] if field in ['description','kpi'] else group['title']
    entry['nativeTextRedistributed']=False
    if norm(resolved['value']).lower()=='no measure':entry['publishedLabel']='No measure'
   else:entry['publishedValue']=resolved['value']
   if field in ['annualBudget']:entry.update({'currency':'UNKNOWN','actualSpend':'UNKNOWN','period':'AS_PRINTED_NOT_AUTOMATIC_ANNUAL_TOTAL','summationAllowed':False})
   if field in ['target','optimalVolume','fundedVolume']:entry['actualOutput']='UNKNOWN'
   if field=='reportingFrequency':entry['legalOperationalFrequency']='UNKNOWN'
   if field=='regulatory':entry['currentLegalApplicability']='UNKNOWN'
   row['fields'][field]=entry
   if field=='csp':
    found=refs(resolved['value'],an,owner)
    for ref in found:
     all_refs[ref['occurrenceId']]=ref
     if ref['occurrenceId'] not in {z['occurrenceId'] for z in group['cspReferences']}:group['cspReferences'].append(ref)
   if field in ['action','description','otherPlans'] and ('LSPS' in resolved['value'] or 'Local Strategic Planning Statement' in resolved['value']):
    ref={'occurrenceId':owner+':'+field+':lsps','pdfPage':p,'physicalRowId':owner,'field':field,'documentLabel':'Local Strategic Planning Statement','sourceAnchor':an,'relationship':'NAMED_DOCUMENT_REFERENCE_ONLY','priorityOrActionMapping':'UNKNOWN','version':'2020' if re.search(r'LSPS\s*2020',resolved['value']) else 'UNKNOWN'}
    if ref['occurrenceId'] not in {z['occurrenceId'] for z in group['lspsReferences']}:group['lspsReferences'].append(ref)
  if rid=='p039-t02-r04':
   row['sourceAnomalies']=['原文提取层混入不可见Corporate Projects星号脚注；可见像素正文为房车公园策略范围及替代管理运营模式。摘要按可见内容写，native digest保留原位异常。'];row['visualAnchor']=raster(p,union(r['bboxes']),'visibleActionWithOccludedFooter')
  group['facts']['rows'].append(row);group['physicalRowIds'].append(rid)
  if p not in group['pages']:group['pages'].append(p)
  group['conditions']+=row['conditions']
  if rid in legacy:group['existingRecordIds']=['csoi:knowledge:op2026:water:activity:'+legacy[rid]];group['qualifiers'].append('复用既有水务Activity；此处为完整原表上下文，不新增第二个语义行动。')
  physical.append({'physicalRowId':rid,'pdfPage':p,'tableId':table,'sourceTableType':r['type'],'logicalUnitId':group['id'],'formal':p>=13,'mergedFirstColumn':r['cells'][0] is None,'crossPageContinuation':rid=='p030-t00-r01','sourceAnchorCount':len(row['sourceAnchors']),'existingRecordIds':group['existingRecordIds']})
  previous_table=table
 for u in units:
  u['summary']='；'.join(dict.fromkeys(r['summary'] for r in u['facts']['rows']))
  u['conditions']=list(dict.fromkeys(u['conditions']))
  for p in u['pages']:
   rs=[r for r in u['facts']['rows'] if r['pdfPage']==p];bb=union(a['bbox'] for r in rs for a in r['sourceAnchors'])
   u['sourceSegments'].append({'pdfPage':p,'physicalRowIds':[r['id'] for r in rs],'bbox':bb})
  u['bbox']=u['sourceSegments'][0]['bbox']
  if u['category']=='GUIDE_EXAMPLE':u['qualifiers'].append('教学示例，排除正式行动、项目、FTE与预算分母；对应后文Open Space正式服务。')
  u['facts']['logicalGrouping']='FIRST_PRINTED_ACTION_OR_PROJECT_CELL_WITH_MERGED_SUBROWS; EXPLICIT_CONTINUATION_ONLY'
  u['facts']['physicalRowCount']=len(u['physicalRowIds'])
  u['facts']['newNativeActivity']=False
 def context(p,category,title,summary,anchors=None):
  bb=list(doc[p-1].rect);an=anchors or [anchor(p,bb,'pageContext')]
  u={'id':f'csoi:op-full:p{p:03d}:{category.lower()}','pdfPage':p,'pages':[p],'category':category,'section':programme(p),'title':title,'summary':summary,'bbox':union(x['bbox'] for x in an),'sourceSegments':[{'pdfPage':p,'bbox':union(x['bbox'] for x in an),'physicalRowIds':[]}],'sourceAnchors':an,'facts':{'interpretation':dict(boundaries)},'conditions':[],'qualifiers':[],'cspReferences':[],'lspsReferences':[],'existingRecordIds':[],'physicalRowIds':[]};units.append(u);return u
 for p,(title,summary) in a.FRONT.items():
  u=context(p,'FRONT_MATTER',title,summary)
  if p in [8,9,10,11]:u['facts']['visualAnchor']=raster(p,list(doc[p-1].rect),'visibleLayout')
  if p==3:
   u['existingRecordIds']=['csoi:knowledge:op2026:water:document'];u['facts'].update({'registeredFilenameVersion':'v3.1','bodyLatestPopulatedVersion':'1.3','workingDraftDisclaimerPresent':True,'blankVersionLabels':['1.4','1.5','1.6'],'versionRows':[{'version':'1.0','date':'31/03/2026','reason':'公开展示草稿','resolution':'-','ownerRole':'Corporate Reporting Officer'},{'version':'1.1','date':'17/04/2026','reason':'提请Council公开展示的草稿','resolution':'88/26','ownerRole':'Corporate Reporting Officer'},{'version':'1.2','date':'04/5/2026','reason':'Cooma及Bombala泳池项目资助金额修订','resolution':'143/26','ownerRole':'Coordinator Strategy Development'},{'version':'1.3','date':'30/06/2026','reason':'表中称Council采用','resolution':'225/26','ownerRole':'Coordinator Strategy Development'}],'printedCopyControl':'UNCONTROLLED_WHEN_PRINTED; INTRANET_CONTROLLED_COPY_NOT_ACCESSED'})
  if p in [4,5]:
   entries=[]
   for b in page_by[p]['blocks']:
    m=re.match(r'(.+?)\x08\s*(\d+)$',b['text'].strip(),re.S)
    if m:entries.append({'label':norm(m[1]),'printedPage':int(m[2]),'sourceAnchor':anchor(p,b['bbox'],'contentsEntry')})
   u['facts']['contentsEntries']=entries
  if p==6:u['facts'].update({'forewordPlannedAmounts':[{'label':'gravel resheeting','publishedValue':'$5.4 million'},{'label':'road resealing','publishedValue':'$2.7 million'},{'label':'water and sewer infrastructure','publishedValue':'$9.25 million'}],'publishedHistoricalAssetQuantities':[{'label':'roads','value':'2,629 kilometres'},{'label':'mains','value':'574 kilometres'},{'label':'pump stations','value':'42'},{'label':'reservoirs','value':'34'},{'label':'treatment plants','value':'12'}],'rateDenominatorAdmission':'UNKNOWN','currency':'UNKNOWN','sumWithCapitalTables':False})
  if p==7:u['facts'].update({'forewordPlannedAmounts':[{'label':'open space and recreation renewal','publishedValue':'$1 million'}],'currency':'UNKNOWN','sumWithCapitalTables':False})
  if p==8:
   u['facts'].update({'opPeriod':'2026/27','deliveryProgramPeriod':'2025-2029','themes':['Our Community','Our Economy','Our Environment','Our Infrastructure','Our Civic Leadership'],'reportingStatements':[{'scope':'DP progress update legislative statement in this source','publishedCadence':'every six months','currentLegalApplicability':'UNKNOWN'},{'scope':'Council commitment aligned with quarterly budget reviews','publishedCadence':'quarterly'}],'diagramNodes':['State Plans and Strategies','Relevant Regional Plans and Priorities','JO Statement of Strategic Regional Priorities','Community Strategic Plan','Other Council Strategies and Plans','Resourcing Strategy','Workforce Management Strategy','Long-Term Financial Plan','Asset Management Strategy and Plans','Delivery Program','Operational Plan','Annual Report','State of Region Report','Community Engagement Strategy / Community Participation Plan'],'diagramMeaning':'IP&R规划文件与持续监测复审的概念联系；不是已准入的执行、因果或法律关系。'})
   u['lspsReferences']=[{'occurrenceId':'p008:diagram:lsps','pdfPage':8,'field':'diagram','documentLabel':'Local Strategic Planning Statement','sourceAnchor':anchor(8,list(doc[7].rect),'diagramContext'),'relationship':'NAMED_DOCUMENT_REFERENCE_ONLY','priorityOrActionMapping':'UNKNOWN','version':'UNKNOWN'}]
  if p==9:
   codes=re.findall(r'(?m)^\s*(\d{1,2}\.\d{1,2})\s',page_by[9]['text']);assert len(codes)==44
   u['cspReferences']=refs(' '.join(codes),anchor(9,list(doc[8].rect),'cspOverviewCodes'),'p009:overview')
   for ref in u['cspReferences']:ref['referenceScope']='CSP_OVERVIEW_DUPLICATE_EXISTING_STRATEGIES'
   u['facts'].update({'themeCount':5,'objectiveCount':14,'strategyCodeCount':44,'printedStrategyCodes':codes,'duplicatesExistingCspContent':True,'reportingStatements':[{'scope':'projects and activities in CSP overview graphic','publishedCadence':'each month to Council'},{'scope':'Annual Report','publishedCadence':'annually'},{'scope':'State of Region Report','publishedCadence':'end of Council term'}]})
   u['qualifiers'].append('44代码仅为CSP总览复述；不计为正式服务行的CSP引用次数，亦不增加44个新策略。')
  if p==10:u['facts'].update({'chartDate':'2026-03-23','visibleOfficeholders':[{'role':'Chief Executive Officer','name':'Noreen Vu'},{'role':'Chief of Community Services','name':'Tony Murray'},{'role':'Chief Financial Officer','name':'Simon Rennie'},{'role':'Chief of Infrastructure and Projects','name':'Tony Lickiss'},{'role':'Chief Strategy Officer','name':'David Rawlings'},{'role':'Chief People and Organisational Performance Officer','name':'Angela Sommerville'}],'currentOfficeholders':'UNKNOWN','hiddenExtractionConflict':{'role':'Chief of Infrastructure and Projects','nativeTextOnlyName':'John Gargett','visibleName':'Tony Lickiss','disposition':'HIDDEN_OR_OCCLUDED_TEXT_NOT_CURRENT_OFFICEHOLDER'},'visibleTeams':{'CEO':['Executive Office'],'Community Services':['Built and Natural Environment','Open Space and Recreation','Communications and Engagement','Community Services Support Programs','Libraries','Resource and Waste','Tourism'],'Finance':['Finance','Procurement and Contractors','Revenue'],'Infrastructure and Projects':['Infrastructure','Project Management','Water and Wastewater'],'Strategy':['Fleet and Plant','Governance','ICT','Strategic Development'],'People and Organisational Performance':['Learning and Development','Work Health and Safety','Workforce','Quality Service and Performance']}})
  if p==11:u['facts'].update({'examplePhysicalRows':6,'exampleLogicalGroups':5,'exampleFte':'26.9','exampleExcludedFromFormalCounts':True,'absentImprovementMeansServiceStopped':False,'fteMeaning':'SERVICE_LEVEL_FULL_TIME_EQUIVALENT_PLAN_NOT_ACTIVITY_HOURS_OR_ACTUAL_FILLED_JOBS','projectAsteriskMeaning':'Corporate Projects team delivery indicated by source'})
 for p,title,summary,fte,scope,roles in a.PROGRAMMES:
  raw=page_by[p];first_table=min((t['bbox'][1] for t in raw['tables']),default=doc[p-1].rect.height)
  bs=[b for b in raw['blocks'] if b['bbox'][1]<first_table and 'SNOWY MONARO REGIONAL COUNCIL' not in b['text'] and not re.fullmatch(r'\s*\d+\s*',b['text'])]
  u=context(p,'PROGRAMME_CONTEXT',title,summary,[anchor(p,b['bbox'],'programmeContext') for b in bs]);u['facts'].update({'programmeLabel':title,'publishedResponsibleRoles':roles,'roleAssignmentStatus':'HISTORICAL_DOCUMENT_LABEL_ONLY','publishedFte':{'value':fte,'unit':'FTE','scope':scope,'actualFilledPositions':'UNKNOWN','activityAllocation':'UNKNOWN','summationAllowed':False},'budgetLocation':'END_OF_DOCUMENT' if 'included at the end' in raw['text'] else 'HELD_BY_OTHER_SERVICES' if p==104 else 'NOT_STATED_ON_THIS_PAGE'})
  fte_blocks=[b for b in bs if re.search(r'\bFTE\b',b['text'])]
  if fte_blocks:u['facts']['publishedFte']['sourceAnchors']=[anchor(p,b['bbox'],'publishedFte') for b in fte_blocks]
  budget_blocks=[b for b in bs if 'included at the end' in b['text'] or 'held by other services' in b['text']]
  u['facts']['budgetLocationAnchors']=[anchor(p,b['bbox'],'budgetLocation') for b in budget_blocks]
  if p==35:u['facts']['publishedFte']['components']=[{'label':'Coordinator','value':'1'},{'label':'communications, engagement and education','value':'3'},{'label':'customer service officers','value':'8'}]
  if p==40:u['facts']['publishedVolunteers']={'value':'22','unit':'people','fteEquivalent':'UNKNOWN'}
  if p==73:u['existingRecordIds']=['csoi:knowledge:op2026:water:programme','csoi:knowledge:op2026:water:staff-plan']
  if p==98:u['qualifiers'].append('13 FTE以组合位置公布；不推断全部归HR，也不与其他服务FTE叠加。')
  if p==104:u['qualifiers'].append('预算由负责QSP项目工作的其他服务持有；不是零预算，亦不得重复计入QSP总支出。')
 for p in original:
  if p['pdfPage']<13:continue
  notes=[];ans=[]
  for b in p['blocks']:
   s=norm(b['text']);msg=None
   if s.startswith('No major projects or infrastructure delivery is planned'):msg='本年度未列主要项目或基础设施交付；原文明确继续日常服务。'
   elif s.startswith('No improvement actions are planned'):msg='本年度未列改进行动；原文明确继续日常服务。'
   elif s.startswith('This service is a reactive service'):msg='本服务全部活动为反应式，不能因无计划工作判定服务缺失。'
   elif s.startswith('This service is not a reactive service'):msg='本服务原文将全部活动归为计划式，未列反应式活动。'
   elif s.startswith('Projects that are being delivered by the Corporate Projects team'):msg='Corporate Projects交付项目列在相关服务并带星号；此处不重复建立项目。'
   if msg:notes.append(msg);ans.append(anchor(p['pdfPage'],b['bbox'],'serviceScopeNote'))
  if notes:context(p['pdfPage'],'SERVICE_SCOPE_NOTE','服务范围与日常运营说明','；'.join(dict.fromkeys(notes)),ans)
 units.sort(key=lambda u:(u['pdfPage'],u['id']))
 pages=[]
 for p in original:
  n=p['pdfPage'];pu=[u for u in units if n in u['pages']];rs=[r for r in physical if r['pdfPage']==n]
  pp={'pdfPage':n,'printedPage':n,'disposition':'PHOTO_SEPARATOR_NO_VISIBLE_POLICY_BODY' if n in PHOTO_PAGES else 'FRONT_MATTER_OR_GUIDE_REVIEWED' if n<=11 else 'SERVICES_CONTEXT_AND_TABLES_REVIEWED','unitIds':[u['id'] for u in pu],'physicalRowIds':[r['physicalRowId'] for r in rs],'nativeTextDigest':digest(norm(doc[n-1].get_text('text'))),'parserVersion':PARSER,'detectedTableCount':len(p['tables']),'gaps':[]}
  if n in PHOTO_PAGES:pp['visualAnchor']=raster(n,list(doc[n-1].rect),'photoSeparator');pp['interpretation']='照片内容不转换为政策/行动；没有可见正文，不用可能被遮挡的提取层制造条款。'
  pages.append(pp)
 counts=collections.Counter(u['category'] for u in units);formal=[u for u in units if u['category'] in ['SERVICE_ACTION','PROJECT','IMPROVEMENT_ACTION']];formal_refs={r['occurrenceId']:r for u in formal for r in u['cspReferences']}
 pairs={(u['id'],r['code']) for u in formal for r in u['cspReferences']}
 coverage={'reviewedPdfPages':106,'fullSourcePdfPages':142,'formalPhysicalRows':517,'formalLogicalGroups':len(formal),'categories':dict(counts),'formalPhysicalRowTypes':dict(collections.Counter(r['sourceTableType'] for r in physical if r['formal'])),'firstColumnPrintedGroupsBeforeExplicitContinuation':418,'crossPageContinuationsMerged':1,'teachingExamplePhysicalRowsExcluded':6,'teachingExampleLogicalGroupsExcluded':5,'existingWaterActivitiesReferenced':len([u for u in formal if u['existingRecordIds']]),'existingWaterNativeRecordsUnchanged':11,'formalPrintedCspCodeOccurrences':len(formal_refs),'formalLogicalUnitCspPairs':len(pairs),'formalDistinctCspCodes':len({r['code'] for r in formal_refs.values()}),'unresolvedPrintedCspCodes':sorted({r['code'] for r in formal_refs.values() if r['resolution'].startswith('UNRESOLVED')}),'photoSeparatorPages':sorted(PHOTO_PAGES),'globalUniqueCouncilProjectDenominator':'UNKNOWN','fullOpCompletedByThisPart':False,'remainingPdfPagesOwnedByFinance':[107,142],'semantics':'行、合并动作、项目和改进行动是不同计数；417不是Council项目数。原文计划不等于实际执行。'}
 assert coverage['formalLogicalGroups']==417 and coverage['existingWaterActivitiesReferenced']==8
 result={'format':'csoi-op-services-author-1','sourceId':SOURCE,'sourceRevision':'sha256:'+PDF_SHA,'sourceBytes':37500187,'sourcePageCount':142,'part':{'id':'services','pdfPageStart':1,'pdfPageEnd':106},'parserVersion':PARSER,'rasterContract':RENDERER,'rights':'UNKNOWN','currentVersion':'UNKNOWN','currentLegalApplicability':'UNKNOWN','officialAdmission':'PENDING','originalBytesCommitted':False,'sourceVersionConflict':{'filename':'adopted-2026-2027-operational-plan-v3.1-w-revenue-policy.pdf','filenameVersion':'3.1','latestPopulatedBodyVersion':'1.3','workingDraftDisclaimerPresent':True,'resolution':'UNRESOLVED_CURRENTNESS'},'coverage':coverage,'pages':pages,'units':units}
 dump('services-author.json',result);dump('physical-row-coverage.json',{'sourceRevision':result['sourceRevision'],'rows':physical});dump('coverage-summary.json',coverage)
 with (HERE/'physical-row-coverage.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(physical[0]));w.writeheader();w.writerows([{**r,'existingRecordIds':'|'.join(r['existingRecordIds'])} for r in physical])
 with (HERE/'unit-coverage.csv').open('w',newline='') as f:
  w=csv.writer(f);w.writerow(['id','pdfPages','category','title','physicalRows','printedCspCodes','existingRecordIds']);w.writerows([u['id'],'|'.join(map(str,u['pages'])),u['category'],u['title'],len(u['physicalRowIds']),'|'.join(sorted({r['code'] for r in u['cspReferences']})),'|'.join(u['existingRecordIds'])] for u in units)
 receipt={'sourceId':SOURCE,'sourceRevision':result['sourceRevision'],'sourceBytes':37500187,'sourcePageCount':142,'inputHashes':{f:digest((HERE/f).read_bytes()) for f in ['row-readings.tsv','context-author.py','build-services-author.py']},'outputHashes':{f:digest((HERE/f).read_bytes()) for f in ['services-author.json','physical-row-coverage.json','physical-row-coverage.csv','unit-coverage.csv','coverage-summary.json']},'nativeWaterBundleDigest':digest((APP/'sources/op-water-public-knowledge.json').read_bytes()),'originalPdfCommitted':False,'independentSemanticReview':'PENDING_FINAL_PACKAGE_READBACK','sourceAnchorVerification':'PENDING_INDEPENDENT_ORIGINAL_VERIFIER'}
 dump('author-receipt.json',receipt)
 print(json.dumps(coverage,ensure_ascii=False));print('services-author.json',receipt['outputHashes']['services-author.json'])
if __name__=='__main__':main()
