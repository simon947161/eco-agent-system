/* atlas-1: bounded, offline evidence contracts. Hashes prove bytes, not truth. */
(function(root){
'use strict';
const domain=typeof module!=='undefined'?require('./atlas-domain.js'):root.AtlasDomain;
const statuses=new Set(['EXPLICIT_OFFICIAL','RESEARCH_INFERRED','HYPOTHESIS_ONLY','SYNTHETIC','UNKNOWN','CONTRADICTED','SUPERSEDED']);
function canonical(v){
 if(v===null||typeof v==='boolean'||typeof v==='string')return JSON.stringify(v);
 if(typeof v==='number'){if(!Number.isFinite(v))throw Error('NON_FINITE');return JSON.stringify(v);}
 if(Array.isArray(v))return '['+v.map(canonical).join(',')+']';
 if(v&&Object.getPrototypeOf(v)===Object.prototype)return '{'+Object.keys(v).sort().map(k=>JSON.stringify(k)+':'+canonical(v[k])).join(',')+'}';
 throw Error('UNSUPPORTED_VALUE');
}
// Portable SHA-256 fallback for offline file:// and HTTP preview contexts.
function sha256(bytes){
 const k=[0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2];
 const h=[0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19];
 const padded=new Uint8Array(Math.ceil((bytes.length+9)/64)*64);padded.set(bytes);padded[bytes.length]=128;
 const view=new DataView(padded.buffer);view.setUint32(padded.length-8,Math.floor(bytes.length/0x20000000));view.setUint32(padded.length-4,(bytes.length*8)>>>0);
 const ro=(v,n)=>(v>>>n)|(v<<(32-n));
 for(let offset=0;offset<padded.length;offset+=64){
  const w=new Uint32Array(64);for(let i=0;i<16;i++)w[i]=view.getUint32(offset+i*4);
  for(let i=16;i<64;i++){const x=w[i-15],y=w[i-2];w[i]=(w[i-16]+(ro(x,7)^ro(x,18)^(x>>>3))+w[i-7]+(ro(y,17)^ro(y,19)^(y>>>10)))>>>0;}
  let [a,b,c,d,e,f,g,j]=h;
  for(let i=0;i<64;i++){const t1=(j+(ro(e,6)^ro(e,11)^ro(e,25))+((e&f)^(~e&g))+k[i]+w[i])>>>0,t2=((ro(a,2)^ro(a,13)^ro(a,22))+((a&b)^(a&c)^(b&c)))>>>0;j=g;g=f;f=e;e=(d+t1)>>>0;d=c;c=b;b=a;a=(t1+t2)>>>0;}
  [a,b,c,d,e,f,g,j].forEach((v,i)=>h[i]=(h[i]+v)>>>0);
 }
 return h.map(v=>v.toString(16).padStart(8,'0')).join('');
}
async function digest(bytes){if(!(bytes instanceof Uint8Array))throw Error('BYTES_REQUIRED');return 'sha256:'+(globalThis.crypto?.subtle?Array.from(new Uint8Array(await globalThis.crypto.subtle.digest('SHA-256',bytes)),b=>b.toString(16).padStart(2,'0')).join(''):sha256(bytes));}
async function objectDigest(value){return digest(new TextEncoder().encode(canonical(value)));}
function applicability(assertion,revision,context){
 if(!revision||!context?.date||!context?.region||!revision.validFrom||!revision.validTo||!revision.region)return 'UNKNOWN';
 if(![context.date,revision.validFrom,revision.validTo].every(x=>/^\d{4}-\d{2}-\d{2}$/.test(x)&&Number.isFinite(Date.parse(x))&&new Date(x).toISOString().slice(0,10)===x)||revision.validFrom>revision.validTo)return 'UNKNOWN';
 if(context.region!==revision.region||context.date<revision.validFrom||context.date>revision.validTo)return 'VERSION_OR_SCOPE_CONFLICT';
 if(assertion.revisionId!==revision.id)return 'VERSION_OR_SCOPE_CONFLICT';
 return assertion.status==='SYNTHETIC'?'SYNTHETIC_ONLY':'REQUIRES_REVIEW';
}
function validate(d){
 const issues=[];if(!d||typeof d!=='object')return ['DATASET_REQUIRED'];if(d.schemaVersion!=='atlas-1')issues.push('SCHEMA_VERSION');
 for(const key of ['sources','revisions','nodes','assertions','hypotheses','contentBlocks','events','edges'])if(!Array.isArray(d[key]))issues.push('ARRAY_REQUIRED:'+key);
 if(issues.length)return issues;
 for(const key of ['sources','revisions','nodes','assertions','hypotheses','contentBlocks','events','edges'])if(d[key].some(o=>!o||typeof o!=='object'||Array.isArray(o)))issues.push('OBJECT_REQUIRED:'+key);
 if(issues.length)return issues;
 for(const key of ['sources','revisions','nodes','assertions','hypotheses','contentBlocks','events','edges']){const seen=new Set();for(const o of d[key]){if(!o.id||seen.has(o.id))issues.push('DUPLICATE_OR_MISSING_ID:'+key);seen.add(o.id);}}
 const nodes=new Map(d.nodes.map(n=>[n.id,n])),revs=new Map(d.revisions.map(r=>[r.id,r])),sources=new Map(d.sources.map(s=>[s.id,s]));
 const blocks=new Map(d.contentBlocks.map(b=>[b.id,b]));
 const hash=x=>/^sha256:[a-f0-9]{64}$/.test(x);
 const day=x=>typeof x==='string'&&/^\d{4}-\d{2}-\d{2}$/.test(x)&&Number.isFinite(Date.parse(x))&&new Date(x).toISOString().slice(0,10)===x;
 for(const s of d.sources){
  if(typeof s.url!=='string'||!(/^(https:\/\/|\.\/qa\/)/.test(s.url)))issues.push('UNSAFE_SOURCE_URL:'+s.id);
  if(s.revisionId!==null&&!revs.has(s.revisionId))issues.push('SOURCE_REVISION:'+s.id);
  if(s.rawDigest!==null&&!hash(s.rawDigest))issues.push('SOURCE_DIGEST:'+s.id);
 }
 for(const r of d.revisions){
  if(!r.logicalId||!r.region||!day(r.validFrom)||!day(r.validTo)||r.validFrom>r.validTo)issues.push('REVISION_SCOPE:'+r.id);
  const source=sources.get(r.sourceId);
  if(!source||source.revisionId!==r.id||r.rawDigest!==source.rawDigest)issues.push('REVISION_SOURCE:'+r.id);
 }
 for(const a of d.assertions){
  const r=revs.get(a.revisionId);
  if(!a.predicate||!r||a.region!==r.region||!day(a.validFrom)||!day(a.validTo)||a.validFrom>a.validTo||a.validFrom<r.validFrom||a.validTo>r.validTo)issues.push('ASSERTION_SCOPE:'+a.id);
  for(const key of ['evidenceRefs','counterevidenceRefs'])for(const ref of Array.isArray(a[key])?a[key]:[]){
   if(!ref||typeof ref!=='object'){issues.push('BROKEN_EVIDENCE_REF:'+a.id);continue;}
   const b=blocks.get(ref.blockId),rev=revs.get(ref.revisionId);
   if(!b||!rev||!ref.locator||b.sourceId!==ref.sourceId||rev.sourceId!==ref.sourceId)issues.push('BROKEN_EVIDENCE_REF:'+a.id);
  }
 }
 for(const h of d.hypotheses)if(h.status!=='HYPOTHESIS_ONLY'||!h.ruleVersion||!h.explanation||!Array.isArray(h.counterevidence)||!h.counterevidence.length||!Array.isArray(h.assertionIds)||!h.assertionIds.length||h.assertionIds.some(id=>!d.assertions.some(a=>a.id===id)))issues.push('INVALID_HYPOTHESIS:'+h.id);
 if(d.sourceObservations!==undefined){
  if(!Array.isArray(d.sourceObservations))issues.push('OBSERVATIONS_ARRAY');
  else {const seen=new Set();for(const o of d.sourceObservations){if(!o||!o.id||seen.has(o.id)||!sources.has(o.sourceId)||!day(o.observedOn)||!o.locator||!o.note||!['METADATA_OBSERVED','PUBLIC_TEXT_OBSERVED'].includes(o.status)||o.rawDigest!==null||o.url&&!o.url.startsWith('https://'))issues.push('INVALID_SOURCE_OBSERVATION');if(o)seen.add(o.id);}}
 }
 for(const b of d.contentBlocks)if(!Number.isInteger(b.offset)||b.offset<0||!Number.isInteger(b.length)||b.length<1||!/^sha256:[a-f0-9]{64}$/.test(b.digest)||!sources.has(b.sourceId))issues.push('INVALID_BLOCK:'+b.id);
 for(const n of d.nodes)if(!n.logicalId||!n.versionId||!revs.has(n.revisionId))issues.push('NODE_IDENTITY:'+n.id);
 for(const e of d.edges)if(!nodes.has(e.from)||!nodes.has(e.to)||!d.assertions.some(a=>a.id===e.id&&a.from===e.from&&a.to===e.to))issues.push('EDGE_TARGET:'+e.id);
 for(const a of d.assertions){
  if(!nodes.has(a.from)||!nodes.has(a.to))issues.push('MISSING_TARGET:'+a.id);
  if(!statuses.has(a.status)||!revs.has(a.revisionId)||!a.assertedBy||!Array.isArray(a.evidenceRefs)||!Array.isArray(a.counterevidenceRefs))issues.push('INVALID_ASSERTION:'+a.id);
  if(a.status==='EXPLICIT_OFFICIAL'){
   const r=revs.get(a.revisionId);
   if(!a.reviewedBy||a.reviewStatus!=='APPROVED'||!a.evidenceRefs?.length||r?.classification==='SYNTHETIC'||nodes.get(a.from)?.status==='SYNTHETIC'||nodes.get(a.to)?.status==='SYNTHETIC')issues.push('OFFICIAL_WITHOUT_EVIDENCE:'+a.id);
   for(const e of Array.isArray(a.evidenceRefs)?a.evidenceRefs:[])if(!e||sources.get(e.sourceId)?.verification!=='VERIFIED'||!e.locator||e.revisionId!==a.revisionId)issues.push('UNVERIFIED_ANCHOR:'+a.id);
  }
 }
 return issues.concat(validateContent(d),domain?domain.validate(d):d.domain?['DOMAIN_VERIFIER_REQUIRED']:[]);
}
function paths(d,from,to,{includeCandidates=false,maxDepth=8,limit=10}={}){
 if(!Number.isInteger(maxDepth)||maxDepth<1||maxDepth>20||!Number.isInteger(limit)||limit<1||limit>100)throw Error('BOUNDS_REQUIRED');
 const results=[];function visit(id,visited,path){if(results.length>=limit)return;if(id===to){results.push(path);return;}if(path.length>=maxDepth)return;
 for(const a of d.assertions){if(a.from!==id||visited.has(a.to)||['CONTRADICTED','SUPERSEDED','UNKNOWN'].includes(a.status)||(!includeCandidates&&['HYPOTHESIS_ONLY','RESEARCH_INFERRED'].includes(a.status)))continue;visit(a.to,new Set([...visited,a.to]),[...path,a.id]);}}
 visit(from,new Set([from]),[]);return results;
}
async function verifyEvents(events){let previous=null;const ids=new Set();for(let i=0;i<events.length;i++){const {digest:hash,...payload}=events[i];if(ids.has(payload.id)||payload.sequence!==i||payload.previousDigest!==previous||await objectDigest(payload)!==hash)return false;ids.add(payload.id);previous=hash;}return true;}
async function appendEvent(events,event){
 if(!await verifyEvents(events))throw Error('INVALID_HISTORY');
 if(!event.id||!event.objectId||!event.actor||!event.reason||!event.observedAt||!['ADD','REVIEW','CONTEST','RETRACT','SUPERSEDE'].includes(event.type))throw Error('INVALID_EVENT');
 if(events.some(e=>e.id===event.id))throw Error('DUPLICATE_EVENT');
 const payload={id:event.id,type:event.type,objectId:event.objectId,actor:event.actor,reason:event.reason,observedAt:event.observedAt,sequence:events.length,previousDigest:events.at(-1)?.digest??null};
 return [...events,Object.freeze({...payload,digest:await objectDigest(payload)})];
}
const contentKinds=new Set(['TOPIC','DOCUMENT','SECTION','CLAUSE','ACTION','INDICATOR','EVIDENCE','QUESTION']);
function contentIndex(d){
 const items=new Map(),children=new Map();
 for(const c of d.contentItems||[]){items.set(c.id,c);if(!children.has(c.parentId))children.set(c.parentId,[]);children.get(c.parentId).push(c);}
 return {items,children};
}
function validateContent(d){
 if(d.contentItems===undefined)return [];
 if(!Array.isArray(d.contentItems))return ['CONTENT_ARRAY_REQUIRED'];
 if(d.contentItems.length>100000)return ['CONTENT_LIMIT'];
 const issues=[],items=new Map(),versions=new Set(),owners=new Set(d.nodes.map(n=>n.id)),observations=new Map((d.sourceObservations||[]).map(o=>[o.id,o]));
 for(const item of d.contentItems){
  if(!item||typeof item!=='object'||typeof item.id!=='string'||!item.id||items.has(item.id)){issues.push('CONTENT_ID');continue;}
  items.set(item.id,item);
  if(!item.logicalId||!item.versionId||versions.has(item.versionId)||!contentKinds.has(item.kind)||typeof item.title!=='string'||!item.title||typeof item.text!=='string'||!['SYNTHETIC','METADATA_OBSERVED','PUBLIC_TEXT_OBSERVED'].includes(item.status))issues.push('CONTENT_FIELDS:'+item.id);
  versions.add(item.versionId);
  if(item.status==='SYNTHETIC'){
   if(!owners.has(item.ownerNodeId)||!d.revisions.some(r=>r.id===item.revisionId&&r.classification==='SYNTHETIC')||item.observationId!==null)issues.push('CONTENT_SCOPE:'+item.id);
  }else if(item.ownerNodeId!==null||item.revisionId!==null||observations.get(item.observationId)?.status!==item.status)issues.push('CONTENT_OBSERVATION:'+item.id);
 }
 const visited=new Set();
 for(const item of items.values()){
  if(item.parentId!==null){const p=items.get(item.parentId);if(!p||p.ownerNodeId!==item.ownerNodeId||p.revisionId!==item.revisionId||p.observationId!==item.observationId||p.status!==item.status)issues.push('CONTENT_PARENT:'+item.id);}
  if(visited.has(item.id))continue;
  let cursor=item;const path=new Set();
  while(cursor&&!visited.has(cursor.id)){if(path.has(cursor.id)){issues.push('CONTENT_CYCLE:'+item.id);break;}path.add(cursor.id);cursor=items.get(cursor.parentId);}
  for(const id of path)visited.add(id);
 }
 return issues;
}
function contentTrail(d,id){
 const {items}=contentIndex(d),trail=[],seen=new Set();let item=items.get(id);
 while(item){if(seen.has(item.id))throw Error('CONTENT_CYCLE');seen.add(item.id);trail.push(item);item=items.get(item.parentId);}return trail.reverse();
}
function contentChildren(d,id){return contentIndex(d).children.get(id)||[];}
function contentPage(d,id,{offset=0,limit=50,query=''}={}){
 if(!Number.isInteger(offset)||offset<0||!Number.isInteger(limit)||limit<1||limit>200||typeof query!=='string')throw Error('CONTENT_PAGE_BOUNDS');
 const {items,children}=contentIndex(d);if(!items.has(id))throw Error('CONTENT_NOT_FOUND');
 const queue=[id],matches=[],seen=new Set();let total=0;
 for(let i=0;i<queue.length;i++){
  const next=queue[i];if(seen.has(next))throw Error('CONTENT_CYCLE');seen.add(next);const item=items.get(next);
  if((item.title+' '+item.text).toLowerCase().includes(query.toLowerCase())){if(total>=offset&&matches.length<limit)matches.push(item);total++;}
  for(const child of children.get(next)||[])queue.push(child.id);
 }
 return {items:matches,total,offset,nextOffset:offset+matches.length<total?offset+matches.length:null};
}
async function contentReceipt(d,id){
 const errors=validateContent(d);if(errors.length)throw Error(errors.join(';'));
 const {items,children}=contentIndex(d),root=items.get(id);if(!root)throw Error('CONTENT_NOT_FOUND');
 const order=[{id,depth:0}],receipts=new Map();let maxDepth=0;
 for(let i=0;i<order.length;i++){const entry=order[i];maxDepth=Math.max(maxDepth,entry.depth);for(const c of children.get(entry.id)||[])order.push({id:c.id,depth:entry.depth+1});}
 for(let i=order.length-1;i>=0;i--){const item=items.get(order[i].id),childReceipts=(children.get(item.id)||[]).slice().sort((a,b)=>a.id<b.id?-1:a.id>b.id?1:0).map(c=>receipts.get(c.id));
  receipts.set(item.id,{id:item.id,versionId:item.versionId,itemDigest:await objectDigest(item),subtreeDigest:await objectDigest({item,children:childReceipts.map(c=>({id:c.id,digest:c.subtreeDigest}))}),children:childReceipts});
 }
 const result=receipts.get(id);if(maxDepth<=128)return result;
 // Flat transport prevents JSON/canonical stack overflow; node hashes are unchanged.
 return {format:'atlas-content-receipt-flat-2',id,versionId:root.versionId,itemDigest:result.itemDigest,subtreeDigest:result.subtreeDigest,records:[...receipts.values()].sort((a,b)=>a.id<b.id?-1:a.id>b.id?1:0).map(r=>({...r,children:r.children.map(c=>({id:c.id,digest:c.subtreeDigest}))}))};
}
function layoutContent(d,rootId,{expanded=new Set(),limit=200}={}){
 if(!Number.isInteger(limit)||limit<1||limit>500)throw Error('LAYOUT_BOUNDS');
 if(validateContent(d).length)throw Error('INVALID_CONTENT');
 const {items,children}=contentIndex(d),root=items.get(rootId);if(!root)return {nodes:[],edges:[],truncated:false};
 const positions=new Map(),allQueue=[{item:root,depth:0}],rows=new Map();
 for(let i=0;i<allQueue.length;i++){const {item,depth}=allQueue[i],row=rows.get(depth)||0;rows.set(depth,row+1);positions.set(item.id,{x:45+depth*270,y:70+row*100});for(const child of children.get(item.id)||[])allQueue.push({item:child,depth:depth+1});}
 const result=[],edges=[],queue=[root];let i=0;
 while(i<queue.length&&result.length<limit){const item=queue[i++];result.push({...item,...positions.get(item.id)});if(expanded.has(item.id))for(const child of children.get(item.id)||[]){queue.push(child);edges.push({from:item.id,to:child.id});}}
 const ids=new Set(result.map(n=>n.id));return {nodes:result,edges:edges.filter(e=>ids.has(e.from)&&ids.has(e.to)),truncated:i<queue.length};
}
function densityFixture(d,count,{shape='branching'}={}){
 if(!['branching','chain'].includes(shape))throw Error('DENSITY_SHAPE');
 if(![60,200,1000,10000].includes(count))throw Error('DENSITY_BOUNDS');
 const copy=structuredClone(d);delete copy.domain;
 for(let i=0;i<count;i++)copy.contentItems.push({id:'density:'+i,logicalId:'density:'+i,versionId:'density:'+i+':v1',revisionId:'synthetic-v1',ownerNodeId:'csp',parentId:i===0?null:'density:'+(shape==='chain'?i-1:Math.floor((i-1)/3)),kind:i===0?'TOPIC':'SECTION',title:i===0?'Synthetic density fixture':('Demo item '+i),text:'Generated synthetic layout fixture only. Not a Council document or an evidence claim.',status:'SYNTHETIC',observationId:null});
 return copy;
}
function discover(d){
 return d.hypotheses.map(h=>({id:h.id,status:h.status,ruleVersion:h.ruleVersion,explanation:h.explanation,counterevidence:h.counterevidence,
  paths:h.assertionIds.map(id=>{const a=d.assertions.find(a=>a.id===id);return {assertionId:id,from:a?.from,to:a?.to,status:a?.status??'UNKNOWN',evidenceRefs:a?.evidenceRefs??[],counterevidenceRefs:a?.counterevidenceRefs??[]};}),
  conclusion:'REQUIRES_REVIEW'}));
}
function findCrossPaths(d,{rootIds=['csp','lsps'],includeCandidates=true,limit=10}={}){
 if(!Array.isArray(rootIds)||rootIds.length<2||rootIds.length>5||!Number.isInteger(limit)||limit<1||limit>100)throw Error('DISCOVERY_BOUNDS');
 const roots=[...new Set(rootIds)];if(roots.some(id=>!d.nodes.some(n=>n.id===id)))throw Error('DISCOVERY_ROOT');
 const results=[];
 for(const target of d.nodes){
  const branches=roots.map(rootId=>({rootId,paths:paths(d,rootId,target.id,{includeCandidates,maxDepth:8,limit:5})})).filter(b=>b.paths.length);
  if(branches.length<2)continue;
  const ids=new Set(branches.flatMap(b=>b.paths.flat()));const assertions=d.assertions.filter(a=>ids.has(a.id));
  results.push({id:'convergence:'+target.id,targetId:target.id,status:'HYPOTHESIS_ONLY',ruleVersion:'bounded-cross-root-convergence-v1',branches,evidenceCount:assertions.reduce((n,a)=>n+a.evidenceRefs.length,0),explanation:'Distinct starting paths converge on this target. Structural convergence alone does not establish a valid policy relationship.',questions:['Do both paths refer to the same revision, geography and effective period?','Is there an explicit exception or conflicting source?','Does primary evidence establish each proposed relationship?']});
  if(results.length>=limit)break;
 }
 return results;
}
async function auditSnapshot(d){
 const issues=validate(d),historyValid=await verifyEvents(d.events)&&(!d.domain||await domain.verify(d,api));
 return {schemaVersion:'atlas-audit-1',datasetDigest:await objectDigest(d),historyHead:d.events.at(-1)?.digest??null,historyValid,issues,
 warning:'Digest verifies supplied content only; no independent witness, signature or semantic truth.'};
}
async function exportSnapshot(d){
 const audit=await auditSnapshot(d);if(audit.issues.length||!audit.historyValid)throw Error('INVALID_DATA');
 const roots=await Promise.all((d.contentItems||[]).filter(c=>c.parentId===null).sort((a,b)=>a.id<b.id?-1:a.id>b.id?1:0).map(c=>contentReceipt(d,c.id)));
 return {format:'atlas-public-snapshot-1',dataset:d,audit,contentRoots:roots};
}
async function verifySnapshot(bundle,expectedDigest=null){
 if(!bundle||bundle.format!=='atlas-public-snapshot-1'||!bundle.dataset||!bundle.audit||!Array.isArray(bundle.contentRoots))return false;
 try{const recomputed=await exportSnapshot(bundle.dataset);return (!expectedDigest||recomputed.audit.datasetDigest===expectedDigest)&&canonical(recomputed.audit)===canonical(bundle.audit)&&canonical(recomputed.contentRoots)===canonical(bundle.contentRoots);}catch{return false;}
}
const api={registerScenario:(d,options)=>domain.registerScenario(d,api,options),appendCalculation:(d,receipt)=>domain.appendCalculation(d,api,receipt),contentIndex,contentPage,legacyBase:d=>domain.legacyBase(d),migrateDataset:(d,cases,catalogue)=>domain.migrateDataset(d,cases,api,catalogue),domainIndex:d=>domain.index(d),domainForStation:domain.forStation,queryRelationships:domain.relationships,commitDomainRevision:(d,options)=>domain.commitRevision(d,api,options),findCrossPaths,exportSnapshot,verifySnapshot,densityFixture,validateContent,contentTrail,contentChildren,contentReceipt,layoutContent,sha256,discover,auditSnapshot,canonical,digest,objectDigest,validate,applicability,paths,appendEvent,verifyEvents};root.AtlasModel=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
