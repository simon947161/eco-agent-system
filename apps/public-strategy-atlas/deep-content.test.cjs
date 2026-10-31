const assert=require('node:assert/strict'),fs=require('node:fs'),m=require('./atlas-model.js'),d=require('./atlas-data.js'),w=require('./atlas-workspace.js');
(async()=>{
 const checkpoint=JSON.parse(fs.readFileSync(__dirname+'/qa/legacy-content-roots.json'));
 for(const expected of checkpoint){const actual=await m.contentReceipt(d,expected.id);assert.equal(actual.subtreeDigest,expected.subtreeDigest);assert.equal(actual.itemDigest,expected.itemDigest);}
 const wide=m.densityFixture(d,10000);assert.deepEqual(m.validate(wide),[]);const all=new Set(wide.contentItems.map(c=>c.id));const layout=m.layoutContent(wide,'density:0',{expanded:all,limit:200});assert.equal(layout.nodes.length,200);assert(layout.truncated);
 const paged=m.contentPage(wide,'density:0',{query:'Demo item',offset:50,limit:50});assert.equal(paged.total,9999);assert.equal(paged.items.length,50);assert.equal(paged.nextOffset,100);
 const chain=structuredClone(d);let parent=null;for(let i=0;i<5000;i++){const id='deep:'+i;chain.contentItems.push({id,logicalId:id,versionId:id+':v1',ownerNodeId:'csp',revisionId:'synthetic-v1',parentId:parent,kind:'SECTION',title:'Deep synthetic '+i,text:'Capacity test only; no official text.',status:'SYNTHETIC',observationId:null});parent=id;}
 assert.deepEqual(m.validateContent(chain),[]);assert.equal(m.contentTrail(chain,parent).length,5000);
 const receipt=await m.contentReceipt(chain,'deep:0');assert.equal(receipt.format,'atlas-content-receipt-flat-2');assert.equal(receipt.records.length,5000);assert.doesNotThrow(()=>JSON.stringify(receipt));
 const workspace=await w.create(chain),local=await w.subtreeReceipt(workspace,chain,'deep:0');assert.equal(local.format,'atlas-local-subtree-flat-2');assert.equal(local.records.length,5000);assert.doesNotThrow(()=>JSON.stringify(local));
 const snapshot=await m.exportSnapshot(chain);assert(await m.verifySnapshot(JSON.parse(JSON.stringify(snapshot))));
 const before=receipt.subtreeDigest;chain.contentItems.at(-1).text+=' Changed descendant.';assert.notEqual((await m.contentReceipt(chain,'deep:0')).subtreeDigest,before);
 chain.contentItems.find(c=>c.id==='deep:0').parentId=parent;assert(m.validateContent(chain).some(i=>i.startsWith('CONTENT_CYCLE')));
 console.log('PASS: exact legacy receipt hashes, 10000-wide indexed pagination/bounded layout, 5000-level iterative traversal/local+source receipts, flat deep snapshot roundtrip and ancestor mutation/cycle rejection');
})().catch(e=>{console.error(e);process.exitCode=1});
