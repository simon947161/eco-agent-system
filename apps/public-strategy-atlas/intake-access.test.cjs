const assert=require('node:assert/strict');
const M=require('./atlas-model.js'),I=require('./atlas-intake.js'),C=require('./sources/public-catalogue.json');
(async()=>{
 const at='2026-10-30T00:00:00Z',later='2026-10-30T01:00:00Z',digest=await M.objectDigest('repository-authored QA bytes');
 const {revisionId,...record}=structuredClone(C.sources[0]);
 Object.assign(record,{id:'qa-access-only',title:'QA fixture; no official document or retrieval',officialUrl:'https://example.invalid/qa-source.pdf',rawDigest:null,extraction:{coverage:'NONE',anchors:[]}});
 const e={actor:'qa-only',at,reason:'Repository-authored test evidence, not an official retrieval'};
 let c=await I.createCatalogue([record],{registeredAt:at});
 const original=structuredClone(c),sourceRevision=c.sources[0].revisionId;
 assert.equal(I.sourceStatus(c,record.id).access.state,'BLOCKED_BY_PERMISSION');
 assert.equal(I.sourceStatus(c,record.id).ownerType,'ENVIRONMENT_ADMIN');
 c=await I.appendStage(c,record.id,'DIRECTORY_OBSERVED',{...e,url:record.directoryUrl,directoryDigest:digest});
 // With no previous retrieval, an unrelated correction retains recorded access.
 const directoryCorrection=await I.correctStage(c,record.id,'DISCOVERED',{...e,at:later,reason:'Withdraw directory observation only'});
 assert.equal(I.sourceStatus(directoryCorrection,record.id).access.state,'BLOCKED_BY_PERMISSION');
 c=await I.appendStage(c,record.id,'SOURCE_RETRIEVED',{...e,url:record.officialUrl,retrievedAt:at,byteLength:10,httpStatus:200,rawDigest:digest});
 const retrieved=c;
 let status=I.sourceStatus(c,record.id);
 assert.equal(status.access.state,'AVAILABLE');assert.equal(status.access.basis,'INTAKE_EVENT');assert.equal(status.access.url,record.officialUrl);
 assert.equal(status.access.checkedAt,at);assert(!JSON.stringify(status.access).includes('403'));
 assert.match(status.access.reason,/current live availability is not implied/);
 assert.equal(status.ownerType,'SOURCE_RESEARCHER_AND_AUTHORISED_REVIEWER');assert.equal(status.nextStage,'RAW_BYTES_VERIFIED');
 assert(!status.nextAction.includes('environment settings'));assert.deepEqual(status.historicalAccess,record.access);
 assert.deepEqual(I.sourceGaps(c)[0],status);
 c=await I.appendStage(c,record.id,'RAW_BYTES_VERIFIED',{...e,rawDigest:digest});
 const verified=c;
 assert.equal(I.sourceStatus(c,record.id).ownerType,'SOURCE_RIGHTS_REVIEWER');assert.match(I.sourceStatus(c,record.id).nextAction,/permitted reuse/);
 await assert.rejects(()=>I.appendStage(c,record.id,'EXTRACTED',{...e,parserVersion:'qa',coverage:'PARTIAL',extractionDigest:digest}),/EXTRACTION_RIGHTS_PENDING/);
 const retained=await I.correctStage(c,record.id,'SOURCE_RETRIEVED',{...e,at:later,reason:'Withdraw byte verification, retain retrieval'});
 assert.equal(I.sourceStatus(retained,record.id).access.state,'AVAILABLE');assert.equal(I.sourceStatus(retained,record.id).nextStage,'RAW_BYTES_VERIFIED');
 const withdrawn=await I.correctStage(c,record.id,'DIRECTORY_OBSERVED',{...e,at:later,reason:'Withdraw retrieval evidence'});
 status=I.sourceStatus(withdrawn,record.id);assert.equal(status.access.state,'NOT_CHECKED');assert.equal(status.access.checkedAt,later);
 assert.equal(status.access.basis,'CORRECTION');assert.equal(status.nextStage,'SOURCE_RETRIEVED');assert.notEqual(status.ownerType,'ENVIRONMENT_ADMIN');
 assert.equal(I.coverage(withdrawn).accessibleDocuments,0);assert.equal(I.coverage(verified).accessibleDocuments,1);
 const restored=await I.appendStage(withdrawn,record.id,'SOURCE_RETRIEVED',{...e,at:later,url:record.officialUrl,retrievedAt:later,byteLength:10,httpStatus:200,rawDigest:digest});
 assert.equal(I.sourceStatus(restored,record.id).access.state,'AVAILABLE');assert.equal(I.sourceStatus(restored,record.id).access.checkedAt,later);
 // Derived views cannot rewrite the immutable record, events or digest.
 const before=await M.objectDigest(restored);I.sourceGaps(restored);I.sourceStatus(restored,record.id);assert.equal(await M.objectDigest(restored),before);
 assert.deepEqual(restored.sources,original.sources);assert.equal(restored.sources[0].revisionId,sourceRevision);
 assert.deepEqual(retrieved.events.slice(0,original.events.length),original.events);
 for(const value of [c,retained,withdrawn,restored])assert(await I.verifyCatalogue(value));
 assert.throws(()=>I.sourceStatus(c,'missing'),/SOURCE_NOT_FOUND/);
 // A permitted synthetic fixture can reach review, but never official admission.
 const synthetic={...record,id:'qa-permitted',classification:'SYNTHETIC',rights:{status:'SYNTHETIC_AUTHORED',permittedUses:['FULL_TEXT'],basis:'Repository-authored test fixture'},currentAsOf:'2026-10-30',extraction:{coverage:'PARTIAL',anchors:[{id:'a',locator:'QA',textKind:'SYNTHETIC',text:'QA',digest:await M.digest(new TextEncoder().encode('QA'))}]}};
 async function toReview(source){let s=await I.createCatalogue([source],{registeredAt:at});
 for(const [stage,fields] of [
  ['DIRECTORY_OBSERVED',{url:record.directoryUrl,directoryDigest:digest}],
  ['SOURCE_RETRIEVED',{url:record.officialUrl,retrievedAt:at,byteLength:10,httpStatus:200,rawDigest:digest}],
  ['RAW_BYTES_VERIFIED',{rawDigest:digest}],
  ['EXTRACTED',{parserVersion:'qa',coverage:'PARTIAL',extractionDigest:await M.objectDigest(source.extraction.anchors)}],
  ['ANCHOR_VERIFIED',{anchorIds:['a'],method:'QA',uncertainty:'SYNTHETIC'}],
  ['CURRENT_VERSION_AND_SCOPE_CHECKED',{currentAsOf:synthetic.currentAsOf,versionConfirmed:true,scopeConfirmed:true,corroboratingUrl:record.officialUrl}],
  ['REVIEW_PENDING',{requiredReviewerRole:'authorised-source-reviewer'}]
 ]){s=await I.appendStage(s,source.id,stage,{...e,...fields});assert.equal(I.sourceStatus(s,source.id).access.state,stage==='DIRECTORY_OBSERVED'?'BLOCKED_BY_PERMISSION':'AVAILABLE');}return s;}
 const s=await toReview(synthetic);
 assert.equal(I.sourceStatus(s,synthetic.id).ownerType,'SOURCE_RESEARCHER_AND_AUTHORISED_REVIEWER');assert.match(I.sourceStatus(s,synthetic.id).nextAction,/cannot receive official admission/);
 assert.equal(I.coverage(s).admittedDocuments,0);
 const publicQa={...synthetic,id:'qa-public-review',classification:'PUBLIC',rights:{status:'METADATA_AND_SHORT_EXCERPTS',permittedUses:['SHORT_EXCERPT'],basis:'QA fixture only; no real reuse permission claimed'},extraction:{...synthetic.extraction,anchors:synthetic.extraction.anchors.map(a=>({...a,textKind:'SOURCE_EXCERPT'}))}};
 const p=await toReview(publicQa);
 assert.equal(I.sourceStatus(p,publicQa.id).ownerType,'AUTHORISED_SOURCE_REVIEWER');assert.match(I.sourceStatus(p,publicQa.id).nextAction,/admission remains disabled/);
 await assert.rejects(()=>I.appendStage(p,publicQa.id,'ADMITTED',{...e,reviewer:e.actor,reviewerRole:'qa-claimed-role',decision:'APPROVE',authorizationRef:'qa-only',authorizationVerified:true,decidedAt:at}),/OFFICIAL_ADMISSION_AUTHORITY_NOT_CONFIGURED/);
 assert.equal(await M.objectDigest(C),'sha256:d03244417a78b09f2b21776564ffeabaa308d97f3d89f4de1304facb24e5180a');
 console.log('PASS: replayed source availability, retained historical access, stage-specific rights/review owners, correction withdrawal/re-retrieval and immutable catalogue identity');
})().catch(error=>{console.error(error);process.exitCode=1;});
