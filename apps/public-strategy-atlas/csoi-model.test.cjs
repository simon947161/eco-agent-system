const assert=require('node:assert/strict'),M=require('./atlas-model.js'),G=require('./csoi-governance.js');
(async()=>{
 const base=require('./atlas-data.js'),d=await M.migrateDataset(base,require('./atlas-accounting.js').cases,require('./sources/public-catalogue.json'));
 const input={id:'csoi:qa-record',ownerModule:'CSOI_OPERATIONS',security:'PUBLIC',layer:'L0',sourceClass:'SYNTHETIC',judgment:'OBSERVATION',authority:'INDEPENDENT_RESEARCH',scope:{region:'SYNTHETIC_PLACE',boundary:'QA',period:{from:'2026-01-01',to:'2026-12-31'}},inputs:[],data:{value:1},sensitivity:{personalData:false,confidential:false,reidentifiable:false},provenance:{contentMode:'SYNTHETIC',rights:{mode:'SYNTHETIC_OWNED',basis:'Repository QA'}},observedAt:'2026-10-30T00:00:00Z'};
 const record=await G.makeRecord(input),original=await M.objectDigest(d);
 let next=await M.registerResearchRecord(d,{record,kind:'ContentBlock',label:'QA public envelope',stationId:'audit',reason:'Test same Atlas registry'});
 assert.equal(M.domainIndex(next).get(record.id).data.csoiRecord.revisionId,record.revisionId);assert.equal(await M.objectDigest(d),original);
 assert.equal(await M.objectDigest(M.legacyBase(next)),await M.objectDigest(base));assert(await M.verifySnapshot(await M.exportSnapshot(next)));
 const old=next.domain.entities.find(e=>e.id===record.id),revised=await G.makeRecord({...input,data:{value:2},observedAt:'2026-10-30T00:01:00Z'});
 next=await M.reviseResearchRecord(next,{id:record.id,expectedRevisionId:old.revisionId,record:revised,reason:'Append independent revision'});
 assert.equal(next.domain.revisions.length,d.domain.revisions.length+2);assert(await M.verifySnapshot(await M.exportSnapshot(next)));
 await assert.rejects(()=>M.reviseResearchRecord(next,{id:record.id,expectedRevisionId:old.revisionId,record:revised,reason:'Stale'}),/CONFLICT/);
 for(const security of ['COUNCIL_PROTECTED','PERSONAL_PRIVATE','APPROVED_RELEASE'])await assert.rejects(()=>M.registerResearchRecord(d,{record:{...record,security},label:'No',stationId:'audit',reason:'No'}),/CSOI_PUBLIC_RECORD_REQUIRED/);
 const bad=await M.exportSnapshot(next);bad.dataset.domain.entities.find(e=>e.id===record.id).data.csoiRecord.data.value=999;assert.equal(await M.verifySnapshot(bad),false);
 const dangling=await G.makeRecord({...input,inputs:[{id:'csoi:missing',revisionId:record.revisionId}]});await assert.rejects(()=>M.registerResearchRecord(d,{record:dangling,label:'Dangling',stationId:'audit',reason:'Reject unbound input'}),/INPUT_REVISION_MISSING/);
 await assert.rejects(()=>M.registerResearchRecord(d,{record,kind:'ReviewDecision',label:'No forged review',stationId:'audit',reason:'No'}),/REGISTRATION_INVALID/);
 console.log('PASS: CSOI records use the existing Atlas registry, immutable revisions, legacy base, independent snapshots, stale-write and protected/official rejection');
})().catch(e=>{console.error(e);process.exitCode=1});
