/* Draft-only management preparation. No identities, accounts, mail or calendar APIs. */
(function(root){
'use strict';
const calendar=typeof module!=='undefined'?require('./csoi-calendar.js'):root.AtlasCSOICalendar;
const UNKNOWN='UNKNOWN';
function fail(ok,code){if(!ok)throw Error(code);}
function freeze(value){const stack=[value];while(stack.length){const x=stack.pop();if(x&&typeof x==='object'&&!Object.isFrozen(x)){Object.values(x).forEach(v=>{if(v&&typeof v==='object')stack.push(v);});Object.freeze(x);}}return value;}
function draftId(kind,week,id){return 'csoi:draft:'+kind+':'+week+':'+id;}
function compileWeek(edition,{date,capacityHours=UNKNOWN}={}){
 calendar.day(date);calendar.index(edition);fail(date>=edition.start&&date<=edition.end,'ASSISTANT_DATE_OUTSIDE_EDITION');
 fail(capacityHours===UNKNOWN||Number.isFinite(capacityHours)&&capacityHours>=0,'CAPACITY_INVALID');
 edition.tasks.forEach(calendar.validateTask);const week=calendar.isoWeek(date),tasks=edition.tasks.filter(t=>t.date>=week.from&&t.date<=week.to),open=t=>!['RECORDED','CANCELLED'].includes(t.executionStatus);
 const knownHours=tasks.filter(t=>t.expectedHours!==UNKNOWN).reduce((n,t)=>n+t.expectedHours,0),unknownHours=tasks.filter(t=>t.expectedHours===UNKNOWN).length;
 const make=(kind,task,detail)=>({id:draftId(kind,week.id,task.id),taskId:task.id,title:task.title,detail,status:'DRAFT',governmentApproval:false,sourceType:task.sourceType,sourceRefs:task.evidenceRefs,sourceRevision:task.sourceBasis?.revisionId||UNKNOWN,classification:task.classification});
 const concerns=tasks.filter(t=>open(t)&&t.risk.level==='HIGH').map(t=>make('risk',t,t.risk.basis));
 const reviewQueue=tasks.filter(t=>t.approval.state!=='APPROVED_FOR_RESEARCH'||t.applicability.state===UNKNOWN).map(t=>make('review',t,'Confirm applicability, source and review role; no operational approval inferred.'));
 const missingMaterials=tasks.flatMap(t=>t.attachments.filter(a=>a.state!=='PRESENT').map(a=>({...make('material',t,'Missing or unverified attachment '+a.id),attachmentId:a.id})));
 const overdue=edition.tasks.filter(t=>open(t)&&t.dueDate<week.from).map(t=>make('overdue',t,'Planned task date passed. This is not proof of a statutory breach.'));
 const dependencies=calendar.conflicts(edition.tasks);
 const bottleneck=capacityHours===UNKNOWN||unknownHours?UNKNOWN:knownHours>capacityHours;
 return freeze({format:'csoi-weekly-draft-1',id:'csoi:draft:week:'+week.id,status:'DRAFT',classification:edition.tasks.every(t=>t.classification==='SYNTHETIC')?'SYNTHETIC':'PUBLIC',assistantLabel:'Michele assistance preparation — draft for human review',period:{from:week.from,to:week.to},editionId:edition.editionId,taskIds:tasks.map(t=>t.id),concerns,reviewQueue,missingMaterials,overdue,dependencies,
  resources:{expectedHoursKnown:knownHours,unknownHoursTasks:unknownHours,availableHours:capacityHours,capacityBasis:capacityHours===UNKNOWN?UNKNOWN:'USER_PROVIDED_PLANNING_SCENARIO',bottleneck,actualHours:tasks.every(t=>t.actualHours!==UNKNOWN)?tasks.reduce((n,t)=>n+t.actualHours,0):UNKNOWN,financialSpend:UNKNOWN},
  nextSteps:tasks.map(t=>make('next',t,t.nextStep)),governmentApproval:false,ownerRole:UNKNOWN,authority:'INDEPENDENT_RESEARCH',outlook:'SIMULATION_DISABLED',warning:'No manager agreement, Council decision, staff assignment, email, reminder or calendar write is created.'});
}
function meetingDraft(weekly,{title='Weekly research preparation',reason='Prepare questions for an authorised human review'}={}){
 fail(weekly?.format==='csoi-weekly-draft-1'&&weekly.status==='DRAFT'&&weekly.governmentApproval===false,'WEEKLY_DRAFT_REQUIRED');
 fail(typeof title==='string'&&title.trim()&&title.length<=240&&typeof reason==='string'&&reason.trim()&&reason.length<=1000,'MEETING_TEXT');
 const agenda=[...weekly.concerns,...weekly.reviewQueue,...weekly.missingMaterials].slice(0,100);
 const draft={format:'csoi-meeting-draft-1',id:weekly.id+':meeting',status:'DRAFT',classification:weekly.classification,title,reason,period:weekly.period,sourceDraftId:weekly.id,
  agenda:agenda.map((item,i)=>({id:weekly.id+':agenda:'+i,taskId:item.taskId,topic:item.detail,sourceRefs:item.sourceRefs,status:'DRAFT'})),
  questions:weekly.reviewQueue.map(item=>({taskId:item.taskId,question:'What evidence establishes applicability, role and next permitted step for '+item.title+'?',sourceRefs:item.sourceRefs,status:'DRAFT'})),
  decisionsToConfirm:[{question:'Which preparation actions, if any, should an authorised person approve?',answer:UNKNOWN,state:'PENDING_HUMAN_REVIEW',governmentApproval:false}],
  followUpActions:weekly.nextSteps.map(item=>({id:item.id+':meeting-action',taskId:item.taskId,action:item.detail,responsibleRole:UNKNOWN,dueDate:UNKNOWN,state:'DRAFT',sourceRefs:item.sourceRefs})),managerAgreement:UNKNOWN,governmentApproval:false,authority:'INDEPENDENT_RESEARCH',outlook:'SIMULATION_DISABLED'};validateDraft(draft);return freeze(draft);
}
function validateDraft(draft){
 fail(draft&&['csoi-weekly-draft-1','csoi-meeting-draft-1'].includes(draft.format)&&draft.status==='DRAFT'&&draft.governmentApproval===false&&draft.authority==='INDEPENDENT_RESEARCH'&&draft.outlook==='SIMULATION_DISABLED','DRAFT_ONLY_BOUNDARY');
 calendar.privacy(draft);calendar.day(draft.period?.from);calendar.day(draft.period?.to);fail(draft.period.from<=draft.period.to,'DRAFT_PERIOD');
 fail(!draft.managerAgreement||draft.managerAgreement===UNKNOWN,'MANAGER_AGREEMENT_FORBIDDEN');
 if(draft.format==='csoi-weekly-draft-1'){
  for(const field of ['taskIds','concerns','reviewQueue','missingMaterials','overdue','dependencies','nextSteps'])fail(Array.isArray(draft[field])&&draft[field].length<=10000,'WEEKLY_DRAFT_FIELDS');
  for(const field of ['concerns','reviewQueue','missingMaterials','overdue','nextSteps'])for(const item of draft[field])fail(item.status==='DRAFT'&&item.governmentApproval===false,'DRAFT_ITEM_NOT_APPROVED');
 }else{
  for(const field of ['agenda','questions','decisionsToConfirm','followUpActions'])fail(Array.isArray(draft[field])&&draft[field].length<=10000,'MEETING_DRAFT_FIELDS');
  for(const item of [...draft.agenda,...draft.questions])fail(item.status==='DRAFT','MEETING_ITEM_NOT_APPROVED');
  for(const item of draft.decisionsToConfirm)fail(item.state==='PENDING_HUMAN_REVIEW'&&item.answer===UNKNOWN&&item.governmentApproval===false,'DECISION_NOT_AUTHORISED');
  for(const item of draft.followUpActions)fail(item.state==='DRAFT'&&item.responsibleRole===UNKNOWN,'ASSIGNMENT_NOT_AUTHORISED');
 }
 return true;
}
function outlookAdapter(){return Object.freeze({mode:'SIMULATION_DISABLED',connected:false,capabilities:Object.freeze({read:false,write:false,send:false,reminders:false,sharing:false}),simulate(draft){validateDraft(draft);return freeze({status:'SIMULATION_ONLY',taskIds:draft.taskIds||draft.followUpActions?.map(a=>a.taskId)||[],networkCalls:0,accountAccess:false,written:false});},read(){throw Error('OUTLOOK_ACCOUNT_ACCESS_NOT_AUTHORISED');},write(){throw Error('OUTLOOK_WRITES_NOT_AUTHORISED');},send(){throw Error('COUNCIL_EMAIL_NOT_AUTHORISED');},remind(){throw Error('OUTLOOK_REMINDERS_NOT_AUTHORISED');}});}
function scenarioPayload(draft,{stationId='water'}={}){validateDraft(draft);fail(draft.classification==='SYNTHETIC','PUBLIC_DRAFT_REQUIRES_SEPARATE_REVIEW');return {id:draft.id,kind:'WorkPackage',label:draft.title||draft.assistantLabel,stationId,scope:{region:'SYNTHETIC_PLACE',boundary:'CSOI_DRAFT_PREPARATION',period:draft.period},data:{status:'SYNTHETIC',assistantDraft:JSON.parse(JSON.stringify(draft))},reason:'Store synthetic draft preparation in existing Atlas immutable model; not an official decision'};}
function governance(){const g=typeof module!=='undefined'?require('./csoi-governance.js'):root.AtlasCSOIGovernance;fail(g,'GOVERNANCE_NOT_AVAILABLE');return g;}
async function draftRecord(draft){validateDraft(draft);fail(draft.classification==='SYNTHETIC','PUBLIC_DRAFT_EXPORT_REQUIRES_SEPARATE_REVIEW');return governance().makeRecord({id:draft.id,ownerModule:'CSOI_OPERATIONS',layer:'L4',security:'PUBLIC',sourceClass:'SYNTHETIC',judgment:'EVIDENCE_INFERENCE',authority:'INDEPENDENT_RESEARCH',scope:{region:'SYNTHETIC_PLACE',boundary:'CSOI_DRAFT_PREPARATION',period:draft.period},inputs:[],data:{draft:JSON.parse(JSON.stringify(draft))},sensitivity:{personalData:false,confidential:false,reidentifiable:false},provenance:{contentMode:'SYNTHETIC',rights:{mode:'SYNTHETIC_OWNED',basis:'Repository-authored synthetic preparation only'}},observedAt:new Date().toISOString()});}
async function exportDraft(draft){return governance().exportPublic([await draftRecord(draft)]);}
async function importDraft(text){const records=await governance().importPublic(text);fail(records.length===1,'ONE_DRAFT_REQUIRED');const draft=records[0].data.draft;validateDraft(draft);fail(draft.classification==='SYNTHETIC','PUBLIC_DRAFT_REQUIRES_SEPARATE_REVIEW');return freeze(draft);}
const api={compileWeek,meetingDraft,validateDraft,outlookAdapter,scenarioPayload,draftRecord,exportDraft,importDraft};root.AtlasCSOIAssistant=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
