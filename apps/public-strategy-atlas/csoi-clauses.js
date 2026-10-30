/* Source-pinned authored clause observations in the existing Atlas domain.
 * Containment is a flat, single-parent outline. Semantic candidates stay separate. */
(function(root){
'use strict';
const M=typeof module!=='undefined'?require('./atlas-model.js'):root.AtlasModel,G=typeof module!=='undefined'?require('./csoi-governance.js'):root.AtlasCSOIGovernance,I=typeof module!=='undefined'?require('./atlas-intake.js'):root.AtlasIntake;
const FORMAT='csoi-dcp-clause-1',METHOD='source-pinned-clause-outline-1',BOUNDARY='PUBLIC_DOCUMENT_CLAUSE_RESEARCH_NOT_LEGAL_APPLICABILITY',UNKNOWN='UNKNOWN';
const NODE_KEYS=['id','parentId','section','label','locator','summary','category','conditions','exceptions','obligations','anchor'];
const CLAUSE_KEYS=['format','parentId','parentRevisionId','section','category','conditions','exceptions','obligations','quantities','legalApplicability','reviewState','currentVersion','anchor'];
const DATA_KEYS=['title','summary','sourceId','sourceDigest','locator','methodVersion','dcpClause'];
const hash=/^sha256:[a-f0-9]{64}$/,id=/^csoi:[A-Za-z0-9][A-Za-z0-9:._/-]{0,185}$/;
function need(ok,code){if(!ok)throw Error(code);}
function plain(value){return !!value&&typeof value==='object'&&!Array.isArray(value)&&Object.getPrototypeOf(value)===Object.prototype;}
function closed(value,keys){return plain(value)&&Object.keys(value).every(k=>keys.includes(k));}
function text(value,max){return typeof value==='string'&&value.trim().length>0&&value.length<=max;}
function strings(value){return Array.isArray(value)&&value.length<=20&&value.every(s=>text(s,600));}
function anchorValid(anchor,source){return closed(anchor,['pdfPage','normalizedPageDigest','parserVersion'])&&Number.isSafeInteger(anchor.pdfPage)&&anchor.pdfPage>0&&anchor.pdfPage<=(source?.extraction?.totalPages||100000)&&hash.test(anchor.normalizedPageDigest||'')&&/^pypdf-[\w.-]+-layout-whitespace-1$/.test(anchor.parserVersion||'');}
function capsule(entity){return entity?.data?.csoiRecord?.data?.dcpClause||null;}
function records(d){return (d.domain?.entities||[]).filter(e=>capsule(e));}
function sourceFor(d,sourceId){return d.domain?.sourceCatalogue?.sources.find(s=>s.id===sourceId)||null;}
function clauseIssues(record,outer,source){
 const issues=[],data=record?.data,c=data?.dcpClause;
 if(!closed(data,DATA_KEYS)||!closed(c,CLAUSE_KEYS))return ['CLAUSE_CLOSED_FIELDS'];
 if(c.format!==FORMAT||data.methodVersion!==METHOD)issues.push('CLAUSE_FORMAT');
 if(!text(data.title,240)||!text(data.summary,1000)||!text(data.locator,600)||!text(c.section,160)||!['DOCUMENT','CHAPTER','SECTION','CLAUSE'].includes(c.category))issues.push('CLAUSE_TEXT_FIELDS');
 if(!strings(c.conditions)||!strings(c.exceptions)||!strings(c.obligations))issues.push('CLAUSE_CONDITIONS');
 if(!anchorValid(c.anchor,source))issues.push('CLAUSE_RESEARCH_ANCHOR');
 if(c.quantities!==UNKNOWN||c.legalApplicability!==UNKNOWN||c.reviewState!=='PENDING'||c.currentVersion!==UNKNOWN)issues.push('CLAUSE_AUTHORITY_OR_QUANTITY');
 if(c.parentId===null?c.parentRevisionId!==null:!id.test(c.parentId||'')||!hash.test(c.parentRevisionId||''))issues.push('CLAUSE_PARENT_FIELDS');
 if(!source||source.recordType!=='DOCUMENT'||source.classification!=='PUBLIC'||!hash.test(source.rawDigest||'')||data.sourceDigest!==source.rawDigest)issues.push('CLAUSE_SOURCE_PIN');
 if(record?.id!==outer?.id||outer?.kind!=='ContentBlock'||outer?.classification!=='LOCAL_RESEARCH'||outer?.admission!=='PENDING'||outer.label!==data.title||M.canonical(outer.scope)!==M.canonical(record.scope))issues.push('CLAUSE_DOMAIN_IDENTITY');
 if(record?.ownerModule!=='CSOI_OPERATIONS'||record?.security!=='PUBLIC'||record?.layer!=='L0'||record?.sourceClass!=='INDEPENDENT_RESEARCH'||record?.judgment!=='OBSERVATION'||record?.authority!=='INDEPENDENT_RESEARCH'||!['ACTIVE','WITHDRAWN'].includes(record?.state))issues.push('CLAUSE_PUBLIC_RESEARCH_ONLY');
 const p=record?.provenance,day=source?.retrievedAt?.slice(0,10);
 if(p?.contentMode!=='RESEARCH_SUMMARY'||p?.rights?.mode!=='AUTHORED_RESEARCH'||p?.url!==source?.officialUrl||p?.sourceRevision!==source?.rawDigest||p?.locator!==data.locator)issues.push('CLAUSE_AUTHORED_PROVENANCE');
 if(record?.scope?.region!==source?.geographicExtent?.label||record?.scope?.boundary!==BOUNDARY||record?.scope?.period?.from!==day||record?.scope?.period?.to!==day)issues.push('CLAUSE_OBSERVATION_SCOPE');
 const inputs=record?.inputs||[];
 if(inputs.length!==(c.parentId===null?1:2)||!inputs.some(i=>i.id===source?.id&&i.revisionId===source?.revisionId)||c.parentId!==null&&!inputs.some(i=>i.id===c.parentId&&i.revisionId===c.parentRevisionId))issues.push('CLAUSE_INPUT_PINS');
 return issues;
}
async function verifyStructure(d){
 const issues=[],all=d.domain?.revisions||[],byRevision=new Map(all.map((r,index)=>[r.id,{...r,index}])),heads=new Map(records(d).map(e=>[e.id,e]));
 for(let index=0;index<all.length;index++){
  const revision=all[index],outer=revision.record,record=outer?.data?.csoiRecord,c=capsule(outer);if(!c)continue;
  const source=sourceFor(d,record.data.sourceId);for(const issue of clauseIssues(record,outer,source))issues.push(issue+':'+outer.id);
  if(!(d.domain.sourceCatalogue?.events||[]).some(e=>e.operation==='STAGE'&&e.sourceId===source?.id&&e.sourceRevision===source?.revisionId&&e.stage==='RAW_BYTES_VERIFIED'&&e.evidence.rawDigest===source?.rawDigest))issues.push('CLAUSE_SOURCE_NEVER_BYTE_VERIFIED:'+outer.id);
  if(!await G.verifyRecord(record)||!G.assessPublic(record,{operation:'STORAGE'}).allowed)issues.push('CLAUSE_ENVELOPE:'+outer.id);
  if(c.parentId!==null){const parent=byRevision.get(c.parentRevisionId),p=parent?.record?.data?.csoiRecord;
   if(!parent||parent.index>=index||parent.logicalId!==c.parentId||!capsule(parent.record))issues.push('CLAUSE_PARENT_REVISION:'+outer.id);
   else if(p.data.sourceId!==record.data.sourceId||p.data.sourceDigest!==record.data.sourceDigest||M.canonical(p.scope)!==M.canonical(record.scope))issues.push('CLAUSE_FOREIGN_PARENT:'+outer.id);
  }
 }
 for(const entity of heads.values()){
  const retained=byRevision.get(entity.revisionId),{revisionId,...payload}=entity;
  if(!retained||M.canonical(retained.record)!==M.canonical(payload))issues.push('CLAUSE_HEAD_REVISION:'+entity.id);
  const c=capsule(entity);if(c.parentId!==null&&!heads.has(c.parentId))issues.push('CLAUSE_PARENT_HEAD_MISSING:'+entity.id);
 }
 // Current logical-parent cycles can arise even when each historical revision pins an older parent.
 const done=new Set();for(const entity of heads.values()){
  if(done.has(entity.id))continue;const path=new Set();let next=entity;
  while(next&&!done.has(next.id)){if(path.has(next.id)){issues.push('CLAUSE_CONTAINMENT_CYCLE:'+entity.id);break;}path.add(next.id);next=heads.get(capsule(next)?.parentId);}
  for(const key of path)done.add(key);
 }
 return {integrity:issues.length===0,issues:[...new Set(issues)]};
}
function validateNode(node){
 need(closed(node,NODE_KEYS),'CLAUSE_NODE_FIELDS');need(id.test(node.id||'')&&(node.parentId===null||id.test(node.parentId||'')),'CLAUSE_NODE_ID');
 need(text(node.section,160)&&text(node.label,240)&&text(node.locator,600)&&text(node.summary,1000),'CLAUSE_NODE_TEXT');
 need(node.category===undefined||['DOCUMENT','CHAPTER','SECTION','CLAUSE'].includes(node.category),'CLAUSE_NODE_CATEGORY');
 need(anchorValid(node.anchor),'CLAUSE_NODE_ANCHOR');
 for(const key of ['conditions','exceptions','obligations'])need(node[key]===undefined||strings(node[key]),'CLAUSE_NODE_ARRAY');
 need(G.inspectPayload(node).length===0,'CLAUSE_PUBLIC_PAYLOAD');
}
async function registerOutline(d,input){
 need(closed(input,['sourceId','sourceRevision','nodes'])&&Array.isArray(input.nodes)&&input.nodes.length>0&&input.nodes.length<=10000,'CLAUSE_OUTLINE_REQUIRED');
 need((await verifyStructure(d)).integrity,'CLAUSE_EXISTING_STRUCTURE_INVALID');
 need(await M.verifySnapshot(await M.exportSnapshot(d)),'CLAUSE_DATASET_INVALID');
 const source=sourceFor(d,input.sourceId),catalogue=d.domain?.sourceCatalogue;
 need(source&&source.recordType==='DOCUMENT'&&source.classification==='PUBLIC'&&source.rawDigest===input.sourceRevision&&hash.test(input.sourceRevision||''),'CLAUSE_SOURCE_REQUIRED');
 need(I.STAGES.indexOf(I.sourceStatus(catalogue,source.id).stage)>=I.STAGES.indexOf('RAW_BYTES_VERIFIED'),'CLAUSE_SOURCE_BYTES_NOT_CURRENT');
 const ids=new Set(),available=new Map(records(d).map(e=>[e.id,e]));
 for(const node of input.nodes){validateNode(node);need(!ids.has(node.id),'CLAUSE_DUPLICATE_ID');ids.add(node.id);
  if(node.parentId!==null){need(available.has(node.parentId),'CLAUSE_PARENT_FIRST_REQUIRED');const parent=available.get(node.parentId);if(parent?.data)need(parent.data.csoiRecord.data.sourceId===source.id&&parent.data.csoiRecord.data.sourceDigest===source.rawDigest,'CLAUSE_FOREIGN_PARENT');}
  available.set(node.id,{pending:true});
 }
 let next=d;
 for(const node of input.nodes){
  const parent=node.parentId===null?null:M.domainIndex(next).get(node.parentId),parentRecord=parent?.data?.csoiRecord;
  if(parent)need(parentRecord?.data.sourceId===source.id&&parentRecord?.data.sourceDigest===source.rawDigest&&parentRecord.state==='ACTIVE','CLAUSE_PARENT_NOT_CURRENT');
  need(anchorValid(node.anchor,source),'CLAUSE_SOURCE_PAGE_BOUNDS');
  const day=source.retrievedAt.slice(0,10),clause={format:FORMAT,parentId:node.parentId,parentRevisionId:parent?.revisionId||null,section:node.section,category:node.category||'CLAUSE',conditions:node.conditions||[],exceptions:node.exceptions||[],obligations:node.obligations||[],quantities:UNKNOWN,legalApplicability:UNKNOWN,reviewState:'PENDING',currentVersion:UNKNOWN,anchor:structuredClone(node.anchor)};
  const record=await G.makeRecord({id:node.id,ownerModule:'CSOI_OPERATIONS',security:'PUBLIC',layer:'L0',sourceClass:'INDEPENDENT_RESEARCH',judgment:'OBSERVATION',authority:'INDEPENDENT_RESEARCH',scope:{region:source.geographicExtent.label,boundary:BOUNDARY,period:{from:day,to:day}},inputs:[{id:source.id,revisionId:source.revisionId},...(parent?[{id:parent.id,revisionId:parent.revisionId}]:[])],data:{title:node.label,summary:node.summary,sourceId:source.id,sourceDigest:source.rawDigest,locator:node.locator,methodVersion:METHOD,dcpClause:clause},sensitivity:{personalData:false,confidential:false,reidentifiable:false},provenance:{contentMode:'RESEARCH_SUMMARY',url:source.officialUrl,locator:node.locator,sourceRevision:source.rawDigest,rights:{mode:'AUTHORED_RESEARCH',basis:'Bounded repository-authored factual observations only. Original source reuse rights, current legal consolidation and authorised admission remain UNKNOWN/PENDING.'}},observedAt:source.retrievedAt,state:'ACTIVE'});
  const existing=M.domainIndex(next).get(node.id);
  if(existing){need(existing.data?.csoiRecord?.revisionId===record.revisionId,'CLAUSE_ID_CONFLICT');continue;}
  next=await M.registerResearchRecord(next,{record,kind:'ContentBlock',label:node.label,stationId:source.stationId,reason:'Append source-pinned authored clause observation; no official rule, applicability, quantity or semantic relationship admitted.'});
 }
 need((await verifyStructure(next)).integrity,'CLAUSE_STRUCTURE_INVALID');return next;
}
function query(d,{parentId=null,sourceId=null,offset=0,limit=30}={}){
 need(Number.isSafeInteger(offset)&&offset>=0&&Number.isSafeInteger(limit)&&limit>0&&limit<=100,'CLAUSE_QUERY_BOUNDS');
 const items=records(d).filter(e=>capsule(e).parentId===parentId&&(!sourceId||e.data.csoiRecord.data.sourceId===sourceId));return {items:items.slice(offset,offset+limit),total:items.length,offset,nextOffset:offset+limit<items.length?offset+limit:null};
}
function parents(d,logicalId){const byId=new Map(records(d).map(e=>[e.id,e])),items=[],seen=new Set();let current=byId.get(logicalId);need(current,'CLAUSE_NOT_FOUND');while(current){need(!seen.has(current.id),'CLAUSE_CONTAINMENT_CYCLE');seen.add(current.id);items.push(current);const p=capsule(current).parentId;if(p===null)break;current=byId.get(p);need(current,'CLAUSE_PARENT_HEAD_MISSING');}return items;}
async function status(d,logicalId){
 const structure=await verifyStructure(d),entity=M.domainIndex(d).get(logicalId);need(capsule(entity),'CLAUSE_NOT_FOUND');const reasons=[];
 if(!structure.integrity)reasons.push('STRUCTURE_INVALID');
 const byId=new Map(records(d).map(e=>[e.id,e])),seen=new Set();let current=entity;
 while(current&&!seen.has(current.id)){
  seen.add(current.id);const record=current.data.csoiRecord,c=capsule(current),source=sourceFor(d,record.data.sourceId);
  if(record.state!=='ACTIVE')reasons.push('CLAUSE_WITHDRAWN');
  if(!source||source.rawDigest!==record.data.sourceDigest)reasons.push('SOURCE_PIN_MISSING');
  else if(I.STAGES.indexOf(I.sourceStatus(d.domain.sourceCatalogue,source.id).stage)<I.STAGES.indexOf('RAW_BYTES_VERIFIED'))reasons.push('SOURCE_BYTES_WITHDRAWN');
  if(c.parentId===null)break;const parent=byId.get(c.parentId);if(!parent){reasons.push('PARENT_MISSING');break;}if(parent.revisionId!==c.parentRevisionId)reasons.push('PARENT_REVISION_CHANGED');current=parent;
 }
 const unique=[...new Set(reasons)];return {integrity:structure.integrity,current:structure.integrity&&unique.length===0,status:unique.length?'INVALIDATED_RESEARCH_CONTEXT':'SOURCE_PINNED_RESEARCH_PENDING_REVIEW',reasons:unique,legalApplicability:UNKNOWN,reviewState:'PENDING',officialAdmission:'PENDING'};
}
const api={FORMAT,METHOD,registerOutline,verifyStructure,query,parents,status,validateNode};root.AtlasCSOIClauses=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
