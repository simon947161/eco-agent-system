const assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path');
const d=require('./atlas-data.js'),m=require('./atlas-model.js');
(async()=>{
 assert.deepEqual(m.validate(d),[]);
 assert.equal(d.nodes.length,15);
 assert.equal(d.contentItems.length,127);
 for(const n of d.nodes){const root=d.contentItems.find(c=>c.ownerNodeId===n.id&&c.parentId===null);assert(root,n.id);const leaf=d.contentItems.find(c=>c.ownerNodeId===n.id&&c.kind==='EVIDENCE');assert(m.contentTrail(d,leaf.id).length>=6);}
 const leaf='water:evidence',trail=m.contentTrail(d,leaf);assert.deepEqual(trail.map(c=>c.kind),['TOPIC','SECTION','CLAUSE','ACTION','INDICATOR','EVIDENCE']);
 assert.equal(m.contentChildren(d,leaf).length,0);
 const before=await m.contentReceipt(d,'water:content');
 const edited=structuredClone(d);edited.contentItems.find(c=>c.id===leaf).text+=' Synthetic amendment.';
 const after=await m.contentReceipt(edited,'water:content');assert.equal(before.itemDigest,after.itemDigest);assert.notEqual(before.subtreeDigest,after.subtreeDigest);
 assert.equal((await m.contentReceipt(d,'csp:content')).subtreeDigest,(await m.contentReceipt(edited,'csp:content')).subtreeDigest);
 const reordered=structuredClone(d);reordered.contentItems.reverse();assert.equal(before.subtreeDigest,(await m.contentReceipt(reordered,'water:content')).subtreeDigest);
 const cases=[
 ['duplicate',x=>x.contentItems.push(x.contentItems[0]),'CONTENT_ID'],
 ['orphan',x=>x.contentItems[1].parentId='missing','CONTENT_PARENT'],
 ['cycle',x=>x.contentItems[0].parentId=x.contentItems[1].id,'CONTENT_CYCLE'],
 ['official laundering',x=>x.contentItems[0].status='EXPLICIT_OFFICIAL','CONTENT_FIELDS'],
 ['mixed source parent',x=>x.contentItems.find(c=>c.id==='obs-csp-summary-61:clause-61').parentId='csp:content','CONTENT_PARENT'],
 ['wrong observation',x=>x.contentItems.find(c=>c.observationId).observationId='missing','CONTENT_OBSERVATION'],
 ['unknown owner',x=>x.contentItems[0].ownerNodeId='missing','CONTENT_SCOPE'],
 ['duplicate version',x=>x.contentItems[1].versionId=x.contentItems[0].versionId,'CONTENT_FIELDS']
 ];
 for(const [name,edit,code]of cases){const copy=structuredClone(d);edit(copy);assert(m.validate(copy).some(e=>e.startsWith(code)),name);await assert.rejects(()=>m.contentReceipt(copy,'csp:content'));}
 for(const count of [60,200]){
  const fixture=m.densityFixture(d,count);assert.deepEqual(m.validate(fixture),[]);const start=performance.now();
  const all=new Set(fixture.contentItems.map(c=>c.id)),layout=m.layoutContent(fixture,'density:0',{expanded:all});assert.equal(layout.nodes.length,count);assert.equal(layout.edges.length,count-1);assert.equal(layout.truncated,false);
  const partial=m.layoutContent(fixture,'density:0',{expanded:new Set(['density:0'])});assert.equal(partial.nodes.length,4);for(const n of partial.nodes){const full=layout.nodes.find(c=>c.id===n.id);assert.equal(full.x,n.x);assert.equal(full.y,n.y);}
  const capped=m.layoutContent(fixture,'density:0',{expanded:all,limit:20});assert.equal(capped.nodes.length,20);assert(capped.truncated);
  assert.equal(new Set(layout.nodes.map(n=>n.x+','+n.y)).size,count);
  console.log(`PASS: ${count} synthetic content nodes, ${count-1} edges, stable coordinates, bounded truncation (${Math.round(performance.now()-start)}ms)`);
 }
 await assert.rejects(()=>m.contentReceipt(d,'missing'),/CONTENT_NOT_FOUND/);assert.throws(()=>m.densityFixture(d,1001),/DENSITY_BOUNDS/);
 for(const c of d.contentItems)assert(!/[\u4e00-\u9fff]/.test(c.title+c.text),'English content '+c.id);
 for(const n of d.nodes)assert(!/[\u4e00-\u9fff]/.test(n.label+n.sub+n.detail),'English graph '+n.id);
 for(const f of ['index.html','atlas.js'])assert(!/[\u4e00-\u9fff]/.test(fs.readFileSync(path.join(__dirname,f),'utf8')),'English UI '+f);
 const cross=m.findCrossPaths(d);assert.equal(cross.length,1);assert.equal(cross[0].targetId,'candidate');assert.equal(cross[0].branches.length,2);assert.equal(cross[0].evidenceCount,0);assert.equal(cross[0].status,'HYPOTHESIS_ONLY');assert.equal(m.findCrossPaths(d,{includeCandidates:false}).length,0);
 const disconnected=structuredClone(d);disconnected.assertions.find(a=>a.id==='e16').status='CONTRADICTED';assert.equal(m.findCrossPaths(disconnected).length,0);
 const bundle=await m.exportSnapshot(d);assert(await m.verifySnapshot(bundle));assert(await m.verifySnapshot(bundle,bundle.audit.datasetDigest));assert.equal(await m.verifySnapshot(bundle,'sha256:'+'0'.repeat(64)),false);
 const corrupt=structuredClone(bundle);corrupt.contentRoots[0].subtreeDigest='sha256:'+'0'.repeat(64);assert.equal(await m.verifySnapshot(corrupt),false);
 const corruptData=structuredClone(bundle);corruptData.dataset.contentItems[0].text='Modified after export';assert.equal(await m.verifySnapshot(corruptData),false);
 console.log('PASS: export/verify roundtrip, external checkpoint and corrupted dataset/receipt rejection');
 console.log('PASS: 15 decomposable topics, 127 items, six-level trail, child/ancestor tamper propagation, order independence, 8 negative cases, English UI/content');
})().catch(e=>{console.error(e);process.exitCode=1});
