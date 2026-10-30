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
  if(r.provenance?.url){try{const url=new URL(r.provenance.url);if(url.protocol!=='https:'||url.username||url.password)errors.push('DOMAIN_UNSAFE_URL:'+r.id);}catch{errors.push('DOMAIN_UNSAFE_URL:'+r.id);}}
  if(r.classification==='PUBLIC_TEXT_OBSERVED'&&(!r.provenance?.url?.startsWith('https://')||!r.provenance?.locator))errors.push('DOMAIN_PROVENANCE:'+r.id);
  if(r.admission!=='PENDING'&&r.admission!=='NOT_APPLICABLE')errors.push('DOMAIN_OFFICIAL_PROMOTION:'+r.id);
 }
 const refIndex=index(d);
 for(const e of x.entities){
  if(!TYPES.has(e.kind)||typeof e.label!=='string'||!e.data||typeof e.data!=='object')errors.push('DOMAIN_ENTITY:'+e.id);
  if(e.data?.status&&!['SYNTHETIC','PUBLIC_TEXT_OBSERVED','UNKNOWN'].includes(e.data.status))errors.push('DOMAIN_DATA_PROMOTION:'+e.id);
  if(e.kind==='FinancialEntry'&&(!['APPROVED_BUDGET','REVISED_BUDGET','COMMITTED','ACTUAL_EXPENDITURE'].includes(e.data.type)||e.data.unit!=='AUD'||!Number.isFinite(e.data.value)||e.data.value<0||typeof e.data.period!=='string'||!e.data.area||!e.data.boundary))errors.push('DOMAIN_FINANCIAL:'+e.id);
  if(['ML','ha','t_CO2e/person'].includes(e.data?.unit)&&e.data.value!=='UNKNOWN'&&(!Number.isFinite(e.data.value)||e.data.value<0))errors.push('DOMAIN_QUANTITY:'+e.id);
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
  const csoiRecords=x.revisions.filter(r=>r.record?.data?.csoiRecord).map(r=>r.record.data.csoiRecord);
  if(csoiRecords.length){const governance=typeof module!=='undefined'?require('./csoi-governance.js'):root.AtlasCSOIGovernance;if(!governance)return false;for(const record of csoiRecords)if(!await governance.verifyRecord(record)||!governance.assessPublic(record,{operation:'STORAGE'}).allowed)return false;}
  const seen=new Set();
  for(let i=0;i<x.revisions.length;i++){
   const r=x.revisions[i],{id,...payload}=r;
   if(await m.objectDigest(payload)!==id||r.parentRevision!==null&&!seen.has(r.parentRevision)||x.events[i].objectId!==id)return false;seen.add(id);
  }
  for(const e of x.entities.filter(e=>e.kind==='DiscoveryHypothesis')){const execution=typeof module!=='undefined'?require('./atlas-execution.js'):root.AtlasExecution;if(!execution||!await execution.verifyCandidate(d,e.data.candidate)||e.data.candidate.status==='REJECTED_CANDIDATE'&&e.state==='APPROVED_FOR_RESEARCH')return false;}
  for(const e of x.entities.filter(e=>e.kind==='ReviewDecision'))if(!['APPROVED_FOR_RESEARCH','CONTESTED','RETRACTED'].includes(e.data.decision)||e.data.governmentApproval!==false||!x.entities.some(h=>h.kind==='DiscoveryHypothesis'&&h.data.candidate.digest===e.data.candidateDigest))return false;
  for(const e of x.entities.filter(e=>e.kind==='AuditReceipt')){const execution=typeof module!=='undefined'?require('./atlas-execution.js'):root.AtlasExecution;if(!execution||!(await execution.verifyDerivation(d,e.data.receipt)).integrity)return false;}
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
  if(stationId==='water'){const spend=x.entities.find(e=>e.stationId===stationId&&e.kind==='FinancialEntry');x.entities.push(await addRevision(x,{...common,id:'synthetic-water-budget',kind:'FinancialEntry',label:'Synthetic approved budget; not Council funds',data:{...spend.data,id:'synthetic-water-budget',type:'APPROVED_BUDGET',value:30000}},m));}
  const entity=id=>x.entities.find(e=>e.id===id)||d.nodes.find(e=>e.id===id);
  const program='wbs:'+stationId+':program',project='wbs:'+stationId+':project',activity='wbs:'+stationId+':activity',review='wbs:'+stationId+':review',task='wbs:'+stationId+':task',deliverable='wbs:'+stationId+':deliverable';
  const links=[[stationId,program,'HAS_ACTIVITY'],[program,project,'HAS_ACTIVITY'],[project,work.id,'HAS_ACTIVITY'],[work.id,activity,'HAS_ACTIVITY'],[activity,task,'HAS_ACTIVITY'],[activity,review,'HAS_ACTIVITY'],[task,review,'HAS_DEPENDENCY'],[task,deliverable,'REPORTS_OUTPUT'],[task,'wbs:'+stationId+':role','RESOURCED_BY'],[task,'wbs:'+stationId+':asset','RESOURCED_BY']];
  for(const record of x.entities.filter(e=>e.stationId===stationId&&['ResourceAccount','FinancialEntry','QuantifiedObservation','Output'].includes(e.kind)))links.push([work.id,record.id,record.kind==='FinancialEntry'?'FUNDED_BY':record.kind==='ResourceAccount'?'RESOURCED_BY':record.kind==='Output'?'REPORTS_OUTPUT':'MEASURED_BY']);
  for(const [from,to,predicate] of links){const a=entity(from),b=entity(to);x.assertions.push(await addRevision(x,{...common,id:'wbs-link:'+from+':'+predicate+':'+to,from,to,fromRevisionId:a.versionId||a.revisionId,toRevisionId:b.versionId||b.revisionId,predicate,method:'synthetic-work-breakdown-1',issuer:'local-researcher',reviewer:null,evidenceRefs:[],counterevidenceRefs:common.gaps.map(reason=>({reason}))},m));}
 }
}
async function addApplicabilityFixtures(d,m){
 const x=d.domain,common={stationId:'area',state:'PROPOSED',classification:'SYNTHETIC_SCENARIO',admission:'NOT_APPLICABLE',provenance:null,gaps:['Synthetic scope falsification case. No real LEP/DCP/parcel control is inferred.'],scope:{region:'SYNTHETIC_PLACE',period:{from:'2026-07-01',to:'2027-06-30'},boundary:'DEMO_LAND_SCOPE'}};
 const cases=[['current','SYNTHETIC_PLACE','ADOPTED','LEP_STATUTORY','2026-07-01','2027-06-30'],['wrong-region','OTHER_SYNTHETIC_PLACE','ADOPTED','LEP_STATUTORY','2026-07-01','2027-06-30'],['draft','SYNTHETIC_PLACE','DRAFT','DCP_GUIDANCE','2026-07-01','2027-06-30'],['expired','SYNTHETIC_PLACE','ADOPTED','LEP_STATUTORY','2024-07-01','2025-06-30']];
 for(const [suffix,area,legalState,legalRole,validFrom,validTo] of cases){const entity=await addRevision(x,{...common,id:'legal-fixture:'+suffix,kind:'StatutoryControl',label:'Synthetic land control — '+suffix,data:{status:'SYNTHETIC',area,legalState,legalRole,spatialType:'SCENARIO_AREA',validFrom,validTo,sourceRevision:'synthetic-source-'+suffix,adoptedAt:legalState==='ADOPTED'?validFrom:null,currentAsOf:'2026-10-29',parcelGeometry:'UNKNOWN'}},m);x.entities.push(entity);
 x.assertions.push(await addRevision(x,{...common,id:'legal-candidate:'+suffix,from:'area',to:entity.id,fromRevisionId:d.nodes.find(n=>n.id==='area').versionId,toRevisionId:entity.revisionId,predicate:'RESEARCH_CANDIDATE',method:'synthetic-spatial-falsification-1',issuer:'local-researcher',reviewer:null,evidenceRefs:[],counterevidenceRefs:common.gaps.map(reason=>({reason}))},m));}
}
async function migrateDataset(base,cases,m,catalogue=null){
 if(base.domain){if(!await verify(base,m))throw Error('INVALID_DOMAIN');return structuredClone(base);}
 if(m.validate(base).length)throw Error('INVALID_BASE');
 const d=structuredClone(base),x={format:'atlas-domain-1',algorithmVersion:'atlas-domain-sha256-1',baseDigest:await m.objectDigest(base),entities:[],assertions:[],revisions:[],events:[]};d.domain=x;
 for(const c of cases){
  const cls=c.metric.status==='SYNTHETIC'?'SYNTHETIC_SCENARIO':'PUBLIC_TEXT_OBSERVED';
  const common={stationId:c.entryNodeId,state:cls==='PUBLIC_TEXT_OBSERVED'?'SOURCE_OBSERVED':'PROPOSED',classification:cls,admission:cls==='PUBLIC_TEXT_OBSERVED'?'PENDING':'NOT_APPLICABLE',provenance:c.metric.source||null,scope:{region:c.metric.area,period:c.metric.period,boundary:c.metric.boundary},gaps:c.uncertainties};
  const records=[{id:c.metric.id,kind:'QuantifiedObservation',label:c.metric.label,data:c.metric},...c.resources.map(r=>({id:r.id,kind:'ResourceAccount',label:r.id,data:r})),...c.funding.map(r=>({id:r.id,kind:'FinancialEntry',label:r.id,data:{...r,currencyBasis:'NOMINAL_AUD_'+r.period,costClass:'OPEX',lineId:'SYNTHETIC_WATER_SERVICE'}}))];
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
 await addApplicabilityFixtures(d,m);
 if(catalogue)x.sourceCatalogue=structuredClone(catalogue);
 if(!await verify(d,m))throw Error('MIGRATION_FAILED');return d;
}
async function commitRevision(d,m,{id,expectedRevisionId,patch,reason,observedAt=new Date().toISOString()}){
 if(!await verify(d,m))throw Error('INVALID_DOMAIN');
 const current=d.domain.entities.find(e=>e.id===id);if(!current)throw Error('DOMAIN_TARGET');
 if(current.revisionId!==expectedRevisionId)throw Error('DOMAIN_CONFLICT');
 if(!reason||typeof reason!=='string')throw Error('REASON_REQUIRED');
 if(!patch||Object.keys(patch).some(k=>!['label','localNote','state','data'].includes(k))||patch.data&&current.classification!=='SYNTHETIC_SCENARIO'||patch.state&&!STATES.has(patch.state)||Object.entries(patch).some(([key,v])=>key==='data'?(!v||Object.getPrototypeOf(v)!==Object.prototype):typeof v!=='string'))throw Error('LOCAL_RESEARCH_FIELDS_ONLY');
 const result=structuredClone(d),{revisionId,...old}=current;
 const next=await addRevision(result.domain,{...old,...patch},m,{parentRevision:revisionId,reason,observedAt,type:patch.state==='CONTESTED'?'CONTEST':'REVIEW'});
 result.domain.entities=result.domain.entities.map(e=>e.id===id?next:e);
 if(!await verify(result,m))throw Error('INVALID_REVISION');return result;
}
async function recordResearchReview(d,m,{candidate,question,decision,reason,observedAt=new Date().toISOString()}){
 const execution=typeof module!=='undefined'?require('./atlas-execution.js'):root.AtlasExecution;
 if(!await verify(d,m)||!await execution.verifyCandidate(d,candidate)||!question||question.length>1000||!reason||reason.length>1000||!['APPROVED_FOR_RESEARCH','CONTESTED','RETRACTED'].includes(decision)||candidate.status==='REJECTED_CANDIDATE'&&decision==='APPROVED_FOR_RESEARCH')throw Error('RESEARCH_REVIEW_INVALID');
 const result=structuredClone(d),from=index(d).get(candidate.from),stationId=from.stationId||d.nodes.find(n=>n.id===from.ownerNodeId)?.id||d.nodes.find(n=>n.id===from.id)?.id;
 if(!stationId)throw Error('RESEARCH_STATION');
 const common={stationId,state:decision,classification:'LOCAL_RESEARCH',admission:'NOT_APPLICABLE',provenance:null,scope:from.scope||{region:'UNKNOWN',period:'UNKNOWN',boundary:'UNKNOWN'},gaps:['Local research review is not government approval or official relationship admission.']};
 const hypothesisId='hypothesis:'+candidate.digest,reviewId='review:'+await m.objectDigest({candidate:candidate.digest,question,decision,reason,observedAt});
 if(!result.domain.entities.some(e=>e.id===hypothesisId))result.domain.entities.push(await addRevision(result.domain,{...common,id:hypothesisId,kind:'DiscoveryHypothesis',label:question,data:{status:'UNKNOWN',candidate}},m,{reason,observedAt,type:'ADD'}));
 result.domain.entities.push(await addRevision(result.domain,{...common,id:reviewId,kind:'ReviewDecision',label:decision+' · '+question,data:{status:'UNKNOWN',question,candidateDigest:candidate.digest,decision,reason,observedAt,reviewer:'local-researcher',governmentApproval:false}},m,{reason,observedAt,type:decision==='CONTESTED'?'CONTEST':decision==='RETRACTED'?'RETRACT':'REVIEW'}));
 return result;
}
async function registerScenario(d,m,{id,kind,label,stationId,data,scope,reason}){
 if(!await verify(d,m)||index(d).has(id)||!TYPES.has(kind)||!d.nodes.some(n=>n.id===stationId)||!label||!reason||data?.status!=='SYNTHETIC')throw Error('SYNTHETIC_SCENARIO_REQUIRED');
 const result=structuredClone(d);result.domain.entities.push(await addRevision(result.domain,{id,kind,label,stationId,data,scope:scope||{region:data.area||'UNKNOWN',period:data.period||'UNKNOWN',boundary:data.boundary||'UNKNOWN'},state:'PROPOSED',classification:'SYNTHETIC_SCENARIO',admission:'NOT_APPLICABLE',provenance:null,gaps:['User-authored synthetic scenario; not Council facts or official performance.']},m,{reason}));
 if(!await verify(result,m))throw Error('INVALID_SCENARIO');return result;
}
async function registerResearchRecord(d,m,{record,kind='ContentBlock',label,stationId,reason}){
 const governance=typeof module!=='undefined'?require('./csoi-governance.js'):root.AtlasCSOIGovernance;
 if(!governance||!await governance.verifyRecord(record)||!governance.assessPublic(record,{operation:'STORAGE'}).allowed)throw Error('CSOI_PUBLIC_RECORD_REQUIRED');
 if(!await verify(d,m)||index(d).has(record.id)||!TYPES.has(kind)||['ReviewDecision','AuditReceipt','DiscoveryHypothesis'].includes(kind)||!d.nodes.some(n=>n.id===stationId)||!label||!reason)throw Error('CSOI_REGISTRATION_INVALID');
 if(!researchInputsPresent(d,record))throw Error('CSOI_INPUT_REVISION_MISSING');
 const synthetic=record.sourceClass==='SYNTHETIC',result=structuredClone(d);
 result.domain.entities.push(await addRevision(result.domain,{id:record.id,kind,label,stationId,data:{status:synthetic?'SYNTHETIC':'PUBLIC_TEXT_OBSERVED',csoiRecord:structuredClone(record)},scope:record.scope,state:synthetic?'PROPOSED':'SOURCE_OBSERVED',classification:synthetic?'SYNTHETIC_SCENARIO':'LOCAL_RESEARCH',admission:synthetic?'NOT_APPLICABLE':'PENDING',provenance:synthetic?null:record.provenance,gaps:['Independent public/synthetic research. No Council assignment, official decision or admitted strategy relationship.']},m,{reason,observedAt:record.observedAt}));
 if(!await verify(result,m))throw Error('CSOI_REGISTRATION_INVALID');return result;
}
async function reviseResearchRecord(d,m,{id,expectedRevisionId,record,reason}){
 const governance=typeof module!=='undefined'?require('./csoi-governance.js'):root.AtlasCSOIGovernance,old=d.domain?.entities.find(e=>e.id===id);
 if(!await verify(d,m)||!old?.data?.csoiRecord||old.revisionId!==expectedRevisionId||record?.id!==id||!reason)throw Error('CSOI_REVISION_CONFLICT');
 if(!governance||!await governance.verifyRecord(record)||!governance.assessPublic(record,{operation:'STORAGE'}).allowed||record.security!==old.data.csoiRecord.security||record.sourceClass!==old.data.csoiRecord.sourceClass||record.ownerModule!==old.data.csoiRecord.ownerModule)throw Error('CSOI_PUBLIC_RECORD_REQUIRED');
 if(!researchInputsPresent(d,record))throw Error('CSOI_INPUT_REVISION_MISSING');
 const {revisionId,...payload}=old,result=structuredClone(d),next=await addRevision(result.domain,{...payload,scope:record.scope,provenance:old.classification==='SYNTHETIC_SCENARIO'?null:record.provenance,data:{...payload.data,csoiRecord:structuredClone(record)}},m,{parentRevision:revisionId,reason,observedAt:record.observedAt,type:'REVIEW'});
 result.domain.entities=result.domain.entities.map(e=>e.id===id?next:e);if(!await verify(result,m))throw Error('CSOI_REVISION_INVALID');return result;
}
function researchInputsPresent(d,record){return record.inputs.every(input=>d.domain.revisions.some(revision=>revision.logicalId===input.id&&(revision.id===input.revisionId||revision.record.data?.csoiRecord?.revisionId===input.revisionId))||(d.domain.sourceCatalogue?.sources||[]).some(source=>source.id===input.id&&source.revisionId===input.revisionId));}
async function appendCalculation(d,m,receipt){
 const execution=typeof module!=='undefined'?require('./atlas-execution.js'):root.AtlasExecution;
 if(!await verify(d,m)||!(await execution.verifyDerivation(d,receipt)).current)throw Error('DERIVATION_NOT_CURRENT');
 if(d.domain.entities.some(e=>e.id===receipt.digest))return structuredClone(d);
 const first=index(d).get(receipt.inputs[0].id),result=structuredClone(d);
 result.domain.entities.push(await addRevision(result.domain,{id:receipt.digest,kind:'AuditReceipt',stationId:first.stationId,label:receipt.request.formula+' — '+receipt.result.value+' '+receipt.result.unit,state:'PROPOSED',classification:'SYNTHETIC_SCENARIO',admission:'NOT_APPLICABLE',provenance:null,scope:first.scope,gaps:first.gaps,data:{status:'SYNTHETIC',receipt}},m,{reason:'Record reproducible synthetic calculation'}));
 const calculation=result.domain.entities.find(e=>e.id===receipt.digest);
 for(const input of receipt.inputs)result.domain.assertions.push(await addRevision(result.domain,{id:receipt.digest+':input:'+input.id,stationId:first.stationId,state:'PROPOSED',classification:'SYNTHETIC_SCENARIO',admission:'NOT_APPLICABLE',provenance:null,scope:first.scope,gaps:first.gaps,from:calculation.id,to:input.id,fromRevisionId:calculation.revisionId,toRevisionId:input.revisionId,predicate:'EVIDENCED_BY',method:receipt.methodVersion,evidenceRefs:[],counterevidenceRefs:[],issuer:'local-researcher',reviewer:null},m,{reason:'Pin calculation input revision'}));
 return result;
}
function forStation(d,id){return {stationId:id,entities:(d.domain?.entities||[]).filter(e=>e.stationId===id),assertions:(d.domain?.assertions||[]).filter(e=>e.stationId===id),trust:'SELF_ATTESTED',signature:'RECEIPT_NOT_PRESENT',witness:'EXTERNAL_WITNESS_UNKNOWN'};}
root.AtlasDomain={TYPES,PREDICATES,STATES,legacyBase,index,relationships,validate,verify,migrateDataset,commitRevision,recordResearchReview,registerScenario,registerResearchRecord,reviseResearchRecord,appendCalculation,forStation};if(typeof module!=='undefined')module.exports=root.AtlasDomain;
})(typeof window!=='undefined'?window:globalThis);
