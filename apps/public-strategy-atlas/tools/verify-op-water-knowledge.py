"""Independent original-column verification of bounded OP water research records.

Does not import the builder or treat a bundle's own hashes as evidence of truth.
Re-reads fixed, independently reviewed page/column coordinates in the original PDF.
"""
import argparse,copy,csv,datetime,hashlib,json,pathlib,re
import pdfplumber,pypdf,subprocess
APP=pathlib.Path(__file__).resolve().parents[1]
SOURCE='csoi:smrc-op-2026:20261030'
RAW='sha256:4e0b6440768c6bb902628ec36e43757366be470f583169834a4c7c3d4cf54fd2'
PREFIX='csoi:knowledge:op2026:water:'
# Independently reviewed table row boundaries, including the two incident KPI subrows.
SPEC={
 'asset-maintenance':(73,(410.1,445.04),'planned',[(15,'<')]),
 'potable-water':(73,(445.04,521.22),'planned',[(20,'<')]),
 'daily-testing':(74,(76.56,149.9),'planned',[(100,'UNKNOWN')]),
 'service-requests':(74,(218.77,253.71),'reactive',[(80,'UNKNOWN')]),
 'water-incidents':(74,(322.58,373.26),'reactive',[(4,'<'),(50,'<')]),
 'reactive-repairs':(74,(373.26,398.61),'reactive',[(4,'<')]),
 'quality-complaints':(74,(398.61,414.35),'reactive',[('UNKNOWN','UNKNOWN')]),
 'sewer-maintenance':(74,(483.22,508.56),'sewer',[(80,'UNKNOWN')])}
COLUMNS={'planned':[36.5,226.77,456.38,525.83,589.61,657.07,739.28,805.39],'reactive':[36.5,226.77,463.46,532.91,588.19,655.65,737.86,805.39],'sewer':[36.5,226.77,460.63,530.08,588.19,655.65,737.86,805.39]}
NAMES=['action','serviceStandard','regulatory','target','reporting','cspReference','otherPlans']
def norm(s):return ' '.join((s or '').split())
def sha(s):return 'sha256:'+hashlib.sha256(s.encode()).hexdigest()
def need(x,code):
 if not x:raise ValueError(code)
def page_digest(reader,n):return sha(norm(reader.pages[n-1].extract_text(extraction_mode='layout')))
def verify(pdf,bundle):
 need('sha256:'+hashlib.sha256(pdf.read_bytes()).hexdigest()==RAW,'ORIGINAL_BYTES_MISMATCH')
 need(bundle['sourceRevision']==RAW and bundle['sourceId']==SOURCE,'SOURCE_BINDING_MISMATCH')
 need(bundle['rights']=='UNKNOWN'and bundle['currentVersion']=='UNKNOWN'and bundle['officialAdmission']=='PENDING','SOURCE_ADMISSION_PROMOTION')
 reader=pypdf.PdfReader(pdf);need(len(reader.pages)==bundle['sourcePageCount']==142,'PAGE_COUNT_MISMATCH')
 records=bundle['records'];by={n['id']:n for n in records};need(len(by)==len(records)==11,'RECORD_CENSUS_MISMATCH')
 expected={PREFIX+x for x in ['document','programme','staff-plan']}|{PREFIX+'activity:'+x for x in SPEC};need(set(by)==expected,'MISSING_OR_EXTRA_RECORD')
 rows=[];refs=[];action_starts=[]
 with pdfplumber.open(pdf)as original:
  for page in [73,74]:
   for word in original.pages[page-1].extract_words():
    if word['x0']<45 and word['text']in ['Undertake','Provide','Daily','Respond','Investigate','Operate']and(page!=73 or word['top']>410):action_starts.append({'page':page,'y':round(word['top'],2),'firstWord':word['text']})
  need(len(action_starts)==8,'ORIGINAL_ACTION_CENSUS_MISMATCH')
  for n in records:
   a=n['anchor'];need(a['parserVersion']=='pypdf-'+pypdf.__version__+'-layout-whitespace-1','PARSER_VERSION_MISMATCH');need(a['normalizedPageDigest']==page_digest(reader,a['pdfPage']),'PAGE_ANCHOR_MISMATCH')
   page=original.pages[a['pdfPage']-1];x0,y0,x1,y1=a['bbox'];need(0<=x0<x1<=page.width and 0<=y0<y1<=page.height,'ANCHOR_OUTSIDE_ORIGINAL_PAGE')
   f=n['facts'];need(all(f[k]=='UNKNOWN'for k in ['actualExecution','actualOutput','actualSpend','actualOutcome']),'FALSE_ACTUAL');need(f['actualCouncilAssignment']=='NOT_CREATED'and f['carbonContribution']=='UNKNOWN_NO_CAUSAL_EVIDENCE'and f['humanReview']=='PENDING'and f['computability']=='NOT_COMPUTABLE','FALSE_AUTHORITY_OR_COMPUTABILITY')
  for key,(page,(top,bottom),layout,values)in SPEC.items():
   n=by[PREFIX+'activity:'+key];f=n['facts'];need(n['category']=='WATER_ACTIVITY'and n['kind']=='Activity'and n['parentId']==PREFIX+'programme','WRONG_ACTIVITY_IDENTITY');need(n['anchor']['pdfPage']==page,'WRONG_PAGE');edges=COLUMNS[layout]
   bounds={name:[edges[i],top,edges[i+1],bottom]for i,name in enumerate(NAMES)};need(f['originalColumnBounds']==bounds,'WRONG_COLUMN_BOUNDS');need(n['anchor']['bbox']==[edges[0],top,edges[-1],bottom],'WRONG_ROW_BOUNDS')
   cells={name:norm(original.pages[page-1].crop(box).extract_text())for name,box in bounds.items()}
   for name,value in cells.items():need(f['originalColumns'][name]=={'normalizedTextDigest':sha(value),'normalizedCharacterCount':len(value)},'SOURCE_COLUMN_MISMATCH:'+key+':'+name)
   need(f['printedAction']==cells['action']and f['printedRegulatory']==cells['regulatory']and f['printedOtherPlans']==cells['otherPlans'],'PRINTED_FIELD_MISMATCH')
   need(f['target']['printed']==cells['target'],'TARGET_VALUE_MISMATCH')
   missing=all(x=='-'for x in cells['target'].split());need(('NOT_STATED_DASH'in f['target']['meaning'])==missing,'DASH_IS_NOT_A_VALUE')
   need(f['printedReportingFrequency']==cells['reporting'],'REPORTING_COLUMN_MISMATCH');freq='UNKNOWN_NOT_STATED_DASH'if all(x=='-'for x in cells['reporting'].split())else cells['reporting'];need(f['reportingFrequency']==freq,'REPORTING_INTERVAL_MISMATCH')
   need(f['printedServiceLevel']['sourceCellDigest']==sha(cells['serviceStandard']),'KPI_SOURCE_MISMATCH')
   need([(s['value'],s['comparator'])for s in f['serviceStandards']]==values,'KPI_NUMBER_OR_COMPARATOR_MISMATCH')
   if key in ['daily-testing','service-requests','sewer-maintenance']:
    need(all(s['comparator']=='UNKNOWN' and 'without a comparison sign'in s.get('comparisonBasis','')for s in f['serviceStandards']),'BARE_PERCENTAGE_COMPARATOR_NOT_STATED')
    need(not re.search(r'[<>=]\s*(?:80|100)\s*%',cells['serviceStandard']),'SOURCE_COMPARATOR_REQUIRES_REVIEW')
   # Verify independent expected numerical values actually appear in their own source KPI column.
   for value,comparator in values:
    if isinstance(value,(int,float)):
     token=('<'+str(value))if comparator=='<'else str(value)+'%';need(token in cells['serviceStandard'],'KPI_VALUE_NOT_IN_ORIGINAL_COLUMN')
   if key=='asset-maintenance':need('100km'in cells['serviceStandard']and f['serviceStandards'][0]['denominator']=='100 km of water main','KPI_DENOMINATOR_MISMATCH')
   if key in ['potable-water','water-incidents']:need('1,000'in cells['serviceStandard'],'SOURCE_CONNECTION_DENOMINATOR')
   codes=re.findall(r'\b\d+\.\d+\b',cells['cspReference']);unique=list(dict.fromkeys(codes));need(f['printedCspReferences']==codes and f['sourceCspCodes']==unique,'SOURCE_CSP_REFERENCE_MISMATCH')
   need([r['targetId']for r in n['relations']]==['csoi:knowledge:csp2035:strategy:'+x for x in unique]and all(r['type']=='EXPLICIT_DOCUMENT_REFERENCE'for r in n['relations']),'RELATION_TARGET_MISMATCH')
   rows.append({'id':n['id'],'sourceId':SOURCE,'sourceRevision':RAW,'pdfPage':page,'printedPage':page,'anchor':n['anchor'],'category':n['category'],'extracted':'YES_BOUNDED_RESEARCH','implemented':'PENDING_PARENT_INTEGRATION','sourceVerified':'PASS_ORIGINAL_COLUMNS_AND_BOUNDED_FACTS','semanticReview':'AI_ASSISTED_BOUNDED_REVIEW_NOT_FORMAL_ADMISSION','gap':'Current applicability, actual execution and financial/activity allocations UNKNOWN; whole OP not extracted.','evidence':'qa/strategy-completion/op/source-verification.json','sourceCellChecks':len(cells)})
   for code in unique:refs.append({'from':n['id'],'to':'csoi:knowledge:csp2035:strategy:'+code,'pdfPage':page,'printedOccurrencesInThisRow':codes.count(code),'type':'EXPLICIT_DOCUMENT_REFERENCE','actualImplementation':'UNKNOWN','causalEffect':'UNKNOWN','officialAdmission':'PENDING'})
  staff=by[PREFIX+'staff-plan'];need(staff['anchor']['pdfPage']==73 and staff['facts']['baseline']['value']==52.5 and staff['facts']['baseline']['unit']=='FTE','STAFF_VALUE_MISMATCH');need('52.5 FTE'in norm(original.pages[72].crop((36,220,190,262)).extract_text()),'STAFF_ORIGINAL_MISMATCH')
  v=by[PREFIX+'document']['facts']['publishedDocument'];version=norm(reader.pages[2].extract_text());need('1.3'in version and '30/06/2026'in version and '225/26'in version and 'working draft'in version,'VERSION_EVIDENCE_MISSING');need(v['latestPopulatedVersionTableLabel']=='1.3'and v['printedDate']=='30/06/2026'and v['printedResolution']=='225/26'and 'v3.1'in v['registeredUrlVersionLabel']and 'UNKNOWN'in v['versionConflict'],'VERSION_CONFLICT_HIDDEN')
  need(by[PREFIX+'document']['facts']['selectedPages']==[73,74]and by[PREFIX+'document']['facts']['wholeDocumentCoverage']=='PARTIAL_SELECTED_TWO_PAGE_PROGRAMME','FALSE_WHOLE_DOCUMENT_COVERAGE')
  for key in ['document','programme','staff-plan']:
   n=by[PREFIX+key];rows.append({'id':n['id'],'sourceId':SOURCE,'sourceRevision':RAW,'pdfPage':n['anchor']['pdfPage'],'printedPage':n['anchor']['pdfPage'],'anchor':n['anchor'],'category':n['category'],'extracted':'YES_BOUNDED_RESEARCH','implemented':'PENDING_PARENT_INTEGRATION','sourceVerified':'PASS_ORIGINAL_METADATA_OR_RESOURCE','semanticReview':'AI_ASSISTED_BOUNDED_REVIEW_NOT_FORMAL_ADMISSION','gap':'Programme staffing is not assigned hours/spend; authoritative current version UNKNOWN.','evidence':'qa/strategy-completion/op/source-verification.json'})
 return {'status':'PASS_TESTED_HERE','at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sourceId':SOURCE,'rawDigest':RAW,'sourcePages':142,'selectedActivityPages':[73,74],'recordsChecked':11,'activityRows':8,'sourceCellsChecked':56,'independentActionStartCensus':action_starts,'distinctActionStrategyReferences':len(refs),'printedCspOccurrences':sum(x['printedOccurrencesInThisRow']for x in refs),'records':rows,'references':refs,'wholeDocumentCoverage':'PARTIAL','sourceAdmission':'PENDING','originalBodyCommitted':False}
def negatives(pdf,b):
 cases={}
 def case(name,change):
  x=copy.deepcopy(b);change(x)
  try:verify(pdf,x)
  except (ValueError,KeyError,IndexError)as e:cases[name]={'status':'REJECTED_EXPECTED','reason':str(e)}
  else:raise AssertionError('NEGATIVE_ACCEPTED:'+name)
 case('wrong-source-digest',lambda x:x.update(sourceRevision='sha256:'+'0'*64))
 case('missing-activity',lambda x:x['records'].pop())
 case('out-of-page-bounds',lambda x:x['records'][0]['anchor'].update(bbox=[36,35,805,575]))
 case('wrong-page',lambda x:x['records'][3]['anchor'].update(pdfPage=74))
 case('wrong-source-column',lambda x:x['records'][3]['facts']['originalColumns']['target'].update(normalizedTextDigest='sha256:'+'0'*64))
 case('target-promoted-or-substituted',lambda x:x['records'][3]['facts']['target'].update(printed='47'))
 case('invented-reference',lambda x:x['records'][3]['facts'].update(sourceCspCodes=['6.1']))
 case('duplicate-source-occurrence-erased',lambda x:x['records'][7]['facts'].update(printedCspReferences=['8.2']))
 case('invented-bare-percentage-equality',lambda x:x['records'][6]['facts']['serviceStandards'][0].update(comparator='='))
 case('invented-bare-percentage-minimum',lambda x:x['records'][10]['facts']['serviceStandards'][0].update(comparator='>='))
 case('false-actual-result',lambda x:x['records'][3]['facts'].update(actualOutput=47))
 case('missing-version-conflict',lambda x:x['records'][0]['facts']['publishedDocument'].update(latestPopulatedVersionTableLabel='3.1'))
 return cases
def supplementary(pdf,out):
 reader=pypdf.PdfReader(pdf);rows=[]
 with pdfplumber.open(pdf)as original:
  for topic,page,y,edges,expected in [('food-first-volume-row',27,[367.02,392.36],[36.5,211.65,257.01,302.36,496.06,557.48,597.73,652.44,730.39,805.39],{'optimal':'168','funded':'84','target':'84','reporting':'Biannual','cspReference':['6.1'],'kpiTokens':['98%','P1, P2 and P3','at least once a year']}),('ltw-complaints-row',30,[111.5,146.45],[36.5,211.65,257.01,302.36,490.39,554.17,600.95,655.65,737.86,806.24],{'optimal':'25','funded':'25','target':'90%','reporting':'Quarterly','cspReference':['6.1','8.2'],'kpiTokens':['90%','LTW','72 hours']})]:
   names=['action','optimal','funded','serviceStandard','regulatory','target','reporting','cspReference','otherPlans'];cells={name:norm(original.pages[page-1].crop((edges[i],y[0],edges[i+1],y[1])).extract_text())for i,name in enumerate(names)}
   for name in ['optimal','funded','target','reporting']:need(cells[name]==expected[name],'EXISTING_OP_FIELD_MISMATCH:'+topic+':'+name)
   codes=re.findall(r'\b\d+\.\d+\b',cells['cspReference']);need(codes==expected['cspReference'],'EXISTING_OP_REFERENCE_MISMATCH');need(all(token in cells['serviceStandard']for token in expected['kpiTokens']),'EXISTING_OP_KPI_MISMATCH')
   rows.append({'id':topic,'sourceId':SOURCE,'sourceRevision':RAW,'pdfPage':page,'normalizedPageDigest':page_digest(reader,page),'rowBounds':[edges[0],y[0],edges[-1],y[1]],'publishedValues':{k:expected[k]for k in ['optimal','funded','target','reporting']},'sourceCspCodes':codes,'sourceCellDigests':{k:sha(v)for k,v in cells.items()},'status':'PASS_FRESH_ORIGINAL_COLUMN_RECHECK','actualOutput':'UNKNOWN','formalAdmission':'PENDING'})
 # Read the current generated registry as evidence; never modify it or assume old audit counts.
 code="const b=require('./sources/csoi-default-snapshot.js').snapshot;console.log(JSON.stringify({digest:b.audit.datasetDigest,rows:b.dataset.domain.assertions.filter(e=>e.id.startsWith('csoi:reported-reference:')||e.id.startsWith('csoi:published-plan-link:')).map(e=>({id:e.id,from:e.from,to:e.to,predicate:e.predicate,state:e.state,admission:e.admission}))}));"
 current=json.loads(subprocess.check_output(['node','-e',code],cwd=APP,text=True));edges=current['rows'];need(len(edges)==8,'EXISTING_CANDIDATE_CENSUS_CHANGED_REVIEW_REQUIRED')
 for edge in edges:edge['evidenceMeaning']='SAME_TABLE_FIELD_ASSOCIATION'if edge['id'].startswith('csoi:published-plan-link:')and not edge['id'].endswith(':programme')else'EXPLICIT_CSP_REFERENCE_ALREADY_REPRESENTED';edge['countsAsAnotherDistinctSourceReference']=False;edge['officialAdmission']='PENDING'
 existing={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sourceId':SOURCE,'sourceRevision':RAW,'sourceRows':rows,'distinctSourceReferenceFacts':3,'existingGraphRepresentations':8,'explicitCspCandidateRepresentations':4,'sameTableFieldRepresentations':4,'generatedRegistryDigest':current['digest'],'existingEdges':edges,'conclusion':'Three distinct source references remain represented by four CSP candidates plus four table-field associations. The old csp6/csp8 endpoints remain research stations, not newly admitted CSP identities; no duplicate source facts are added by this check.'}
 (out/'existing-op-relationships.json').write_text(json.dumps(existing,ensure_ascii=False,indent=2)+'\n')
 contents=[]
 for page in [4,5]:
  for line in reader.pages[page-1].extract_text().splitlines():
   match=re.match(r'(.+?)\s+(\d{1,3})$',line.strip())
   if match and not line.startswith('SNOWY')and 'OPERATIONAL PLAN'not in line:contents.append({'sectionTitle':match[1],'startsAtPrintedPage':int(match[2]),'tocPdfPage':page,'tocPageDigest':page_digest(reader,page),'coverage':'SELECTED_WATER_ROWS_ONLY'if 'Water and Wastewater'in line else'NOT_FULLY_EXTRACTED_IN_THIS_BATCH'})
 needs={75:'Remaining planned/reactive wastewater rows plus initial capital-project rows: not implemented by the selected eight-action bundle.',76:'Water capital-project table: not implemented; budget/target/status not promoted to actuals.',77:'Further water capital projects and wastewater capital-project table: not implemented.',78:'Wastewater capital-project rows and dated action list: not implemented.',79:'No extractable text; graphical content not independently interpreted.',107:'Capital expenditure schedule starts here per contents; complete schedule not extracted.',112:'Service budgets start here per contents; activity-level allocations not established.',118:'Budget summary starts here per contents; not integrated as actual expenditure.',124:'Revenue policy appendix starts here per contents; not extracted.'}
 inventory=[]
 for page in range(1,143):
  status='FULL_SELECTED_ACTION_ROWS_VERIFIED'if page in [73,74]else'SELECTED_EXISTING_ROW_RECHECK'if page in [27,30]else'VERSION_CONFLICT_REVIEWED'if page==3 else'TABLE_OF_CONTENTS_REVIEWED'if page in [4,5]else'IDENTIFIED_GAP'if page in needs else'NOT_CENSUSED_THIS_BATCH'
  inventory.append({'pdfPage':page,'reviewStatus':status,'gap':needs.get(page,'No whole-page or complete-document extraction claim.'if page not in [73,74]else'Only selected service/action table and programme resource fields; no actual results or legal applicability established.')})
 (out/'document-coverage.json').write_text(json.dumps({'sourceId':SOURCE,'sourceRevision':RAW,'pages':142,'tableOfContents':contents,'pageInventory':inventory,'fullDocumentAtomicItemDenominator':'UNKNOWN_NOT_CENSUSED','fullDocumentReferenceDenominator':'UNKNOWN_NOT_CENSUSED','selectedActionDenominator':8,'selectedActionsExtracted':8,'otherWaterPages':[75,76,77,78,79],'versionConflict':'URL v3.1; internal latest populated table1.3; working-draft statement remains. Current authoritative version UNKNOWN.','notARecoveryOfPriorUncommittedFiles':True},ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('pdf',type=pathlib.Path);p.add_argument('bundle',type=pathlib.Path,nargs='?',default=APP/'sources/op-water-public-knowledge.json');p.add_argument('--out',type=pathlib.Path,default=APP/'qa/strategy-completion/op');p.add_argument('--negative',action='store_true');a=p.parse_args();b=json.loads(a.bundle.read_text());a.out.mkdir(parents=True,exist_ok=True);result=verify(a.pdf,b);(a.out/'source-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');(a.out/'coverage-matrix.json').write_text(json.dumps(result['records'],ensure_ascii=False,indent=2)+'\n');
 with (a.out/'coverage-matrix.csv').open('w',newline='')as f:
  fields=['id','sourceId','sourceRevision','pdfPage','printedPage','category','extracted','implemented','sourceVerified','semanticReview','gap','evidence'];w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(result['records'])
 supplementary(a.pdf,a.out)
 if a.negative:(a.out/'negative-results.json').write_text(json.dumps(negatives(a.pdf,b),indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items()if k not in ['records','references']},ensure_ascii=False))
