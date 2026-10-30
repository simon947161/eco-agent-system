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
 return result;
}
function coverage(catalogue,observations){const coverage=I.coverage(catalogue),unavailableStatutoryReferences=catalogue.sources.filter(s=>s.publisher==='NSW legislation website — content not retrieved').length;return {...coverage,registeredDocumentRevisionDenominator:coverage.documentDenominator,uniqueRegisteredUrls:new Set(catalogue.sources.filter(s=>s.officialUrl).map(s=>s.officialUrl)).size,coreObservedUrlDenominator:observations.coverage.observedUrlDenominator,unavailableStatutoryReferences,totalAttemptedUrls:observations.coverage.observedUrlDenominator+unavailableStatutoryReferences,freshHttp200:observations.coverage.http200,freshByteVerified:observations.coverage.byteVerified,authoredResearchSummarySources:observations.coverage.researchSummarySourceCount,sourceExtractionAdmitted:0,rightsApproved:0,currentLegalVersionConfirmed:0,note:'Document revisions, registered URL leads, successful receipts, research notes, source extraction and official admission are separate measures.'};}
root.CsoiIntake={extendCatalogue,registerSummaries,coverage};if(typeof module!=='undefined')module.exports=root.CsoiIntake;
})(typeof window!=='undefined'?window:globalThis);
