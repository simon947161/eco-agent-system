/* Plan-level, read-only WCOS bridge. This does not implement or connect to private WCOS. */
(function(root){
'use strict';
const M=typeof module!=='undefined'?require('./atlas-model.js'):root.AtlasModel;
const G=typeof module!=='undefined'?require('./csoi-governance.js'):root.AtlasCSOIGovernance;
const FORMAT='csoi-wcos-abstract-1';
const JUDGMENTS=Object.freeze(['RULE','EVIDENCE_INFERENCE','DISCRETION','FORMAL_DECISION']);
const CHAIN=Object.freeze(['MISSION','OPERATING_YEAR','QUARTER','MONTH','WEEK','DAY','TASK','PREMISES','FIELD_BRIEF','EXECUTION','FOLLOW_UP','ANNUAL_REPORT']);
const need=(ok,code)=>{if(!ok)throw Error(code);};
const clone=v=>structuredClone(v);
function freeze(v){if(v&&typeof v==='object'){Object.values(v).forEach(freeze);Object.freeze(v);}return v;}
function day(value){return typeof value==='string'&&/^\d{4}-\d{2}-\d{2}$/.test(value)&&Number.isFinite(Date.parse(value))&&new Date(value).toISOString().slice(0,10)===value;}
function syntheticFixture(){
 const records=[
  {id:'SYN-WCOS-MISSION',kind:'MISSION',parentId:null,label:'Synthetic regulatory learning mission',stationId:'water'},
  {id:'SYN-WCOS-YEAR',kind:'OPERATING_YEAR',parentId:'SYN-WCOS-MISSION',label:'Synthetic operating year',stationId:'water'},
  {id:'SYN-WCOS-QUARTER',kind:'QUARTER',parentId:'SYN-WCOS-YEAR',label:'Synthetic quarter',stationId:'water'},
  {id:'SYN-WCOS-MONTH',kind:'MONTH',parentId:'SYN-WCOS-QUARTER',label:'Synthetic month',stationId:'water'},
  {id:'SYN-WCOS-WEEK',kind:'WEEK',parentId:'SYN-WCOS-MONTH',label:'Synthetic week',stationId:'water'},
  {id:'SYN-WCOS-DAY',kind:'DAY',parentId:'SYN-WCOS-WEEK',label:'Synthetic day',stationId:'water'},
  {id:'SYN-WCOS-TASK',kind:'TASK',parentId:'SYN-WCOS-DAY',label:'Synthetic preparation task',stationId:'water'},
  {id:'SYN-WCOS-PREMISES',kind:'PREMISES',parentId:'SYN-WCOS-TASK',label:'Synthetic activity object — no address or customer',stationId:'water'},
  {id:'SYN-WCOS-BRIEF',kind:'FIELD_BRIEF',parentId:'SYN-WCOS-PREMISES',label:'Synthetic field brief',stationId:'water'},
  {id:'SYN-WCOS-EXECUTION',kind:'EXECUTION',parentId:'SYN-WCOS-BRIEF',label:'Synthetic execution proposal, not completed work',stationId:'water'},
  {id:'SYN-WCOS-FOLLOWUP',kind:'FOLLOW_UP',parentId:'SYN-WCOS-EXECUTION',label:'Synthetic follow-up review',stationId:'water'},
  {id:'SYN-WCOS-REPORT',kind:'ANNUAL_REPORT',parentId:'SYN-WCOS-FOLLOWUP',label:'Synthetic annual report preparation',stationId:'water'}
 ];
 return {format:FORMAT,classification:'PUBLIC',synthetic:true,sourceKind:'AUTHOR_SYNTHETIC_TEMPLATE',records};
}
function noSensitiveKeys(value){
 const forbidden=/^(?:name|customer|customerName|address|email|phone|account|accountNumber|parcel|coordinates|latitude|longitude|employee|officer|token|password|secret|approval|approvedBy)$/i;
 const queue=[value];for(let i=0;i<queue.length;i++){need(i<10000,'ADAPTER_LIMIT');const v=queue[i];if(v&&typeof v==='object')for(const [key,child]of Object.entries(v)){need(!forbidden.test(key),'PROTECTED_FIELD_DENIED');if(child&&typeof child==='object')queue.push(child);}}
}
function adapt(envelope,{mode='READ_ONLY',verifyPublicSource=null}={}){
 need(mode==='READ_ONLY','READ_ONLY_ADAPTER');need(envelope&&Object.getPrototypeOf(envelope)===Object.prototype,'ADAPTER_FORMAT');
 need(envelope.classification==='PUBLIC','CLASSIFICATION_DENIED');noSensitiveKeys(envelope);
 need(envelope.format===FORMAT&&Array.isArray(envelope.records)&&envelope.records.length<=1000,'ADAPTER_FORMAT');
 let records;
 if(envelope.synthetic===true){
  // An arbitrary payload labelled "synthetic" is not a licence to copy protected records.
  need(M.canonical(envelope)===M.canonical(syntheticFixture()),'UNTRUSTED_SYNTHETIC_FIXTURE');records=clone(envelope.records);
 }else{
  need(envelope.synthetic===false&&envelope.sourceKind==='VETTED_PUBLIC_METADATA'&&typeof verifyPublicSource==='function','PUBLIC_SOURCE_REVIEW_REQUIRED');
  const allowed=new Set(['id','kind','label','url','sourceId','revisionId','locator','stationId']);
  records=envelope.records.map(r=>{
   need(r&&Object.keys(r).every(k=>allowed.has(k))&&r.kind==='PUBLIC_RULE_METADATA'&&typeof r.id==='string'&&typeof r.label==='string'&&r.label.length<=300&&r.sourceId&&r.revisionId&&r.locator,'PUBLIC_METADATA_ONLY');
   const url=new URL(r.url);need(url.protocol==='https:'&&!url.username&&!url.password,'UNSAFE_PUBLIC_URL');
   need(verifyPublicSource(clone(r))===true,'PUBLIC_SOURCE_REVIEW_REQUIRED');return clone(r);
  });
 }
 need(G&&G.inspectPayload(envelope).length===0,'PUBLIC_PAYLOAD_DENIED');
 return freeze({format:FORMAT,classification:'PUBLIC',synthetic:envelope.synthetic,records,mode:'READ_ONLY',sync:'NOT_CONNECTED',privateCompatibility:'BLOCKED_AUTHORISED_TECHNICAL_CONTRACT_NOT_SUPPLIED',governmentAuthority:false});
}
function condition(value,whenTrue,whenFalse){return value===true?whenTrue:value===false?whenFalse:'UNKNOWN';}
function conditionalServices(activity={}){
 const result={food:condition(activity.handlesFood,'APPLICABLE_FOR_RESEARCH','NOT_APPLICABLE'),ltw:'UNKNOWN',backflow:'UNKNOWN'};
 if(activity.dischargesLiquidTradeWaste===false||activity.sewerConnection===false)result.ltw='NOT_APPLICABLE';
 else if(activity.dischargesLiquidTradeWaste===true&&activity.sewerConnection===true)result.ltw='APPLICABLE_FOR_RESEARCH';
 if(activity.testableBackflowDevice===false||activity.waterConnection===false)result.backflow='NOT_APPLICABLE';
 else if(activity.testableBackflowDevice===true&&activity.waterConnection===true)result.backflow='APPLICABLE_FOR_RESEARCH';
 return {...result,judgment:'EVIDENCE_INFERENCE',authority:'NONE',officialApproval:'BLOCKED',ruleStatus:'PUBLIC_RULE_AND_LOCAL_APPLICABILITY_REVIEW_REQUIRED',explanation:'Activities, sewer discharge and testable devices are separate conditions. A property or business label alone establishes none of the three obligations.'};
}
function ltwWorkflow(activity={}){
 const services=conditionalServices(activity),category=['A','B','C','S'].includes(activity.ltwCategory)?activity.ltwCategory:'UNKNOWN';
 const stages=[['INTAKE','Register and screen the discharge activity'],['INFORMATION','Identify missing discharge, process and sewer-connection facts'],['CLASSIFICATION','Check classification and exact guideline conditions'],['APPROVAL_EVIDENCE','Check Council approval and any concurrence evidence'],['FIELD_REVIEW','Prepare a reviewable field brief'],['PRETREATMENT','Record applicable pretreatment evidence'],['MONITORING','Review applicable monitoring evidence'],['RECTIFICATION','Record defects and proposed corrective follow-up'],['RECHECK','Prepare any required reinspection'],['CLOSE_REPORT','Review evidence before closure or reporting']];
 return {format:'csoi-ltw-workflow-1',applicability:services.ltw,category,categoryVerification:'UNKNOWN',classificationAuthority:'NONE',stages:stages.map(([id,label])=>({id,label,status:'PROPOSED',judgment:id==='CLASSIFICATION'?'RULE':id==='APPROVAL_EVIDENCE'?'FORMAL_DECISION':'EVIDENCE_INFERENCE',sourceAnchor:'UNKNOWN',responsibleRole:'UNKNOWN',completed:false})),limitations:['This is a research work template, not an internal Council SOP.','A/B/C/S membership is not computed without a verified rule and discharge facts.','No AI approval, concurrence or Council decision is issued.']};
}
function verifiedPublicRule(rule){
 try{const phe=typeof module!=='undefined'?require('./csoi-phe.js'):(root.CsoiPhe||root.AtlasCSOIPhe);return typeof phe?.backflowRule==='function'&&M.canonical(rule)===M.canonical(phe.backflowRule());}catch{return false;}
}
function addMonths(date,months){const original=new Date(date+'T00:00:00Z'),year=original.getUTCFullYear(),month=original.getUTCMonth(),dayOfMonth=original.getUTCDate(),end=new Date(Date.UTC(year,month+months+1,0)).getUTCDate();return new Date(Date.UTC(year,month+months,Math.min(dayOfMonth,end))).toISOString().slice(0,10);}
function backflowDue(device={},rule={},asOf){
 need(day(asOf),'AS_OF_DATE_REQUIRED');
 const unknown=reason=>({status:'UNKNOWN',dueDate:null,reason,officialCompliance:'UNKNOWN',governmentDecision:false});
 if(device.testable===false)return {status:'NOT_APPLICABLE',dueDate:null,reason:'Fixture says this is not a testable device; no recurring test date is inferred.',officialCompliance:'UNKNOWN',governmentDecision:false};
 if(device.testable!==true||!device.deviceType||!day(device.lastTestDate))return unknown('A known testable device type and valid last-test date are required.');
 if(device.lastTestDate>asOf)return unknown('The recorded last-test date is after the as-of date.');
 if(!Number.isInteger(rule.intervalMonths)||rule.intervalMonths<1||rule.intervalMonths>120||!(Array.isArray(rule.deviceTypes)&&rule.deviceTypes.includes(device.deviceType)||rule.applicability==='TESTABLE_DEVICE'&&device.testable===true))return unknown('No applicable device-specific interval is established.');
 if(rule.classification!=='SYNTHETIC_SCENARIO'&&!(rule.classification==='PUBLIC'&&verifiedPublicRule(rule)&&rule.anchorVerified===true&&rule.currentVersionChecked===true&&rule.sourceId&&rule.locator&&rule.revisionId))return unknown('An independently anchored, current public interval or labelled synthetic rule is required.');
 if(rule.validFrom&&!day(rule.validFrom)||rule.validTo&&!day(rule.validTo))return unknown('The rule effective interval is malformed.');
 if(rule.validFrom&&asOf<rule.validFrom||rule.validTo&&asOf>rule.validTo)return unknown('The rule is outside its verified effective interval.');
 if(rule.region&&device.region!==rule.region)return unknown('Device region and rule scope differ.');
 const dueDate=addMonths(device.lastTestDate,rule.intervalMonths);
 return {status:dueDate<asOf?'OVERDUE':dueDate===asOf?'DUE':'NOT_YET_DUE',dueDate,reason:'Last-test date plus the explicitly applicable interval; this is a schedule, not a compliance ruling.',classification:rule.classification,sourceId:rule.sourceId||'SYNTHETIC_RULE',sourceRevision:rule.revisionId||'SYNTHETIC_RULE',officialCompliance:'UNKNOWN',governmentDecision:false};
}
function judgment(kind,{statement='',sourceIds=[],reviewer=null}={}){
 need(G&&G.inspectPayload({statement,sourceIds,reviewer}).length===0,'PUBLIC_PAYLOAD_DENIED');
 need(JUDGMENTS.includes(kind),'JUDGMENT_CLASS');need(typeof statement==='string'&&statement.length<=2000&&Array.isArray(sourceIds),'JUDGMENT_FIELDS');
 return freeze({kind,statement,sourceIds:clone(sourceIds),reviewer:kind==='FORMAL_DECISION'?null:reviewer,status:kind==='FORMAL_DECISION'?'BLOCKED':kind==='RULE'&&!sourceIds.length?'UNKNOWN':'DRAFT_FOR_REVIEW',authority:'NONE',governmentApproval:false,requiresHumanReview:true,reason:kind==='FORMAL_DECISION'?'Formal decisions remain with an explicitly authorised human in the authoritative Council system.':'Research judgment class kept distinct from official authority.'});
}
function summary(records,{minimumCellSize=5,synthetic=false}={}){
 need(Array.isArray(records)&&records.length<=10000&&Number.isInteger(minimumCellSize)&&minimumCellSize>=5,'SUMMARY_BOUNDS');
 need(synthetic===true&&records.every(r=>typeof r.id==='string'&&r.id.startsWith('SYN-')),'REAL_RECORD_SUMMARY_NOT_AUTHORISED');
 need(G&&G.inspectPayload(records).length===0,'PUBLIC_PAYLOAD_DENIED');
 const ids=new Set(records.map(r=>r.id));need(ids.size===records.length,'DUPLICATE_OBJECT');
 const groups={};for(const row of records){const kind=CHAIN.includes(row.kind)?row.kind:'UNKNOWN';groups[kind]=(groups[kind]||0)+1;}
 return {classification:'PUBLIC',synthetic:true,denominator:ids.size,groups,suppression:'SYNTHETIC_ONLY_NOT_REAL_STATISTICS',realSmallSamplePolicy:'DENY_REAL_RECORDS; authorised future aggregate release must suppress small cells and pass independent disclosure review',minimumCellSize,officialKpi:'UNKNOWN'};
}
const api={FORMAT,JUDGMENTS,CHAIN,syntheticFixture,adapt,conditionalServices,ltwWorkflow,backflowDue,judgment,summary};
root.AtlasCSOIWcos=api;root.CsoiWcos=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
