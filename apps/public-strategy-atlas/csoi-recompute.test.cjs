const assert=require('node:assert/strict'),M=require('./atlas-model.js'),L=require('./csoi-layers.js'),G=require('./csoi-governance.js');
(async()=>{
 const d=await M.migrateDataset(require('./atlas-data.js'),require('./atlas-accounting.js').cases,require('./sources/public-catalogue.json')),{dataset,records}=await L.demo(d),q=records.find(r=>r.layer==='L3');
 assert((await L.verifyDerivation(dataset,q)).integrity);
 // Re-signing a false calculation cannot defeat independent formula replay.
 const {revisionId,...payload}=structuredClone(q);payload.data.receipt.result.value=1;payload.data.measurement.value=1;
 const {digest,...receipt}=payload.data.receipt;payload.data.receipt.digest=await M.objectDigest(receipt);const forged=await G.makeRecord(payload);
 assert(await G.verifyRecord(forged));assert.equal((await L.verifyDerivation(dataset,forged)).integrity,false);
 assert((await L.verifyCurrent(dataset,forged)).reasons.includes('CALCULATION_RECOMPUTATION_FAILED'));
 const source=records.find(r=>r.layer==='L0'),withdrawn=await L.revise(source,{state:'WITHDRAWN',reason:'Withdraw synthetic source',observedAt:'2026-10-30T01:00:00Z'}),changed=await L.register(dataset,withdrawn);
 assert.equal((await L.verifyCurrent(changed,q)).current,false);assert((await L.verifyDerivation(changed,q)).integrity);assert(await M.verifySnapshot(await M.exportSnapshot(changed)));
 console.log('PASS: independently recomputed pinned historical layer receipts reject self-consistent false math; source changes invalidate current use while historical exports remain verifiable');
})().catch(e=>{console.error(e);process.exitCode=1});
