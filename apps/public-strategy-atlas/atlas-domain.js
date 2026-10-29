/* Additive AtlasModel registry. Station IDs stay authoritative; no parallel route graph. */
(function(root){
'use strict';
const TYPES=new Set(('StrategicOutcome Goal Objective PolicyRequirement PlanningPriority StatutoryControl Decision ImplementationMechanism Program Project WorkPackage Activity Task Dependency Deliverable Area SpatialUnit PopulationGroup IndustrySector ServiceArea Asset Infrastructure Role ResourceAccount MetricDefinition QuantifiedObservation Assumption Baseline Target Output Outcome ContributionClaim FinancialEntry CostAllocation FundingSource BudgetRevision ActualExpenditure SourceArtifact DocumentRevision ContentBlock EvidenceAnchor RelationshipAssertion CounterEvidence DiscoveryHypothesis ChangeEvent ReviewDecision AuditReceipt').split(' '));
const PREDICATES=new Set(('STATES_GOAL ALIGNS_WITH IMPLEMENTS HAS_ACTIVITY HAS_DEPENDENCY FUNDED_BY RESOURCED_BY MEASURED_BY REPORTS_OUTPUT CONTRIBUTES_TO_OUTCOME EVIDENCED_BY APPLIES_IN_AREA CONSTRAINED_BY_LEP GUIDED_BY_DCP RELEVANT_TO CONTESTED_BY SUPERSEDED_BY RESEARCH_CANDIDATE').split(' '));
const STATES=new Set(['PROPOSED','SOURCE_OBSERVED','IN_REVIEW','APPROVED_FOR_RESEARCH','CONTESTED','SUPERSEDED','RETRACTED','UNKNOWN']);
const CLASSES=new Set(['SYNTHETIC_SCENARIO','PUBLIC_TEXT_OBSERVED','LOCAL_RESEARCH']);
function legacyBase(d){const copy={...d};delete copy.domain;return copy;}
function index(d){return new Map([...d.nodes,...d.contentItems,...(d.domain?.entities||[])].map(r=>[r.id,r]));}
function relationships(d,id,{direction='both'}={}){if(!['forward','reverse','both'].includes(direction))throw Error('DIRECTION');return [...d.assertions,...(d.domain?.assertions||[])].filter(a=>direction==='forward'?a.from===id:direction==='reverse'?a.to===id:a.from===id||a.to===id);}
function validate(d){
 const x=d.domain;if(!x)return [];const errors=[];
 if(x.format!=='atlas-domain-1'||x.algorithmVersion!=='atlas-domain-sha256-1'||!Array.isArray(x.entities)||!Array.isArray(x.assertions)||!Array.isArray(x.revisions)||!Array.isArray(x.events))return ['DOMAIN_FORMAT'];
 if(x.entities.length+x.assertions.length>100000||x.revisions.length>200000)return ['DOMAIN_LIMIT'];
 if(x.sourceCatalogue&&x.sourceCatalogue.sources?.some(s=>!d.nodes.some(n=>n.id===s.stationId)))errors.push('CATALOGUE_STATION');
 const ids=new Set([...d.nodes,...d.contentItems].map(r=>r.id)),stations=new Set(d.nodes.map(n=>n.id)),revisions=new Map(x.revisions.map(r=>[r.id,r]));
 if(revisions.size!==x.revisions.length)errors.push('DOMAIN_DUPLICATE_REVISION');
 for(const r of [...x.entities,...x.assertions]){
  if(!r||typeof r.id!=='string'||!r.id||ids.has(r.id)){errors.push('DOMAIN_ID');continue;}ids.add(r.id);
  if(!STATES.has(r.state)||!CLASSES.has(r.classification)||!stations.has(r.stationId)||!revisions.has(r.revisionId))errors.push('DOMAIN_FIELDS:'+r.id);
  if(r.kind&&!TYPES.has(r.kind))errors.push('DOMAIN_KIND:'+r.id);
  if(r.classification==='PUBLIC_TEXT_OBSERVED'&&(!r.provenance?.url?.startsWith('https://')||!r.provenance?.locator))errors.push('DOMAIN_PROVENANCE:'+r.id);
  if(r.admission!=='PENDING'&&r.admission!=='NOT_APPLICABLE')errors.push('DOMAIN_OFFICIAL_PROMOTION:'+r.id);
 }
 const refIndex=index(d);
 for(const e of x.entities){
  if(!TYPES.has(e.kind)||typeof e.label!=='string'||!e.data||typeof e.data!=='object')errors.push('DOMAIN_ENTITY:'+e.id);
  if(e.data?.status&&!['SYNTHETIC','PUBLIC_TEXT_OBSERVED','UNKNOWN'].includes(e.data.status))errors.push('DOMAIN_DATA_PROMOTION:'+e.id);
  if(e.kind==='QuantifiedObservation'&&(!e.data.unit||e.data.value!=='UNKNOWN'&&!(typeof e.data.value==='number'&&Number.isFinite(e.data.value))))errors.push('DOMAIN_MEASUREMENT:'+e.id);
 }
 for(const a of x.assertions){
  if(!PREDICATES.has(a.predicate)||!ids.has(a.from)||!ids.has(a.to)||!Array.isArray(a.evidenceRefs)||!Array.isArray(a.counterevidenceRefs)||!a.method||!a.scope)errors.push('DOMAIN_ASSERTION:'+a.id);
  for(const [id,revision] of [[a.from,a.fromRevisionId],[a.to,a.toRevisionId]]){
   const old=revisions.get(revision),record=refIndex.get(id);
   if(old?old.logicalId!==id:record?.versionId!==revision)errors.push('DOMAIN_ENDPOINT_REVISION:'+a.id);
  }
 }
 for(const revision of x.revisions){if(!revision.record||revision.logicalId!==revision.record.id||revision.parentRevision!==null&&(!revisions.has(revision.parentRevision)||revisions.get(revision.parentRevision).logicalId!==revision.logicalId))errors.push('DOMAIN_REVISION_PARENT');}
 return errors;
}
async function verify(d,m){
 try{
  const x=d.domain;if(!x)return true;if(validate(d).length||x.baseDigest!==await m.objectDigest(legacyBase(d))||!await m.verifyEvents(x.events)||x.events.length!==x.revisions.length)return false;
  if(x.sourceCatalogue){const intake=typeof module!=='undefined'?require('./atlas-intake.js'):root.AtlasIntake;if(!intake||!await intake.verifyCatalogue(x.sourceCatalogue))return false;}
  const seen=new Set();
  for(let i=0;i<x.revisions.length;i++){
   const r=x.revisions[i],{id,...payload}=r;
   if(await m.objectDigest(payload)!==id||r.parentRevision!==null&&!seen.has(r.parentRevision)||x.events[i].objectId!==id)return false;seen.add(id);
  }
  for(const record of [...x.entities,...x.assertions]){const rev=x.revisions.find(r=>r.id===record.revisionId),{revisionId,...payload}=record;if(!rev||m.canonical(rev.record)!==m.canonical(payload))return false;}
  return true;
 }catch{return false;}
}
async function addRevision(domain,record,m,{parentRevision=null,reason='Migrate source-bounded accounting record',observedAt='2026-10-29T00:00:00.000Z',type='ADD'}={}){
 const payload={logicalId:record.id,parentRevision,record},revision={id:await m.objectDigest(payload),...payload};
 domain.revisions.push(revision);domain.events=await m.appendEvent(domain.events,{id:'domain-event-'+domain.events.length,type,objectId:revision.id,actor:'local-researcher',reason,observedAt});
 return {...record,revisionId:revision.id};
}
async function addWorkBreakdowns(d,m){
 const x=d.domain;
 for(const stationId of ['water','area']){
  const seed=x.entities.find(e=>e.stationId===stationId),work=x.entities.find(e=>e.stationId===stationId&&e.kind==='WorkPackage');
  const {id:unused,revisionId:unusedRevision,kind:unusedKind,label:unusedLabel,data:unusedData,...common}=seed;
  const definitions=[['program','Program','Synthetic service research program'],['project','Project','Synthetic evidence and delivery proposal'],['activity','Activity','Synthetic scoped work preparation'],['review','Task','Synthetic prerequisite source and safety review'],['task','Task','Synthetic activity execution proposal'],['deliverable','Deliverable','Synthetic work record and evidence bundle'],['role','Role','Synthetic reviewer role; not Council responsibility'],['asset','Asset','Synthetic service-area resource; no real asset identified']];
  for(const [suffix,kind,label] of definitions)x.entities.push(await addRevision(x,{...common,id:'wbs:'+stationId+':'+suffix,kind,label,data:{status:'SYNTHETIC',executionStatus:'PROPOSED',responsibility:'SYNTHETIC_ROLE_NOT_COUNCIL_ASSIGNMENT',quantity:'UNKNOWN',schedule:'UNKNOWN',approvalGate:'RESEARCH_REVIEW_PENDING'}},m));
  const entity=id=>x.entities.find(e=>e.id===id)||d.nodes.find(e=>e.id===id);
  const program='wbs:'+stationId+':program',project='wbs:'+stationId+':project',activity='wbs:'+stationId+':activity',review='wbs:'+stationId+':review',task='wbs:'+stationId+':task',deliverable='wbs:'+stationId+':deliverable';
  const links=[[stationId,program,'HAS_ACTIVITY'],[program,project,'HAS_ACTIVITY'],[project,work.id,'HAS_ACTIVITY'],[work.id,activity,'HAS_ACTIVITY'],[activity,task,'HAS_ACTIVITY'],[activity,review,'HAS_ACTIVITY'],[task,review,'HAS_DEPENDENCY'],[task,deliverable,'REPORTS_OUTPUT'],[task,'wbs:'+stationId+':role','RESOURCED_BY'],[task,'wbs:'+stationId+':asset','RESOURCED_BY']];
  for(const record of x.entities.filter(e=>e.stationId===stationId&&['ResourceAccount','FinancialEntry','QuantifiedObservation','Output'].includes(e.kind)))links.push([work.id,record.id,record.kind==='FinancialEntry'?'FUNDED_BY':record.kind==='ResourceAccount'?'RESOURCED_BY':record.kind==='Output'?'REPORTS_OUTPUT':'MEASURED_BY']);
  for(const [from,to,predicate] of links){const a=entity(from),b=entity(to);x.assertions.push(await addRevision(x,{...common,id:'wbs-link:'+from+':'+predicate+':'+to,from,to,fromRevisionId:a.versionId||a.revisionId,toRevisionId:b.versionId||b.revisionId,predicate,method:'synthetic-work-breakdown-1',issuer:'local-researcher',reviewer:null,evidenceRefs:[],counterevidenceRefs:common.gaps.map(reason=>({reason}))},m));}
 }
}
async function migrateDataset(base,cases,m,catalogue=null){
 if(base.domain){if(!await verify(base,m))throw Error('INVALID_DOMAIN');return structuredClone(base);}
 if(m.validate(base).length)throw Error('INVALID_BASE');
 const d=structuredClone(base),x={format:'atlas-domain-1',algorithmVersion:'atlas-domain-sha256-1',baseDigest:await m.objectDigest(base),entities:[],assertions:[],revisions:[],events:[]};d.domain=x;
 for(const c of cases){
  const cls=c.metric.status==='SYNTHETIC'?'SYNTHETIC_SCENARIO':'PUBLIC_TEXT_OBSERVED';
  const common={stationId:c.entryNodeId,state:cls==='PUBLIC_TEXT_OBSERVED'?'SOURCE_OBSERVED':'PROPOSED',classification:cls,admission:cls==='PUBLIC_TEXT_OBSERVED'?'PENDING':'NOT_APPLICABLE',provenance:c.metric.source||null,scope:{region:c.metric.area,period:c.metric.period,boundary:c.metric.boundary},gaps:c.uncertainties};
  const records=[{id:c.metric.id,kind:'QuantifiedObservation',label:c.metric.label,data:c.metric},...c.resources.map(r=>({id:r.id,kind:'ResourceAccount',label:r.id,data:r})),...c.funding.map(r=>({id:r.id,kind:'FinancialEntry',label:r.id,data:r}))];
  if(c.work.id)records.push({id:c.work.id,kind:'WorkPackage',label:c.work.description,data:c.work});
  for(const [i,o] of c.outputs.entries())records.push({id:c.id+':output:'+i,kind:'Output',label:o.description,data:o});
  for(const record of records){
   const entity=await addRevision(x,{...common,...record},m);x.entities.push(entity);
   const predicate=record.kind==='QuantifiedObservation'?'MEASURED_BY':record.kind==='FinancialEntry'?'FUNDED_BY':record.kind==='ResourceAccount'?'RESOURCED_BY':record.kind==='Output'?'REPORTS_OUTPUT':'HAS_ACTIVITY';
   const link={...common,id:c.id+':'+predicate+':'+record.id,from:c.entryNodeId,to:record.id,fromRevisionId:d.nodes.find(n=>n.id===c.entryNodeId).versionId,toRevisionId:entity.revisionId,predicate,method:'accounting-migration-v1; context only, not official implementation',evidenceRefs:common.provenance?[common.provenance]:[],counterevidenceRefs:c.uncertainties.map(reason=>({reason})),issuer:'local-researcher',reviewer:null};
   x.assertions.push(await addRevision(x,link,m));
  }
 }
 await addWorkBreakdowns(d,m);
 if(catalogue)x.sourceCatalogue=structuredClone(catalogue);
 if(!await verify(d,m))throw Error('MIGRATION_FAILED');return d;
}
async function commitRevision(d,m,{id,expectedRevisionId,patch,reason,observedAt=new Date().toISOString()}){
 if(!await verify(d,m))throw Error('INVALID_DOMAIN');
 const current=d.domain.entities.find(e=>e.id===id);if(!current)throw Error('DOMAIN_TARGET');
 if(current.revisionId!==expectedRevisionId)throw Error('DOMAIN_CONFLICT');
 if(!reason||typeof reason!=='string')throw Error('REASON_REQUIRED');
 if(!patch||Object.keys(patch).some(k=>!['label','localNote','state'].includes(k))||patch.state&&!STATES.has(patch.state)||Object.values(patch).some(v=>typeof v!=='string'))throw Error('LOCAL_RESEARCH_FIELDS_ONLY');
 const result=structuredClone(d),{revisionId,...old}=current;
 const next=await addRevision(result.domain,{...old,...patch},m,{parentRevision:revisionId,reason,observedAt,type:patch.state==='CONTESTED'?'CONTEST':'REVIEW'});
 result.domain.entities=result.domain.entities.map(e=>e.id===id?next:e);
 if(!await verify(result,m))throw Error('INVALID_REVISION');return result;
}
function forStation(d,id){return {stationId:id,entities:(d.domain?.entities||[]).filter(e=>e.stationId===id),assertions:(d.domain?.assertions||[]).filter(e=>e.stationId===id),trust:'SELF_ATTESTED',signature:'RECEIPT_NOT_PRESENT',witness:'EXTERNAL_WITNESS_UNKNOWN'};}
root.AtlasDomain={TYPES,PREDICATES,STATES,legacyBase,index,relationships,validate,verify,migrateDataset,commitRevision,forStation};if(typeof module!=='undefined')module.exports=root.AtlasDomain;
})(typeof window!=='undefined'?window:globalThis);
