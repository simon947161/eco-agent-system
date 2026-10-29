/* Local research annotations only. No network or automatic persistence. */
(function(root){
'use strict';
const m=typeof module!=='undefined'?require('./atlas-model.js'):root.AtlasModel;
const hash=/^sha256:[a-f0-9]{64}$/;
const actions=new Set(['CORRECT','SUPERSEDE','RETRACT','REVERT','CONTEST']);
function freeze(value){if(value&&typeof value==='object'){Object.values(value).forEach(freeze);Object.freeze(value);}return value;}
function checkDay(s){return typeof s==='string'&&/^\d{4}-\d{2}-\d{2}$/.test(s)&&Number.isFinite(Date.parse(s))&&new Date(s).toISOString().slice(0,10)===s;}
function checkTime(s){return typeof s==='string'&&/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?Z$/.test(s)&&Number.isFinite(Date.parse(s))&&new Date(s).toISOString().slice(0,10)===s.slice(0,10);}
function fields(item){return {title:item.title,text:item.text};}
async function create(dataset){return freeze({format:'atlas-local-workspace-1',baseDigest:await m.objectDigest(m.legacyBase(dataset)),revisions:[],events:[],signature:null});}
function head(workspace,targetId){return workspace.revisions.filter(r=>r.targetId===targetId).at(-1)||null;}
function compare(before,after){return ['title','text'].filter(k=>before[k]!==after[k]).map(field=>({field,before:before[field],after:after[field]}));}
async function validate(workspace,dataset){
 const issues=[];
 if(!workspace||workspace.format!=='atlas-local-workspace-1'||!Array.isArray(workspace.revisions)||!Array.isArray(workspace.events))return ['WORKSPACE_FORMAT'];
 if(workspace.signature!==null)return ['UNSUPPORTED_SIGNATURE'];
 if(workspace.revisions.length>500||workspace.events.length!==workspace.revisions.length)return ['WORKSPACE_BOUNDS'];
 if(workspace.baseDigest!==await m.objectDigest(m.legacyBase(dataset)))return ['BASE_DATASET_CONFLICT'];
 const heads=new Map(),versions=new Map(),items=new Map(dataset.contentItems.map(c=>[c.id,c]));let previous=null;
 for(let i=0;i<workspace.revisions.length;i++){
  const r=workspace.revisions[i],e=workspace.events[i];
  if(!r||!e||typeof r!=='object'||typeof e!=='object'){issues.push('RECORD_REQUIRED');continue;}
  const item=items.get(r.targetId),old=heads.get(r.targetId);
  if(!item||r.sequence!==i||r.id!=='local-revision-'+i||!actions.has(r.action)||!r.reason||typeof r.reason!=='string'||r.reason.length>1000||!checkTime(r.observedAt)||r.actor!=='local-researcher'||r.classification!=='LOCAL_ANNOTATION'||r.signature!==null)issues.push('REVISION_FIELDS:'+i);
  if(!r.content||Object.keys(r.content).sort().join(',')!=='text,title'||typeof r.content.title!=='string'||!r.content.title.trim()||r.content.title.length>200||typeof r.content.text!=='string'||r.content.text.length>20000)issues.push('REVISION_CONTENT:'+i);
  if(r.parentRevisionDigest!==(old?.digest??null)||item&&r.baseItemDigest!==await m.objectDigest(item))issues.push('REVISION_PARENT:'+i);
  if(r.state!==(r.action==='RETRACT'?'RETRACTED':r.action==='CONTEST'?'CONTESTED':'ACTIVE'))issues.push('REVISION_STATE:'+i);
  if(r.action==='REVERT'){
   const target=r.revertsTo===null?item:versions.get(r.revertsTo);
   if(!target||r.revertsTo!==null&&target.targetId!==r.targetId||m.canonical(r.content)!==m.canonical(r.revertsTo===null?fields(item):target.content))issues.push('INVALID_REVERT:'+i);
  }else if(r.revertsTo!==null)issues.push('UNEXPECTED_REVERT_TARGET:'+i);
  const {digest,...payload}=r;if(!hash.test(digest)||await m.objectDigest(payload)!==digest)issues.push('REVISION_DIGEST:'+i);
  const {digest:eventDigest,...eventPayload}=e;
  if(e.id!=='local-event-'+i||e.sequence!==i||e.previousDigest!==previous||e.revisionDigest!==r.digest||e.targetId!==r.targetId||e.type!==r.action||e.reason!==r.reason||e.observedAt!==r.observedAt||await m.objectDigest(eventPayload)!==eventDigest)issues.push('EVENT_CHAIN:'+i);
  if(r.action==='RETRACT'&&item&&m.canonical(r.content)!==m.canonical(old?.content??fields(item)))issues.push('RETRACT_CHANGED_CONTENT:'+i);
  heads.set(r.targetId,r);versions.set(r.digest,r);previous=e.digest;
 }
 return issues;
}
async function commit(workspace,dataset,{targetId,expectedHead=null,content,action='CORRECT',reason,observedAt=new Date().toISOString(),revertsTo=null}){
 const errors=await validate(workspace,dataset);if(errors.length)throw Error(errors.join(';'));
 const item=dataset.contentItems.find(c=>c.id===targetId);if(!item)throw Error('TARGET_NOT_FOUND');
 const old=head(workspace,targetId);if((old?.digest??null)!==expectedHead)throw Error('CONFLICT: target changed since this editor opened');
 const sequence=workspace.revisions.length;
 const payload={id:'local-revision-'+sequence,sequence,targetId,baseItemDigest:await m.objectDigest(item),parentRevisionDigest:expectedHead,content,action,state:action==='RETRACT'?'RETRACTED':action==='CONTEST'?'CONTESTED':'ACTIVE',reason,observedAt,actor:'local-researcher',classification:'LOCAL_ANNOTATION',revertsTo,signature:null};
 const revision={...payload,digest:await m.objectDigest(payload)};
 const eventPayload={id:'local-event-'+sequence,sequence,targetId,type:action,reason,observedAt,revisionDigest:revision.digest,previousDigest:workspace.events.at(-1)?.digest??null};
 const result={...workspace,revisions:[...workspace.revisions,revision],events:[...workspace.events,{...eventPayload,digest:await m.objectDigest(eventPayload)}]};
 const after=await validate(result,dataset);if(after.length)throw Error(after.join(';'));return freeze(result);
}
async function revert(workspace,dataset,{targetId,expectedHead,revertsTo=null,reason,observedAt}){
 const source=revertsTo===null?dataset.contentItems.find(c=>c.id===targetId):workspace.revisions.find(r=>r.digest===revertsTo&&r.targetId===targetId);if(!source)throw Error('REVERT_TARGET_NOT_FOUND');
 return commit(workspace,dataset,{targetId,expectedHead,revertsTo,reason,observedAt,action:'REVERT',content:revertsTo===null?fields(source):source.content});
}
async function importWorkspace(text,dataset,expectedDigest=null){
 if(typeof text!=='string'||new TextEncoder().encode(text).length>2*1024*1024)throw Error('IMPORT_TOO_LARGE');
 const parsed=JSON.parse(text),issues=await validate(parsed,dataset);if(issues.length)throw Error(issues.join(';'));
 if(expectedDigest&&await m.objectDigest(parsed)!==expectedDigest)throw Error('WORKSPACE_CHECKPOINT_MISMATCH');return freeze(parsed);
}
function replay(workspace,dataset,through=workspace.revisions.length-1){
 if(!Number.isInteger(through)||through< -1||through>=workspace.revisions.length)throw Error('REPLAY_BOUNDS');
 const result=new Map(dataset.contentItems.map(c=>[c.id,{...fields(c),classification:c.status,localState:'BASE'}]));
 for(const r of workspace.revisions.slice(0,through+1))result.set(r.targetId,{...r.content,classification:'LOCAL_ANNOTATION',localState:r.state,revisionDigest:r.digest});return result;
}
async function subtreeReceipt(workspace,dataset,rootId,through=workspace.revisions.length-1){
 const errors=await validate(workspace,dataset);if(errors.length)throw Error(errors.join(';'));
 const view=replay(workspace,dataset,through),items=new Map(dataset.contentItems.map(c=>[c.id,c]));if(!items.has(rootId))throw Error('CONTENT_NOT_FOUND');
 const {children}=m.contentIndex(dataset),order=[{id:rootId,depth:0}],receipts=new Map(),seen=new Set();let maxDepth=0;
 for(let i=0;i<order.length;i++){const {id,depth}=order[i];if(seen.has(id))throw Error('CONTENT_CYCLE');seen.add(id);maxDepth=Math.max(maxDepth,depth);for(const c of children.get(id)||[])order.push({id:c.id,depth:depth+1});}
 for(let i=order.length-1;i>=0;i--){const id=order[i].id,item=items.get(id),local=view.get(id),childReceipts=(children.get(id)||[]).slice().sort((a,b)=>a.id<b.id?-1:a.id>b.id?1:0).map(c=>receipts.get(c.id));
  const payload={id,sourceItemDigest:await m.objectDigest(item),localView:local,children:childReceipts.map(c=>({id:c.id,digest:c.digest}))};receipts.set(id,{id,digest:await m.objectDigest(payload),children:childReceipts});
 }
 const receipt=receipts.get(rootId);return maxDepth<=128?receipt:{format:'atlas-local-subtree-flat-2',id:rootId,digest:receipt.digest,records:[...receipts.values()].sort((a,b)=>a.id<b.id?-1:a.id>b.id?1:0).map(r=>({...r,children:r.children.map(c=>({id:c.id,digest:c.digest}))}))};
}
function assessAdmission(record){
 const stages=['SOURCE_OBSERVED','BYTE_VERIFIED','CONTENT_EXTRACTED','OFFICIAL_REVISION_CONFIRMED','ADMISSION_PENDING_REVIEW','ADMITTED'];
 const blockers=[];
 if(!record||!record.sourceUrl?.startsWith('https://www.snowymonaro.nsw.gov.au/')||!checkTime(record.retrievedAt)||record.httpStatus!==200||record?.stages?.SOURCE_OBSERVED!=='PASS')blockers.push('SOURCE_NOT_VERIFIED');
 if(!hash.test(record?.rawDigest)||!Number.isInteger(record?.byteLength)||record.byteLength<1||record?.stages?.BYTE_VERIFIED!=='PASS')blockers.push('BYTES_NOT_VERIFIED');
 if(!record?.extraction?.text||record?.extraction?.digest!=='sha256:'+m.sha256(new TextEncoder().encode(record.extraction.text))||record?.stages?.CONTENT_EXTRACTED!=='PASS'||!Number.isInteger(record?.anchor?.page)||record.anchor.page<1)blockers.push('EXTRACTION_NOT_VERIFIED');
 if(record?.revision?.status!=='CONFIRMED'||!checkDay(record?.revision?.currentAsOf)||!checkDay(record?.revision?.adoptedOnObserved)||record?.stages?.OFFICIAL_REVISION_CONFIRMED!=='PASS')blockers.push('REVISION_NOT_CONFIRMED');
 if(record?.permission?.status!=='PERMITTED'||!record?.permission?.licence)blockers.push('REUSE_PERMISSION_UNKNOWN');
 if(!record?.geography?.region||!checkDay(record?.effectivePeriod?.from)||!checkDay(record?.effectivePeriod?.to)||record.effectivePeriod.from>record.effectivePeriod.to)blockers.push('APPLICABILITY_UNKNOWN');
 if(record?.review?.decision!=='APPROVED'||record.review.reviewerRole!=='HUMAN_REVIEWER'||!record.review.reviewer||!checkTime(record.review.decidedAt))blockers.push('HUMAN_REVIEW_PENDING');
 return {status:blockers.length?'ADMISSION_PENDING_REVIEW':'ADMITTED',blockers,stages:stages.map(stage=>({stage,state:stage==='ADMITTED'?(blockers.length?'NO':'YES'):record?.stages?.[stage]??'UNKNOWN'}))};
}
function extendsHistory(previous,next){return previous.baseDigest===next.baseDigest&&next.revisions.length>=previous.revisions.length&&previous.revisions.every((r,i)=>r.digest===next.revisions[i].digest);}
function database(){return new Promise((resolve,reject)=>{if(!globalThis.indexedDB){reject(Error('LOCAL_DATABASE_UNAVAILABLE'));return;}const r=indexedDB.open('climateos-atlas-local-research-v1',1);r.onupgradeneeded=()=>{r.result.createObjectStore('heads');r.result.createObjectStore('snapshots');};r.onerror=()=>reject(r.error);r.onsuccess=()=>resolve(r.result);});}
async function loadLocal(baseDigest){
 const db=await database();try{return await new Promise((resolve,reject)=>{const tx=db.transaction('heads','readonly'),r=tx.objectStore('heads').get(baseDigest);r.onsuccess=()=>resolve(r.result??null);r.onerror=()=>reject(r.error);});}finally{db.close();}
}
async function saveLocal(workspace,dataset,expectedCheckpoint=null){
 const errors=await validate(workspace,dataset);if(errors.length)throw Error(errors.join(';'));
 const checkpoint=await m.objectDigest(workspace),db=await database();
 try{return await new Promise((resolve,reject)=>{let error;const tx=db.transaction(['heads','snapshots'],'readwrite'),heads=tx.objectStore('heads'),r=heads.get(workspace.baseDigest);
  r.onsuccess=()=>{const old=r.result;
   if((old?.checkpoint??null)!==expectedCheckpoint||old&&!extendsHistory(old.workspace,workspace)){error=Error('STORAGE_CONFLICT: load the saved head; prior revisions cannot be overwritten');tx.abort();return;}
   const record={checkpoint,workspace,savedAt:new Date().toISOString()};heads.put(record,workspace.baseDigest);tx.objectStore('snapshots').put(record,checkpoint);
  };tx.oncomplete=()=>resolve(checkpoint);tx.onabort=()=>reject(error||tx.error||Error('SAVE_ABORTED'));tx.onerror=()=>{error=tx.error;};
 });}finally{db.close();}
}
const api={subtreeReceipt,extendsHistory,saveLocal,loadLocal,create,head,compare,validate,commit,revert,importWorkspace,replay,assessAdmission,fields};root.AtlasWorkspace=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
