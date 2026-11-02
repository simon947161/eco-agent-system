/* Projections of source-primary research in the existing domain, not a second graph. */
(function(root){'use strict';
const M=typeof module!=='undefined'?require('./atlas-model.js'):root.AtlasModel,K=typeof module!=='undefined'?require('./csoi-knowledge.js'):root.AtlasCSOIKnowledge;
const LEGACY_CARBON='csp2035-carbon-per-capita-baseline';
function bundles(){return typeof module!=='undefined'?[require('./sources/csp-public-knowledge.json'),require('./sources/lsps-public-knowledge.json'),require('./sources/op-water-public-knowledge.json')]:[root.CsoiCspKnowledge,root.CsoiLspsKnowledge,root.CsoiOpWaterKnowledge];}
function capsule(e){return e?.data?.csoiRecord?.data?.publicKnowledge||null;}
function canonicalCarbon(source=bundles()){return source[0].records.find(n=>n.category==='CSP_INDICATOR'&&n.anchor.pdfPage===30&&n.facts.baseline?.value===29.9);}
async function registerAll(dataset,source=bundles()){
 let next=dataset;for(const bundle of source)next=await K.registerBundle(next,bundle);
 const old=M.domainIndex(next).get(LEGACY_CARBON),replacement=canonicalCarbon(source);
 if(!replacement)throw Error('CANONICAL_CARBON_SOURCE_REQUIRED');
 if(old&&old.state!=='SUPERSEDED')next=await M.commitDomainRevision(next,{id:old.id,expectedRevisionId:old.revisionId,patch:{state:'SUPERSEDED',localNote:'Retained unpinned historical observation. Use source-pinned research record '+replacement.id+'. This correction does not admit arithmetic, current law or actual Council emissions.'},reason:'Append a supersession marker after independently checking the canonical CSP indicator; retain original value, source gap and immutable history.',observedAt:'2026-11-01T23:12:00.000Z'});
 return next;
}
function family(bundle){return bundle.sourceId.includes('csp-full')?'CSP':bundle.sourceId.includes('lsps')?'LSPS':'OP';}
function group(n){return n.category==='ACTION'?(n.facts.sourceSection==='IMPLEMENTATION_TABLE'?'LSPS_IMPLEMENTATION_ACTION':'LSPS_OTHER_ACTION_OCCURRENCE'):n.category;}
async function matrix(dataset,source=bundles()){
 const byId=M.domainIndex(dataset),rows=[];
 for(const b of source){K.validateBundle(b);for(const n of b.records){
  const e=byId.get(n.id),c=capsule(e),data=e?.data?.csoiRecord?.data;
  const matched=!!c&&data.sourceId===b.sourceId&&data.sourceDigest===b.sourceRevision&&data.locator===n.locator&&c.category===n.category&&M.canonical(c.anchor)===M.canonical(n.anchor)&&M.canonical(c.facts)===M.canonical(n.facts)&&c.code===n.code&&c.parentId===n.parentId&&M.canonical(c.relations.map(({targetRevisionId,...r})=>r))===M.canonical(n.relations)&&e.kind===n.kind&&data.title===n.title&&data.summary===n.summary;
  let state={current:false,reasons:['RECORD_NOT_IMPLEMENTED']};if(c)try{state=await K.status(dataset,n.id);}catch{state={current:false,reasons:['RECORD_CONTEXT_INVALID']};}
  rows.push({id:n.id,family:family(b),category:group(n),code:n.code,title:n.title,sourceId:b.sourceId,sourceVersion:b.sourceRevision,pdfPage:n.anchor.pdfPage,pageDigest:n.anchor.normalizedPageDigest,locator:n.locator,recordedLocator:data?.locator||null,recordRevision:e?.revisionId||null,extracted:'SOURCE_PRIMARY_RECONSTRUCTION',implemented:e?'PRESENT':'MISSING',verification:matched&&state.current?'SOURCE_CHECKED_BOUNDED':!e?'NOT_IMPLEMENTED':!matched?'CONTENT_DIFFERS_FROM_CHECKED_SOURCE':'INVALIDATED',sourceAndParentPins:state.current?'CURRENT':'STALE_OR_MISSING',gaps:[...(!matched&&e?['CONTENT_DIFFERS_FROM_CHECKED_SOURCE']:[]),...state.reasons,'CURRENT_VERSION_UNKNOWN','OFFICIAL_ADMISSION_PENDING'],sourceAnomalies:n.facts.sourceAnomalies||n.facts.sourceConflictIds||[],actualCouncilPerformance:'UNKNOWN'});
 }}
 const categories=[...new Set(rows.map(r=>r.category))].map(category=>{const all=rows.filter(r=>r.category===category);return {category,expected:all.length,implemented:all.filter(r=>r.implemented==='PRESENT').length,sourceCheckedCurrent:all.filter(r=>r.verification==='SOURCE_CHECKED_BOUNDED').length,missing:all.filter(r=>r.implemented==='MISSING').length,invalidated:all.filter(r=>r.implemented==='PRESENT'&&r.verification!=='SOURCE_CHECKED_BOUNDED').length};});
 return {format:'csoi-item-coverage-1',basis:'Individually checked source items; counts do not certify full-document meaning, current law, implementation or outcomes.',rows,categories,wholeDocumentUnderstanding:'NOT_CLAIMED',officialRelationships:0,actualOutcome:'UNKNOWN'};
}
function publishedReferences(dataset){return K.records(dataset).filter(e=>capsule(e).category==='WATER_ACTIVITY').flatMap(e=>capsule(e).relations.map(r=>({from:e.id,to:r.targetId,type:r.type,locator:r.locator,targetRevision:r.targetRevisionId,meaning:'Printed OP reference only; not proof of implementation, legal authority or causality.'})));}
function matches(e,{family:which,category,q=''}={}){const c=capsule(e),sid=e.data.csoiRecord.data.sourceId;return (!which||family({sourceId:sid})===which)&&(!category||group({...c,facts:c.facts})===category)&&(!q||JSON.stringify([e.id,e.label,e.data.csoiRecord.data.summary,c.code,c.facts]).toLowerCase().includes(q.toLowerCase()));}
function select(dataset,{family:which,category,q='',page=1,limit=25}={}){
 if(!Number.isSafeInteger(page)||page<1||!Number.isSafeInteger(limit)||limit<1||limit>100)throw Error('RESEARCH_QUERY_BOUNDS');
 const items=K.records(dataset).filter(e=>matches(e,{family:which,category,q}));
 return {items:items.slice((page-1)*limit,page*limit),total:items.length,nextPage:page*limit<items.length?page+1:null};
}
const api={bundles,capsule,registerAll,matrix,select,publishedReferences,matches,canonicalCarbon,LEGACY_CARBON};root.AtlasStrategyResearch=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
