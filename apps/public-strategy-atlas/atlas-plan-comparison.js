// A read-only comparison of already registered project rows; no graph writes.
(function(root) {
'use strict';
const commonJS = typeof module !== 'undefined';
const M = commonJS ? require('./atlas-model.js') : root.AtlasModel;
const K = commonJS ? require('./csoi-knowledge.js') : root.AtlasCSOIKnowledge;
const P = commonJS ? require('./csoi-paths.js') : root.AtlasCSOIPaths;
const E = commonJS ? require('./atlas-execution.js') : root.AtlasExecution;
const pin = item => ({id:item.id,revisionId:item.revisionId});
function projectView(dataset,id) {
 const records=M.domainIndex(dataset), item=records.get(id), capsule=item?.data?.csoiRecord?.data?.publicKnowledge;
 if(capsule?.category!=='PLAN_PROJECT') throw Error('PRINTED_PROJECT_REQUIRED');
 const publication=records.get(capsule.parentId);
 const doc=publication?.data?.csoiRecord?.data?.publicKnowledge;
 const source=dataset.domain.sourceCatalogue.sources.find(s=>s.id===item.data.csoiRecord.data.sourceId);
 if(doc?.category!=='PLAN_EDITION'||!source) throw Error('EDITION_REQUIRED');
 const children=K.children(dataset,id,{limit:100});
 if(children.nextOffset!==null) throw Error('PROJECT_CHILD_LIMIT');
 const amounts=children.items.filter(e=>e.data.csoiRecord.data.publicKnowledge.category==='PLAN_BUDGET');
 const resources=children.items.filter(e=>e.data.csoiRecord.data.publicKnowledge.category==='PLAN_RESOURCES');
 const deps=P.assessDependencies(dataset,[item,...children.items]);
 return {project:pin(item),projectLabel:item.label,document:pin(publication),source:pin(source),rawDigest:source.rawDigest,url:source.officialUrl,
  documentLabel:source.title,editionDate:doc.facts.editionDate,versionConflict:doc.facts.versionConflict,page:capsule.anchor.pdfPage,
  region:source.geographicExtent.label,locality:capsule.facts.locality,resolution:capsule.facts.resolution,period:capsule.facts.projectPeriod,
  purpose:capsule.facts.plannedOutput,condition:capsule.facts.condition,
  goal:capsule.relations.filter(r=>r.type==='EXPLICIT_DOCUMENT_REFERENCE').map(r=>({id:r.targetId,revisionId:r.targetRevisionId})),
  budget:amounts.map(e=>({record:pin(e),basis:e.data.csoiRecord.data.publicKnowledge.facts.budgetBasis,amount:e.data.value,currency:e.data.unit,period:e.data.period})),
  resources:resources.map(e=>({record:pin(e),basis:e.data.csoiRecord.data.publicKnowledge.facts.resourceBasis})),
  currentInputs:deps.current,invalidations:deps.invalidations,limitations:deps.gaps};
}
async function compare(dataset,{left,right,locality,asOf}) {
 if(left===right||typeof locality!=='string'||!locality.trim()||locality.length>180||!/^\d{4}-\d\d-\d\d$/.test(asOf)||!Number.isFinite(Date.parse(asOf))||new Date(asOf).toISOString().slice(0,10)!==asOf) throw Error('PROJECT_COMPARISON_CONTEXT');
 const sides=[projectView(dataset,left),projectView(dataset,right)];
 const [a,b]=sides;
 const checks=[
  ['DIFFERENT_DOCUMENT_EDITIONS',a.source.id!==b.source.id],
  ['MATCHING_LOCALITY',sides.every(s=>s.locality===locality)&&a.region===b.region],
  ['MATCHING_PRINTED_RESOLUTION',a.resolution===b.resolution&&a.resolution!=='UNKNOWN'],
  ['MATCHING_PLANNED_WORK',a.purpose===b.purpose&&a.purpose!=='UNKNOWN'],
  ['SHARED_PRINTED_CSP_REFERENCE',a.goal.some(goal=>b.goal.some(other=>other.id===goal.id&&other.revisionId===goal.revisionId))],
  ['EDITIONS_AVAILABLE_BY_SELECTED_DATE',sides.every(s=>s.editionDate<=asOf)],
  ['OVERLAPPING_DELIVERY_PERIOD',a.period===b.period&&sides.every(s=>{
   const range=E.timeRange({data:{period:'FY'+s.period.replace('/','-')}});
   return range && range.from<=asOf && range.to>=asOf;
  })],
  ['CURRENT_INPUT_PINS',sides.every(s=>s.currentInputs)]
 ].map(([name,passes])=>({name,passes}));
 const record={format:'atlas-published-project-comparison-1',rule:'printed-plan-project-1',query:{left,right,locality,asOf},sides,checks,
  status:checks.every(c=>c.passes)?'SUPPORTED_RESEARCH_CANDIDATE':'REJECTED_CANDIDATE',
  counterevidence:sides.map(s=>s.versionConflict), alternative:'One resolution or strategy can cover several work items.',
  falsifier:'A different locality, delivery period, work purpose, source correction or budget allocation can defeat the proposed match.',
  budgetTreatment:'KEEP_SEPARATE_NO_ADDITION',actualSpend:'UNKNOWN',actualOutput:'UNKNOWN',actualOutcome:'UNKNOWN',officialRelationship:'PENDING'};
 return {...record,digest:await M.objectDigest(record)};
}
async function verify(dataset,receipt) {
 try {return M.canonical(await compare(dataset,receipt.query))===M.canonical(receipt);} catch {return false;}
}
const api={projectView,compare,verify};
root.AtlasPlanComparison=api;
if(commonJS) module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
