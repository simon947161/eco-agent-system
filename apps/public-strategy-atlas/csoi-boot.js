/* Verified default snapshot cache. Same Atlas data/history, no alternative graph. */
(function(root){'use strict';
const M=typeof module!=='undefined'?require('./atlas-model.js'):root.AtlasModel;
async function load(seed,inputs,fixture=null,release=null){
 if(seed?.format!=='csoi-default-snapshot-cache-1'||seed.inputDigest!==await M.objectDigest(inputs)||!await M.verifySnapshot(seed.snapshot))throw Error('BOOT_CACHE_INVALID_OR_STALE');
 if(await M.objectDigest(M.legacyBase(seed.snapshot.dataset))!==await M.objectDigest(inputs.base))throw Error('BOOT_BASE_MISMATCH');
 if(!fixture&&release)return publishedDefaults(seed.snapshot.dataset,release.first,release.packed);
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
 // Export already validates the full domain, event chain and all content roots.
 // Compare its independently calculated digest with the release commitment.
 const verified=await M.exportSnapshot(next).catch(()=>null);
 if(verified?.audit.datasetDigest!==delta.datasetDigest)throw Error('EDITION_SUFFIX_INVALID');
 return structuredClone(next);
}
async function publishedDefaults(dataset,first,packed){
 if(!packed)return appendEditionSuffix(dataset,first);
 if(!Number.isSafeInteger(packed.byteLength)||packed.byteLength<1||packed.byteLength>4000000||typeof packed.compressed!=='string'||packed.compressed.length>1000000)throw Error('PROJECT_REGISTER_CACHE_INVALID');
 const bytes=Uint8Array.from(atob(packed.compressed),c=>c.charCodeAt(0));
 const reader=new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip')).getReader();
 const chunks=[];let size=0;
 try{
  for(;;){const part=await reader.read();if(part.done)break;size+=part.value.length;if(size>packed.byteLength)throw Error('PROJECT_REGISTER_CACHE_LENGTH');chunks.push(part.value);}
 }finally{await reader.cancel();}
 if(size!==packed.byteLength)throw Error('PROJECT_REGISTER_CACHE_LENGTH');
 const second=JSON.parse(await new Blob(chunks).text());
 if(second.baseDigest!==first.datasetDigest||second.format!==first.format||second.sources.length||second.sourceEvents.length)throw Error('PROJECT_REGISTER_CACHE_PARENT');
 return appendEditionSuffix(dataset,{...first,datasetDigest:second.datasetDigest,revisions:first.revisions.concat(second.revisions),events:first.events.concat(second.events)});
}
const api={load,appendEditionSuffix,publishedDefaults};root.AtlasCSOIBoot=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
