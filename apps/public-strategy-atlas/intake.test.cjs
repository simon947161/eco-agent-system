const assert=require('node:assert/strict'),fs=require('node:fs'),m=require('./atlas-model.js'),I=require('./atlas-intake.js'),C=require('./sources/public-catalogue.json');
(async()=>{
 assert(await I.verifyCatalogue(C));assert.deepEqual(require('./sources/public-catalogue.js'),C);assert.equal(I.coverage(C).registeredRequirements,15);assert.equal(I.coverage(C).accessibleDocuments,0);assert.equal(I.coverage(C).admittedDocuments,0);assert.equal(I.sourceGaps(C).length,15);
 const now='2026-10-29T00:00:00Z',digest=await m.objectDigest('synthetic permitted source bytes'),record={...structuredClone(C.sources[0]),id:'fixture',classification:'SYNTHETIC',rights:{status:'SYNTHETIC_AUTHORED',permittedUses:['FULL_TEXT','SHORT_EXCERPT'],basis:'Repository-authored synthetic QA'},rawDigest:digest,currentAsOf:'2026-10-29',extraction:{coverage:'PARTIAL',anchors:[{id:'a',locator:'Section 1',textKind:'SYNTHETIC',text:'Fixture only',digest:await m.digest(new TextEncoder().encode('Fixture only'))}]}};delete record.revisionId;
 let c=await I.createCatalogue([record],{registeredAt:now});
 const evidence={actor:'local-researcher',at:now,reason:'Synthetic pipeline QA'};
 await assert.rejects(()=>I.appendStage(c,'fixture','EXTRACTED',evidence),/STAGE_ORDER/);
 for(const [stage,fields] of [
 ['DIRECTORY_OBSERVED',{url:record.officialUrl,directoryDigest:digest}],
 ['SOURCE_RETRIEVED',{url:record.officialUrl,retrievedAt:now,byteLength:10,httpStatus:200,rawDigest:digest}],
 ['RAW_BYTES_VERIFIED',{rawDigest:digest}],
 ['EXTRACTED',{parserVersion:'synthetic-parser-1',extractionDigest:await m.objectDigest(record.extraction.anchors),coverage:'PARTIAL'}],
 ['ANCHOR_VERIFIED',{anchorIds:['a'],method:'manual synthetic anchor check',uncertainty:'SYNTHETIC'}],
 ['CURRENT_VERSION_AND_SCOPE_CHECKED',{currentAsOf:record.currentAsOf,versionConfirmed:true,scopeConfirmed:true,corroboratingUrl:record.officialUrl}],
 ['REVIEW_PENDING',{requiredReviewerRole:'authorised-source-reviewer'}]])c=await I.appendStage(c,'fixture',stage,{...evidence,...fields});
 assert(await I.verifyCatalogue(c));assert.equal(I.replay(c).get('fixture').stage,'REVIEW_PENDING');
 await assert.rejects(()=>I.appendStage(c,'fixture','ADMITTED',{...evidence,reviewer:'local-researcher',decision:'APPROVE',authorizationVerified:true}),/SYNTHETIC_NOT_OFFICIAL/);
 const corrected=await I.correctStage(c,'fixture','SOURCE_RETRIEVED',{...evidence,reason:'Withdraw failed anchor review'});assert.equal(I.replay(corrected).get('fixture').stage,'SOURCE_RETRIEVED');assert(corrected.events.length>c.events.length);assert(await I.verifyCatalogue(corrected));
 assert.equal(I.coverage(corrected).byteVerified,0);assert.equal(I.coverage(c).byteVerified,1);
 for(const mutate of [x=>x.sources[0].rights.status='LICENCED',x=>x.events[1].stage='ADMITTED',x=>x.events.reverse(),x=>x.events[0].evidence.reason='changed']){const bad=structuredClone(c);mutate(bad);assert.equal(await I.verifyCatalogue(bad),false);}
 assert(I.recordIssues({...record,officialUrl:'javascript:alert(1)'}).includes('UNSAFE_SOURCE_URL'));
 assert(I.recordIssues({...record,effectiveFrom:'2026-02-30'}).includes('SOURCE_DATE:effectiveFrom'));
 assert(I.recordIssues({...record,classification:'RESTRICTED'}).includes('PUBLIC_ONLY'));
 const publicRecord={...record,classification:'PUBLIC',rights:{status:'UNKNOWN',permittedUses:['FULL_TEXT']}};assert(I.recordIssues(publicRecord).includes('FULL_TEXT_RIGHTS_REQUIRED'));
 assert.equal(I.contentRecords(C,'smrc-csp-full')[0].status,'PUBLIC_TEXT_REPORTED_NOT_REVERIFIED');
 const {revisionId:unusedRevision,...newDocument}=structuredClone(C.sources[0]);newDocument.id='smrc-csp-future-revision';newDocument.lineage={supersedes:[C.sources[0].id],revisionLabel:'UNKNOWN'};
 const extended=await I.registerSource(C,newDocument,{registeredAt:now,reason:'Synthetic registry extension test; no new public source retrieved'});assert.equal(extended.sources.length,C.sources.length+1);assert.deepEqual(extended.events.slice(0,C.events.length),C.events);assert(await I.verifyCatalogue(extended));
 await assert.rejects(()=>I.registerSource(C,{...newDocument,lineage:{supersedes:['missing'],revisionLabel:'UNKNOWN'}},{registeredAt:now}),/SOURCE_LINEAGE/);
 const migrated=await m.migrateDataset(require('./atlas-data.js'),require('./atlas-accounting.js').cases,C);assert(await m.verifySnapshot(await m.exportSnapshot(migrated)));
 const corrupt=await m.exportSnapshot(migrated);corrupt.dataset.domain.sourceCatalogue.events[0].stage='ADMITTED';assert.equal(await m.verifySnapshot(corrupt),false);
 console.log('PASS: 15 source requirements, exact catalogue mirror/hash, ordered intake/correction replay, permitted synthetic pipeline, rights/date/URL/private-data gates, corruption/forged stage rejection and honest coverage denominators');
})().catch(e=>{console.error(e);process.exitCode=1});
