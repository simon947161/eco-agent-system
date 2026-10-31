/* Verified default snapshot cache. Same Atlas data/history, no alternative graph. */
(function(root){'use strict';
const M=typeof module!=='undefined'?require('./atlas-model.js'):root.AtlasModel;
async function load(seed,inputs,fixture=null){
 if(seed?.format!=='csoi-default-snapshot-cache-1'||seed.inputDigest!==await M.objectDigest(inputs)||!await M.verifySnapshot(seed.snapshot))throw Error('BOOT_CACHE_INVALID_OR_STALE');
 if(await M.objectDigest(M.legacyBase(seed.snapshot.dataset))!==await M.objectDigest(inputs.base))throw Error('BOOT_BASE_MISMATCH');
 if(!fixture)return structuredClone(seed.snapshot.dataset);
 // Explicit synthetic fixtures have a new legacy base. The retained domain is
 // identical to rebuilding it over that base; no imported snapshot is rebound.
 const d=M.densityFixture(inputs.base,fixture.count,fixture.options);d.domain=structuredClone(seed.snapshot.dataset.domain);d.domain.baseDigest=await M.objectDigest(M.legacyBase(d));
 if(!await M.verifySnapshot(await M.exportSnapshot(d)))throw Error('BOOT_FIXTURE_INVALID');return d;
}
const api={load};root.AtlasCSOIBoot=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
