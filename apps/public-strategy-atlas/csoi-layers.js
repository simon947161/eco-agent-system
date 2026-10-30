/* L0–L5 are research transformations, never permission upgrades or official decisions. */
(function(root){
'use strict';
const M=typeof module!=='undefined'?require('./atlas-model.js'):root.AtlasModel;
const G=typeof module!=='undefined'?require('./csoi-governance.js'):root.AtlasCSOIGovernance;
const A=typeof module!=='undefined'?require('./atlas-accounting.js'):root.AtlasAccounting;
const METHODS=Object.freeze({NORMALIZE:'csoi-identity-1',STATEMENT:'csoi-statement-1',CALCULATE:'csoi-calculation-1',AGGREGATE:'csoi-management-1',RELEASE:'csoi-release-draft-1'});
const IDENTITY_TYPES=new Set(['PROPERTY','PREMISES','BUSINESS_ACTIVITY','CONNECTION_POINT','DEVICE','WORK_EVENT']);
const STATES=new Set(['ACTIVE','WITHDRAWN']);
function need(value,code){if(!value)throw Error(code);}
function same(a,b){return M.canonical(a)===M.canonical(b);}
function currentRecords(d){return [...M.domainIndex(d).values()].map(e=>e.data?.csoiRecord||e.data?.csoi).filter(Boolean);}
function find(d,id){return M.domainIndex(d).get(id)?.data?.csoiRecord||M.domainIndex(d).get(id)?.data?.csoi||null;}
function normalizeIdentity({type,id,namespace='SYNTHETIC',validFrom,validTo}){
 need(IDENTITY_TYPES.has(type)&&typeof namespace==='string'&&/^[A-Z0-9_-]{1,40}$/.test(namespace)&&typeof id==='string'&&id.trim().length>0&&id.length<=160,'IDENTITY_REQUIRED');
 const normalized=id.trim().replace(/\s+/g,' ').toUpperCase();need(/^[A-Z0-9:._/-]+$/.test(normalized),'IDENTITY_NOT_A_SAFE_ABSTRACT_KEY');
 need(typeof validFrom==='string'&&typeof validTo==='string'&&/^\d{4}-\d{2}-\d{2}$/.test(validFrom)&&/^\d{4}-\d{2}-\d{2}$/.test(validTo)&&Number.isFinite(Date.parse(validFrom))&&Number.isFinite(Date.parse(validTo))&&new Date(validFrom).toISOString().slice(0,10)===validFrom&&new Date(validTo).toISOString().slice(0,10)===validTo&&validFrom<=validTo,'IDENTITY_INTERVAL');
 return {type,id:namespace+':'+type+':'+normalized,originalKey:id,namespace,validFrom,validTo};
}
function quality(records,{asOf=null,expectedUnit=null}={}){
 const reasons=new Set(),ids=new Set(),identities=new Set();let scope=null;
 if(!Array.isArray(records)||!records.length||records.length>10000)return {passed:false,reasons:['INPUT_RECORDS_REQUIRED']};
 for(const r of records){
  for(const issue of G.validateRecord(r))reasons.add(issue);
  if(ids.has(r.id))reasons.add('DUPLICATE_INPUT_RECORD');ids.add(r.id);
  if(!G.assessPublic(r,{operation:'STORAGE'}).allowed)reasons.add('PUBLIC_TRANSFORMATION_DENIED');
  if(r.state!=='ACTIVE')reasons.add('INPUT_WITHDRAWN_OR_STATE_UNKNOWN');
  if(scope&&!same(scope,r.scope))reasons.add('TIME_OR_GEOGRAPHY_MISMATCH');scope=r.scope;
  if(Array.isArray(r.data?.sourceConflicts)&&r.data.sourceConflicts.length)reasons.add('UNRESOLVED_SOURCE_CONFLICT');
  if(r.data?.sourceLost===true)reasons.add('SOURCE_LOST');
  if(r.data?.legalState&&r.data.legalState!=='ADOPTED')reasons.add('LEGAL_STATE_NOT_EFFECTIVE');
  if(asOf&&r.data?.validTo&&r.data.validTo<asOf)reasons.add('EXPIRED_RULE');
  if(asOf&&r.data?.validFrom&&r.data.validFrom>asOf)reasons.add('RULE_NOT_YET_EFFECTIVE');
  if(expectedUnit&&r.data?.measurement?.unit!==expectedUnit)reasons.add('UNIT_MISMATCH');
  for(const identity of r.data?.identities||[]){if(identities.has(identity.id))reasons.add('DUPLICATE_IDENTITY');identities.add(identity.id);}
 }
 return {passed:reasons.size===0,reasons:[...reasons].sort(),scope};
}
async function validate(records,options){
 const report=quality(records,options);for(const r of records||[])if(!await G.verifyRecord(r))report.reasons.push('INPUT_RECEIPT_INVALID');
 report.reasons=[...new Set(report.reasons)].sort();report.passed=report.reasons.length===0;return report;
}
async function source(input){
 need(input?.layer===undefined||input.layer==='L0','SOURCE_LAYER_MUST_BE_L0');
 const r=await G.makeRecord({...input,layer:'L0',state:'ACTIVE',previousRevisionId:null,inputs:[],history:await M.appendEvent([],{id:'csoi-create:'+input.id,type:'ADD',objectId:input.id,actor:'local-researcher',reason:'Register public/synthetic source identity; protected originals stay in their authoritative environment',observedAt:input.observedAt})});
 G.assertPublic(r,{operation:'STORAGE'});return r;
}
function inputRefs(records){return records.map(r=>({id:r.id,revisionId:r.revisionId}));}
async function transform(records,{id,targetLayer,data,judgment='EVIDENCE_INFERENCE',responsibleRole,reason,observedAt,asOf=null}){
 need(typeof id==='string'&&typeof reason==='string'&&reason.trim()&&['RESEARCH_OPERATOR','SYNTHETIC_REVIEWER'].includes(responsibleRole),'TRANSFORMATION_RESPONSIBILITY_REQUIRED');
 need(G.LAYERS.includes(targetLayer)&&targetLayer!=='L0','TARGET_LAYER');
 const level=G.LAYERS.indexOf(targetLayer);need(Array.isArray(records)&&records.length&&records.every(r=>G.LAYERS.indexOf(r.layer)===level-1),'SEQUENTIAL_LAYER_REQUIRED');
 const report=await validate(records,{asOf});need(report.passed,'TRANSFORMATION_QUALITY:'+report.reasons.join(','));
 need(records.every(r=>r.security===records[0].security),'SECURITY_CLASSIFICATION_MISMATCH');
 const method=[null,METHODS.NORMALIZE,METHODS.STATEMENT,METHODS.CALCULATE,METHODS.AGGREGATE,METHODS.RELEASE][level];
 const inherited=records[0],history=await M.appendEvent(inherited.history,{id:'csoi-transform:'+id,type:'ADD',objectId:id,actor:'local-researcher',reason,observedAt});
 const synthetic=records.every(r=>r.sourceClass==='SYNTHETIC');
 const r=await G.makeRecord({id,ownerModule:'CSOI_OPERATIONS',layer:targetLayer,security:inherited.security,sourceClass:synthetic?'SYNTHETIC':'INDEPENDENT_RESEARCH',judgment,authority:'INDEPENDENT_RESEARCH',scope:structuredClone(inherited.scope),inputs:inputRefs(records),data:{...data,methodVersion:method,responsibleRole,quality:report},sensitivity:structuredClone(inherited.sensitivity),provenance:{contentMode:synthetic?'SYNTHETIC':'RESEARCH_SUMMARY',rights:{mode:synthetic?'SYNTHETIC_OWNED':'PERMITTED_REUSE',basis:synthetic?'Repository-authored synthetic transformation':'Original independent research transformation; original source text is not redistributed'}},state:'ACTIVE',previousRevisionId:null,history,observedAt});
 G.assertPublic(r,{operation:'STORAGE'});return r;
}
async function normalize(record,{id,identities,measurement=null,reason='Normalize abstract object identities without merging different activities',observedAt=record.observedAt}){
 need(Array.isArray(identities)&&identities.length>0&&identities.length<=10000,'IDENTITIES_REQUIRED');
 const normalized=identities.map(normalizeIdentity);need(new Set(normalized.map(i=>i.id)).size===normalized.length,'DUPLICATE_IDENTITY');
 const data={identities:normalized,historicalIdentityPolicy:'Validity intervals remain attached; property, activity, premises, connection and device identities are distinct',measurement:measurement||record.data.measurement||null,sourceConflicts:record.data.sourceConflicts||[]};
 return transform([record],{id,targetLayer:'L1',data,judgment:'OBSERVATION',responsibleRole:'RESEARCH_OPERATOR',reason,observedAt});
}
async function statement(record,{id,judgment='EVIDENCE_INFERENCE',text,counterevidence=[],unknowns=[],rule=null,reason='Separate observation, rule, inference and human discretion',observedAt=record.observedAt}){
 need(['RULE','OBSERVATION','EVIDENCE_INFERENCE','DISCRETION','UNKNOWN'].includes(judgment)&&typeof text==='string'&&text.length>0&&text.length<=5000,'STATEMENT_REQUIRED');
 need(Array.isArray(counterevidence)&&Array.isArray(unknowns),'STATEMENT_CHALLENGES_REQUIRED');
 if(judgment==='RULE')need(rule&&rule.sourceId&&rule.sourceRevision&&rule.locator&&rule.legalRole&&rule.applicability,'RULE_SOURCE_AND_APPLICABILITY_REQUIRED');
 const data={judgment,text,counterevidence,unknowns,rule,identities:record.data.identities,measurement:record.data.measurement,sourceConflicts:record.data.sourceConflicts||[],officialDecision:false};
 return transform([record],{id,targetLayer:'L2',data,judgment,responsibleRole:'SYNTHETIC_REVIEWER',reason,observedAt});
}
function calculate(records,request){
 need(request&&['COVERAGE','SUM_WORK_HOURS','UNIT_CONVERSION'].includes(request.formula),'LAYER_FORMULA_UNKNOWN');
 const ms=records.map(r=>r.data.measurement);need(ms.every(m=>m&&typeof m.value==='number'&&Number.isFinite(m.value)&&m.value>=0&&typeof m.unit==='string'),'MEASUREMENT_UNKNOWN');
 const common=ms[0];for(const m of ms)for(const key of ['period','area','boundary'])need(same(common[key]??null,m[key]??null)&&m[key]!==undefined,'MEASUREMENT_SCOPE_MISMATCH:'+key);
 let result,denominator=null,numerator=null,eligibleIds=[];
 if(request.formula==='COVERAGE'){
  need(records.length===2&&ms.every(m=>m.unit==='count'),'COUNT_INPUTS_REQUIRED');
  const [n,d]=ms;need(n.meaning==='INSPECTED_ELIGIBLE'&&d.meaning==='ELIGIBLE_DUE','DENOMINATOR_MEANING_REQUIRED');
  need(Array.isArray(n.objectIds)&&Array.isArray(d.objectIds)&&new Set(n.objectIds).size===n.objectIds.length&&new Set(d.objectIds).size===d.objectIds.length&&n.value===n.objectIds.length&&d.value===d.objectIds.length,'DENOMINATOR_IDENTITIES_REQUIRED');
  need(d.value>0&&n.value<=d.value&&n.objectIds.every(id=>d.objectIds.includes(id)),'DENOMINATOR_INVALID');
  need(records[0].id!==records[1].id,'DUPLICATE_INPUT_RECORD');numerator=n.value;denominator=d.value;eligibleIds=[...d.objectIds];result={value:n.value/d.value,unit:'ratio',meaning:'WORK_COVERAGE_NOT_COMPLIANCE',numerator,denominator};
 }else if(request.formula==='SUM_WORK_HOURS'){
  need(ms.every(m=>m.unit==='h'&&['ESTIMATE','OBSERVED_SYNTHETIC'].includes(m.basis)&&m.workEventId),'WORK_HOUR_BASIS_REQUIRED');
  need(new Set(ms.map(m=>m.workEventId)).size===ms.length,'DOUBLE_COUNTED_WORK_EVENT');
  result={value:ms.reduce((sum,m)=>sum+m.value,0),unit:'h',meaning:'WORKLOAD_NOT_FINANCIAL_EXPENDITURE',basis:ms.every(m=>m.basis==='OBSERVED_SYNTHETIC')?'OBSERVED_SYNTHETIC':'ESTIMATE'};
 }else{need(ms.length===1&&typeof request.outputUnit==='string','CONVERSION_INPUT_REQUIRED');result={value:A.unitConvert(common.value,common.unit,request.outputUnit),unit:request.outputUnit,meaning:'UNIT_CONVERSION_ONLY'};}
 return {result:{...result,period:common.period,area:common.area,boundary:common.boundary,actualCompliance:'UNKNOWN',environmentalOutcome:'UNKNOWN',causalAttribution:'UNKNOWN'},numerator,denominator,eligibleIds};
}
async function quantify(records,{id,request,observedAt=records[0]?.observedAt}){
 const calculated=calculate(records,request),payload={format:'csoi-calculation-receipt-1',formulaVersion:METHODS.CALCULATE,request:structuredClone(request),inputs:inputRefs(records),...calculated,trust:'SELF_ATTESTED',externalWitness:'EXTERNAL_WITNESS_UNKNOWN'};
 const receipt={...payload,digest:await M.objectDigest(payload)};
 return transform(records,{id,targetLayer:'L3',data:{receipt,measurement:calculated.result,eligibleIds:calculated.eligibleIds},responsibleRole:'RESEARCH_OPERATOR',reason:'Reproducible quantity calculation with exact input versions, units and denominators',observedAt});
}
async function aggregate(records,{id,observedAt=records[0]?.observedAt}){
 need(records.every(r=>r.data.receipt?.request?.formula==='COVERAGE'),'MANAGEMENT_COVERAGE_INPUTS_REQUIRED');
 const allIds=records.flatMap(r=>r.data.eligibleIds||[]);need(new Set(allIds).size===allIds.length,'OVERLAPPING_STATISTICAL_DENOMINATORS');
 let numerator=0,denominator=0;
 for(const r of records){const receipt=r.data.receipt;need(receipt.result.unit==='ratio'&&Number.isInteger(receipt.numerator)&&Number.isInteger(receipt.denominator)&&receipt.denominator>0,'MANAGEMENT_DENOMINATOR_REQUIRED');const {digest,...payload}=receipt;need(await M.objectDigest(payload)===digest,'CALCULATION_RECEIPT_INVALID');numerator+=receipt.numerator;denominator+=receipt.denominator;}
 need(denominator>=5,'SMALL_CELL_SUPPRESSED');
 const data={title:'Management work coverage — independent synthetic/research view',measurement:{value:numerator/denominator,unit:'ratio',numerator,denominator,meaning:'WORK_COVERAGE_NOT_COMPLIANCE',area:records[0].scope.region,boundary:records[0].scope.boundary,period:records[0].scope.period},eligibleIds:allIds,qualityDefinition:'Inspected eligible objects / defined eligible-due objects; unchecked is UNKNOWN, never compliant',actualCompliance:'UNKNOWN',riskElimination:'UNKNOWN',outcome:'UNKNOWN',privacyReview:'REVIEW_REQUIRED'};
 return transform(records,{id,targetLayer:'L4',data,responsibleRole:'SYNTHETIC_REVIEWER',reason:'Management summary with disjoint eligible identities and explicit numerator/denominator',observedAt});
}
async function prepareRelease(record,{id,alignmentId=null,observedAt=record.observedAt}){
 const r=await transform([record],{id,targetLayer:'L5',data:{title:'Draft research sharing review',summary:record.data.measurement,sourceLayerId:record.id,reviewState:'REVIEW_PENDING',draftOnly:true,officialReport:false,strategicAlignment:alignmentId?{candidateId:alignmentId,status:'RESEARCH_CANDIDATE_NOT_OFFICIAL'}:'UNKNOWN',reviewQueue:['Check source/rights and current versions','Review aggregate reidentification and complementary disclosure','Independently authorise any real release in its authoritative environment'],actualCompliance:'UNKNOWN'},responsibleRole:'SYNTHETIC_REVIEWER',reason:'Create pending sharing review; analytical layer does not upgrade security classification',observedAt});
 return r;
}
async function verifyHistory(record){return G.verifyRecord(record).then(async ok=>ok&&STATES.has(record.state)&&Array.isArray(record.history)&&await M.verifyEvents(record.history)&&record.history.at(-1)?.objectId===record.id);}
async function verifyDerivation(d,record){
 try{
  if(record.layer!=='L3'||!await verifyHistory(record))return {integrity:false};
  const receipt=record.data.receipt,{digest,...payload}=receipt;
  if(await M.objectDigest(payload)!==digest||receipt.formulaVersion!==METHODS.CALCULATE||!same(receipt.inputs,record.inputs))return {integrity:false};
  const inputs=record.inputs.map(ref=>d.domain.revisions.map(r=>r.record.data?.csoiRecord).find(r=>r?.id===ref.id&&r.revisionId===ref.revisionId));
  if(inputs.some(r=>!r))return {integrity:false};
  for(const input of inputs)if(!await verifyHistory(input))return {integrity:false};
  const computed=calculate(inputs,receipt.request);
  if(!['result','numerator','denominator','eligibleIds'].every(key=>same(receipt[key],computed[key]))||!same(record.data.measurement,computed.result))return {integrity:false};
  return {integrity:true,trust:'SELF_ATTESTED',officialAdmission:'UNKNOWN'};
 }catch{return {integrity:false};}
}
async function verifyCurrent(d,record,{limit=10000}={}){
 if(!Number.isInteger(limit)||limit<1||limit>100000)throw Error('LINEAGE_BOUNDS');
 const reasons=new Set(),queue=[record],seen=new Set();let i=0;
 for(;i<queue.length&&i<limit;i++){
  const r=queue[i],key=r.id+'@'+r.revisionId;if(seen.has(key))continue;seen.add(key);
  if(!await verifyHistory(r)){reasons.add('RECORD_HISTORY_INVALID');continue;}
  if(r.layer==='L3'&&!(await verifyDerivation(d,r)).integrity)reasons.add('CALCULATION_RECOMPUTATION_FAILED');
  if(r.state!=='ACTIVE')reasons.add('WITHDRAWN_INPUT');
  for(const ref of r.inputs){const current=find(d,ref.id);if(!current){reasons.add('INPUT_NOT_REGISTERED');continue;}if(current.revisionId!==ref.revisionId)reasons.add('INPUT_VERSION_CHANGED');queue.push(current);}
 }
 if(i<queue.length)reasons.add('LINEAGE_TRUNCATED');
 return {current:reasons.size===0,status:reasons.size?'INVALIDATED':'CURRENT_SELF_ATTESTED',reasons:[...reasons].sort(),visited:seen.size,officialAdmission:'UNKNOWN'};
}
function registrationPayload(record,{stationId='water',reason='Register public/synthetic L0–L5 research object in existing AtlasModel'}={}){
 G.assertPublic(record,{operation:'STORAGE'});return {id:record.id,kind:'ContentBlock',stationId,label:record.data.title||record.data.text?.slice(0,100)||record.layer+' research record',scope:{region:record.scope.region,period:record.scope.period,boundary:record.scope.boundary},data:{status:'SYNTHETIC',transport:'PUBLIC_OR_SYNTHETIC_RESEARCH_CONTRACT',csoiRecord:record},reason};
}
async function register(d,record,options={}){
 need(await verifyHistory(record),'CSOI_RECORD_HISTORY');G.assertPublic(record,{operation:'STORAGE'});
 for(const ref of record.inputs){const current=find(d,ref.id);need(current&&current.revisionId===ref.revisionId&&current.state==='ACTIVE','CURRENT_INPUTS_REQUIRED');}
 const existing=M.domainIndex(d).get(record.id),payload=registrationPayload(record,options);
 if(!existing)return typeof M.registerResearchRecord==='function'?M.registerResearchRecord(d,{record,kind:payload.kind,label:payload.label,stationId:payload.stationId,reason:payload.reason}):M.registerScenario(d,payload);
 const previous=existing.data?.csoiRecord||existing.data?.csoi;need(previous&&record.previousRevisionId===previous.revisionId&&record.history.length===previous.history.length+1&&previous.history.every((e,i)=>e.digest===record.history[i].digest),'LAYER_REVISION_LINEAGE');
 return typeof M.reviseResearchRecord==='function'?M.reviseResearchRecord(d,{id:record.id,expectedRevisionId:existing.revisionId,record,reason:options.reason||'Append classified research-layer revision'}):M.commitDomainRevision(d,{id:record.id,expectedRevisionId:existing.revisionId,patch:{data:payload.data,label:payload.label},reason:options.reason||'Append classified research-layer revision'});
}
async function revise(record,{data=record.data,state='ACTIVE',reason,observedAt}){
 need(await verifyHistory(record)&&typeof reason==='string'&&reason.trim()&&STATES.has(state),'REVISION_REQUIRED');
 need(state==='WITHDRAWN'||record.layer==='L0','DERIVED_RECORD_REQUIRES_RECALCULATION');
 const {revisionId,...old}=record,history=await M.appendEvent(record.history,{id:'csoi-revision:'+record.id+':'+record.history.length,type:state==='WITHDRAWN'?'RETRACT':'SUPERSEDE',objectId:record.id,actor:'local-researcher',reason,observedAt});
 const next=await G.makeRecord({...old,data:structuredClone(data),state,previousRevisionId:revisionId,history,observedAt});G.assertPublic(next,{operation:'STORAGE'});return next;
}
async function replay(d,id,domainRevisionId){
 const r=d.domain?.revisions.find(r=>r.id===domainRevisionId&&r.logicalId===id)?.record?.data?.csoiRecord||d.domain?.revisions.find(r=>r.id===domainRevisionId&&r.logicalId===id)?.record?.data?.csoi;
 need(r&&await verifyHistory(r),'HISTORICAL_LAYER_REVISION_NOT_FOUND');return structuredClone(r);
}
async function demo(d){
 let result=d;const records=[];
 const scope={region:'SYNTHETIC_PLACE',boundary:'SYNTHETIC_REGULATORY_SERVICE',period:{from:'2026-07-01',to:'2027-06-30'}},ids=Array.from({length:10},(_,i)=>'DEMO-OBJECT-'+(i+1));
 const make=async(role,objects)=>{
  const s=await source({id:'csoi:demo:'+role+':source',ownerModule:'CSOI_OPERATIONS',security:'PUBLIC',sourceClass:'SYNTHETIC',judgment:'OBSERVATION',authority:'INDEPENDENT_RESEARCH',scope,inputs:[],data:{title:'Synthetic '+role+' object list',measurement:{value:objects.length,unit:'count',meaning:role==='inspected'?'INSPECTED_ELIGIBLE':'ELIGIBLE_DUE',objectIds:objects,period:scope.period,area:scope.region,boundary:scope.boundary}},sensitivity:{personalData:false,confidential:false,reidentifiable:false},provenance:{contentMode:'SYNTHETIC',rights:{mode:'SYNTHETIC_OWNED',basis:'Repository-authored synthetic capacity fixture; no real customers or work records'}},observedAt:'2026-10-30T00:00:00.000Z'});
  const n=await normalize(s,{id:'csoi:demo:'+role+':normalized',identities:objects.map(id=>({id,type:'WORK_EVENT',namespace:role.toUpperCase(),validFrom:scope.period.from,validTo:scope.period.to}))});
  const e=await statement(n,{id:'csoi:demo:'+role+':evidence',judgment:'OBSERVATION',text:'Synthetic count only. Uninspected objects have UNKNOWN compliance, not a pass.',unknowns:['Real eligible population and local operational allocation UNKNOWN']});
  for(const r of [s,n,e]){result=await register(result,r);records.push(r);}return e;
 };
 const n=await make('inspected',ids.slice(0,6)),eligible=await make('eligible',ids);
 const q=await quantify([n,eligible],{id:'csoi:demo:work-coverage',request:{formula:'COVERAGE'}});result=await register(result,q);records.push(q);
 const management=await aggregate([q],{id:'csoi:demo:management'});result=await register(result,management);records.push(management);
 const release=await prepareRelease(management,{id:'csoi:demo:sharing-review'});result=await register(result,release);records.push(release);
 return {dataset:result,records,summary:{software:'L0–L5 synthetic lineage',workCoverage:'6 / 10 = 0.6',compliance:'UNKNOWN',officialAdmission:'UNKNOWN',release:'REVIEW_PENDING'}};
}
const api={METHODS,IDENTITY_TYPES,normalizeIdentity,quality,validate,source,transform,normalize,statement,calculate,quantify,aggregate,prepareRelease,verifyHistory,verifyDerivation,verifyCurrent,registrationPayload,register,revise,replay,currentRecords,find,demo};root.AtlasCSOILayers=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
