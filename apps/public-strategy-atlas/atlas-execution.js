/* Queries operate on AtlasModel identities; synthetic execution is never Council progress. */
(function(root){
'use strict';
const M=typeof module!=='undefined'?require('./atlas-model.js'):root.AtlasModel;
function assertions(d){return [...d.assertions,...(d.domain?.assertions||[])];}
function shortestPath(d,from,to,{direction='forward',mode='DISCOVERY_CANDIDATE',maxVisited=10000}={}){
 if(!['forward','reverse','both'].includes(direction)||!['KNOWN_LINK','DISCOVERY_CANDIDATE'].includes(mode)||!Number.isInteger(maxVisited)||maxVisited<1||maxVisited>100000)throw Error('QUERY_BOUNDS');
 const entities=M.domainIndex(d);if(!entities.has(from)||!entities.has(to))throw Error('QUERY_ENDPOINT');
 const edges=assertions(d).filter(a=>!['CONTRADICTED','SUPERSEDED','RETRACTED','CONTESTED'].includes(a.status||a.state));
 // No authority verifier is configured; local claims cannot create KNOWN_LINK.
 if(mode==='KNOWN_LINK')return {status:'UNKNOWN',path:[],nodeIds:[],reason:'No officially admitted authority-backed relationships are configured.',truncated:false};
 const adjacency=new Map();
 function add(a,b,id){if(!adjacency.has(a))adjacency.set(a,[]);adjacency.get(a).push({to:b,id});}
 for(const a of edges){if(direction!=='reverse')add(a.from,a.to,a.id);if(direction!=='forward')add(a.to,a.from,a.id);}
 const queue=[from],seen=new Set([from]),previous=new Map();let found=from===to,i=0;
 while(i<queue.length&&!found&&i<maxVisited){const current=queue[i++];for(const edge of adjacency.get(current)||[]){if(seen.has(edge.to))continue;seen.add(edge.to);previous.set(edge.to,{node:current,edge:edge.id});queue.push(edge.to);if(edge.to===to){found=true;break;}}}
 if(!found)return {status:'UNKNOWN',path:[],nodeIds:[],reason:'No eligible bounded path; context or missing relationships may prevent traversal.',truncated:i>=maxVisited};
 const path=[],nodeIds=[to];let cursor=to;while(cursor!==from){const p=previous.get(cursor);path.push(p.edge);nodeIds.push(p.node);cursor=p.node;}
 return {status:'DISCOVERY_CANDIDATE',path:path.reverse(),nodeIds:nodeIds.reverse(),reason:'Model path only. Synthetic/research links do not establish causation, statutory authority or official implementation.',truncated:false};
}
function workBreakdown(d,stationId,{limit=200}={}){
 if(!Number.isInteger(limit)||limit<1||limit>1000)throw Error('WBS_BOUNDS');
 const entities=M.domainIndex(d);if(!entities.has(stationId))throw Error('WBS_STATION');
 const queue=[{id:stationId,depth:0}],seen=new Set(),rows=[],relations=assertions(d).filter(a=>['HAS_ACTIVITY','RESOURCED_BY','FUNDED_BY','REPORTS_OUTPUT','MEASURED_BY','HAS_DEPENDENCY'].includes(a.predicate));
 for(let i=0;i<queue.length&&rows.length<limit;i++){const row=queue[i];if(seen.has(row.id))continue;seen.add(row.id);const entity=entities.get(row.id);rows.push({...row,entity,executionState:entity?.state||'UNKNOWN',evidenceState:entity?.admission||'UNKNOWN'});for(const a of relations.filter(a=>a.from===row.id)){queue.push({id:a.to,depth:row.depth+1,via:a.id});}}
 const included=new Set(rows.map(r=>r.id));
 const dependencies=relations.filter(a=>a.predicate==='HAS_DEPENDENCY'&&included.has(a.from));
 const pending=new Map(rows.map(r=>[r.id,dependencies.filter(a=>a.from===r.id).map(a=>a.to)])),order=[],ready=[...pending].filter(([,deps])=>!deps.length).map(([id])=>id);
 for(let i=0;i<ready.length;i++){const id=ready[i];if(order.includes(id))continue;order.push(id);for(const [target,deps] of pending){const next=deps.filter(dep=>dep!==id);if(next.length!==deps.length){pending.set(target,next);if(!next.length)ready.push(target);}}}
 return {stationId,rows,dependencies,dependencyOrder:order,dependencyCycle:order.length<rows.length,truncated:queue.some(r=>!seen.has(r.id)),execution:'RESEARCH_ONLY',evidence:'OFFICIAL_IMPLEMENTATION_UNKNOWN',gaps:['Public work ownership, approvals and outputs remain unverified.','Synthetic work states are not Council workflow approvals.']};
}
const A=typeof module!=='undefined'?require('./atlas-accounting.js'):root.AtlasAccounting;
function need(ok,code){if(!ok)throw Error(code);}
function comparableScope(a,b){for(const key of ['area','boundary','period','currencyBasis','costClass','lineId'])need(M.canonical(a[key]??null)===M.canonical(b[key]??null),'SCOPE_MISMATCH:'+key);}
function calculate(records,request){
 const data=records.map(r=>r.data),[a,b,c]=data,formula=request.formula;
 need(records.length>0&&records.every(r=>r.classification==='SYNTHETIC_SCENARIO'),'UNADMITTED_INPUTS');
 let result,ledger='PHYSICAL_ENVIRONMENTAL';
 if(formula==='UNIT_CONVERSION'){
  need(data.length===1,'INPUT_COUNT');need(typeof a.value==='number'&&Number.isFinite(a.value),'VALUE_UNKNOWN');
  if(a.unit==='ML'&&request.outputUnit==='ML/day'){
   const p=a.period,from=typeof p==='object'?p.from:null,to=typeof p==='object'?p.to:null;
   need(/^\d{4}-\d{2}-\d{2}$/.test(from)&&/^\d{4}-\d{2}-\d{2}$/.test(to)&&Number.isFinite(Date.parse(from))&&Number.isFinite(Date.parse(to)),'EXPLICIT_DURATION_REQUIRED');
   const days=(Date.parse(to)-Date.parse(from))/86400000+1;need(days>0&&days===request.durationDays,'DURATION_MISMATCH');result={value:a.value/days,unit:'ML/day'};
  }else result={value:A.unitConvert(a.value,a.unit,request.outputUnit),unit:request.outputUnit};
 }else if(formula==='COST_PER_OUTPUT'){
  need(data.length===2,'INPUT_COUNT');need(a.currencyBasis&&a.currencyBasis!=='UNKNOWN','CURRENCY_BASIS_UNKNOWN');result=A.costPerOutput(a,b);ledger='FINANCIAL_RESOURCE';
 }else if(formula==='BUDGET_VARIANCE'){
  need(data.length===2,'INPUT_COUNT');A.assertFinancial(a);A.assertFinancial(b);need(['APPROVED_BUDGET','REVISED_BUDGET'].includes(a.type)&&b.type==='ACTUAL_EXPENDITURE','BUDGET_ACTUAL_REQUIRED');comparableScope(a,b);need(a.currencyBasis&&a.currencyBasis!=='UNKNOWN'&&a.lineId&&a.costClass,'FINANCIAL_BASIS_UNKNOWN');result={value:b.value-a.value,unit:'AUD'};ledger='FINANCIAL_RESOURCE';
 }else if(formula==='PER_CAPITA_TOTAL'){
  need(data.length===2,'INPUT_COUNT');result=A.totalFromPerCapita(a,b);
 }else if(formula==='RESULT_COMPARISON'){
  need(data.length===3,'INPUT_COUNT');A.assertComparable(a,b);A.assertComparable(a,c);need([a.value,b.value,c.value].every(v=>typeof v==='number'&&Number.isFinite(v)),'RESULT_UNKNOWN');need(a.baseline===true&&b.target===true&&c.actual===true,'RESULT_ROLES_REQUIRED');need(b.value!==a.value,'ZERO_TARGET_INTERVAL');result={value:(c.value-a.value)/(b.value-a.value),unit:'ratio',causalAttribution:'UNKNOWN'};ledger='RESULTS_EVIDENCE';
 }else if(formula==='ALLOCATED_SUM'){
  need(new Set(records.map(r=>r.id)).size===records.length,'DUPLICATE_EXPENDITURE');for(const e of data)A.assertFinancial(e);
  need(data.every(e=>e.type==='ACTUAL_EXPENDITURE'),'ACTUAL_EXPENDITURE_REQUIRED');for(const e of data)comparableScope(data[0],e);
  need(Array.isArray(request.allocations)&&request.allocations.length>0&&request.goalId,'ALLOCATION_REQUIRED');
  let value=0;for(const r of records){const shares=request.allocations.filter(s=>s.inputId===r.id);need(shares.length&&shares.every(s=>Number.isFinite(s.share)&&s.share>=0&&s.share<=1&&typeof s.goalId==='string'),'ALLOCATION_REQUIRED');need(new Set(shares.map(s=>s.goalId)).size===shares.length,'DUPLICATE_ALLOCATION');need(Math.abs(shares.reduce((v,s)=>v+s.share,0)-1)<1e-9,'DOUBLE_COUNT_OR_UNALLOCATED');value+=r.data.value*shares.filter(s=>s.goalId===request.goalId).reduce((v,s)=>v+s.share,0);}
  need(request.allocations.every(s=>records.some(r=>r.id===s.inputId)),'ALLOCATION_INPUT');result={value,unit:'AUD'};ledger='FINANCIAL_RESOURCE';
 }else if(formula==='EMISSIONS_FACTOR'){
  need(data.length===2,'INPUT_COUNT');need(a.unit==='MWh'&&b.unit==='t_CO2e/MWh','EMISSIONS_UNITS');need(b.factorVersion&&b.source?.url&&b.source?.locator&&a.sector===b.sector&&a.inventoryScope===b.inventoryScope,'FACTOR_SOURCE_OR_SCOPE_UNKNOWN');for(const key of ['period','area','boundary'])need(M.canonical(a[key])===M.canonical(b[key]),'FACTOR_SCOPE_MISMATCH');need(Number.isFinite(a.value)&&Number.isFinite(b.value),'VALUE_UNKNOWN');result={value:a.value*b.value,unit:'t_CO2e'};
 }else throw Error('FORMULA_UNSUPPORTED');
 need(Number.isFinite(result.value),'NON_FINITE_RESULT');return {...result,status:'SYNTHETIC_SCENARIO',ledger,quality:'RESEARCH_FIXTURE',uncertainty:'Not real Council evidence; input uncertainties remain',causalAttribution:'UNKNOWN'};
}
async function derive(d,request){
 need(request&&Array.isArray(request.inputIds)&&request.inputIds.length>0&&request.inputIds.length<=100,'INPUTS_REQUIRED');
 const index=M.domainIndex(d),records=request.inputIds.map(id=>index.get(id));need(records.every(r=>r&&r.revisionId),'INPUT_NOT_FOUND');
 for(const record of records){const revision=d.domain.revisions.find(r=>r.id===record.revisionId),{revisionId,...payload}=record;need(revision&&M.canonical(payload)===M.canonical(revision.record),'INPUT_REVISION_MISMATCH');const {id,...revisionPayload}=revision;need(await M.objectDigest(revisionPayload)===id,'INPUT_REVISION_DIGEST');}
 const payload={format:'atlas-derivation-1',methodVersion:'atlas-ledger-1',request:structuredClone(request),inputs:records.map(r=>({id:r.id,revisionId:r.revisionId,provenance:r.provenance})),result:calculate(records,request),trust:'SELF_ATTESTED',externalWitness:'EXTERNAL_WITNESS_UNKNOWN'};
 return {...payload,digest:await M.objectDigest(payload)};
}
async function verifyDerivation(d,receipt){
 try{
  const {digest,...payload}=receipt;if(receipt.format!=='atlas-derivation-1'||receipt.methodVersion!=='atlas-ledger-1'||await M.objectDigest(payload)!==digest)return {integrity:false,current:false,status:'CORRUPT_DERIVATION'};
  const revisions=new Map(d.domain.revisions.map(r=>[r.id,r])),records=[];
  for(const input of receipt.inputs){const r=revisions.get(input.revisionId);if(r){const {id,...p}=r;if(await M.objectDigest(p)!==id)return {integrity:false,current:false,status:'INPUT_REVISION_DIGEST'};}if(!r||r.logicalId!==input.id||M.canonical(r.record.provenance)!==M.canonical(input.provenance))return {integrity:false,current:false,status:'INPUT_HISTORY_MISSING'};records.push({...r.record,revisionId:r.id});}
  if(M.canonical(records.map(r=>r.id))!==M.canonical(receipt.request.inputIds)||M.canonical(calculate(records,receipt.request))!==M.canonical(receipt.result))return {integrity:false,current:false,status:'RESULT_MISMATCH'};
  const index=M.domainIndex(d),current=receipt.inputs.every(input=>index.get(input.id)?.revisionId===input.revisionId);
  return {integrity:true,current,status:current?'CURRENT_INPUTS':'INVALIDATED_INPUT_REVISION'};
 }catch{return {integrity:false,current:false,status:'INVALID_DERIVATION'};}
}
const api={derive,verifyDerivation,calculate,assertions,shortestPath,workBreakdown};root.AtlasExecution=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
