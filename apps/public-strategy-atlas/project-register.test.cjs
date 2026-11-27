const assert=require('node:assert/strict');
const M=require('./atlas-model.js'),I=require('./atlas-intake.js'),R=require('./atlas-project-register.js'),B=require('./csoi-boot.js');
const historical=require('./sources/csoi-default-snapshot.js').snapshot.dataset,suffix=require('./sources/plan-edition-suffix.js');
async function main(){
 const base=await B.appendEditionSuffix(historical,suffix),published=await B.publishedDefaults(historical,suffix,require('./sources/project-register-cache.js'));
 assert.equal(published.domain.entities.length,918);
 assert.deepEqual(R.releaseInventory(published).map(r=>r.present),[148,117]);
 assert(R.releaseInventory(historical).every(r=>!r.currentSource&&r.present===0));
 const nodes=M.domainIndex(published);
 for(const [family,total] of [['DP',148],['OP',117]]){
  const table=await R.verify(family,require('./sources/project-table-'+family.toLowerCase()+'.json'));
  assert.equal(R.search(family,table).total,total);
  assert.equal(R.coverage(published,family,table).registered,total);
  assert.equal(R.coverage(base,family,table).registered,1);
  for(const row of table.rows)assert(nodes.has(R.identity(family,row)));
  const selected=R.search(family,table,{code:'6.2',query:'aquatic weed'}).rows[0];
  assert.equal(selected.amountAUD,family==='DP'?60000:20000);
  const id=R.identity(family,selected),prior=nodes.get(id),goal='csoi:knowledge:csp2035:strategy:6.2';
  assert(prior.data.csoiRecord.inputs.some(i=>i.id===goal));
  assert.equal(await R.add(published,family,table,[R.key(selected)]),published);
  const smaller=await R.add(base,family,table,[R.key(selected)]);
  assert.equal(M.domainIndex(smaller).get(id).revisionId,prior.revisionId);
  const changed=structuredClone(table);changed.rows[0].amountAUD=1;
  await assert.rejects(()=>R.verify(family,changed),/EDITION_MISMATCH/);
  const withdrawn={...base,domain:{...base.domain,sourceCatalogue:await I.correctStage(base.domain.sourceCatalogue,table.sourceId,'SOURCE_RETRIEVED',{actor:'QA',at:'2026-11-28T00:00:00Z',reason:'Withdraw PDF verification'})}};
  await assert.rejects(()=>R.add(withdrawn,family,table,[R.key(selected)]),/SOURCE_NOT_CURRENT/);
  if(family==='OP'){
   assert.equal(table.gaps.length,3);
   assert(table.rows.filter(r=>r.budgetCell.includes('over 2 years')).every(r=>r.amountAUD===null));
  }
 }
 const cache=require('./sources/project-register-cache.js');
 await assert.rejects(()=>B.publishedDefaults(historical,suffix,{...cache,byteLength:300}),/CACHE_LENGTH/);
 console.log('PASS two current editions, 265 project rows, 263 new immutable Projects, retention of existing two identities, review gates, amount qualifiers, printed cross-branch goals, withdrawal and portable cache');
}
main().catch(e=>{console.error(e);process.exitCode=1;});
