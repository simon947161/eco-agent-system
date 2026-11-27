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
// The verified previous default stays reproducible for historical imports.
async function appendEditionSuffix(dataset, delta) {
 if (delta?.format !== 'atlas-plan-edition-suffix-1' || !Array.isArray(delta.revisions) ||
     !Array.isArray(delta.events) || delta.revisions.length !== delta.events.length ||
     !Array.isArray(delta.sources) || !Array.isArray(delta.sourceEvents)) throw Error('EDITION_SUFFIX_REQUIRED');
 const base = await M.objectDigest(dataset);
 if (base !== delta.baseDigest) throw Error('EDITION_BASE_MISMATCH');
 const domain = dataset.domain;
 const catalogue = domain.sourceCatalogue;
 const next = {...dataset, domain:{...domain,
  sourceCatalogue:{...catalogue,sources:catalogue.sources.concat(delta.sources),events:catalogue.events.concat(delta.sourceEvents)},
  revisions:domain.revisions.concat(delta.revisions),events:domain.events.concat(delta.events),
  entities:domain.entities.concat(delta.revisions.map(rev => ({...rev.record,revisionId:rev.id})))
 }};
 if (await M.objectDigest(next) !== delta.datasetDigest || !await M.verifySnapshot(await M.exportSnapshot(next))) throw Error('EDITION_SUFFIX_INVALID');
 return structuredClone(next);
}
const api={load,appendEditionSuffix};root.AtlasCSOIBoot=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
