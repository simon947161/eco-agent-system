const assert=require('node:assert/strict'),M=require('./atlas-model.js'),I=require('./atlas-intake.js'),C=require('./sources/public-catalogue.json'),S=require('./sources/csoi-source-observations.json'),X=require('./csoi-intake.js');
(async()=>{
 assert.deepEqual(require('./sources/csoi-source-observations.js'),S);
 const cat=await X.extendCatalogue(C,S);assert(await I.verifyCatalogue(cat));assert.deepEqual(cat.events.slice(0,C.events.length),C.events);assert.deepEqual(cat.sources.slice(0,C.sources.length),C.sources);
 assert.equal(I.coverage(cat).accessibleDocuments+cat.sources.filter(s=>s.recordType==='DIRECTORY').length,S.coverage.http200);
 assert.equal(I.coverage(cat).admittedDocuments,0);assert.equal(I.coverage(cat).partiallyExtracted,0);assert(cat.sources.every(s=>s.rights.status==='UNKNOWN'));
 assert.notEqual(I.sourceStatus(cat,'smrc-csp-full').ownerType,'ENVIRONMENT_ADMIN');assert(I.sourceStatus(cat,'smrc-csp-full').newerObservationIds.length);
 let d=await M.migrateDataset(require('./atlas-data.js'),require('./atlas-accounting.js').cases,cat);d=await X.registerSummaries(d,S);
 assert(d.domain.entities.some(e=>e.data.csoiRecord?.data.locator?.includes('page 27')));assert.equal(await M.objectDigest(M.legacyBase(d)),await M.objectDigest(require('./atlas-data.js')));assert(await M.verifySnapshot(await M.exportSnapshot(d)));
 const bad=structuredClone(S);bad.observations.find(o=>o.knowledgeAnchors?.length).knowledgeAnchors[0].text+=' altered';await assert.rejects(async()=>X.registerSummaries(await M.migrateDataset(require('./atlas-data.js'),require('./atlas-accounting.js').cases,cat),bad),/SUMMARY_DIGEST/);
 console.log('PASS: actual public observation receipts extend original catalogue, preserve histories/rights gates, and bind bounded research summaries to existing Atlas snapshots');
})().catch(e=>{console.error(e);process.exitCode=1});
