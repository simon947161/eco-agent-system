const assert=require('node:assert/strict'),M=require('./atlas-model.js'),E=require('./atlas-execution.js'),D=require('./atlas-data.js'),A=require('./atlas-accounting.js');
(async()=>{
 const d=await M.migrateDataset(D,A.cases),index=M.domainIndex(d),context={date:'2026-10-29',region:'SYNTHETIC_PLACE',spatialType:'SCENARIO_AREA',soughtEffect:'LEP_STATUTORY'};
 for(const [id,status] of [['current','SYNTHETIC_ONLY'],['wrong-region','REJECTED_REGION'],['draft','REJECTED_DRAFT'],['expired','REJECTED_TIME']])assert.equal(E.applicability(index.get('legal-fixture:'+id),context).status,status);
 assert.equal(E.applicability(index.get('legal-fixture:current'),{...context,spatialType:'PARCEL'}).status,'REJECTED_SPATIAL_GRAIN');
 assert.equal(E.applicability(index.get('legal-fixture:current'),{...context,date:'2026-02-30'}).status,'UNKNOWN');
 assert.equal(E.applicability(index.get('legal-fixture:current'),{...context,sourceRevision:'wrong'}).status,'REJECTED_REVISION');
 assert.equal(E.applicability(index.get('legal-fixture:current'),{...context,soughtEffect:'DCP_GUIDANCE'}).status,'REJECTED_LEGAL_EFFECT');
 assert.equal(E.shortestPath(d,'area','legal-fixture:wrong-region',{context}).status,'UNKNOWN');
 assert.equal(E.shortestPath(d,'area','legal-fixture:current',{context}).status,'DISCOVERY_CANDIDATE');
 assert.equal(E.applicability({...index.get('legal-fixture:current'),data:{...index.get('legal-fixture:current').data,supersededAt:'2026-09-01'}},context).status,'REJECTED_SUPERSEDED');
 assert(E.scopeIndex(d).has('SYNTHETIC_PLACE'));assert.equal(E.asOf(d,{...context,kind:'StatutoryControl'}).records.length,1);
 assert.equal(E.asOf(d,{...context,date:'2024-10-29',kind:'StatutoryControl'}).records[0].id,'legal-fixture:expired');
 const old=index.get('legal-fixture:current'),changed=await M.commitDomainRevision(d,{id:old.id,expectedRevisionId:old.revisionId,patch:{data:{...old.data,sourceRevision:'conflicting-source'}},reason:'Synthetic conflicting revision'});
 assert.equal(E.asOf(changed,{...context,kind:'StatutoryControl'}).conflicts.length,1);assert(await M.verifySnapshot(await M.exportSnapshot(changed)));
 console.log('PASS: spatial/effective-time indexes, historical as-of queries, wrong region/date/parcel/revision/draft/legal-effect rejection, overlapping source revision conflict and rejected candidate path exclusion');
})().catch(e=>{console.error(e);process.exitCode=1});
