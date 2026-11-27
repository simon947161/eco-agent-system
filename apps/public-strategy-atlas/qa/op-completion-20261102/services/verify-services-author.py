#!/usr/bin/env python3
"""Author-side original-position/column verifier, NOT independent semantic review.
Reads the original PDF itself. No network, source mutation, or raw redistribution.
"""
import argparse,copy,csv,hashlib,json,re,unicodedata
from collections import Counter
from pathlib import Path
import fitz
HERE=Path(__file__).resolve().parent;APP=HERE.parents[2]
REV='sha256:4e0b6440768c6bb902628ec36e43757366be470f583169834a4c7c3d4cf54fd2'
PARSER='pymupdf-1.26.6-text-nfkc-whitespace-v1';RENDERER='pymupdf-1.26.6-rgb-100dpi-fresh-document-clip-v2'
PHOTO={12,15,34,43,54,63,79,97,106}
WATER={'p073-t00-r01':'asset-maintenance','p073-t00-r02':'potable-water','p074-t00-r01':'daily-testing','p074-t01-r01':'service-requests','p074-t02-r01':'water-incidents','p074-t02-r03':'reactive-repairs','p074-t02-r04':'quality-complaints','p074-t03-r01':'sewer-maintenance'}
def norm(t):return re.sub(r'\s+',' ',unicodedata.normalize('NFKC',t or '')).strip()
def dg(v):return 'sha256:'+hashlib.sha256(v if isinstance(v,bytes) else v.encode()).hexdigest()
def require(ok,msg):
 if not ok:raise ValueError(msg)
def state(v):return 'MERGED_FROM_PRINTED_CELL' if v is None else 'BLANK' if not norm(v) else 'NOT_STATED_DASH' if norm(v)=='-' else 'NO_MEASURE' if norm(v).lower()=='no measure' else 'PRINTED_NIL' if norm(v).lower()=='nil' else 'PRINTED'
def source_gate(pdf):
 require(pdf.exists(),'missing original PDF');require(pdf.stat().st_size==37500187,'original byte count mismatch');require(dg(pdf.read_bytes())==REV,'original source revision mismatch')
def walk(obj):
 if isinstance(obj,dict):
  yield obj
  for v in obj.values():yield from walk(v)
 elif isinstance(obj,list):
  for v in obj:yield from walk(v)
class Verify:
 def __init__(self,pdf):
  source_gate(pdf);require(fitz.VersionBind=='1.26.6','parser version unavailable');self.pdf=pdf;self.doc=fitz.open(pdf);require(len(self.doc)==142,'original page count');self.rows={};self.groups={};self.expected={};self.hashes={};self.rasters={};self.native_text={}
  self.readings={r[0]:r[1:] for r in csv.reader((HERE/'row-readings.tsv').open(),delimiter='\t')}
  self.known={r['id'].rsplit(':',1)[-1]:r['id'] for r in json.loads((APP/'sources/csp-public-knowledge.json').read_text())['records'] if ':strategy:' in r['id']}
  current_group=None
  for pn in range(1,107):
   page=self.doc[pn-1];self.native_text[pn]=norm(page.get_text('text'))
   for ti,table in enumerate(page.find_tables().tables):
    values=table.extract();headers=values[0] if values else [];title=norm(headers[0]) if headers else ''
    if pn<13 and pn!=11:continue
    typ='SERVICE' if title=='Action/Program Description' else 'PROJECT' if title=='Major Project/Infrastructure Delivery' else 'IMPROVEMENT' if title=='Action' and len(headers)==2 else None
    if not typ:continue
    cols=['action','kpi','regulatory','target','reportingFrequency','csp','otherPlans'] if typ=='SERVICE' and len(headers)==7 else ['action','optimalVolume','fundedVolume','kpi','regulatory','target','reportingFrequency','csp','otherPlans'] if typ=='SERVICE' else ['projectTitle','description','annualBudget','resources','csp','otherPlans','start','end'] if typ=='PROJECT' else ['action','target']
    owners={}
    for ri in range(1,len(values)):
     rid=f'p{pn:03d}-t{ti:02d}-r{ri:02d}';vals=values[ri];boxes=table.rows[ri].cells
     if vals[0] is not None:
      current_group='csoi:op-full:'+rid
      if rid=='p030-t00-r01':require('cont.' in norm(vals[0]),'explicit continuation absent in source');current_group='csoi:op-full:p029-t00-r08'
     require(current_group is not None,'orphan merged source row')
     self.groups.setdefault(current_group,[]).append(rid)
     fields={}
     for ci,name in enumerate(cols):
      if boxes[ci] is not None:owners[name]={'owner':rid,'bbox':list(boxes[ci]),'value':norm(vals[ci]),'pdfPage':pn}
      require(name in owners,'original orphan cell');fields[name]={**owners[name],'state':state(vals[ci])}
     self.rows[rid]={'id':rid,'pdfPage':pn,'type':typ,'fields':fields,'values':vals,'unitId':current_group}
  require(len(self.rows)==523,'full original row denominator changed');require(sum(r['pdfPage']>=13 for r in self.rows.values())==517,'formal original denominator')
 def anchor(self,a):
  p=a['pdfPage'];bb=a['bbox'];require(type(p)==int and 1<=p<=106,'anchor page outside selected source');require(len(bb)==4 and all(isinstance(v,(int,float)) and not isinstance(v,bool) for v in bb),'invalid bbox')
  bounds=self.doc[p-1].rect;require(0<=bb[0]<bb[2]<=bounds.width+0.001 and 0<=bb[1]<bb[3]<=bounds.height+0.001,'bbox outside original page')
  key=(p,tuple(bb))
  if 'normalizedTextDigest' in a:
   require(a.get('parserVersion')==PARSER,'wrong parser contract')
   if key not in self.hashes:self.hashes[key]=dg(norm(self.doc[p-1].get_text('text',clip=fitz.Rect(bb))))
   require(a['normalizedTextDigest']==self.hashes[key],f'original text/crop mismatch at {p} {bb}')
  if 'rasterDigest' in a:
   require(a.get('renderer')==RENDERER,'wrong raster contract')
   if key not in self.rasters:
    with fitz.open(self.pdf) as fresh:
     pix=fresh[p-1].get_pixmap(matrix=fitz.Matrix(100/72,100/72),clip=fitz.Rect(bb),colorspace=fitz.csRGB,alpha=False)
     self.rasters[key]=(dg(f'RGB|{pix.width}x{pix.height}|'.encode()+pix.samples),pix.width,pix.height)
   original=self.rasters[key];require(a['rasterDigest']==original[0],'original pixel crop mismatch');require(a.get('width')==original[1] and a.get('height')==original[2],'original raster dimensions mismatch')
 def check(self,x):
  require(x['sourceRevision']==REV and x['sourceId']=='csoi:smrc-op-2026:20261030','source identity/version mismatch');require(x['sourcePageCount']==142 and x['sourceBytes']==37500187,'source bounds')
  require(x['part']=={'id':'services','pdfPageStart':1,'pdfPageEnd':106},'part scope mismatch');require(x['coverage']['fullOpCompletedByThisPart'] is False,'part falsely claims full OP completion')
  require(x['sourceVersionConflict']['filenameVersion']=='3.1' and x['sourceVersionConflict']['latestPopulatedBodyVersion']=='1.3' and x['sourceVersionConflict']['workingDraftDisclaimerPresent'] is True,'version conflict erased')
  require([p['pdfPage'] for p in x['pages']]==list(range(1,107)),'page coverage incomplete')
  us={u['id']:u for u in x['units']};require(len(us)==len(x['units'])==483,'unit denominator mismatch')
  actual={};formalrefs={};pairs=set();water={}
  for uid,u in us.items():
   require(u['pdfPage']==u['pages'][0] and len(set(u['pages']))==len(u['pages']),'unit first/source pages')
   for name in ['currentVersion','currentLegalApplicability','actualOutput','actualExecution','actualSpend','actualOutcome','activityResourceAllocation']:require(u['facts']['interpretation'][name]=='UNKNOWN','unadmitted actual/legal/allocation claim')
   require(u['facts']['interpretation']['councilAssignmentCreated'] is False,'official task assignment invented')
   rs=u['facts'].get('rows',[])
   if rs:
    expected_ids=self.groups.get(uid);require(expected_ids is not None and [r['id'] for r in rs]==expected_ids and u['physicalRowIds']==expected_ids,'logical grouping or physical row missing/duplicate')
    expcat='GUIDE_EXAMPLE' if self.rows[rs[0]['id']]['pdfPage']==11 else {'SERVICE':'SERVICE_ACTION','PROJECT':'PROJECT','IMPROVEMENT':'IMPROVEMENT_ACTION'}[self.rows[rs[0]['id']]['type']]
    require(u['category']==expcat,'guide/formal category or table type mixed')
    require(u['pages']==list(dict.fromkeys(self.rows[r]['pdfPage'] for r in expected_ids)),'cross-page source lost')
    expected_refs={}
    for row in rs:
     rid=row['id'];require(rid not in actual,'source row duplicated');actual[rid]=row;src=self.rows[rid]
     require(row['pdfPage']==src['pdfPage'],'row moved from original page');require(set(row['fields'])==set(src['fields']),'column omitted or added')
     if src['pdfPage']>=13:
      reading=self.readings[rid];require(row['summary']==reading[1],'authored semantic reading altered');require(row['conditions']==([] if reading[2]=='-' else [reading[2]]),'authored source condition dropped/altered')
     for name,f in row['fields'].items():
      expected=src['fields'][name];an=f['sourceAnchor'];require(f['sourceState']==expected['state'],'dash/blank/merged/No measure/Nil distinction lost');require(f['sourceCellOwnerRow']==expected['owner'],'wrong merged cell owner')
      require(an['field']==name and an['pdfPage']==expected['pdfPage'] and an['bbox']==expected['bbox'],'anchor moved to wrong source page/column/cell')
      if name not in ['action','projectTitle','description','kpi']:require(f['publishedValue']==expected['value'],'printed source value/unit/period/comparator changed')
      if name=='annualBudget':require(f['currency']=='UNKNOWN' and f['summationAllowed'] is False,'currency/annualisation invented')
      if name=='csp':
       for code in re.findall(r'(?<![\d.])\d{1,2}\.\d{1,2}(?![\d.])',expected['value']):expected_refs[expected['owner']+':csp:'+code]=(code,expected)
     for r in row['sourceAnchors']:self.anchor(r)
    require({r['occurrenceId'] for r in u['cspReferences']}==set(expected_refs),'printed CSP reference occurrence omitted/added')
    for r in u['cspReferences']:
     code,exp=expected_refs[r['occurrenceId']];require(r['code']==code and r['targetId']==self.known.get(code),'invented CSP mapping');require(r['relationship']=='PRINTED_SOURCE_REFERENCE_ONLY','CSP reference promoted to official mapping');require(r['sourceAnchor']['bbox']==exp['bbox'] and r['sourceAnchor']['pdfPage']==exp['pdfPage'],'CSP original position wrong')
     if expcat!='GUIDE_EXAMPLE':formalrefs[r['occurrenceId']]=r;pairs.add((uid,code))
    expected_water=WATER.get(expected_ids[0]);require(u['existingRecordIds']==(['csoi:knowledge:op2026:water:activity:'+expected_water] if expected_water else []),'legacy water semantic identity duplicated/missing')
    if expected_water:water[expected_water]=u
   if u['category']=='FRONT_MATTER':require(u['section']==('Reading guide and example' if u['pdfPage']==11 else 'Document front matter'),'front matter mislabelled guide')
   if u['category']=='PROGRAMME_CONTEXT':
    pn=u['pdfPage'];fte_matches=re.findall(r'(\d+(?:\.\d+)?)\s+FTE\b',self.native_text[pn])
    require(u['facts']['publishedFte']['value']==(fte_matches[0] if fte_matches else None),'published FTE differs from original service page')
    require(u['facts']['publishedFte']['unit']=='FTE' and u['facts']['publishedFte']['summationAllowed'] is False,'FTE changed to actual jobs or additive allocation')
    for role in u['facts']['publishedResponsibleRoles']:require(norm(role) in self.native_text[pn],'responsible role absent from original page')
   for ref in u['lspsReferences']:require(ref['relationship']=='NAMED_DOCUMENT_REFERENCE_ONLY' and ref['priorityOrActionMapping']=='UNKNOWN','invented LSPS action mapping')
  require(set(actual)==set(self.rows),'full original physical row coverage missing')
  require(len(water)==8 and sum(len(u['physicalRowIds']) for u in water.values())==9,'existing water action/source row count')
  require(len({r['occurrenceId'] for u in water.values() for r in u['cspReferences']})==10 and len({(u['id'],r['code']) for u in water.values() for r in u['cspReferences']})==9,'water ten occurrences/nine pairs lost')
  require(x['coverage']['formalPrintedCspCodeOccurrences']==len(formalrefs)==694,'formal CSP occurrence denominator');require(x['coverage']['formalLogicalUnitCspPairs']==len(pairs)==594,'formal CSP pair denominator')
  require(x['coverage']['formalLogicalGroups']==417 and x['coverage']['formalPhysicalRows']==517,'row/group denominator conflated')
  require(us['csoi:op-full:p098:programme_context']['facts']['publishedFte']['scope']=='PORTFOLIO','portfolio FTE falsely assigned to HR')
  require(us['csoi:op-full:p104:programme_context']['facts']['budgetLocation']=='HELD_BY_OTHER_SERVICES','QSP held-elsewhere budget treated as zero/own allocation')
  require(us['csoi:op-full:p035:programme_context']['facts']['publishedFte']['components']==[{'label':'Coordinator','value':'1'},{'label':'communications, engagement and education','value':'3'},{'label':'customer service officers','value':'8'}],'FTE composition altered')
  require(us['csoi:op-full:p040:programme_context']['facts']['publishedVolunteers']=={'value':'22','unit':'people','fteEquivalent':'UNKNOWN'},'volunteers silently converted to FTE')
  for p in x['pages']:
   n=p['pdfPage'];require(p['nativeTextDigest']==dg(self.native_text[n]),'original page digest mismatch');require(p['unitIds']==[u['id'] for u in x['units'] if n in u['pages']],'page unit membership incomplete');require(p['physicalRowIds']==[r for r in self.rows if self.rows[r]['pdfPage']==n],'page row membership incomplete')
   if n in PHOTO:require(p['disposition']=='PHOTO_SEPARATOR_NO_VISIBLE_POLICY_BODY','photo treated as policy body')
  for obj in walk(x):
   if 'bbox' in obj and ('normalizedTextDigest' in obj or 'rasterDigest' in obj):self.anchor(obj)
  return {'uniqueOriginalTextAnchors':len(self.hashes),'uniqueOriginalPixelAnchors':len(self.rasters),'originalPages':106,'physicalRows':523,'formalRows':517,'formalGroups':417,'units':483,'legacyWaterActivities':8,'formalPrintedCspOccurrences':694,'formalUnitCspPairs':594}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--pdf',default='/tmp/csoi-strategy-completion-20261101/op.pdf');ap.add_argument('--author',default=str(HERE/'services-author.json'));args=ap.parse_args();pdf=Path(args.pdf);v=Verify(pdf);x=json.loads(Path(args.author).read_text());result=v.check(x)
 # These original-text preconditions ground selected semantic regressions; they do not prove all semantics.
 selected=[('p037-t00-r01',r'consultation and approved by CEO'),('p039-t01-r02',r'over 2 years'),('p073-t00-r01',r'per 100km of water main/year'),('p102-t01-r03',r'Upon notification.*48 hours'),('p105-t00-r02',r'Commence streamlined')]
 for rid,pattern in selected:require(re.search(pattern,norm(' '.join(s or '' for s in v.rows[rid]['values'])),re.I),'selected semantic original condition absent: '+rid)
 def findrow(y,rid):return next(r for u in y['units'] for r in u['facts'].get('rows',[]) if r['id']==rid)
 def unit(y,uid):return next(u for u in y['units'] if u['id']==uid)
 cases=[]
 def negative(name,mutate):
  y=copy.deepcopy(x);mutate(y)
  try:v.check(y)
  except (ValueError,KeyError,TypeError) as exc:cases.append({'case':name,'outcome':'REJECTED','reason':str(exc)});return
  raise RuntimeError('negative wrongly admitted: '+name)
 negative('wrong_source_version',lambda y:y.update(sourceRevision='sha256:'+'0'*64))
 negative('wrong_page_same_hash',lambda y:findrow(y,'p073-t00-r01')['fields']['target']['sourceAnchor'].update(pdfPage=72))
 def wrongcol(y):
  row=findrow(y,'p073-t00-r01');row['fields']['target']['sourceAnchor']=copy.deepcopy(row['fields']['reportingFrequency']['sourceAnchor']);row['fields']['target']['sourceAnchor']['field']='target'
 negative('wrong_column_even_with_valid_other_column_hash',wrongcol)
 negative('wrong_original_bbox',lambda y:findrow(y,'p073-t00-r01')['sourceAnchors'][1]['bbox'].__setitem__(0,40))
 negative('wrong_budget_unit',lambda y:findrow(y,'p039-t01-r02')['fields']['annualBudget'].update(publishedValue='$4,012,048 thousand over 2 years'))
 negative('deleted_two_year_period',lambda y:findrow(y,'p039-t01-r02')['fields']['annualBudget'].update(publishedValue='$4,012,048'))
 negative('deleted_CEO_approval_condition',lambda y:findrow(y,'p037-t00-r01').update(conditions=[]))
 negative('notification_start_changed_to_injury_time',lambda y:findrow(y,'p102-t01-r03').update(conditions=['伤害发生后48小时。']))
 negative('commence_changed_to_completed',lambda y:findrow(y,'p105-t00-r02').update(summary='已完成派工系统。'))
 negative('invented_CSP_mapping',lambda y:unit(y,'csoi:op-full:p073-t00-r01')['cspReferences'][0].update(targetId='csoi:knowledge:csp2035:strategy:12.3'))
 negative('invented_LSPS_action_mapping',lambda y:unit(y,'csoi:op-full:p008:front_matter')['lspsReferences'][0].update(priorityOrActionMapping='priority12:action1'))
 negative('guide_example_counted_as_formal_action',lambda y:unit(y,'csoi:op-full:p011-t00-r01').update(category='SERVICE_ACTION'))
 negative('dash_promoted_to_zero',lambda y:findrow(y,'p013-t00-r01')['fields']['target'].update(sourceState='PRINTED',publishedValue='0'))
 negative('planned_FTE_changed',lambda y:unit(y,'csoi:op-full:p073:programme_context')['facts']['publishedFte'].update(value='53'))
 negative('source_target_marked_actual',lambda y:unit(y,'csoi:op-full:p073-t00-r01')['facts']['interpretation'].update(actualOutput='PASS'))
 negative('portfolio_13FTE_assigned_to_HR',lambda y:unit(y,'csoi:op-full:p098:programme_context')['facts']['publishedFte'].update(scope='BUSINESS_UNIT'))
 negative('pixel_crop_digest_corrupt',lambda y:unit(y,'csoi:op-full:p010:front_matter')['facts']['visualAnchor'].update(rasterDigest='sha256:'+'0'*64))
 negative('incomplete_part_claims_entire_OP',lambda y:y['coverage'].update(fullOpCompletedByThisPart=True))
 negative('dropped_physical_source_row',lambda y:unit(y,'csoi:op-full:p073-t00-r01')['facts']['rows'].clear())
 for name,path in [('missing_original_pdf',Path('/tmp/csoi-op-full-20261102/does-not-exist-original.pdf'))]:
  try:source_gate(path)
  except ValueError as exc:cases.append({'case':name,'outcome':'REJECTED','reason':str(exc)})
  else:raise RuntimeError('missing original accepted')
 bad=Path('/tmp/csoi-op-full-20261102/services/corrupt-original-negative.pdf');raw=bytearray(pdf.read_bytes());raw[100]^=1;bad.write_bytes(raw)
 try:
  try:source_gate(bad)
  except ValueError as exc:cases.append({'case':'same_size_corrupt_original_pdf','outcome':'REJECTED','reason':str(exc)})
  else:raise RuntimeError('corrupt original accepted')
 finally:bad.unlink()
 report={'format':'csoi-op-services-author-verification-1','sourceRevision':REV,'authorFileDigest':dg(Path(args.author).read_bytes()),'verifierDigest':dg(Path(__file__).read_bytes()),'status':'PASS_AUTHOR_SIDE_ORIGINAL_POSITION_AND_COLUMN_CHECKS','independent':False,'semanticScope':'All authored row/condition transfers bound; selected original text conditions checked. This is not independent or exhaustive automated semantic proof. Independent reviewer has a separate report.','verified':result,'selectedOriginalSemanticPreconditions':[{'physicalRowId':r,'originalTextPattern':p} for r,p in selected],'negativeTests':cases,'negativeCount':len(cases),'originalBytesCommitted':False}
 (HERE/'author-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':report['status'],'verified':result,'negativeCount':len(cases),'authorFileDigest':report['authorFileDigest']},ensure_ascii=False))
if __name__=='__main__':main()
