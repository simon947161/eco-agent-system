const assert=require('node:assert/strict');
const path=require('node:path');
const P=require('./atlas-page-index.js'), B=require('./csoi-boot.js'), I=require('./atlas-intake.js');
const roots=require('./sources/pdf-page-roots.js');
const prior=require('./sources/csoi-default-snapshot.js').snapshot.dataset;
const suffix=require('./sources/plan-edition-suffix.js');
function read(id){return require(path.join(__dirname,'sources/pdf-page-receipts',roots[id].rawDigest.slice(7)+'.json'));}
async function main(){
 const d=await B.appendEditionSuffix(prior,suffix);
 let pages=0;
 for(const id of Object.keys(roots)){
  const body=await P.verify(d,id,read(id));
  pages+=body.pages.length;
  assert.equal(P.pageView(d,id,body,1).page,1);
  assert.equal(P.pageView(d,id,body,body.pages.length).page,body.pages.length);
  assert.throws(()=>P.pageView(d,id,body,0),/OUT_OF_RANGE/);
 }
 assert.equal(pages,1962);
 const id='csoi:smrc-op-2026:20261128', body=read(id);
 assert(!P.edition(prior,id));
 const project=P.pageView(d,id,body,68);
 assert(project.anchored.some(e=>e.kind==='Project'));
 const historical=P.pageView(d,id,body,9);
 assert.equal(historical.historicalMatch.page,9);assert(!historical.anchored.length);
 assert.equal(P.pageView(d,id,body,2).historicalMatch,null);
 const changed=structuredClone(body);changed.pages.reverse();
 await assert.rejects(()=>P.verify(d,id,changed),/MISMATCH/);
 assert.throws(()=>P.pageView(d,id,changed,1),/MISMATCH/);
 const sourceCatalogue=await I.correctStage(d.domain.sourceCatalogue,id,'SOURCE_RETRIEVED',{actor:'QA',at:'2026-11-28T00:00:00Z',reason:'Withdraw the byte check'});
 const withdrawn={...d,domain:{...d.domain,sourceCatalogue}};
 assert.equal(P.pageView(withdrawn,id,body,68).current,false);
 console.log('PASS 12 verified source indexes, 1962 pages, pinned current and earlier readings, missing/withdrawn editions and changed page order');
}
main().catch(e=>{console.error(e);process.exitCode=1;});
