/* Queries operate on AtlasModel identities; synthetic execution is never Council progress. */
(function(root){
'use strict';
const M=typeof module!=='undefined'?require('./atlas-model.js'):root.AtlasModel;
function assertions(d){return [...d.assertions,...(d.domain?.assertions||[])];}
function shortestPath(d,from,to,{direction='forward',mode='DISCOVERY_CANDIDATE',maxVisited=10000,context=null}={}){
 if(!['forward','reverse','both'].includes(direction)||!['KNOWN_LINK','DISCOVERY_CANDIDATE'].includes(mode)||!Number.isInteger(maxVisited)||maxVisited<1||maxVisited>100000)throw Error('QUERY_BOUNDS');
 const entities=M.domainIndex(d);if(!entities.has(from)||!entities.has(to))throw Error('QUERY_ENDPOINT');
 const edges=assertions(d).filter(a=>(!context||![a,entities.get(a.to)].filter(Boolean).some(r=>applicability(r,context).status.startsWith('REJECTED')))&&!['CONTRADICTED','SUPERSEDED','RETRACTED','CONTESTED'].includes(a.status||a.state));
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
function day(value){return typeof value==='string'&&/^\d{4}-\d{2}-\d{2}$/.test(value)&&Number.isFinite(Date.parse(value))&&new Date(value).toISOString().slice(0,10)===value;}
function timeRange(record){
 const data=record.data||{},scope=record.scope||{};
 let from=data.validFrom||data.period?.from||scope.period?.from||record.validFrom,to=data.validTo||data.period?.to||scope.period?.to||record.validTo;
 const fiscal=typeof data.period==='string'?/^FY(\d{4})-(\d{2})$/.exec(data.period):null;
 if(fiscal&&Number(fiscal[2])===(Number(fiscal[1])+1)%100){from=fiscal[1]+'-07-01';to=(Number(fiscal[1])+1)+'-06-30';}
 return day(from)&&day(to)&&from<=to?{from,to}:null;
}
function applicability(record,context){
 if(!record||!context||!day(context.date)||!context.region||context.region==='UNKNOWN')return {status:'UNKNOWN',reason:'Explicit valid date and region required.'};
 const data=record.data||{},region=data.area||record.scope?.region||record.region;
 if(!region||region==='UNKNOWN')return {status:'UNKNOWN',reason:'Source geography is unconfirmed.'};
 if(region!==context.region)return {status:'REJECTED_REGION',reason:'Jurisdiction/area differs; shared wording is insufficient.'};
 if(context.spatialType&&!(data.spatialType||record.scope?.spatialType))return {status:'UNKNOWN',reason:'Spatial grain is not established.'};
 if(context.spatialType&&context.spatialType!==(data.spatialType||record.scope?.spatialType))return {status:'REJECTED_SPATIAL_GRAIN',reason:'Administrative/service/parcel scopes are not interchangeable.'};
 const interval=timeRange(record);if(!interval)return {status:'UNKNOWN',reason:'Effective interval is not established. A planning horizon is not an effective date.'};
 if(context.date<interval.from||context.date>interval.to)return {status:'REJECTED_TIME',reason:'Selected date lies outside this effective interval.'};
 if(data.legalState==='DRAFT')return {status:'REJECTED_DRAFT',reason:'A draft is not an adopted control.'};
 if(data.supersededAt&&(!day(data.supersededAt)||context.date>=data.supersededAt))return {status:'REJECTED_SUPERSEDED',reason:'Selected source revision has been superseded at this date.'};
 if(context.soughtEffect&&!data.legalRole)return {status:'UNKNOWN',reason:'Legal role is not established.'};
 if(context.soughtEffect&&data.legalRole!==context.soughtEffect)return {status:'REJECTED_LEGAL_EFFECT',reason:'LEP statutory control, DCP guidance and strategic policy have different legal roles.'};
 if(context.sourceRevision&&context.sourceRevision!==(data.sourceRevision||record.revisionId))return {status:'REJECTED_REVISION',reason:'The requested document revision does not match.'};
 if(record.kind==='StatutoryControl'&&data.legalState!=='ADOPTED')return {status:'UNKNOWN',reason:'Adoption/effectiveness not verified.'};
 if(record.classification==='SYNTHETIC_SCENARIO')return {status:'SYNTHETIC_ONLY',reason:'Compatible fixture scope only; no real legal applicability.'};
 return {status:'REQUIRES_REVIEW',reason:'Matching metadata does not establish legal applicability or authorised admission.'};
}
function scopeIndex(d){
 const regions=new Map();for(const r of d.domain?.entities||[]){const area=r.data?.area||r.scope?.region||'UNKNOWN';if(!regions.has(area))regions.set(area,[]);regions.get(area).push({id:r.id,revisionId:r.revisionId,kind:r.kind,interval:timeRange(r)});}return regions;
}
function asOf(d,context){
 const matched=new Map(),rejected=[];
 for(const revision of d.domain?.revisions||[]){if(!revision.record.kind||context.kind&&revision.record.kind!==context.kind)continue;const r={...revision.record,revisionId:revision.id},result=applicability(r,context);if(!['SYNTHETIC_ONLY','REQUIRES_REVIEW'].includes(result.status)){rejected.push({id:r.id,revisionId:r.revisionId,...result});continue;}if(!matched.has(r.id))matched.set(r.id,new Map());matched.get(r.id).set(r.data.sourceRevision||'LOCAL',r);}
 const records=[],conflicts=[];for(const [id,versions] of matched){if(versions.size>1)conflicts.push({id,status:'CONFLICTING_SOURCE_REVISIONS',revisionIds:[...versions.values()].map(v=>v.revisionId)});else records.push([...versions.values()][0]);}
 return {records,conflicts,rejected,officialApplicability:'UNKNOWN'};
}
function candidateSignals(from,to){
 const a=from.data||{},b=to.data||{},signals=[];
 if((a.crossReferences||[]).includes(to.id)||(b.crossReferences||[]).includes(from.id))signals.push('EXPLICIT_REFERENCE');
 if(a.projectCode&&a.projectCode===b.projectCode)signals.push('SHARED_PROJECT_CODE');
 if(a.area&&a.area!=='UNKNOWN'&&a.area===b.area)signals.push('SHARED_AREA');
 if(a.unit&&a.unit===b.unit)signals.push('SHARED_UNIT');
 const vocab=(a.vocabulary||[]).filter(word=>(b.vocabulary||[]).includes(word));if(vocab.length)signals.push('CONTROLLED_VOCABULARY:'+vocab.join(','));
 const stop=new Set(['synthetic','the','and','for','not','unknown','scenario','research','council','source']);
 const tokens=text=>new Set(String(text).toLowerCase().match(/[a-z]{4,}/g)?.filter(w=>!stop.has(w))||[]);
 const left=tokens(from.label||from.title),right=tokens(to.label||to.title);if([...left].some(w=>right.has(w)))signals.push('WORDING_OVERLAP_WEAK');
 return signals;
}
async function candidates(d,fromId,{context=null,limit=20,maxVisited=10000}={}){
 need(Number.isInteger(limit)&&limit>0&&limit<=100&&Number.isInteger(maxVisited)&&maxVisited>0&&maxVisited<=100000,'DISCOVERY_BOUNDS');
 const index=M.domainIndex(d),from=index.get(fromId);need(from,'DISCOVERY_ENDPOINT');const out=[];let visited=0;
 for(const to of index.values()){
  if(visited++>=maxVisited||out.length>=limit)break;if(to.id===fromId)continue;const signals=candidateSignals(from,to);if(!signals.length)continue;
  const a=from.data||{},b=to.data||{},reasons=[];
  if(a.area&&b.area&&a.area!=='UNKNOWN'&&b.area!=='UNKNOWN'&&a.area!==b.area)reasons.push('REJECTED_REGION');
  if(a.period&&b.period&&M.canonical(a.period)!==M.canonical(b.period))reasons.push('REJECTED_PERIOD');
  if(a.unit&&b.unit&&a.unit!==b.unit&&['QuantifiedObservation','MetricDefinition'].includes(from.kind)&&['QuantifiedObservation','MetricDefinition'].includes(to.kind))reasons.push('REJECTED_UNIT_MEANING');
  if(b.sourceLost||b.sourceStatus==='LOST')reasons.push('REJECTED_SOURCE_LOST');
  if(b.conflictingSourceRevisions?.length)reasons.push('REJECTED_SOURCE_REVISION_CONFLICT');
  if(context)for(const r of [from,to]){const result=applicability(r,context);if(result.status.startsWith('REJECTED'))reasons.push(result.status);}
  const path=shortestPath(d,fromId,to.id,{direction:'both',context});
  const payload={format:'atlas-discovery-candidate-1',ruleVersion:'atlas-scope-signals-1',from:fromId,to:to.id,fromRevisionId:from.versionId||from.revisionId,toRevisionId:to.versionId||to.revisionId,context,signals,status:reasons.length?'REJECTED_CANDIDATE':'DISCOVERY_CANDIDATE',rejectionReasons:[...new Set(reasons)],sourcePaths:path.path,sourceNodeIds:path.nodeIds,rationale:'Signals identify a research question, not an official implementation, legal or causal relationship.',alternativeExplanation:'Shared terminology, accounting units or administrative context can occur without any direct policy or delivery link.',falsifier:'Reject or contest if official anchors do not explicitly support this relation, or region/effective period/legal role/units/accounting basis conflict.',counterevidence:[...(to.gaps||[]),...reasons],reviewState:'PENDING',knownLink:'UNKNOWN',trust:'SELF_ATTESTED'};
  out.push({...payload,digest:await M.objectDigest(payload)});
 }
 return out;
}
async function verifyCandidate(d,candidate){
 try{
  const {digest,...payload}=candidate;if(candidate.format!=='atlas-discovery-candidate-1'||candidate.ruleVersion!=='atlas-scope-signals-1'||!['REJECTED_CANDIDATE','DISCOVERY_CANDIDATE'].includes(candidate.status)||candidate.knownLink!=='UNKNOWN'||candidate.reviewState!=='PENDING'||await M.objectDigest(payload)!==digest)return false;
  const index=M.domainIndex(d),revs=new Map((d.domain?.revisions||[]).map(r=>[r.id,r]));
  for(const [id,revision] of [[candidate.from,candidate.fromRevisionId],[candidate.to,candidate.toRevisionId]])if(index.get(id)?.versionId!==revision&&revs.get(revision)?.logicalId!==id)return false;
  return Array.isArray(candidate.signals)&&candidate.signals.length>0&&Array.isArray(candidate.sourcePaths)&&candidate.sourcePaths.every(id=>assertions(d).some(a=>a.id===id))&&typeof candidate.falsifier==='string'&&candidate.falsifier.length>0;
 }catch{return false;}
}
function searchRecords(d,query,{stationId=null,region=null,date=null,kind=null,classification=null,includeUnknownScope=false,offset=0,limit=12}={}){
 need(typeof query==='string'&&Number.isInteger(offset)&&offset>=0&&Number.isInteger(limit)&&limit>0&&limit<=100,'SEARCH_BOUNDS');
 const tokens=query.toLowerCase().replace(/_/g,' ').trim().split(/\s+/).filter(Boolean),results=[];
 const rows=[...d.nodes.map(record=>({category:'station',record})),...d.contentItems.map(record=>({category:'content',record})),...(d.domain?.entities||[]).map(record=>({category:'entity',record})),...(d.domain?.sourceCatalogue?.sources||[]).map(record=>({category:'source',record:{...record,kind:'SourceArtifact',label:record.title}}))];
 for(const row of rows){const r=row.record,area=r.data?.area||r.scope?.region||r.geographicExtent?.label||null,owner=r.stationId||r.ownerNodeId||(row.category==='station'?r.id:null),status=r.classification||r.status||'UNKNOWN';
  if(stationId&&owner!==stationId||region&&area!==region||kind&&(r.kind||r.type)!==kind||classification&&status!==classification)continue;
  let applicabilityStatus='NOT_REQUESTED';if(date){const result=applicability(r,{date,region:region||area});applicabilityStatus=result.status;if(result.status.startsWith('REJECTED')||result.status==='UNKNOWN'&&!includeUnknownScope)continue;}
  const text=[r.id,r.label,r.title,r.text,r.localNote,r.kind,status,r.data?.value,r.data?.unit,r.provenance?.locator,r.officialUrl,r.directoryUrl,M.canonical(r.data||{}),M.canonical(r.scope||{}),r.family].filter(v=>v!==undefined).join(' ').toLowerCase().replace(/_/g,' ');
  if(tokens.every(token=>text.includes(token)))results.push({...row,stationId:owner,classification:status,applicability:applicabilityStatus});
 }
 return {total:results.length,items:results.slice(offset,offset+limit),offset,nextOffset:offset+limit<results.length?offset+limit:null};
}
function diffRecords(before,after){return [...new Set([...Object.keys(before||{}),...Object.keys(after||{})])].sort().filter(field=>M.canonical(before?.[field]??null)!==M.canonical(after?.[field]??null)).map(field=>({field,before:before?.[field]??null,after:after?.[field]??null}));}
const api={searchRecords,diffRecords,candidates,verifyCandidate,candidateSignals,timeRange,applicability,scopeIndex,asOf,derive,verifyDerivation,calculate,assertions,shortestPath,workBreakdown};root.AtlasExecution=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
