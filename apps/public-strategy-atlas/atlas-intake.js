/* Source intake is an auditable register, not an additional strategy graph. */
(function(root){
'use strict';
const M=typeof module!=='undefined'?require('./atlas-model.js'):root.AtlasModel;
const FORMAT='atlas-source-catalogue-1';
const STAGES=Object.freeze(['DISCOVERED','DIRECTORY_OBSERVED','SOURCE_RETRIEVED','RAW_BYTES_VERIFIED','EXTRACTED','ANCHOR_VERIFIED','CURRENT_VERSION_AND_SCOPE_CHECKED','REVIEW_PENDING','ADMITTED']);
const USES=new Set(['METADATA_ONLY','SHORT_EXCERPT','FULL_TEXT']);
const hash=v=>typeof v==='string'&&/^sha256:[a-f0-9]{64}$/.test(v);
const objectHash=v=>'sha256:'+M.sha256(new TextEncoder().encode(M.canonical(v)));
const textHash=v=>'sha256:'+M.sha256(new TextEncoder().encode(v));
const date=v=>typeof v==='string'&&/^\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|\+00:00))?$/.test(v)&&Number.isFinite(Date.parse(v))&&new Date(v).toISOString().slice(0,10)===v.slice(0,10);
function requireThat(v,message){if(!v)throw Error(message);}
function safeUrl(url){try{const parsed=new URL(url);return parsed.protocol==='https:'&&!parsed.username&&!parsed.password;}catch{return false;}}
function freeze(value){if(value&&typeof value==='object'){for(const child of Object.values(value))freeze(child);Object.freeze(value);}return value;}
function recordIssues(record){
 const issues=[];
 if(!record||typeof record!=='object'||Array.isArray(record))return ['SOURCE_OBJECT_REQUIRED'];
 for(const field of ['id','family','publisher','title','recordType','mediaType','classification'])if(typeof record[field]!=='string'||!record[field])issues.push('SOURCE_FIELD:'+field);
 if(!['DOCUMENT','DIRECTORY','REQUIREMENT'].includes(record.recordType))issues.push('RECORD_TYPE');
 if(record.officialUrl!==null&&!safeUrl(record.officialUrl))issues.push('UNSAFE_SOURCE_URL');
 if(record.directoryUrl!==null&&!safeUrl(record.directoryUrl))issues.push('UNSAFE_DIRECTORY_URL');
 if(record.recordType==='DOCUMENT'&&!safeUrl(record.officialUrl))issues.push('DOCUMENT_URL_REQUIRED');
 if(typeof record.stationId!=='string'||!record.stationId||!record.access||!['BLOCKED_BY_PERMISSION','NOT_CHECKED','AVAILABLE','UNAVAILABLE','LOST'].includes(record.access.state))issues.push('SOURCE_ACCESS_OR_STATION');
 if(record.classification!=='PUBLIC'&&record.classification!=='SYNTHETIC')issues.push('PUBLIC_ONLY');
 if(!record.rights||!['UNKNOWN','METADATA_AND_SHORT_EXCERPTS','LICENCED','SYNTHETIC_AUTHORED'].includes(record.rights.status)||!Array.isArray(record.rights.permittedUses)||record.rights.permittedUses.some(use=>!USES.has(use)))issues.push('RIGHTS_REQUIRED');
 if(record.rights?.permittedUses?.includes('FULL_TEXT')&&!['LICENCED','SYNTHETIC_AUTHORED'].includes(record.rights.status))issues.push('FULL_TEXT_RIGHTS_REQUIRED');
 for(const field of ['retrievedAt','adoptedAt','effectiveFrom','effectiveTo','amendedAt','supersededAt','currentAsOf'])if(record[field]!==null&&!date(record[field]))issues.push('SOURCE_DATE:'+field);
 if(record.rawDigest!==null&&!hash(record.rawDigest))issues.push('SOURCE_DIGEST');
 if(!record.geographicExtent||typeof record.geographicExtent.label!=='string')issues.push('GEOGRAPHY_REQUIRED');
 if(!record.lineage||!Array.isArray(record.lineage.supersedes)||!Array.isArray(record.corroboratingEvidence))issues.push('LINEAGE_REQUIRED');
 if(!record.extraction||!['NONE','PARTIAL','FULL','UNKNOWN'].includes(record.extraction.coverage)||!Array.isArray(record.extraction.anchors))issues.push('EXTRACTION_REQUIRED');
 for(const anchor of record.extraction?.anchors||[]){
  if(!anchor.id||!anchor.locator||!['SOURCE_EXCERPT','RESEARCH_SUMMARY','SYNTHETIC'].includes(anchor.textKind)||typeof anchor.text!=='string'||anchor.text.length>1000)issues.push('ANCHOR_FIELDS');
  if(anchor.textKind==='SOURCE_EXCERPT'&&!record.rights?.permittedUses?.includes('SHORT_EXCERPT')&&!record.rights?.permittedUses?.includes('FULL_TEXT'))issues.push('EXCERPT_RIGHTS_REQUIRED');
  if(anchor.textKind==='SYNTHETIC'&&record.classification!=='SYNTHETIC')issues.push('SYNTHETIC_SOURCE_REQUIRED');
  if(anchor.textKind!=='SYNTHETIC'&&record.classification==='SYNTHETIC')issues.push('SYNTHETIC_CLASSIFICATION');
  if(anchor.digest!==null&&(!hash(anchor.digest)||anchor.digest!==textHash(anchor.text)))issues.push('ANCHOR_DIGEST');
 }
 return issues;
}
async function createCatalogue(records,{registeredAt,actor='local-researcher'}={}){
 requireThat(Array.isArray(records)&&records.length<=10000,'SOURCE_LIMIT');requireThat(date(registeredAt),'REGISTERED_AT_REQUIRED');
 const ids=new Set();const sources=[];
 for(const record of records){const errors=recordIssues(record);requireThat(!errors.length,errors.join(';'));requireThat(!ids.has(record.id),'DUPLICATE_SOURCE');ids.add(record.id);sources.push({...structuredClone(record),revisionId:await M.objectDigest(record)});}
 let result={format:FORMAT,algorithmVersion:'atlas-source-intake-1',sources,events:[]};
 for(const record of sources)result=await appendStage(result,record.id,'DISCOVERED',{actor,at:registeredAt,reason:'Registered source requirement or public research metadata; no admission implied.'});
 return freeze(result);
}
async function registerSource(catalogue,record,{registeredAt,actor='local-researcher',reason='Register a newly identified document revision'}={}){
 requireThat(await verifyCatalogue(catalogue),'INVALID_CATALOGUE');requireThat(date(registeredAt)&&reason,'REGISTERED_AT_REQUIRED');
 const errors=recordIssues(record);requireThat(!errors.length,errors.join(';'));requireThat(!catalogue.sources.some(s=>s.id===record.id),'DUPLICATE_SOURCE');requireThat(record.lineage.supersedes.every(id=>catalogue.sources.some(s=>s.id===id)),'SOURCE_LINEAGE');
 const source={...structuredClone(record),revisionId:await M.objectDigest(record)},next={...catalogue,sources:[...catalogue.sources,source]};
 return appendStage(next,source.id,'DISCOVERED',{actor,at:registeredAt,reason});
}
function replay(catalogue){
 const state=new Map(catalogue.sources.map(source=>[source.id,{stage:null,evidence:{},corrections:[]}])) ;
 for(const event of catalogue.events){const current=state.get(event.sourceId);if(event.operation==='CORRECTION'){current.corrections.push(event);current.stage=event.stage;if(STAGES.indexOf(event.stage)<STAGES.indexOf('SOURCE_RETRIEVED')&&current.evidence.SOURCE_RETRIEVED)current.retrievalWithdrawal={at:event.evidence.at};for(const stage of STAGES.slice(STAGES.indexOf(event.stage)+1))delete current.evidence[stage];}else{current.stage=event.stage;current.evidence[event.stage]=event.evidence;if(event.stage==='SOURCE_RETRIEVED')delete current.retrievalWithdrawal;}}
 return state;
}
function gate(source,stage,evidence,current){
 requireThat(STAGES.includes(stage),'INTAKE_STAGE');requireThat(evidence&&typeof evidence==='object'&&typeof evidence.actor==='string'&&evidence.actor&&date(evidence.at)&&typeof evidence.reason==='string'&&evidence.reason,'INTAKE_EVIDENCE_REQUIRED');
 requireThat(STAGES.indexOf(stage)===STAGES.indexOf(current.stage)+1,'STAGE_ORDER');
 if(stage==='DIRECTORY_OBSERVED')requireThat(safeUrl(evidence.url)&&hash(evidence.directoryDigest),'DIRECTORY_OBSERVATION_REQUIRED');
 if(stage==='SOURCE_RETRIEVED')requireThat(safeUrl(evidence.url)&&date(evidence.retrievedAt)&&Number.isInteger(evidence.byteLength)&&evidence.byteLength>0&&evidence.httpStatus===200&&hash(evidence.rawDigest),'RETRIEVAL_REQUIRED');
 if(stage==='RAW_BYTES_VERIFIED')requireThat(hash(evidence.rawDigest)&&(source.rawDigest===null||source.rawDigest===evidence.rawDigest)&&current.evidence.SOURCE_RETRIEVED?.rawDigest===evidence.rawDigest,'RAW_DIGEST_MISMATCH');
 if(stage==='EXTRACTED')requireThat(source.classification==='SYNTHETIC'||source.rights.permittedUses.includes('SHORT_EXCERPT')||source.rights.permittedUses.includes('FULL_TEXT'),'EXTRACTION_RIGHTS_PENDING');
 if(stage==='EXTRACTED')requireThat(typeof evidence.parserVersion==='string'&&evidence.parserVersion&&evidence.extractionDigest===objectHash(source.extraction.anchors)&&['PARTIAL','FULL'].includes(evidence.coverage),'EXTRACTION_EVIDENCE_REQUIRED');
 if(stage==='ANCHOR_VERIFIED')requireThat(source.extraction.anchors.length>0&&Array.isArray(evidence.anchorIds)&&evidence.anchorIds.length>0&&evidence.anchorIds.every(id=>source.extraction.anchors.some(anchor=>anchor.id===id&&anchor.digest===textHash(anchor.text)))&&evidence.method&&evidence.uncertainty,'ANCHOR_REVIEW_REQUIRED');
 if(stage==='CURRENT_VERSION_AND_SCOPE_CHECKED')requireThat(date(evidence.currentAsOf)&&evidence.versionConfirmed===true&&evidence.scopeConfirmed===true&&safeUrl(evidence.corroboratingUrl)&&source.currentAsOf===evidence.currentAsOf,'VERSION_SCOPE_REQUIRED');
 if(stage==='REVIEW_PENDING')requireThat(source.rights.permittedUses.length>0&&evidence.requiredReviewerRole,'REVIEW_SCOPE_REQUIRED');
 if(stage==='ADMITTED'){
  requireThat(source.classification==='PUBLIC','SYNTHETIC_NOT_OFFICIAL');
  requireThat(source.rights.status==='LICENCED'||source.rights.status==='METADATA_AND_SHORT_EXCERPTS','RIGHTS_PENDING');
  requireThat(evidence.decision==='APPROVE'&&evidence.reviewer&&evidence.reviewerRole&&evidence.authorizationRef&&evidence.authorizationVerified===true&&date(evidence.decidedAt),'AUTHORISED_REVIEW_REQUIRED');
  requireThat(evidence.actor===evidence.reviewer,'REVIEW_ACTOR_MISMATCH');
  // Local self-asserted role strings and booleans cannot establish public authority.
  // Integrate a separately approved authority verifier before enabling this gate.
  throw Error('OFFICIAL_ADMISSION_AUTHORITY_NOT_CONFIGURED');
 }
}
async function appendUnchecked(catalogue,payload){
 const event={...payload,sequence:catalogue.events.length,previousDigest:catalogue.events.at(-1)?.digest??null};
 return freeze({...catalogue,events:[...catalogue.events,{...event,digest:await M.objectDigest(event)}]});
}
async function appendStage(catalogue,sourceId,stage,evidence){
 requireThat(await verifyCatalogue(catalogue),'INVALID_CATALOGUE');const source=catalogue.sources.find(source=>source.id===sourceId);requireThat(source,'SOURCE_NOT_FOUND');const current=replay(catalogue).get(sourceId);gate(source,stage,evidence,current);
 return appendUnchecked(catalogue,{operation:'STAGE',sourceId,sourceRevision:source.revisionId,stage,evidence:structuredClone(evidence)});
}
async function correctStage(catalogue,sourceId,stage,evidence){
 requireThat(await verifyCatalogue(catalogue),'INVALID_CATALOGUE');const source=catalogue.sources.find(source=>source.id===sourceId);requireThat(source,'SOURCE_NOT_FOUND');const current=replay(catalogue).get(sourceId);
 requireThat(STAGES.includes(stage)&&STAGES.indexOf(stage)<STAGES.indexOf(current.stage),'CORRECTION_MUST_DOWNGRADE');requireThat(evidence?.actor&&evidence?.reason&&date(evidence?.at),'CORRECTION_REASON_REQUIRED');
 return appendUnchecked(catalogue,{operation:'CORRECTION',sourceId,sourceRevision:source.revisionId,stage,evidence:structuredClone(evidence)});
}
async function verifyCatalogue(catalogue,expectedDigest=null){
 try{
  if(!catalogue||catalogue.format!==FORMAT||catalogue.algorithmVersion!=='atlas-source-intake-1'||!Array.isArray(catalogue.sources)||catalogue.sources.length>10000||!Array.isArray(catalogue.events)||catalogue.events.length>100000)return false;
  const ids=new Set();for(const source of catalogue.sources){const {revisionId,...record}=source;if(ids.has(source.id)||recordIssues(record).length||await M.objectDigest(record)!==revisionId)return false;if(source.lineage.supersedes.some(id=>!ids.has(id)))return false;ids.add(source.id);}
  const scratch={sources:catalogue.sources,events:[]};let previous=null;
  for(let i=0;i<catalogue.events.length;i++){
   const event=catalogue.events[i],{digest,...payload}=event,source=scratch.sources.find(s=>s.id===event.sourceId);if(!source||source.revisionId!==event.sourceRevision||event.sequence!==i||event.previousDigest!==previous||await M.objectDigest(payload)!==digest)return false;
   const current=replay(scratch).get(event.sourceId);
   if(event.operation==='STAGE')gate(source,event.stage,event.evidence,current);
   else if(event.operation==='CORRECTION'){if(!STAGES.includes(event.stage)||STAGES.indexOf(event.stage)>=STAGES.indexOf(current.stage)||!event.evidence?.actor||!event.evidence?.reason||!date(event.evidence?.at))return false;}
   else return false;
   scratch.events.push(event);previous=digest;
  }
  return !expectedDigest||await M.objectDigest(catalogue)===expectedDigest;
 }catch{return false;}
}
function coverage(catalogue){
 const states=replay(catalogue),documents=catalogue.sources.filter(source=>source.recordType==='DOCUMENT'),atLeast=(source,stage)=>STAGES.indexOf(states.get(source.id).stage)>=STAGES.indexOf(stage);
 return {inventoryCompleteness:'UNKNOWN',registeredRequirements:catalogue.sources.length,documentDenominator:documents.length,directoryDenominator:catalogue.sources.filter(source=>source.recordType==='DIRECTORY').length,requiredFamilyDenominator:new Set(catalogue.sources.map(source=>source.family)).size,discoveredDocuments:documents.length,accessibleDocuments:documents.filter(source=>atLeast(source,'SOURCE_RETRIEVED')).length,byteVerified:documents.filter(source=>atLeast(source,'RAW_BYTES_VERIFIED')).length,partiallyExtracted:documents.filter(source=>atLeast(source,'EXTRACTED')&&states.get(source.id).evidence.EXTRACTED?.coverage==='PARTIAL').length,fullyExtracted:documents.filter(source=>atLeast(source,'EXTRACTED')&&states.get(source.id).evidence.EXTRACTED?.coverage==='FULL').length,anchorReviewed:documents.filter(source=>atLeast(source,'ANCHOR_VERIFIED')).length,versionConfirmed:documents.filter(source=>atLeast(source,'CURRENT_VERSION_AND_SCOPE_CHECKED')).length,admittedDocuments:documents.filter(source=>atLeast(source,'ADMITTED')).length,admittedRelationships:0,relationshipCoverage:'NOT_COMPUTED_BY_SOURCE_REGISTER',officialOutcomeKpi:'UNKNOWN',warning:'Registered requirements are not a complete official document inventory. Historical reported checks do not count as current executed stages.'};
}
function statusFor(source,current){
 const retrieval=current.evidence.SOURCE_RETRIEVED,withdrawal=current.retrievalWithdrawal;
 // Source metadata is immutable. Availability follows retained intake evidence;
 // withdrawing that evidence requires a new check, not a new claim of denial.
 const access=retrieval?{state:'AVAILABLE',checkedAt:retrieval.retrievedAt,url:retrieval.url,reason:'HTTP 200 retrieval retained in the replayed intake history; current live availability is not implied.',basis:'INTAKE_EVENT'}:
  withdrawal?{state:'NOT_CHECKED',checkedAt:withdrawal.at,reason:'Retrieval evidence was withdrawn by correction; recheck the official source.',basis:'CORRECTION'}:
  {...source.access,basis:'HISTORICAL_SOURCE_RECORD'};
 const nextStage=STAGES[STAGES.indexOf(current.stage)+1]??null;
 let ownerType='SOURCE_RESEARCHER_AND_AUTHORISED_REVIEWER',nextAction='Independently review source evidence; retain unknowns and pending admission.';
 if(access.state==='BLOCKED_BY_PERMISSION'&&STAGES.indexOf(current.stage)<STAGES.indexOf('SOURCE_RETRIEVED')){
  ownerType='ENVIRONMENT_ADMIN';nextAction='Review the recorded destination-policy failure, then retry official retrieval through the configured proxy; retain UNKNOWN until successful.';
 }else if(nextStage==='DIRECTORY_OBSERVED')nextAction='Observe the official directory and record its digest before retrieving the document.';
 else if(nextStage==='SOURCE_RETRIEVED')nextAction='Retrieve the exact official source through the configured proxy and record the HTTP result, time, byte length and digest.';
 else if(nextStage==='RAW_BYTES_VERIFIED')nextAction='Verify the retrieved original bytes against their recorded digest; retain immutable prior receipts.';
 else if(nextStage==='EXTRACTED'){
  if(source.classification!=='SYNTHETIC'&&!source.rights.permittedUses.some(use=>['SHORT_EXCERPT','FULL_TEXT'].includes(use))){ownerType='SOURCE_RIGHTS_REVIEWER';nextAction='Confirm permitted reuse before extracting source content; public access alone does not grant reuse rights.';}
  else nextAction='Extract only permitted content and retain parser version, coverage, units, footnotes and exact anchors.';
 }else if(nextStage==='ANCHOR_VERIFIED')nextAction='Verify the extracted page/section anchors, content digests and extraction uncertainty.';
 else if(nextStage==='CURRENT_VERSION_AND_SCOPE_CHECKED')nextAction='Independently confirm the document revision, current-as-of date and geographic/effective scope.';
 else if(nextStage==='REVIEW_PENDING')nextAction='Identify the independently authorised reviewer and record the pending review scope.';
 else if(nextStage==='ADMITTED'){
  if(source.classification==='SYNTHETIC')nextAction='Synthetic research sources cannot receive official admission; retain them as explicitly synthetic research.';
  else {ownerType='AUTHORISED_SOURCE_REVIEWER';nextAction='Await independently authorised human review; official admission remains disabled until its authority verifier is configured.';}
 }
 return {sourceId:source.id,family:source.family,title:source.title,stage:current.stage,nextStage,access,historicalAccess:{...source.access},rights:source.rights.status,ownerType,nextAction};
}
function observationStatus(catalogue,source,current){const status=statusFor(source,current),newer=catalogue.sources.filter(s=>s.lineage.supersedes.includes(source.id));if(newer.length){status.newerObservationIds=newer.map(s=>s.id);status.ownerType='SOURCE_RESEARCHER_AND_AUTHORISED_REVIEWER';status.nextAction='Review later registered source observations '+status.newerObservationIds.join(', ')+'. This historical observation is retained; document legal supersession and current live access are not inferred.';}else if(status.access.state==='BLOCKED_BY_PERMISSION'&&!current.evidence.SOURCE_RETRIEVED){const directory=catalogue.sources.find(s=>s.id!==source.id&&s.officialUrl===source.directoryUrl&&s.access.state==='AVAILABLE');if(directory){const receipt=replay(catalogue).get(directory.id).evidence.SOURCE_RETRIEVED;if(receipt){status.access={state:'NOT_CHECKED',checkedAt:receipt.retrievedAt,basis:'DIRECTORY_RECEIPT_ONLY',reason:'The discovery directory was retrieved. Exact document access is not established; the historical denial is not a current policy finding.'};status.ownerType='SOURCE_RESEARCHER_AND_AUTHORISED_REVIEWER';status.nextAction='Discover and verify the exact document/version, then review its rights and applicability. Directory availability does not prove document access or admission.';}}}return status;}
function sourceStatus(catalogue,sourceId){const source=catalogue.sources.find(source=>source.id===sourceId);requireThat(source,'SOURCE_NOT_FOUND');return observationStatus(catalogue,source,replay(catalogue).get(sourceId));}
function sourceGaps(catalogue){const states=replay(catalogue);return catalogue.sources.filter(source=>states.get(source.id).stage!=='ADMITTED').map(source=>observationStatus(catalogue,source,states.get(source.id)));}
function contentRecords(catalogue,sourceId){
 const source=catalogue.sources.find(source=>source.id===sourceId);requireThat(source,'SOURCE_NOT_FOUND');
 return source.extraction.anchors.map(anchor=>({id:'source:'+source.id+':'+anchor.id,logicalId:'source:'+source.id+':'+anchor.id,sourceId:source.id,sourceRevision:source.revisionId,locator:anchor.locator,textKind:anchor.textKind,title:anchor.title||anchor.locator,text:anchor.text,status:source.classification==='SYNTHETIC'?'SYNTHETIC':STAGES.indexOf(replay(catalogue).get(source.id).stage)>=STAGES.indexOf('EXTRACTED')?'PUBLIC_TEXT_OBSERVED':'PUBLIC_TEXT_REPORTED_NOT_REVERIFIED',reviewStatus:'PENDING',machineVerification:replay(catalogue).get(source.id).stage,officialMapping:'UNKNOWN'}));
}
const api={registerSource,FORMAT,STAGES,recordIssues,safeUrl,createCatalogue,appendStage,correctStage,verifyCatalogue,replay,coverage,sourceStatus,sourceGaps,contentRecords};root.AtlasIntake=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
