/* Bounded OP page/unit reading in the existing immutable research domain. */
(function(root){'use strict';
const M=typeof module!=='undefined'?require('./atlas-model.js'):root.AtlasModel,K=typeof module!=='undefined'?require('./csoi-knowledge.js'):root.AtlasCSOIKnowledge;
function manifest(){return typeof module!=='undefined'?require('./sources/op-completion-review.json'):root.CsoiOpCompletionReview;}
function project(source,review=manifest()){
 const next=structuredClone(source),base=next.find(b=>b.sourceId===review.sourceId);if(!base||base.sourceRevision!==review.sourceRevision||base.sourcePageCount!==142)throw Error('OP_REVIEW_SOURCE_MISMATCH');
 const ids=new Set(base.records.map(n=>n.id));for(const n of review.records){if(ids.has(n.id))throw Error('OP_REVIEW_DUPLICATE');ids.add(n.id);base.records.push(structuredClone(n));}K.validateBundle(base);return next;
}
async function apply(dataset,source,review=manifest()){return K.registerBundle(dataset,project(source,review).find(b=>b.sourceId===review.sourceId));}
function nodeOf(e){const r=e.data.csoiRecord.data,c=r.publicKnowledge;return {id:e.id,kind:e.kind,category:c.category,code:c.code,parentId:c.parentId,title:r.title,summary:r.summary,locator:r.locator,anchor:c.anchor,facts:c.facts,relations:c.relations.map(({targetRevisionId,...x})=>x)};}
function isCurrentContent(e,review=manifest()){const n=review.records.find(x=>x.id===e.id);return !!n&&M.canonical(nodeOf(e))===M.canonical(n);}
async function unitMatrix(dataset,review=manifest()){
 const byId=M.domainIndex(dataset),rows=[];
 for(const n of review.records.filter(n=>n.category==='OP_PAGE')){const e=byId.get(n.id),matches=!!e&&isCurrentContent(e,review),state=e?await K.status(dataset,e.id):{current:false,reasons:['RECORD_NOT_IMPLEMENTED']};for(const u of n.facts.units)rows.push({id:u.id,pageRecordId:n.id,pdfPage:u.pdfPage,sourcePages:u.pages||[u.pdfPage],sourceSegments:u.sourceSegments||[],category:u.category,title:u.title,sourceId:review.sourceId,sourceRevision:review.sourceRevision,recordRevision:e?.revisionId||null,verification:matches&&state.current?'SOURCE_CHECKED_BOUNDED':!e?'NOT_IMPLEMENTED':!matches?'CONTENT_DIFFERS_FROM_CHECKED_SOURCE':'INVALIDATED',physicalRowIds:u.physicalRowIds||[],sourceAnchors:u.sourceAnchors,conditions:u.conditions,qualifiers:u.qualifiers,cspReferences:u.cspReferences,lspsReferences:u.lspsReferences,existingRecordIds:u.existingRecordIds,currentLegalApplicability:'UNKNOWN',actualPerformance:'UNKNOWN',gaps:[...state.reasons,'CURRENT_VERSION_UNKNOWN','OFFICIAL_ADMISSION_PENDING']});}
 return {format:'csoi-op-unit-coverage-1',basis:review.scope,counts:review.counts,rows,officialRelationships:0,actualOutcome:'UNKNOWN'};
}
const api={manifest,project,apply,nodeOf,isCurrentContent,unitMatrix};root.AtlasOpReview=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
