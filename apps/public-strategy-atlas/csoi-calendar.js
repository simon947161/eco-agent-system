/* Calendar projections and synthetic task cards over the existing Atlas model.
 * Dates are UTC civil dates; no Outlook, Council records or automatic scheduling. */
(function(root){
'use strict';
const FORMAT='csoi-annual-edition-1';
const ORIGINS=['LEGAL_OBLIGATION','PUBLIC_OPERATIONAL_GOAL','AUTHORISED_ASSIGNMENT','PERSONAL_LEARNING','RESEARCH_PROPOSAL'];
const TASK_KEYS=new Set('id title date dueDate sourceType classification sourceBasis applicability responsibleRole reviewRole approval expectedHours actualHours quantity attachments nextStep discretion evidenceRefs revisions executionStatus workItemId fieldBriefId followUpId reportId stationId dependencies risk'.split(' '));
const UNKNOWN='UNKNOWN';
function fail(ok,code){if(!ok)throw Error(code);}
function freeze(value){const stack=[value];while(stack.length){const x=stack.pop();if(x&&typeof x==='object'&&!Object.isFrozen(x)){for(const v of Object.values(x))if(v&&typeof v==='object')stack.push(v);Object.freeze(x);}}return value;}
function copy(v){return JSON.parse(JSON.stringify(v));}
function day(value){fail(typeof value==='string'&&/^\d{4}-\d{2}-\d{2}$/.test(value),'CIVIL_DATE_REQUIRED');const date=new Date(value+'T00:00:00Z');fail(Number.isFinite(+date)&&date.toISOString().slice(0,10)===value,'INVALID_CIVIL_DATE');return date;}
function dateText(date){return date.toISOString().slice(0,10);}
function addDays(value,count){fail(Number.isSafeInteger(count)&&Math.abs(count)<=40000,'DAY_INTERVAL_BOUNDS');const date=day(value);date.setUTCDate(date.getUTCDate()+count);return dateText(date);}
function monthEnd(y,m){return new Date(Date.UTC(y,m,0)).getUTCDate();}
function addMonths(value,count){fail(Number.isSafeInteger(count)&&Math.abs(count)<=1200,'MONTH_INTERVAL_BOUNDS');const d=day(value),n=d.getUTCFullYear()*12+d.getUTCMonth()+count,y=Math.floor(n/12),m=n-y*12;return dateText(new Date(Date.UTC(y,m,Math.min(d.getUTCDate(),monthEnd(y,m+1)))));}
function isoWeek(value){const d=day(value),weekday=d.getUTCDay()||7;d.setUTCDate(d.getUTCDate()+4-weekday);const year=d.getUTCFullYear(),first=new Date(Date.UTC(year,0,1)),week=Math.ceil((((d-first)/86400000)+1)/7),from=addDays(value,1-weekday);return {id:year+'-W'+String(week).padStart(2,'0'),year,week,from,to:addDays(from,6)};}
function safeSource(source){try{const url=new URL(source?.url);return !!(url.protocol==='https:'&&!url.username&&!url.password&&source.locator&&source.revisionId&&source.revisionId!==UNKNOWN);}catch{return false;}}
function privacy(record){
 fail(record&&['SYNTHETIC','PUBLIC'].includes(record.classification),'NONPUBLIC_CALENDAR_RECORD');
 const encoded=JSON.stringify(record);fail(encoded.length<=200000,'CALENDAR_RECORD_TOO_LARGE');
 fail(!/(?:"(?:customerName|customerEmail|employeeEmail|streetAddress|accountNumber|accessToken|secret|councilProtected)"\s*:)/i.test(encoded),'SENSITIVE_CALENDAR_FIELD');
 const issues=governance().inspectPayload(record);fail(issues.length===0,'CALENDAR_PUBLIC_DENIED:'+issues.join(','));
 return true;
}
function validateTask(task){
 privacy(task);fail(task&&typeof task==='object'&&!Array.isArray(task),'TASK_REQUIRED');
 fail(Object.keys(task).every(k=>TASK_KEYS.has(k)),'TASK_FIELD_NOT_ALLOWED');
 fail(typeof task.id==='string'&&/^[a-zA-Z0-9:_-]{1,160}$/.test(task.id)&&typeof task.title==='string'&&task.title.trim()&&task.title.length<=240,'TASK_ID_OR_TITLE');
 day(task.date);day(task.dueDate);fail(task.date<=task.dueDate,'TASK_DUE_BEFORE_PLAN');
 fail(ORIGINS.includes(task.sourceType),'TASK_ORIGIN_REQUIRED');
 fail(task.applicability&&['APPLIES','DOES_NOT_APPLY',UNKNOWN].includes(task.applicability.state),'TASK_APPLICABILITY');
 fail(task.approval&&['UNKNOWN','PENDING_REVIEW','APPROVED_FOR_RESEARCH'].includes(task.approval.state)&&task.approval.governmentApproval===false,'OFFICIAL_APPROVAL_FORBIDDEN');
 fail(Array.isArray(task.approval.evidenceRefs),'APPROVAL_EVIDENCE_REQUIRED');
 if(task.approval.state==='APPROVED_FOR_RESEARCH')fail(task.approval.evidenceRefs.length>0,'RESEARCH_APPROVAL_WITHOUT_EVIDENCE');
 fail(['UNKNOWN','PLANNED','IN_PROGRESS','RECORDED','CANCELLED'].includes(task.executionStatus),'TASK_EXECUTION_STATE');
 for(const field of ['responsibleRole','reviewRole'])fail(typeof task[field]==='string'&&task[field].length<=240,'ROLE_REQUIRED');
 if(task.classification!=='SYNTHETIC'&&(task.responsibleRole!==UNKNOWN||task.reviewRole!==UNKNOWN))fail(safeSource(task.sourceBasis),'UNEVIDENCED_ROLE');
 if(task.sourceType==='AUTHORISED_ASSIGNMENT')fail(task.classification==='SYNTHETIC'||task.approval.evidenceRefs.length>0,'ASSIGNMENT_AUTHORISATION_MISSING');
 if(task.sourceType==='AUTHORISED_ASSIGNMENT'&&task.classification!=='SYNTHETIC')fail(false,'ASSIGNMENT_AUTHORITY_NOT_CONFIGURED');
 if(task.sourceType==='LEGAL_OBLIGATION'&&task.applicability.state==='APPLIES'&&task.classification!=='SYNTHETIC')fail(safeSource(task.sourceBasis)&&task.applicability.sourceVerified===true,'LEGAL_APPLICABILITY_UNVERIFIED');
 if(task.sourceType==='LEGAL_OBLIGATION'&&task.applicability.state==='APPLIES'&&task.classification!=='SYNTHETIC')fail(false,'LEGAL_APPLICABILITY_AUTHORITY_NOT_CONFIGURED');
 for(const field of ['expectedHours','actualHours'])fail(task[field]===UNKNOWN||typeof task[field]==='number'&&Number.isFinite(task[field])&&task[field]>=0&&task[field]<=10000,'TASK_HOURS_INVALID');
 fail(task.actualHours===UNKNOWN||task.executionStatus==='RECORDED','ACTUAL_HOURS_WITHOUT_RECORD');
 for(const key of ['attachments','evidenceRefs','revisions','dependencies'])fail(Array.isArray(task[key])&&task[key].length<=500,'TASK_ARRAY_'+key);
 fail(task.actualHours===UNKNOWN||task.evidenceRefs.length>0,'ACTUAL_HOURS_WITHOUT_EVIDENCE');
 fail(task.dependencies.every(id=>typeof id==='string'&&id.length>0)&&new Set(task.dependencies).size===task.dependencies.length,'TASK_DEPENDENCIES');
 for(const ref of task.evidenceRefs)fail(ref&&typeof ref==='object'&&typeof ref.id==='string'&&ref.id&&typeof ref.revisionId==='string'&&/^sha256:[a-f0-9]{64}$/.test(ref.revisionId),'TASK_EVIDENCE_IDENTITY');
 for(const a of task.attachments)fail(a&&typeof a.id==='string'&&['MISSING','PRESENT','UNKNOWN'].includes(a.state),'ATTACHMENT_STATE');
 for(const field of ['nextStep','discretion'])fail(typeof task[field]==='string'&&task[field].length<=3000,'TASK_CARD_'+field);
 fail(task.risk&&['UNKNOWN','LOW','MODERATE','HIGH'].includes(task.risk.level)&&typeof task.risk.basis==='string','TASK_RISK_BASIS');
 return true;
}
function taskCard(task){validateTask(task);return freeze({...copy(task),basisState:safeSource(task.sourceBasis)?'SOURCE_REFERENCE_PRESENT':'SOURCE_OR_REVISION_UNKNOWN',approvalMeaning:'Research workflow only; no Council or Michele decision',actualResult:task.executionStatus==='RECORDED'&&task.evidenceRefs.length?'RECORD_PRESENT_NOT_OUTCOME_PROOF':UNKNOWN});}
function syntheticTasks(year=2026){
 fail(Number.isSafeInteger(year)&&year>=1900&&year<=2200,'YEAR_BOUNDS');
 return [['ltw','Synthetic LTW preparation','water','11-02',3],['backflow','Synthetic backflow evidence review','water','11-03',2],['pool','Synthetic public-pool learning case','csp6','11-04',2.5],['quarter','Synthetic quarterly research review','csp','11-05',1.5]].map(([suffix,title,stationId,monthday,hours],i)=>({
  id:'csoi:task:'+year+':'+suffix,title,date:year+'-'+monthday,dueDate:year+'-'+monthday,sourceType:i===2?'PERSONAL_LEARNING':'RESEARCH_PROPOSAL',classification:'SYNTHETIC',sourceBasis:null,
  applicability:{state:UNKNOWN,conditions:['Synthetic learning case; actual local obligation and device applicability unverified']},responsibleRole:UNKNOWN,reviewRole:UNKNOWN,
  approval:{state:UNKNOWN,evidenceRefs:[],governmentApproval:false},expectedHours:hours,actualHours:UNKNOWN,quantity:UNKNOWN,
  attachments:[{id:'synthetic-source-material:'+suffix,state:'MISSING'}],nextStep:'Verify source, applicability and authorised review before any real activity.',discretion:'Human reviewer must decide applicability and operational action; no automatic approval.',
  evidenceRefs:[],revisions:[],executionStatus:'PLANNED',workItemId:'csoi:work:'+suffix,fieldBriefId:'csoi:brief:'+suffix,followUpId:'csoi:followup:'+suffix,reportId:'csoi:report:'+year,stationId,dependencies:[],risk:{level:i===1?'HIGH':UNKNOWN,basis:'SYNTHETIC_REHEARSAL_NOT_ACTUAL_REGULATORY_RISK'}
 }));
}
function annualEdition({year,missionId='csoi:mission:research',yearBasis='CALENDAR',tasks=[]}={}){
 fail(Number.isSafeInteger(year)&&year>=1900&&year<=2200,'YEAR_BOUNDS');fail(['CALENDAR','AU_FISCAL'].includes(yearBasis),'YEAR_BASIS');fail(typeof missionId==='string'&&/^[\w:-]{1,160}$/.test(missionId),'MISSION_ID');
 fail(Array.isArray(tasks)&&tasks.length<=10000,'TASK_LIMIT');const ids=new Set();
 for(const task of tasks){validateTask(task);fail(!ids.has(task.id),'DUPLICATE_TASK');ids.add(task.id);}
 const start=year+(yearBasis==='CALENDAR'?'-01-01':'-07-01'),end=yearBasis==='CALENDAR'?year+'-12-31':(year+1)+'-06-30';
 for(const task of tasks)fail(task.date>=start&&task.date<=end,'TASK_OUTSIDE_EDITION');
 const prefix='calendar:'+yearBasis+':'+year,editionId=prefix+':year',nodes=[],byId=new Map();
 function put(node){if(byId.has(node.id))return byId.get(node.id);const n={...node,parentIds:[],childIds:[]};nodes.push(n);byId.set(n.id,n);return n;}
 function link(parentId,childId){const parent=byId.get(parentId),child=byId.get(childId);fail(parent&&child,'CALENDAR_LINK');if(!parent.childIds.includes(childId))parent.childIds.push(childId);if(!child.parentIds.includes(parentId))child.parentIds.push(parentId);}
 put({id:missionId,kind:'MISSION',label:'Independent research mission',from:start,to:end});
 put({id:editionId,kind:'OPERATING_YEAR',label:yearBasis==='CALENDAR'?String(year):'FY'+year+'–'+String(year+1).slice(2),from:start,to:end});link(missionId,editionId);
 for(let i=0;i<12;i++){
  const first=addMonths(start,i),last=addDays(addMonths(start,i+1),-1),quarter=Math.floor(i/3)+1,qId=prefix+':Q'+quarter,mId=prefix+':month:'+first.slice(0,7);
  if(!byId.has(qId)){put({id:qId,kind:'QUARTER',label:'Operating quarter '+quarter,quarter,from:first,to:addDays(addMonths(start,quarter*3),-1)});link(editionId,qId);}
  put({id:mId,kind:'MONTH',label:day(first).toLocaleString('en-AU',{month:'long',year:'numeric',timeZone:'UTC'}),from:first,to:last});link(qId,mId);
 }
 for(let date=start;date<=end;date=addDays(date,1)){
  const week=isoWeek(date),wId=prefix+':week:'+week.id,mId=prefix+':month:'+date.slice(0,7),dId=prefix+':day:'+date;
  put({id:wId,kind:'WEEK',label:'ISO '+week.id,isoYear:week.year,isoWeek:week.week,from:week.from,to:week.to,inEditionFrom:week.from<start?start:week.from,inEditionTo:week.to>end?end:week.to});link(mId,wId);
  put({id:dId,kind:'DAY',label:date,date,from:date,to:date});link(wId,dId);
 }
 for(const task of tasks){
  put({id:task.id,kind:'TASK',label:task.title,from:task.date,to:task.dueDate,taskId:task.id});link(prefix+':day:'+task.date,task.id);
  const work=task.workItemId||task.id+':work',brief=task.fieldBriefId||task.id+':brief',execution=task.id+':execution',follow=task.followUpId||task.id+':followup',report=task.reportId||prefix+':report';
  for(const [id,kind,label] of [[work,'WORK_ITEM','Work item'],[brief,'FIELD_BRIEF','Field brief / preparation'],[execution,'EXECUTION','Execution record'],[follow,'FOLLOW_UP','Follow-up'],[report,'REPORT','Annual research report']])put({id,kind,label:label+' · '+(kind==='REPORT'?year:task.title),from:kind==='REPORT'?start:task.date,to:kind==='REPORT'?end:task.dueDate,taskId:kind==='REPORT'?null:task.id,state:UNKNOWN});
  link(task.id,work);link(work,brief);link(brief,execution);
  const evidence=task.evidenceRefs.length?task.evidenceRefs:[{id:task.id+':evidence-gap'}];
  for(const [i,ref] of evidence.entries()){const eId=task.id+':evidence:'+i;put({id:eId,kind:'EVIDENCE',label:task.evidenceRefs.length?'Evidence reference · '+(ref.id||ref.locator||i):'Evidence gap · UNKNOWN',reference:copy(ref),from:task.date,to:task.dueDate,taskId:task.id,state:task.evidenceRefs.length?'REFERENCE_NOT_VERIFIED':UNKNOWN});link(execution,eId);link(eId,follow);}
  link(follow,report);link(editionId,report);
 }
 // Indexes and links are reproducible projections, not a second authoritative graph.
 return freeze({format:FORMAT,year,yearBasis,missionId,editionId,start,end,nodes,tasks:copy(tasks),classification:tasks.every(t=>t.classification==='SYNTHETIC')?'SYNTHETIC':'PUBLIC',scope:'Independent public/synthetic research edition; no Council schedule',provenance:'DERIVED_CIVIL_DATE_PROJECTION_V1'});
}
function index(edition){fail(edition?.format===FORMAT&&Array.isArray(edition.nodes),'EDITION_FORMAT');return new Map(edition.nodes.map(n=>[n.id,n]));}
function page(records,{offset=0,limit=50}={}){fail(Number.isSafeInteger(offset)&&offset>=0&&Number.isSafeInteger(limit)&&limit>=1&&limit<=100,'CALENDAR_PAGE_BOUNDS');return {items:records.slice(offset,offset+limit),total:records.length,offset,nextOffset:offset+limit<records.length?offset+limit:null};}
function children(edition,id,options={}){const map=index(edition),node=map.get(id);fail(node,'CALENDAR_NOT_FOUND');let records=node.childIds.map(key=>map.get(key));if(options.within){const scope=map.get(options.within);fail(scope,'SCOPE_NOT_FOUND');records=records.filter(n=>n.to>=scope.from&&n.from<=scope.to);}return page(records,options);}
function parents(edition,id){const map=index(edition),node=map.get(id);fail(node,'CALENDAR_NOT_FOUND');return node.parentIds.map(key=>map.get(key));}
function query(edition,{from=edition.start,to=edition.end,sourceType=null,executionStatus=null,kind='TASK',offset=0,limit=50}={}){day(from);day(to);fail(from<=to,'QUERY_PERIOD');fail(['TASK','DAY','WEEK','MONTH','QUARTER','OPERATING_YEAR','MISSION','WORK_ITEM','FIELD_BRIEF','EXECUTION','EVIDENCE','FOLLOW_UP','REPORT'].includes(kind),'QUERY_KIND');const tasks=new Map(edition.tasks.map(t=>[t.id,t]));return page(edition.nodes.filter(n=>n.kind===kind&&n.to>=from&&n.from<=to&&(!sourceType||tasks.get(n.taskId)?.sourceType===sourceType)&&(!executionStatus||tasks.get(n.taskId)?.executionStatus===executionStatus)),{offset,limit});}
function trace(edition,id,{limit=100}={}){fail(Number.isSafeInteger(limit)&&limit>=1&&limit<=500,'TRACE_BOUNDS');const map=index(edition);fail(map.has(id),'CALENDAR_NOT_FOUND');const seen=new Set(),queue=[id],nodes=[];for(let i=0;i<queue.length&&nodes.length<limit;i++){const key=queue[i];if(seen.has(key))continue;seen.add(key);const n=map.get(key);nodes.push(n);queue.push(...n.parentIds);}return {nodes,truncated:queue.some(key=>!seen.has(key)),meaning:'Calendar ancestry only; strategy attribution remains source-gated'};}
function recurrence({start,until,everyDays=null,everyMonths=null,applicability,sourceBasis,classification='SYNTHETIC',exceptions=[],maxOccurrences=500}={}){
 privacy({classification,start,until,everyDays,everyMonths,applicability,sourceBasis,exceptions,maxOccurrences});
 day(start);day(until);fail(start<=until,'RECURRENCE_PERIOD');fail(Number.isSafeInteger(maxOccurrences)&&maxOccurrences>=1&&maxOccurrences<=1000,'RECURRENCE_BOUNDS');
 fail((Number.isSafeInteger(everyDays)&&everyDays>0&&everyDays<=3660&&everyMonths===null)||(Number.isSafeInteger(everyMonths)&&everyMonths>0&&everyMonths<=120&&everyDays===null),'RECURRENCE_INTERVAL');
 fail(Array.isArray(exceptions)&&exceptions.length<=1000,'RECURRENCE_EXCEPTIONS');exceptions.forEach(day);fail(new Set(exceptions).size===exceptions.length,'DUPLICATE_RECURRENCE_EXCEPTION');
 if(applicability?.state!=='APPLIES')return freeze({state:applicability?.state==='DOES_NOT_APPLY'?'NOT_APPLICABLE':'PENDING_APPLICABILITY',dates:[],reason:'A known applicable obligation or explicit synthetic condition is required; no default duty for every premises.'});
 fail(classification==='SYNTHETIC'||classification==='PUBLIC'&&safeSource(sourceBasis),'RECURRENCE_SOURCE_UNKNOWN');
 fail(classification==='SYNTHETIC'||applicability.sourceVerified===true,'RECURRENCE_RULE_UNVERIFIED');
 if(classification==='PUBLIC')return freeze({state:'PENDING_AUTHORISED_RULE_REVIEW',dates:[],reason:'Caller-supplied source verification flags cannot establish current statutory applicability; no independent authority verifier is configured.',governmentApproval:false});
 const dates=[];let n=0,next=start;for(;next<=until;n++){
  if(!exceptions.includes(next))dates.push(next);fail(dates.length<=maxOccurrences,'RECURRENCE_CAP');
  const following=everyMonths!==null?addMonths(start,(n+1)*everyMonths):addDays(start,(n+1)*everyDays);fail(following>next,'RECURRENCE_CYCLE');next=following;
 }
 return freeze({state:'PROPOSED_SCHEDULE',dates,method:'csoi-recurrence-1; monthly clamp anchored to original day',classification,governmentApproval:false});
}
function conflicts(tasks){tasks.forEach(validateTask);const map=new Map(tasks.map(t=>[t.id,t])),issues=[];fail(map.size===tasks.length,'DUPLICATE_TASK');
 for(const t of tasks)for(const ref of t.dependencies){if(!map.has(ref))issues.push({taskId:t.id,code:'MISSING_DEPENDENCY',dependency:ref});else if(map.get(ref).dueDate>t.date)issues.push({taskId:t.id,code:'DEPENDENCY_AFTER_START',dependency:ref});}
 const colors=new Map();for(const task of tasks){if(colors.get(task.id)===2)continue;const stack=[[task.id,0]];while(stack.length){const [id,pos]=stack.at(-1),t=map.get(id);if(!t){stack.pop();continue;}if(pos===0)colors.set(id,1);if(pos>=t.dependencies.length){colors.set(id,2);stack.pop();continue;}stack[stack.length-1][1]++;const next=t.dependencies[pos];if(colors.get(next)===1)issues.push({taskId:id,code:'DEPENDENCY_CYCLE',dependency:next});else if(map.has(next)&&colors.get(next)!==2)stack.push([next,0]);}}
 return issues;
}
function scenarioPayload(task){validateTask(task);fail(task.classification==='SYNTHETIC','PUBLIC_TASK_REGISTRATION_REQUIRES_REVIEW');return {id:task.id,kind:'Task',label:task.title,stationId:task.stationId||'water',scope:{region:'SYNTHETIC_PLACE',period:{from:task.date,to:task.dueDate},boundary:'CSOI_SYNTHETIC_RESEARCH'},data:{status:'SYNTHETIC',csoiTask:copy(task)},reason:'Register synthetic Annual Edition task; no Council assignment or approval'};}
function governance(){const g=typeof module!=='undefined'?require('./csoi-governance.js'):root.AtlasCSOIGovernance;fail(g,'GOVERNANCE_NOT_AVAILABLE');return g;}
async function taskRecord(task){validateTask(task);fail(task.classification==='SYNTHETIC','PUBLIC_TASK_EXPORT_REQUIRES_SEPARATE_REVIEW');const g=governance();return g.makeRecord({id:task.id,ownerModule:'CSOI_OPERATIONS',layer:'L2',security:'PUBLIC',sourceClass:'SYNTHETIC',judgment:'OBSERVATION',authority:'INDEPENDENT_RESEARCH',scope:{region:'SYNTHETIC_PLACE',boundary:'CSOI_SYNTHETIC_RESEARCH',period:{from:task.date,to:task.dueDate}},inputs:[],data:{task:copy(task)},sensitivity:{personalData:false,confidential:false,reidentifiable:false},provenance:{contentMode:'SYNTHETIC',rights:{mode:'SYNTHETIC_OWNED',basis:'Repository-authored synthetic fixture'}},observedAt:new Date().toISOString()});}
async function exportTasks(tasks){fail(Array.isArray(tasks)&&tasks.length<=10000,'TASK_LIMIT');const records=await Promise.all(tasks.map(taskRecord));return governance().exportPublic(records);}
async function importTasks(text){const records=await governance().importPublic(text);fail(Array.isArray(records)&&records.length<=10000,'TASK_LIMIT');const tasks=records.map(r=>r.data.task);tasks.forEach(task=>{validateTask(task);fail(task.classification==='SYNTHETIC','PUBLIC_TASK_EXPORT_REQUIRES_SEPARATE_REVIEW');});return freeze(tasks);}
const api={FORMAT,ORIGINS,day,addDays,addMonths,isoWeek,validateTask,taskCard,syntheticTasks,annualEdition,index,children,parents,query,trace,recurrence,conflicts,scenarioPayload,privacy,taskRecord,exportTasks,importTasks};root.AtlasCSOICalendar=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
