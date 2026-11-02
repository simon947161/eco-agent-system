"""Read-only source inventory and bounded evidence audit. No source KB is changed.

Semantic conclusions are a documented AI-assisted review of selected claims. Token
checks reproduce page selection, not automatic proof of semantic completeness.
"""
from pathlib import Path
import csv,collections,hashlib,importlib.util,json
from pypdf import PdfReader
ROOT=Path('/tmp/csoi-integrity-audit-20261031');OUT=ROOT/'coverage';APP=ROOT/'readonly-head/apps/public-strategy-atlas'
catalogue=json.loads((APP/'sources/csoi-catalogue.json').read_text());obs=json.loads((APP/'sources/csoi-source-observations.json').read_text())['observations'];recovery=json.loads((ROOT/'local-originals.json').read_text())['results'];dataset=json.loads((OUT/'default-dataset.json').read_text())
recov={r['sourceId']:r for r in recovery};observed={o['intakeRecord']['id']:o for o in obs if o.get('httpStatus')==200 and o.get('intakeRecord')};entities={e['id']:e for e in dataset['domain']['entities']}
records=collections.defaultdict(list)
for e in entities.values():
 data=e.get('data',{}).get('csoiRecord',{}).get('data',{});sid=data.get('sourceId')
 if sid:
  kind='clause' if 'dcpClause' in data else 'historical_reference' if 'sourceClauseId' in data else 'published_plan' if e['id'].startswith('csoi:published-plan:') else 'research_note'
  records[sid].append({'id':e['id'],'kind':kind,'locator':e.get('provenance',{}).get('locator'),'record':e})
pdfs={r['observationId']:PdfReader(r['path']) for r in recovery if r.get('mediaType')=='application/pdf' and r.get('status')=='RETRIEVED_CURRENT_PUBLIC_COPY'}
def page_text(name,page):return ' '.join((pdfs[name].pages[page-1].extract_text(extraction_mode='layout') or '').split())
def norm(text):return ''.join(text.casefold().split())
samples=[]
def sample(record_id,name,pages,criterion,tokens,status='VERIFIED_SELECTED_CLAIM',defect=None):
 e=entities[record_id];assert e['data']['csoiRecord']['data']['sourceId']==observed[next(o['intakeRecord']['id'] for o in obs if o.get('id')==name and o.get('intakeRecord'))]['intakeRecord']['id']
 text=' '.join(page_text(name,p) for p in pages);assert all(norm(t) in norm(text) for t in tokens),(record_id,tokens)
 samples.append({'recordId':record_id,'sourceId':e['data']['csoiRecord']['data']['sourceId'],'sourceObservationId':name,'pdfPages':pages,'claimReviewed':criterion,'verification':status,'defect':defect,'pageContentDigests':['sha256:'+hashlib.sha256(page_text(name,p).encode()).hexdigest() for p in pages],'limits':'Only stated bounded observation checked; not current law, full-page/full-document completeness, actual performance or authority admission.'})
note_specs={
 'smrc-csp-full-2025':[('carbon-p30',[30],'Published29.9per-capita baseline;2021-22source;desireddecrease',['29.9','2021-22','CO2e emissions per capita']),('goal61',[22],'Environmentalstrategy6.1contextexists;doesnotproveimplementation',['6.1','Monitor environmental assets'])],
 'smrc-op-2026':[('food-program-p27',[27],'Publishedfoodplanning168/84/84,98%annualpremisestarget,CSP6.1',['168','84','98%','6.1']),('ltw-complaints-p30',[30],'LTWcomplaintsrowexplicitCSP6.1and8.2;planningnotactual',['LTW complaints','6.1','8.2','72 hours'])],
 'smrc-resourcing-2026':[('cover',[1],'Cover2025-2029horizon;directory2026revisionnotcurrentlegaldetermination',['RESOURCING STRATEGY','2025','2029'])],
 'smrc-ltfp-2026':[('cover',[1],'Cover2026-2036financialplan;notactualspend',['LONG TERM FINANCIAL PLAN','2026','2036'])],
 'smrc-lsps-2020':[('title-adoption',[1],'Cover2020adopted21May2020;notcurrentparcelcontrol',['2020','21 May 2020'])],
 'smrc-dp-2026':[('phe-csp61-p31',[31],'PHEregulationrowexplicitCSP6.1and2025-2029period',['6.1','2025','2029','Regulation of public health'])],
 'nsw-ltw-guidelines':[('classification',[34,36,37],'A/B/C/Sdistinctions;nospecificapproval',['Concurrence Classification A','Concurrence Classification B','Concurrence Classification C','Concurrence Classification S'])],
 'smrc-dcp-bombala-2014':[('opening-scope-amendment',[1,4,5],'2012Amendment2identityandlisted-zonehistoricalscope',['2012','Amendment 2','RU1','SP3'])],
 'smrc-dcp-cooma-2014-amend4':[('opening-scope-version-conflict',[1,2,11,12],'CoomaAmendment4identity,formerlyareawordingandprecedenceconflicts',['Amendment 4','362/19','58/22','1.5'])],
 'smrc-dcp-snowy-2013-amend3':[('amendment-and-historical-scope',[2,16,17],'Amendment3/58-23,scopeT2exception,LEPprecedence',['Amendment 3','58/23','Tyrolean','LEP prevails'])]
}
for name,items in note_specs.items():
 for suffix,pages,claim,tokens in items:sample('csoi:source-note:'+name+':'+suffix,name,pages,claim,tokens)
sample('csoi:source-note:smrc-water-amp-2025:revision-and-network-scope','smrc-water-amp-2025',[1,3,13,14],'Horizon/adoptionfactsagree;registeredAssetsbyLocationlocatorPDF14iswrong;actualTable4PDF13',['2025','2035','142/25','Table 4','Table 5'],'PARTIAL_LOCATOR_ERROR','data/provenance locator listsPDF14; actualAssetsbyLocationTable4isPDF13. SourceTOCalsomisnumbersit14.')
for suffix,tokens in [('programme',['Undertake food inspection program']),('optimal',['168']),('funded',['84']),('target',['84']),('service-kpi',['98%'])]:sample('csoi:published-plan:food-2026:'+suffix,'smrc-op-2026',[27],'Publishedfoodplanningrecordonly;notactualdelivery/expenditure',tokens)
for suffix,tokens in [('A1:3',['Tyrolean Village Stage 3']),('A1:5',['LEP prevails']),('C9:3:1:b:soil',['analysis of soil suitability and topography'])]:sample('csoi:dcp:snowy2013:'+suffix,'smrc-dcp-snowy-2013-amend3',[16 if suffix=='A1:3' else 17 if suffix=='A1:5' else 166],'Selectedhistoricalclausefactandconditionsmatch;currentlawUNKNOWN',tokens)
for suffix,pages,tokens in [('1:5',[12],['whole of the Cooma-Monaro local government area']),('versions:conflicts',[2],['362/19','58/22']),('7:4:2:2:soil',[159],['NATA','topography','soil composition'])]:sample('csoi:dcp:cooma2014:'+suffix,'smrc-dcp-cooma-2014-amend4',pages,'Selectedhistoricalclausefact/versionconflictmatch',tokens)
for suffix,pages,tokens in [('1:1:1',[5],['Bombala','RU1','SP3']),('3:1:5:A9:soil',[55],['soil type','permeability']),('4:5:4:A3',[85],['40 metres','top of the bank'])]:sample('csoi:dcp:bombala2012:'+suffix,'smrc-dcp-bombala-2014',pages,'Selectedhistoricalscope/evidence/distancefactmatches;A3doesnotextractthe40mquantity',tokens)
for suffix,tokens in [('potable-accommodation',['110 litres']),('potable-other',['90 litres']),('nonpotable',['40 litres'])]:sample('csoi:dcp-reference:snowy:'+suffix,'smrc-dcp-snowy-2013-amend3',[164],'HistoricalL/person/dayreferencefactonly;notactualwateruse/approveddesign',tokens)
assert collections.Counter(s['verification'] for s in samples)=={'VERIFIED_SELECTED_CLAIM':29,'PARTIAL_LOCATOR_ERROR':1}
versions={
 'smrc-csp-full-2025':'CSP2035,2025Revision;currentconsolidationnotestablished',
 'smrc-csp-summary':'CSP2035plan-on-page;separate6.1excerptreceipt;currentversionreviewPENDING',
 'smrc-dp-2026':'2026Revision;v2.4dated22Oct2026additionofpumptrack;v2.3adopted30Jun2026;workingdrafttextalsoexists(PDF3)',
 'smrc-op-2026':'2026-27;v1.3adopted30Jun2026resolution225/26;workingdrafttextalsoexists(PDF3)',
 'smrc-resourcing-2026':'2025-2029;cover/version1.0endorsed19Jun2025res142/25;directorylabels2026revision;componentrevisionsneedseparatecensus',
 'smrc-ltfp-2026':'2026-2036;v1.1dated30Jun2026/adopted26Jun2026res225/26;workingdrafttext;CSP2035/2042conflict(PDF5/6)',
 'smrc-lsps-2020':'2020,coveradopted21May2020',
 'nsw-ltw-guidelines':'2021fourthedition;publishedDPIE;knowledgeasofDec2020disclaimer(PDF2/4)',
 'smrc-annual-report-2025-retrieved':'2024-2025;v3.1dated27Nov2025organisationchartcorrection;v3.0endorsed20Nov2025res399/25(PDF2)',
 'smrc-water-amp-2025':'2025-2035;v1.0adopted19Jun2025res142/25;directory2025-2029conflict',
 'smrc-dcp-bombala-2014':'Cover2012Amendment2effective7Apr2022;directory2014;history7Apr2022(30Mar2022)conflict',
 'smrc-dcp-cooma-2014-amend4':'2014Amendment4Issue6;17Mar2022/58-22,7Apr2022;coverSnowyfooter/bodyAmendment1/362-19conflicts',
 'smrc-dcp-snowy-2013-amend3':'2013Amendment3Issue4,16Mar2023res58/23,commencement29Mar2023'
}
structures={
 'smrc-csp-full-2025':'Vision;fiveoutcomeareas;strategicobjectives/strategies,Councilroles,partners,measures/baselines/sources/trends,versionhistory;rootCSPcensusseparate',
 'smrc-csp-summary':'One-pagevision/fiveoutcomes/objectives/numberedstrategies;legacy6.1exactexcerptseparate',
 'smrc-lsps-2020':'12coreplanningpriorities,rationales,CouncilWill/actions,town/subregionplans,maps,implementation/timeframes,regional/CSP/LEPalignments',
 'smrc-dp-2026':'Portfolios/services,principalactivities/CSP/regulatorydriver,outcomes/timeframes,majorprojects/resources/budgets,servicechanges',
 'smrc-op-2026':'Serviceactions,optimal/fundedvolumes,KPI/target/frequency,CSP/regulatory/strategycolumns,resources,budgets',
 'smrc-resourcing-2026':'LTFP,workforce,strategy/policyandassetplansinclproperty/transport/openspace/water/wastewater;componentversions,servicelevels,risks,finance',
 'smrc-ltfp-2026':'Assumptions,fund-specificincome/expenditure/cash/balanceforecasts,scenario/sensitivity/risk,strategicalignment',
 'smrc-water-amp-2025':'Assetinventory/value/condition/life,servicelevels,climate-demand,lifecycle/renewal/maintenance,risks,costs,LTFPlinks,improvementplan',
 'smrc-annual-report-2025-retrieved':'Serviceperformance,DP/OPreportedprogress,projectcompletion,water/sewerageresults,statutoryreports/financials;2024-25andCSP2042context',
 'nsw-ltw-guidelines':'Concurrenceclasses,approval/enforcementsteps,policy,acceptancelimits,sector-specificpretreatment,fees,monitoring,appendices/standards',
 'smrc-dcp-snowy-2013-amend3':'PartsA-F:framework,localities,generalcontrols,residential/nonresidential/site-specificcontrols;conditions/exceptions/maps/quantitativefacts/relationships',
 'smrc-dcp-cooma-2014-amend4':'Chapters1-8andappendices:introduction/general/specific/subdivision/works/localities/non-design/notification;criteria/solutions/exceptions/quantities/maps',
 'smrc-dcp-bombala-2014':'Chapters1-5:introduction/sustainabledesign/subdivision/building/accessparking;separateperformancecriteria/solutions,scope/savings,quantities/maps'
}
omissions=[]
def omission(key,name,pdf,printed,section,description,tokens,kind='MISSING_STRUCTURED_RECORD'):
 text=page_text(name,pdf);assert all(norm(t) in norm(text) for t in tokens),(key,tokens)
 r=next(r for r in recovery if r['observationId']==name)
 omissions.append({'omissionId':key,'sourceId':r['sourceId'],'observationId':name,'pdfPage':pdf,'printedPage':printed,'originalSection':section,'omittedOrIncompleteContent':description,'status':kind,'verification':'ORIGINAL_PAGE_AND_ABSENCE_OF_CORRESPONDING_TYPED_RECORD_REVIEWED','rawDigest':r['rawDigest'],'officialUrl':r['url'],'originalPageDigest':'sha256:'+hashlib.sha256(text.encode()).hexdigest(),'notAClaimOfCurrentLegalApplicability':True})
omission('LSPS-P1-ACTIONS','smrc-lsps-2020',24,23,'PlanningPriority1:Actions1.1-1.8','Indigenousheritagestudy/developmentcontrols/heritagestrategyetcarenotrepresented;onlycovernoteexists',['Actions','1.1','1.8'])
omission('LSPS-PRIORITIES','smrc-lsps-2020',21,20,'12coreplanningpriorities','Priority-levelcensus12;typedpriorityrecordsfromthissource0;actions/mapsadditionaldenominatorUNKNOWN',['12 core planning priorities'])
omission('DP-WATER-CSP82','smrc-dp-2026',62,62,'OngoingDeliveryProgramActivities:WaterandWastewater','Potablewater/sewerageprincipalactivitiesandCSP8.2/outcomes/periodnotstructured;notcoveredbyp31PHEsummary',['8.2','Operate and maintain','2025','2029'])
omission('DP-WATER-RESOURCES','smrc-dp-2026',61,61,'WaterandWastewater:Whatwedeliver/resources','Published9.2MLdrinkingwater/day,4.1MLwastewater/day,52.5FTEandassetinventoryunextracted;publishedobservationsnotindependentlymeasuredactuals',['9.2','4.1','52.5'])
omission('OP-WATER-ACTIONS','smrc-op-2026',73,73,'PlannedWaterOperations','52.5FTE,maintenance15breaks/100km/yearcriterion,target47pa,CSP8.2/frequencynotstructured',['52.5','15','47','8.2'])
omission('OP-WATER-TESTING','smrc-op-2026',74,74,'Dailyoperationswatercompliancetestingandinspections','100%testingtarget;80%service-responseKPI;CSP8.2/12.2;frequencycolumnsnotstructured',['100%','80%','12.2'])
omission('RESOURCING-COMPONENTS','smrc-resourcing-2026',7,7,'ComponentsoftheResourcingStrategy','Bundlecomponentinventoryincludingworkforce/water/wastewaterandfinancial/lifecyclelinksunstructured;onlycovernoteexists',['Workforce','Water assets','Wastewater'])
omission('LTFP-CSP-VERSION-CONFLICT','smrc-ltfp-2026',6,3,'1.1PurposeofLong-TermFinancialPlanning','CSP2042statementconflictswithCSP2035onPDF5/printed2;currentcovernoteomitsthisconflict',['2042','1.1'])
omission('LTFP-WATER-INDEXES','smrc-ltfp-2026',20,17,'4.8Tableofindexes','Waterannual/usercharges,sewerchargesandexpenseindexesbyforecastyearunstructured;notactualspend',['4.8','Water Annual','Water User','7.2%'])
omission('AMP-STRATEGIC-LINKS','smrc-water-amp-2025',19,19,'3.1StrategicandCorporateGoals/Table7','Sourceexplicitlylinksassetplanningtogoals8and11;onlycover/version/scopeownnotecaptured',['Current Corporate Goals','8.','11.'])
omission('AMP-LOCATOR','smrc-water-amp-2025',13,13,'Table4AssetsbyLocation','ExistingnotelocatesAssetsbyLocationatPDF14(actualTable5AssetsbyType),whereTable4isPDF13',['Table 4','Assets by Location'],'WRONG_PDF_LOCATOR')
omission('ANNUAL-WATER-PROGRESS','smrc-annual-report-2025-retrieved',80,80,'ServiceareaWaterandWastewater','Published2024-25DPpotable/sewerage100%,OPactions60%,projectprogress95%/0%unstructured;CSP2042periodmustremainseparate',['100%','60%','95%','2042'])
omission('LTW-APPROVAL-STEPS','nsw-ltw-guidelines',42,17,'2.3Step1Pre-applicationconsultation','Onlyclassificationnoteexists;step-specificDA/dischargecoordinationandapprovalrequirementsnotstructured',['2.3','Pre-application consultation'])
omission('SNOWY-SUBDIVISION','smrc-dcp-snowy-2013-amend3',62,47,'C1§2.2ControlsC1.2-1/C1.2-2','Minimumlotsize-mapreferenceandconditionaldesigncontrolsoutsideA/C8/C9selectedoutlineunstructured',['C1.2-1','C1.2-2'])
omission('SNOWY-GREYWATER','smrc-dcp-snowy-2013-amend3',164,149,'PrintedC6.2-3(g)withinC9','Eco-tourist100%greywater-reusetargethasnotypedhistoricalquantitativereference;existing3ratesare110/90/40L/person/day',['grey water','100%'],'MISSING_NUMERIC_FACT_WITHIN_INDEXED_PAGE')
omission('COOMA-ENERGY','smrc-dcp-cooma-2014-amend4',31,31,'2.7.1Objectives/buildingperformance','Energy/waterefficiencycriteria/acceptable-solutionsandBASIXconditionsunstructured',['2.7.1','BASIX'])
omission('COOMA-INSTALLATION','smrc-dcp-cooma-2014-amend4',159,16,'7.4.2.4Installationoftheon-sitewastemanagementsystem','Installation/report/licensedplumberclausebetweenselected7.4.2.3and7.4.2.5notstructured',['7.4.2.4','licensed plumber'])
omission('BOMBALA-ROADS','smrc-dcp-bombala-2014',51,30,'3.1.4RoadsP1-P4/A1-A6','Roadperformancecriteriaandacceptablesolutionsomitted;adjacentcolumnsarenotautomaticallypaired',['3.1.4 Roads','P1','A6'])
omission('BOMBALA-DISTANCE-NUMBER','smrc-dcp-bombala-2014',85,64,'4.5.4A3','Existingclauseonlysaysdistance-reference;explicit40mhistoricalnumbernotretainedinquantitativerecord',['40 metres','top of the bank'],'PARTIAL_NUMERIC_EXTRACTION')
by_sample=collections.defaultdict(collections.Counter)
for s in samples:by_sample[s['sourceId']][s['verification']]+=1
by_omission=collections.defaultdict(list)
for o in omissions:by_omission[o['sourceId']].append(o)
rows=[]
for s in catalogue['sources']:
 sid=s['id'];o=observed.get(sid,{});r=recov.get(sid,{});name=o.get('id');counts=collections.Counter(x['kind'] for x in records[sid]);t=by_sample[sid];is_document=s['recordType']=='DOCUMENT';denom_reason='No complete original atomic-goal/action/measure/condition/map census; own notes/parent nodes and original units have different grains.'
 if s['recordType']!='DOCUMENT':denom_reason='DIRECTORY/REQUIREMENT is not a received original document; do not include in document-content denominator.'
 rows.append({'source_id':sid,'record_type':s['recordType'],'family':s['family'],'title':s['title'],'official_url':s['officialUrl'],'registered_raw_digest':s.get('rawDigest'),'audit_byte_receipt':'MATCH' if r.get('receiptMatch') else 'CURRENT_HTML_BYTES_DIFFER_HISTORICAL_COPY_UNAVAILABLE' if r and s.get('mediaType')=='text/html' else 'NO_ORIGINAL_RECEIPT_AT_THIS_RECORD','audit_original_path':r.get('path'),'observed_version':versions.get(name,'UNKNOWN_DYNAMIC_HTML' if r else 'UNKNOWN_REQUIREMENT_OR_LEGACY_REFERENCE'),'pdf_pages_audit':r.get('pages'),'pdf_pages_registered':s['extraction'].get('totalPages'),'original_structure_to_extract':structures.get(name,'PublicHTMLdomaincontent/conditions/exceptions/links:completeinventorynotestablished' if r else 'Notreceivedasthisrecord;specificin-forceversion/maps/sectionsunknown'),'expected_original_atomic_items_total':'UNKNOWN' if is_document else 'NOT_APPLICABLE','research_note_records':counts['research_note'],'clause_records':counts['clause'],'historical_reference_records':counts['historical_reference'],'published_plan_records':counts['published_plan'],'actual_governed_record_total':sum(counts.values()),'verified_selected_claim_samples_coverage_subtask':t['VERIFIED_SELECTED_CLAIM'],'partial_selected_claim_samples_coverage_subtask':t['PARTIAL_LOCATOR_ERROR'],'existing_records_outside_initial_coverage_subtask_sample':sum(counts.values())-sum(t.values()),'omitted_or_incomplete_original_items_total':'UNKNOWN' if is_document else 'NOT_APPLICABLE','missing_or_incomplete_examples':'; '.join(x['omissionId']+':PDF'+str(x['pdfPage'])+'/'+x['originalSection'] for x in by_omission[sid]),'full_document_knowledge_coverage':'UNKNOWN' if is_document else 'NOT_APPLICABLE','subset_scope':'LSPS12coreplanningprioritiesonly' if name=='smrc-lsps-2020' else 'NOT_CENSUSED','subset_original_total':12 if name=='smrc-lsps-2020' else None,'subset_structured_units':0 if name=='smrc-lsps-2020' else None,'subset_coverage':0.0 if name=='smrc-lsps-2020' else None,'legacy_exact_excerpt_separately_verified':1 if name=='smrc-csp-summary' else 0,'coverage_unknown_reason':denom_reason,'source_current_version_review':s.get('currentAsOf') or 'UNKNOWN','legal_or_authorised_admission':'PENDING_NOT_GRANTED','rights_status':s['rights']['status']})
# Same-document aliases must not be counted as two missing physical originals.
source_by_id={s['id']:s for s in catalogue['sources']};received_by_url={r['url']:r for r in recovery}
combined_status={s['recordId']:('VERIFIED_BOUNDED' if s['verification']=='VERIFIED_SELECTED_CLAIM' else 'PARTIAL') for s in samples}
clause_review=json.loads((ROOT/'clause-semantics/all-72-dcp-semantic-audit.json').read_text())
for item in clause_review['items']:combined_status[item['recordId']]=item['status']
combined_status['csoi:dcp-reference:snowy:potable-accommodation']='PARTIAL'
for row in rows:
 resolved=received_by_url.get(row['official_url']);alias=row['record_type']=='DOCUMENT' and not row['registered_raw_digest'] and resolved is not None
 row['resolved_receipted_source_id']=resolved['sourceId'] if resolved else None
 row['physical_document_key']=resolved['sourceId'] if row['record_type']=='DOCUMENT' and resolved else None
 row['duplicate_legacy_alias']=alias
 row['duplicate_alias_note']='Legacyplaceholderalias;receivedoriginalexistsunderresolvedsourceID.DonotcountasanadditionalphysicaldocumentoradditionalmissingPDF.' if alias else ''
 if alias:
  row['audit_byte_receipt']='MATCHED_PHYSICAL_ORIGINAL_VIA_RECEIPTED_ALIAS';row['pdf_pages_audit']=resolved.get('pages');row['observed_version']=versions.get(resolved['observationId']);row['original_structure_to_extract']=structures.get(resolved['observationId']);row['coverage_unknown_reason']='LegacyaliasofreceivedphysicalPDF;contentdenominatorandactualrecordsreportedonresolvedsourceID,notdoublecounted.'
 st=collections.Counter(combined_status.get(x['id'],'NOT_VERIFIED') for x in records[row['source_id']])
 row['bounded_correct_records_combined_audit']=st['VERIFIED_BOUNDED'];row['partial_records_combined_audit']=st['PARTIAL'];row['wrong_records_combined_audit']=st['WRONG'];row['not_verified_records_combined_audit']=st['NOT_VERIFIED'];row['combined_correctness_basis']='Full72DCPbounded-clauseauditplusselected13PDFnotes/fiveOPplans/threehistoricalnumericreferences;110minimumoperatorretainedasPARTIAL;currentlaw/whole-filecompletenessnotestablished.'
 if not alias and row['source_id']=='csoi:smrc-csp-summary:20261030':
  row['subset_scope']='44numberedstrategies:exactoriginalexcerptcoverageONLY,notfull-fieldcapsules';row['subset_original_total']=44;row['subset_structured_units']=1;row['subset_coverage']=1/44
 if not alias and row['source_id']=='csoi:smrc-csp-full-2025:20261030':
  row['subset_scope']='63publishedbaselinemetricrows:onelegacyattributedstructuredrow,notraw-recomputedorsource-admitted';row['subset_original_total']=63;row['subset_structured_units']=1;row['subset_coverage']=1/63
 row['csp_fullfield_strategy_capsules']='0/44' if not alias and row['source_id']=='csoi:smrc-csp-full-2025:20261030' else 'NOT_APPLICABLE'

assert len(rows)==52 and sum(r['actual_governed_record_total'] for r in rows)==105
assert sum(r['bounded_correct_records_combined_audit'] for r in rows)==89
assert sum(r['partial_records_combined_audit'] for r in rows)==3
assert sum(r['wrong_records_combined_audit'] for r in rows)==1
assert sum(r['not_verified_records_combined_audit'] for r in rows)==12
assert sum(r['verified_selected_claim_samples_coverage_subtask'] for r in rows)==29
def write_csv(name,data):
 with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
for name,value in [('source-coverage-matrix.json',rows),('original-omissions.json',omissions),('semantic-samples.json',samples)]:
 (OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
write_csv('source-coverage-matrix.csv',rows);write_csv('original-omissions.csv',omissions);write_csv('semantic-samples.csv',samples)
spec=importlib.util.spec_from_file_location('anchors',APP/'tools/verify-document-anchors.py');anchors=importlib.util.module_from_spec(spec);spec.loader.exec_module(anchors)
anchor_results=[]
for name,obsid in [('snowy','smrc-dcp-snowy-2013-amend3'),('cooma','smrc-dcp-cooma-2014-amend4'),('bombala','smrc-dcp-bombala-2014')]:
 manifest=json.loads((APP/('sources/'+name+'-dcp-outline-anchors.json')).read_text());anchor_results.append(anchors.verify(ROOT/('originals/'+obsid+'.pdf'),manifest))
(OUT/'independent-dcp-anchor-results.json').write_text(json.dumps(anchor_results,indent=2)+'\n')
summary={'auditHead':'744ab46b2bec2ad601da0c4ae528694a4c982154','recordTypes':dict(collections.Counter(s['recordType'] for s in catalogue['sources'])),'verifiedOriginalPdfCopies':13,'currentHtmlCopies':20,'currentHtmlByteMatches':sum(r.get('receiptMatch',False) for r in recovery if r.get('mediaType')=='text/html'),'receivedPdfsMissingRegisteredPageCount':sum(r['pdf_pages_audit'] is not None and r['pdf_pages_registered'] is None and not r['duplicate_legacy_alias'] for r in rows),'governedSourceRecords':105,'ownResearchNotes':25,'authoredDcpObservations':72,'historicalDesignReferences':3,'publishedPlanningRecords':5,'verifiedSelectedClaimSamples':29,'combinedBoundedCorrectRecords':89,'combinedPartialRecords':3,'combinedWrongRecords':1,'combinedNotSemanticallyVerified':12,'duplicateLegacyDocumentAliases':2,'partialLocatorErrorExistingRecords':1,'outsideInitialCoverageSubtaskSample':75,'independentDcpPageAnchors':sum(len(r['anchors']) for r in anchor_results),'exactOriginalOmissionOrPartialExamples':len(omissions),'fullDocumentCoverageDenominator':'UNKNOWN','regionalStrategyStandaloneDocuments':0,'retrievedLEPorSEPPStatutoryDocuments':0,'rawPagesOrBodiesRedistributable':False,'importantLimits':['40DCPpagehashesarenot72semanticproofs','29verifiedsampleclaimsarenotfull105recordsemanticacceptance','105ownstructuredrecordsarenot105originalatomicitems','20HTMLbytemismatchesdonotprove20semanticchanges','Currentversion/parcel/legal/authoritynotgranted','CSProotcensusandlegacy6.1excerptareseparatefromthese29governedsamples']}
(OUT/'coverage-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,ensure_ascii=False))
