"""Check reconstructed CSP items directly against original PDF columns using a second parser.
Does not import the builder or treat hashes as proof of paraphrase meaning. A passing
result is bounded source-census/tabular/role verification, not official admission.
"""
import argparse,copy,csv,hashlib,json,re,tempfile,datetime
from pathlib import Path
import fitz,pypdf
from pypdf import PdfReader
APP=Path(__file__).resolve().parents[1]
SHA='sha256:dc4fe1fca1d860b3389ea1e5ddca3826efaf5d02a7d029242a45ec20666cf743'
SID='csoi:smrc-csp-full-2025:20261030';PREFIX='csoi:knowledge:csp2035:'
REGIONS=[(29,'community',168.662,767.74),(30,'economy',158.56,447.70),(30,'environment',481.709,714.20),(31,'infrastructure',158.56,476.04),(31,'civic',512.89,702.82)]
X={29:[56.693,235.35,409.606,460.63,537.165],30:[57.443,244.779,411.079,462.103,538.637],31:[56.443,243.78,410.079,461.103,537.637]}
def norm(s):return ' '.join(s.split())
def h(s):return 'sha256:'+hashlib.sha256(s.encode()).hexdigest()
def need(ok,why):
 if not ok:raise ValueError(why)
def cell(words,b):
 x0,y0,x1,y1=b
 selected=[w for w in words if x0<=w[0]<x1 and y0<=(w[1]+w[3])/2<y1]
 # Group baselines before x order; glyph bounds differ slightly across mixed font runs.
 selected.sort(key=lambda w:((w[1]+w[3])/2,w[0]));lines=[]
 for w in selected:
  mid=(w[1]+w[3])/2
  if not lines or abs(mid-lines[-1][0])>3:lines.append([mid,[]])
  lines[-1][1].append(w)
 return norm(' '.join(' '.join(w[4]for w in sorted(line,key=lambda w:w[0]))for _,line in lines))
def expected_rows(pdf):
 out=[]
 for page,pillar,top,end in REGIONS:
  q=pdf[page-1];edges=set()
  for drawing in q.get_drawings():
   for item in drawing['items']:
    if item[0]=='l':
     a,b=item[1:3]
     if abs(a.y-b.y)<0.1 and 450<a.x<470 and b.x>530 and top+.5<a.y<end-.5:edges.add(round(a.y,3))
  bounds=[top]+sorted(edges)+[end]
  for i,(start,stop)in enumerate(zip(bounds,bounds[1:]),1):out.append({'code':f'CSP-KPI-{page}-{pillar}-{i:02d}','page':page,'pillar':pillar,'row':i,'bounds':[X[page][0],start,X[page][-1],stop],'cells':[cell(q.get_text('words'),[X[page][j],start,X[page][j+1],stop])for j in range(4)]})
 return out
class Source:
 def __init__(self,path):
  self.body=path.read_bytes();self.sha='sha256:'+hashlib.sha256(self.body).hexdigest();need(self.sha==SHA,'ORIGINAL_BYTE_MISMATCH');self.pdf=fitz.open(path);self.reader=PdfReader(path);need(len(self.pdf)==36,'PAGE_CENSUS')
  self.hashes={n:h(norm(self.reader.pages[n-1].extract_text(extraction_mode='layout')or''))for n in range(1,37)};self.metrics=expected_rows(self.pdf);self.strategy={}
  for page in range(18,28):
   q=self.pdf[page-1];words=q.get_text('words');codes=[w for w in words if re.fullmatch(r'\d{1,2}\.\d',w[4])and 170<w[0]<220];codes.sort(key=lambda w:w[1])
   if not codes:continue
   head=next(w for w in words if w[4]=='Council’s');partner=next(w[0]for w in words if w[4]=='Our'and abs(w[1]-head[1])<2)-6
   role=min(w[0]for w in words if w[4]in ['Provide','Collaborate','Advocate']and w[0]>300 and w[1]>=codes[0][1]-2)
   end=next(((w[1]+w[3])/2-9 for w in words if w[4]=='Supporting'and w[1]>codes[-1][1]),786)
   for i,w in enumerate(codes):
    top=(w[1]+w[3])/2-8;bottom=(codes[i+1][1]+codes[i+1][3])/2-8 if i+1<len(codes)else end
    self.strategy[w[4]]={'page':page,'roles':cell(words,[role-2,top,partner,bottom]).split(),'partners':cell(words,[partner,top,550,bottom]),'point':[w[0],(w[1]+w[3])/2]}
 def verify(self,b):
  need(b['sourceId']==SID and b['sourceRevision']==self.sha,'SOURCE_ID_OR_REVISION');need(b['sourcePageCount']==len(self.pdf),'PAGE_COUNT');need(b['rights']=='UNKNOWN'and b['officialAdmission']=='PENDING'and b['currentVersion']=='UNKNOWN','AUTHORITY_OR_RIGHTS_PROMOTION')
  nodes=b['records'];by={n['id']:n for n in nodes};need(len(by)==len(nodes),'DUPLICATE_ITEM');bycat={k:[n for n in nodes if n['category']==k]for k in {n['category']for n in nodes}}
  need(len(self.metrics)==63 and len(self.strategy)==44 and len({c.split('.')[0]for c in self.strategy})==14,'ORIGINAL_CENSUS_CHANGED')
  need({n['code']for n in bycat.get('CSP_INDICATOR',[])}=={r['code']for r in self.metrics},'MISSING_OR_EXTRA_METRIC')
  need({n['code']for n in bycat.get('CSP_STRATEGY',[])}==set(self.strategy),'MISSING_OR_EXTRA_STRATEGY')
  need({n['code']for n in bycat.get('CSP_OBJECTIVE',[])}=={s.split('.')[0]for s in self.strategy},'MISSING_OR_EXTRA_OBJECTIVE')
  need({n['code']for n in bycat.get('CSP_PILLAR',[])}=={r[1]for r in REGIONS},'MISSING_OR_EXTRA_PILLAR');need(len(bycat.get('CSP_DOCUMENT',[]))==1,'DOCUMENT_COUNT')
  need('3.0' in self.pdf[34].get_text() and '1/5/25' in self.pdf[34].get_text() and '73/25' in self.pdf[34].get_text(),'VERSION_TABLE')
  for n in nodes:
   a=n['anchor'];p=a['pdfPage'];need(p in self.hashes and a['normalizedPageDigest']==self.hashes[p],'PAGE_HASH:'+n['id']);need(a['parserVersion']=='pypdf-'+pypdf.__version__+'-layout-whitespace-1','PARSER_VERSION');need(0<=a['bbox'][0]<a['bbox'][2]<=596 and 0<=a['bbox'][1]<a['bbox'][3]<=842,'BBOX_BOUNDS');need(n['parentId']is None or n['parentId']in by,'PARENT_MISSING')
  for expected in self.metrics:
   n=next(n for n in bycat['CSP_INDICATOR']if n['code']==expected['code']);f=n['facts'];page=expected['page'];need(n['anchor']['pdfPage']==page,'METRIC_PAGE');need(n['parentId']==PREFIX+'pillar:'+expected['pillar']and f['pillar']==expected['pillar'],'METRIC_PILLAR')
   need(all(abs(a-b)<.03 for a,b in zip(n['anchor']['bbox'],expected['bounds'])),'METRIC_ROW_BOUNDS')
   for key,value in zip(['printedLabel','printedSource','printedBaseline','printedDesiredTrend'],expected['cells']):need(norm(f[key])==value,'COLUMN_'+key+':'+n['code']+' expected='+value+' actual='+str(f[key]))
   need(f['desiredTrend']==f['printedDesiredTrend'],'TREND_MISMATCH');need(f['tableRow']==expected['row'],'TABLE_ROW')
   for j,key in enumerate(['measure','source','baseline','trend']):need(all(abs(a-b)<.03 for a,b in zip(f['originalColumnBounds'][key],[X[page][j],expected['bounds'][1],X[page][j+1],expected['bounds'][3]])),'COLUMN_BOUNDS')
   printed=expected['cells'][2];value=float(re.search(r'-?\d[\d,]*(?:\.\d+)?',printed).group().replace(',',''));scale=10**6 if re.search(r'\dM\b',printed)else 1;need(f['baseline']['value']==value and f['baseline']['scale']==scale and f['baseline']['normalisedValue']==value*scale,'BASELINE_NUMERIC')
   yrs=re.findall(r'20\d\d(?:[-–]\d{2,4})?',expected['cells'][1]);need(f['sourceYear']==(yrs[-1]if yrs else'UNKNOWN'),'SOURCE_YEAR')
   need(f['computability']=='NOT_COMPUTABLE'and f['actualValue']=='UNKNOWN'and f['denominator']['value']=='UNKNOWN'and f['humanReview']=='PENDING','METRIC_AUTHORITY_OR_COMPUTABILITY')
  for n in bycat['CSP_STRATEGY']:
   e=self.strategy[n['code']];need(n['anchor']['pdfPage']==e['page'],'STRATEGY_PAGE');need(n['parentId']==PREFIX+'objective:'+n['code'].split('.')[0],'STRATEGY_PARENT');need(n['facts']['councilRoles']==e['roles'],'STRATEGY_ROLES:'+n['code']+str(e['roles']));need(norm(n['facts']['partners']['printedColumnText'])==e['partners'],'STRATEGY_PARTNERS:'+n['code']+' expected='+e['partners']);need(n['facts']['actualOutcome']=='UNKNOWN','STRATEGY_ACTUAL')
  leadership=next(n for n in bycat['CSP_STRATEGY']if n['code']=='12.1')
  need('visible and accessible' in norm(self.pdf[25].get_text()).lower(),'LEADERSHIP_SOURCE_QUALIFIERS')
  need(all(re.search(r'\b'+word+r'\b',leadership['summary'].lower())for word in ['visible','accessible']),'LEADERSHIP_SUMMARY_QUALIFIERS')
  for n in bycat['CSP_PILLAR']:
   page={'community':19,'economy':21,'environment':23,'infrastructure':25,'civic':27}[n['code']]
   source_lines=self.pdf[page-1].get_text(sort=True).split('Supporting documents, plans or strategies',1)[1].splitlines()
   expected_names=[norm(line)for line in source_lines if norm(line)and not re.fullmatch(r'\d+',norm(line))]
   need([r['title']for r in n['facts']['supportingDocuments']]==expected_names,'SUPPORTING_DOCUMENT_CENSUS:'+n['code'])
   for reference in n['facts']['supportingDocuments']:
    page=reference['pdfPage'];need(reference['normalizedPageDigest']==self.hashes[page],'SUPPORTING_DOCUMENT_ANCHOR');need(norm(reference['title'])in norm(self.pdf[page-1].get_text()),'SUPPORTING_DOCUMENT_NAME');need(reference['version']=='UNKNOWN'and reference['implementation']=='UNKNOWN'and reference['relationship']=='SOURCE_LISTED_SUPPORTING_DOCUMENT','SUPPORTING_DOCUMENT_PROMOTION')
  water=next(n for n in nodes if n['code']=='CSP-KPI-31-infrastructure-05');carbon=next(n for n in nodes if n['code']=='CSP-KPI-30-environment-03');need(water['facts']['baseline']['value']==7519 and water['facts']['baseline']['unit']=='UNKNOWN','WATER_UNIT_NOT_STATED');need(carbon['facts']['baseline']['value']==29.9 and carbon['facts']['baseline']['unit']=='tonnes CO2e/person','CARBON_UNIT_SCOPE')
  conflicts={n['code']:n for n in nodes if n['code']in ['CSP-KPI-29-community-22','CSP-KPI-31-infrastructure-03']};need(len(conflicts)==2 and {n['facts']['baseline']['value']for n in conflicts.values()}=={2.1,3.1}and all(set(n['facts']['sourceConflictIds'])==set(conflicts)for n in conflicts.values()),'TRANSPORT_CONFLICT_NOT_RETAINED')
  return {'status':'PASS_ORIGINAL_COLUMNS_AND_CENSUS','sourceId':SID,'sourceRevision':self.sha,'pages':36,'itemCounts':{k:len(v)for k,v in bycat.items()},'verifiedMetricColumnCells':252,'verifiedStrategyRolePartnerRows':44,'precision':'Two-parser source/page/row/column checks plus authored paraphrase review; hashes alone do not establish semantic truth.','officialAdmission':'PENDING','currentLaw':'UNKNOWN','fullDocumentSemanticCoverage':'NOT_CLAIMED','independentActualRecalculation':'NOT_COMPUTABLE'}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('pdf',type=Path);p.add_argument('bundle',type=Path);p.add_argument('--out',type=Path);p.add_argument('--negative-out',type=Path);a=p.parse_args();source=Source(a.pdf);b=json.loads(a.bundle.read_text());result=source.verify(b);result['at']=datetime.datetime.now(datetime.timezone.utc).isoformat()
 if a.out:a.out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 if a.negative_out:
  cases=[]
  def reject(label,mutate):
   x=copy.deepcopy(b);mutate(x)
   try:source.verify(x)
   except (ValueError,KeyError)as e:cases.append({'case':label,'status':'REJECTED_EXPECTED','reason':str(e)});return
   raise AssertionError('NEGATIVE_ACCEPTED:'+label)
  metric=lambda x:next(n for n in x['records']if n['code']=='CSP-KPI-31-infrastructure-05')
  reject('omitted-visible-leadership-qualifier',lambda x:next(n for n in x['records']if n['code']=='12.1').update(summary='Make leadership accessible to the community.'));reject('omitted-supporting-document',lambda x:next(n for n in x['records']if n['category']=='CSP_PILLAR')['facts']['supportingDocuments'].pop());reject('changed-source-revision',lambda x:x.update(sourceRevision='sha256:'+'0'*64));reject('omitted-last-indicator',lambda x:x['records'].pop());reject('forged-water-tonnes',lambda x:metric(x)['facts']['baseline'].update(unit='tonnes'));reject('changed-baseline-value',lambda x:metric(x)['facts']['baseline'].update(value=7500));reject('wrong-row-page',lambda x:metric(x)['anchor'].update(pdfPage=30));reject('shifted-cell-bounds',lambda x:metric(x)['facts']['originalColumnBounds']['source'].__setitem__(0,1));reject('fabricated-role',lambda x:next(n for n in x['records']if n['code']=='8.1')['facts'].update(councilRoles=['Provide']));reject('missing-partner',lambda x:next(n for n in x['records']if n['code']=='8.2')['facts']['partners'].update(printedColumnText='NSW Health'));reject('promoted-actual',lambda x:metric(x)['facts'].update(actualValue=7519));reject('removed-source-conflict',lambda x:next(n for n in x['records']if n['code']=='CSP-KPI-29-community-22')['facts'].update(sourceConflictIds=[]))
  a.negative_out.write_text(json.dumps(cases,ensure_ascii=False,indent=2)+'\n');result['negativeCasesRejected']=len(cases)
 print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
