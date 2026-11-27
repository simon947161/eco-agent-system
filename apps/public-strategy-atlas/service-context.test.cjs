const assert=require('node:assert/strict');
const M=require('./atlas-model.js'), I=require('./atlas-intake.js'), K=require('./csoi-knowledge.js');
const S=require('./csoi-strategy-research.js'), B=require('./csoi-boot.js'), P=require('./atlas-plan-comparison.js');
const historical=require('./sources/csoi-default-snapshot.js').snapshot.dataset;
const suffix=require('./sources/plan-edition-suffix.js');
async function run() {
 const data=await B.appendEditionSuffix(historical,suffix);
 const contexts=P.serviceContext(data);
 assert.equal(contexts.length,5);assert(contexts.every(r=>r.current));
 const reported=contexts.find(r=>r.unit==='samples');
 assert.equal(reported.value,536);assert.equal(reported.period,'FY2024-25');
 const asset='csoi:knowledge:service-context:asset';
 const leaf=K.subtreePage(data,asset,{query:'reservoir'}).items[0];
 assert.equal(leaf.data.value,25);assert.equal(K.parents(data,leaf.id).length,4);
 assert.deepEqual(K.subtreePage(data,leaf.id).items,[]);
 assert.equal(K.subtreePage(data,asset).items.length,1);
 const narrow=K.subtreePage(data,asset+':section:2',{limit:1});
 assert.equal(narrow.nextOffset,1);
 const scoped=S.releaseBundles().filter(b=>!S.bundles().some(old=>old.sourceId===b.sourceId));
 const coverage=await S.matrix(data,scoped);
 assert.equal(coverage.rows.length,20);
 assert(coverage.rows.every(r=>r.verification==='SOURCE_CHECKED_BOUNDED'));
 assert((await S.matrix(historical,scoped)).rows.every(r=>r.implemented==='MISSING'));
 assert.equal(S.select(data,{family:'ANNUAL_REPORT'}).total,3);
 const changed={...data,domain:{...data.domain,sourceCatalogue:await I.correctStage(data.domain.sourceCatalogue,'csoi:smrc-water-amp-2025:20261030','SOURCE_RETRIEVED',{actor:'QA',at:'2026-11-28T00:00:00Z',reason:'Isolate a withdrawal'})}};
 assert(P.serviceContext(changed).filter(r=>r.record.id.startsWith(asset)).every(r=>!r.current));
 assert(P.serviceContext(changed).find(r=>r.unit==='samples').current);
 // Directly exercise the iterative public containment query without fabricating Council data.
 const depth=6000, entities=[];
 for(let i=0;i<depth;i++) entities.push({id:'fixture-'+i,label:'Synthetic '+i,data:{csoiRecord:{data:{publicKnowledge:{parentId:i?'fixture-'+(i-1):null,code:String(i)},summary:'Synthetic',locator:'Synthetic'}}}});
 const deep={domain:{entities}};
 assert.equal(K.subtreePage(deep,'fixture-0',{query:'Synthetic 5999'}).items[0].id,'fixture-5999');
 assert.equal(K.parents(deep,'fixture-5999').length,depth);
 console.log('PASS three real service sources, five scope-bounded findings, twenty release coverage rows and old-snapshot gaps, independent withdrawals, 6,000-level public containment query');
}
run().catch(e=>{console.error(e);process.exitCode=1;});
