const assert=require('node:assert/strict'),m=require('./atlas-model.js'),base=require('./atlas-data.js'),a=require('./atlas-accounting.js'),w=require('./atlas-workspace.js');
(async()=>{
 const frozen=await m.objectDigest(base),old=await m.exportSnapshot(base),workspace=await w.create(base);
 const d=await m.migrateDataset(base,a.cases);
 assert.equal(frozen,'sha256:13e765c81f1340918322b1e985da85f2362da3c72e1997804f952865edf365d2');
 assert.equal(await m.objectDigest(base),frozen);assert.equal(await m.objectDigest(m.legacyBase(d)),frozen);assert.deepEqual(m.validate(d),[]);assert.equal(d.contentItems.length,127);
 assert(await m.verifySnapshot(old,frozen));assert.deepEqual(await w.validate(workspace,d),[]);
 const bundle=await m.exportSnapshot(d);assert(await m.verifySnapshot(bundle));assert.notEqual(bundle.audit.datasetDigest,frozen);assert.equal(bundle.audit.historyValid,true);
 for(const id of ['csp6','water','area'])assert(m.domainForStation(d,id).entities.length>0);
 const metric=m.domainIndex(d).get('csp2035-carbon-per-capita-baseline');assert.equal(metric.data.value,29.9);assert.equal(metric.admission,'PENDING');assert.equal(metric.data.unit,'t_CO2e/person');
 assert(m.queryRelationships(d,metric.id,{direction:'reverse'}).some(a=>a.from==='csp6'));
 const next=await m.commitDomainRevision(d,{id:metric.id,expectedRevisionId:metric.revisionId,patch:{state:'CONTESTED',localNote:'Synthetic QA challenge to provenance completeness'},reason:'Check reversible local review'});
 assert.notEqual(m.domainIndex(next).get(metric.id).revisionId,metric.revisionId);assert.equal(metric.state,'SOURCE_OBSERVED');assert.equal(next.domain.revisions.length,d.domain.revisions.length+1);assert(await m.verifySnapshot(await m.exportSnapshot(next)));
 await assert.rejects(()=>m.commitDomainRevision(next,{id:metric.id,expectedRevisionId:metric.revisionId,patch:{label:'stale'},reason:'stale'}),/DOMAIN_CONFLICT/);
 await assert.rejects(()=>m.commitDomainRevision(d,{id:metric.id,expectedRevisionId:metric.revisionId,patch:{admission:'ADMITTED'},reason:'forged'}),/LOCAL_RESEARCH_FIELDS_ONLY/);
 for(const mutate of [x=>x.domain.entities[0].data.value=999,x=>x.domain.entities[0].admission='ADMITTED',x=>x.domain.assertions[0].to='missing',x=>x.domain.revisions[0].parentRevision=x.domain.revisions.at(-1).id,x=>x.domain.events.reverse()]){const bad=structuredClone(bundle);mutate(bad.dataset);assert.equal(await m.verifySnapshot(bad),false);}
 const edited=await w.commit(workspace,d,{targetId:'water:content',content:{title:'Local synthetic review',text:'QA only'},reason:'Backward compatible editing'});assert.deepEqual(await w.validate(edited,base),[]);
 assert.deepEqual(await m.migrateDataset(d,a.cases),d);
 console.log('PASS: additive domain migration, 127-item/base digest preservation, legacy workspace/snapshot compatibility, versioned accounting provenance/reverse links, immutable local reviews, stale/forged/corrupt history rejection');
})().catch(e=>{console.error(e);process.exitCode=1});
