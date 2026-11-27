"""Verify LSPS research against the original PDF, independently of its builder.
Source-first census, column crops and embedded tick image positions are checked.
This verifies bounded metadata/locations, not current law or authorised semantic admission.
"""
import argparse,collections,copy,csv,datetime,hashlib,json,re
from pathlib import Path
import pdfplumber,pypdf
APP=Path(__file__).resolve().parents[1]
RAW='sha256:9bf75ec6fb98f1d03bad47f5b9cda44e6ffadce3bf452eb5a343b394322f8f47'
SOURCE='csoi:smrc-lsps-2020:20261030';PREFIX='csoi:knowledge:lsps2020:'
def require(v,why):
 if not v:raise ValueError(why)
def norm(s):return ' '.join(s.split())
def hashtext(s):return 'sha256:'+hashlib.sha256(s.encode()).hexdigest()
def verify(pdfpath,bundle):
 raw=Path(pdfpath).read_bytes();require('sha256:'+hashlib.sha256(raw).hexdigest()==RAW,'ORIGINAL_BYTES_MISMATCH');require(bundle['sourceRevision']==RAW and bundle['sourceId']==SOURCE,'SOURCE_BINDING_MISMATCH');reader=pypdf.PdfReader(pdfpath);require(len(reader.pages)==bundle['sourcePageCount']==118,'SOURCE_PAGE_COUNT')
 require(bundle['rights']=='UNKNOWN'and bundle['currentVersion']=='UNKNOWN'and bundle['officialAdmission']=='PENDING'and bundle['originalBytesCommitted']is False,'SOURCE_BOUNDARY_PROMOTION')
 page_text={n:' '.join((reader.pages[n-1].extract_text(extraction_mode='layout')or'').split())for n in range(1,119)}
 page_hash={n:hashtext(t)for n,t in page_text.items()}
 # Independent whole implementation-page census using layout lines, not supplied row anchors.
 table_codes=[]
 for n in range(90,105):
  layout=reader.pages[n-1].extract_text(extraction_mode='layout')or''
  table_codes.extend(re.findall(r'^\s*(\d{1,2}\.\d{1,2})\s',layout,re.M))
 require(len(table_codes)==len(set(table_codes)),'ORIGINAL_DUPLICATE_IMPLEMENTATION_CODE')
 records=bundle['records'];require(len({r['id']for r in records})==len(records),'DUPLICATE_RECORD_ID')
 impl=[r for r in records if r['category']=='ACTION'and r['facts'].get('sourceSection')=='IMPLEMENTATION_TABLE'];require(set(table_codes)=={r['code']for r in impl}and len(table_codes)==len(impl),'IMPLEMENTATION_CENSUS_MISSING_OR_EXTRA')
 priorities=[r for r in records if r['category']=='PRIORITY'];root=next(r for r in records if r['category']=='DOCUMENT');require(len(priorities)==12 and root['facts']['implementationActionsExpected']==len(impl)==root['facts']['implementationActionsStructured'],'PRIORITY_OR_IMPLEMENTATION_COUNT')
 require(root['facts']['printedAdoptionDate']=='21 May 2020'and root['facts']['printedAdoptionDate']in page_text[1],'ADOPTION_NOT_IN_SOURCE');require('as of 2019' in page_text[104],'AGENCY_DATE_FOOTNOTE')
 expected_time={'Immediate':(0,1),'Short':(1,5),'Medium':(5,10),'Long':(10,20)}
 for label,(lo,hi)in expected_time.items():
  require(f'{label} {lo}-{hi} years following the adoption of the LSPS'in page_text[90],'SOURCE_RELATIVE_TIME_DEFINITION');f=root['facts']['timeframeDefinitions'][label];require(f=={'minimumYearsAfterAdoption':lo,'maximumYearsAfterAdoption':hi},'RELATIVE_TIME_DEFINITION_TAMPERED')
 require(root['facts']['timeframeDefinitions']['Ongoing']=={'basis':'WHEN_ITEM_ARISES'},'ONGOING_NOT_FIXED_DATE')
 parser='pypdf-'+pypdf.__version__+'-layout-whitespace-1'
 def check_anchor(a):
  require(a['parserVersion']==parser,'PARSER_REQUIRES_REVIEW');pn=a['pdfPage'];require(isinstance(pn,int)and 1<=pn<=118,'PAGE_BOUNDS');require(a['normalizedPageDigest']==page_hash[pn],'PAGE_ANCHOR_MISMATCH')
  if 'bbox'in a:require(len(a['bbox'])==4 and all(isinstance(x,(float,int))for x in a['bbox'])and 0<=a['bbox'][0]<a['bbox'][2]<=float(reader.pages[pn-1].mediabox.width)and 0<=a['bbox'][1]<a['bbox'][3]<=float(reader.pages[pn-1].mediabox.height),'BBOX_BOUNDS')
 def pointer(e):return e['anchor']['pdfPage'],tuple(e['anchor']['bbox'])
 all_rows=[];all_occurrences=[];tick_count=0
 with pdfplumber.open(pdfpath)as pdf:
  # Independent occurrence census from actual bullet/code pairs across all narrative/local pages.
  source_occ={}
  for pn in range(23,90):
   p=pdf.pages[pn-1];ws=p.extract_words();starts=[w for w in ws if w['x0']>290 and re.fullmatch(r'\d{1,2}\.\d{1,2}',w['text'])and any(x['text']==''and abs(x['top']-w['top'])<4 and 0<w['x0']-x['x0']<35 for x in ws)]
   for j,w in enumerate(starts):
    end=starts[j+1]['top']-1 if j+1<len(starts)else min(775,p.height-55);selected=[x for x in ws if x['x0']>=w['x0']-1 and w['top']-1<=x['top']<end];txt=norm(' '.join(x['text']for x in selected));source_occ[pn,w['text']]={'text':txt,'bbox':[round(w['x0']-1,3),round(w['top']-1,3),round(p.width-35,3),round(max(x['bottom']for x in selected)+1,3)]}
  represented=collections.Counter()
  for r in records:
   check_anchor(r['anchor']);f=r['facts'];row={'recordId':r['id'],'code':r['code'],'category':r['category'],'pdfPage':r['anchor']['pdfPage'],'sourceRevision':RAW,'pageHash':'PASS','status':'PASS_SOURCE_FIELDS_AND_LOCATORS','semanticReview':'AI_ASSISTED_BOUNDED_PARAPHRASE_REVIEW_NOT_AUTHORISED_ADMISSION','currentLaw':'UNKNOWN','actualWork':'UNKNOWN','officialAdmission':'PENDING'}
   if r['category']=='PRIORITY':
    c=int(r['code']);expected=[x for x in table_codes if x.split('.')[0]==str(c)];require(f['implementationActionCodes']==expected and f['implementationActionCount']==len(expected),'PRIORITY_ACTION_CENSUS');require(re.sub(r'\s+','',f['printedTitle'])in re.sub(r'\s+','',page_text[r['anchor']['pdfPage']]),'PRIORITY_TITLE_MISMATCH')
   if r['category']=='ACTION':
    require(f['actionCode']==r['code']and r['parentId']==PREFIX+'priority:'+r['code'].split('.')[0],'ACTION_PARENT_OR_CODE');require(f['actualCouncilAssignment']=='NOT_CREATED'and all(f[k]=='UNKNOWN'for k in ['actualExecution','actualOutcome','actualSpend','currentBudget','currentLegalApplicability'])and f['officialAdmission']=='PENDING','ACTUAL_OR_AUTHORITY_PROMOTION')
    evidence=f['evidenceAnchors'];require(len(evidence)>0,'MISSING_EVIDENCE')
    for e in evidence:
     check_anchor(e['anchor'])
     if e['role']!='IMPLEMENTATION_ROW':
      key=(e['anchor']['pdfPage'],r['code']);require(key in source_occ,'NARRATIVE_OCCURRENCE_MISSING');original=source_occ[key];require(e['anchor']['bbox']==original['bbox'],'NARRATIVE_ROW_BOUNDS');require(e['occurrenceTextDigest']==hashtext(original['text']),'NARRATIVE_TEXT_DIGEST');represented[key]+=1;all_occurrences.append({'pdfPage':key[0],'code':key[1],'recordId':r['id'],'role':e['role'],'status':'PASS_ORIGINAL_OCCURRENCE'})
    if f['sourceSection']=='IMPLEMENTATION_TABLE':
     segments=[e for e in evidence if e['role']=='IMPLEMENTATION_ROW'];require(pointer(segments[0])==(r['anchor']['pdfPage'],tuple(r['anchor']['bbox'])),'PRIMARY_ANCHOR_MISMATCH');cols=collections.defaultdict(list);ticks=[]
     for segment in segments:
      a=segment['anchor'];pn=a['pdfPage'];p=pdf.pages[pn-1];require(90<=pn<=104,'IMPLEMENTATION_PAGE_REQUIRED');x0,y0,x1,y1=a['bbox'];ws=p.extract_words();header_y=next(w['top']for w in ws if w['text']=='No.'and 80<w['top']<350);heads={k:next(w for w in ws if w['text']==k and abs(w['top']-header_y)<2)for k in ['Action','Timing','Who','Funded','CSP','DCP','LEP','CP','Strategy','Other']};names=list(heads);bounds=[heads[k]['x0']-5 for k in names]+[780]
      # Crop independently from the original PDF at the header column boundaries.
      for i,key in enumerate(names):
       crop=p.crop((bounds[i],y0,bounds[i+1],y1));cell=norm(crop.extract_text(x_tolerance=3,y_tolerance=3)or'');cols[key].append(cell);require(hashtext(cell)==segment['sourceCellDigests'][key],f'SOURCE_CELL_MISMATCH:{r["code"]}:PDF{pn}:{key}')
      for im in p.images:
       if y0<=im['top']+3<y1:
        category=next((key for i,key in enumerate(names)if bounds[i]<=im['x0']<bounds[i+1]),None)
        if category in ['DCP','LEP','CP','Strategy','Other']:ticks.append({'pdfPage':pn,'category':category,'imageDigest':'sha256:'+hashlib.sha256(im['stream'].get_data()).hexdigest(),'bbox':[round(im[k],3)for k in ['x0','top','x1','bottom']]})
     # At least the first source cell starts alongside the exact printed row number.
     a=segments[0]['anchor'];p=pdf.pages[a['pdfPage']-1];codecell=norm(p.crop((70,a['bbox'][1],100,a['bbox'][3])).extract_text()or'');require(codecell==r['code'],'WRONG_ORIGINAL_ROW')
     for field,col in [('printedTiming','Timing'),('printedWho','Who'),('who','Who'),('printedFunded','Funded'),('funded','Funded')]:require(f[field]==norm(' '.join(cols[col])),f'PRINTED_COLUMN_MISMATCH:{r["code"]}:{field}')
     refs=f['relatedPolicyReferences'];require(len(refs)==1 and refs[0]['column']=='CSP Delivery Program'and refs[0]['printedCode']==norm(' '.join(cols['CSP'])),'HISTORICAL_REFERENCE_COLUMN')
     require(f['relatedDocumentTickEvidence']==ticks,'TICK_IMAGE_POSITION_MISMATCH');categories=sorted({t['category']for t in ticks});require(f['printedRelatedDocumentCategories']==categories,'TICK_CATEGORY_MISMATCH');require(f['untickedRelatedDocumentCategories']==[c for c in ['DCP','LEP','CP','Strategy','Other']if c not in categories],'UNTICKED_CATEGORY_MISMATCH');tick_count+=len(ticks)
     row.update(columnVerification='PASS_SOURCE_CROPS',tickImagesVerified=len(ticks),continuationPages=[e['anchor']['pdfPage']for e in segments])
    else:
     require(f['sourceSection']in ['CORE_NARRATIVE_CONFLICT','LOCAL_ACTION_CONFLICT'],'UNKNOWN_SOURCE_SECTION');require(all(f[key]=='UNKNOWN_NOT_STATED_IN_THIS_OCCURRENCE'for key in ['printedTiming','printedWho','who','printedFunded','funded']),'BORROWED_TABLE_FACTS_FOR_DISTINCT_OCCURRENCE');require(f['relatedPolicyReferences']==[],'BORROWED_TABLE_RELATION_FOR_DISTINCT_OCCURRENCE')
   all_rows.append(row)
  require(set(represented)==set(source_occ)and all(v==1 for v in represented.values()),'NARRATIVE_CENSUS_MISSING_DUPLICATE_OR_EXTRA')
  # Specific source-anomaly guards prevent publication of false uniformity.
  by={r['code']:r for r in impl}
  # Explicit semantic safeguards requested by an independent source reviewer.
  semantic_qualifiers={'1.2':['Bombala','Delegate','streetscape','built form','heritage','visual'], '1.8':['Nimmitabel','restoration','adaptive reuse'], '6.7':['Berridale','town-centre'], '5.2':['consolidated LEP','prevent fragmentation','agricultural','resource land','value-adding'], '5.3':['agri-tourism','figures19 and28','innovation','diversification'], '4.2':['review and update','DCP','subdivision','solar orientation','active transport','stormwater','open space'], '11.6':['review and update','policies','guidelines','public-domain','water efficiency','drought','water availability']}
  for code,tokens in semantic_qualifiers.items():
   r=by[code];require(r['summary']==r['facts']['actionDescription'],'SUMMARY_FACT_DESCRIPTION_MISMATCH');require(all(token.casefold()in r['summary'].casefold()for token in tokens),'SEMANTIC_QUALIFIER_MISSING:'+code)
  for code,places in {'1.2':['Bombala','Delegate'],'1.8':['Nimmitabel'],'6.7':['Berridale']}.items():require(by[code]['facts']['namedLocations']==places,'NAMED_LOCATION_SCOPE_MISSING:'+code)
  require(by['2.1']['facts']['printedTiming']=='Medium/','SOURCE_TIMING_ANOMALY_LOST');require(by['3.1']['facts']['printedWho']=='SMRC &','SOURCE_RESPONSIBILITY_ANOMALY_LOST')
  for pn,code in [(27,'3.2'),(27,'3.3'),(27,'3.4'),(34,'5.4'),(42,'8.1'),(71,'6.8'),(89,'5.7')]:require(any(r['id']==PREFIX+f'narrative-action:p{pn}:{code}'for r in records),'SOURCE_CONFLICT_OCCURRENCE_LOST')
 return {'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_BOUNDED_SOURCE_VERIFICATION','sourceId':SOURCE,'rawDigest':RAW,'pages':118,'implementationCensus':len(table_codes),'priorities':len(priorities),'narrativeLocalOccurrences':len(source_occ),'distinctPrintedCodes':len(set(table_codes)|{c for p,c in source_occ}),'supplementalConflictRecords':len([r for r in records if r['category']=='ACTION'and r['facts']['sourceSection']!='IMPLEMENTATION_TABLE']),'tickImagesChecked':tick_count,'semanticQualifierChecks':list(semantic_qualifiers),'records':all_rows,'occurrences':all_occurrences,'limits':['Original byte/hash, full implementation row/column census, and all identified numbered narrative/local occurrence anchors verified.','Descriptions and source-internal conflicts reviewed by AI; not authorised independent human semantic admission.','Maps/diagrams and non-action narrative are inventoried but not fully structured; whole-document knowledge remains PARTIAL.','Historical reference codes/category ticks are not admitted current CSP2035, LEP/DCP, implementation or causal relationships.'],'officialAdmission':'PENDING','currentLegalApplicability':'UNKNOWN'}

def negative_checks(pdf,bundle):
 cases=[]
 def test(name,mutate):
  copy_bundle=copy.deepcopy(bundle);mutate(copy_bundle)
  try:verify(pdf,copy_bundle)
  except(ValueError,KeyError,StopIteration)as e:cases.append({'case':name,'status':'REJECTED_EXPECTED','reason':str(e)});return
  raise AssertionError('NEGATIVE_ACCEPTED:'+name)
 def impl(b):return next(r for r in b['records']if r['facts'].get('sourceSection')=='IMPLEMENTATION_TABLE')
 test('missing_implementation_row',lambda b:b['records'].remove(impl(b)))
 test('wrong_source_version',lambda b:b.update(sourceRevision='sha256:'+'0'*64))
 test('wrong_page_digest',lambda b:impl(b)['anchor'].update(normalizedPageDigest='sha256:'+'0'*64))
 test('wrong_funding_column',lambda b:impl(b)['facts'].update(funded='Yes'))
 test('wrong_tick_category',lambda b:impl(b)['facts']['relatedDocumentTickEvidence'][0].update(category='DCP'))
 test('missing_narrative_conflict',lambda b:b['records'].remove(next(r for r in b['records']if r['id']==PREFIX+'narrative-action:p27:3.2')))
 test('wrong_relative_time',lambda b:b['records'][0]['facts']['timeframeDefinitions']['Short'].update(maximumYearsAfterAdoption=10))
 test('claimed_actual_execution',lambda b:impl(b)['facts'].update(actualExecution='COMPLETE'))
 def drop_qualifier(b,code,old,new):
  r=next(r for r in b['records']if r['code']==code and r['facts'].get('sourceSection')=='IMPLEMENTATION_TABLE');r['summary']=r['summary'].replace(old,new);r['facts']['actionDescription']=r['summary']
 test('authored_location_scope_dropped',lambda b:drop_qualifier(b,'1.2','Bombala and Delegate','the towns'))
 test('authored_update_action_dropped',lambda b:drop_qualifier(b,'11.6','Review and update','Review'))
 return cases
if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('pdf',type=Path);ap.add_argument('bundle',type=Path);ap.add_argument('--out',type=Path);ap.add_argument('--negatives',type=Path);args=ap.parse_args();b=json.loads(args.bundle.read_text());result=verify(args.pdf,b)
 if args.out:args.out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 if args.negatives:args.negatives.write_text(json.dumps(negative_checks(args.pdf,b),indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items()if k not in ['records','occurrences','limits']},indent=2))
