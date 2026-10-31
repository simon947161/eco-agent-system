/* Immutable path proofs over existing assertions and governed input lineage. */
(function(root){'use strict';
const M=typeof module!=='undefined'?require('./atlas-model.js'):root.AtlasModel,E=typeof module!=='undefined'?require('./atlas-execution.js'):root.AtlasExecution,I=typeof module!=='undefined'?require('./atlas-intake.js'):root.AtlasIntake;
const METHOD='atlas-pinned-path-sets-1',badStates=new Set(['RETRACTED','CONTESTED','CONTRADICTED','SUPERSEDED']);
function need(ok,code){if(!ok)throw Error(code);}
function closed(o,keys){return o&&typeof o==='object'&&!Array.isArray(o)&&Object.keys(o).every(k=>keys.includes(k));}
const key=r=>r.id+'|'+(r.revisionId||'CURRENT');
function validate(spec){need(closed(spec,['nodes','relationships'])&&Array.isArray(spec.nodes)&&spec.nodes.length>0&&spec.nodes.length<=32&&Array.isArray(spec.relationships)&&spec.relationships.length===spec.nodes.length-1,'PATH_BOUNDS');for(const r of spec.relationships)need(['ASSERTION','INPUT'].includes(r.kind)&&closed(r,r.kind==='ASSERTION'?['kind','id','revisionId','direction']:['kind','ownerId','inputIndex','revisionId','direction'])&&['FORWARD','REVERSE',undefined].includes(r.direction),'PATH_RELATIONSHIP_FIELDS');}
// Evaluate all retained input dependencies, even when a displayed proof has a
// single node. This changes current-context assessment, never historical pins.
function assessDependencies(d,records,{maxVisited=10000}={}){
 need(Array.isArray(records)&&Number.isSafeInteger(maxVisited)&&maxVisited>0&&maxVisited<=100000,'PATH_DEPENDENCY_BOUNDS');
 const sources=new Map((d.domain?.sourceCatalogue?.sources||[]).map(s=>[s.id,s])),heads=new Map((d.domain?.entities||[]).map(e=>[e.id,e])),history=new Map(),invalid=new Set(),gaps=new Set(),seen=new Set(),active=new Set(),sourceChecks=new Set(),stack=records.map(record=>({record,exit:false}));
 for(const revision of d.domain?.revisions||[]){history.set(revision.id,revision.record);if(revision.record.data?.csoiRecord?.revisionId)history.set(revision.record.data.csoiRecord.revisionId,revision.record);}
 const hash=/^sha256:[a-f0-9]{64}$/;
 function checkSource(source,pin,digest){
  if(!source){invalid.add('DEPENDENCY_SOURCE_MISSING');return;}
  const sourceKey=source.id+'|'+(pin||'')+'|'+(digest||'');if(sourceChecks.has(sourceKey))return;sourceChecks.add(sourceKey);
  if(pin&&pin!==source.revisionId)invalid.add('DEPENDENCY_SOURCE_REVISION_CHANGED');
  if(digest&&digest!=='UNKNOWN'&&digest!==source.rawDigest)invalid.add('DEPENDENCY_SOURCE_DIGEST_MISMATCH');
  if(I.STAGES.indexOf(I.sourceStatus(d.domain.sourceCatalogue,source.id).stage)<I.STAGES.indexOf('RAW_BYTES_VERIFIED'))invalid.add('DEPENDENCY_SOURCE_BYTES_NOT_CURRENT');
  if(source.rights?.status==='UNKNOWN')gaps.add('SOURCE_RIGHTS_UNKNOWN');
  if(!source.currentAsOf)gaps.add('SOURCE_CURRENT_VERSION_UNKNOWN');
 }
 while(stack.length){
  const frame=stack.pop(),record=frame.record,capsule=record?.data?.csoiRecord,data=capsule?.data||record?.data||{},identity=record?.id+'|'+(record?.revisionId||capsule?.revisionId||'LEGACY');
  if(frame.exit){active.delete(identity);continue;}
  if(active.has(identity)){invalid.add('DEPENDENCY_CYCLE');continue;}
  if(seen.has(identity))continue;
  if(seen.size>=maxVisited){invalid.add('DEPENDENCY_TRAVERSAL_LIMIT');break;}
  seen.add(identity);active.add(identity);stack.push({record,exit:true});
  if(badStates.has(record?.state||record?.status)||capsule?.state==='WITHDRAWN')invalid.add('DEPENDENCY_RECORD_WITHDRAWN');
  if(sources.has(record?.id)){checkSource(sources.get(record.id),record.revisionId,record.rawDigest);continue;}
  const isSourceBacked=!!capsule&&capsule.sourceClass!=='SYNTHETIC'||record?.classification==='PUBLIC_TEXT_OBSERVED'||record?.classification==='LOCAL_RESEARCH'||['PUBLIC_TEXT_OBSERVED','METADATA_OBSERVED'].includes(record?.status);
  if(isSourceBacked){
   if(data.sourceId){
    const source=sources.get(data.sourceId);checkSource(source,null,data.sourceDigest||capsule?.provenance?.sourceRevision);
    if(capsule&&!(capsule.inputs||[]).some(i=>i.id===data.sourceId))gaps.add('LEGACY_SOURCE_INPUT_NOT_RECORDED');
   }else{
    const provenance=capsule?.provenance||data.source||record.provenance,observation=(d.sourceObservations||[]).find(o=>o.id===record.observationId),legacy=(d.sources||[]).find(s=>s.id===(record.sourceId||observation?.sourceId)),url=provenance?.url||observation?.url||legacy?.url||legacy?.officialUrl;
    if(url){
     const digest=provenance?.rawDigest||provenance?.sourceRevision||observation?.rawDigest||legacy?.rawDigest,candidates=[...sources.values()].filter(s=>s.officialUrl===url&&hash.test(s.rawDigest||'')&&(!hash.test(digest||'')||s.rawDigest===digest));
     if(candidates.length===1)checkSource(candidates[0],null,digest);else invalid.add(candidates.length?'DEPENDENCY_SOURCE_VERSION_AMBIGUOUS':'DEPENDENCY_SOURCE_MISSING');
     if(!hash.test(digest||'')){invalid.add('DEPENDENCY_SOURCE_DIGEST_NOT_PINNED');gaps.add('LEGACY_SOURCE_INPUT_NOT_RECORDED');}
    }else if(record?.sourceId||record?.observationId||record?.classification==='PUBLIC_TEXT_OBSERVED'||['PUBLIC_TEXT_OBSERVED','METADATA_OBSERVED'].includes(record?.status)){invalid.add('DEPENDENCY_SOURCE_MISSING');}
   }
  }
  for(const input of capsule?.inputs||[]){
   const source=sources.get(input.id);if(source){checkSource(source,input.revisionId,null);continue;}
   const head=heads.get(input.id),retained=history.get(input.revisionId);
   if(!head||!retained||retained.id!==input.id){invalid.add('DEPENDENCY_INPUT_PIN_MISSING');continue;}
   if(input.revisionId!==head.revisionId&&input.revisionId!==head.data?.csoiRecord?.revisionId)invalid.add('DEPENDENCY_INPUT_REVISION_CHANGED');
   if(badStates.has(head.state)||head.data?.csoiRecord?.state==='WITHDRAWN')invalid.add('DEPENDENCY_RECORD_WITHDRAWN');
   stack.push({record:{...retained,revisionId:input.revisionId},exit:false});
  }
 }
 return {current:invalid.size===0,invalidations:[...invalid],gaps:[...gaps],dependencyRecordsChecked:seen.size};
}
async function pinPath(d,spec){
 validate(spec);const requests=[...spec.nodes,...spec.relationships.filter(r=>r.kind==='ASSERTION').map(r=>({id:r.id,...(r.revisionId?{revisionId:r.revisionId}:{})}))],batch=await E.pinRecords(d,requests),views=batch.records.slice(0,spec.nodes.length),edges=[],gaps=new Set(['OFFICIAL_ADMISSION_UNKNOWN']),invalid=new Set();let edgeIndex=views.length;
 for(let n=0;n<spec.relationships.length;n++){
  const r=spec.relationships[n],reverse=r.direction==='REVERSE',from=views[n+(reverse?1:0)],to=views[n+(reverse?0:1)];let edge;
  if(r.kind==='ASSERTION'){
   const selected=batch.records[edgeIndex++],a=selected.record;need(a.from===from.id&&a.to===to.id,'PATH_ENDPOINT_ID_MISMATCH');
   for(const [expected,view]of [[a.fromRevisionId,from],[a.toRevisionId,to]]){if(expected){need([view.revisionId,view.record.versionId,view.record.data?.csoiRecord?.revisionId].includes(expected),'PATH_ENDPOINT_REVISION_MISMATCH');if(expected===view.record.versionId&&expected!==view.revisionId)gaps.add('LEGACY_ENDPOINT_LABEL_NOT_INDEPENDENTLY_WITNESSED');}else gaps.add('RELATIONSHIP_ENDPOINT_VERSION_NOT_RECORDED');}
   edge={kind:'ASSERTION',id:selected.id,revisionId:selected.revisionId,from:a.from,to:a.to,direction:reverse?'REVERSE':'FORWARD',predicate:a.predicate,state:a.state||a.status||'UNKNOWN',admission:a.admission||'UNKNOWN',evidenceRefs:structuredClone(a.evidenceRefs||[]),counterevidenceRefs:structuredClone(a.counterevidenceRefs||[])};
   const current=E.assertions(d).find(a=>a.id===selected.id);if(current&&badStates.has(current.state||current.status))invalid.add('RELATIONSHIP_WITHDRAWN');if(selected.currentRevisionId!==selected.revisionId)invalid.add('RELATIONSHIP_REVISION_CHANGED');
  }else{
   need(r.ownerId===from.id&&Number.isSafeInteger(r.inputIndex)&&r.inputIndex>=0,'PATH_INPUT_OWNER');const input=from.record.data?.csoiRecord?.inputs?.[r.inputIndex];need(input&&input.id===to.id,'PATH_INPUT_ENDPOINT');need([to.revisionId,to.record.data?.csoiRecord?.revisionId].includes(input.revisionId),'PATH_INPUT_REVISION_MISMATCH');
   const payload={ownerId:from.id,ownerRevisionId:from.revisionId,inputIndex:r.inputIndex,inputId:input.id,inputRevisionId:input.revisionId};const digest=await M.objectDigest(payload);if(r.revisionId)need(r.revisionId===digest,'PATH_INPUT_PROOF_MISMATCH');
   edge={kind:'INPUT',id:'input:'+from.id+':'+r.inputIndex,revisionId:digest,ownerId:from.id,inputIndex:r.inputIndex,from:from.id,to:to.id,direction:reverse?'REVERSE':'FORWARD',predicate:'GOVERNED_INPUT_LINEAGE',state:from.record.data.csoiRecord.state||'ACTIVE',admission:'PENDING',evidenceRefs:[{sourceRevision:from.record.provenance?.sourceRevision||null,locator:from.record.provenance?.locator||null}],counterevidenceRefs:[{reason:'Input lineage is not an official implementation, legal duty or causal relationship.'}]};
  }
  for(const evidence of edge.evidenceRefs){if(!evidence.sourceId){gaps.add('EVIDENCE_SOURCE_VERSION_UNKNOWN');continue;}const source=d.domain?.sourceCatalogue?.sources.find(s=>s.id===evidence.sourceId);if(!source||source.revisionId!==evidence.sourceRevision||evidence.rawDigest&&source.rawDigest!==evidence.rawDigest)invalid.add('EVIDENCE_SOURCE_PIN_INVALID');else if(I.STAGES.indexOf(I.sourceStatus(d.domain.sourceCatalogue,source.id).stage)<I.STAGES.indexOf('RAW_BYTES_VERIFIED'))invalid.add('EVIDENCE_SOURCE_BYTES_NOT_CURRENT');}
  if(badStates.has(edge.state)||edge.state==='WITHDRAWN')invalid.add('RELATIONSHIP_WITHDRAWN');if(edge.counterevidenceRefs.length)gaps.add('COUNTEREVIDENCE_RETAINED');if(edge.admission!=='ADMITTED')gaps.add('RELATIONSHIP_NOT_ADMITTED');edges.push(edge);
 }
 for(const view of views){if(view.historical)invalid.add('NODE_REVISION_CHANGED');if(view.record.data?.csoiRecord?.state==='WITHDRAWN')invalid.add('NODE_WITHDRAWN');if(view.category==='source'){const state=I.sourceStatus(d.domain.sourceCatalogue,view.id);if(I.STAGES.indexOf(state.stage)<I.STAGES.indexOf('RAW_BYTES_VERIFIED'))invalid.add('SOURCE_BYTES_NOT_CURRENT');if(state.rights==='UNKNOWN')gaps.add('SOURCE_RIGHTS_UNKNOWN');}}
 const dependencies=assessDependencies(d,views.map(v=>v.record));for(const issue of dependencies.invalidations)invalid.add(issue);for(const issue of dependencies.gaps)gaps.add(issue);
 if(new Set(views.map(v=>v.id)).size<views.length)gaps.add('CYCLE_REVISIT_EXPLICIT');
 const pinnedSpec={nodes:views.map(v=>({id:v.id,revisionId:v.revisionId})),relationships:edges.map(e=>e.kind==='ASSERTION'?{kind:e.kind,id:e.id,revisionId:e.revisionId,direction:e.direction}:{kind:e.kind,ownerId:e.ownerId,inputIndex:e.inputIndex,revisionId:e.revisionId,direction:e.direction})},core={format:'atlas-path-proof-1',methodVersion:METHOD,spec:pinnedSpec,nodePins:views.map(v=>({id:v.id,revisionId:v.revisionId,contentDigest:v.contentDigest})),relationships:edges};
 const regions=views.map(v=>v.record.data?.area||v.record.scope?.region||v.record.geographicExtent?.label||v.record.region).filter(v=>v&&v!=='UNKNOWN'),regionConflict=new Set(regions).size>1;
 return {core,digest:await M.objectDigest(core),views,assessment:{current:invalid.size===0,currentMeaning:'RECORDED_INPUT_CONTEXT_NOT_LIVE_SITE_OR_CURRENT_LAW',researchStatus:invalid.size?'INVALIDATED_RESEARCH_PATH':'PINNED_RESEARCH_PATH_ONLY',invalidations:[...invalid],gaps:[...gaps],dependencyRecordsChecked:dependencies.dependencyRecordsChecked,geographicContext:regionConflict?'CONFLICT_REQUIRES_REVIEW':'NOT_PROOF_OF_APPLICABILITY',currentLaw:'UNKNOWN',officialUse:'REJECTED_UNKNOWN_ADMISSION',arithmetic:'NOT_PERFORMED'},datasetDigest:batch.datasetDigest};
}
async function verifyPath(d,proof){try{need(proof.core?.methodVersion===METHOD&&await M.objectDigest(proof.core)===proof.digest,'PATH_PROOF_DIGEST');const check=await pinPath(d,proof.core.spec);return {integrity:check.digest===proof.digest,current:check.assessment.current,assessment:check.assessment};}catch(error){return {integrity:false,current:false,reason:error.message};}}
async function discover(d,{from,to,mode='BOTH',maxVisited=2000}={}){
 need(['ASSERTION','INPUT','BOTH','STRUCTURED'].includes(mode)&&Number.isSafeInteger(maxVisited)&&maxVisited>0&&maxVisited<=10000,'PATH_DISCOVERY_BOUNDS');const adjacency=new Map(),add=(a,b,r)=>{if(!adjacency.has(a))adjacency.set(a,[]);adjacency.get(a).push({to:b,relationship:r});};
 if(mode!=='INPUT')for(const a of E.assertions(d)){if(badStates.has(a.state||a.status))continue;add(a.from,a.to,{kind:'ASSERTION',id:a.id,direction:'FORWARD'});add(a.to,a.from,{kind:'ASSERTION',id:a.id,direction:'REVERSE'});}
 if(mode!=='ASSERTION')for(const owner of d.domain?.entities||[])for(const [index,input]of (owner.data?.csoiRecord?.inputs||[]).entries()){const data=owner.data.csoiRecord.data,parent=data.dcpClause?.parentId||data.sourceClauseId||data.reviewPlan?.clauseId;if(mode==='STRUCTURED'&&parent&&input.id!==parent)continue;add(owner.id,input.id,{kind:'INPUT',ownerId:owner.id,inputIndex:index,direction:'FORWARD'});add(input.id,owner.id,{kind:'INPUT',ownerId:owner.id,inputIndex:index,direction:'REVERSE'});}
 const queue=[from],seen=new Set([from]),previous=new Map();let i=0;
 while(i<queue.length&&i<maxVisited&&!seen.has(to)){const node=queue[i++];for(const step of adjacency.get(node)||[]){if(seen.has(step.to))continue;seen.add(step.to);previous.set(step.to,{from:node,relationship:step.relationship});queue.push(step.to);}}
 if(!seen.has(to))return {status:'UNKNOWN',truncated:i>=maxVisited,reason:'No eligible bounded relationship/input path; missing links are not inferred.'};
 const ids=[to],relationships=[];let cursor=to;while(cursor!==from){const step=previous.get(cursor);need(step,'PATH_TRACE_MISSING');relationships.push(step.relationship);ids.push(step.from);cursor=step.from;if(ids.length>32)return {status:'UNKNOWN',truncated:true,reason:'Path exceeds32display/proof nodes; inspect smaller retained segments.'};}
 const spec={nodes:ids.reverse().map(id=>({id})),relationships:relationships.reverse()};return {status:'FOUND_RESEARCH_ONLY',truncated:false,path:await pinPath(d,spec)};
}
async function comparePathSets(d,{left,right}={}){
 need(Array.isArray(left)&&Array.isArray(right)&&left.length>0&&right.length>0&&left.length<=4&&right.length<=4,'PATH_SET_BOUNDS');const l=[],r=[];for(const spec of left)l.push(await pinPath(d,spec));for(const spec of right)r.push(await pinPath(d,spec));
 const unique=paths=>[...new Map(paths.flatMap(p=>p.views).map(v=>[key(v),v])).values()],a=unique(l),b=unique(r),pairs=[];const used=new Set();let omitted=0;
 for(const v of a){const bucket=v.record.kind||v.record.recordType||v.category,w=b.find(w=>!used.has(key(w))&&(w.record.kind||w.record.recordType||w.category)===bucket);if(!w){omitted++;continue;}used.add(key(w));if(pairs.length>=16){omitted++;continue;}const compared=await E.compareRecords(d,{left:{id:v.id,revisionId:v.revisionId},right:{id:w.id,revisionId:w.revisionId}});pairs.push({left:{id:v.id,revisionId:v.revisionId},right:{id:w.id,revisionId:w.revisionId},checks:compared.checks,compatibility:compared.compatibility});}
 const core={format:'atlas-path-set-comparison-1',methodVersion:METHOD,left:l.map(p=>({core:p.core,digest:p.digest})),right:r.map(p=>({core:p.core,digest:p.digest})),pairs,unpairedRecords:omitted+b.filter(v=>!used.has(key(v))).length,arithmetic:'NOT_PERFORMED',officialRelationship:'UNKNOWN'};
 return {core,digest:await M.objectDigest(core),left:l,right:r,metadataCompatibility:pairs.some(p=>p.compatibility.status==='CONFLICT')?'CONFLICT':core.unpairedRecords||pairs.some(p=>p.compatibility.status==='UNKNOWN')?'UNKNOWN':'MATCHED_METADATA_ONLY',officialUse:'REJECTED_UNKNOWN_ADMISSION',current:l.concat(r).every(p=>p.assessment.current),meaning:'Typed research paths and gaps only; no statutory/implementation/causal promotion or arithmetic.'};
}
async function verifyComparison(d,proof){try{need(proof.core?.methodVersion===METHOD&&await M.objectDigest(proof.core)===proof.digest,'PATH_SET_PROOF_DIGEST');const check=await comparePathSets(d,{left:proof.core.left.map(p=>p.core.spec),right:proof.core.right.map(p=>p.core.spec)});return {integrity:check.digest===proof.digest,current:check.current,metadataCompatibility:check.metadataCompatibility,officialUse:check.officialUse};}catch(error){return {integrity:false,current:false,reason:error.message};}}
const api={pinPath,verifyPath,discover,comparePathSets,verifyComparison,assessDependencies};root.AtlasCSOIPaths=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
