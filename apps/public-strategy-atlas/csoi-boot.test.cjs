const assert=require('node:assert/strict'),M=require('./atlas-model.js'),B=require('./csoi-boot.js'),Build=require('./tools/build-csoi-boot.cjs');
(async()=>{
 const seed=require('./sources/csoi-default-snapshot.js'),inputs=Build.inputs();assert.deepEqual(seed,await Build.build());
 const d=await B.load(seed,inputs);assert.equal(await M.objectDigest(d),'sha256:621a3a17781a60ae7b18f0006fc98cf498292b1f5d49ae52e4c4776478f967dd');assert.equal(d.domain.entities.length,135);assert(await M.verifySnapshot(await M.exportSnapshot(d)));
 const fixture={count:60,options:{shape:'chain',table:true}},fast=await B.load(seed,inputs,fixture),rebuilt=await require('./csoi-intake.js').registerSummaries(await M.migrateDataset(M.densityFixture(inputs.base,fixture.count,fixture.options),inputs.cases,inputs.catalogue),inputs.observations);assert.deepEqual(fast,rebuilt);assert.equal(fast.contentItems.length,187);assert.deepEqual(fast.domain.revisions,d.domain.revisions);
 const wrong=structuredClone(seed);wrong.snapshot.dataset.domain.entities[0].label='Corrupted cache';await assert.rejects(()=>B.load(wrong,inputs),/BOOT_CACHE_INVALID/);
 const stale=structuredClone(inputs);stale.outlines[2].nodes[0].summary+=' Changed source input.';await assert.rejects(()=>B.load(seed,stale),/BOOT_CACHE_INVALID_OR_STALE/);await assert.rejects(()=>B.load(seed,inputs,{count:999,options:{}}),/DENSITY_BOUNDS/);
 d.domain.entities[0].label='Independent caller mutation';assert.notEqual(seed.snapshot.dataset.domain.entities[0].label,d.domain.entities[0].label);
 console.log('PASS: startup cache equals full registration, synthetic fixture equals rebuilt history/base, exact default digest, isolated clones and stale/tampered/unsupported cache rejection');
})().catch(e=>{console.error(e);process.exitCode=1});
