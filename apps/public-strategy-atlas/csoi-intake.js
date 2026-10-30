/* An append-only version of the existing source register, never a second graph. */
(function(root){
'use strict';
const M=typeof module!=='undefined'?require('./atlas-model.js'):root.AtlasModel,I=typeof module!=='undefined'?require('./atlas-intake.js'):root.AtlasIntake,G=typeof module!=='undefined'?require('./csoi-governance.js'):root.AtlasCSOIGovernance;
async function extendCatalogue(base,observations,unavailableReferences=[]){
 if(!await I.verifyCatalogue(base)||observations?.format!=='csoi-public-source-observations-1'||observations.originalBytesCommitted!==false)throw Error('CSOI_SOURCE_OBSERVATIONS_REQUIRED');
 let catalogue=base;
 for(const observation of observations.observations){
  if(observation.httpStatus!==200||observation.byteVerification!=='PASS_TESTED_HERE')continue;
  const record=structuredClone(observation.intakeRecord);if(I.recordIssues(record).length)throw Error('CSOI_SOURCE_RECORD_INVALID');
  if(observation.family.endsWith('_DIRECTORY'))record.recordType='DIRECTORY';
  record.lineage.supersedes=base.sources.filter(s=>s.officialUrl===record.officialUrl).map(s=>s.id);
  if(catalogue.sources.some(s=>s.id===record.id))throw Error('CSOI_SOURCE_ID_CONFLICT');
  catalogue=await I.registerSource(catalogue,record,{registeredAt:observation.retrievedAt,actor:'public-source-research',reason:'Append actual public-source observation; rights, legal currency and human admission remain pending.'});
  for(const stage of ['DIRECTORY_OBSERVED','SOURCE_RETRIEVED','RAW_BYTES_VERIFIED'])catalogue=await I.appendStage(catalogue,record.id,stage,{...observation.stageEvidence[stage],actor:'public-source-research',at:observation.retrievedAt,reason:'Executed HTTPS retrieval and original-byte digest evidence; no extraction/admission permission inferred.'});
 }
 for(const reference of unavailableReferences){
  if(reference.access!=='UNAVAILABLE')throw Error('CSOI_UNAVAILABLE_REFERENCE_REQUIRED');
  const record=structuredClone(base.sources[0]);delete record.revisionId;
  Object.assign(record,{id:'csoi:'+reference.id+':20261030',family:reference.family,publisher:'NSW legislation website — content not retrieved',officialUrl:reference.url,directoryUrl:reference.url,title:reference.id+' — statutory reference pending retrieval',recordType:'REQUIREMENT',mediaType:'UNKNOWN',rawDigest:null,retrievedAt:null,adoptedAt:null,effectiveFrom:null,effectiveTo:null,currentAsOf:null,geographicExtent:{type:'STATE',label:'NSW, Australia',parcelApplicability:'UNKNOWN'},extraction:{coverage:'NONE',anchors:[]},lineage:{supersedes:[],revisionLabel:'UNKNOWN'},corroboratingEvidence:[],access:{state:'UNAVAILABLE',checkedAt:reference.retrievedAt,reason:'HTTP response 403; statutory content, current consolidation and applicability remain unverified.'}});
  catalogue=await I.registerSource(catalogue,record,{registeredAt:reference.retrievedAt,actor:'public-source-research',reason:'Register failed official reference as a requirement, not a retrieved/admitted statutory document.'});
 }
 return catalogue;
}
async function registerSummaries(dataset,observations){
 let result=dataset;
 for(const observation of observations.observations.filter(o=>o.httpStatus===200))for(const anchor of observation.knowledgeAnchors||[]){
  const id='csoi:source-note:'+observation.id+':'+anchor.id;
  if(M.domainIndex(result).has(id))continue;
  if(anchor.textKind!=='RESEARCH_SUMMARY'||await M.digest(new TextEncoder().encode(anchor.text))!==anchor.digest)throw Error('CSOI_RESEARCH_SUMMARY_DIGEST');
  const record=await G.makeRecord({id,ownerModule:'CSOI_OPERATIONS',security:'PUBLIC',layer:'L0',sourceClass:'INDEPENDENT_RESEARCH',judgment:'OBSERVATION',authority:'INDEPENDENT_RESEARCH',scope:{region:observation.intakeRecord.geographicExtent.label,boundary:'PUBLIC_DOCUMENT_RESEARCH_NOT_LEGAL_APPLICABILITY',period:{from:observation.retrievedAt.slice(0,10),to:observation.retrievedAt.slice(0,10)}},inputs:[],data:{title:anchor.title,summary:anchor.text,sourceId:observation.intakeRecord.id,sourceDigest:observation.rawDigest,locator:anchor.locator,verification:anchor.verification,uncertainty:anchor.uncertainty,officialRelationship:'PENDING'},sensitivity:{personalData:false,confidential:false,reidentifiable:false},provenance:{contentMode:'RESEARCH_SUMMARY',url:observation.url,locator:anchor.locator,sourceRevision:observation.rawDigest,rights:{mode:'AUTHORED_RESEARCH',basis:'Repository-authored bounded factual research summary only. Underlying source reuse rights UNKNOWN; no original body, page image or full extracted text is redistributed.'}},observedAt:observation.retrievedAt});
  result=await M.registerResearchRecord(result,{record,kind:'ContentBlock',label:observation.title+' — '+anchor.title,stationId:observation.intakeRecord.stationId,reason:'Append bounded attributed public research note, not admitted official source extraction or Council approval.'});
  const targets=observation.id==='smrc-op-2026'&&anchor.id==='food-program-p27'?['csp6']:observation.id==='smrc-op-2026'&&anchor.id==='ltw-complaints-p30'?['csp6','csp8']:[];
  for(const to of targets)if(M.domainIndex(result).has(to))result=await M.registerResearchLink(result,{id:'csoi:reported-reference:'+anchor.id+':'+to,from:id,to,reason:'Retain exact OP table CSP Link reference as a research candidate only; no automatic official admission.'});
 }
 result=await registerPlanningFacts(result,observations);
 const outline=typeof module!=='undefined'?require('./sources/snowy-dcp-outline.json'):root.CsoiDcpOutline,clauses=typeof module!=='undefined'?require('./csoi-clauses.js'):root.AtlasCSOIClauses;
 if(outline&&result.domain.sourceCatalogue.sources.some(s=>s.id===outline.sourceId)){
  if(!clauses||outline.format!=='csoi-public-dcp-outline-1'||outline.originalBytesCommitted!==false)throw Error('DCP_OUTLINE_REQUIRED');
  result=await clauses.registerOutline(result,{sourceId:outline.sourceId,sourceRevision:outline.sourceRevision,nodes:outline.nodes});
  result=await registerReferenceMeasurements(result,outline);
 }
 return result;
}
async function registerReferenceMeasurements(dataset,outline){
 let result=dataset;const source=result.domain.sourceCatalogue.sources.find(s=>s.id===outline.sourceId);
 for(const reference of outline.referenceMeasurements){if(M.domainIndex(result).has(reference.id))continue;
  if(Object.keys(reference).some(k=>!['id','clauseId','value','unit','role','label'].includes(k))||!Number.isFinite(reference.value)||reference.value<0||reference.unit!=='L/person/day')throw Error('DCP_REFERENCE_MEASUREMENT_INVALID');
  const clause=M.domainIndex(result).get(reference.clauseId),data=clause?.data?.csoiRecord?.data;
  if(!data?.dcpClause||data.sourceId!==source.id||data.sourceDigest!==source.rawDigest)throw Error('DCP_REFERENCE_CLAUSE_PIN');
  const scope={region:source.geographicExtent.label,boundary:'HISTORICAL_DOCUMENT_REFERENCE_NOT_ACTUAL_OR_CURRENT_LAW',period:{from:source.retrievedAt.slice(0,10),to:source.retrievedAt.slice(0,10)}},measurement={value:reference.value,unit:reference.unit,role:reference.role,meaning:'HISTORICAL_DESIGN_REFERENCE_NOT_ACTUAL_OUTPUT_OR_CURRENT_OBLIGATION',area:scope.region,boundary:scope.boundary,period:scope.period,quantityNature:'REFERENCE_RATE',eligibleDenominator:'UNKNOWN'};
  const record=await G.makeRecord({id:reference.id,ownerModule:'CSOI_OPERATIONS',security:'PUBLIC',layer:'L0',sourceClass:'INDEPENDENT_RESEARCH',judgment:'OBSERVATION',authority:'INDEPENDENT_RESEARCH',scope,inputs:[{id:source.id,revisionId:source.revisionId},{id:clause.id,revisionId:clause.revisionId}],data:{title:reference.label,summary:'Own observation of a historical document design rate, not actual demand, delivery, spend or a verified current duty. Source admission, actual population and outcome remain UNKNOWN/PENDING.',sourceId:source.id,sourceDigest:source.rawDigest,sourceClauseId:clause.id,measurement,actualDemand:'UNKNOWN',actualSpend:'UNKNOWN',actualOutcome:'UNKNOWN',legalApplicability:'UNKNOWN'},sensitivity:{personalData:false,confidential:false,reidentifiable:false},provenance:{contentMode:'RESEARCH_SUMMARY',url:source.officialUrl,locator:data.locator,sourceRevision:source.rawDigest,rights:{mode:'AUTHORED_RESEARCH',basis:'Bounded authored observation of numeric facts only. Original source reuse rights/current applicability/admission remain UNKNOWN/PENDING.'}},observedAt:source.retrievedAt});
  result=await M.registerResearchRecord(result,{record,kind:'QuantifiedObservation',label:reference.label,stationId:'dcp',reason:'Retain independently traceable historical design reference; no operational calculation, current legal duty or actual result admitted.'});
 }
 return result;
}
async function registerPlanningFacts(dataset,observations){
 const observation=observations.observations.find(o=>o.id==='smrc-op-2026'),anchor=observation?.knowledgeAnchors.find(a=>a.id==='food-program-p27');
 if(observation?.rawDigest!=='sha256:4e0b6440768c6bb902628ec36e43757366be470f583169834a4c7c3d4cf54fd2'||anchor?.digest!=='sha256:56b908ad5ad5ba88557be46cc06ddcbaf9d614bd7429916f712c297b069700a3')return dataset;
 const source=dataset.domain.sourceCatalogue.sources.find(s=>s.id===observation.intakeRecord.id);let result=dataset;
 const definitions=[['programme','WorkPackage','Published food inspection programme — planned only',null],['optimal','QuantifiedObservation','OP optimal volume — units unverified',{value:168,unit:'UNKNOWN',role:'OPTIMAL_VOLUME'}],['funded','QuantifiedObservation','OP funded volume — not money or actual spend',{value:84,unit:'UNKNOWN',role:'FUNDED_VOLUME'}],['target','QuantifiedObservation','OP target volume — not completed work',{value:84,unit:'UNKNOWN',role:'TARGET_VOLUME'}],['service-kpi','QuantifiedObservation','Published service target — not actual coverage',{value:98,unit:'percent',role:'SERVICE_KPI_TARGET'}]];
 for(const [suffix,kind,title,quantity]of definitions){const id='csoi:published-plan:food-2026:'+suffix;if(M.domainIndex(result).has(id))continue;const scope={region:'Snowy Monaro, NSW, Australia',boundary:'PUBLISHED_OP_PLANNING_ROW_NOT_ACTUAL_OUTPUT_OR_LEGAL_APPLICABILITY',period:{from:'2026-07-01',to:'2027-06-30'}},data={title,domain:'food',sourceId:source.id,summary:'Attributed research observation of the OP page27 planning row. Funded volume is not expenditure; actual inspections, eligible population, outcome and official applicability remain UNKNOWN.',tableCaption:'Planned – Public Health and Environment',locator:anchor.locator,fiscalBasis:'OP2026–27 planning period; adoption/currentness requires review',footnotes:['Planning volume units have not been independently resolved.','98% refers to the published annual P1/P2/P3 premises target; the actual eligible denominator and performance are UNKNOWN.'],actualOutput:'UNKNOWN',actualSpend:'UNKNOWN',actualOutcome:'UNKNOWN',responsibleRole:'UNKNOWN'};if(quantity)data.measurement={...quantity,period:scope.period,area:scope.region,boundary:scope.boundary,meaning:'PUBLISHED_PLAN_NOT_ACTUAL',eligibleDenominator:'UNKNOWN'};
  const record=await G.makeRecord({id,ownerModule:'CSOI_OPERATIONS',security:'PUBLIC',layer:'L0',sourceClass:'INDEPENDENT_RESEARCH',judgment:'OBSERVATION',authority:'INDEPENDENT_RESEARCH',scope,inputs:[{id:source.id,revisionId:source.revisionId}],data,sensitivity:{personalData:false,confidential:false,reidentifiable:false},provenance:{contentMode:'RESEARCH_SUMMARY',url:source.officialUrl,locator:anchor.locator,sourceRevision:source.rawDigest,rights:{mode:'AUTHORED_RESEARCH',basis:'Bounded authored observations of published numeric facts. Original source redistribution rights and admission remain UNKNOWN/PENDING.'}},observedAt:observation.retrievedAt});
  result=await M.registerResearchRecord(result,{record,kind,label:title,stationId:'csp6',reason:'Preserve source-pinned published planning quantities without inventing units, actual work or money.'});result=await M.registerResearchLink(result,{id:'csoi:published-plan-link:'+suffix,from:id,to:suffix==='programme'?'csp6':'csoi:published-plan:food-2026:programme',reason:'Research candidate from the same published OP table; official linkage remains pending review.'});
 }
 return result;
}
function coverage(catalogue,observations){const coverage=I.coverage(catalogue),unavailableStatutoryReferences=catalogue.sources.filter(s=>s.publisher==='NSW legislation website — content not retrieved').length;return {...coverage,registeredDocumentRevisionDenominator:coverage.documentDenominator,registeredRecords:catalogue.sources.length,unresolvedRequirementRecords:catalogue.sources.filter(s=>s.recordType==='REQUIREMENT').length,uniqueRegisteredUrls:new Set(catalogue.sources.filter(s=>s.officialUrl).map(s=>s.officialUrl)).size,coreRequestAttempts:observations.observations.length,distinctCoreAttemptedUrls:new Set(observations.observations.map(o=>o.url)).size,unavailableStatutoryReferences,totalRequestAttempts:observations.observations.length+unavailableStatutoryReferences,distinctAttemptedUrls:new Set([...observations.observations.map(o=>o.url),...catalogue.sources.filter(s=>s.publisher==='NSW legislation website — content not retrieved').map(s=>s.officialUrl)]).size,freshHttp200:observations.coverage.http200,freshByteVerified:observations.coverage.byteVerified,authoredResearchSummarySources:observations.coverage.researchSummarySourceCount,sourceExtractionAdmitted:0,rightsApproved:0,currentLegalVersionConfirmed:0,note:'Document revisions, registered URL leads, successful receipts, research notes, source extraction and official admission are separate measures.'};}
root.CsoiIntake={extendCatalogue,registerSummaries,coverage};if(typeof module!=='undefined')module.exports=root.CsoiIntake;
})(typeof window!=='undefined'?window:globalThis);
