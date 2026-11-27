/* Reproducible research work/resource accounting. No operational records or financial postings. */
(function(root){
'use strict';
const M=typeof module!=='undefined'?require('./atlas-model.js'):root.AtlasModel;
const E=typeof module!=='undefined'?require('./atlas-execution.js'):root.AtlasExecution;
const G=typeof module!=='undefined'?require('./csoi-governance.js'):root.AtlasCSOIGovernance;
const PHASES=Object.freeze(['preparation','field','travel','documentation','reinspection','administration']);
const MEASUREMENTS=Object.freeze(['ESTIMATED','MEASURED','ASSUMED']);
const need=(ok,code)=>{if(!ok)throw Error(code);};
const clone=v=>structuredClone(v);
function day(value){return typeof value==='string'&&/^\d{4}-\d{2}-\d{2}$/.test(value)&&Number.isFinite(Date.parse(value))&&new Date(value).toISOString().slice(0,10)===value;}
function syntheticFixture(){
 const common={classification:'PUBLIC',synthetic:true,sourceId:'AUTHOR_SYNTHETIC_TEMPLATE',revisionId:'csoi-work-template-1',period:'FY2026-27',region:'SYNTHETIC_SERVICE_AREA'};
 const items=[
  {id:'SYN-REG-FOOD-1',entityId:'SYN-ACTIVITY-1',entityType:'BUSINESS_ACTIVITY',service:'FOOD',propertyId:'SYN-PROPERTY-1',registered:true,approvalRequired:'UNKNOWN',eligible:true,planned:true,dueDate:'2026-10-01',requiredVisits:1,events:[{id:'SYN-EVENT-1',completedAt:'2026-09-28',evidenceId:'SYN-EVIDENCE-1'}],issues:[{id:'SYN-ISSUE-1',state:'OPEN'}]},
  {id:'SYN-REG-LTW-1',entityId:'SYN-DISCHARGE-1',entityType:'DISCHARGE_ACTIVITY',service:'LTW',propertyId:'SYN-PROPERTY-1',registered:true,approvalRequired:true,eligible:true,planned:true,dueDate:'2026-10-01',requiredVisits:1,events:[],issues:[]},
  {id:'SYN-REG-BACKFLOW-1',entityId:'SYN-DEVICE-1',entityType:'DEVICE',service:'BACKFLOW',propertyId:'SYN-PROPERTY-1',registered:true,approvalRequired:'UNKNOWN',eligible:true,planned:false,dueDate:'2027-02-28',requiredVisits:1,events:[],issues:[]},
  {id:'SYN-REG-FOOD-2',entityId:'SYN-ACTIVITY-2',entityType:'BUSINESS_ACTIVITY',service:'FOOD',propertyId:'SYN-PROPERTY-1',registered:false,approvalRequired:'UNKNOWN',eligible:'UNKNOWN',planned:false,dueDate:null,requiredVisits:'UNKNOWN',events:[],issues:[]},
  {id:'SYN-REG-LTW-2',entityId:'SYN-DISCHARGE-2',entityType:'DISCHARGE_ACTIVITY',service:'LTW',propertyId:'SYN-PROPERTY-2',registered:false,approvalRequired:false,eligible:false,planned:false,dueDate:null,requiredVisits:0,events:[],issues:[]}
 ].map(item=>({...common,...item}));
 const task=(id,entityId,hours,measurement,skills,vehicleHours)=>({...common,id,entityId,stationId:'water',status:'PROPOSED',sourceKind:'RESEARCH_PROPOSAL',skills,vehicleHours,trainingHours:0,facilityHours:0,phases:Object.fromEntries(PHASES.map((phase,i)=>[phase,{hours:hours[i],measurement,sourceId:'AUTHOR_SYNTHETIC_TEMPLATE'}]))});
 const tasks=[task('SYN-TASK-1','SYN-ACTIVITY-1',[.5,1,.5,.5,0,.25],'ESTIMATED',['SYN-INSPECTION-SKILL'],.5),task('SYN-TASK-2','SYN-DISCHARGE-1',[.5,1.5,.75,.75,.5,.25],'ASSUMED',['SYN-LTW-REVIEW-SKILL'],.75)];
 return {format:'csoi-work-fixture-1',classification:'PUBLIC',synthetic:true,items,tasks,resources:{annualProductiveHoursPerPerson:1400,classification:'SYNTHETIC_ASSUMPTION',sourceId:'AUTHOR_SYNTHETIC_TEMPLATE'}};
}
function publicInput(value){
 const queue=[value];for(let i=0;i<queue.length;i++){need(i<100000,'INPUT_LIMIT');const row=queue[i];if(!row||typeof row!=='object')continue;for(const key of ['classification','security','permission','privacy'])if(Object.prototype.hasOwnProperty.call(row,key))need(!['PERSONAL_PRIVATE','COUNCIL_PROTECTED','APPROVED_RELEASE','UNKNOWN'].includes(row[key]),'PROTECTED_INPUT_DENIED');for(const [key,v] of Object.entries(row)){need(!/^(?:customerName|address|email|phone|accountNumber|employeeName|token|password|secret|rawRecord)$/i.test(key),'PROTECTED_FIELD_DENIED');if(v&&typeof v==='object')queue.push(v);}}
 need(G&&G.inspectPayload(value).length===0,'PUBLIC_PAYLOAD_DENIED');
}
function requireSynthetic(rows){
 need(Array.isArray(rows)&&rows.length<=10000,'WORK_BOUNDS');publicInput(rows);
 for(const r of rows)need(r&&r.classification==='PUBLIC'&&r.synthetic===true&&typeof r.id==='string'&&r.id.startsWith('SYN-')&&r.sourceId&&r.revisionId,'WORK_PUBLIC_SYNTHETIC_ONLY');
}
function tri(value){return value===true||value===false||value==='UNKNOWN';}
function denominatorKey(row){return row.service+'|'+row.entityType+'|'+row.entityId;}
function coverage(items,asOf){
 requireSynthetic(items);need(day(asOf),'AS_OF_DATE_REQUIRED');
 const objects=new Map(),eventIndex=new Map(),issueIndex=new Map(),ids=new Set();let duplicateRows=0;
 for(const item of items){
  need(!ids.has(item.id),'DUPLICATE_RECORD_ID');ids.add(item.id);
  need(typeof item.entityId==='string'&&item.entityId.startsWith('SYN-')&&['BUSINESS_ACTIVITY','DISCHARGE_ACTIVITY','DEVICE','SYSTEM','FACILITY'].includes(item.entityType)&&typeof item.service==='string'&&item.service.length>0,'REGULATORY_OBJECT_ID');
  need(['registered','approvalRequired','eligible','planned'].every(key=>tri(item[key]))&&Array.isArray(item.events)&&Array.isArray(item.issues),'REGULATORY_FIELDS');
  need(item.dueDate===null||day(item.dueDate),'DUE_DATE');need(item.requiredVisits==='UNKNOWN'||Number.isInteger(item.requiredVisits)&&item.requiredVisits>=0,'VISIT_REQUIREMENT');
  need(typeof item.region==='string'&&typeof item.period==='string','COUNT_SCOPE_REQUIRED');
  if(items.length)need(item.region===items[0].region&&item.period===items[0].period,'COUNT_SCOPE_MISMATCH');
  const key=denominatorKey(item),old=objects.get(key);
  const fingerprint={registered:item.registered,approvalRequired:item.approvalRequired,eligible:item.eligible,planned:item.planned,dueDate:item.dueDate,requiredVisits:item.requiredVisits,period:item.period,region:item.region};
  if(old){need(M.canonical(old.fingerprint)===M.canonical(fingerprint),'CONFLICTING_DENOMINATOR');duplicateRows++;}else objects.set(key,{...item,fingerprint,events:[],issues:[]});
  const current=objects.get(key);
  for(const event of item.events){need(event&&typeof event.id==='string'&&event.id.startsWith('SYN-')&&day(event.completedAt)&&event.completedAt<=asOf&&typeof event.evidenceId==='string'&&event.evidenceId.startsWith('SYN-'),'EXECUTION_EVIDENCE_REQUIRED');const prior=eventIndex.get(event.id);need(!prior||prior.objectKey===key&&M.canonical(prior.event)===M.canonical(event),'DUPLICATE_EVENT_CONFLICT');if(!prior){eventIndex.set(event.id,{objectKey:key,event});current.events.push(event);}}
  for(const issue of item.issues){need(issue&&typeof issue.id==='string'&&issue.id.startsWith('SYN-')&&['OPEN','CLOSED','UNKNOWN'].includes(issue.state),'ISSUE_FIELDS');need(issue.state!=='CLOSED'||typeof issue.closureEvidenceId==='string'&&issue.closureEvidenceId.startsWith('SYN-'),'CLOSURE_EVIDENCE_REQUIRED');const prior=issueIndex.get(issue.id);need(!prior||prior.objectKey===key&&M.canonical(prior.issue)===M.canonical(issue),'DUPLICATE_ISSUE_CONFLICT');if(!prior){issueIndex.set(issue.id,{objectKey:key,issue});current.issues.push(issue);}}
 }
 function count(rows){
  const knownEligible=rows.filter(r=>r.eligible===true),completed=knownEligible.filter(r=>Number.isInteger(r.requiredVisits)&&r.requiredVisits>0&&r.events.length>=r.requiredVisits),unknown=rows.filter(r=>r.eligible==='UNKNOWN');
  const required=knownEligible.every(r=>r.requiredVisits!=='UNKNOWN')?knownEligible.reduce((n,r)=>n+r.requiredVisits,0):'UNKNOWN';
  return {registered:rows.filter(r=>r.registered===true).length,registrationUnknown:rows.filter(r=>r.registered==='UNKNOWN').length,approvalRequired:rows.filter(r=>r.approvalRequired===true).length,approvalUnknown:rows.filter(r=>r.approvalRequired==='UNKNOWN').length,eligible:knownEligible.length,planned:knownEligible.filter(r=>r.planned===true).length,planningUnknown:knownEligible.filter(r=>r.planned==='UNKNOWN').length,completed:completed.length,inspectedObjects:knownEligible.filter(r=>r.events.length>0).length,unknownVisitRequirement:knownEligible.filter(r=>r.requiredVisits==='UNKNOWN').length,overdue:knownEligible.filter(r=>r.dueDate&&r.dueDate<asOf&&Number.isInteger(r.requiredVisits)&&r.requiredVisits>r.events.length).length,unknown:unknown.length,notEligible:rows.filter(r=>r.eligible===false).length,unknownDue:knownEligible.filter(r=>r.dueDate===null).length,dueDevices:knownEligible.filter(r=>r.entityType==='DEVICE'&&r.dueDate&&r.dueDate<=asOf).length,requiredInspectionEvents:required,completedInspectionEvents:rows.reduce((n,r)=>n+r.events.length,0),openIssues:rows.reduce((n,r)=>n+r.issues.filter(i=>i.state==='OPEN').length,0),closedIssues:rows.reduce((n,r)=>n+r.issues.filter(i=>i.state==='CLOSED').length,0),coverage:knownEligible.length?completed.length/knownEligible.length:'UNKNOWN',coverageBasis:'Known-eligible service objects meeting the explicitly stated visit requirement / all known-eligible service objects; unknown eligibility and requirements are disclosed',completeInventoryCoverage:'UNKNOWN',environmentalOutcome:'UNKNOWN',compliance:'UNKNOWN'};
 }
 const rows=[...objects.values()],byService={};for(const service of [...new Set(rows.map(r=>r.service))])byService[service]=count(rows.filter(r=>r.service===service));
 return {format:'csoi-coverage-1',classification:'PUBLIC',synthetic:true,asOf,denominator:'UNIQUE_SERVICE_ENTITY_TYPE_ENTITY_ID',uniqueObjects:objects.size,uniqueProperties:new Set(rows.map(r=>r.propertyId).filter(Boolean)).size,duplicateRowsRemoved:duplicateRows,...count(rows),byService,governmentKpi:'UNKNOWN',limitations:['Work coverage is not compliance, risk elimination or an environmental outcome.','Multiple activities/devices at one property are not one common regulatory denominator.','Risk labels do not create a visit requirement; an explicit applicable requirement is needed.']};
}
function workload(tasks){
 requireSynthetic(tasks);const ids=new Set(),totals={ESTIMATED:0,MEASURED:0,ASSUMED:0},byPhase=Object.fromEntries(PHASES.map(phase=>[phase,{ESTIMATED:0,MEASURED:0,ASSUMED:0,unknown:0}]));let unknown=0;
 for(const task of tasks){need(!ids.has(task.id),'DUPLICATE_TASK');ids.add(task.id);need(task.phases&&typeof task.phases==='object'&&Object.keys(task.phases).every(p=>PHASES.includes(p)),'PHASE_FIELDS');
  for(const phase of PHASES){const entry=task.phases[phase];if(!entry||entry.hours==='UNKNOWN'){unknown++;byPhase[phase].unknown++;continue;}need(Number.isFinite(entry.hours)&&entry.hours>=0&&MEASUREMENTS.includes(entry.measurement)&&typeof entry.sourceId==='string','PHASE_HOURS');totals[entry.measurement]+=entry.hours;byPhase[phase][entry.measurement]+=entry.hours;}}
 return {format:'csoi-workload-1',classification:'PUBLIC',synthetic:true,unit:'person_hour',taskCount:ids.size,totals,byPhase,unknownPhases:unknown,actualSpend:'UNKNOWN',actualSpendReason:'Hours, estimated or measured, are not an expenditure entry.',completion:'UNKNOWN'};
}
function resources(tasks,{annualProductiveHoursPerPerson='UNKNOWN'}={}){
 const load=workload(tasks),skills={};let vehicleHours=0,trainingHours=0,facilityHours=0;const resourceUnknown=[];
 for(const task of tasks){need(Array.isArray(task.skills)&&task.skills.every(s=>typeof s==='string'&&s.startsWith('SYN-')),'SKILL_FIELDS');for(const skill of new Set(task.skills))skills[skill]=(skills[skill]||0)+1;
  for(const field of ['vehicleHours','trainingHours','facilityHours'])if(task[field]==='UNKNOWN'||task[field]===undefined)resourceUnknown.push({taskId:task.id,field});else {need(Number.isFinite(task[field])&&task[field]>=0,'RESOURCE_HOURS');if(field==='vehicleHours')vehicleHours+=task[field];if(field==='trainingHours')trainingHours+=task[field];if(field==='facilityHours')facilityHours+=task[field];}}
 const capacityKnown=typeof annualProductiveHoursPerPerson==='number'&&Number.isFinite(annualProductiveHoursPerPerson)&&annualProductiveHoursPerPerson>0;need(capacityKnown||annualProductiveHoursPerPerson==='UNKNOWN','PRODUCTIVE_CAPACITY');
 return {format:'csoi-resources-1',classification:'PUBLIC',synthetic:true,workload:load,skills,vehicleHours,trainingHours,facilityHours,resourceUnknown,annualProductiveHoursPerPerson,plannedFteEquivalent:capacityKnown&&!load.unknownPhases?(load.totals.ESTIMATED+load.totals.ASSUMED)/annualProductiveHoursPerPerson:'UNKNOWN',measuredFteEquivalent:capacityKnown&&!load.unknownPhases?load.totals.MEASURED/annualProductiveHoursPerPerson:'UNKNOWN',personnelHeadcount:'UNKNOWN',funding:'UNKNOWN',actualSpend:'UNKNOWN',limitation:'FTE equivalents are capacity scenarios, not staff assignments, establishment approvals, rosters or paid expenses.'};
}
function ledgerSummary(dataset,stationId){
 const dossier=M.domainForStation(dataset,stationId),physical=[],financial=[],results=[];
 for(const e of dossier.entities){const row={id:e.id,revisionId:e.revisionId,kind:e.kind,label:e.label,data:clone(e.data),classification:e.classification,provenance:clone(e.provenance),state:e.state};if(['FinancialEntry','CostAllocation','FundingSource','BudgetRevision','ActualExpenditure'].includes(e.kind))financial.push(row);else if(['Baseline','Target','Output','Outcome','Impact','ContributionClaim'].includes(e.kind))results.push(row);else if(['MetricDefinition','QuantifiedObservation','ResourceAccount','Asset','Infrastructure','SpatialUnit'].includes(e.kind))physical.push(row);}
 return {stationId,physical,financial,results,actualCouncilSpend:'UNKNOWN',actualOutcome:'UNKNOWN',officialStrategicMapping:'UNKNOWN',limitations:dossier.entities.flatMap(e=>e.gaps||[])};
}
async function derive(dataset,request){return E.derive(dataset,request);}
async function verifyDerivation(dataset,value){return E.verifyDerivation(dataset,value);}
function reverseTrace(dataset,id){
 const index=M.domainIndex(dataset),record=index.get(id);need(record,'TRACE_ID');
 const incoming=M.queryRelationships(dataset,id,{direction:'reverse'}),stationId=record.stationId||record.ownerNodeId||(dataset.nodes.some(n=>n.id===id)?id:null);
 const path=stationId?E.shortestPath(dataset,id,stationId,{direction:'reverse',mode:'DISCOVERY_CANDIDATE'}):{status:'UNKNOWN',path:[],nodeIds:[]};
 return {id,revisionId:record.revisionId||record.versionId||'UNKNOWN',stationId,provenance:clone(record.provenance||null),incoming:clone(incoming),path,formula:record.kind==='AuditReceipt'?record.data?.receipt?.request:null,inputReceipts:record.kind==='AuditReceipt'?clone(record.data?.receipt?.inputs||[]):[],officialMapping:'UNKNOWN',breaks:stationId?['Station context does not prove an official OP/DP/CSP implementation link.']:['No evidenced strategic context is known.']};
}
async function receipt(input){
 publicInput(input);const payload={format:'csoi-work-receipt-1',algorithm:'csoi-work-sha256-1',input:clone(input),inputDigest:await M.objectDigest(input),trust:'SELF_ATTESTED',witness:'EXTERNAL_WITNESS_UNKNOWN',governmentAuthority:false};return {...payload,digest:await M.objectDigest(payload)};
}
async function verifyReceipt(value,currentInput){try{publicInput(value);const {digest,...payload}=value;if(value.format!=='csoi-work-receipt-1'||value.algorithm!=='csoi-work-sha256-1'||await M.objectDigest(payload)!==digest||await M.objectDigest(value.input)!==value.inputDigest||value.governmentAuthority!==false)return {integrity:false,current:false,status:'CORRUPT'};const current=await M.objectDigest(currentInput)===value.inputDigest;return {integrity:true,current,status:current?'CURRENT':'STALE_INPUT_RECALCULATE'};}catch{return {integrity:false,current:false,status:'CORRUPT'};}}
const api={PHASES,MEASUREMENTS,syntheticFixture,denominatorKey,coverage,workload,resources,ledgerSummary,derive,verifyDerivation,reverseTrace,receipt,verifyReceipt};
root.AtlasCSOIWork=api;root.CsoiWork=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
