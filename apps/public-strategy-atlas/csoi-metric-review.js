/* A bounded second source review appends revisions; the published v2 records stay in history. */
(function(root){'use strict';
const M=typeof module!=='undefined'?require('./atlas-model.js'):root.AtlasModel,K=typeof module!=='undefined'?require('./csoi-knowledge.js'):root.AtlasCSOIKnowledge,G=typeof module!=='undefined'?require('./csoi-governance.js'):root.AtlasCSOIGovernance;
const supplied=typeof module!=='undefined'?require('./sources/csp-indicator-review.json'):root.CsoiCspIndicatorReview;
const PLAN=structuredClone(supplied);
function freeze(v){if(v&&typeof v==='object'){Object.freeze(v);for(const x of Object.values(v))freeze(x);}return v;}freeze(PLAN);
function need(ok,code){if(!ok)throw Error(code);}
function nodeOf(e){const r=e.data.csoiRecord,d=r.data,c=d.publicKnowledge;return {id:e.id,kind:e.kind,category:c.category,code:c.code,parentId:c.parentId,title:d.title,summary:d.summary,locator:d.locator,anchor:c.anchor,facts:c.facts,relations:c.relations.map(({targetRevisionId,...x})=>x)};}
function validate(plan=PLAN){
 need(plan?.format==='csoi-csp-indicator-review-1'&&plan.officialAdmission==='PENDING'&&plan.currentLegalApplicability==='UNKNOWN'&&plan.method==='INDEPENDENT_AI_SOURCE_REVIEW_NOT_OFFICIAL'&&Array.isArray(plan.records)&&plan.records.length===63,'METRIC_REVIEW_MANIFEST');
 const seen=new Set();for(const row of plan.records){const n=row.node;need(n&&n.id===row.id&&n.category==='CSP_INDICATOR'&&!seen.has(row.id)&&/^sha256:[a-f0-9]{64}$/.test(row.beforeNodeDigest||'')&&typeof row.reason==='string'&&row.reason.length>0,'METRIC_REVIEW_ROW');K.validateNode(n);need(n.facts.semanticReview?.reviewId===plan.reviewId&&n.facts.semanticReview.sourceRevision===plan.sourceRevision,'METRIC_REVIEW_SOURCE');seen.add(row.id);}return true;
}
function project(bundles,plan=PLAN){
 validate(plan);const copy=structuredClone(bundles),bundle=copy.find(b=>b.sourceId===plan.sourceId);need(bundle&&bundle.sourceRevision===plan.sourceRevision,'METRIC_REVIEW_BUNDLE');const byId=new Map(plan.records.map(r=>[r.id,r.node]));need(bundle.records.filter(n=>n.category==='CSP_INDICATOR').every(n=>byId.has(n.id)),'METRIC_REVIEW_CENSUS');bundle.records=bundle.records.map(n=>byId.has(n.id)?structuredClone(byId.get(n.id)):n);K.validateBundle(bundle);return copy;
}
async function apply(dataset,plan=PLAN){
 validate(plan);need(await M.verifySnapshot(await M.exportSnapshot(dataset)),'METRIC_REVIEW_DATASET');let next=dataset;const changes=[];
 for(const row of plan.records){
  const old=M.domainIndex(next).get(row.id);need(old?.data?.csoiRecord?.data?.publicKnowledge,'METRIC_REVIEW_MISSING_RECORD');
  const current=nodeOf(old),after=row.node;if(M.canonical(current)===M.canonical(after))continue;
  need(await M.objectDigest(current)===row.beforeNodeDigest,'METRIC_REVIEW_CONCURRENT_EDIT');
  const oldRecord=old.data.csoiRecord;need(oldRecord.data.sourceId===plan.sourceId&&oldRecord.data.sourceDigest===plan.sourceRevision&&(await K.status(next,row.id)).current,'METRIC_REVIEW_SOURCE_OR_PARENT_STALE');
  need(current.title===after.title&&current.id===after.id&&current.kind===after.kind&&current.parentId===after.parentId&&current.locator===after.locator&&M.canonical(current.anchor)===M.canonical(after.anchor)&&M.canonical(current.relations)===M.canonical(after.relations),'METRIC_REVIEW_IDENTITY_CHANGE');
  const data={...structuredClone(oldRecord.data),summary:after.summary,publicKnowledge:{...structuredClone(oldRecord.data.publicKnowledge),facts:structuredClone(after.facts)}};data.measurement=K.measurement(after,oldRecord.scope);
  const record=await G.makeRecord({...oldRecord,data,observedAt:plan.observedAt});next=await M.reviseResearchRecord(next,{id:row.id,expectedRevisionId:old.revisionId,record,reason:row.reason});
  const revised=M.domainIndex(next).get(row.id);changes.push({id:row.id,oldRevision:old.revisionId,newRevision:revised.revisionId,reason:row.reason});
 }
 need((await K.verifyStructure(next)).integrity&&await M.verifySnapshot(await M.exportSnapshot(next)),'METRIC_REVIEW_RESULT');return {dataset:next,changes};
}
const api={manifest:PLAN,validate,project,apply,nodeOf};root.AtlasCspMetricReview=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
