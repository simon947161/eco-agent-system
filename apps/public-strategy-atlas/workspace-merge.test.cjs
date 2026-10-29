const assert=require('node:assert/strict'),W=require('./atlas-workspace.js'),D=require('./atlas-data.js');
(async()=>{
 const base=await W.create(D),id='water:content';
 const local=await W.commit(base,D,{targetId:id,content:{title:'Local title',text:'Local text'},reason:'Local branch'});
 const incoming=await W.commit(base,D,{targetId:id,content:{title:'Imported title',text:'Imported text'},reason:'Import branch'});
 const preview=await W.previewMerge(local,incoming,D);assert.equal(preview.commonRevisionCount,0);assert.equal(preview.targets.length,1);assert.equal(preview.targets[0].fields.filter(f=>f.conflict).length,2);
 await assert.rejects(()=>W.resolveMerge(local,incoming,D,{preview,resolutions:{},reason:'Missing choices'}),/EXPLICIT_FIELD/);
 const merged=await W.resolveMerge(local,incoming,D,{preview,resolutions:{[id]:{title:'LOCAL',text:'IMPORT'}},reason:'Explicit field resolution'});
 assert.deepEqual(await W.validate(merged,D),[]);assert.equal(W.head(merged,id).action,'RESOLVE');assert.equal(W.head(merged,id).content.title,'Local title');assert.equal(W.head(merged,id).content.text,'Imported text');assert.equal(merged.revisions[0].digest,local.revisions[0].digest);assert.deepEqual(merged.mergeRecords[0].importedWorkspace,incoming);
 assert.deepEqual(await W.importWorkspace(JSON.stringify(merged),D),merged);assert(W.extendsHistory(local,merged));
 const newer=await W.commit(local,D,{targetId:id,expectedHead:W.head(local,id).digest,content:{title:'Newer',text:'Newer'},reason:'Advance local'});
 await assert.rejects(()=>W.resolveMerge(newer,incoming,D,{preview,resolutions:{[id]:{title:'LOCAL',text:'IMPORT'}},reason:'Stale preview'}),/MERGE_PREVIEW_STALE/);
 for(const mutate of [x=>x.mergeRecords[0].importedWorkspace.revisions[0].content.title='forged',x=>x.mergeRecords[0].resolutions[id].text='LOCAL',x=>x.revisions.at(-1).resolutionReceiptDigest='sha256:'+'0'.repeat(64),x=>x.events.at(-1).type='APPROVED',x=>x.officialStatus='ADMITTED']){const bad=structuredClone(merged);mutate(bad);assert((await W.validate(bad,D)).length>0);}
 const follow=await W.commit(merged,D,{targetId:id,expectedHead:W.head(merged,id).digest,content:{title:'After merge',text:'Retain archives'},reason:'Normal edit after merge'});assert.deepEqual(await W.validate(follow,D),[]);
 console.log('PASS: checkpoint-bound three-way preview, explicit field choices, archived imported history, appended RESOLVE events, old workspace compatibility, stale preview and corruption/promotion rejection');
})().catch(e=>{console.error(e);process.exitCode=1});
