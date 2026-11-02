/* Append source-reading context to the original LSPS document; never infer GIS or legal authority. */
(function(root){'use strict';
const M=typeof module!=='undefined'?require('./atlas-model.js'):root.AtlasModel,K=typeof module!=='undefined'?require('./csoi-knowledge.js'):root.AtlasCSOIKnowledge;
function manifest(){return typeof module!=='undefined'?require('./sources/lsps-context-review.json'):root.CsoiLspsContextReview;}
function project(source,review=manifest()){
 const next=structuredClone(source),base=next.find(b=>b.sourceId===review.sourceId);if(!base||base.sourceRevision!==review.sourceRevision||base.sourcePageCount!==118)throw Error('LSPS_CONTEXT_SOURCE_MISMATCH');
 const seen=new Set(base.records.map(n=>n.id));for(const n of review.records){if(seen.has(n.id))throw Error('LSPS_CONTEXT_DUPLICATE');seen.add(n.id);base.records.push(structuredClone(n));}K.validateBundle(base);return next;
}
async function apply(dataset,source,review=manifest()){
 const projected=project(source,review),bundle=projected.find(b=>b.sourceId===review.sourceId);
 return K.registerBundle(dataset,bundle);
}
function nodeOf(e){const r=e.data.csoiRecord.data,c=r.publicKnowledge;return {id:e.id,kind:e.kind,category:c.category,code:c.code,parentId:c.parentId,title:r.title,summary:r.summary,locator:r.locator,anchor:c.anchor,facts:c.facts,relations:c.relations.map(({targetRevisionId,...x})=>x)};}
function isCurrentContent(e,review=manifest()){const n=review.records.find(x=>x.id===e.id);return !!n&&M.canonical(nodeOf(e))===M.canonical(n);}
function scope(base){const review=manifest();return {...base,documents:base.documents.map(d=>d.family==='LSPS'?{...d,scope:review.scope,pages:review.pages}:d)};}
const api={manifest,project,apply,nodeOf,isCurrentContent,scope};root.AtlasLspsContext=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
