/* Offline, byte-checked append into the existing catalogue. No network or admission. */
'use strict';
const fs=require('node:fs'),path=require('node:path'),M=require('../atlas-model.js'),I=require('../atlas-intake.js'),X=require('../csoi-intake.js'),G=require('../csoi-governance.js');
const APP=path.resolve(__dirname,'..'),MAX=64*1024*1024;
function requireThat(ok,reason){if(!ok)throw Error(reason);}
function closed(value,keys,reason){requireThat(value&&typeof value==='object'&&!Array.isArray(value)&&Object.keys(value).every(k=>keys.includes(k)),reason);}
function bounded(value,max=600){return typeof value==='string'&&value.length>0&&value.length<=max;}
function publicCouncilUrl(value){try{const u=new URL(value);return u.protocol==='https:'&&u.hostname==='www.snowymonaro.nsw.gov.au'&&!u.username&&!u.password&&!u.port&&!u.hash&&!u.search&&/^\/(?:files\/assets\/public\/|Building-and-Planning\/|Council\/Integrated-Planning-and-Reporting)/.test(u.pathname);}catch{return false;}}
function readOriginal(filename){const real=fs.realpathSync(filename);requireThat(real.startsWith('/tmp/'),'TEMPORARY_PUBLIC_ORIGINAL_REQUIRED');requireThat(fs.statSync(real).size<=MAX,'ORIGINAL_BYTE_LIMIT');return fs.readFileSync(real);}
async function prepare(catalogue,observations,batch,read=readOriginal){
 requireThat(await I.verifyCatalogue(catalogue),'EXISTING_CATALOGUE_INVALID');
 requireThat(observations.format==='csoi-public-source-observations-1'&&observations.originalBytesCommitted===false,'EXISTING_OBSERVATIONS_REQUIRED');
 closed(batch,['format','receipts'],'RECEIPT_BATCH_FIELDS');
 requireThat(batch.format==='csoi-receipt-batch-1'&&Array.isArray(batch.receipts)&&batch.receipts.length>0&&batch.receipts.length<=30,'RECEIPT_BATCH_REQUIRED');
 const next=structuredClone(observations),added=[],ids=new Set(next.observations.map(o=>o.id));let result=catalogue;
 for(const receipt of batch.receipts){
  closed(receipt,['id','classification','rights','admission','currentVersion','family','stationId','recordType','title','url','resolvedUrl','directoryUrl','directoryDigest','httpStatus','workspacePath','mediaType','byteLength','rawDigest','retrievedAt','geographicExtent','pageCount','knowledgeAnchors','revisionObservation','documentLinks'],'RECEIPT_FIELDS');
  requireThat(!G.inspectPayload(receipt).length,'PUBLIC_METADATA_SCREENING_FAILED');
  requireThat(receipt.classification==='PUBLIC'&&receipt.rights==='UNKNOWN'&&receipt.admission==='PENDING'&&receipt.currentVersion==='UNKNOWN','NO_AUTOMATIC_SOURCE_PROMOTION');
  requireThat(/^[a-z0-9][a-z0-9-]{0,100}$/.test(receipt.id)&&!ids.has(receipt.id),'UNIQUE_OBSERVATION_REQUIRED');
  requireThat(/^[A-Z][A-Z0-9_]{0,79}$/.test(receipt.family)&&require('../atlas-data.js').nodes.some(n=>n.id===receipt.stationId),'SOURCE_FAMILY_AND_STATION_REQUIRED');
  requireThat(publicCouncilUrl(receipt.url)&&publicCouncilUrl(receipt.directoryUrl)&&publicCouncilUrl(receipt.resolvedUrl||receipt.url)&&receipt.httpStatus===200,'OFFICIAL_PUBLIC_RECEIPT_REQUIRED');
  requireThat(['DOCUMENT','DIRECTORY'].includes(receipt.recordType)&&typeof receipt.title==='string'&&receipt.title.length<=300,'SOURCE_METADATA_REQUIRED');
  const directory=result.sources.find(s=>s.officialUrl===receipt.directoryUrl&&s.rawDigest===receipt.directoryDigest);
  requireThat(directory&&I.sourceStatus(result,directory.id).access.state==='AVAILABLE','PINNED_RETRIEVED_DIRECTORY_REQUIRED');
  const bytes=await read(receipt.workspacePath);requireThat(bytes instanceof Uint8Array&&bytes.length<=MAX&&bytes.length===receipt.byteLength,'ORIGINAL_BYTE_LENGTH_MISMATCH');
  const digest=await M.digest(bytes);requireThat(digest===receipt.rawDigest,'ORIGINAL_BYTE_DIGEST_MISMATCH');
  requireThat(['application/pdf','text/html'].includes(receipt.mediaType),'MEDIA_TYPE_REQUIRED');
  if(receipt.mediaType==='application/pdf')requireThat(new TextDecoder().decode(bytes.slice(0,5))==='%PDF-','ORIGINAL_PDF_HEADER_REQUIRED');
  else requireThat(/<(?:!doctype\s+html|html)(?:\s|>)/i.test(new TextDecoder().decode(bytes.slice(0,2048))),'ORIGINAL_HTML_HEADER_REQUIRED');
  closed(receipt.geographicExtent,['type','label','parcelApplicability'],'GEOGRAPHY_FIELDS');
  requireThat(bounded(receipt.geographicExtent.type,100)&&bounded(receipt.geographicExtent.label)&&receipt.geographicExtent.parcelApplicability==='UNKNOWN','GEOGRAPHY_NOT_ADMITTED');
  const revision=receipt.revisionObservation||null;
  if(revision){closed(revision,['titleOnCover','directoryLinkLabel','versionObserved','adoptionDateObserved','effectiveDateObserved','resolutionObserved','locator','scopeObserved','conflicts','currentness','legalApplicability'],'REVISION_METADATA_FIELDS');for(const [key,value]of Object.entries(revision))requireThat(key==='conflicts'?Array.isArray(value)&&value.length<=10&&value.every(x=>bounded(x,500)):bounded(value),'REVISION_METADATA_BOUNDS');requireThat(revision.currentness==='UNKNOWN'&&revision.legalApplicability==='UNKNOWN','NO_AUTOMATIC_SOURCE_PROMOTION');}
  const links=receipt.documentLinks||[];requireThat(Array.isArray(links)&&links.length<=100,'DISCOVERY_LINK_LIMIT');
  for(const lead of links){closed(lead,['url','title'],'DISCOVERY_LINK_FIELDS');requireThat(publicCouncilUrl(lead.url)&&bounded(lead.title,300),'OFFICIAL_PUBLIC_DISCOVERY_LINK_REQUIRED');}
  requireThat(Array.isArray(receipt.knowledgeAnchors||[])&&(receipt.knowledgeAnchors||[]).length<=10,'SUMMARY_LIMIT');
  const anchorIds=new Set(),anchors=(receipt.knowledgeAnchors||[]).map(anchor=>{
   closed(anchor,['id','title','locator','textKind','text','digest','parserVersion','verification','uncertainty'],'SUMMARY_FIELDS');
   requireThat(anchor.textKind==='RESEARCH_SUMMARY'&&typeof anchor.text==='string'&&anchor.text.length<=1000&&anchor.locator&&anchor.id,'BOUNDED_AUTHORED_SUMMARY_ONLY');
   requireThat(/^[a-z0-9][a-z0-9-]{0,100}$/.test(anchor.id)&&bounded(anchor.locator)&&bounded(anchor.title||anchor.locator,300),'SUMMARY_METADATA_BOUNDS');
   requireThat(!anchorIds.has(anchor.id),'UNIQUE_SUMMARY_REQUIRED');anchorIds.add(anchor.id);
   return {id:anchor.id,title:anchor.title||anchor.locator,locator:anchor.locator,textKind:'RESEARCH_SUMMARY',text:anchor.text,digest:'sha256:'+M.sha256(new TextEncoder().encode(anchor.text)),verification:'SOURCE_OBSERVED_NOT_FORMAL_ADMISSION',parserVersion:'reviewed-public-summary-2',uncertainty:'Reuse rights, current consolidation, legal applicability and authorised admission remain UNKNOWN/PENDING.'};
  });
  const template=structuredClone(observations.observations.find(o=>o.intakeRecord).intakeRecord);delete template.revisionId;
  const record={...template,id:'csoi:'+receipt.id+':'+String(receipt.retrievedAt).slice(0,10).replaceAll('-',''),family:receipt.family,stationId:receipt.stationId,title:receipt.title,recordType:receipt.recordType,publisher:'Snowy Monaro Regional Council',officialUrl:receipt.url,directoryUrl:receipt.directoryUrl,classification:'PUBLIC',mediaType:receipt.mediaType,rights:{status:'UNKNOWN',licence:null,basis:'Public original temporarily verified. Only metadata and bounded own factual research wording are retained; original redistribution rights remain UNKNOWN.',permittedUses:['METADATA_ONLY']},rawDigest:digest,retrievedAt:receipt.retrievedAt,adoptedAt:null,effectiveFrom:null,effectiveTo:null,amendedAt:null,supersededAt:null,currentAsOf:null,geographicExtent:receipt.geographicExtent,extraction:{parser:'local review; no formal source extraction',version:'csoi-receipt-append-1',coverage:'NONE',totalPages:receipt.pageCount||null,extractedPages:[],anchors:[]},lineage:{supersedes:[],revisionLabel:digest},corroboratingEvidence:[],access:{state:'AVAILABLE',checkedAt:receipt.retrievedAt,reason:'Original bytes independently rehashed from temporary public-source retrieval; permission/currentness/admission pending.'}};
  requireThat(!I.recordIssues(record).length,'SOURCE_RECORD_INVALID:'+I.recordIssues(record).join(','));
  const observation={id:receipt.id,family:receipt.family,url:receipt.url,retrievedAt:receipt.retrievedAt,classification:'PUBLIC',rights:'UNKNOWN',currentVersion:'UNKNOWN',legalApplicability:'UNKNOWN',admission:'PENDING',geography:receipt.geographicExtent.label,httpStatus:200,resolvedUrl:receipt.resolvedUrl||receipt.url,mediaType:receipt.mediaType,byteLength:bytes.length,rawDigest:digest,title:receipt.title,documentLinks:receipt.documentLinks||[],access:'AVAILABLE',knowledgeAnchors:anchors,rightsNote:record.rights.basis,originalBytesCommitted:false,currentAsOf:null,effectiveFrom:null,effectiveTo:null,adoptedAt:null,revisionObservation:receipt.revisionObservation||null,byteVerification:'PASS_TESTED_HERE',intakeRecord:record,stageEvidence:{DIRECTORY_OBSERVED:{url:receipt.directoryUrl,directoryDigest:receipt.directoryDigest},SOURCE_RETRIEVED:{url:receipt.url,resolvedUrl:receipt.resolvedUrl||receipt.url,retrievedAt:receipt.retrievedAt,httpStatus:200,byteLength:bytes.length,rawDigest:digest},RAW_BYTES_VERIFIED:{rawDigest:digest}}};
  result=await X.extendCatalogue(result,{format:observations.format,originalBytesCommitted:false,observations:[observation]});
  next.observations.push(observation);ids.add(receipt.id);added.push(receipt.id);
 }
 requireThat(M.canonical(result.sources.slice(0,catalogue.sources.length))===M.canonical(catalogue.sources)&&M.canonical(result.events.slice(0,catalogue.events.length))===M.canonical(catalogue.events),'IMMUTABLE_CATALOGUE_PREFIX_CHANGED');
 requireThat(M.canonical(next.observations.slice(0,observations.observations.length))===M.canonical(observations.observations),'IMMUTABLE_OBSERVATION_PREFIX_CHANGED');
 const successful=next.observations.filter(o=>o.httpStatus===200&&o.byteVerification==='PASS_TESTED_HERE');
 next.observedAt=new Date(Math.max(...next.observations.map(o=>Date.parse(o.retrievedAt)))).toISOString();
 next.coverage={...next.coverage,observedUrlDenominator:next.observations.length,http200:successful.length,byteVerified:successful.length,researchSummarySourceCount:successful.filter(o=>o.knowledgeAnchors?.length).length,uniqueAttemptedUrls:new Set(next.observations.map(o=>o.url)).size,httpExchangeCount:'UNKNOWN_REDIRECTS_NOT_INSTRUMENTED',note:'Selected URL request-attempt records include retries; same-host redirects can add HTTP exchanges. Complete corpus coverage and official admission are separate.'};
 const proof={format:'csoi-source-prefix-proof-1',previousCatalogueDigest:await M.objectDigest(catalogue),previousSourceCount:catalogue.sources.length,previousEventCount:catalogue.events.length,previousEventHead:catalogue.events.at(-1).digest,previousObservationCount:observations.observations.length,previousObservationsDigest:await M.objectDigest(observations.observations),addedObservationIds:added,currentCatalogueDigest:await M.objectDigest(result),cataloguePrefixUnchanged:true,observationPrefixUnchanged:true,originalBodiesCommitted:false,rights:'UNKNOWN',admission:'PENDING'};
 return {catalogue:result,observations:next,proof,summary:{added:added.length,totalRecords:result.sources.length,successfulByteReceipts:successful.length,officialAdmitted:0}};
}
module.exports={prepare,readOriginal,publicCouncilUrl};
if(require.main===module)(async()=>{
 requireThat(process.argv[2],'Usage: node tools/csoi-append-receipts.cjs TEMP_BATCH.json [--apply]');
 const filename=path.resolve(process.argv[2]);requireThat(fs.statSync(filename).size<=1024*1024,'MANIFEST_LIMIT');
 const result=await prepare(JSON.parse(fs.readFileSync(path.join(APP,'sources/csoi-catalogue.json'))),JSON.parse(fs.readFileSync(path.join(APP,'sources/csoi-source-observations.json'))),JSON.parse(fs.readFileSync(filename)));
 if(process.argv[3]==='--apply'){
  for(const [name,value,globalName]of [['csoi-catalogue',result.catalogue,'CsoiRegisteredSources'],['csoi-source-observations',result.observations,'CsoiSourceObservations']]){
   fs.writeFileSync(path.join(APP,'sources',name+'.json'),JSON.stringify(value,null,2)+'\n');
   fs.writeFileSync(path.join(APP,'sources',name+'.js'),`(function(root){const value=${JSON.stringify(value)};root.${globalName}=value;if(typeof module!=='undefined')module.exports=value;})(typeof window!=='undefined'?window:globalThis);\n`);
  }
  fs.writeFileSync(path.join(APP,'qa/csoi/source-extension-prefix-20261030.json'),JSON.stringify(result.proof,null,2)+'\n');
 }
 console.log(JSON.stringify({mode:process.argv[3]==='--apply'?'APPLIED':'DRY_RUN',...result.summary,proof:result.proof},null,2));
})().catch(error=>{console.error(error.message);process.exitCode=1});
