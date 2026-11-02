"""Compile reviewed author units into the existing source-pinned page record model."""
from pathlib import Path
import collections, hashlib, json, sys, unicodedata
import fitz
APP=Path(__file__).resolve().parents[1]
PDF=Path(sys.argv[1] if len(sys.argv)>1 and not sys.argv[1].startswith('--') else '/tmp/csoi-strategy-completion-20261101/op.pdf')
SHA='4e0b6440768c6bb902628ec36e43757366be470f583169834a4c7c3d4cf54fd2'
assert hashlib.sha256(PDF.read_bytes()).hexdigest()==SHA
doc=fitz.open(PDF);assert len(doc)==142
input_bytes={}
def read(p):
 data=(APP/p).read_bytes();input_bytes[p]=data;return json.loads(data)
def clean(v):
 if isinstance(v,dict):return {k:clean(x) for k,x in v.items() if k not in ['localOnlyCrop','localCropPath']}
 if isinstance(v,list):return [clean(x) for x in v]
 return v
def digest(s):return 'sha256:'+hashlib.sha256(s.encode()).hexdigest()
def norm(s):return ' '.join(unicodedata.normalize('NFKC',s).split())
services=read('qa/op-completion-20261102/services/services-author.json');finance=read('qa/op-completion-20261102/finance/finance-author.json')
parts=[services,finance]
def partkey(x):return x['part']['id'] if isinstance(x['part'],dict) else x['part']
def denominator(x):return x.get('sourceDenominators',x.get('coverage'))
source='csoi:smrc-op-2026:20261030'
assert all(x['sourceId']==source and x['sourceRevision']=='sha256:'+SHA for x in parts)
units=clean([u for x in parts for u in x['units']]);assert len({u['id'] for u in units})==len(units)
pages=[p for x in parts for p in x['pages']];assert sorted(p['pdfPage'] for p in pages)==list(range(1,143))
csp={n['code']:n['id'] for n in read('sources/csp-public-knowledge.json')['records'] if n['category']=='CSP_STRATEGY'}
old=read('sources/op-water-public-knowledge.json');water={n['id'] for n in old['records']}
root='csoi:knowledge:op2026:review:document';pageid=lambda p:'csoi:knowledge:op2026:review:page:'+str(p).zfill(3)
common={'reviewId':'OP-FULL-REVIEW-20261102','reviewMethod':'INDEPENDENT_AI_SOURCE_REVIEW_NOT_OFFICIAL','sourceRevision':'sha256:'+SHA,'currentLaw':'UNKNOWN','currentLegalApplicability':'UNKNOWN','actualExecution':'UNKNOWN','actualOutput':'UNKNOWN','actualSpend':'UNKNOWN','actualOutcome':'UNKNOWN','officialAdmission':'PENDING','humanReview':'PENDING'}
scope='Bounded reading of this registered 142-page OP artifact, including service/action KPI subrows, projects, improvements, contextual text/graphics, budget tables, revenue policy and rating maps. Page and unit counts describe explicit source coverage, not comprehension percentage, current-law admission, parcel applicability or actual Council delivery. The original eight selected water activities remain unchanged; no other-year expansion or private ledger access.'
def anchor(p):return {'pdfPage':p,'normalizedPageDigest':digest(norm(doc[p-1].get_text('text'))),'parserVersion':'pymupdf-1.26.6-text-nfkc-whitespace-v1'}
def record(p,category,title,summary,facts,relations=None):return {'id':root if category=='OP_DOCUMENT' else pageid(p),'kind':'DocumentRevision' if category=='OP_DOCUMENT' else 'ContentBlock','category':category,'code':'OP-FULL-REVIEW' if category=='OP_DOCUMENT' else 'OP-PAGE-'+str(p).zfill(3),'parentId':None if category=='OP_DOCUMENT' else root,'title':title,'summary':summary,'locator':f'OP 2026–27 · PDF {p} · page/unit reading; exact per-field source anchors retained','anchor':anchor(p),'facts':{**common,**facts},'relations':relations or []}
records=[record(3,'OP_DOCUMENT','OP 2026–27 · 142 页有界原文梳理','在同一登记原件和模型中补齐逐页阅读。服务行动、指标子行、项目、预算与收入政策分别保存，不表示实际交付或官方准入。',{'totalPages':142,'scope':scope,'sourceVersionBoundaries':finance['sourceVersionBoundaries'],'sourceDenominators':{partkey(x):denominator(x) for x in parts}})]
findings=read('qa/op-completion-20261102/independent/initial-source-findings.json')['findings']
diagnostics=clean([v for x in parts for v in x.get('diagnostics',[])])
compiledPages=[];references=[]
for u in units:
 for ref in u['cspReferences']:
  assert isinstance(ref,dict) and isinstance(ref['code'],str)
  target=csp.get(ref['code']);assert ref.get('targetId')==target
  references.append({'unitId':u['id'],'unitCategory':u['category'],**ref,'targetId':target,'relationship':'PRINTED_SOURCE_REFERENCE_ONLY'})
for p in pages:
 number=p['pdfPage'];selected=[u for u in units if u['pdfPage']==number];refs=[r for r in references if r['pdfPage']==number];existing=[]
 for u in selected:
  assert set(u['existingRecordIds'])<=water;existing.extend(u['existingRecordIds'])
 existing=sorted(set(existing));relations=[]
 for target in sorted({r['targetId'] for r in refs if r['targetId'] and r['unitCategory'] in ['SERVICE_ACTION','PROJECT','IMPROVEMENT_ACTION']}):
  matching=[r for r in refs if r['targetId']==target and r['unitCategory'] in ['SERVICE_ACTION','PROJECT','IMPROVEMENT_ACTION']]
  ids=[r['unitId'] for r in matching];refpages=','.join(str(v) for v in sorted({r['pdfPage'] for r in matching}))
  relations.append({'type':'EXPLICIT_DOCUMENT_REFERENCE','targetId':target,'locator':f'Reading record anchored at PDF {number}; actual printed CSP reference pages {refpages}, in {len(set(ids))} reading unit(s); precise per-unit/row anchors in facts.printedCspReferences. This page link does not assign every page action to the strategy.'})
 for target in existing:relations.append({'type':'SOURCE_READING_CONTEXT','targetId':target,'locator':f'PDF {number}: retained original water selection; exact unit IDs in facts.units. Same activity, not a duplicate work assignment.'})
 assert len(relations)<=20,(number,len(relations))
 anomalies=[x for x in diagnostics if x.get('pdfPage')==number or number in x.get('pdfPages',[])]+[x for x in findings if number in x.get('pdfPages',[])]
 continued=[{'unitId':u['id'],'pageRecordId':pageid(u['pdfPage']),'sourcePages':u.get('pages',[u['pdfPage']])} for u in units if u['pdfPage']!=number and number in u.get('pages',[])]
 for continuation in continued:relations.append({'type':'SOURCE_READING_CONTEXT','targetId':continuation['pageRecordId'],'locator':f"PDF {number}: explicit continuation of {continuation['unitId']}; full unit retained once on its first page."})
 assert len(relations)<=20
 section=p.get('section') or ' / '.join(dict.fromkeys(u['section'] for u in selected))[:250] or p['disposition']
 n=record(number,'OP_PAGE',f'OP PDF {number} · {section}',f'本页归档 {len(selected)} 个阅读单元，另有 {len(continued)} 个跨页续行入口；分开保留计划目标、实际未知、单位、角色、条件和原件疑点。',{'units':selected,'pageDisposition':p['disposition'],'sourceAnomalies':anomalies,'printedCspReferences':refs,'existingRecordIds':existing,'continuedReadings':continued},relations);records.append(n)
 compiledPages.append({'pdfPage':number,'section':section,'status':p['disposition'],'pageDigest':n['anchor']['normalizedPageDigest'],'recordIds':list(dict.fromkeys([n['id'],*existing,*[u['pageRecordId'] for u in continued]])),'unitIds':[u['id'] for u in selected]+[u['unitId'] for u in continued],'gap':'Current controlled version, legal/parcel applicability, authorised human admission and actual execution remain UNKNOWN/PENDING. '+('Source conflicts retained; not automatically resolved.' if anomalies else '')})
counts={'pages':142,'pageRecords':142,'semanticUnits':len(units),'unitCategories':dict(collections.Counter(u['category'] for u in units)),'retainedWaterActivities':8,'allPrintedCspReferenceOccurrences':len(references),'formalPrintedCspReferenceOccurrences':sum(r['unitCategory'] in ['SERVICE_ACTION','PROJECT','IMPROVEMENT_ACTION'] for r in references),'resolvedCspReferenceOccurrences':sum(r['targetId'] is not None for r in references),'unresolvedCspReferenceOccurrences':sum(r['targetId'] is None for r in references),'sourceDiagnostics':len(diagnostics),'parts':{partkey(x):denominator(x) for x in parts}}
value={'format':'csoi-op-completion-review-1','sourceId':source,'sourceRevision':'sha256:'+SHA,'sourcePageCount':142,'reviewId':common['reviewId'],'scope':scope,'counts':counts,'pages':compiledPages,'records':records,'referenceIndex':references,'diagnostics':diagnostics,'sourceAuthorHashes':{f: 'sha256:'+hashlib.sha256(input_bytes[f]).hexdigest() for f in ['qa/op-completion-20261102/services/services-author.json','qa/op-completion-20261102/finance/finance-author.json']}}
assert len(records)==143 and sum(len(n['facts'].get('units',[])) for n in records)==len(units)
outputs={'sources/op-completion-review.json':json.dumps(value,ensure_ascii=False,indent=2)+'\n','sources/op-completion-review.js':'(function(root){const value='+json.dumps(value,ensure_ascii=False,separators=(',',':'))+';root.CsoiOpCompletionReview=value;if(typeof module!==\'undefined\')module.exports=value;})(typeof window!==\'undefined\'?window:globalThis);\n'}
for file,data in input_bytes.items():assert (APP/file).read_bytes()==data,'SOURCE_CHANGED_DURING_BUILD:'+file
for file,body in outputs.items():
 if '--check' in sys.argv:assert (APP/file).read_text()==body,'OP_REVIEW_MIRROR_STALE'
 else:(APP/file).write_text(body)
print(json.dumps(counts,ensure_ascii=False))
